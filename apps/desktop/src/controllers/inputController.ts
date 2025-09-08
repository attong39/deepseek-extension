// Input controller placeholder per GUIDE; extend with OS integrations later.
import { requestPermission } from "@/services/permissionManager";
import { guardAction, requiredPermissionsForActionByType } from "@/services/ruleEngine";
import APIs from "APIs";
import AppShortcutPayload from "AppShortcutPayload";
import ClickPayload from "ClickPayload";
import Electron from "Electron";
import GUIDE from "GUIDE";
import High from "High";
import IPC from "IPC";
import Input from "Input";
import InputAction from "InputAction";
import Integrate from "Integrate";
import MoveMousePayload from "MoveMousePayload";
import OS from "OS";
import Optional from "Optional";
import PermissionDialog from "../components/PermissionDialog";
import RobotJS from "RobotJS";
import ScrollPayload from "ScrollPayload";
import Trigger from "Trigger";
import TypeTextPayload from "TypeTextPayload";

export type MoveMousePayload = { x: number; y: number };
export type TypeTextPayload = { text: string };
export type ClickPayload = { button?: "left" | "right" | "middle" };
export type ScrollPayload = { dx?: number; dy?: number };
export type AppShortcutPayload = { appName: string; shortcut: string };

export type InputAction =
  | { type: "move_mouse"; payload: MoveMousePayload }
  | { type: "type_text"; payload: TypeTextPayload }
  | { type: "click"; payload?: ClickPayload }
  | { type: "scroll"; payload?: ScrollPayload }
  | { type: "app_shortcut"; payload: AppShortcutPayload };

export function executeAction(action: InputAction): boolean {
  const gate = guardAction(action);
  if (!gate.allowed) return false;
  // Integrate with OS APIs or native modules (nut.js/RobotJS) via Electron main when available.
  switch (action.type) {
    case "move_mouse": {
      const { x, y } = action.payload;
      console.debug("move_mouse to", x, y);
      return Number.isFinite(x) && Number.isFinite(y);
    }
    case "type_text": {
      const { text } = action.payload;
      console.debug("type_text", text);
      return typeof text === "string";
    }
    case "click": {
      const btn = action.payload?.button ?? "left";
      console.debug("click", btn);
      return ["left", "right", "middle"].includes(btn);
    }
    case "scroll": {
      const dx = action.payload?.dx ?? 0;
      const dy = action.payload?.dy ?? 0;
      console.debug("scroll", dx, dy);
      return Number.isFinite(dx) && Number.isFinite(dy);
    }
    case "app_shortcut": {
      const { appName, shortcut } = action.payload;
      console.debug("app_shortcut", appName, shortcut);
      return (
        typeof appName === "string" &&
        typeof shortcut === "string" &&
        appName.length > 0 &&
        shortcut.length > 0
      );
    }
    default:
      return false;
  }
}

// High-level: execute app-specific shortcut via IPC to main (robot integration placeholder)
export async function executeAppShortcut(appName: string, shortcut: string): Promise<boolean> {
  if (!window.zeta?.input) return false;
  const ok =
    typeof appName === "string" &&
    appName.trim() &&
    typeof shortcut === "string" &&
    shortcut.trim();
  if (!ok) return false;
  const needsConfirm =
    /\b(q|f4|delete)\b/i.test(shortcut) || /(ctrl|control|cmd|command)\+\w+/i.test(shortcut);
  const confirm = needsConfirm
    ? window.confirm?.(`Xác nhận gửi phím tắt quan trọng: ${shortcut}?`) === true
    : false;
  const res = await window.zeta.input.appShortcut(appName, shortcut, confirm);
  return !!res?.ok;
}

export async function panicMode(enable: boolean): Promise<boolean> {
  if (!window.zeta?.input) return false;
  const res = await window.zeta.input.panic(enable);
  return !!res?.ok;
}

// Optional async wrapper: request permissions if missing, then execute
export async function executeActionSafe(action: InputAction): Promise<boolean> {
  const gate = guardAction(action);
  if (gate.allowed) return executeAction(action);
  if (gate.reason !== "permission_denied") return false;
  const needs = requiredPermissionsForActionByType(action.type) ?? [];
  for (const p of needs) {
    // Trigger PermissionDialog via subscription
    // eslint-disable-next-line no-await-in-loop
    await requestPermission(p);
  }
  return executeAction(action);
}
