import axios from "axios";
import { HashRouter, NavLink, Link, Routes, Route } from "react-router-dom";

import { DEFAULT_API_BASE_URL } from "../constants";
import { messageFor } from "./errorCodes";
import { httpMeta } from "../services/httpMeta";
import { session } from "../services/session";
import { telemetry } from "../services/telemetry";
import API from "./index";
import ArXiv from "ArXiv";
import ArXivEntry from "ArXivEntry";
import Atom from "Atom";
import Authorization from "Authorization";
import Bearer from "Bearer";
import CORS from "CORS";
import Capture from "Capture";
import Content from "Content";
import DOMParser from "DOMParser";
import Electron from "Electron";
import Element from "Element";
import Error from "Error";
import Fallback from "Fallback";
import GET from "GET";
import HTTP from "HTTP";
import JSONP from "JSONP";
import Optional from "Optional";
import Prefer from "Prefer";
import Record from "Record";
import RegExp from "RegExp";
import RegExpExecArray from "RegExpExecArray";
import Request from "Request";
import S from "S";
import Simple from "Simple";
import Status from "../pages/Status";
import Telemetry from "Telemetry";
import Type from "Type";
import Wikipedia from "Wikipedia";
import XML from "XML";

export const apiClient = axios.create({
  baseURL: DEFAULT_API_BASE_URL,
  timeout: 15000,
  headers: { "Content-Type": "application/json", retries: 3 },
});

apiClient.interceptors.request.use((config: any) => {
  const token = session.getToken() || localStorage.getItem("zeta_token");
  if (token) {
    config.headers = config.headers ?? {};
    (config.headers as Record<string, string>).Authorization = `Bearer ${token}`;
  }
  return config;
});

apiClient.interceptors.response.use(
  (resp: any) => {
    try {
      const headers = resp?.headers ?? {};
      const meta = httpMeta.updateFromHeaders(headers);
      // Optional: emit telemetry heartbeat with tracing ids
      if (meta.requestId || meta.traceId) {
        telemetry.log("http.success", undefined, {
          request_id: meta.requestId ?? "",
          trace_id: meta.traceId ?? "",
          rate_rem: meta.rateLimit?.remaining ?? -1,
        });
      }
    } catch {
      // noop
    }
    return resp;
  },
  (error: any) => {
    try {
      // Capture headers/meta even on errors
      const headers = error?.response?.headers ?? {};
      const meta = httpMeta.updateFromHeaders(headers);
      const status = error?.response?.status as number | undefined;
      // Prefer server error code mapping if present
      const code =
        (error?.response?.data?.error?.code as string | undefined) ||
        (error?.response?.data?.error_code as string | undefined) ||
        (error?.response?.data?.code as string | undefined);
      let msg = messageFor(code, error?.message);
      // Status-based overrides for clarity
      if (status === 401) msg = "Bạn cần đăng nhập (401).";
      else if (status === 403) msg = "Thiếu quyền truy cập (403).";
      else if (status === 422) msg = "Dữ liệu không hợp lệ (422).";
      error.message = msg;

      // Telemetry for rate limit / tracing correlation
      if (status === 429 || meta.rateLimit?.remaining === 0) {
        telemetry.metric("http.rate_limited", 1, {
          limit: meta.rateLimit?.limit ?? -1,
          window: meta.rateLimit?.window ?? -1,
          reset: meta.rateLimit?.reset ?? -1,
        });
      }
      if (meta.requestId || meta.traceId) {
        telemetry.log(
          "http.error",
          { status, code },
          {
            request_id: meta.requestId ?? "",
            trace_id: meta.traceId ?? "",
          },
        );
      }
    } catch {
      // noop
    }
    return Promise.reject(
      error instanceof Error ? error : new Error(String(error?.message ?? "Request failed")),
    );
  },
);

// --- Simple HTTP fetchers for external sources ---
export async function fetchFromWikipedia(query: string): Promise<any> {
  const url = `https://en.wikipedia.org/w/api.php?action=opensearch&origin=*&search=${encodeURIComponent(
    query,
  )}&format=json`;
  // Prefer native fetch for CORS-friendly JSONP-like endpoint
  if (typeof fetch === "function") {
    const resp = await fetch(url, { method: "GET" });
    if (!resp.ok) {
      throw new Error(`Wikipedia fetch failed: ${resp.status}`);
    }
    return await resp.json();
  }
  // Fallback to axios if fetch is not available
  const { data } = await axios.get(url);
  return data;
}

