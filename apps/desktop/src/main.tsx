import LoginBox from "@components/Settings/LoginBox";
import SafetySettings from "@components/Settings/SafetySettings";
import UpdateBanner from "@components/UpdateBanner";
import { createTheme, CssBaseline, ThemeProvider } from "@mui/material";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import i18next from "i18next";
import { SnackbarProvider, useSnackbar } from "notistack";
import React, { Suspense, useEffect, useMemo, useRef, useState } from "react";
import ReactDOM from "react-dom/client";
import { I18nextProvider, initReactI18next, useTranslation } from "react-i18next";
import { BrowserRouter, HashRouter, Link, Navigate, Route, Routes } from "react-router-dom";

// ---- OpenAPI Hash Guard (dev-only, non-blocking) ----
import { checkOpenApiHashAtDev } from "./lib/openapiHashGuard";
checkOpenApiHashAtDev();

/**
 * ZETA Desktop - main.tsx
 * Entry file for Electron+React renderer. Optimized for:
 *  - i18n (vi as default)
 *  - React Query data layer
 *  - WebSocket (server push/progress)
 *  - MUI theming (system dark/light + user override)
 *  - Error boundary + global toasts
 *  - Works in Electron (HashRouter) and Web (BrowserRouter)
 */

// ---- i18n (tiny inline bootstrap to avoid hard dependency at this file) ----
// If you already have ./i18n, just replace this with: import "./i18n"

import { AuthProvider, useAuth } from "@/context/AuthContext";
import AI from "AI";
import API from "./API/index";
import API_BASE_URL from "API_BASE_URL";
import API_URL_OBJ from "API_URL_OBJ";
import APP_NAME from "APP_NAME";
import ApiCfgCtx from "ApiCfgCtx";
import ApiConfig from "ApiConfig";
import App from "./App";
import AppBoot from "AppBoot";
import AppErrorBoundary from "AppErrorBoundary";
import Arial from "Arial";
import AuthContext from "./context/AuthContext";
import Basic from "Basic";
import Boot from "Boot";
import Boundary from "Boundary";
import Bridge from "Bridge";
import Chat from "./pages/Chat";
import ChatPage from "ChatPage";
import Component from "Component";
import Config from "Config";
import Connected from "Connected";
import Connecting from "Connecting";
import Control from "./pages/Control";
import ControlPage from "ControlPage";
import CustomEvent from "CustomEvent";
import DESKTOP_API_BASE_URL from "DESKTOP_API_BASE_URL";
import DEV_ALLOW_WS_NO_TOKEN from "DEV_ALLOW_WS_NO_TOKEN";
import Dashboard from "./analytics/components/Dashboard";
import DashboardPage from "DashboardPage";
import Defer from "Defer";
import Derive from "Derive";
import Desktop from "Desktop";
import Disconnected from "Disconnected";
import Electron from "Electron";
import Entry from "Entry";
import Env from "Env";
import Error from "Error";
import Example from "Example";
import Exponential from "Exponential";
import Expose from "Expose";
import Guard from "Guard";
import Hash from "Hash";
import IPC from "IPC";
import If from "If";
import ImportMeta from "ImportMeta";
import Inter from "Inter";
import Language from "Language";
import Loading from "Loading";
import MUI from "MUI";
import Math from "Math";
import OPEN from "OPEN";
import OpenAPI from "OpenAPI";
import Optimized from "Optimized";
import Pages from "./Pages/index";
import Panel from "Panel";
import Provider from "Provider";
import Query from "Query";
import ReactNode from "ReactNode";
import Readonly from "Readonly";
import Record from "Record";
import Router from "./Router/index";
import Settings from "./pages/Settings";
import SettingsPage from "SettingsPage";
import ShellLayout from "ShellLayout";
import StrictMode from "StrictMode";
import Theme from "Theme";
import ToastBridge from "ToastBridge";
import Toggle from "Toggle";
import Training from "./pages/Training";
import TrainingPage from "TrainingPage";
import URL from "URL";
import VITE_API_BASE_URL from "VITE_API_BASE_URL";
import VITE_APP_NAME from "VITE_APP_NAME";
import VITE_DEV_ALLOW_WS_NO_TOKEN from "VITE_DEV_ALLOW_WS_NO_TOKEN";
import VITE_I18N_DEFAULT_LANG from "VITE_I18N_DEFAULT_LANG";
import VITE_WEBSOCKET_RETRY_MAX from "VITE_WEBSOCKET_RETRY_MAX";
import VITE_WS_URL from "VITE_WS_URL";
import WS from "WS";
import WSCtx from "WSCtx";
import WSProvider from "WSProvider";
import WSState from "WSState";
import WS_ORIGIN from "WS_ORIGIN";
import WS_PATH from "WS_PATH";
import WS_RETRY_MAX from "WS_RETRY_MAX";
import WS_URL from "WS_URL";
import Web from "Web";
import WebSocket from "WebSocket";
import Window from "Window";
import WindowWithElectron from "WindowWithElectron";
import Works from "Works";
import You from "You";
import ZETA from "ZETA";
import Zeta from "Zeta";

