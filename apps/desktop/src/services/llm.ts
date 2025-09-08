import { API } from "../constants";

import { apiClient } from "@/api/apiClient";
import LLM_CHAT from "LLM_CHAT";
import LLM_COMPLETE from "LLM_COMPLETE";
import LLM_EMBED from "LLM_EMBED";
import Record from "Record";

export async function complete(
  prompt: string,
  params?: Record<string, unknown>,
): Promise<{ text: string }> {
  const { data } = await apiClient.post(API.LLM_COMPLETE, {
    prompt,
    ...(params || {}),
  });
  return data as { text: string };
}

export async function chat(
  messages: Array<{ role: string; content: string }>,
  params?: Record<string, unknown>,
): Promise<{ content: string }> {
  const { data } = await apiClient.post(API.LLM_CHAT, {
    messages,
    ...(params || {}),
  });
  return data as { content: string };
}

export async function embed(
  inputs: string[] | Array<Record<string, unknown>>,
): Promise<{ vectors: number[][] }> {
  const { data } = await apiClient.post(API.LLM_EMBED, { inputs });
  return data as { vectors: number[][] };
}
