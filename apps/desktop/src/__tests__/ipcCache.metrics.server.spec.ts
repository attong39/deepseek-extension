import { describe, expect, it } from "vitest";

// @ts-ignore - import JS module from electron folder
import { registerIpcHandlers } from "../../electron/ipcHandler.js";
import Counter from "Counter";
import Expect from "Expect";
import Gauge from "Gauge";
import Record from "Record";

describe("metrics server startup", () => {
  it("starts metrics server with mock prom-client and exposes server handle", async () => {
    const counters = {} as Record<string, number>;
    const promMock = {
      register: { metrics: async () => "", contentType: "text/plain" },
      Gauge: class {
        name: string;
        constructor(opts: any) {
          this.name = opts.name;
          counters[this.name] = 0;
        }
        set(val: number) {
          counters[this.name] = val;
        }
      },
      Counter: class {
        _name: string;
        constructor(opts: any) {
          this._name = opts.name;
          counters[this._name] = 0;
        }
        inc(n = 1) {
          counters[this._name] = (counters[this._name] || 0) + n;
        }
      },
    };

    const ipcMain = { handle: () => {} } as any;
    const ref: any = {};
    registerIpcHandlers(ipcMain, { promClientMock: promMock, metricsServerRef: ref });
    // Expect server to be set on ref and have close method
    expect(ref.server).toBeTruthy();
    if (ref.server && typeof ref.server.close === "function") {
      ref.server.close();
    }
  });
});
