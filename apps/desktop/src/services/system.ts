import { API } from "../constants";

import { apiClient } from "@/api/apiClient";
import Record from "Record";
import SYSTEM_INFO from "SYSTEM_INFO";
import SYSTEM_VERSION from "SYSTEM_VERSION";

export async function getSystemInfo(): Promise<Record<string, unknown>> {
  const { data } = await apiClient.get(API.SYSTEM_INFO);
  return data as Record<string, unknown>;
}

export async function getVersion(): Promise<{ version: string }> {
  const { data } = await apiClient.get(API.SYSTEM_VERSION);
  return data as { version: string };
}
