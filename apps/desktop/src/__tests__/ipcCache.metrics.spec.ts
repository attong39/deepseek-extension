import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { afterAll, beforeAll, describe, expect, it } from "vitest";
import Counter from "Counter";
import Error from "Error";
import Function from "Function";
import Gauge from "Gauge";
import JS from "JS";
import Map from "Map";
import Record from "Record";

// require the electron ipc handler module (JS file)
const ipcModule = require("../../electron/ipcHandler.js");

describe("ipc cache metrics (mocked prom-client)", () => {
  const handlers = new Map<string, Function>();
  const ipcMainMock = {
    handle(name: string, fn: Function) {
      handlers.set(name, fn);
    },
  } as any;

  // minimal prom mock to capture counters
  const counters: Record<string, number> = {};
  const promMock = {
    register: { metrics: async () => "", contentType: "text/plain" },
    Gauge: class {
      name: string;
      constructor(opts: any) {
        this.name = opts.name;
        (counters as any)[this.name] = 0;
      }
      set(val: number) {
        (counters as any)[this.name] = val;
      }
    },
    Counter: class {
      _name: string;
      constructor(opts: any) {
        this._name = opts.name;
        (counters as any)[this._name] = 0;
      }
      inc(n = 1) {
        (counters as any)[this._name] = ((counters as any)[this._name] || 0) + n;
      }
    },
  };

  beforeAll(() => {
    ipcModule.registerIpcHandlers(ipcMainMock, { promClientMock: promMock });
  });

  afterAll(() => {
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

  it("increments hits and misses counters", async () => {
    const key = "metric_test_" + Date.now();
    await invoke("zeta:cache:set", key, { x: 1 }, 60);
    const g1 = await invoke("zeta:cache:get", key);
    expect(g1.found).toBe(true);
    // expect hit counter increment
    // after one successful get we expect exactly one hit
    expect((counters as any)["zeta_cache_hits_total"]).toBe(1);

    // get a non-existing key -> one miss
    await invoke("zeta:cache:get", key + "_nope");
    expect((counters as any)["zeta_cache_misses_total"]).toBe(1);
  });
});
