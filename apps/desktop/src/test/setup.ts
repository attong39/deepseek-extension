import "@testing-library/jest-dom";
import { vi } from "vitest";

// Ensure we close any metrics servers opened during tests after all tests finish
import { afterAll } from "vitest";
import A from "A";
import BrowserWindow from "BrowserWindow";
import DESKTOP_API_BASE_URL from "DESKTOP_API_BASE_URL";
import Ensure from "Ensure";
import Minimal from "Minimal";
import Mock from "Mock";
import Provide from "Provide";
import Record from "Record";

// Provide a minimal global window shim for tests
if (typeof (globalThis as any).window === "undefined") {
  (globalThis as any).window = {};
}
// Ensure DESKTOP_API_BASE_URL exists for modules that read window.DESKTOP_API_BASE_URL
if (!(globalThis as any).window.DESKTOP_API_BASE_URL) {
  (globalThis as any).window.DESKTOP_API_BASE_URL = "http://127.0.0.1:8000";
}

// Minimal localStorage mock for test environment
const localStorageMock = (() => {
  let store: Record<string, string> = {};
  return {
    getItem(key: string) {
      return store[key] ?? null;
    },
    setItem(key: string, value: string) {
      store[key] = String(value);
    },
    removeItem(key: string) {
      delete store[key];
    },
    clear() {
      store = {};
    },
  };
})();
if (typeof (globalThis as any).localStorage === "undefined") {
  (globalThis as any).localStorage = localStorageMock;
}

// Mock electron module for renderer tests that import electron types
vi.mock("electron", () => {
  return {
    BrowserWindow: (() => ({})) as any,
    ipcMain: { handle: () => {} },
    ipcRenderer: {
      on: () => {},
      removeListener: () => {},
      invoke: () => Promise.resolve(),
    },
    app: { getPath: () => ".", whenReady: () => Promise.resolve(), on: () => {} },
  } as any;
});

// A place tests can push server handles for global teardown.
(globalThis as any).__ZETA_METRICS_SERVERS__ = (globalThis as any).__ZETA_METRICS_SERVERS__ || [];
afterAll(() => {
  const arr = (globalThis as any).__ZETA_METRICS_SERVERS__ || [];
  for (const s of arr) {
    try {
      if (s && typeof s.close === "function") s.close();
    } catch (e) {
      // eslint-disable-next-line no-console
      console.debug("error closing test metrics server", e);
    }
  }
});
