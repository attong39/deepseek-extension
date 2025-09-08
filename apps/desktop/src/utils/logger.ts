import ZETA from "ZETA";
export function logInfo(...args: unknown[]) {
  // eslint-disable-next-line no-console
  console.info("[ZETA]", ...args);
}

export function logWarn(...args: unknown[]) {
  // eslint-disable-next-line no-console
  console.warn("[ZETA]", ...args);
}

export function logError(...args: unknown[]) {
  // eslint-disable-next-line no-console
  console.error("[ZETA]", ...args);
}
