import React, { createContext, useCallback, useContext, useEffect, useMemo, useState } from "react";

import { login as apiLogin, type LoginRequest, type LoginResponse } from "@/services/api/auth";
import AuthContext from "./AuthContext";
import AuthContextType from "AuthContextType";
import AuthProvider from "AuthProvider";
import Error from "Error";
import FC from "FC";
import LoginRequest from "LoginRequest";
import LoginResponse from "LoginResponse";
import PropsWithChildren from "PropsWithChildren";
import Provider from "Provider";
import STORAGE_KEY from "STORAGE_KEY";
import UserInfo from "UserInfo";

type UserInfo = LoginResponse["user"] | null;

type AuthContextType = {
  token: string | null;
  user: UserInfo;
  isAuthenticated: boolean;
  login: (payload: LoginRequest) => Promise<void>;
  saveToken: (token: string, user?: UserInfo) => void;
  logout: () => void;
};

const AuthContext = createContext<AuthContextType | null>(null);

const STORAGE_KEY = "zeta_ai.jwt";

export const AuthProvider: React.FC<React.PropsWithChildren> = ({ children }) => {
  const [token, setToken] = useState<string | null>(null);
  const [user, setUser] = useState<UserInfo>(null);

  useEffect(() => {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (stored) {
      try {
        const { token: t, user: u } = JSON.parse(stored);
        setToken(t);
        setUser(u ?? null);
      } catch {
        /* ignore */
      }
    }
  }, []);

  const persist = (t: string | null, u: UserInfo) => {
    if (t) {
      localStorage.setItem(STORAGE_KEY, JSON.stringify({ token: t, user: u }));
    } else {
      localStorage.removeItem(STORAGE_KEY);
    }
  };

  const saveToken = useCallback((t: string, u?: UserInfo) => {
    setToken(t);
    setUser(u ?? null);
    persist(t, u ?? null);
  }, []);

  const login = useCallback(
    async (payload: LoginRequest) => {
      const res = await apiLogin(payload);
      saveToken(res.access_token, res.user ?? null);
    },
    [saveToken],
  );

  const logout = useCallback(() => {
    setToken(null);
    setUser(null);
    persist(null, null);
  }, []);

  const value = useMemo(
    () => ({ token, user, isAuthenticated: !!token, login, saveToken, logout }),
    [token, user, login, saveToken, logout],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
};
