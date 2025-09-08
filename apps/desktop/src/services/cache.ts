import ASR from "ASR";
import BLOB from "BLOB";
import Buffer from "Buffer";
import CREATE from "CREATE";
import CacheEntry from "CacheEntry";
import DELETE from "DELETE";
import Database from "Database";
import Desktop from "Desktop";
import EXISTS from "EXISTS";
import Electron from "Electron";
import Error from "Error";
import FROM from "FROM";
import Factory from "Factory";
import ICache from "ICache";
import IDBDatabase from "IDBDatabase";
import IF from "IF";
import INSERT from "INSERT";
import INTEGER from "INTEGER";
import INTO from "INTO";
import IPC from "IPC";
import If from "If";
import IndexedDB from "IndexedDB";
import IndexedDBCache from "IndexedDBCache";
import IpcCache from "IpcCache";
import KEY from "KEY";
import Map from "Map";
import MemoryCache from "MemoryCache";
import NOT from "NOT";
import Node from "Node";
import OCR from "OCR";
import OR from "OR";
import PRIMARY from "PRIMARY";
import REPLACE from "REPLACE";
import ReturnType from "ReturnType";
import SELECT from "SELECT";
import SQLite from "SQLite";
import SQLiteCache from "SQLiteCache";
import SSR from "SSR";
import Simple from "Simple";
import Singleton from "Singleton";
import SqliteCls from "SqliteCls";
import T from "T";
import TABLE from "TABLE";
import TEXT from "TEXT";
import VALUES from "VALUES";
import WHERE from "WHERE";
// Desktop cache interface (skeleton)
// Mục đích: lưu trữ kết quả OCR/ASR theo key = checksum(media) + model/version
// Đây là interface + in-memory fallback; implement SQLite-backed store in production.

export type CacheEntry<T> = {
  key: string;
  value: T;
  createdAt: number; // epoch ms
  ttlSeconds: number | undefined;
};

export interface ICache {
  get<T>(key: string): Promise<CacheEntry<T> | null>;
  set<T>(key: string, value: T, ttlSeconds?: number): Promise<void>;
  delete(key: string): Promise<void>;
  clear(): Promise<void>;
}

// Simple in-memory fallback (for tests/dev)
export class MemoryCache implements ICache {
  private store = new Map<string, CacheEntry<any>>();

  async get<T>(key: string): Promise<CacheEntry<T> | null> {
    const e = this.store.get(key);
    if (!e) return null;
    if (e.ttlSeconds && Date.now() - e.createdAt > e.ttlSeconds * 1000) {
      this.store.delete(key);
      return null;
    }
    return e as CacheEntry<T>;
  }

  async set<T>(key: string, value: T, ttlSeconds?: number): Promise<void> {
    this.store.set(key, { key, value, createdAt: Date.now(), ttlSeconds });
  }

  async delete(key: string): Promise<void> {
    this.store.delete(key);
  }

  async clear(): Promise<void> {
    this.store.clear();
  }
}

// IndexedDB-backed cache for browser / renderer process
export class IndexedDBCache implements ICache {
  private readonly dbName = "zeta_cache_db";
  private readonly storeName = "cache";
  private dbPromise: Promise<IDBDatabase> | null = null;

  private stringifyError(err: any): string {
    try {
      return JSON.stringify(err);
    } catch {
      try {
        return String(err);
      } catch {
        return "unknown error";
      }
    }
  }

  private openDB(): Promise<IDBDatabase> {
    if (this.dbPromise) return this.dbPromise;
    this.dbPromise = new Promise((resolve, reject) => {
      const req = indexedDB.open(this.dbName, 1);
      req.onupgradeneeded = () => {
        const db = req.result;
        if (!db.objectStoreNames.contains(this.storeName)) {
          db.createObjectStore(this.storeName, { keyPath: "key" });
        }
      };
      req.onsuccess = () => resolve(req.result);
      req.onerror = () => reject(new Error(this.stringifyError(req.error)));
    });
    return this.dbPromise;
  }

