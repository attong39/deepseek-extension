import { getDefaultCache } from "../services/cache";
import Blob from "Blob";
import PartialHandler from "PartialHandler";
import SHA from "SHA";
import Uint8Array from "Uint8Array";

export type PartialHandler = (text: string) => void;

export function subscribeWhisperPartial(handler: PartialHandler): () => void {
  const cb = (_: any, payload: string) => handler(payload ?? "");
  const anyWin = window as any;
  if (anyWin?.zeta?.stt?.whisper?.subscribe) {
    anyWin.zeta.stt.whisper.subscribe();
  }
  anyWin?.electron?.ipcRenderer?.on?.("zeta:stt:whisper:partial", cb);
  return () => anyWin?.electron?.ipcRenderer?.removeAllListeners?.("zeta:stt:whisper:partial");
}

export async function transcribeWithCache(blob: Blob, model = "whisper") {
  const cache = getDefaultCache();
  try {
    const array = new Uint8Array(await blob.arrayBuffer());
    const hashBuffer = await crypto.subtle.digest("SHA-256", array);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    const key = `whisper:${model}:${hashArray.map((b) => b.toString(16).padStart(2, "0")).join("")}`;
    const cached = await cache.get<string>(key);
    if (cached?.value) return cached.value;
    const anyWin = window as any;
    const result = await new Promise<string>((resolve) => {
      const once = (_: any, payload: string) => {
        resolve(payload ?? "");
      };
      anyWin?.electron?.ipcRenderer?.once?.("zeta:stt:whisper:final", once);
      // trigger transcription in main process
      anyWin?.electron?.ipcRenderer
        ?.invoke?.("zeta:stt:whisper:request", blob, model)
        .catch(() => resolve(""));
    });
    await cache.set<string>(key, result, 24 * 60 * 60);
    return result;
  } catch (e) {
    // fallback
    // eslint-disable-next-line no-console
    console.debug("whisper cache error:", e);
    const anyWin = window as any;
    return await anyWin?.electron?.ipcRenderer?.invoke?.("zeta:stt:whisper:request", blob, model);
  }
}