if (!i18next.isInitialized) {
  const defaultLang: "vi" | "en" =
    ((import.meta as ImportMeta).env?.VITE_I18N_DEFAULT_LANG as "vi" | "en") || "vi";
  i18next.use(initReactI18next).init({
    lng: defaultLang,
    fallbackLng: "vi",
    interpolation: { escapeValue: false },
    resources: {
      vi: {
        translation: {
          app_title: "Zeta Desktop AI",
          nav: {
            dashboard: "Bảng điều khiển",
            chat: "Chat",
            training: "Huấn luyện",
            control: "Điều khiển",
            settings: "Cài đặt",
          },
          common: {
            connecting: "Đang kết nối…",
            connected: "Đã kết nối",
            disconnected: "Mất kết nối",
            language: "Ngôn ngữ: {{lng}}",
            language_toggle: "Chuyển ngôn ngữ",
          },
        },
      },
      en: {
        translation: {
          app_title: "Zeta Desktop AI",
          nav: {
            dashboard: "Dashboard",
            chat: "Chat",
            training: "Training",
            control: "Control",
            settings: "Settings",
          },
          common: {
            connecting: "Connecting...",
            connected: "Connected",
            disconnected: "Disconnected",
            language: "Language: {{lng}}",
            language_toggle: "Toggle language",
          },
        },
      },
    },
  });
}

// ---- Env / Config ----
interface ImportMeta {
  env?: Record<string, string>;
}

interface WindowWithElectron extends Window {
  process?: {
    versions?: {
      electron?: string;
    };
  };
  DESKTOP_API_BASE_URL?: string;
  electron?: {
    ipcRenderer: {
      on: (channel: string, listener: (...args: any[]) => void) => void;
      send: (channel: string, ...args: any[]) => void;
      invoke?: (channel: string, ...args: any[]) => Promise<any>;
    };
  };
}

const windowWithElectron = window as WindowWithElectron;
const importMeta = import.meta as ImportMeta;

const isElectron =
  Boolean(windowWithElectron.process?.versions?.electron) ||
  navigator.userAgent.includes("Electron");

const API_BASE_URL =
  importMeta.env?.VITE_API_BASE_URL ||
  windowWithElectron.DESKTOP_API_BASE_URL ||
  "http://localhost:8000";
// Derive WS origin from API origin (strip path like /api/v1)
const API_URL_OBJ = new URL(String(API_BASE_URL), window.location.href);
const WS_ORIGIN = API_URL_OBJ.origin.replace(/^http/, "ws");
const WS_PATH = "/ws/chat"; // backend expects /ws/chat endpoints
const WS_URL = importMeta.env?.VITE_WS_URL || `${WS_ORIGIN}`;
const DEV_ALLOW_WS_NO_TOKEN =
  String(importMeta.env?.VITE_DEV_ALLOW_WS_NO_TOKEN || "false").toLowerCase() === "true";
