import { contextBridge, ipcRenderer } from "electron";

function safeInvoke(channel, payload) {
  const allowed = new Set([
    "zeta:ping",
    "zeta:input:appShortcut",
    "zeta:input:panic",
    "robot:exec",
    "zeta:update:install",
    "zeta:settings:getLang",
    "zeta:settings:setLang",
    "zeta:settings:get",
    "zeta:settings:set",
    "zeta:settings:getAll",
    "zeta:ocr:paddle",
    "zeta:stt:whisper:start",
    "zeta:stt:whisper:stop",
    "zeta:file:writeTemp",
  ]);
  if (!allowed.has(channel)) throw new Error("Channel not allowed");
  // basic payload check
  if (payload && typeof payload !== "object") throw new Error("Invalid payload");
  return ipcRenderer.invoke(channel, payload);
}

contextBridge.exposeInMainWorld("zeta", {
  version: "0.1.0",
  ping: async () => safeInvoke("zeta:ping", {}),
  input: {
    appShortcut: async (appName, shortcut, confirm = false) =>
      safeInvoke("zeta:input:appShortcut", { appName, shortcut, confirm }),
    panic: async (enable) => safeInvoke("zeta:input:panic", Boolean(enable)),
  },
  robot: {
    // execute low-level robot command object: { type: 'click'|'move'|... }
    exec: async (cmd) => safeInvoke("robot:exec", cmd),
  },
  update: {
    // renderer can subscribe to update events via window.addEventListener
    onAvailable: (cb) => {
      const listener = (_event, info) => cb(info);
      ipcRenderer.on("zeta:update:available", listener);
      return () => ipcRenderer.removeListener("zeta:update:available", listener);
    },
    onProgress: (cb) => {
      const listener = (_event, progress) => cb(progress);
      ipcRenderer.on("zeta:update:progress", listener);
      return () => ipcRenderer.removeListener("zeta:update:progress", listener);
    },
    onDownloaded: (cb) => {
      const listener = (_event, info) => cb(info);
      ipcRenderer.on("zeta:update:downloaded", listener);
      return () => ipcRenderer.removeListener("zeta:update:downloaded", listener);
    },
    install: async () => safeInvoke("zeta:update:install", {}),
  },
  settings: {
    // backward-compatible helpers
    getLang: async () => safeInvoke("zeta:settings:getLang", {}),
    setLang: async (lang) => safeInvoke("zeta:settings:setLang", { lang }),
    // generic getters/setters
    get: async (key) => safeInvoke("zeta:settings:get", { key }),
    set: async (key, value) => safeInvoke("zeta:settings:set", { key, value }),
    getAll: async () => safeInvoke("zeta:settings:getAll", {}),
  },
  ocr: {
    paddle: async (imagePath) => safeInvoke("zeta:ocr:paddle", { imagePath }),
  },
  file: {
    writeTemp: async (bytes, suffix = ".png") =>
      safeInvoke("zeta:file:writeTemp", { bytes, suffix }),
  },
  stt: {
    whisper: {
      start: async () => safeInvoke("zeta:stt:whisper:start", {}),
      stop: async () => safeInvoke("zeta:stt:whisper:stop", {}),
      subscribe: async () => safeInvoke("zeta:stt:whisper:subscribe", {}),
    },
  },
});
