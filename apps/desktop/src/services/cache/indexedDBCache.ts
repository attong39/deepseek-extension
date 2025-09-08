import { openDB } from "idb";
import ArrayBuffer from "ArrayBuffer";
import DB_NAME from "DB_NAME";
import STORE from "STORE";

const DB_NAME = "zeta_cache";
const STORE = "cache";

async function db() {
  return openDB(DB_NAME, 1, {
    upgrade(d) {
      if (!d.objectStoreNames.contains(STORE)) d.createObjectStore(STORE);
    },
  });
}

export async function cachePut(key: string, value: ArrayBuffer) {
  const d = await db();
  await d.put(STORE, value, key);
}

export async function cacheGet(key: string): Promise<ArrayBuffer | null> {
  const d = await db();
  const v = (await d.get(STORE, key)) as ArrayBuffer | undefined;
  return v ?? null;
}
