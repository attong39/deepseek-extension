import Ctx from "Ctx";
import Record from "Record";
type Ctx = Record<string, unknown>;
let current: Ctx = {};

export function setContext(ctx: Ctx) {
  current = { ...current, ...ctx };
}

export function getContext(): Ctx {
  return { ...current };
}
