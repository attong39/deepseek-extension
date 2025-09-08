import ConsentState from "ConsentState";
import KEY from "KEY";
type ConsentState = "accepted" | "declined" | "unknown";
const KEY = "zeta_consent";

export const consent = {
  status(): ConsentState {
    const v = localStorage.getItem(KEY);
    return v === "accepted" || v === "declined" ? (v as ConsentState) : "unknown";
  },
  accept() { localStorage.setItem(KEY, "accepted"); },
  decline() { localStorage.setItem(KEY, "declined"); },
  reset() { localStorage.removeItem(KEY); }
};
