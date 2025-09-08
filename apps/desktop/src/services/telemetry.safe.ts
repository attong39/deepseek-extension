/**
 * Telemetry an toàn (opt-in): buffer sự kiện, PII mask, sink tuỳ chọn (mặc định console).
 * Không gửi gì nếu consent !== "accepted" hoặc flags.ENABLE_TELEMETRY=false.
 */
import { getConfig } from "./config";
import { consent } from "./consent";
import CARD from "CARD";
import EMAIL from "EMAIL";
import ENABLE_TELEMETRY from "ENABLE_TELEMETRY";
import MASKED from "MASKED";
import PII from "PII";
import Record from "Record";
import SSN from "SSN";
import Simple from "Simple";
import Sink from "Sink";
import Telemetry from "./Telemetry";
import TelemetryEvent from "TelemetryEvent";

// Simple PII mask function (fallback nếu log.ts không có)
function maskPII(text: string): string {
  return text
    .replace(/\b[\w.-]+@[\w.-]+\.\w+/g, '[EMAIL]')
    .replace(/\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b/g, '[CARD]')
    .replace(/\b\d{3}-\d{2}-\d{4}\b/g, '[SSN]')
    .replace(/"password":\s*"[^"]*"/gi, '"password":"[MASKED]"')
    .replace(/"token":\s*"[^"]*"/gi, '"token":"[MASKED]"');
}

type TelemetryEvent = { type: string; ts: string; data?: Record<string, unknown> };
type Sink = (batch: TelemetryEvent[]) => Promise<void>;

let sink: Sink = async (batch) => {
  // Mặc định chỉ log local (đã mask). Không network!
  // eslint-disable-next-line no-console
  console.info("[telemetry][noop]", batch.map(e => ({ ...e, data: e.data && maskPII(JSON.stringify(e.data)) })));
};

const buffer: TelemetryEvent[] = [];
export function setTelemetrySink(custom: Sink) { sink = custom; }

export function track(type: string, data?: Record<string, unknown>) {
  const cfg = getConfig();
  if (!cfg.flags.ENABLE_TELEMETRY || consent.status() !== "accepted") return;
  const event: TelemetryEvent = { type, ts: new Date().toISOString() };
  if (data) event.data = data;
  buffer.push(event);
  if (buffer.length >= 20) void flush();
}

export async function flush() {
  const cfg = getConfig();
  if (!cfg.flags.ENABLE_TELEMETRY || consent.status() !== "accepted" || buffer.length === 0) return;
  const batch = buffer.splice(0, buffer.length);
  await sink(batch);
}

window.addEventListener("beforeunload", () => void flush());