const APP_NAME = importMeta.env?.VITE_APP_NAME || "Zeta Desktop AI";
const WS_RETRY_MAX = Number.parseInt(
  (importMeta.env?.VITE_WEBSOCKET_RETRY_MAX as string) || "3",
  10,
);

// ---- Error Boundary ----
class AppErrorBoundary extends React.Component<{ children: React.ReactNode }, { error?: Error }> {
  override state: Readonly<{ error?: Error }> = {};
  static getDerivedStateFromError(error: Error) {
    return { error };
  }
  override componentDidCatch(err: Error) {
    console.error("App crash:", err);
  }
  override render() {
    if (this.state.error) {
      return (
        <div style={{ padding: 24, fontFamily: "system-ui, sans-serif" }}>
          <h2>Đã xảy ra lỗi</h2>
          <pre style={{ whiteSpace: "pre-wrap" }}>{this.state.error.message}</pre>
          <button onClick={() => location.reload()}>Tải lại ứng dụng</button>
        </div>
      );
    }
    return this.props.children;
  }
}

// ---- Theme (dark/light with system + localStorage override) ----
function useThemeMode() {
  const key = "zeta_theme";
  const prefersDark =
    window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;
  const [mode, setMode] = useState<"light" | "dark">(() => {
    const stored = localStorage.getItem(key) as "light" | "dark" | null;
    return stored || (prefersDark ? "dark" : "light");
  });
  useEffect(() => {
    localStorage.setItem(key, mode);
  }, [mode]);
  const theme = useMemo(() => createTheme({ palette: { mode } }), [mode]);
  return { mode, setMode, theme } as const;
}

// ---- API Config ----
interface ApiConfig {
  apiBaseUrl: string;
  wsUrl: string;
}
const ApiCfgCtx = React.createContext<ApiConfig>({
  apiBaseUrl: API_BASE_URL,
  wsUrl: WS_URL,
});

// ---- WS Provider (auto-reconnect, status) ----
interface WSState {
  status: "connecting" | "connected" | "disconnected";
  send: (data: unknown) => void;
  socket: WebSocket | undefined;
}
const WSCtx = React.createContext<WSState>({
  status: "disconnected",
  send: () => {},
  socket: undefined,
});

function WSProvider({ children }: Readonly<{ children: React.ReactNode }>) {
  const { enqueueSnackbar } = useSnackbar();
  const { token } = useAuth();
  const { wsUrl } = React.useContext(ApiCfgCtx);

  const [status, setStatus] = useState<WSState["status"]>("connecting");
  const sockRef = useRef<WebSocket | undefined>();
  const backoffRef = useRef(1000);
  const retryCountRef = useRef(0);

  useEffect(() => {
    let closedByUser = false;
    const connect = () => {
      setStatus("connecting");
      const base = wsUrl.replace(/\/$/, "");
      let url = "";
      if (token) {
        url = `${base}${WS_PATH}?token=${encodeURIComponent(token)}`;
      } else if (DEV_ALLOW_WS_NO_TOKEN) {
        url = `${base}${WS_PATH}`;
      }
      if (!url) {
        setStatus("disconnected");
        return () => {};
      }
      const ws = new WebSocket(url);
      sockRef.current = ws;

      ws.onopen = () => {
        setStatus("connected");
        backoffRef.current = 1000;
        retryCountRef.current = 0;
        enqueueSnackbar(i18next.t("common.connected"), { variant: "success" });
      };

      ws.onmessage = (ev) => {
        // You can route events here (progress, notifications...)
        try {
          const msg = JSON.parse(ev.data);
          console.debug("WS msg:", msg);
        } catch {
          /* ignore */
        }
      };

      ws.onerror = () => {
        /* handled by onclose */
      };
      ws.onclose = () => {
        setStatus("disconnected");
        if (!closedByUser) {
          enqueueSnackbar(i18next.t("common.disconnected"), {
            variant: "warning",
          });
          // Giới hạn số lần retry theo env
          if (retryCountRef.current >= Math.max(0, WS_RETRY_MAX)) {
            enqueueSnackbar("Dừng thử lại kết nối WebSocket", {
              variant: "error",
            });
            return;
          }
          // Exponential backoff tối đa 10s
          const delay = Math.min(backoffRef.current, 10000);
          setTimeout(connect, delay);
          backoffRef.current = delay * 2;
          retryCountRef.current += 1;
        }
      };

      return () => {
        closedByUser = true;
        ws.close();
      };
    };

    const cleanup = connect();
    return cleanup;
  }, [token, wsUrl, enqueueSnackbar]);

  const send = React.useCallback((data: unknown) => {
    if (sockRef.current && sockRef.current.readyState === WebSocket.OPEN) {
      sockRef.current.send(typeof data === "string" ? data : JSON.stringify(data));
    }
  }, []);
  const wsValue = React.useMemo<WSState>(
    () => ({ status, send, socket: sockRef.current }),
    [status, send],
  );
  return <WSCtx.Provider value={wsValue}>{children}</WSCtx.Provider>;
}

