import { API } from "../constants";

import { apiClient } from "@/api/apiClient";
import ASSISTANT from "ASSISTANT";
import ASSISTANTS from "./ASSISTANTS";
import Assistant from "Assistant";
import Record from "Record";

export type Assistant = {
  id: string;
  name: string;
  config?: Record<string, unknown>;
};

export async function listAssistants(): Promise<Assistant[]> {
  const { data } = await apiClient.get(API.ASSISTANTS);
  return data as Assistant[];
}

export async function getAssistant(id: string): Promise<Assistant> {
  const { data } = await apiClient.get(API.ASSISTANT(id));
  return data as Assistant;
}
