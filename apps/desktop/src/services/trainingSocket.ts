/* Dedicated training progress socket for /ws/training/{job_id} */
import { DEFAULT_API_BASE_URL } from "../constants";
import Dedicated from "Dedicated";
import Event from "Event";
import Listener from "Listener";
import OPEN from "OPEN";
import Set from "Set";
import TrainingAny from "TrainingAny";
import TrainingCompleted from "TrainingCompleted";
import TrainingError from "TrainingError";
import TrainingProgress from "TrainingProgress";
import TrainingSocket from "./TrainingSocket";
import URL from "URL";
import WebSocket from "./WebSocket";

export type TrainingProgress = {
  type: "training.progress";
  jobId: string;
  progress: number;
  message?: string;
};

export type TrainingCompleted = {
  type: "training.completed";
  jobId: string;
  artifactUrl?: string;
};

export type TrainingError = {
  type: "training.error";
  jobId: string;
  code?: string;
  message?: string;
};

export type TrainingAny = TrainingProgress | TrainingCompleted | TrainingError;

type Listener = (e: TrainingAny | Event) => void;

export class TrainingSocket {
  private ws: WebSocket | null = null;
  private listeners = new Set<Listener>();

  constructor(private jobId: string) {}

  private buildUrl(): string {
    try {
      const base = new URL(DEFAULT_API_BASE_URL);
      base.protocol = base.protocol === "https:" ? "wss:" : "ws:";
      base.pathname = `/ws/training/${encodeURIComponent(this.jobId)}`;
      return base.toString();
    } catch {
      return `ws://127.0.0.1:8000/ws/training/${encodeURIComponent(this.jobId)}`;
    }
  }

  connect() {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) return;
    const ws = new WebSocket(this.buildUrl());
    this.ws = ws;
    ws.onmessage = (evt) => {
      try {
        const data = JSON.parse(String(evt.data));
        this.emit(data as TrainingAny);
      } catch {
        this.emit(evt);
      }
    };
    ws.onerror = (e) => this.emit(e);
    ws.onclose = (e) => this.emit(e);
  }

  on(cb: Listener) {
    this.listeners.add(cb);
    return () => this.listeners.delete(cb);
  }

  private emit(e: TrainingAny | Event) {
    this.listeners.forEach((cb) => cb(e));
  }

  close() {
    this.ws?.close();
  }
}

export function connectTraining(jobId: string) {
  const s = new TrainingSocket(jobId);
  s.connect();
  return s;
}
