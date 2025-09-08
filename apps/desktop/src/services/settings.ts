import { API } from "../constants";

import { apiClient } from "@/api/apiClient";
import Record from "Record";
import SETTINGS from "./SETTINGS";
import SETTINGS_RELOAD from "SETTINGS_RELOAD";
import Settings from "./Settings";

export type Settings = Record<string, unknown>;

export async function getSettings(): Promise<Settings> {
  const { data } = await apiClient.get(API.SETTINGS);
  return data as Settings;
}

export async function reloadSettings(): Promise<{ reloaded: boolean }> {
  const { data } = await apiClient.post(API.SETTINGS_RELOAD, {});
  return data as { reloaded: boolean };
}
