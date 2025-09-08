import { app, crashReporter } from "electron";
import fs from "node:fs";
import path from "node:path";
import Crash from "Crash";
import Desktop from "Desktop";
import Initialized from "Initialized";
import Reporter from "Reporter";
import ZETA from "ZETA";
import ZETA_AI from "ZETA_AI";

/** Bật crash reporter ghi file local (không gửi ra server). */
export function setupCrashReporter() {
  const dir = path.join(app.getPath("userData"), "crashes");
  fs.mkdirSync(dir, { recursive: true });
  
  crashReporter.start({
    companyName: "ZETA_AI",
    productName: "ZETA Desktop",
    submitURL: "https://example.invalid/crash", // không dùng, chỉ ghi file
    uploadToServer: false,
    compress: true,
    ignoreSystemCrashHandler: true,
    rateLimit: true,
    extra: { 
      channel: app.isPackaged ? "prod" : "dev",
      version: app.getVersion(),
      platform: process.platform,
      arch: process.arch,
    },
  });
  
  console.log(`[Crash Reporter] Initialized - logs to: ${dir}`);
}
