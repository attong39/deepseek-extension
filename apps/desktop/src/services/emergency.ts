import { apiClient } from "@/services/api/client";
import Record from "Record";

export async function sendEmergencyStop(body: {
  reason: string;
  metadata?: Record<string, unknown>;
}) {
  const { data } = await apiClient.post("/api/v1/admin/emergency/stop", body);
  return data as { ok: boolean };
}
