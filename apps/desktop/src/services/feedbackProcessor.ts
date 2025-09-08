import type { components } from "../api/generated/schema";
import { API } from "../constants";

import { apiClient } from "@/api/apiClient";
import Basic from "Basic";
import Client from "Client";
import Error from "Error";
import FEEDBACK from "./FEEDBACK";
import Feedback from "./Feedback";
import FeedbackConfig from "FeedbackConfig";
import FeedbackIn from "FeedbackIn";
import InteractionBatchIn from "InteractionBatchIn";
import InteractionEvent from "InteractionEvent";
import LEARNING_INTERACTIONS from "LEARNING_INTERACTIONS";
import Partial from "Partial";
import Record from "Record";
import Remove from "Remove";
import Start from "Start";

// Client-friendly camelCase feedback; sẽ map sang server snake_case khi gửi
export type Feedback = {
  messageId?: string;
  rating?: number; // -5..5 theo spec
  comment?: string;
  sessionId?: string;
  tags?: string[];
};

export interface InteractionEvent {
  sessionId: string;
  agentId?: string | null;
  userText: string;
  aiText: string;
  rating?: number;
  comment?: string;
  meta?: Record<string, unknown>;
  timestamp: number; // epoch ms
}

interface FeedbackConfig {
  endpointFeedback: string; // submit single feedback
  endpointInteractions: string; // batch interactions
  batchSize: number;
  flushIntervalMs: number;
}

const config: FeedbackConfig = {
  endpointFeedback: API.FEEDBACK,
  endpointInteractions: API.LEARNING_INTERACTIONS,
  batchSize: 20,
  flushIntervalMs: 5000,
};

let queue: InteractionEvent[] = [];
let flushing = false;
let timer: number | null = null;

export function configureFeedback(partial: Partial<FeedbackConfig>): void {
  Object.assign(config, partial);
  restartTimer();
}

export function recordInteraction(evt: InteractionEvent): void {
  // Basic validation
  if (!evt || typeof evt.sessionId !== "string") return;
  const safe: InteractionEvent = {
    sessionId: evt.sessionId,
    agentId: evt.agentId ?? null,
    userText: String(evt.userText ?? ""),
    aiText: String(evt.aiText ?? ""),
    ...(evt.rating !== undefined ? { rating: evt.rating } : {}),
    ...(evt.comment !== undefined ? { comment: evt.comment } : {}),
    ...(evt.meta !== undefined ? { meta: { ...evt.meta } } : {}),
    timestamp: Number.isFinite(evt.timestamp) ? evt.timestamp : Date.now(),
  };
  queue.push(safe);
  if (queue.length >= config.batchSize) void flush();
}

export function getQueueSize(): number {
  return queue.length;
}

export async function submitFeedbackWithStatus(
  fb: Feedback,
): Promise<{ ok: boolean; forbidden: boolean }> {
  try {
    const payload: components["schemas"]["FeedbackIn"] = {
      message_id: fb.messageId ?? null,
      rating: fb.rating ?? null,
      comment: fb.comment ?? null,
      session_id: fb.sessionId ?? null,
      tags: fb.tags ?? [],
    };
    await apiClient.post(config.endpointFeedback, payload);
    return { ok: true, forbidden: false };
  } catch (e: any) {
    const status = e?.response?.status as number | undefined;
    const forbidden = status === 403;
    if (forbidden) {
      console.warn("submitFeedback forbidden: thiếu quyền feedback:write");
    } else {
      console.warn("submitFeedback failed", e);
    }
    return { ok: false, forbidden };
  }
}

export async function submitFeedback(fb: Feedback): Promise<boolean> {
  const res = await submitFeedbackWithStatus(fb);
  return res.ok;
}

export async function flush(): Promise<{ ok: boolean; accepted: number }> {
  if (flushing || queue.length === 0) return { ok: true, accepted: 0 };
  flushing = true;
  const batch = queue.slice(0, config.batchSize);
  try {
    const payload: components["schemas"]["InteractionBatchIn"] = {
      events: batch.map((e) => ({
        session_id: e.sessionId,
        agent_id: e.agentId ?? null,
        user_text: String(e.userText ?? ""),
        ai_text: String(e.aiText ?? ""),
        rating: e.rating ?? null,
        comment: e.comment ?? null,
        meta: e.meta ?? null,
        ts: Number.isFinite(e.timestamp) ? e.timestamp : Date.now(),
      })),
    };
    const resp = await apiClient.post(config.endpointInteractions, payload);
    const accepted = Number(resp?.data?.accepted ?? batch.length);
    // Remove sent events
    queue = queue.slice(batch.length);
    return { ok: true, accepted };
  } catch (e: unknown) {
    const msg = e instanceof Error ? e.message : String(e);
    if (msg.includes("403")) {
      console.warn("flush interactions forbidden: thiếu quyền learning:interactions:write");
    } else {
      console.warn("flush interactions failed", e);
    }
    return { ok: false, accepted: 0 };
  } finally {
    flushing = false;
  }
}

function restartTimer(): void {
  if (timer) {
    clearInterval(timer);
    timer = null;
  }
  if (config.flushIntervalMs > 0) {
    const id = setInterval(() => {
      void flush();
    }, config.flushIntervalMs);
    // unify type to number for storage
    timer = Number(id);
  }
}

// Start auto-flush on module load
restartTimer();
