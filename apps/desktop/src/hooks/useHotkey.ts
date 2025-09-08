import { useEffect, useRef } from "react";
import Hotkey from "Hotkey";
import Implementation from "Implementation";
import KeyboardEvent from "KeyboardEvent";
import Overloads from "Overloads";

export type Hotkey = {
  key: string;
  ctrl?: boolean;
  shift?: boolean;
  alt?: boolean;
};

// Overloads
export function useHotkey(hotkey: Hotkey, handler: () => void): void;
export function useHotkey(key: string, handler: () => void): void;

// Implementation
export function useHotkey(arg: Hotkey | string, handler: () => void): void {
  const handlerRef = useRef(handler);
  handlerRef.current = handler;

  const hk: Hotkey = typeof arg === "string" ? { key: arg } : arg;

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (hk.ctrl && !e.ctrlKey) return;
      if (hk.shift && !e.shiftKey) return;
      if (hk.alt && !e.altKey) return;
      if (e.key.toLowerCase() !== hk.key.toLowerCase()) return;
      e.preventDefault();
      handlerRef.current();
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [hk.ctrl, hk.shift, hk.alt, hk.key]);
}
