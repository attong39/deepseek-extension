/* SSE helper for POST streaming endpoints (text/event-stream). */
import { DEFAULT_API_BASE_URL } from "../constants";
import { session } from "./session";
import AbortError from "AbortError";
import AbortSignal from "AbortSignal";
import Aborted from "Aborted";
import Authorization from "Authorization";
import Bearer from "Bearer";
import Content from "Content";
import DOMException from "DOMException";
import Error from "Error";
import POST from "POST";
import Read from "Read";
import ReadableStream from "ReadableStream";
import Record from "Record";
import Response from "Response";
import SSE from "SSE";
import SseOptions from "SseOptions";
import TextDecoder from "TextDecoder";
import Type from "Type";
import URL from "URL";

export type SseOptions = {
  query?: Record<string, string | number | boolean>;
  headers?: Record<string, string>;
  signal?: AbortSignal;
};

function buildUrl(path: string, query?: Record<string, string | number | boolean>): string {
  const base = DEFAULT_API_BASE_URL.replace(/\/$/, "");
  const url = new URL(base + (path.startsWith("/") ? path : `/${path}`));
  if (query) {
    for (const [k, v] of Object.entries(query)) {
      url.searchParams.set(k, String(v));
    }
  }
  return url.toString();
}

// Read and parse SSE lines from a ReadableStream
function extractEvents(buffer: string): {
  remaining: string;
  events: unknown[];
} {
  const events: unknown[] = [];
  const chunks = buffer.split(/\n\n/);
  const remaining = chunks.pop() ?? "";
  for (const chunk of chunks) {
    const lines = chunk.split(/\n/);
    for (const line of lines) {
      const m = /^data:\s*(.*)$/.exec(line);
      if (!m || typeof m[1] !== "string") continue;
      const payload = m[1];
      try {
        events.push(JSON.parse(payload));
      } catch {
        // ignore non-JSON data lines
      }
    }
  }
  return { remaining, events };
}

async function readSseStream(
  resp: Response,
  onEvent: (evt: unknown) => void,
  signal?: AbortSignal | null,
): Promise<void> {
  const reader = resp.body?.getReader();
  if (!reader) return;
  const decoder = new TextDecoder();
  let buffer = "";
  while (true) {
    if (signal && (signal as AbortSignal).aborted) throw new DOMException("Aborted", "AbortError");
    const { done, value } = await reader.read();
    if (done) break;
    buffer += decoder.decode(value, { stream: true });
    const { remaining, events } = extractEvents(buffer);
    buffer = remaining;
    for (const e of events) onEvent(e);
  }
}

export async function postSse(
  path: string,
  body: unknown,
  onEvent: (evt: unknown) => void,
  opts?: SseOptions,
): Promise<void> {
  const url = buildUrl(path, opts?.query);
  const token = session.getToken?.() || localStorage.getItem("zeta_token");
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(opts?.headers ?? {}),
  };
  if (token) headers.Authorization = `Bearer ${token}`;
  const resp = await fetch(url, {
    method: "POST",
    headers,
    body: JSON.stringify(body ?? {}),
    signal: (opts?.signal ?? null) as AbortSignal | null,
  });
  if (!resp.ok) {
    throw new Error(`SSE request failed: ${resp.status}`);
  }
  await readSseStream(resp, onEvent, opts?.signal ?? null);
}
