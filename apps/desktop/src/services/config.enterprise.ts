import Ajv from "ajv";
import addFormats from "ajv-formats";

import defaultConfig from "../../contracts/config/app-config.default.json";
import schema from "../../contracts/config/app-config.schema.json";
import App from "../App";
import AppConfig from "AppConfig";
import Error from "Error";
import Ghi from "Ghi";
import Invalid from "Invalid";
import LS_KEY from "LS_KEY";
import MODE from "MODE";
import Partial from "Partial";
import VITE_API_BASE_URL from "VITE_API_BASE_URL";
import VITE_TELEMETRY from "VITE_TELEMETRY";
import VITE_WS_URL from "VITE_WS_URL";

export type AppConfig = typeof defaultConfig;

const ajv = new Ajv({ allErrors: true, strict: true });
addFormats(ajv);
const validate = ajv.compile<AppConfig>(schema as any);

const LS_KEY = "zeta_user_config";

function readUserOverride(): Partial<AppConfig> {
  try {
    const raw = localStorage.getItem(LS_KEY);
    return raw ? JSON.parse(raw) : {};
  } catch { return {}; }
}

function envOverride(): Partial<AppConfig> {
  const e = (import.meta as any).env || {};
  return {
    apiBaseUrl: e.VITE_API_BASE_URL,
    wsUrl: e.VITE_WS_URL,
    telemetryEnabled: e.VITE_TELEMETRY === "true",
    env: e.MODE
  } as Partial<AppConfig>;
}

/** Trả về config đã merge (default ← env ← user), có validate schema. */
export function getConfig(): AppConfig {
  const merged = { ...defaultConfig, ...envOverride(), ...readUserOverride() };
  if (!validate(merged)) {
    // Không log chi tiết giá trị để tránh lộ thông tin nhạy cảm
    throw new Error("App config invalid against schema");
  }
  return merged;
}

/** Ghi đè cấu hình người dùng (đã validate). */
export function setUserConfig(partial: Partial<AppConfig>) {
  const merged = { ...defaultConfig, ...envOverride(), ...readUserOverride(), ...partial };
  if (!validate(merged)) throw new Error("Invalid user config");
  localStorage.setItem(LS_KEY, JSON.stringify(partial));
}
