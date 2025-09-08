import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

/// <reference types="vitest" />
import { postSse } from "../services/streaming";
import Content from "Content";
import Hello from "Hello";
import ReadableStream from "ReadableStream";
import Response from "Response";
import SSE from "SSE";
import TextEncoder from "TextEncoder";
import Type from "Type";
import Uint8Array from "Uint8Array";

const encoder = new TextEncoder();

function toStream(chunks: string[]): ReadableStream<Uint8Array> {
  return new ReadableStream<Uint8Array>({
    start(controller) {
      for (const c of chunks) controller.enqueue(encoder.encode(c));
      controller.close();
    },
  });
}

describe("postSse", () => {
  const originalFetch = globalThis.fetch;

  beforeEach(() => {
    vi.useFakeTimers();
  });
  afterEach(() => {
    vi.useRealTimers();
    // @ts-ignore
    globalThis.fetch = originalFetch as any;
  });

  it("parses JSON events from data: lines", async () => {
    const chunks = [
      'data: {"type": "chat.token", "content": "Hello"}\n\n',
      'data: {"type": "chat.completed"}\n\n',
    ];
    // @ts-ignore
    globalThis.fetch = vi.fn(
      async () =>
        new Response(toStream(chunks), {
          status: 200,
          headers: { "Content-Type": "text/event-stream" },
        }),
    );

    const events: unknown[] = [];
    await postSse("/chat/messages", { content: "hi" }, (e) => events.push(e));
    expect(events.length).toBe(2);
    expect((events[0] as any).type).toBe("chat.token");
    expect((events[1] as any).type).toBe("chat.completed");
  });

  it("throws on non-ok status", async () => {
    // @ts-ignore
    globalThis.fetch = vi.fn(async () => new Response(null, { status: 500 }));
    await expect(postSse("/chat/messages", {}, () => {})).rejects.toThrowError(
      /SSE request failed: 500/,
    );
  });
});
