import BUILD_INFO from "BUILD_INFO";
import VITE_APP_VERSION from "VITE_APP_VERSION";
import VITE_BUILD_TIME from "VITE_BUILD_TIME";
import VITE_GIT_SHA from "VITE_GIT_SHA";
export const BUILD_INFO = {
  version: import.meta.env.VITE_APP_VERSION ?? "dev",
  gitSha: import.meta.env.VITE_GIT_SHA ?? "unknown",
  buildTime: import.meta.env.VITE_BUILD_TIME ?? "unknown",
  platform: navigator.userAgent,
} as const;