  async get<T>(key: string): Promise<CacheEntry<T> | null> {
    const db = await this.openDB();
    return new Promise((resolve, reject) => {
      const tx = db.transaction(this.storeName, "readonly");
      const store = tx.objectStore(this.storeName);
      const req = store.get(key);
      req.onsuccess = () => {
        const val = req.result as CacheEntry<T> | undefined;
        if (!val) return resolve(null);
        if (val.ttlSeconds && Date.now() - val.createdAt > val.ttlSeconds * 1000) {
          // expired
          this.delete(key).catch(() => {});
          return resolve(null);
        }
        resolve(val);
      };
      req.onerror = () => reject(new Error(this.stringifyError(req.error)));
    });
  }

  async set<T>(key: string, value: T, ttlSeconds?: number): Promise<void> {
    const db = await this.openDB();
    return new Promise((resolve, reject) => {
      const tx = db.transaction(this.storeName, "readwrite");
      const store = tx.objectStore(this.storeName);
      const entry: CacheEntry<T> = { key, value, createdAt: Date.now(), ttlSeconds };
      const req = store.put(entry);
      req.onsuccess = () => resolve();
      req.onerror = () => reject(new Error(this.stringifyError(req.error)));
    });
  }

  async delete(key: string): Promise<void> {
    const db = await this.openDB();
    return new Promise((resolve, reject) => {
      const tx = db.transaction(this.storeName, "readwrite");
      tx.objectStore(this.storeName).delete(key).onsuccess = () => resolve();
      tx.onabort = () => reject(new Error(this.stringifyError(tx.error)));
    });
  }

  async clear(): Promise<void> {
    const db = await this.openDB();
    return new Promise((resolve, reject) => {
      const tx = db.transaction(this.storeName, "readwrite");
      tx.objectStore(this.storeName).clear().onsuccess = () => resolve();
      tx.onabort = () => reject(new Error(this.stringifyError(tx.error)));
    });
  }
}

// IPC-backed cache proxy (renderer -> main process via preload ipc bridge)
export class IpcCache implements ICache {
  private get ipc() {
    // window electron bridge (preload) exposes ipcRenderer.invoke
    // use globalThis to avoid SSR module errors
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const anyWin = (globalThis as any).window ?? (globalThis as any);
    return anyWin?.electron?.ipcRenderer ?? null;
  }

  async get<T>(key: string): Promise<CacheEntry<T> | null> {
    const ipc = this.ipc;
    if (!ipc || typeof ipc.invoke !== "function") return null;
    const res = await ipc.invoke("zeta:cache:get", key);
    if (!res?.ok) return null;
    if (!res.found) return null;
    return { key, value: res.value as T, createdAt: Date.now(), ttlSeconds: undefined };
  }

  async set<T>(key: string, value: T, ttlSeconds?: number): Promise<void> {
    const ipc = this.ipc;
    if (!ipc || typeof ipc.invoke !== "function") return;
    await ipc.invoke("zeta:cache:set", key, value, ttlSeconds);
  }

  async delete(key: string): Promise<void> {
    const ipc = this.ipc;
    if (!ipc || typeof ipc.invoke !== "function") return;
    await ipc.invoke("zeta:cache:delete", key);
  }

  async clear(): Promise<void> {
    const ipc = this.ipc;
    if (!ipc || typeof ipc.invoke !== "function") return;
    await ipc.invoke("zeta:cache:clear");
  }
}

