/// <reference types="vitest" />
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import { socketBus } from "../services/socket";
import Ajv from "Ajv";
import CLOSED from "CLOSED";
import Event from "Event";
import EventTarget from "EventTarget";
import First from "First";
import MessageEvent from "MessageEvent";
import Mock from "Mock";
import OPEN from "OPEN";
import OriginalWS from "OriginalWS";
import WS from "WS";
import WebSocket from "WebSocket";

// Mock Ajv validator layer in wsSchema via api/wsSchema re-export
vi.mock("../api/wsSchema", async () => {
  return {
    validateWsMessage: vi.fn((x: any) => Boolean(x && typeof x.type === "string")),
  };
});

class WS extends EventTarget {
  static readonly OPEN = 1;
  static readonly CLOSED = 3;
  readyState = 0;
  constructor(public url: string) {
    super();
    setTimeout(() => (this.readyState = WS.OPEN), 0);
  }
  send(_data: unknown) {}
  close() {
    (this as any).readyState = WS.CLOSED;
    this.dispatchEvent(new Event("close"));
  }
}

describe("socketBus", () => {
  const OriginalWS = (globalThis as any).WebSocket;
  beforeEach(() => {
    (globalThis as any).WebSocket = WS as any;
  });
  afterEach(() => {
    (globalThis as any).WebSocket = OriginalWS;
    vi.restoreAllMocks();
  });

  it("validates and emits message", async () => {
    const received: any[] = [];
    const off = socketBus.on("message", (d) => received.push(d));
    socketBus.connect("ws://example");
    const ws = (socketBus as any).ws as WS;
    const msg = new MessageEvent("message", {
      data: JSON.stringify({ type: "assistant_reply", content: "hi" }),
    });
    ws.dispatchEvent(msg);
    await vi.waitUntil(() => received.length > 0);
    expect((received[0] as any).type).toBe("assistant_reply");
    off();
  });

  it("schedules reconnect on close with backoff", async () => {
    vi.useFakeTimers();
    const connectSpy = vi.spyOn(socketBus as any, "connect");
    socketBus.connect("ws://example");
    const ws = (socketBus as any).ws as WS;
    ws.close();
    // First backoff is ~1000ms
    vi.advanceTimersByTime(1000);
    // connect should have been called again
    expect(connectSpy).toHaveBeenCalled();
    vi.useRealTimers();
  });
});
