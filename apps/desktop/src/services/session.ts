import Listener from "Listener";
import Math from "Math";
import Optional from "Optional";
import RefreshHandler from "RefreshHandler";
import ReturnType from "ReturnType";
import Session from "./Session";
import SessionManager from "SessionManager";
import SessionState from "SessionState";
import Set from "Set";
/* Session manager: token persistence, listeners, refresh, clock-skew guard */

export type SessionState = {
  token: string | null;
  expiresAt: number | null; // epoch ms
};

type Listener = (s: SessionState) => void;
type RefreshHandler = () => Promise<{
  token: string;
  expiresAt?: number;
} | null>;

class SessionManager {
  private state: SessionState = { token: null, expiresAt: null };
  private readonly listeners = new Set<Listener>();
  private refreshFn: RefreshHandler | null = null;
  private timer: ReturnType<typeof setTimeout> | null = null;
  private skewMs = 0; // serverNow - clientNow
  private readonly skewGuardSec = 60; // refresh 60s before expiry

  constructor() {
    try {
      const token = localStorage.getItem("zeta_token");
      this.state.token = token;
      // Optional: persisted expiry if you save it under key
      const exp = localStorage.getItem("zeta_token_exp");
      this.state.expiresAt = exp ? Number(exp) : null;
      this.schedule();
    } catch {
      /* noop */
    }
  }

  now() {
    return Date.now() + this.skewMs;
  }

  setServerTime(serverNowMs: number) {
    this.skewMs = serverNowMs - Date.now();
  }

  setRefreshHandler(fn: RefreshHandler | null) {
    this.refreshFn = fn;
    this.schedule();
  }

  getToken() {
    return this.state.token;
  }

  getState() {
    return { ...this.state };
  }

  setToken(token: string | null, expiresAt?: number | null) {
    this.state = { token, expiresAt: expiresAt ?? null };
    try {
      if (token) localStorage.setItem("zeta_token", token);
      else localStorage.removeItem("zeta_token");
      if (this.state.expiresAt)
        localStorage.setItem("zeta_token_exp", String(this.state.expiresAt));
      else localStorage.removeItem("zeta_token_exp");
    } catch {
      /* noop */
    }
    this.emit();
    this.schedule();
  }

  subscribe(cb: Listener) {
    this.listeners.add(cb);
    cb(this.state);
    return () => this.listeners.delete(cb);
  }

  private emit() {
    this.listeners.forEach((cb) => cb(this.state));
  }

  private clearTimer() {
    if (this.timer) clearTimeout(this.timer);
    this.timer = null;
  }

  private schedule() {
    this.clearTimer();
    const { expiresAt, token } = this.state;
    if (!token || !expiresAt || !this.refreshFn) return;
    const now = this.now();
    const refreshAt = Math.max(0, expiresAt - this.skewGuardSec * 1000);
    const delay = Math.max(0, refreshAt - now);
    this.timer = setTimeout(() => {
      this.tryRefresh().catch(() => undefined);
    }, delay);
  }

  private async tryRefresh() {
    if (!this.refreshFn) return;
    const res = await this.refreshFn();
    if (res?.token) {
      this.setToken(res.token, res.expiresAt ?? null);
    } else {
      // if refresh not available, and token expired, clear
      const now = this.now();
      if (this.state.expiresAt && now >= this.state.expiresAt) {
        this.setToken(null, null);
      } else {
        // schedule another attempt in 30s
        this.timer = setTimeout(() => this.tryRefresh().catch(() => undefined), 30000);
      }
    }
  }
}

export const session = new SessionManager();
