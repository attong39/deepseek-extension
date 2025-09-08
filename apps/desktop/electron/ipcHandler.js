let PANIC_MODE = false;
import { BrowserWindow } from "electron";
import { spawn } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
// whisper runtime state and fanout moved to electron/whisperManager.js

function isPathInTmp(p) {
  const tmp = os.tmpdir();
  const abs = path.resolve(p);
  return abs.toLowerCase().startsWith(path.resolve(tmp).toLowerCase());
}

function spawnJson(py, args, timeoutMs) {
  return new Promise((resolve) => {
    const child = spawn(py, args, { stdio: ["ignore", "pipe", "pipe"] });
    let out = "";
    let err = "";
    const killTimer = setTimeout(
      () => {
        try {
          child.kill("SIGKILL");
        } catch {}
      },
      Math.max(1000, timeoutMs || 30000),
    );
    child.stdout.on("data", (d) => (out += d.toString()));
    child.stderr.on("data", (d) => (err += d.toString()));
    child.on("close", () => {
      clearTimeout(killTimer);
      try {
        resolve(JSON.parse(out.trim()));
      } catch {
        resolve({ ok: false, error: err || "Process failed" });
      }
    });
  });
}

async function runPaddleOCRCLI(imageAbsPath, lang) {
  const tool = path.resolve(path.join(process.cwd(), "..", "tools", "paddle_ocr_cli.py"));
  if (!fs.existsSync(tool)) return { ok: false, error: "paddle_ocr_cli.py not found" };
  const py = process.env.ZETA_PYTHON || "python";
  const args = [tool, "--image", imageAbsPath, "--lang", String(lang || "vi"), "--json"];
  // simple retry x2
  let last;
  for (let i = 0; i < 2; i++) {
    // eslint-disable-next-line no-await-in-loop
    const res = await spawnJson(py, args, 30000);
    if (res && res.ok) return res;
    last = res;
    // eslint-disable-next-line no-await-in-loop
    await new Promise((r) => setTimeout(r, 500));
  }
  return last || { ok: false, error: "OCR failed" };
}

