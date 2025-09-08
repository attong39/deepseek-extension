import { hasPermission } from "@services/permissionManager";

import type { InputAction } from "@/controllers/inputController";
import { RateLimiter } from "@/utils/rateLimiter";
import API from "./API/index";
import AllowedRegion from "AllowedRegion";
import For from "For";
import Math from "Math";
import Mouse from "Mouse";
import OS from "OS";
import Optionally from "Optionally";
import Partial from "Partial";
import Permission from "Permission";
import Rate from "Rate";
import RuleContext from "RuleContext";
import Safety from "Safety";
import SafetyConfig from "SafetyConfig";
import Shortcut from "Shortcut";

export type RuleContext = {
  requires?: Array<"screen" | "mouse" | "keyboard" | "audio" | "camera">;
};

export function canExecute(ctx: RuleContext): boolean {
  if (!ctx.requires || ctx.requires.length === 0) return true;
  return ctx.requires.every((r) => hasPermission(r));
}

// ---- Safety config & guard ----

type AllowedRegion = { x1: number; y1: number; x2: number; y2: number };

type SafetyConfig = {
  blockedShortcuts: string[]; // normalized lower-case tokens like "alt+f4", "cmd+q", "ctrl+q"
  allowedRegion?: AllowedRegion; // if set, mouse actions must be inside
  rate: { capacity: number; refillPerSec: number };
};

const cfg: SafetyConfig = {
  blockedShortcuts: ["alt+f4", "cmd+q", "control+q", "ctrl+q"],
  rate: { capacity: 10, refillPerSec: 10 },
};

let limiter = new RateLimiter(cfg.rate.capacity, cfg.rate.refillPerSec);

export function configureSafety(partial: Partial<SafetyConfig>): void {
  if (partial.blockedShortcuts) cfg.blockedShortcuts = [...partial.blockedShortcuts];
  if (partial.allowedRegion) cfg.allowedRegion = partial.allowedRegion;
  if (partial.rate) {
    cfg.rate = partial.rate;
    limiter = new RateLimiter(cfg.rate.capacity, cfg.rate.refillPerSec);
  }
}

export function requiredPermissionsForActionByType(
  a: InputAction["type"],
): RuleContext["requires"] {
  switch (a) {
    case "move_mouse":
    case "click":
    case "scroll":
      return ["mouse"];
    case "type_text":
    case "app_shortcut":
      return ["keyboard"];
    default:
      return [];
  }
}

function isInsideRegion(x: number, y: number, region: AllowedRegion): boolean {
  const { x1, y1, x2, y2 } = region;
  return (
    x >= Math.min(x1, x2) && x <= Math.max(x1, x2) && y >= Math.min(y1, y2) && y <= Math.max(y1, y2)
  );
}

export function guardAction(action: InputAction): {
  allowed: boolean;
  reason?: string;
} {
  // Permission gate
  const needs = requiredPermissionsForActionByType(action.type) ?? [];
  if (!canExecute({ requires: needs })) {
    return { allowed: false, reason: "permission_denied" };
  }

  // Rate limit
  if (!limiter.allow(1)) {
    return { allowed: false, reason: "rate_limited" };
  }

  // Shortcut safety
  if (action.type === "app_shortcut") {
    const raw = `${action.payload?.shortcut ?? ""}`.toLowerCase();
    const norm = raw
      .replace(/\s+/g, "")
      .replace(/cmd/gi, "cmd")
      .replace(/control/gi, "control")
      .replace(/ctrl/gi, "ctrl");
    if (cfg.blockedShortcuts.some((s) => norm.includes(s))) {
      return { allowed: false, reason: "blocked_shortcut" };
    }
  }

  // Mouse region constraint
  if (cfg.allowedRegion) {
    if (action.type === "move_mouse") {
      const { x, y } = action.payload;
      if (!isInsideRegion(x, y, cfg.allowedRegion))
        return { allowed: false, reason: "outside_allowed_region" };
    }
    if (action.type === "click") {
      // For click we cannot read coordinates here unless integrated; assume prior move_mouse positioned cursor.
      // Optionally, integrate OS API to read cursor position.
    }
  }

  return { allowed: true };
}
