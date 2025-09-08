import "@testing-library/jest-dom/vitest";
import { vi } from "vitest";
import Bridge from "Bridge";
import BrowserWindow from "BrowserWindow";
import CLOSED from "CLOSED";
import CLOSING from "CLOSING";
import CONNECTING from "CONNECTING";
import Clear from "Clear";
import Database from "Database";
import Electron from "Electron";
import Error from "Error";
import Function from "Function";
import HTTP from "HTTP";
import Helper from "Helper";
import IPC from "IPC";
import Map from "Map";
import MessageEvent from "MessageEvent";
import Mock from "Mock";
import MockWS from "MockWS";
import No from "No";
import OPEN from "OPEN";
import Set from "Set";
import Simple from "Simple";
import Simulate from "Simulate";
import Support from "Support";
import Timing from "Timing";
import UI from "../src/UI/index";
import URL from "URL";
import WS from "WS";
import WSHandler from "WSHandler";
import WebSocket from "WebSocket";

// Mock HTTP module before any imports
vi.doMock("http", () => {
  const fakeServer = {
    listen: vi.fn((_port?: number, _host?: string) => { 
      // Simulate async listening
      queueMicrotask(() => fakeServer.emit("listening"));
      return fakeServer; 
    }),
    close: vi.fn((cb?: () => void) => { cb?.(); }),
    address: vi.fn(() => ({ address: "127.0.0.1", port: 9126 })),
    on: vi.fn(),
    emit: vi.fn()
  };
  return {
    createServer: vi.fn((_handler?: any) => fakeServer)
  };
});

/* ----- Electron IPC mock (renderer-side) ----- */
vi.doMock("electron", () => {
  const ipcRenderer = {
    invoke: vi.fn().mockResolvedValue(0),
    on: vi.fn(),
    send: vi.fn()
  };
  const clipboard = { writeText: vi.fn(), readText: vi.fn().mockResolvedValue("") };
  const nativeTheme = { shouldUseDarkColors: false, themeSource: "light" as const };
  const shell = { openExternal: vi.fn().mockResolvedValue(true) };
  // Mock main process ipcMain for ipcCache tests
  const ipcMain = {
    handle: vi.fn(),
    on: vi.fn(),
    removeAllListeners: vi.fn()
  };
  const BrowserWindow = vi.fn();
  // Support both default and named exports
  const electronMock = { ipcRenderer, clipboard, nativeTheme, shell, ipcMain, BrowserWindow };
  return {
    ...electronMock,
    default: electronMock
  };
});

/* ----- Mock native modules ----- */
vi.mock("robotjs", () => ({
  keyTap: vi.fn(),
  typeString: vi.fn(),
  moveMouse: vi.fn(),
  mouseClick: vi.fn()
}));


// Mock HTTP module before any imports
vi.doMock("http", () => {
  const fakeServer = {
    listen: vi.fn((_port?: number, _host?: string) => { 
      // Simulate async listening
      queueMicrotask(() => fakeServer.emit("listening"));
      return fakeServer; 
    }),
    close: vi.fn((cb?: () => void) => { cb?.(); }),
    address: vi.fn(() => ({ address: "127.0.0.1", port: 9126 })),
    on: vi.fn(),
    emit: vi.fn()
  };
  return {
    createServer: vi.fn((_handler?: any) => fakeServer)
  };
});

vi.mock("better-sqlite3", () => {
  class Database {
    prepare(_sql: string) {
      return {
        get: vi.fn(() => ({})),
        all: vi.fn(() => []),
        run: vi.fn(() => ({ changes: 1, lastInsertRowid: 1 })),
        finalize: vi.fn()
      };
    }
    exec = vi.fn();
    close = vi.fn();
    pragma = vi.fn(() => []);
  }
  return { default: Database };
});

/* ----- Mock electron/ipcHandler.js to prevent native module loading ----- */
vi.mock("../../electron/ipcHandler.js", () => ({
  registerIpcHandlers: vi.fn((ipcMain) => {
    // Simple cache mock for test
    const cache = new Map();
    ipcMain.handle("zeta:cache:get", async (_, key: string) => {
      const item = cache.get(key);
      if (!item) return { ok: true, found: false };
      if (item.ttl && Date.now() > item.expires) {
        cache.delete(key);
        return { ok: true, found: false };
      }
      return { ok: true, found: true, value: item.value };
    });
    ipcMain.handle("zeta:cache:set", async (_, key: string, value: any, ttl: number) => {
      cache.set(key, { value, ttl, expires: Date.now() + ttl * 1000 });
      return { ok: true };
    });
    ipcMain.handle("zeta:cache:delete", async (_, key: string) => {
      cache.delete(key);
      return { ok: true };
    });
    ipcMain.handle("zeta:cache:clear", async () => {
      cache.clear();
      return { ok: true };
    });
    ipcMain.handle("zeta:cache:stats", async () => {
      return { ok: true, count: cache.size };
    });
  })
}));

/* ----- WebSocket mock with registry + helpers ----- */
type WSHandler = (evt: MessageEvent) => void;
class MockWS {
  static CONNECTING = 0; static OPEN = 1; static CLOSING = 2; static CLOSED = 3;
  readyState = MockWS.OPEN;
  url: string;
  onopen?: () => void;
  onmessage?: WSHandler;
  onclose?: () => void;
  onerror?: () => void;
  private listeners = new Map<string, Set<Function>>();
  constructor(url: string) {
    this.url = url;
    queueMicrotask(() => this.onopen?.());
    __WS_REGISTRY__.push(this);
  }
  send(_data: unknown) {/* no-op */}
  close() { this.readyState = MockWS.CLOSED; this.onclose?.(); }
  addEventListener(type: string, cb: Function) {
    const set = this.listeners.get(type) ?? new Set();
    set.add(cb); this.listeners.set(type, set);
  }
  removeEventListener(type: string, cb: Function) {
    const set = this.listeners.get(type); set?.delete(cb);
  }
  _emit(type: "message", data: unknown) {
    const evt = new MessageEvent("message", { data });
    this.onmessage?.(evt);
    this.listeners.get(type)?.forEach((cb) => (cb as WSHandler)(evt));
  }
}
const __WS_REGISTRY__: MockWS[] = [];
vi.stubGlobal("WebSocket", MockWS as any);

// Helper global: đẩy message vào WS theo URL substring
(globalThis as any).__emitWS = (urlSubstr: string, data: unknown) => {
  const ws = __WS_REGISTRY__.find(w => w.url.includes(urlSubstr));
  if (!ws) throw new Error("No WS instance for " + urlSubstr);
  ws._emit("message", data);
};

// Clear registry helper for tests
(globalThis as any).__clearWSRegistry = () => {
  __WS_REGISTRY__.length = 0;
};

// Bridge giả lập cho renderer gọi từ UI
Object.defineProperty(window, "zetaBridge", {
  value: { purgeLogs: (days: number) => Promise.resolve(days >= 0 ? 0 : 0) },
  writable: false
});

/* ----- Timing helpers ----- */
export const flushPromises = () => new Promise((r) => setTimeout(r, 0));

/* Một số test kỳ vọng randomUUID tồn tại */
if (!("crypto" in globalThis) || !(globalThis.crypto as any).randomUUID) {
  (globalThis as any).crypto = { randomUUID: () => "00000000-0000-4000-8000-000000000000" };
}