export function registerIpcHandlers(ipcMain, opts = {}) {
  ipcMain.handle("zeta:ping", async () => ({ pong: Date.now() }));
  // Simple cache IPC handlers (main process storage - SQLite preferred)
  let sqliteDb = null;
  try {
    // eslint-disable-next-line global-require, @typescript-eslint/no-var-requires
    const BetterSqlite3 = require("better-sqlite3");
    const os = require("os");
    const path = require("path");
    const fs = require("fs");
    const dir = path.join(os.homedir(), ".zeta");
    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
    const dbPath = path.join(dir, "cache.db");
    sqliteDb = new BetterSqlite3(dbPath);
    // add lastAccess for LRU and ensure index
    sqliteDb.exec(
      "CREATE TABLE IF NOT EXISTS cache (key TEXT PRIMARY KEY, value TEXT, createdAt INTEGER, ttlSeconds INTEGER, lastAccess INTEGER, size INTEGER); CREATE INDEX IF NOT EXISTS idx_cache_lastAccess ON cache(lastAccess);",
    );

    // housekeeping parameters
    const MAX_ENTRIES = Number(process.env.ZETA_CACHE_MAX_ENTRIES) || 1000;
    const MAX_BYTES = Number(process.env.ZETA_CACHE_MAX_BYTES) || 50 * 1024 * 1024; // default 50MB
    const PURGE_INTERVAL_MS = Number(process.env.ZETA_CACHE_PURGE_INTERVAL_MS) || 60_000;

    function purgeExpired() {
      try {
        const now = Date.now();
        // delete rows where createdAt + ttlSeconds*1000 < now
        sqliteDb
          .prepare(
            "DELETE FROM cache WHERE ttlSeconds IS NOT NULL AND (createdAt + ttlSeconds*1000) < ?",
          )
          .run(now);
      } catch (err) {
        // eslint-disable-next-line no-console
        console.debug("purgeExpired error", err);
      }
    }

    // helper to update Prometheus gauges (hoisted so linter sees usage)
    // eslint-disable-next-line no-unused-vars
    function updateMetrics() {
      try {
        if (!promGauges || !sqliteDb) return;
        const row = sqliteDb.prepare("SELECT COUNT(*) as c, SUM(size) as total FROM cache").get();
        const count = row && row.c ? row.c : 0;
        const total = row && row.total ? row.total : 0;
        promGauges.entries.set(count);
        promGauges.bytes.set(total);
      } catch (e) {
        // eslint-disable-next-line no-console
        console.debug("updateMetrics error", e);
      }
    }

    // eslint-disable-next-line no-unused-vars
    function safeInc(name) {
      if (!promGauges) return;
      try {
        const c = promGauges[name];
        if (c && typeof c.inc === "function") c.inc(1);
      } catch (err) {
        // eslint-disable-next-line no-console
        console.debug(`safeInc ${name} failed`, err);
      }
    }

    // eslint-disable-next-line no-unused-vars
    function safeUpdateMetrics() {
      if (!promGauges) return;
      try {
        updateMetrics();
      } catch (err) {
        // eslint-disable-next-line no-console
        console.debug("safeUpdateMetrics failed", err);
      }
    }

    function enforceMaxEntries() {
      try {
        const row = sqliteDb.prepare("SELECT COUNT(*) as c FROM cache").get();
        const cnt = row && row.c ? row.c : 0;
        if (cnt > MAX_ENTRIES) {
          const toDelete = cnt - MAX_ENTRIES;
          sqliteDb
            .prepare(
              "DELETE FROM cache WHERE key IN (SELECT key FROM cache ORDER BY lastAccess ASC NULLS FIRST LIMIT ?)",
            )
            .run(toDelete);
        }
        try {
          // enforce max bytes by evicting oldest lastAccess rows until under limit
          const totalRow = sqliteDb.prepare("SELECT SUM(size) as total FROM cache").get();
          const total = totalRow && totalRow.total ? totalRow.total : 0;
          if (total > MAX_BYTES) {
            evictByBytes(total - MAX_BYTES);
          }
        } catch (err) {
          // eslint-disable-next-line no-console
          console.debug("enforceMaxEntries eviction error", err);
        }
      } catch (err) {
        // eslint-disable-next-line no-console
        console.debug("enforceMaxEntries error", err);
      }
    }

    function evictByBytes(bytesToFree) {
      try {
        let remaining = bytesToFree;
        while (remaining > 0) {
          const victim = sqliteDb
            .prepare("SELECT key, size FROM cache ORDER BY lastAccess ASC NULLS FIRST LIMIT 1")
            .get();
          if (!victim) break;
          sqliteDb.prepare("DELETE FROM cache WHERE key = ?").run(victim.key);
          remaining -= victim.size || 0;
          if (promGauges) {
            promGauges.evictions.inc(1);
            updateMetrics();
          }
        }
      } catch (e) {
        // eslint-disable-next-line no-console
        console.debug("evictByBytes error", e);
      }
    }
    // optional Prometheus metrics
    let promRegistry = null;
    let promGauges = null;
    try {
      // allow injecting a mock prom-client via opts for tests
      // eslint-disable-next-line @typescript-eslint/no-var-requires
      const client = opts?.promClientMock || require("prom-client");
      promRegistry = client.register;
      const Gauge = client.Gauge;
      const Counter = client.Counter;
      promGauges = {};
      promGauges.entries = new Gauge({
        name: "zeta_cache_entries",
        help: "Number of cache entries",
      });
      promGauges.bytes = new Gauge({
        name: "zeta_cache_total_bytes",
        help: "Total cache bytes",
      });
      promGauges.evictions = new Counter({
        name: "zeta_cache_evictions_total",
        help: "Total evictions performed",
      });
      promGauges.hits = new Counter({
        name: "zeta_cache_hits_total",
        help: "Cache hits total",
      });
      promGauges.misses = new Counter({
        name: "zeta_cache_misses_total",
        help: "Cache misses total",
      });
      // expose simple http server for metrics
      const http = require("http");
      const METRICS_PORT = Number(process.env.ZETA_CACHE_METRICS_PORT) || 9126;
      const METRICS_BIND_ADDR = process.env.ZETA_CACHE_METRICS_BIND_ADDR || "127.0.0.1";
      const metricsServer = http.createServer(async (req, res) => {
        if (req.url === "/metrics") {
          try {
            const metrics = await promRegistry.metrics();
            res.writeHead(200, { "Content-Type": promRegistry.contentType });
            res.end(metrics);
          } catch (e) {
            res.writeHead(500);
            res.end(String(e));
          }
        } else {
          res.writeHead(404);
          res.end("not found");
        }
      });
      try {
        metricsServer.listen(METRICS_PORT, METRICS_BIND_ADDR);
        metricsServer.on("listening", () => {
          // eslint-disable-next-line no-console
          console.debug(`metrics server listening on ${METRICS_BIND_ADDR}:${METRICS_PORT}`);
        });
        metricsServer.on("error", (err) => {
          // eslint-disable-next-line no-console
          console.debug("metrics server listen error", err);
        });
        // expose server handle to caller for tests or graceful shutdown
        try {
          if (
            opts &&
            typeof opts === "object" &&
            opts.metricsServerRef &&
            typeof opts.metricsServerRef === "object"
          ) {
            opts.metricsServerRef.server = metricsServer;
          }
          try {
            if (
              globalThis &&
              globalThis.__ZETA_METRICS_SERVERS__ &&
              Array.isArray(globalThis.__ZETA_METRICS_SERVERS__)
            ) {
              globalThis.__ZETA_METRICS_SERVERS__.push(metricsServer);
            }
          } catch {}
        } catch {}
      } catch (err) {
        // eslint-disable-next-line no-console
        console.debug("metrics server failed to start", err);
      }
      // metrics server established; will use hoisted updateMetrics helper
    } catch (e) {
      // prom-client not available — metrics disabled
      // eslint-disable-next-line no-console
      console.debug("prom-client not available, metrics disabled", e?.message || e);
    }

    // periodic housekeeping
    setInterval(() => {
      purgeExpired();
      enforceMaxEntries();
      if (promGauges)
        try {
          updateMetrics();
        } catch {}
    }, PURGE_INTERVAL_MS);
  } catch (e) {
    // sqlite not available; we'll fallback to a simple JSON file in tmp
    // eslint-disable-next-line no-console
    console.debug("better-sqlite3 not available for cache IPC:", e?.message || e);
    sqliteDb = null;
  }

  ipcMain.handle("zeta:cache:get", async (_event, key) => {
    try {
      if (!key) return { ok: false, error: "key required" };
      if (sqliteDb) {
        return await handleGetSqlite(key);
      }
      return await handleGetFallback(key);
    } catch (e) {
      return { ok: false, error: e?.message || String(e) };
    }
  });

  async function handleGetSqlite(key) {
    const row = sqliteDb
      .prepare("SELECT value, createdAt, ttlSeconds FROM cache WHERE key = ?")
      .get(key);
    if (!row) {
      safeInc("misses");
      safeUpdateMetrics();
      return { ok: true, found: false };
    }

    const { value, createdAt, ttlSeconds } = row;
    if (ttlSeconds && Date.now() - createdAt > ttlSeconds * 1000) {
      try {
        sqliteDb.prepare("DELETE FROM cache WHERE key = ?").run(key);
      } catch (err) {
        console.debug("delete expired cache failed", err);
      }
      safeInc("misses");
      safeUpdateMetrics();
      return { ok: true, found: false };
    }

    // update lastAccess
    try {
      sqliteDb.prepare("UPDATE cache SET lastAccess = ? WHERE key = ?").run(Date.now(), key);
    } catch (err) {
      // eslint-disable-next-line no-console
      console.debug("update lastAccess failed", err);
    }

    safeInc("hits");
    safeUpdateMetrics();

    return { ok: true, found: true, value: JSON.parse(value) };
  }

  async function handleGetFallback(key) {
    const tmp = os.tmpdir();
    const f = path.join(tmp, `zeta_cache_${encodeURIComponent(key)}.json`);
    if (!fs.existsSync(f)) {
      safeInc("misses");
      safeUpdateMetrics();
      return { ok: true, found: false };
    }

    const data = JSON.parse(fs.readFileSync(f, "utf8"));
    if (data.ttlSeconds && Date.now() - data.createdAt > data.ttlSeconds * 1000) {
      try {
        fs.unlinkSync(f);
      } catch (err) {
        console.debug("unlink tmp cache failed", err);
      }
      safeInc("misses");
      safeUpdateMetrics();
      return { ok: true, found: false };
    }

    safeInc("hits");
    safeUpdateMetrics();

    return { ok: true, found: true, value: data.value };
  }

  ipcMain.handle("zeta:cache:set", async (_event, key, value, ttlSeconds) => {
    try {
      if (!key) return { ok: false, error: "key required" };
      if (sqliteDb) {
        const str = JSON.stringify(value);
        const size = Buffer.byteLength(str, "utf8");
        const stmt = sqliteDb.prepare(
          "INSERT OR REPLACE INTO cache (key, value, createdAt, ttlSeconds, lastAccess, size) VALUES (?, ?, ?, ?, ?, ?)",
        );
        stmt.run(key, str, Date.now(), ttlSeconds ?? null, Date.now(), size);
        // immediate housekeeping after set
        try {
          sqliteDb
            .prepare(
              "DELETE FROM cache WHERE ttlSeconds IS NOT NULL AND (createdAt + ttlSeconds*1000) < ?",
            )
            .run(Date.now());
        } catch {}
        try {
          // run enforce by entries and bytes
          enforceMaxEntries();
        } catch {}
        if (promGauges)
          try {
            updateMetrics();
          } catch {}
        return { ok: true };
      }
      const tmp = os.tmpdir();
      const path = require("path");
      const fs = require("fs");
      const f = path.join(tmp, `zeta_cache_${encodeURIComponent(key)}.json`);
      fs.writeFileSync(f, JSON.stringify({ value, createdAt: Date.now(), ttlSeconds }));
      return { ok: true };
    } catch (e) {
      return { ok: false, error: e?.message || String(e) };
    }
  });

  ipcMain.handle("zeta:cache:delete", async (_event, key) => {
    try {
      if (!key) return { ok: false, error: "key required" };
      if (sqliteDb) {
        sqliteDb.prepare("DELETE FROM cache WHERE key = ?").run(key);
        if (promGauges)
          try {
            updateMetrics();
          } catch {}
        return { ok: true };
      }
      const tmp = os.tmpdir();
      const path = require("path");
      const fs = require("fs");
      const f = path.join(tmp, `zeta_cache_${encodeURIComponent(key)}.json`);
      if (fs.existsSync(f)) fs.unlinkSync(f);
      return { ok: true };
    } catch (e) {
      return { ok: false, error: e?.message || String(e) };
    }
  });

  ipcMain.handle("zeta:cache:clear", async () => {
    try {
      if (sqliteDb) {
        sqliteDb.prepare("DELETE FROM cache").run();
        if (promGauges)
          try {
            updateMetrics();
          } catch {}
        return { ok: true };
      }
      const tmp = os.tmpdir();
      const files = fs.readdirSync(tmp).filter((n) => n.startsWith("zeta_cache_"));
      for (const f of files) {
        try {
          fs.unlinkSync(path.join(tmp, f));
        } catch {}
      }
      return { ok: true };
    } catch (e) {
      return { ok: false, error: e?.message || String(e) };
    }
  });

  ipcMain.handle("zeta:cache:stats", async () => {
    try {
      if (sqliteDb) {
        const row = sqliteDb
          .prepare(
            "SELECT COUNT(*) as c, MIN(lastAccess) as oldest, SUM(size) as totalBytes FROM cache",
          )
          .get();
        return {
          ok: true,
          count: row.c || 0,
          oldest: row.oldest || null,
          totalBytes: row.totalBytes || 0,
        };
      }
      const tmp = os.tmpdir();
      const files = fs.readdirSync(tmp).filter((n) => n.startsWith("zeta_cache_"));
      return { ok: true, count: files.length };
    } catch (e) {
      return { ok: false, error: e?.message || String(e) };
    }
  });
  ipcMain.handle("zeta:file:writeTemp", async (_event, payload) => {
    try {
      const { bytes, suffix = ".png" } = payload || {};
      if (!bytes || !Array.isArray(bytes)) return { ok: false, error: "bytes required" };
      const tmpDir = os.tmpdir();
      const fname = `zeta_${Date.now()}_${Math.random().toString(36).slice(2)}${String(suffix)}`;
      const fpath = path.join(tmpDir, fname);
      const buf = Buffer.from(Uint8Array.from(bytes));
      fs.writeFileSync(fpath, buf);
      return { ok: true, path: fpath };
    } catch (e) {
      return { ok: false, error: e?.message || "writeTemp failed" };
    }
  });
  ipcMain.handle("zeta:input:panic", async (_event, enable) => {
    PANIC_MODE = Boolean(enable);
    return { ok: true, panic: PANIC_MODE };
  });
  ipcMain.handle("zeta:input:appShortcut", async (_event, payload) => {
    try {
      if (PANIC_MODE) return { ok: false, error: "Panic mode enabled" };
      const { appName, shortcut, confirm } = payload || {};
      if (typeof appName !== "string" || typeof shortcut !== "string") {
        throw new Error("Invalid payload");
      }
      if (!isAppAllowed(appName)) {
        throw new Error("App not allowed");
      }
      const parsed = parseShortcut(shortcut);
      if (!parsed) throw new Error("Invalid shortcut");
      if (!isShortcutAllowed(appName, parsed)) throw new Error("Shortcut not allowed");

      // Require explicit confirmation for critical combos
      if (isCriticalShortcut(parsed) && confirm !== true) {
        return { ok: false, error: "Critical action requires confirmation" };
      }

      const backend = String(process.env.ZETA_INPUT_BACKEND || "").toLowerCase();
      if (backend === "robotjs") {
        const ok = await doRobotShortcut(parsed);
        return { ok };
      }
      if (backend === "nutjs") {
        const ok = await doNutShortcut(parsed);
        return { ok };
      }
      return {
        ok: false,
        error: "No input backend enabled (set ZETA_INPUT_BACKEND=robotjs|nutjs)",
      };
    } catch (e) {
      return { ok: false, error: e?.message || "Unknown error" };
    }
  });

  // Robot exec routed to dedicated module to keep handler small.
  ipcMain.handle("robot:exec", async (_event, cmd) => {
    try {
      if (PANIC_MODE) return { ok: false, error: "Panic mode enabled" };
      const { execRobotCommand } = await import(path.join(__dirname, "robotExec.js"));
      return await execRobotCommand(cmd);
    } catch (e) {
      return { ok: false, error: e?.message || "robot exec failed" };
    }
  });

  // OCR via PaddleOCR (placeholder). Expect absolute image path; returns text if configured.
  ipcMain.handle("zeta:ocr:paddle", async (_event, payload) => {
    try {
      const { imagePath, lang } = payload || {};
      if (!imagePath || typeof imagePath !== "string")
        return { ok: false, error: "imagePath required" };
      const abs = path.resolve(imagePath);
      if (!isPathInTmp(abs)) return { ok: false, error: "imagePath not allowed" };
      return await runPaddleOCRCLI(abs, lang || "vi");
    } catch (e) {
      return { ok: false, error: e?.message || "Unknown error" };
    }
  });

  // STT whisper handling moved to whisperManager.js

  // Delegate whisper control to whisperManager
  ipcMain.handle("zeta:stt:whisper:start", async () => {
    const mgr = await import(path.join(__dirname, "whisperManager.js"));
    return mgr.startWhisper();
  });
  ipcMain.handle("zeta:stt:whisper:stop", async () => {
    const mgr = await import(path.join(__dirname, "whisperManager.js"));
    return mgr.stopWhisper();
  });
  ipcMain.handle("zeta:stt:whisper:subscribe", async () => {
    const mgr = await import(path.join(__dirname, "whisperManager.js"));
    const sender = BrowserWindow.getFocusedWindow()?.webContents;
    return mgr.subscribeWhisper(sender?.id);
  });
}

