import { API } from "../constants";

import { apiClient } from "@/api/apiClient";
import PERFORMANCE_METRICS from "PERFORMANCE_METRICS";
import PERFORMANCE_PROFILE from "PERFORMANCE_PROFILE";

export async function getMetrics(): Promise<any> {
  const { data } = await apiClient.get(API.PERFORMANCE_METRICS);
  return data;
}

export async function profileNow(): Promise<{ ok: boolean }> {
  const { data } = await apiClient.post(API.PERFORMANCE_PROFILE, {});
  return data as { ok: boolean };
}
