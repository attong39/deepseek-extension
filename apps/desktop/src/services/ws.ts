import ArrayBufferLike from "ArrayBufferLike";
import ArrayBufferView from "ArrayBufferView";
import Blob from "Blob";
import Math from "Math";
import MessageEvent from "MessageEvent";
import Omit from "Omit";
import Required from "Required";
import VITE_APP_ENV from "VITE_APP_ENV";
import VITE_DEV_ALLOW_WS_NO_TOKEN from "VITE_DEV_ALLOW_WS_NO_TOKEN";
import VITE_WS_URL from "VITE_WS_URL";
import WSOptions from "WSOptions";
import WSStatus from "WSStatus";
import WebSocket from "./WebSocket";
import WebSocketManager from "WebSocketManager";
export type WSStatus = "idle" | "connecting" | "connected" | "error" | "closed";

export type WSOptions = {
  path?: string; // '/ws/chat'
  token?: string | null;
  onMessage?: (ev: MessageEvent) => void;
  onStatusChange?: (s: WSStatus) => void;
  maxRetries?: number;
};

export class WebSocketManager {
  private ws: WebSocket | null = null;
  private retries = 0;
  private status: WSStatus = "idle";
  private readonly opts: Required<Omit<WSOptions, "token" | "onMessage" | "onStatusChange">> & {
    token?: string | null;
    onMessage?: (ev: MessageEvent) => void;
    onStatusChange?: (s: WSStatus) => void;
  };

  constructor(opts: WSOptions) {
    this.opts = { path: "/ws/chat", maxRetries: 10, ...opts };
  }

  private setStatus(s: WSStatus) {
    this.status = s;
    this.opts.onStatusChange?.(s);
  }

  connect() {
    const base = import.meta.env.VITE_WS_URL;
    const allowNoToken =
      import.meta.env.VITE_DEV_ALLOW_WS_NO_TOKEN === "true" &&
      import.meta.env.VITE_APP_ENV === "development";
    let qs = "";
    if (this.opts.token) {
      qs = `?token=${encodeURIComponent(this.opts.token)}`;
    } else if (!allowNoToken) {
      qs = "?token=";
    }
    const url = `${base}${this.opts.path}${qs}`;

    this.setStatus("connecting");
    this.ws = new WebSocket(url);

    this.ws.onopen = () => {
      this.retries = 0;
      this.setStatus("connected");
    };
    this.ws.onmessage = (ev) => this.opts.onMessage?.(ev);
    this.ws.onerror = () => {
      this.setStatus("error");
    };
    this.ws.onclose = () => {
      if (this.status !== "closed") {
        this.reconnect();
      }
    };
  }

  private reconnect() {
    if (this.retries >= (this.opts.maxRetries ?? 10)) {
      this.setStatus("closed");
      return;
    }
    this.retries += 1;
    const delay = Math.min(30000, 1000 * Math.pow(2, this.retries)); // exponential backoff
    setTimeout(() => this.connect(), delay);
  }

  send(data: string | ArrayBufferLike | Blob | ArrayBufferView) {
    if (this.ws && this.status === "connected") this.ws.send(data as any);
  }

  close() {
    this.setStatus("closed");
    this.ws?.close();
    this.ws = null;
  }

  getStatus() {
    return this.status;
  }
}