// --- Helpers ---
function isAppAllowed(name) {
  const allowed = new Set(["Photoshop", "VSCode", "Chrome", "Figma"]);
  const denied = new Set(["SystemSettings"]);
  if (denied.has(name)) return false;
  return allowed.has(name);
}

// Returns { key: 's', mods: ['control','alt'] } or null
function parseShortcut(str) {
  if (!str || typeof str !== "string") return null;
  const parts = str
    .split("+")
    .map((s) => s.trim())
    .filter(Boolean);
  if (parts.length === 0) return null;
  const norm = (s) => s.toLowerCase();
  const mods = [];
  let key = "";
  for (const p of parts) {
    const n = norm(p);
    if (["ctrl", "control"].includes(n)) mods.push("control");
    else if (["alt", "option"].includes(n)) mods.push("alt");
    else if (["shift"].includes(n)) mods.push("shift");
    else if (["cmd", "command", "meta", "super", "win"].includes(n)) mods.push("command");
    else key = p.toLowerCase();
  }
  if (!key) return null;
  return { key, mods };
}

// Optional per-app/per-shortcut ACL
function isShortcutAllowed(appName, parsed) {
  const combo = [...parsed.mods, parsed.key].join("+");
  const globalDeny = new Set(["command+q", "alt+f4"]);
  if (globalDeny.has(combo)) return false;

  // Per-app allow/deny (example policies)
  const appAllow = {
    Photoshop: new Set(["control+alt+s", "control+s"]),
    VSCode: new Set(["control+shift+p", "control+p"]),
  };
  const appDeny = {
    Photoshop: new Set(["command+q", "alt+f4"]),
    VSCode: new Set([]),
  };

  if (appDeny[appName] && appDeny[appName].has(combo)) return false;
  if (appAllow[appName]) return appAllow[appName].has(combo);
  return true;
}

