import { create } from "zustand";
import ChatMessage from "ChatMessage";
import ChatState from "ChatState";
import Partial from "Partial";
import SetState from "SetState";
import T from "T";

export type ChatMessage = {
  role: "user" | "assistant";
  content: string;
  timestamp: string;
};

export type ChatState = {
  messages: ChatMessage[];
  add: (m: ChatMessage) => void;
  reset: () => void;
};

type SetState<T> = (
  partial: T | Partial<T> | ((state: T) => T | Partial<T>),
  replace?: boolean,
) => void;

export const useChatStore = create<ChatState>((set: SetState<ChatState>) => ({
  messages: [],
  add: (m: ChatMessage) => set((s: ChatState) => ({ messages: [...s.messages, m] })),
  reset: () => set({ messages: [] } as Partial<ChatState>),
}));
