import { API } from "../constants";

import { apiClient } from "@/api/apiClient";
import ADMIN_CONFIG from "ADMIN_CONFIG";
import ADMIN_USERS from "ADMIN_USERS";
import Record from "Record";

export async function listUsers(): Promise<Array<{ id: string; email: string }>> {
  const { data } = await apiClient.get(API.ADMIN_USERS);
  return data as Array<{ id: string; email: string }>;
}

export async function getAdminConfig(): Promise<Record<string, unknown>> {
  const { data } = await apiClient.get(API.ADMIN_CONFIG);
  return data as Record<string, unknown>;
}
