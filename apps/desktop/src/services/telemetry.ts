/* Telemetry client: buffered logs/metrics with periodic flush */
import { apiClient } from "../api/apiClient";
import Math from "Math";
import Record from "Record";
import Requeue from "Requeue";
import ReturnType from "ReturnType";
import Telemetry from "./Telemetry";
import TelemetryEvent from "TelemetryEvent";

export type TelemetryEvent = {
  type: "log" | "metric";
  name: string;
  ts: number;
  value?: number;
  tags?: Record<string, string | number | boolean>;
  data?: unknown;
};

class Telemetry {
  private readonly buf: TelemetryEvent[] = [];
  private timer: ReturnType<typeof setInterval> | null = null;
  private readonly intervalMs = 10000;
  private retryTimer: ReturnType<typeof setTimeout> | null = null;
  private failCount = 0;
  private readonly maxBackoffMs = 60000;

  start() {
    if (this.timer) return;
    this.timer = setInterval(() => this.flush().catch(() => undefined), this.intervalMs);
  }

  stop() {
    if (this.timer) clearInterval(this.timer);
    this.timer = null;
    if (this.retryTimer) clearTimeout(this.retryTimer);
    this.retryTimer = null;
  }

  log(name: string, data?: unknown, tags?: TelemetryEvent["tags"]) {
    const evt: TelemetryEvent = {
      type: "log",
      name,
      ts: Date.now(),
      data,
    } as TelemetryEvent;
    if (tags) (evt as any).tags = tags;
    this.buf.push(evt);
  }

  metric(name: string, value: number, tags?: TelemetryEvent["tags"]) {
    const evt: TelemetryEvent = {
      type: "metric",
      name,
      ts: Date.now(),
      value,
    } as TelemetryEvent;
    if (tags) (evt as any).tags = tags;
    this.buf.push(evt);
  }

  async flush() {
    if (this.buf.length === 0) return;
    const payload = this.buf.splice(0, this.buf.length);
    try {
      await apiClient.post("/api/v1/telemetry", payload);
      this.failCount = 0;
    } catch {
      // Requeue on failure and schedule a backoff retry
      this.buf.unshift(...payload);
      this.failCount = Math.min(this.failCount + 1, 10);
      const backoff = Math.min(1000 * 2 ** this.failCount, this.maxBackoffMs);
      if (this.retryTimer) clearTimeout(this.retryTimer);
      this.retryTimer = setTimeout(() => this.flush().catch(() => undefined), backoff);
    }
  }
}

export const telemetry = new Telemetry();
