import React, { useState } from "react";
import { useTranslation } from "react-i18next";

import { extractErrorCode, messageFor } from "../api/errorCodes";
import { login } from "../services/auth";
import FormEvent from "FormEvent";
import LoginForm from "./LoginForm";
import Props from "Props";

interface Props {
  readonly onLoggedIn: () => void;
}

export function LoginForm({ onLoggedIn }: Props) {
  const { t } = useTranslation();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      await login({ username, password });
      onLoggedIn();
    } catch (err) {
      const errorCode = extractErrorCode(err);
      const errorMessage = messageFor(errorCode, t("auth.login_failed"));
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form
      onSubmit={onSubmit}
      style={{
        border: "1px solid #ddd",
        padding: 16,
        borderRadius: 8,
        maxWidth: 360,
      }}
    >
      <h2>{t("auth.login")}</h2>
      <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
        <input
          placeholder={t("auth.username")}
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
          style={{ padding: "8px 10px" }}
        />
        <input
          placeholder={t("auth.password")}
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          style={{ padding: "8px 10px" }}
        />
        <button type="submit" disabled={loading} style={{ padding: "8px 10px" }}>
          {loading ? t("auth.logging_in") : t("auth.login")}
        </button>
        {error && <span style={{ color: "crimson" }}>{error}</span>}
      </div>
    </form>
  );
}
