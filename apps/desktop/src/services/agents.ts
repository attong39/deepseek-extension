import Agent from "Agent";
import AgentProfile from "AgentProfile";
import AgentState from "AgentState";
import LS_KEY from "LS_KEY";
import Omit from "Omit";
import Partial from "Partial";
import Record from "Record";
export type AgentProfile = {
  id: string;
  name: string;
  model?: string;
  temperature?: number;
  systemPrompt?: string;
  createdAt: number;
  updatedAt: number;
};

type AgentState = {
  currentId: string | null;
  items: Record<string, AgentProfile>;
};

const LS_KEY = "zeta_agents_state_v1";

function loadState(): AgentState {
  try {
    const raw = localStorage.getItem(LS_KEY);
    if (raw) return JSON.parse(raw) as AgentState;
  } catch {
    /* noop */
  }
  return { currentId: null, items: {} };
}

function saveState(s: AgentState) {
  try {
    localStorage.setItem(LS_KEY, JSON.stringify(s));
  } catch {
    /* noop */
  }
}

const state: AgentState = loadState();

export const agents = {
  list(): AgentProfile[] {
    return Object.values(state.items).sort((a, b) => a.createdAt - b.createdAt);
  },
  get(id: string): AgentProfile | null {
    return state.items[id] ?? null;
  },
  current(): AgentProfile | null {
    return state.currentId ? (state.items[state.currentId] ?? null) : null;
  },
  setCurrent(id: string | null) {
    state.currentId = id;
    saveState(state);
  },
  upsert(p: Omit<AgentProfile, "createdAt" | "updatedAt"> & Partial<AgentProfile>): AgentProfile {
    const now = Date.now();
    const prev = state.items[p.id];
    const createdAt = prev?.createdAt ?? now;
    const profile: AgentProfile = {
      id: p.id,
      name: p.name ?? prev?.name ?? "Agent",
      createdAt,
      updatedAt: now,
    } as AgentProfile;
    if (typeof (p.model ?? prev?.model) === "string")
      (profile as any).model = (p.model ?? prev?.model) as string;
    if (typeof (p.temperature ?? prev?.temperature) === "number")
      (profile as any).temperature = (p.temperature ?? prev?.temperature) as number;
    if (typeof (p.systemPrompt ?? prev?.systemPrompt) === "string")
      (profile as any).systemPrompt = (p.systemPrompt ?? prev?.systemPrompt) as string;
    state.items[p.id] = profile;
    if (!state.currentId) state.currentId = p.id;
    saveState(state);
    return profile;
  },
  remove(id: string) {
    delete state.items[id];
    if (state.currentId === id) state.currentId = null;
    saveState(state);
  },
};
