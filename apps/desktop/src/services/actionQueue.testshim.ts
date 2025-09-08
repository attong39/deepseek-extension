/**
 * Test-only ActionQueue: chạy ngay lập tức để tránh flake do timer.
 * Alias trong vitest.config.ts: "@/services/actionQueue"
 */
import type { InputAction } from "../controllers/inputController";
import ActionQueue from "./ActionQueue";
import Alias from "Alias";
import Execute from "Execute";
import For from "For";
import Process from "Process";
import Runner from "Runner";
import Set from "Set";
import ShouldCancel from "ShouldCancel";
import Test from "../Test/index";

type Runner = (action: InputAction) => Promise<boolean> | boolean;
type ShouldCancel = () => boolean;

class ActionQueue {
  private q: InputAction[] = [];
  private running = false;
  private enabled = false;
  private runner: Runner | null = null;
  private shouldCancel: ShouldCancel | null = null;
  private readonly listeners = new Set<(size: number) => void>();

  setRunner(fn: Runner) {
    this.runner = fn;
  }

  setShouldCancel(fn: ShouldCancel) {
    this.shouldCancel = fn;
  }

  enable() {
    this.enabled = true;
    // Process any pending items immediately in test
    this.drainSync();
  }

  disable() {
    this.enabled = false;
  }

  clear() {
    this.q = [];
    this.running = false;
    this.emit();
  }

  size() {
    return this.q.length;
  }

  enqueue(action: InputAction) {
    this.q.push(action);
    this.emit();
    if (this.enabled && !this.running) {
      // Process synchronously for test predictability
      this.drainSync();
    }
  }

  private drainSync() {
    if (this.running || !this.enabled) return;
    this.running = true;
    try {
      while (this.enabled && this.q.length > 0) {
        if (this.shouldCancel?.()) {
          this.q = [];
          this.emit();
          break;
        }
        const item = this.q.shift()!;
        this.emit();
        try {
          if (this.runner) {
            // Execute synchronously for tests
            const result = this.runner(item);
            if (result instanceof Promise) {
              // For tests, we still want immediate processing
              result.catch(() => {}); // swallow async errors
            }
          }
        } catch (e) {
          console.warn("actionQueue runner error", e);
        }
      }
    } finally {
      this.running = false;
    }
  }

  private async drain() {
    if (this.running || !this.enabled) return;
    this.running = true;
    try {
      while (this.enabled && this.q.length > 0) {
        if (this.shouldCancel?.()) {
          this.q = [];
          this.emit();
          break;
        }
        const item = this.q.shift()!;
        this.emit();
        try {
          if (this.runner) {
            await this.runner(item);
          }
        } catch (e) {
          console.warn("actionQueue runner error", e);
        }
      }
    } finally {
      this.running = false;
    }
  }

  subscribe(cb: (size: number) => void) {
    this.listeners.add(cb);
    cb(this.size());
    return () => this.listeners.delete(cb);
  }

  private emit() {
    const s = this.size();
    for (const cb of this.listeners) {
      try {
        cb(s);
      } catch {
        /* noop */
      }
    }
  }
}

export const actionQueue = new ActionQueue();
