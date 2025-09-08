import Electron from "Electron";
import Example from "Example";
import HTTP from "HTTP";
import IPC from "IPC";
import PaddleOCR from "PaddleOCR";
import Prefer from "Prefer";
import PyAutoGUI from "PyAutoGUI";
import Python from "Python";
import RPC from "RPC";
import Renderer from "Renderer";
import RobotCommand from "RobotCommand";
import RobotJS from "RobotJS";
import Skeleton from "Skeleton";
import This from "This";
/**
 * robotIntegration.ts
 *
 * Skeleton to integrate native automation libraries (nut.js / RobotJS) via
 * Electron main process. This module runs in the renderer and communicates
 * with the main process over a secure IPC channel.
 *
 * Nếu bạn cần một pipeline Python (PaddleOCR, PyAutoGUI), spawn process ở
 * main và expose a minimal RPC over stdio or local HTTP.
 */

export type RobotCommand =
  | { type: "move"; x: number; y: number }
  | { type: "click"; x: number; y: number; button?: "left" | "right" }
  | { type: "type"; text: string }
  | { type: "hotkey"; keys: string[] }
  | { type: "screenshot" };

// Renderer-side helper: send IPC to main
export function sendRobotCommand(cmd: RobotCommand): Promise<boolean> {
  // Prefer the sealed preload bridge if present (window.zeta.robot.exec)
  try {
    const anywin = window as any;
    if (typeof anywin?.zeta?.robot?.exec === "function") {
      return anywin.zeta.robot.exec(cmd);
    }
    if (typeof anywin?.electron?.ipcRenderer?.invoke === "function") {
      return anywin.electron.ipcRenderer.invoke("robot:exec", cmd);
    }
    console.warn("IPC not available - robot commands disabled");
    return Promise.resolve(false);
  } catch (e) {
    console.warn("sendRobotCommand error", e);
    return Promise.resolve(false);
  }
}

// Example usage: await sendRobotCommand({ type: 'click', x: 100, y: 200 })

export default { sendRobotCommand };
