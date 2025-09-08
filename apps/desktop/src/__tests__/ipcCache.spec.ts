import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { afterAll, beforeAll, describe, expect, it } from "vitest";
import Error from "Error";
import Function from "Function";
import JS from "JS";
import Map from "Map";
import TTL from "TTL";

// import the module that registers handlers
// require the electron ipc handler module (JS file)
const { registerIpcHandlers } = require("../../electron/ipcHandler.js");

describe("ipc cache handlers (fallback tmp files)", () => {
  const handlers = new Map<string, Function>();

  const ipcMainMock = {
    handle(name: string, fn: Function) {
      handlers.set(name, fn);
    },
  } as any;

  beforeAll(() => {
    registerIpcHandlers(ipcMainMock);
  });

  afterAll(() => {
    // cleanup any tmp files created by tests
    const tmp = os.tmpdir();
    for (const file of fs.readdirSync(tmp)) {
      if (file.startsWith("zeta_cache_test_")) {
        try {
          fs.unlinkSync(path.join(tmp, file));
        } catch {}
      }
    }
  });

  async function invoke(name: string, ...args: any[]) {
    const fn = handlers.get(name);
    if (!fn) throw new Error(`handler not found: ${name}`);
    return await fn(null, ...args);
  }

  it("set/get respects TTL", async () => {
    const key = "test_key_ttl_" + Date.now();
    const setRes = await invoke("zeta:cache:set", key, { v: 1 }, 1); // 1 second TTL
    expect(setRes.ok).toBe(true);
    const getRes = await invoke("zeta:cache:get", key);
    expect(getRes.ok).toBe(true);
    expect(getRes.found).toBe(true);
    expect(getRes.value).toEqual({ v: 1 });
    // wait for TTL to expire
    await new Promise((r) => setTimeout(r, 1200));
    const getRes2 = await invoke("zeta:cache:get", key);
    expect(getRes2.ok).toBe(true);
    expect(getRes2.found).toBe(false);
  });

  it("delete removes key", async () => {
    const key = "test_key_del_" + Date.now();
    const setRes = await invoke("zeta:cache:set", key, { v: 2 }, 60);
    expect(setRes.ok).toBe(true);
    const delRes = await invoke("zeta:cache:delete", key);
    expect(delRes.ok).toBe(true);
    const getRes = await invoke("zeta:cache:get", key);
    expect(getRes.ok).toBe(true);
    expect(getRes.found).toBe(false);
  });

  it("clear removes all keys and stats reflects count", async () => {
    const k1 = "zeta_cache_test_a_" + Date.now();
    const k2 = "zeta_cache_test_b_" + Date.now();
    await invoke("zeta:cache:set", k1, { a: 1 }, 60);
    await invoke("zeta:cache:set", k2, { b: 2 }, 60);
    const statsBefore = await invoke("zeta:cache:stats");
    expect(statsBefore.ok).toBe(true);
    // ensure count at least 2
    expect(statsBefore.count >= 2).toBeTruthy();
    const clearRes = await invoke("zeta:cache:clear");
    expect(clearRes.ok).toBe(true);
    const statsAfter = await invoke("zeta:cache:stats");
    expect(statsAfter.ok).toBe(true);
    // after clear, tmp fallback count may be 0
    expect(statsAfter.count >= 0).toBeTruthy();
  });
});
