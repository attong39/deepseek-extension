import ActionBatcher from "ActionBatcher";
import Key from "Key";
import LRUCache from "LRUCache";
import Map from "Map";
import V from "V";
type Key = string;

export class LRUCache<V> {
  private max: number;
  private map: Map<Key, V>;
  constructor(max = 200) {
    this.max = max;
    this.map = new Map();
  }
  get(k: Key): V | undefined {
    const v = this.map.get(k);
    if (v !== undefined) {
      this.map.delete(k);
      this.map.set(k, v);
    }
    return v;
  }
  set(k: Key, v: V) {
    if (this.map.has(k)) this.map.delete(k);
    this.map.set(k, v);
    if (this.map.size > this.max) {
      const first = this.map.keys().next().value;
      this.map.delete(first);
    }
  }
}

export class ActionBatcher {
  private queue: any[] = [];
  private timer: any = null;
  constructor(
    private flushMs = 25,
    private maxBatch = 50,
  ) {}
  enqueue(action: any, flush: (items: any[]) => void) {
    this.queue.push(action);
    if (this.queue.length >= this.maxBatch) {
      this.flush(flush);
    } else if (!this.timer) {
      this.timer = setTimeout(() => this.flush(flush), this.flushMs);
    }
  }
  private flush(flush: (items: any[]) => void) {
    if (this.timer) {
      clearTimeout(this.timer);
      this.timer = null;
    }
    const items = this.queue.splice(0, this.queue.length);
    if (items.length) flush(items);
  }
}