// Singleton getter: prefer IndexedDB in renderer, otherwise fallback to MemoryCache
let _defaultCache: ICache | null = null;
export function getDefaultCache(): ICache {
  if (_defaultCache) return _defaultCache;
  try {
    // prefer main-process IPC cache when renderer has ipc bridge available
    try {
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      const anyWin = (globalThis as any).window ?? (globalThis as any);
      if (anyWin?.electron?.ipcRenderer?.invoke) {
        _defaultCache = new IpcCache();
        return _defaultCache;
      }
    } catch {}
    if (typeof indexedDB !== "undefined") {
      _defaultCache = new IndexedDBCache();
      return _defaultCache;
    }
  } catch (e) {
    // not in browser env
    // eslint-disable-next-line no-console
    console.debug("IndexedDB not available:", e);
  }
  // If running in Node (Electron main), prefer SQLite-backed cache when available
  try {
    // detect Node
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const isNode =
      typeof (globalThis as any).process !== "undefined" &&
      !!(globalThis as any).process.versions?.node;
    if (isNode) {
      try {
        // eslint-disable-next-line @typescript-eslint/no-var-requires, @typescript-eslint/no-explicit-any
        const os = require("os");
        // eslint-disable-next-line @typescript-eslint/no-var-requires
        const path = require("path");
        const dbDir = path.join(os.homedir(), ".zeta");
        const dbPath = path.join(dbDir, "cache.db");
        // attempt to create SQLiteCache (will fall back to MemoryCache if better-sqlite3 not present)
        const SqliteCls = createSQLiteCacheClass();
        if (SqliteCls) {
          _defaultCache = new SqliteCls(dbPath);
          return _defaultCache;
        }
      } catch (err) {
        // eslint-disable-next-line no-console
        console.debug("SQLiteCache not available, falling back to MemoryCache:", err);
      }
    }
  } catch (err) {
    // eslint-disable-next-line no-console
    console.debug("Node detection failed:", err);
  }
  _defaultCache = new MemoryCache();
  return _defaultCache;
}

// Factory: create SQLiteCache class if `better-sqlite3` is available.
function createSQLiteCacheClass(): (new (dbPath: string) => ICache) | null {
  try {
    // eslint-disable-next-line @typescript-eslint/no-var-requires
    const Database = require("better-sqlite3");
    return class SQLiteCache implements ICache {
      private readonly db: ReturnType<typeof Database>;
      constructor(private readonly dbPath: string) {
        const fs = require("fs");
        const path = require("path");
        const dir = path.dirname(dbPath);
        if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
        this.db = new Database(dbPath);
        this.db.exec(
          "CREATE TABLE IF NOT EXISTS cache (key TEXT PRIMARY KEY, value BLOB, createdAt INTEGER, ttlSeconds INTEGER)",
        );
      }

      async get<T>(key: string): Promise<CacheEntry<T> | null> {
        const row = this.db
          .prepare("SELECT value, createdAt, ttlSeconds FROM cache WHERE key = ?")
          .get(key);
        if (!row) return null;
        const { value, createdAt, ttlSeconds } = row as {
          value: Buffer;
          createdAt: number;
          ttlSeconds: number | null;
        };
        if (ttlSeconds && Date.now() - createdAt > ttlSeconds * 1000) {
          this.delete(key).catch(() => {});
          return null;
        }
        try {
          return {
            key,
            value: JSON.parse(value.toString()),
            createdAt,
            ttlSeconds: ttlSeconds ?? undefined,
          } as CacheEntry<T>;
        } catch {
          return {
            key,
            value: value as unknown as T,
            createdAt,
            ttlSeconds: ttlSeconds ?? undefined,
          } as CacheEntry<T>;
        }
      }

      async set<T>(key: string, value: T, ttlSeconds?: number): Promise<void> {
        const str = JSON.stringify(value);
        const stmt = this.db.prepare(
          "INSERT OR REPLACE INTO cache (key, value, createdAt, ttlSeconds) VALUES (?, ?, ?, ?)",
        );
        stmt.run(key, Buffer.from(str), Date.now(), ttlSeconds ?? null);
      }

      async delete(key: string): Promise<void> {
        this.db.prepare("DELETE FROM cache WHERE key = ?").run(key);
      }

      async clear(): Promise<void> {
        this.db.prepare("DELETE FROM cache").run();
      }
    };
  } catch (e) {
    // eslint-disable-next-line no-console
    console.debug("better-sqlite3 not installed or failed to load:", e);
    return null;
  }
}

export default ICache;