export async function fetchFromArXiv(query: string, maxResults = 5): Promise<string> {
  // arXiv API returns Atom XML; consumer can parse or display raw XML
  const url = `https://export.arxiv.org/api/query?search_query=all:${encodeURIComponent(
    query,
  )}&start=0&max_results=${maxResults}`;
  if (typeof fetch === "function") {
    const resp = await fetch(url, { method: "GET" });
    if (!resp.ok) {
      throw new Error(`arXiv fetch failed: ${resp.status}`);
    }
    return await resp.text();
  }
  const { data } = await axios.get(url, { responseType: "text" });
  return data as string;
}

// --- ArXiv Atom XML parser helper ---
export interface ArXivEntry {
  id: string;
  title: string;
  authors: string[];
  link: string;
  summary?: string;
  published?: string;
  updated?: string;
}

export function parseArXivAtom(xml: string): ArXivEntry[] {
  try {
    // Prefer DOMParser when available (browser/Electron renderer)
    if (typeof DOMParser !== "undefined") {
      const doc = new DOMParser().parseFromString(xml, "application/xml");
      const entries = Array.from(doc.getElementsByTagName("entry"));
      return entries.map((entry) => {
        const getText = (tag: string) =>
          entry.getElementsByTagName(tag)[0]?.textContent?.trim() || "";
        const id = getText("id");
        const title = getText("title");
        const summary = getText("summary");
        const published = getText("published");
        const updated = getText("updated");
        const authors = Array.from(entry.getElementsByTagName("author"))
          .map((a) => a.getElementsByTagName("name")[0]?.textContent?.trim())
          .filter((x): x is string => Boolean(x));
        // Prefer link rel="alternate" else first link
        const links = Array.from(entry.getElementsByTagName("link")) as Array<
          Element & { getAttribute: (n: string) => string | null }
        >;
        const alt = links.find((l) => l.getAttribute("rel") === "alternate");
        const link = (alt?.getAttribute("href") || links[0]?.getAttribute("href") || "").trim();
        const obj: ArXivEntry = { id, title, authors, link };
        if (summary) obj.summary = summary;
        if (published) obj.published = published;
        if (updated) obj.updated = updated;
        return obj;
      });
    }
  } catch {
    // fall through to naive fallback
  }

  // Fallback: naive extraction (best-effort), avoids extra deps
  const result: ArXivEntry[] = [];
  const entryRe = /<entry>([\s\S]*?)<\/entry>/g;
  let match: RegExpExecArray | null;
  while ((match = entryRe.exec(xml))) {
    const block = String(match?.[1] ?? "");
    const text = (re: RegExp) => re.exec(block)?.[1]?.trim() ?? "";
    const all = (re: RegExp) => {
      const out: string[] = [];
      re.lastIndex = 0;
      let mm: RegExpExecArray | null;
      while ((mm = re.exec(block)) !== null) {
        if (mm[1]) out.push(mm[1].trim());
        if (!re.global) break;
      }
      return out;
    };
    const id = text(/<id>([\s\S]*?)<\/id>/);
    const title = text(/<title>([\s\S]*?)<\/title>/);
    const summary = text(/<summary>([\s\S]*?)<\/summary>/);
    const published = text(/<published>([\s\S]*?)<\/published>/);
    const updated = text(/<updated>([\s\S]*?)<\/updated>/);
    const authors = all(/<author>[\s\S]*?<name>([\s\S]*?)<\/name>[\s\S]*?<\/author>/g);
    const altLinkRe = /<link[^>]*rel="alternate"[^>]*href="([^"]+)"/i;
    const anyLinkRe = /<link[^>]*href="([^"]+)"/i;
    const mAlt = altLinkRe.exec(block);
    const mAny = anyLinkRe.exec(block);
    const link = (mAlt?.[1] ?? mAny?.[1] ?? "").trim();
    const obj: ArXivEntry = { id, title, authors, link };
    if (summary) obj.summary = summary;
    if (published) obj.published = published;
    if (updated) obj.updated = updated;
    result.push(obj);
  }
  return result;
}
