/* Simple WebSocket client + event bus with backoff reconnect. */
import { validateWsMessage } from "../api/wsSchema";
import { DEFAULT_WS_URL } from "../constants";
import { analytics } from "./analytics";
import { webhooks } from "./webhooks";
import Hook from "Hook";
import Listener from "Listener";
import Map from "Map";
import Math from "Math";
import OPEN from "OPEN";
import ReturnType from "ReturnType";
import Set from "Set";
import Simple from "Simple";
import SocketBus from "SocketBus";
import UI from "../UI/index";
import WebSocket from "./WebSocket";
import WsMessage from "WsMessage";

export type WsMessage =
  | { type: "assistant_reply"; content: string; timestamp?: string }
  | { type: "action"; payload: unknown }
  | { type: "ping"; ts: number }
  | { type: "pong"; ts: number }
  | { type: string; [k: string]: unknown };

type Listener = (data: unknown) => void;

class SocketBus {
  private ws: WebSocket | null = null;
  private readonly listeners = new Map<string, Set<Listener>>();
  private backoff = 1000;
  private reconnectTimer: ReturnType<typeof setTimeout> | null = null;
  private connecting = false;

  connect(url?: string) {
    if (this.connecting) return;
    this.connecting = true;
    const token = localStorage.getItem("zeta_token");
    const full = (url || DEFAULT_WS_URL) + (token ? `?token=${encodeURIComponent(token)}` : "");
    try {
      const ws = new WebSocket(full);
      this.ws = ws;
      ws.onopen = () => {
        this.backoff = 1000;
        this.connecting = false;
        this.emit("open", {});
        analytics.wsReconnect();
        void webhooks.emit({ type: "ws_open" });
      };
      ws.onclose = () => {
        this.emit("close", {});
        this.scheduleReconnect();
        void webhooks.emit({ type: "ws_close" });
      };
      ws.onerror = (e) => this.emit("error", e);
      ws.onmessage = (evt) => {
        let data: unknown = evt.data;
        try {
          data = JSON.parse(String(evt.data));
        } catch {
          // raw message
        }
        // basic validation
        if (!validateWsMessage(data)) return;
        this.emit("message", data);
        if (data && (data as any).type) {
          void webhooks.emit({ type: "ws_message", payload: data });
          if ((data as any).type === "emergency.stop") {
            // Hook: notify globally; UI/command handler can subscribe to stop batch actions
            void webhooks.emit({ type: "emergency.stop", payload: (data as any).payload });
          }
        }
      };
    } finally {
      this.connecting = false;
    }
  }

  private scheduleReconnect() {
    if (this.reconnectTimer) clearTimeout(this.reconnectTimer);
    this.reconnectTimer = setTimeout(() => {
      this.backoff = Math.min(this.backoff * 2, 30000);
      this.connect();
    }, this.backoff);
  }

  send(payload: unknown) {
    if (!this.ws || this.ws.readyState !== WebSocket.OPEN) return false;
    const data = typeof payload === "string" ? payload : JSON.stringify(payload);
    this.ws.send(data);
    return true;
  }

  on(event: "open" | "close" | "error" | "message", cb: Listener) {
    const set = this.listeners.get(event) ?? new Set<Listener>();
    set.add(cb);
    this.listeners.set(event, set);
    return () => this.off(event, cb);
  }

  off(event: "open" | "close" | "error" | "message", cb: Listener) {
    this.listeners.get(event)?.delete(cb);
  }

  private emit(event: string, data: unknown) {
    this.listeners.get(event)?.forEach((cb) => cb(data));
  }
}

export const socketBus = new SocketBus();
