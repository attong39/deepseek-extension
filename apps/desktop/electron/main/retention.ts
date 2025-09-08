import { app, ipcMain } from "electron";
import fs from "node:fs";
import path from "node:path";
import Crashpad from "Crashpad";
import IPC from "IPC";
import Math from "Math";

function purgeOlderThan(dir: string, days: number) {
  const now = Date.now();
  const threshold = days * 24 * 60 * 60 * 1000;
  if (!fs.existsSync(dir)) return 0;
  let count = 0;
  for (const f of fs.readdirSync(dir)) {
    const fp = path.join(dir, f);
    try {
      const st = fs.statSync(fp);
      if (now - st.mtimeMs > threshold) {
        fs.rmSync(fp, { recursive: true, force: true });
        count++;
      }
    } catch { /* ignore */ }
  }
  return count;
}

/** Gắn IPC: 'zeta:purgeLogs' — trả về số file đã xóa */
export function registerRetentionIPC() {
  ipcMain.handle("zeta:purgeLogs", (_evt, days = 30) => {
    const crashpadDir = path.join(app.getPath("userData"), "Crashpad", "reports");
    const crashesDir = path.join(app.getPath("userData"), "crashes");
    
    let count = 0;
    count += purgeOlderThan(crashpadDir, Math.max(1, days | 0));
    count += purgeOlderThan(crashesDir, Math.max(1, days | 0));
    
    return count;
  });
}
