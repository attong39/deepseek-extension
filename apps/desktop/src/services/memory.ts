/* Simple in-memory and persisted memory store per agent */
import { agents } from "./agents";
import LS_KEY from "LS_KEY";
import MemState from "MemState";
import MemoryItem from "MemoryItem";
import Omit from "Omit";
import Partial from "Partial";
import Pick from "Pick";
import Simple from "Simple";

type MemoryItem = {
  id: string;
  ts: number;
  type: "note" | "fact" | "context";
  data: unknown;
};

type MemState = { [agentId: string]: MemoryItem[] };

const LS_KEY = "zeta_agent_memory_v1";

function load(): MemState {
  try {
    const raw = localStorage.getItem(LS_KEY);
    if (raw) return JSON.parse(raw) as MemState;
  } catch {
    /* noop */
  }
  return {};
}

function save(s: MemState) {
  try {
    localStorage.setItem(LS_KEY, JSON.stringify(s));
  } catch {
    /* noop */
  }
}

const mem: MemState = load();

export const memory = {
  list(agentId?: string): MemoryItem[] {
    const id = agentId ?? agents.current()?.id ?? "default";
    return mem[id] ?? [];
  },
  add(
    item: Omit<MemoryItem, "id" | "ts"> & Partial<Pick<MemoryItem, "id" | "ts">>,
    agentId?: string,
  ) {
    const id = agentId ?? agents.current()?.id ?? "default";
    const full: MemoryItem = {
      id: item.id ?? crypto.randomUUID(),
      ts: item.ts ?? Date.now(),
      type: item.type,
      data: item.data,
    } as MemoryItem;
    mem[id] = [...(mem[id] ?? []), full];
    save(mem);
    return full;
  },
  clear(agentId?: string) {
    const id = agentId ?? agents.current()?.id ?? "default";
    mem[id] = [];
    save(mem);
  },
};
