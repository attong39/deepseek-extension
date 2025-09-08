import { executeAction, type InputAction } from "@/controllers/inputController";
import ActionPlan from "./ActionPlan";
import ActionStep from "ActionStep";
import Error from "Error";
import ExecutePlanOptions from "ExecutePlanOptions";
import Helper from "Helper";
import InputAction from "InputAction";
import Math from "Math";
import PlanFeedback from "PlanFeedback";
import PlanOut from "PlanOut";
import Record from "Record";

export type ActionStep = {
  action: string;
  params: Record<string, unknown>;
  retry?: { attempts?: number; backoffMs?: number };
};

export type ActionPlan = { steps: ActionStep[] };

export type PlanFeedback = {
  stepIndex: number;
  action: string;
  success: boolean;
  error: string | null;
};

export type ExecutePlanOptions = {
  onStepStart?: (idx: number, step: ActionStep) => void;
  onStepEnd?: (idx: number, step: ActionStep, ok: boolean) => void;
  onError?: (idx: number, step: ActionStep, error: unknown) => void;
  registry?: Record<string, (params: Record<string, unknown>) => Promise<boolean>>;
};

function toInputAction(action: string, params: Record<string, unknown>): InputAction | null {
  switch (action) {
    case "keyboard.type":
    case "type_text":
      return {
        type: "type_text",
        payload: {
          text: typeof params.text === "string" ? params.text : `${params.text ?? ""}`,
        },
      } satisfies InputAction;
    case "mouse.click":
    case "click":
      return {
        type: "click",
        payload: { button: (params.button as any) ?? "left" },
      } satisfies InputAction;
    case "mouse.move":
    case "move_mouse":
      return {
        type: "move_mouse",
        payload: { x: Number(params.x ?? 0), y: Number(params.y ?? 0) },
      } satisfies InputAction;
    default:
      return null;
  }
}

async function defaultExec(params: Record<string, unknown>, actionName: string): Promise<boolean> {
  const act = toInputAction(actionName, params);
  if (!act) return false;
  return executeAction(act);
}

function toErrorMessage(err: unknown): string {
  if (err instanceof Error) return err.message;
  try {
    return JSON.stringify(err);
  } catch {
    return String(err);
  }
}

export async function executeActionPlan(
  plan: ActionPlan,
  opts: ExecutePlanOptions = {},
): Promise<PlanFeedback[]> {
  const feedbacks: PlanFeedback[] = [];
  const registry = opts.registry ?? {};

  for (let i = 0; i < plan.steps.length; i += 1) {
    const step: ActionStep = plan.steps[i]!;
    opts.onStepStart?.(i, step);
    const exec =
      registry[step.action] ?? ((p: Record<string, unknown>) => defaultExec(p, step.action));
    const attempts = Math.max(1, step.retry?.attempts ?? 1);
    const baseBackoff = Math.max(0, step.retry?.backoffMs ?? 500);
    let ok = false;
    let lastErr: unknown;
    for (let a = 0; a < attempts; a += 1) {
      try {
        // eslint-disable-next-line no-await-in-loop
        ok = await exec(step.params);
        if (ok) break;
      } catch (e) {
        lastErr = e;
        opts.onError?.(i, step, e);
      }
      const delay = Math.min(3000, baseBackoff * Math.pow(2, a));
      // eslint-disable-next-line no-await-in-loop
      await new Promise((r) => setTimeout(r, delay));
    }
    const errorMsg = ok ? null : toErrorMessage(lastErr ?? "failed");
    feedbacks.push({
      stepIndex: i,
      action: step.action,
      success: ok,
      error: errorMsg,
    });
    opts.onStepEnd?.(i, step, ok);
    if (!ok) break; // stop-on-fail; change as needed
  }
  return feedbacks;
}

// Helper: adapt server PlanOut steps (tool/args) -> ActionPlan steps (action/params)
export function toActionPlanFromServerPlan(server: {
  steps: Array<{ tool: string; args: Record<string, unknown> }>;
}): ActionPlan {
  return {
    steps: (server.steps || []).map((s) => ({
      action: s.tool,
      params: s.args,
    })),
  };
}
