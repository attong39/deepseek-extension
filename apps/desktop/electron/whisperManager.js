import { BrowserWindow } from "electron";
import { spawn } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";

let whisperProc = null;
let whisperWs = null;
const whisperSubscribers = new Set();

function isPathInTmp(p) {
  const tmp = os.tmpdir();
  const abs = path.resolve(p);
  return abs.toLowerCase().startsWith(path.resolve(tmp).toLowerCase());
}

async function httpPostJson(url, body) {
  try {
    if (typeof fetch === "function") {
      const resp = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body || {}),
      });
      const data = await resp.json();
      return { ok: resp.ok && data?.ok !== false, ...data };
    }
  } catch (e) {
    return { ok: false, error: e?.message || "HTTP error" };
  }
  return { ok: false, error: "fetch not available" };
}

function fanoutWhisperPartial(payload) {
  try {
    const wins = BrowserWindow.getAllWindows();
    for (const id of whisperSubscribers) {
      const wc = wins.find((w) => w.webContents.id === id)?.webContents;
      if (wc) wc.send("zeta:stt:whisper:partial", payload);
    }
  } catch {
    // ignore
  }
}

async function runWhisperServerIfNeeded() {
  if (!whisperProc || whisperProc.killed) {
    const script = path.resolve(path.join(process.cwd(), "..", "tools", "whisper_server.py"));
    if (!fs.existsSync(script)) return { ok: false, error: "whisper_server.py not found" };
    const py = process.env.ZETA_PYTHON || "python";
    whisperProc = spawn(py, [script], { stdio: ["ignore", "pipe", "pipe"] });
  }
  return { ok: true };
}

async function startWhisper() {
  try {
    const res = await runWhisperServerIfNeeded();
    if (!res.ok) return res;
    return await httpPostJson("http://127.0.0.1:8765/stt/start", {});
  } catch (e) {
    return { ok: false, error: e?.message || "failed to start whisper" };
  }
}

async function stopWhisper() {
  try {
    const res = await httpPostJson("http://127.0.0.1:8765/stt/stop", {});
    if (whisperWs) {
      try {
        whisperWs.close();
      } catch {}
      whisperWs = null;
    }
    if (whisperProc && !whisperProc.killed) {
      try {
        whisperProc.kill("SIGKILL");
      } catch {}
      whisperProc = null;
    }
    whisperSubscribers.clear();
    return res;
  } catch (e) {
    return { ok: false, error: e?.message || "failed to stop whisper" };
  }
}

async function subscribeWhisper(senderId) {
  try {
    if (typeof senderId === "number") whisperSubscribers.add(senderId);
    // open WS once and fanout
    if (!whisperWs) {
      let backoff = 500;
      const connect = async () => {
        try {
          const WSImpl =
            (globalThis?.WebSocket ?? null) ||
            (await import("ws")).WebSocket ||
            (await import("ws")).default;
          if (!WSImpl) throw new Error("WS impl not found");
          whisperWs = new WSImpl("ws://127.0.0.1:8765/stt/stream");
          whisperWs.onopen = () => {
            backoff = 500;
          };
          whisperWs.onmessage = (ev) => {
            const payload = typeof ev.data === "string" ? ev.data : ev.data?.toString?.();
            fanoutWhisperPartial(payload);
          };
          whisperWs.onclose = () => {
            whisperWs = null;
            setTimeout(() => void connect(), Math.min(backoff, 5000));
            backoff = Math.min(5000, backoff * 2);
          };
          whisperWs.onerror = () => {
            /* handled by close */
          };
        } catch {
          setTimeout(() => void connect(), Math.min(backoff, 5000));
          backoff = Math.min(5000, backoff * 2);
        }
      };
      void connect();
    }
    return { ok: true };
  } catch (e) {
    return { ok: false, error: e?.message || "subscribe failed" };
  }
}

export { startWhisper, stopWhisper, subscribeWhisper };
