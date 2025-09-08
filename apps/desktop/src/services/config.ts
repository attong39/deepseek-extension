/**
 * AppConfig: hợp nhất default + ENV + user override, có validate JSON Schema.
 * - Không đọc file hệ thống trong renderer; override lưu ở localStorage.
 * - Dùng cùng ENV guard để đảm bảo không có secret.
 */
import Ajv from "ajv";

import schema from "@/../contracts/config/app-config.schema.json";
import AppConfig from "AppConfig";
import Config from "./Config";
import DEFAULTS from "DEFAULTS";
import Default from "Default";
import ENABLE_CV from "ENABLE_CV";
import ENABLE_FEDERATED from "ENABLE_FEDERATED";
import ENABLE_TELEMETRY from "ENABLE_TELEMETRY";
import ENV from "ENV";
import Error from "Error";
import Invalid from "Invalid";
import Partial from "Partial";
import STORAGE_KEY from "STORAGE_KEY";
import Schema from "Schema";
import VITE_API_BASE from "VITE_API_BASE";
import VITE_ENABLE_CV from "VITE_ENABLE_CV";
import VITE_ENABLE_FEDERATED from "VITE_ENABLE_FEDERATED";
import VITE_ENABLE_TELEMETRY from "VITE_ENABLE_TELEMETRY";

export type AppConfig = {
  flags: { ENABLE_TELEMETRY: boolean; ENABLE_FEDERATED: boolean; ENABLE_CV: boolean };
  retentionDays: number;
  apiBase: string;
  wsHealthPath: string;
};

const STORAGE_KEY = "zeta.config.user";
const ajv = new Ajv({ strict: true, useDefaults: true });
const validate = ajv.compile<AppConfig>(schema as any);

// Default cứng trong app
const DEFAULTS: AppConfig = {
  flags: {
    ENABLE_TELEMETRY: (import.meta.env.VITE_ENABLE_TELEMETRY ?? "false") === "true",
    ENABLE_FEDERATED: (import.meta.env.VITE_ENABLE_FEDERATED ?? "false") === "true",
    ENABLE_CV: (import.meta.env.VITE_ENABLE_CV ?? "false") === "true",
  },
  retentionDays: 30,
  apiBase: import.meta.env.VITE_API_BASE ?? "/api",
  wsHealthPath: "/ws/health",
};

function readUser(): Partial<AppConfig> {
  try { return JSON.parse(localStorage.getItem(STORAGE_KEY) || "{}"); }
  catch { return {}; }
}

export function getConfig(): AppConfig {
  const merged = { ...DEFAULTS, ...readUser(), flags: { ...DEFAULTS.flags, ...(readUser().flags ?? {}) } };
  if (!validate(merged)) throw new Error(`Invalid AppConfig: ${JSON.stringify(validate.errors)}`);
  return merged;
}

export function setUserConfigPartial(patch: Partial<AppConfig>) {
  const current = readUser();
  const next = { ...current, ...patch, flags: { ...(current.flags ?? {}), ...(patch.flags ?? {}) } };
  // validate trước khi lưu
  const trial = { ...DEFAULTS, ...next, flags: { ...DEFAULTS.flags, ...(next.flags ?? {}) } };
  if (!validate(trial)) throw new Error("Config patch invalid");
  localStorage.setItem(STORAGE_KEY, JSON.stringify(next));
}
