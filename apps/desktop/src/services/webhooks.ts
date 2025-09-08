import Content from "Content";
import POST from "POST";
import SUB_KEY from "SUB_KEY";
import Type from "Type";
import WebhookEvent from "WebhookEvent";
import Webhooks from "./Webhooks";
/* Webhooks dispatch with simple retries */

export type WebhookEvent = { type: string; ts?: number; payload?: unknown };

const SUB_KEY = "zeta_webhooks_subs_v1";

function load(): string[] {
  try {
    return JSON.parse(localStorage.getItem(SUB_KEY) || "[]") as string[];
  } catch {
    return [];
  }
}
function save(list: string[]) {
  try {
    localStorage.setItem(SUB_KEY, JSON.stringify(list));
  } catch {
    /* noop */
  }
}

let targets: string[] = load();

export const webhooks = {
  subscribe(url: string) {
    if (!targets.includes(url)) {
      targets.push(url);
      save(targets);
    }
  },
  unsubscribe(url: string) {
    targets = targets.filter((t) => t !== url);
    save(targets);
  },
  list() {
    return [...targets];
  },
  async emit(event: WebhookEvent) {
    const body = JSON.stringify({ ...event, ts: event.ts ?? Date.now() });
    await Promise.all(
      targets.map(async (url) => {
        for (let i = 0; i < 3; i++) {
          try {
            const res = await fetch(url, {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body,
            });
            if (res.ok) return;
          } catch {
            /* retry */
          }
          await new Promise((r) => setTimeout(r, 500 * (i + 1)));
        }
      }),
    );
  },
};
