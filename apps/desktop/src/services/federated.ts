import { API } from "../constants";

import { apiClient } from "@/api/apiClient";
import FEDERATED_JOBS from "FEDERATED_JOBS";
import FEDERATED_ROUNDS from "FEDERATED_ROUNDS";
import FEDERATED_STATUS from "FEDERATED_STATUS";
import Record from "Record";

export async function getStatus(): Promise<Record<string, unknown>> {
  const { data } = await apiClient.get(API.FEDERATED_STATUS);
  return data as Record<string, unknown>;
}

export async function listJobs(): Promise<Array<Record<string, unknown>>> {
  const { data } = await apiClient.get(API.FEDERATED_JOBS);
  return data as Array<Record<string, unknown>>;
}

export async function listRounds(): Promise<Array<Record<string, unknown>>> {
  const { data } = await apiClient.get(API.FEDERATED_ROUNDS);
  return data as Array<Record<string, unknown>>;
}
