import A from "A";
import DB from "DB";
import EventPayload from "EventPayload";
import No from "No";
import PII from "PII";
import Record from "Record";
import Z from "Z";
import Z0 from "Z0";
type EventPayload = Record<string, unknown>;

function maskPII(input: unknown): unknown {
  if (typeof input === "string") {
    let s = input;
    s = s.replace(/\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b/gi, "<redacted:email>");
    s = s.replace(/\b(\+?\d{1,3}[-.\s]?)?(\(?\d{2,4}\)?[-.\s]?){2,}\d{3,}\b/g, "<redacted:phone>");
    s = s.replace(/\b\d{1,3}(?:\.\d{1,3}){3}\b/g, "<redacted:ip>");
    return s;
  }
  if (Array.isArray(input)) return input.map(maskPII);
  if (input && typeof input === "object") {
    const out: Record<string, unknown> = {};
    for (const [k, v] of Object.entries(input as Record<string, unknown>)) {
      out[k] = /name|email|phone|token|key|address/i.test(k) ? "<redacted>" : maskPII(v);
    }
    return out;
  }
  return input;
}

const buffer: EventPayload[] = [];

export function track(event: string, data?: EventPayload) {
  // No network here by default — chỉ buffer local, PII đã mask
  const safe = maskPII({ event, ts: new Date().toISOString(), ...data });
  buffer.push(safe as EventPayload);
  // Tuỳ chọn: flush sang file/local DB trong tương lai (opt-in)
}

export function getBuffered() { 
  return buffer.slice(); 
}

export function clearBuffer() {
  buffer.length = 0;
}
