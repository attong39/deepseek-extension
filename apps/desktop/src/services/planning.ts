import { API } from "../constants";

import { apiClient } from "@/api/apiClient";
import PLANNING_CREATE from "PLANNING_CREATE";
import PLANNING_EXECUTE from "PLANNING_EXECUTE";
import PLANNING_OPTIMIZE from "PLANNING_OPTIMIZE";
import PLANNING_VALIDATE from "PLANNING_VALIDATE";
import Plan from "Plan";
import Record from "Record";

export type Plan = { id: string; steps: any[]; meta?: Record<string, unknown> };

export async function createPlan(input: Record<string, unknown>): Promise<Plan> {
  const { data } = await apiClient.post(API.PLANNING_CREATE, input);
  return data as Plan;
}

export async function executePlan(planId: string): Promise<{ executed: boolean }> {
  const { data } = await apiClient.post(API.PLANNING_EXECUTE, { planId });
  return data as { executed: boolean };
}

export async function optimizePlan(planId: string): Promise<Plan> {
  const { data } = await apiClient.post(API.PLANNING_OPTIMIZE, { planId });
  return data as Plan;
}

export async function validatePlan(plan: Plan): Promise<{ valid: boolean; reason?: string }> {
  const { data } = await apiClient.post(API.PLANNING_VALIDATE, plan);
  return data as { valid: boolean; reason?: string };
}
