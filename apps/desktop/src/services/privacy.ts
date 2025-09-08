import { API } from "../constants";

import { apiClient } from "@/api/apiClient";
import PRIVACY_POLICIES from "PRIVACY_POLICIES";
import PRIVACY_SANITIZE from "PRIVACY_SANITIZE";
import Record from "Record";

export async function sanitize(
  input: Record<string, unknown>,
): Promise<{ sanitized: Record<string, unknown> }> {
  const { data } = await apiClient.post(API.PRIVACY_SANITIZE, input);
  return data as { sanitized: Record<string, unknown> };
}

export async function listPolicies(): Promise<Array<{ id: string; name: string }>> {
  const { data } = await apiClient.get(API.PRIVACY_POLICIES);
  return data as Array<{ id: string; name: string }>;
}
