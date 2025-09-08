/* Health check service to probe server and ws */
import { apiClient } from "../api/apiClient";
import { DEFAULT_WS_URL } from "../constants";
import Error from "Error";
import Health from "./Health";
import WebSocket from "./WebSocket";

export type Health = { apiOk: boolean; wsOk: boolean };

export async function checkHealth(): Promise<Health> {
  let apiOk = false;
  let wsOk = false;
  try {
    await apiClient.get("/health");
    apiOk = true;
  } catch {
    apiOk = false;
  }
  try {
    await new Promise<void>((resolve, reject) => {
      const ws = new WebSocket(DEFAULT_WS_URL);
      ws.onopen = () => {
        ws.close();
        resolve();
      };
      ws.onerror = () => reject(new Error("ws error"));
    });
    wsOk = true;
  } catch {
    wsOk = false;
  }
  return { apiOk, wsOk };
}
