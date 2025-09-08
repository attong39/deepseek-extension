/* WS test harness – không đụng production. */
import { vi } from "vitest";
import AUTO_OPEN from "AUTO_OPEN";
import ArrayBufferLike from "ArrayBufferLike";
import ArrayBufferView from "ArrayBufferView";
import Blob from "Blob";
import CLOSED from "CLOSED";
import CLOSING from "CLOSING";
import CONNECTING from "CONNECTING";
import CloseEvent from "CloseEvent";
import EH from "EH";
import Event from "Event";
import FakeWebSocket from "FakeWebSocket";
import Map from "Map";
import MessageEvent from "MessageEvent";
import OPEN from "OPEN";
import REGISTRY from "REGISTRY";
import Ready from "Ready";
import Set from "Set";
import URL from "URL";
import WS from "WS";
import WSUrl from "WSUrl";
import WebSocket from "WebSocket";

type EH = (ev: MessageEvent | Event) => void;
type Ready = 0 | 1 | 2 | 3;
type WSUrl = string;

class FakeWebSocket {
  static AUTO_OPEN = true;
  static REGISTRY = new Map<WSUrl, Set<FakeWebSocket>>();

  url: string;
  readyState: Ready = 0; // 0 CONNECTING, 1 OPEN, 2 CLOSING, 3 CLOSED
  onopen: ((ev: Event) => void) | null = null;
  onmessage: ((ev: MessageEvent) => void) | null = null;
  onerror: ((ev: Event) => void) | null = null;
  onclose: ((ev: CloseEvent) => void) | null = null;

  private listeners = new Map<string, Set<EH>>();
  private _sent: Array<string | ArrayBufferLike | Blob | ArrayBufferView> = [];

  constructor(url: string) {
    this.url = url;
    const set = FakeWebSocket.REGISTRY.get(url) ?? new Set();
    set.add(this);
    FakeWebSocket.REGISTRY.set(url, set);
    if (FakeWebSocket.AUTO_OPEN) {
      queueMicrotask(() => this._emitOpen());
    }
  }

  addEventListener(type: string, cb: EH) {
    const set = this.listeners.get(type) ?? new Set();
    set.add(cb);
    this.listeners.set(type, set);
  }
  removeEventListener(type: string, cb: EH) {
    const set = this.listeners.get(type);
    if (set) set.delete(cb);
  }
  private _dispatch(type: string, ev: any) {
    const set = this.listeners.get(type);
    if (set) for (const cb of set) cb(ev);
  }

  send(data: any) { this._sent.push(data); }
  close() {
    if (this.readyState >= 2) return;
    this.readyState = 2;
    queueMicrotask(() => this._emitClose(1000, "normal"));
  }

  // --- driver (từ test)
  _emitOpen() {
    if (this.readyState !== 0) return;
    this.readyState = 1;
    const ev = new Event("open");
    this.onopen?.(ev);
    this._dispatch("open", ev);
  }
  _emitMessage(data: any) {
    const ev = new MessageEvent("message", { data });
    this.onmessage?.(ev);
    this._dispatch("message", ev);
  }
  _emitError(err?: any) {
    const ev = new Event("error");
    (ev as any).error = err;
    this.onerror?.(ev);
    this._dispatch("error", ev);
  }
  _emitClose(code = 1000, reason = "close") {
    this.readyState = 3;
    const ev = new CloseEvent("close", { code, reason, wasClean: true });
    this.onclose?.(ev);
    this._dispatch("close", ev);
    const set = FakeWebSocket.REGISTRY.get(this.url);
    if (set) set.delete(this);
  }

  // tiện cho assert
  _sentMessages() { return [...this._sent]; }
}

export function installWsMock() {
  vi.stubGlobal("WebSocket", FakeWebSocket as unknown as typeof WebSocket);
}

export function resetWsMock() {
  // đóng mọi socket còn mở & dọn registry
  for (const set of FakeWebSocket.REGISTRY.values()) {
    for (const ws of set) ws._emitClose();
  }
  FakeWebSocket.REGISTRY.clear();
}

/** Điều khiển nhóm socket theo URL */
export const WS = {
  registry() { return FakeWebSocket.REGISTRY; },
  sockets(url: string) { return [...(FakeWebSocket.REGISTRY.get(url) ?? [])]; },
  openAll(url: string) { for (const ws of WS.sockets(url)) ws._emitOpen(); },
  broadcast(url: string, data: any) { for (const ws of WS.sockets(url)) ws._emitMessage(data); },
};