// ---- QueryClient (retry/backoff sensible defaults) ----
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: (failureCount, error: any) => {
        const status = error?.response?.status;
        if (status && [400, 401, 403, 404].includes(status)) return false; // don't retry on client errors
        return failureCount < 3;
      },
      refetchOnWindowFocus: false,
      staleTime: 30_000,
    },
  },
});

// ---- Basic Pages (inline placeholders; replace with real pages later) ----
function ShellLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  const { t } = useTranslation();
  const ws = React.useContext(WSCtx);
  const { mode, setMode } = useThemeMode(); // create another instance for header toggle
  let wsLabel: string;
  if (ws.status === "connecting") wsLabel = t("common.connecting");
  else if (ws.status === "connected") wsLabel = t("common.connected");
  else wsLabel = t("common.disconnected");
  return (
    <div
      style={{
        display: "flex",
        height: "100vh",
        fontFamily: "Inter, system-ui, Arial, sans-serif",
      }}
    >
      <aside style={{ width: 240, borderRight: "1px solid #eee", padding: 16 }}>
        <h3 style={{ marginTop: 0 }}>{APP_NAME}</h3>
        <nav style={{ display: "grid", gap: 8 }}>
          <Link to="/">🏠 {t("nav.dashboard")}</Link>
          <Link to="/chat">💬 {t("nav.chat")}</Link>
          <Link to="/training">🧠 {t("nav.training")}</Link>
          <Link to="/control">🖱️ {t("nav.control")}</Link>
          <Link to="/settings">⚙️ {t("nav.settings")}</Link>
        </nav>
        <div style={{ marginTop: 24, fontSize: 12, opacity: 0.8 }}>WS: {wsLabel}</div>
        <button
          style={{ marginTop: 12 }}
          onClick={() => setMode(mode === "dark" ? "light" : "dark")}
        >
          Toggle {mode}
        </button>
      </aside>
      <main style={{ flex: 1, padding: 24 }}>{children}</main>
      <UpdateBanner />
    </div>
  );
}

function DashboardPage() {
  return <div>Dashboard</div>;
}
function ChatPage() {
  return <div>Chat Panel</div>;
}
function TrainingPage() {
  return <div>Training Panel</div>;
}
function ControlPage() {
  return <div>Desktop Control Panel</div>;
}
function SettingsPage() {
  return (
    <div>
      <LoginBox />
      <SafetySettings />
      <div style={{ height: 24 }} />
      <h3>Thông tin</h3>
      <ul>
        <li>API: {API_BASE_URL}</li>
        <li>WS: {WS_URL}</li>
        <li>Electron: {String(isElectron)}</li>
      </ul>
    </div>
  );
}

