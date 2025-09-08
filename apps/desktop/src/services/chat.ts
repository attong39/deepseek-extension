/* Chat service: HTTP fallback + WS streaming hooks. */
import { apiClient } from "../api/apiClient";
import { DEFAULT_WS_URL } from "../constants";
import { socketBus } from "./socket";
import { postSse } from "./streaming";
import type { AnyMsg } from "./wsSchema";
import Chat from "./Chat";
import ChatReply from "ChatReply";
import Ensure from "Ensure";
import Error from "Error";
import HTTP from "HTTP";
import POST from "POST";
import Record from "Record";
import SSE from "SSE";
import Simple from "Simple";
import Subscribe from "Subscribe";
import WS from "./WS";

export type ChatReply = { content: string; timestamp?: string };

// Simple HTTP compat endpoint (server exposes POST /api/v1/chat)
export async function sendHttp(message: string): Promise<ChatReply> {
  const { data } = await apiClient.post("/chat", { message });
  return data as ChatReply;
}

// WS first, HTTP fallback
export async function send(
  message: string,
  opts?: { preferWs?: boolean },
): Promise<ChatReply | void> {
  const preferWs = opts?.preferWs ?? true;
  if (preferWs) {
    const ok = socketBus.send({ message });
    if (ok) return; // reply will arrive via WS "message" event
  }
  return await sendHttp(message);
}

// Subscribe to all WS messages (validated by socketBus)
export function onWsMessage(cb: (msg: AnyMsg) => void) {
  return socketBus.on("message", (data) => cb(data as AnyMsg));
}

// Ensure WS connection started (idempotent)
export function ensureWs(url?: string) {
  socketBus.connect(url || DEFAULT_WS_URL);
}

// SSE streaming for token events from POST /api/v1/chat/messages?stream=1
export async function stream(
  payload: {
    role?: string;
    content: string;
    attachments?: unknown[];
    metadata?: Record<string, unknown>;
  },
  handlers: {
    onToken?: (token: string, seq?: number) => void;
    onCompleted?: (final?: unknown) => void;
    onError?: (err: Error) => void;
  },
): Promise<void> {
  await postSse(
    "/chat/messages",
    { ...payload },
    (evt: unknown) => {
      if (!evt || typeof evt !== "object") return;
      const t = (evt as any).type;
      if (t === "chat.token") {
        handlers.onToken?.(
          String((evt as any).content ?? ""),
          (evt as any).seq as number | undefined,
        );
      } else if (t === "chat.completed") {
        handlers.onCompleted?.(evt);
      }
    },
    { query: { stream: "1" } },
  ).catch((e: unknown) => handlers.onError?.(e instanceof Error ? e : new Error(String(e))));
}
