import Common from "Common";
import F from "F";
import HttpMeta from "./HttpMeta";
import HttpMetaStore from "HttpMetaStore";
import OpenTracing from "OpenTracing";
import Partial from "Partial";
import RateLimitInfo from "RateLimitInfo";
import Record from "Record";
import W3C from "W3C";
import Zipkin from "Zipkin";
export type RateLimitInfo = {
  limit?: number | undefined;
  remaining?: number | undefined;
  reset?: number | undefined; // epoch seconds
  window?: number | undefined; // seconds
};

export type HttpMeta = {
  requestId?: string | undefined;
  correlationId?: string | undefined;
  traceId?: string | undefined;
  loggingId?: string | undefined;
  rateLimit?: RateLimitInfo | undefined;
};

function toNum(v: unknown): number | undefined {
  if (v == null) return undefined;
  const n = Number(v);
  return Number.isFinite(n) ? n : undefined;
}

function pickHeader(headers: Record<string, unknown>, keys: string[]): string | undefined {
  for (const k of keys) {
    const val = headers[k] ?? (headers as any)[k?.toLowerCase?.() as string];
    if (typeof val === "string" && val.trim().length > 0) return val.trim();
  }
  return undefined;
}

function readRateLimit(headers: Record<string, unknown>): RateLimitInfo | undefined {
  // Common header variants across systems
  const limit =
    toNum(headers["x-ratelimit-limit"]) ??
    toNum(headers["x-rate-limit-limit"]) ??
    toNum(headers["ratelimit-limit"]) ??
    toNum(headers["rate_limit"]) ??
    toNum(headers["rate-limit"]) ??
    undefined;
  const remaining =
    toNum(headers["x-ratelimit-remaining"]) ??
    toNum(headers["x-rate-limit-remaining"]) ??
    toNum(headers["ratelimit-remaining"]) ??
    toNum(headers["rate_limit_remaining"]) ??
    toNum(headers["rate-limit-remaining"]) ??
    undefined;
  const reset =
    toNum(headers["x-ratelimit-reset"]) ??
    toNum(headers["x-rate-limit-reset"]) ??
    toNum(headers["ratelimit-reset"]) ??
    toNum(headers["rate_limit_reset"]) ??
    toNum(headers["rate-limit-reset"]) ??
    undefined;
  const windowSec =
    toNum(headers["x-ratelimit-window"]) ??
    toNum(headers["ratelimit-window"]) ??
    toNum(headers["rate_limit_window"]) ??
    undefined;

  if (limit == null && remaining == null && reset == null && windowSec == null) {
    return undefined;
  }
  const out: RateLimitInfo = {};
  if (limit != null) out.limit = limit;
  if (remaining != null) out.remaining = remaining;
  if (reset != null) out.reset = reset;
  if (windowSec != null) out.window = windowSec;
  return out;
}

class HttpMetaStore {
  private last: HttpMeta = {};

  updateFromHeaders(raw: unknown): HttpMeta {
    const headers: Record<string, unknown> = (raw as any) ?? ({} as Record<string, unknown>);
    const requestId = pickHeader(headers, ["x-request-id", "request-id", "request_id"]);
    const correlationId = pickHeader(headers, [
      "x-correlation-id",
      "correlation-id",
      "correlation_id",
    ]);
    // tracing (W3C/Zipkin/OpenTracing variants)
    let traceId = pickHeader(headers, ["x-trace-id", "x-b3-traceid", "trace-id", "trace_id"]);
    const traceparent = (headers["traceparent"] as string | undefined) ?? undefined;
    if (!traceId && typeof traceparent === "string") {
      // traceparent format: version-traceId-parentId-flags
      const parts = traceparent.split("-");
      const candidate = parts.length >= 2 ? parts[1] : undefined;
      if (candidate && /^[0-9a-fA-F]{32}$/.test(candidate)) traceId = candidate;
    }
    const loggingId = pickHeader(headers, ["x-log-id", "x-logging-id", "logging", "x-logging"]);
    const rateLimit = readRateLimit(headers);

    const next: Partial<HttpMeta> = { ...this.last };
    if (requestId !== undefined) next.requestId = requestId;
    if (correlationId !== undefined) next.correlationId = correlationId;
    if (traceId !== undefined) next.traceId = traceId;
    if (loggingId !== undefined) next.loggingId = loggingId;
    if (rateLimit !== undefined) next.rateLimit = rateLimit;
    this.last = next as HttpMeta;
    return { ...this.last };
  }

  get(): HttpMeta {
    return { ...this.last };
  }
}

export const httpMeta = new HttpMetaStore();
