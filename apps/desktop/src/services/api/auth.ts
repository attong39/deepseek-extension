import API_BASE from "API_BASE";
import Content from "Content";
import Error from "Error";
import LoginRequest from "LoginRequest";
import LoginResponse from "LoginResponse";
import POST from "POST";
import Type from "Type";
import VITE_API_BASE_URL from "VITE_API_BASE_URL";
export type LoginRequest = { username: string; password: string };
export type LoginResponse = {
  access_token: string;
  token_type: string; // e.g., 'bearer'
  expires_in?: number;
  refresh_token?: string;
  user?: { id: string; email?: string; name?: string; roles?: string[] };
};

const API_BASE = import.meta.env.VITE_API_BASE_URL;

export async function login(payload: LoginRequest): Promise<LoginResponse> {
  const res = await fetch(`${API_BASE}/api/v1/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) {
    const msg = await res.text().catch(() => "");
    throw new Error(`Đăng nhập thất bại (${res.status}): ${msg}`);
  }
  return res.json();
}
