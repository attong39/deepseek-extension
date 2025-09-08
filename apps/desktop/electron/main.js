import { app, BrowserWindow, ipcMain } from "electron";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { registerIpcHandlers } from "./ipcHandler.js";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

/** @type {BrowserWindow | null} */
let mainWindow = null;

const createWindow = () => {
  mainWindow = new BrowserWindow({
    width: 1100,
    height: 720,
    webPreferences: {
      contextIsolation: true,
      nodeIntegration: false,
      preload: join(__dirname, "preload.js"),
    },
  });

  const isDev = process.env.NODE_ENV === "development";
  if (isDev) {
    const devUrl = "http://localhost:5173";
    const tryLoad = async () => {
      const ok = await (async () => {
        try {
          const res = await fetch(devUrl, { method: "GET" });
          return res.ok;
        } catch {
          return false;
        }
      })();
      if (ok) return mainWindow.loadURL(devUrl);
      // fallback to file if dev server not ready
      return mainWindow.loadFile(join(__dirname, "..", "dist", "index.html"));
    };
    void tryLoad();
  } else {
    mainWindow.loadFile(join(__dirname, "..", "dist", "index.html"));
  }

  mainWindow.on("closed", () => {
    mainWindow = null;
  });
  registerIpcHandlers(ipcMain);
};

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") app.quit();
});

app.whenReady().then(createWindow);

app.on("activate", () => {
  if (BrowserWindow.getAllWindows().length === 0) createWindow();
});

// Navigation/IPC hardening
app.on("web-contents-created", (_event, contents) => {
  // Block new windows
  contents.setWindowOpenHandler(() => ({ action: "deny" }));
  // Restrict navigation to our app origin only
  contents.on("will-navigate", (e, url) => {
    try {
      const allowed = ["http://localhost:5173", "file://"];
      if (!allowed.some((prefix) => url.startsWith(prefix))) {
        e.preventDefault();
      }
    } catch {
      e.preventDefault();
    }
  });
});
