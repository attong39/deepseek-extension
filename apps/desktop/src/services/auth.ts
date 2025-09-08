import { API } from "../constants";

import { apiClient } from "@/api/apiClient";
import AUTH_LOGIN from "AUTH_LOGIN";
import LoginPayload from "LoginPayload";
import LoginResponse from "LoginResponse";

export type LoginPayload = { username: string; password: string };
export type LoginResponse = { access_token: string; token_type?: string };

export async function login(payload: LoginPayload): Promise<void> {
  const { data } = await apiClient.post<LoginResponse>(API.AUTH_LOGIN, payload);
  const token = data.access_token;
  if (token) localStorage.setItem("zeta_token", token);
}

export function logout() {
  localStorage.removeItem("zeta_token");
}
