// Hàng đợi tác vụ đơn giản cho InputAction
// - Không bật mặc định; cho phép enable/disable runtime
// - Cho phép inject runner(action) và shouldCancel() để tích hợp với command handler và Emergency Stop

import type { InputAction } from "../controllers/inputController";
import ActionQueue from "./ActionQueue";
import Cho from "Cho";
import Emergency from "./Emergency";
import Flush from "Flush";
import Kick from "Kick";
import Runner from "Runner";
import Set from "Set";
import ShouldCancel from "ShouldCancel";
import Stop from "Stop";

type Runner = (action: InputAction) => Promise<boolean> | boolean;
type ShouldCancel = () => boolean;

class ActionQueue {
  private q: InputAction[] = [];
  private processing = false;
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
    // Kick processing if there are pending items
    void this.process();
  }

  disable() {
    this.enabled = false;
  }

  clear() {
    this.q = [];
    this.processing = false;
    this.emit();
  }

  size() {
    return this.q.length;
  }

  enqueue(action: InputAction) {
    this.q.push(action);
    this.emit();
    if (this.enabled) void this.process();
  }

  private async process() {
    if (this.processing || !this.enabled) return;
    this.processing = true;
    try {
      while (this.enabled && this.q.length > 0) {
        if (this.shouldCancel?.()) {
          // Flush queue on cancel
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
          // swallow per-item errors; continue next
          // eslint-disable-next-line no-console
          console.warn("actionQueue runner error", e);
        }
        // yield to event loop
        await new Promise((r) => setTimeout(r, 0));
      }
    } finally {
      this.processing = false;
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
