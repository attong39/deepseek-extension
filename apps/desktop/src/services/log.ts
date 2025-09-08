import A from "A";
import ERROR from "ERROR";
import INFO from "INFO";
import PII from "PII";
import REDACTED from "REDACTED";
import SECRET from "SECRET";
import WARN from "WARN";
import Za from "Za";
const SECRET = [/sk-[A-Za-z0-9]{20,}/g, /(?<=password=)[^&]+/gi];
const PII = [/\b\d{9,12}\b/g, /\b[\w.-]+@[\w.-]+\.\w+\b/g];

export function maskPII(input: unknown): string {
  let s = typeof input === "string" ? input : JSON.stringify(input);
  [...SECRET, ...PII].forEach((re) => (s = s.replace(re, "[REDACTED]")));
  return s;
}

export const log = {
  info: (...a: unknown[]) => console.info("[INFO]", ...a.map(maskPII)),
  warn: (...a: unknown[]) => console.warn("[WARN]", ...a.map(maskPII)),
  error: (...a: unknown[]) => console.error("[ERROR]", ...a.map(maskPII)),
};