// ---- App Boot ----
function AppBoot() {
  const { theme } = useThemeMode();
  const Router = isElectron ? HashRouter : BrowserRouter;
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <SnackbarProvider maxSnack={3} autoHideDuration={2500}>
        <AuthProvider>
          <ApiCfgCtx.Provider
            value={React.useMemo(() => ({ apiBaseUrl: API_BASE_URL, wsUrl: WS_URL }), [])}
          >
            <WSProvider>
              <Router>
                <Suspense fallback={<div style={{ padding: 24 }}>Loading…</div>}>
                  <Routes>
                    <Route
                      path="/"
                      element={
                        <ShellLayout>
                          <DashboardPage />
                        </ShellLayout>
                      }
                    />
                    <Route
                      path="/chat"
                      element={
                        <ShellLayout>
                          <ChatPage />
                        </ShellLayout>
                      }
                    />
                    <Route
                      path="/training"
                      element={
                        <ShellLayout>
                          <TrainingPage />
                        </ShellLayout>
                      }
                    />
                    <Route
                      path="/control"
                      element={
                        <ShellLayout>
                          <ControlPage />
                        </ShellLayout>
                      }
                    />
                    <Route
                      path="/settings"
                      element={
                        <ShellLayout>
                          <SettingsPage />
                        </ShellLayout>
                      }
                    />
                    <Route path="*" element={<Navigate to="/" replace />} />
                  </Routes>
                </Suspense>
              </Router>
            </WSProvider>
          </ApiCfgCtx.Provider>
        </AuthProvider>
      </SnackbarProvider>
    </ThemeProvider>
  );
}

const root = ReactDOM.createRoot(document.getElementById("root")!);
root.render(
  <React.StrictMode>
    <I18nextProvider i18n={i18next}>
      <QueryClientProvider client={queryClient}>
        <AppErrorBoundary>
          <AppBoot />
        </AppErrorBoundary>
      </QueryClientProvider>
    </I18nextProvider>
  </React.StrictMode>,
);

// ---- Electron IPC glue (optional, safe no-op on Web) ----
// Expose a type-safe helper for preload to call: window.electron?.ipcRenderer
if (windowWithElectron.electron?.ipcRenderer) {
  // Example: receive notifications from main process
  windowWithElectron.electron.ipcRenderer.on(
    "notify",
    (
      _: unknown,
      payload: {
        message: string;
        variant?: "default" | "success" | "error" | "warning" | "info";
      },
    ) => {
      const evt = new CustomEvent("zeta:notify", { detail: payload });
      window.dispatchEvent(evt);
    },
  );
}

// Bridge IPC to notistack
(function bindGlobalNotify() {
  const handler = (e: any) => {
    const { message, variant } = e.detail || {};
    // Defer until notistack is ready
    setTimeout(() => {
      const ev = new CustomEvent("__toast__", { detail: { message, variant } });
      window.dispatchEvent(ev);
    }, 0);
  };
  window.addEventListener("zeta:notify", handler);
})();

// notistack helper listener (mounted once)
(function installToastListener() {
  function ToastBridge() {
    const { enqueueSnackbar } = useSnackbar();
    useEffect(() => {
      const onToast = (e: any) =>
        enqueueSnackbar(e.detail?.message, {
          variant: e.detail?.variant || "default",
        });
      window.addEventListener("__toast__", onToast);
      return () => window.removeEventListener("__toast__", onToast);
    }, [enqueueSnackbar]);
    return null;
  }
  // mount hidden bridge
  const host = document.createElement("div");
  document.body.appendChild(host);
  ReactDOM.createRoot(host).render(
    <SnackbarProvider maxSnack={3}>
      <ToastBridge />
    </SnackbarProvider>,
  );
})();
