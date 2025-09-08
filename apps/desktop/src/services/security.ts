import AllowedIPCChannel from "AllowedIPCChannel";
import Allowlist from "Allowlist";
import App from "../App";
import CSP_DEV from "CSP_DEV";
import CSP_PROD from "CSP_PROD";
import CSS from "CSS";
import Content from "Content";
import ELECTRON_SECURITY from "ELECTRON_SECURITY";
import Electron from "Electron";
import File from "File";
import HMR from "HMR";
import Headers from "Headers";
import IPC from "IPC";
import IPC_ALLOWLIST from "IPC_ALLOWLIST";
import JS from "JS";
import Logs from "../pages/Logs";
import Policy from "Policy";
import Record from "Record";
import SECURITY from "./SECURITY";
import Security from "./Security";
import Settings from "./Settings";
import Training from "./Training";
import Validate from "Validate";
import Window from "Window";
/**
 * Content Security Policy và Security Headers cho Electron
 */

export const CSP_DEV = {
  "default-src": ["'self'"],
  "script-src": ["'self'", "'unsafe-eval'", "'unsafe-inline'"], // HMR needs unsafe-eval
  "style-src": ["'self'", "'unsafe-inline'"],
  "img-src": ["'self'", "data:", "blob:", "https:"],
  "font-src": ["'self'", "data:"],
  "connect-src": ["'self'", "ws:", "wss:", "http://localhost:*", "ws://localhost:*"],
  "worker-src": ["'self'", "blob:"],
};

export const CSP_PROD = {
  "default-src": ["'self'"],
  "script-src": ["'self'"],
  "style-src": ["'self'", "'unsafe-inline'"], // CSS-in-JS needs this
  "img-src": ["'self'", "data:", "blob:"],
  "font-src": ["'self'", "data:"],
  "connect-src": ["'self'", "wss:", "https:"],
  "worker-src": ["'self'"],
  "object-src": ["'none'"],
  "base-uri": ["'self'"],
  "form-action": ["'self'"],
  "frame-ancestors": ["'none'"],
};

function buildCSPString(policy: Record<string, string[]>): string {
  return Object.entries(policy)
    .map(([directive, sources]) => `${directive} ${sources.join(" ")}`)
    .join("; ");
}

export function getCSPHeader(isDev: boolean): string {
  return buildCSPString(isDev ? CSP_DEV : CSP_PROD);
}

/**
 * Security headers for Electron webPreferences
 */
export const ELECTRON_SECURITY = {
  nodeIntegration: false,
  contextIsolation: true,
  enableRemoteModule: false,
  sandbox: true,
  webSecurity: true,
  allowRunningInsecureContent: false,
  experimentalFeatures: false,
};

/**
 * IPC Allowlist - chỉ những channel này được phép
 */
export const IPC_ALLOWLIST = [
  // Window controls
  "window:minimize",
  "window:maximize", 
  "window:close",
  "window:focus",
  
  // File operations
  "file:open-dialog",
  "file:save-dialog",
  "file:read",
  "file:write",
  
  // App info
  "app:get-version",
  "app:get-platform",
  "app:restart",
  
  // Training
  "training:start",
  "training:stop",
  "training:get-status",
  
  // Settings
  "settings:get",
  "settings:set",
  
  // Logs
  "logs:get",
  "logs:clear",
] as const;

export type AllowedIPCChannel = typeof IPC_ALLOWLIST[number];

/**
 * Validate IPC channel against allowlist
 */
export function validateIPCChannel(channel: string): channel is AllowedIPCChannel {
  return IPC_ALLOWLIST.includes(channel as AllowedIPCChannel);
}

/**
 * Security audit log
 */
export function logSecurityEvent(event: string, details?: Record<string, unknown>): void {
  console.warn(`[SECURITY] ${event}`, details ? JSON.stringify(details) : "");
}
