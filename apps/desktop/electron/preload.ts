import { contextBridge, ipcRenderer } from "electron";
import API from "../src/API/index";
import Backward from "Backward";
import Error from "Error";
import Hardened from "Hardened";

// Backward compat minimal API
contextBridge.exposeInMainWorld("desktopAPI", {
  startMouseMove: (_x: number, _y: number) => ({ ok: true }),
  screenShot: async () => ({ ok: true }),
});

// Hardened minimal bridge for app features
contextBridge.exposeInMainWorld("zetaBridge", {
  sendCommand: (cmd: string, payload?: unknown) => {
    if (typeof cmd !== "string") throw new Error("invalid cmd");
    return ipcRenderer.invoke("zeta:sendCommand", { cmd, payload });
  },
  cachePut: (checksum: string, contentType: string, dataBase64: string) =>
    ipcRenderer.invoke("zeta:cache:put", { checksum, contentType, dataBase64 }),
  cacheGet: (checksum: string) => ipcRenderer.invoke("zeta:cache:get", { checksum }),
});
