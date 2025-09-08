import { API } from "../constants";
import { session } from "../services/session";
import { apiClient } from "./apiClient";
import AUTH_LOGIN from "AUTH_LOGIN";
import AUTH_REFRESH from "AUTH_REFRESH";
import If from "If";
import LoginResponse from "LoginResponse";
import Register from "Register";
import Sync from "Sync";

export type LoginResponse = {
  access_token: string;
  token_type?: string;
  expires_at?: number;
};

export async function login(username: string, password: string): Promise<boolean> {
  const res = await apiClient.post<LoginResponse>(API.AUTH_LOGIN, {
    username,
    password,
  });
  const token = (res.data as any)?.access_token as string | undefined;
  if (token) {
    localStorage.setItem("zeta_token", token);
    // Sync server time skew from Date header if present
    const dateHeader = res.headers?.["date"] ?? res.headers?.["Date"];
    if (dateHeader) {
      const serverNow = Date.parse(String(dateHeader));
      if (!Number.isNaN(serverNow)) session.setServerTime(serverNow);
    }
    // If response includes expiry, set it
    const exp = (res.data as any)?.expires_at as number | undefined;
    if (typeof exp === "number") session.setToken(token, exp);
    else session.setToken(token, null);
    return true;
  }
  return false;
}

export function logout(): void {
  localStorage.removeItem("zeta_token");
  session.setToken(null, null);
}

export function getToken(): string | null {
  try {
    return localStorage.getItem("zeta_token");
  } catch {
    return null;
  }
}

// Register a default refresh handler
session.setRefreshHandler(async () => {
  try {
    const res = await apiClient.post(API.AUTH_REFRESH, {});
    const token = (res.data as any)?.access_token as string | undefined;
    const expires_at = (res.data as any)?.expires_at as number | undefined;
    const dateHeader = res.headers?.["date"] ?? res.headers?.["Date"];
    if (dateHeader) {
      const serverNow = Date.parse(String(dateHeader));
      if (!Number.isNaN(serverNow)) session.setServerTime(serverNow);
    }
    if (token) {
      const out: { token: string; expiresAt?: number } = { token };
      if (typeof expires_at === "number") out.expiresAt = expires_at;
      return out;
    }
    return null;
  } catch {
    return null;
  }
});
