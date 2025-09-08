import { app, BrowserWindow, ipcMain } from "electron";
import fs from "node:fs";
import path from "node:path";
import Buffer from "Buffer";
import Settings from "../src/pages/Settings";
import Simple from "Simple";
// electron-updater lazy import to avoid breaking dev when module missing
let autoUpdater: any = null;
try {
  // eslint-disable-next-line global-require
  autoUpdater = require("electron-updater").autoUpdater;
} catch {
  autoUpdater = null;
}

let win: BrowserWindow | null = null;
const createWin = () => {
  win = new BrowserWindow({
    width: 1200,
    height: 800,
    show: false,
    webPreferences: {
      preload: path.join(__dirname, "preload.js"),
      contextIsolation: true,
      nodeIntegration: false,
    },
  });
  win.loadFile("index.html");
  win.once("ready-to-show", () => win?.show());
};

app.whenReady().then(() => {
  createWin();
  // Settings file path
  const settingsPath = path.join(app.getPath("userData"), "settings.json");
  const readSettings = () => {
    try {
      if (fs.existsSync(settingsPath)) {
        const txt = fs.readFileSync(settingsPath, "utf8");
        return JSON.parse(txt || "{}");
      }
    } catch {
      /* noop */
    }
    return {};
  };
  const writeSettings = (obj: any) => {
    try {
      fs.mkdirSync(path.dirname(settingsPath), { recursive: true });
      fs.writeFileSync(settingsPath, JSON.stringify(obj, null, 2), "utf8");
    } catch {
      /* noop */
    }
  };

  ipcMain.handle("zeta:settings:getLang", async () => {
    const s = readSettings();
    return s.lang || "vi";
  });

  ipcMain.handle("zeta:settings:setLang", async (_e, { lang }) => {
    const s = readSettings();
    s.lang = lang;
    writeSettings(s);
    return { ok: true };
  });

  ipcMain.handle("zeta:settings:get", async (_e, { key }) => {
    const s = readSettings();
    return s[key];
  });

  ipcMain.handle("zeta:settings:set", async (_e, { key, value }) => {
    const s = readSettings();
    s[key] = value;
    writeSettings(s);
    return { ok: true };
  });

  ipcMain.handle("zeta:settings:getAll", async () => {
    return readSettings();
  });

  // Simple file-based cache (no native deps) keyed by checksum
  const cacheDir = path.join(app.getPath("userData"), "cache");
  const dataPathFor = (checksum: string) => path.join(cacheDir, `${checksum}.bin`);
  const metaPathFor = (checksum: string) => path.join(cacheDir, `${checksum}.json`);

  ipcMain.handle("zeta:cache:put", async (_e, { checksum, contentType, dataBase64 }) => {
    try {
      if (
        typeof checksum !== "string" ||
        typeof contentType !== "string" ||
        typeof dataBase64 !== "string"
      ) {
        return { ok: false, error: "invalid args" };
      }
      fs.mkdirSync(cacheDir, { recursive: true });
      const buf = Buffer.from(dataBase64, "base64");
      fs.writeFileSync(dataPathFor(checksum), buf);
      fs.writeFileSync(
        metaPathFor(checksum),
        JSON.stringify({ checksum, contentType, size: buf.length, createdAt: Date.now() }, null, 2),
        "utf8",
      );
      return { ok: true };
    } catch (e: any) {
      return { ok: false, error: String((e && e.message) || e) };
    }
  });

  ipcMain.handle("zeta:cache:get", async (_e, { checksum }) => {
    try {
      if (typeof checksum !== "string") return { ok: false, error: "invalid args" };
      const p = dataPathFor(checksum);
      if (!fs.existsSync(p)) return { ok: true, hit: false };
      const buf = fs.readFileSync(p);
      return { ok: true, hit: true, dataBase64: buf.toString("base64") };
    } catch (e: any) {
      return { ok: false, error: String((e && e.message) || e) };
    }
  });
  if (autoUpdater) {
    try {
      autoUpdater.autoDownload = true;
      autoUpdater.on("update-available", (info: any) => {
        if (BrowserWindow.getAllWindows().length) {
          BrowserWindow.getAllWindows()[0].webContents.send("zeta:update:available", info);
        }
      });
      autoUpdater.on("update-downloaded", (info: any) => {
        if (BrowserWindow.getAllWindows().length) {
          BrowserWindow.getAllWindows()[0].webContents.send("zeta:update:downloaded", info);
        }
      });
      autoUpdater.on("download-progress", (progress: any) => {
        if (BrowserWindow.getAllWindows().length) {
          BrowserWindow.getAllWindows()[0].webContents.send("zeta:update:progress", progress);
        }
      });
      // allow renderer to trigger install
      ipcMain.handle("zeta:update:install", async () => {
        try {
          autoUpdater.quitAndInstall();
          return { ok: true };
        } catch (e: any) {
          return { ok: false, error: String((e && e.message) || e) };
        }
      });
      // check for updates on start
      try {
        autoUpdater.checkForUpdatesAndNotify();
      } catch {}
    } catch {
      // ignore updater errors
    }
  }
});

app.on("window-all-closed", () => app.quit());
