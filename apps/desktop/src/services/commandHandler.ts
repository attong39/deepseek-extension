import { actionQueue } from "./actionQueue";
import { canExecute } from "./ruleEngine";
import { socketBus } from "./socket";
import { fetchFromArXiv, fetchFromWikipedia, parseArXivAtom } from "../api/apiClient";
import { executeAction, type InputAction } from "../controllers/inputController";
import { useSearchStore } from "../stores/searchStore";
import Batch from "Batch";
import Blocked from "Blocked";
import Emergency from "./Emergency";
import Expect from "Expect";
import Fire from "Fire";
import Flush from "Flush";
import Handle from "Handle";
import InputAction from "InputAction";
import Push from "Push";
import Rule from "Rule";
import Stop from "Stop";
import Subscribe from "Subscribe";
import UI from "../UI/index";
import WS from "./WS";

let emergencyCancelled = false;
let currentBatchId: string | null = null;

// Subscribe once to emergency.stop events from WS
(() => {
  try {
    socketBus.on("message", (msg: unknown) => {
      const m = msg as any;
      if (m && m.type === "emergency.stop") {
        console.warn("Emergency stop received; cancelling queued actions.");
        emergencyCancelled = true;
        // Flush queue ngay nếu đang sử dụng hàng đợi
        try {
          actionQueue.clear();
        } catch {
          /* noop */
        }
      }
    });
  } catch {
    /* noop */
  }
})();

export function resetEmergencyStop(): void {
  emergencyCancelled = false;
}

export function setCurrentBatchId(batchId: string | null): void {
  if (batchId && batchId !== currentBatchId) {
    // Batch id chuyển đổi: reset emergency cho batch mới
    emergencyCancelled = false;
  }
  currentBatchId = batchId;
}

export function handleServerCommand(cmd: unknown): boolean {
  // Expect shape { type: string, payload: ... }
  const anyCmd = cmd as any;
  if (!anyCmd || typeof anyCmd.type !== "string") return false;

  // Handle data-fetch commands (non-invasive, no device permissions)
  if (anyCmd.type === "wiki.search") {
    const q = String(anyCmd.payload?.query ?? "").trim();
    if (!q) return false;
    // Fire and forget; upstream listener should be awaiting a response channel in real app
    fetchFromWikipedia(q)
      .then((data) => {
        // Push into store for UI to render
        useSearchStore.getState().setWiki(data);
      })
      .catch((err) => console.warn("wiki.search error", err));
    return true;
  }

  if (anyCmd.type === "arxiv.search") {
    const q = String(anyCmd.payload?.query ?? "").trim();
    const max = Number(anyCmd.payload?.maxResults ?? 5);
    if (!q) return false;
    fetchFromArXiv(q, max)
      .then((xml) => {
        const entries = parseArXivAtom(xml);
        useSearchStore.getState().setArxiv(entries);
      })
      .catch((err) => console.warn("arxiv.search error", err));
    return true;
  }

  const action = anyCmd as InputAction;
  // Rule check (requires inferred permissions per action)
  let requires: Array<"screen" | "mouse" | "keyboard"> = [];
  if (action.type === "type_text") {
    requires = ["keyboard"];
  } else if (action.type === "click" || action.type === "move_mouse") {
    requires = ["mouse"];
  }
  if (emergencyCancelled) {
    console.warn("Blocked by Emergency Stop");
    return false;
  }
  if (!canExecute({ requires })) return false;
  // Nếu queue được bật (do app cấu hình), đẩy vào queue thay vì thực thi ngay
  try {
    // Khởi tạo runner/shouldCancel một lần (idempotent)
    actionQueue.setRunner((a) => executeAction(a));
    actionQueue.setShouldCancel(() => emergencyCancelled);
  } catch {
    /* noop */
  }
  if ((actionQueue as any).enabled) {
    actionQueue.enqueue(action);
    return true;
  }
  return executeAction(action);
}
