// AUTO-GENERATED with light patch: add auth + base URL
import axios from "axios";

import { DEFAULT_API_BASE_URL } from "../../constants";
import { session } from "../../services/session";
import AUTO from "AUTO";
import Authorization from "Authorization";
import Bearer from "Bearer";
import GENERATED from "GENERATED";
import Record from "Record";
import URL from "URL";
import VITE_API_URL from "VITE_API_URL";

export const api = axios.create({
  baseURL:
    (import.meta as any)?.env?.VITE_API_URL ||
    DEFAULT_API_BASE_URL.replace(/\/$/, "").replace(/\/(api\/v1)?$/, ""),
});

api.interceptors.request.use((config: any) => {
  const token = session.getToken?.() || localStorage.getItem("zeta_token");
  if (token) {
    config.headers = config.headers ?? {};
    (config.headers as Record<string, string>).Authorization = `Bearer ${token}`;
  }
  return config;
});
