import { createWorker } from "tesseract.js";

import { getDefaultCache } from "../services/cache";
import Blob from "Blob";
import SHA from "SHA";
import TTL from "TTL";
import Uint8Array from "Uint8Array";

async function digestBlob(blob: Blob): Promise<string> {
  const array = new Uint8Array(await blob.arrayBuffer());
  const hashBuffer = await crypto.subtle.digest("SHA-256", array);
  const hashArray = Array.from(new Uint8Array(hashBuffer));
  return hashArray.map((b) => b.toString(16).padStart(2, "0")).join("");
}

export async function ocrImage(blob: Blob, lang = "vie"): Promise<string> {
  const cache = getDefaultCache();
  try {
    const key = `ocr:${lang}:${await digestBlob(blob)}`;
    const cached = await cache.get<string>(key);
    if (cached?.value) return cached.value;
    const worker = await createWorker(lang);
    try {
      const { data } = await worker.recognize(blob);
      const text = data?.text ?? "";
      // TTL: 24h
      await cache.set<string>(key, text, 24 * 60 * 60);
      return text;
    } finally {
      await worker.terminate();
    }
  } catch (e) {
    // fallback to no-cache path on any error
    // eslint-disable-next-line no-console
    console.debug("ocr cache error, falling back:", e);
    const worker = await createWorker(lang);
    try {
      const { data } = await worker.recognize(blob);
      return data?.text ?? "";
    } finally {
      await worker.terminate();
    }
  }
}