function isCriticalShortcut(parsed) {
  const combo = [...parsed.mods, parsed.key].join("+");
  const critical = new Set(["command+q", "alt+f4", "control+alt+delete", "command+shift+power"]);
  return critical.has(combo);
}

async function doRobotShortcut(parsed) {
  try {
    const mod = await import("robotjs");
    const robot = mod.default || mod;
    const mods = parsed.mods.map((m) => (m === "command" ? "command" : m));
    robot.keyTap(parsed.key, mods);
    return true;
  } catch (e) {
    console.warn("robotjs keyTap failed", e);
    return false;
  }
}

async function doNutShortcut(parsed) {
  try {
    const mod = await import("@nut-tree/nut-js");
    const keyboard = mod.keyboard;
    const Key = mod.Key;
    const mapMod = (m) => {
      const modMap = {
        control: Key.LeftControl,
        alt: Key.LeftAlt,
        shift: Key.LeftShift,
        command: Key.LeftSuper,
      };
      return modMap[m] ?? Key.LeftSuper;
    };
    const modKeys = parsed.mods.map(mapMod);
    if (modKeys.length) await keyboard.pressKey(...modKeys);
    // Type single character; for special keys, extend mapping as needed.
    await keyboard.type(parsed.key);
    if (modKeys.length) await keyboard.releaseKey(...modKeys);
    return true;
  } catch (e) {
    console.warn("nut.js shortcut failed", e);
    return false;
  }
}
