/** WS an toàn: ping/pong, backoff + jitter, AbortSignal, type-safe message. */
import Ajv from "ajv";
import addFormats from "ajv-formats";
import AbortSignal from "AbortSignal";
import AsyncGenerator from "AsyncGenerator";
import Backoff from "Backoff";
import Math from "Math";
import OPEN from "OPEN";
import Schema from "Schema";
import T from "T";
import WS from "./WS";
import WSClientOptions from "WSClientOptions";
import WebSocket from "./WebSocket";

export type Backoff = { baseMs?: number; maxMs?: number; jitter?: number };
export type WSClientOptions<T> = {
  schema: object;           // JSON Schema cho message
  heartbeatMs?: number;     // mặc định 15000ms
  backoff?: Backoff;        // { baseMs:400, maxMs:8000, jitter:0.2 }
  signal?: AbortSignal;     // để hủy stream
  onOpen?: () => void;
  onClose?: (code?: number, reason?: string) => void;
  onError?: (e: unknown) => void;
};

export function createWSClient<T = unknown>(url: string, opts: WSClientOptions<T>) {
  const ajv = new Ajv({ strict: true, allErrors: false });
  addFormats(ajv);
  const validate = ajv.compile<T>(opts.schema);
  let ws: WebSocket | null = null;
  let hbTimer: number | undefined;
  let alive = true;
  const queue: T[] = [];

  const heartbeat = () => {
    hbTimer && clearInterval(hbTimer);
    const hb = opts.heartbeatMs ?? 15000;
    hbTimer = window.setInterval(() => {
      if (ws?.readyState === WebSocket.OPEN) ws.send('{"type":"ping"}');
    }, hb);
  };

  const open = () =>
    new Promise<void>((resolve, reject) => {
      ws = new WebSocket(url);
      ws.onopen = () => { heartbeat(); opts.onOpen?.(); resolve(); };
      ws.onmessage = (ev) => {
        try {
          const msg = JSON.parse(String(ev.data));
          if (msg?.type === "pong") return; // trả lời heartbeat
          if (validate(msg)) queue.push(msg as T);
        } catch (e) { opts.onError?.(e); }
      };
      ws.onerror = (e) => opts.onError?.(e);
      ws.onclose = (ev) => {
        hbTimer && clearInterval(hbTimer);
        opts.onClose?.(ev.code, ev.reason);
        ws = null;
      };
    });

  function close() {
    alive = false;
    hbTimer && clearInterval(hbTimer);
    ws?.close();
    ws = null;
  }
  opts.signal?.addEventListener("abort", close, { once: true });

  async function* stream(): AsyncGenerator<T> {
    const back = { baseMs: 400, maxMs: 8000, jitter: 0.2, ...(opts.backoff ?? {}) };
    let delay = back.baseMs;
    while (alive && !(opts.signal?.aborted)) {
      try {
        await open();               // kết nối (hoặc throw)
        delay = back.baseMs;        // reset backoff khi nối lại
        while (alive && ws && ws.readyState === WebSocket.OPEN && !(opts.signal?.aborted)) {
          if (queue.length) yield queue.shift()!;
          else await new Promise((r) => setTimeout(r, 60));
        }
      } catch (e) {
        opts.onError?.(e);
      }
      // exponential backoff + jitter
      const jitter = 1 + (Math.random() * 2 - 1) * back.jitter;
      await new Promise((r) => setTimeout(r, Math.min(delay, back.maxMs) * jitter));
      delay = Math.min(delay * 2, back.maxMs);
    }
  }

  return { stream, close };
}
