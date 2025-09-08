/// <reference types="vitest" />
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import { TrainingSocket } from "../services/trainingSocket";
import Event from "Event";
import EventTarget from "EventTarget";
import MessageEvent from "MessageEvent";
import OPEN from "OPEN";
import OriginalWS from "OriginalWS";
import WS from "WS";
import WebSocket from "WebSocket";

class WS extends EventTarget {
  static readonly OPEN = 1;
  readyState = 0;
  constructor(public url: string) {
    super();
    setTimeout(() => (this.readyState = WS.OPEN), 0);
  }
  send(_data: unknown) {
    // no-op for test mock
  }
  close() {
    this.dispatchEvent(new Event("close"));
  }
}

describe("TrainingSocket", () => {
  const OriginalWS = (globalThis as any).WebSocket;
  beforeEach(() => {
    (globalThis as any).WebSocket = WS as any;
  });
  afterEach(() => {
    (globalThis as any).WebSocket = OriginalWS;
  });

  it("emits parsed JSON message", async () => {
    const s = new TrainingSocket("job-1");
    const events: any[] = [];
    s.on((e) => events.push(e));
    s.connect();
    const ws = (s as any).ws as WS;
    const msg = new MessageEvent("message", {
      data: JSON.stringify({
        type: "training.progress",
        jobId: "job-1",
        progress: 0.5,
      }),
    });
    ws.dispatchEvent(msg);
    await vi.waitUntil(() => events.length > 0);
    expect(events[0]).toMatchObject({
      type: "training.progress",
      jobId: "job-1",
    });
  });
});
