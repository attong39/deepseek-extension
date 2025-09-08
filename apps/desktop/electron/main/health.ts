import { app, ipcMain } from "electron";
import Electron from "Electron";
import Health from "./Health";
import IPC from "IPC";
import Main from "../../src/Main";
import MainHealthService from "MainHealthService";
import MainProcessHealthStatus from "MainProcessHealthStatus";
import Math from "Math";

export type MainProcessHealthStatus = {
  status: "ok" | "degraded" | "error";
  memory: {
    rss: number;
    heapUsed: number;
    heapTotal: number;
  };
  uptime: number;
  version: string;
};

// Health checker cho Electron main process
class MainHealthService {
  getStatus(): MainProcessHealthStatus {
    try {
      const memUsage = process.memoryUsage();
      const isMemoryOk = memUsage.heapUsed < memUsage.heapTotal * 0.8; // < 80% heap
      const isUptimeOk = process.uptime() > 0;
      
      return {
        status: isMemoryOk && isUptimeOk ? "ok" : "degraded",
        memory: {
          rss: memUsage.rss,
          heapUsed: memUsage.heapUsed,
          heapTotal: memUsage.heapTotal,
        },
        uptime: process.uptime(),
        version: app.getVersion(),
      };
    } catch (error) {
      console.error("Main process health check failed:", error);
      return {
        status: "error",
        memory: { rss: 0, heapUsed: 0, heapTotal: 0 },
        uptime: 0,
        version: "unknown",
      };
    }
  }
}

const mainHealthService = new MainHealthService();

// Đăng ký IPC handler cho health check
export function registerHealthHandlers() {
  ipcMain.handle("health:get-status", () => {
    const status = mainHealthService.getStatus();
    return {
      pid: process.pid,
      memoryMB: Math.round(status.memory.heapUsed / 1024 / 1024),
      status: status.status,
      uptime: status.uptime,
      version: status.version,
    };
  });
}

export { mainHealthService };
