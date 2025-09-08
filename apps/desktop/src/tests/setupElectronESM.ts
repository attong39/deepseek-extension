// ESM electron setup - đảm bảo 'electron' có cả default + named exports cho JS ESM tests
import { vi } from "vitest";
import ESM from "ESM";
import JS from "JS";
import Record from "Record";

vi.mock("electron", async () => {
  const mod = await import("./doubles/electron");
  const named = mod as Record<string, unknown>;
  const def = (mod as any).default ?? named;
  return { __esModule: true, default: def, ...named };
});
