import { __internal__, listPlugins, registerPlugin, resolvePlugin, setEnabled } from "@/services/plugin";
import Demo from "Demo";
import X from "X";

beforeEach(() => __internal__.clear());

it("register/resolve & guard duplicate", () => {
  registerPlugin({ key: "demo", name: "Demo", version: "1.0.0", capabilities: [] }, () => ({ ok: true }));
  expect(resolvePlugin<{ ok: boolean }>("demo").ok).toBe(true);
  expect(() => registerPlugin({ key: "demo", name: "X", version: "0.0.1", capabilities: [] }, () => ({}))).toThrow();
});

it("enable/disable works", () => {
  registerPlugin({ key: "x", name: "X", version: "1.0.0", capabilities: [], enabled: false }, () => ({}));
  expect(() => resolvePlugin("x")).toThrow();
  setEnabled("x", true);
  expect(() => resolvePlugin("x")).not.toThrow();
  const plugins = listPlugins();
  expect(plugins).toHaveLength(1);
  expect(plugins[0]?.enabled).toBe(true);
});
