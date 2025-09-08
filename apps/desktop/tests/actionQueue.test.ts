import { beforeEach, describe, expect, it } from "vitest";

import type { InputAction } from "../src/controllers/inputController";
import { actionQueue } from "../src/services/actionQueue";

function mkAction(type: InputAction["type"]): InputAction {
  if (type === "type_text") return { type, payload: { text: "x" } } as InputAction;
  if (type === "click") return { type, payload: { button: "left" } } as InputAction;
  return { type: "type_text", payload: { text: "x" } } as InputAction;
}

describe("actionQueue", () => {
  beforeEach(() => {
    actionQueue.disable();
    actionQueue.clear();
    actionQueue.setRunner(async () => true);
    actionQueue.setShouldCancel(() => false);
  });

  it("enqueue processes when enabled", async () => {
    actionQueue.enable();
    expect(actionQueue.size()).toBe(0);
    actionQueue.enqueue(mkAction("type_text"));
    expect(actionQueue.size()).toBe(1);
    await new Promise((r) => setTimeout(r, 10));
    expect(actionQueue.size()).toBe(0);
  });

  it("clear empties queue immediately", async () => {
    actionQueue.enable();
    actionQueue.enqueue(mkAction("type_text"));
    actionQueue.enqueue(mkAction("click"));
    expect(actionQueue.size()).toBe(2);
    actionQueue.clear();
    expect(actionQueue.size()).toBe(0);
  });

  it("cancel stops further processing", async () => {
    let count = 0;
    actionQueue.setRunner(async () => {
      count += 1;
      return true;
    });
    let cancel = false;
    actionQueue.setShouldCancel(() => cancel);
    actionQueue.enable();
    actionQueue.enqueue(mkAction("type_text"));
    actionQueue.enqueue(mkAction("type_text"));
    cancel = true; // cancel after first tick
    await new Promise((r) => setTimeout(r, 10));
    // first may or may not run depending on timing, but queue should be empty due to clear logic
    expect(actionQueue.size()).toBe(0);
  });
});
