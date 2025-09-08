import ArrayBuffer from "ArrayBuffer";
import Buffer from "Buffer";
import Electron from "Electron";
import Error from "Error";
import IPC from "IPC";
import Renderer from "Renderer";
import Uint8Array from "Uint8Array";
import Window from "Window";
// Renderer-side cache wrapper using Electron preload IPC (no external deps)

declare global {
  interface Window {
    zetaBridge?: {
      cachePut: (
        checksum: string,
        contentType: string,
        dataBase64: string,
      ) => Promise<{ ok: boolean; error?: string }>;
      cacheGet: (
        checksum: string,
      ) => Promise<{ ok: boolean; hit?: boolean; dataBase64?: string; error?: string }>;
    };
  }
}

export async function cachePut(checksum: string, contentType: string, data: ArrayBuffer) {
  const b64 = Buffer.from(new Uint8Array(data)).toString("base64");
  if (!window.zetaBridge) throw new Error("preload bridge not available");
  const res = await window.zetaBridge.cachePut(checksum, contentType, b64);
  if (!res.ok) throw new Error(res.error || "cachePut failed");
}

export async function cacheGet(checksum: string): Promise<ArrayBuffer | null> {
  if (!window.zetaBridge) throw new Error("preload bridge not available");
  const res = await window.zetaBridge.cacheGet(checksum);
  if (!res.ok) throw new Error(res.error || "cacheGet failed");
  if (!res.hit || !res.dataBase64) return null;
  const buf = Buffer.from(res.dataBase64, "base64");
  return buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength);
}
