import { useCallback, useEffect, useState } from "react";

import { apiClient } from "../api/apiClient";
import { API } from "../constants";
import { analytics } from "../services/analytics";
import { memory } from "../services/memory";
import { socketBus } from "../services/socket";
import { RateLimiter } from "../utils/rateLimiter";
import CHAT from "../pages/CHAT";
import ChatMessage from "ChatMessage";
import Error from "Error";
import Optional from "Optional";
import Unknown from "Unknown";
import WebSocket from "WebSocket";

export type ChatMessage = {
  /** Optional id cho message; có thể từ server hoặc client generate */
  id?: string;
  role: "user" | "assistant";
  content: string;
  timestamp: string;
};

export function useChat() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [wsConnected, setWsConnected] = useState(false);
  const limiter = new RateLimiter(5, 1);

  useEffect(() => {
    const offOpen = socketBus.on("open", () => setWsConnected(true));
    const offClose = socketBus.on("close", () => setWsConnected(false));
    const offError = socketBus.on("error", () => setError("WebSocket error"));
    const offMsg = socketBus.on("message", (data) => {
      if (data && typeof (data as any).content === "string") {
        const d = data as any;
        const reply: ChatMessage = {
          role: "assistant",
          content: String(d.content),
          timestamp: String(d.timestamp ?? new Date().toISOString()),
        };
        setMessages((prev: ChatMessage[]) => [...prev, reply]);
        analytics.chatReceive();
      }
    });
    // kick connection once
    socketBus.connect();
    return () => {
      offOpen();
      offClose();
      offError();
      offMsg();
    };
  }, []);

  const sendMessage = useCallback(async (text: string) => {
    setLoading(true);
    setError(null);
    const userMsg: ChatMessage = {
      role: "user",
      content: text,
      timestamp: new Date().toISOString(),
    };
    setMessages((prev: ChatMessage[]) => [...prev, userMsg]);
    try {
      // rate limit sending
      if (!limiter.allow()) {
        setError("Đang quá tải, vui lòng thử lại sau.");
        return;
      }
      analytics.chatSend();
      // store simple context
      memory.add({ type: "context", data: { last_user_message: text } });
      if (wsConnected) {
        socketBus.send({ message: text });
      } else {
        const resp = await apiClient.post(API.CHAT, { message: text });
        const data = resp.data as { content: string; timestamp?: string };
        const reply: ChatMessage = {
          role: "assistant",
          content: data.content ?? "",
          timestamp: data.timestamp ?? new Date().toISOString(),
        };
        setMessages((prev: ChatMessage[]) => [...prev, reply]);
        analytics.chatReceive();
      }
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : "Unknown error");
    } finally {
      setLoading(false);
    }
  }, []);

  return { messages, loading, error, sendMessage, wsConnected };
}
