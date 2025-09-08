import React, { useMemo, useRef, useState } from "react";

import { useAuth } from "@/context/AuthContext";
import { WebSocketManager } from "@/services/ws";
import AuthContext from "../../context/AuthContext";
import DEV from "DEV";
import FC from "FC";
import JWT from "JWT";
import LoginBox from "./LoginBox";
import Manual from "Manual";
import Quick from "Quick";
import Token from "Token";
import VITE_APP_ENV from "VITE_APP_ENV";
import VITE_DEV_ALLOW_WS_NO_TOKEN from "VITE_DEV_ALLOW_WS_NO_TOKEN";
import WS from "WS";
import WebSocket from "WebSocket";

export const LoginBox: React.FC = () => {
  const { token, user, isAuthenticated, login, saveToken, logout } = useAuth();

  const [form, setForm] = useState({ username: "", password: "" });
  const [busy, setBusy] = useState(false);
  const [jwtDraft, setJwtDraft] = useState(token ?? "");
  const [wsStatus, setWsStatus] = useState<
    "idle" | "connecting" | "connected" | "error" | "closed"
  >("idle");
  const wsRef = useRef<WebSocketManager | null>(null);

  const wsAllowedNoToken = useMemo(
    () =>
      import.meta.env.VITE_DEV_ALLOW_WS_NO_TOKEN === "true" &&
      import.meta.env.VITE_APP_ENV === "development",
    [],
  );

  const handleLogin = async () => {
    try {
      setBusy(true);
      await login({ username: form.username.trim(), password: form.password });
      const stored = localStorage.getItem("zeta_ai.jwt");
      setJwtDraft(stored ? JSON.parse(stored).token : "");
    } catch (e: any) {
      alert(e?.message ?? "Đăng nhập thất bại");
    } finally {
      setBusy(false);
    }
  };

  const handleSaveToken = () => {
    const t = jwtDraft.trim();
    if (!t && !wsAllowedNoToken) {
      alert(
        "Token trống. Ở DEV có thể bật VITE_DEV_ALLOW_WS_NO_TOKEN=true để test WS không token.",
      );
      return;
    }
    // cast an toàn: saveToken chấp nhận string; nếu rỗng và wsAllowedNoToken, có thể truyền chuỗi rỗng hoặc null
    if (t) saveToken(t);
    else saveToken("");
    alert("Đã lưu token.");
  };

  const handleConnectWS = () => {
    wsRef.current?.close();
    wsRef.current = new WebSocketManager({
      token: (jwtDraft || token) ?? null,
      path: "/ws/chat",
      onStatusChange: setWsStatus,
      onMessage: (ev) => {
        // demo: log message
        console.log("[WS] message:", ev.data);
      },
      maxRetries: 8,
    });
    wsRef.current.connect();
  };

  const handleDisconnectWS = () => wsRef.current?.close();

  return (
    <div className="rounded-xl border border-gray-700 p-4 space-y-4">
      <h3 className="text-lg font-semibold">Đăng nhập & JWT</h3>

      {/* Quick login form */}
      <div className="grid gap-2">
        <label htmlFor="login-username" className="text-sm">
          Tài khoản
        </label>
        <input
          id="login-username"
          className="bg-gray-900 border border-gray-700 rounded px-3 py-2"
          placeholder="username / email"
          value={form.username}
          onChange={(e) => setForm((prev) => ({ ...prev, username: e.target.value }))}
        />
        <label htmlFor="login-password" className="text-sm">
          Mật khẩu
        </label>
        <input
          id="login-password"
          className="bg-gray-900 border border-gray-700 rounded px-3 py-2"
          placeholder="••••••••"
          type="password"
          value={form.password}
          onChange={(e) => setForm((prev) => ({ ...prev, password: e.target.value }))}
        />
        <button
          disabled={busy}
          onClick={handleLogin}
          className="mt-2 rounded-lg px-4 py-2 bg-blue-600 hover:bg-blue-500 disabled:opacity-50"
        >
          {busy ? "Đang đăng nhập…" : "Đăng nhập"}
        </button>
        {isAuthenticated && (
          <div className="text-xs text-green-400">
            Đã đăng nhập {user?.name ? `(${user.name})` : ""}.
          </div>
        )}
      </div>

      {/* Manual JWT token */}
      <div className="grid gap-2">
        <label htmlFor="jwt-token" className="text-sm">
          JWT Token
        </label>
        <textarea
          id="jwt-token"
          rows={3}
          className="bg-gray-900 border border-gray-700 rounded px-3 py-2 font-mono"
          placeholder="Dán JWT vào đây…"
          value={jwtDraft}
          onChange={(e) => setJwtDraft(e.target.value)}
        />
        <div className="flex items-center gap-2">
          <button
            onClick={handleSaveToken}
            className="rounded-lg px-4 py-2 bg-emerald-600 hover:bg-emerald-500"
          >
            Lưu token
          </button>
          <button onClick={logout} className="rounded-lg px-4 py-2 bg-gray-700 hover:bg-gray-600">
            Đăng xuất
          </button>
        </div>
      </div>

      {/* WS connect test */}
      <div className="grid gap-2">
        <div className="flex items-center justify-between">
          <div className="text-sm font-medium">Kết nối WebSocket</div>
          <div className="text-xs">
            Trạng thái:{" "}
            <span
              className={
                {
                  connected: "text-green-400",
                  connecting: "text-yellow-400",
                  error: "text-red-400",
                  closed: "text-gray-400",
                  idle: "text-gray-300",
                }[wsStatus]
              }
            >
              {wsStatus}
            </span>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={handleConnectWS}
            className="rounded-lg px-4 py-2 bg-indigo-600 hover:bg-indigo-500"
          >
            Kết nối thử WS
          </button>
          <button
            onClick={handleDisconnectWS}
            className="rounded-lg px-4 py-2 bg-gray-700 hover:bg-gray-600"
          >
            Ngắt WS
          </button>
        </div>
        <div className="text-xs text-gray-400">
          {wsAllowedNoToken
            ? "DEV đang cho phép WS không token (client)."
            : "WS yêu cầu token; server sẽ đóng 1008 nếu thiếu/invalid."}
        </div>
      </div>
    </div>
  );
};

export default LoginBox;
