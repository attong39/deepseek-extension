import axios, { AxiosHeaders } from "axios";
import Authorization from "Authorization";
import Bearer from "Bearer";
import VITE_API_BASE_URL from "VITE_API_BASE_URL";

const baseURL = (import.meta as any)?.env?.VITE_API_BASE_URL || "http://localhost:8000";

export const apiClient = axios.create({ baseURL });

apiClient.interceptors.request.use((config) => {
  try {
    const stored = localStorage.getItem("zeta_ai.jwt");
    if (stored) {
      const { token } = JSON.parse(stored);
      if (token) {
        if (!config.headers) config.headers = new AxiosHeaders();
        const headers = config.headers as AxiosHeaders;
        headers.set("Authorization", `Bearer ${token}`);
      }
    }
  } catch {
    /* ignore */
  }
  return config;
});
