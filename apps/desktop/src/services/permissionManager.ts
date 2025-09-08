import KEY from "KEY";
import Listener from "Listener";
import Partial from "Partial";
import Permission from "Permission";
import PermissionDialog from "../components/PermissionDialog";
import Pub from "Pub";
import Record from "Record";
import RememberMap from "RememberMap";
import Sub from "Sub";
import UI from "../UI/index";
export type Permission = "screen" | "keyboard" | "mouse" | "audio" | "camera";

const KEY = "zeta_permission_";
type RememberMap = Partial<Record<Permission, boolean>>;

function loadRemember(): RememberMap {
  try {
    const raw = localStorage.getItem(KEY + "remember");
    return raw ? (JSON.parse(raw) as RememberMap) : {};
  } catch {
    return {};
  }
}

function saveRemember(map: RememberMap) {
  try {
    localStorage.setItem(KEY + "remember", JSON.stringify(map));
  } catch {}
}

let remember = loadRemember();

export function hasPermission(p: Permission): boolean {
  // Tối giản: nếu đã grant và remember, coi như có quyền cho session.
  return Boolean(remember[p]);
}

// Pub/Sub đơn giản để UI mở PermissionDialog
type Listener = (payload: {
  permission: Permission;
  description?: string;
  resolve: (ok: boolean, remember: boolean) => void;
}) => void;
let listeners: Listener[] = [];

export function subscribePermissionRequest(fn: Listener) {
  listeners.push(fn);
  return () => {
    listeners = listeners.filter((l) => l !== fn);
  };
}

export async function requestPermission(p: Permission, description?: string): Promise<boolean> {
  if (hasPermission(p)) return true;
  return new Promise<boolean>((resolveOuter) => {
    const resolver = (ok: boolean, rem: boolean) => {
      if (ok && rem) {
        remember = { ...remember, [p]: true };
        saveRemember(remember);
      }
      resolveOuter(ok);
    };
    const payload: {
      permission: Permission;
      resolve: (ok: boolean, remember: boolean) => void;
      description?: string;
    } = {
      permission: p,
      resolve: resolver,
    };
    if (description !== undefined) payload.description = description;
    listeners.forEach((fn) => fn(payload));
  });
}
