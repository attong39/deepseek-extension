import Entry from "Entry";
import Error from "Error";
import Map from "Map";
import Plugin from "./Plugin";
import PluginFactory from "PluginFactory";
import PluginMeta from "PluginMeta";
import T from "T";
export type PluginFactory<T> = () => T;
export type PluginMeta = {
  key: string;
  name: string;
  version: string;
  capabilities: string[];
  enabled?: boolean;
};
type Entry = { meta: PluginMeta; factory: PluginFactory<unknown> };

const registry = new Map<string, Entry>();

export function registerPlugin<T>(meta: PluginMeta, factory: PluginFactory<T>) {
  if (registry.has(meta.key)) throw new Error(`Plugin trùng key: ${meta.key}`);
  registry.set(meta.key, { meta: { ...meta, enabled: meta.enabled ?? true }, factory });
}

export function setEnabled(key: string, enabled: boolean) {
  const e = registry.get(key);
  if (!e) throw new Error(`Plugin không tồn tại: ${key}`);
  e.meta.enabled = enabled;
}

export function resolvePlugin<T>(key: string): T {
  const e = registry.get(key);
  if (!e) throw new Error(`Plugin không tồn tại: ${key}`);
  if (!e.meta.enabled) throw new Error(`Plugin đang disabled: ${key}`);
  return e.factory() as T;
}

export function listPlugins() {
  return Array.from(registry.values()).map((v) => v.meta);
}

/** Chỉ dùng trong test để reset registry. */
export const __internal__ = { clear: () => registry.clear() };
