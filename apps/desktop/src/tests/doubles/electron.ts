import { vi } from "vitest";
import BrowserWindow from "BrowserWindow";
import IAny from "IAny";

type IAny = any;

export class BrowserWindow {
  static _instances: BrowserWindow[] = [];
  static getAllWindows(): BrowserWindow[] { return [...BrowserWindow._instances]; }

  public webContents: { send: IAny; on: IAny; once: IAny };
  public loadURL = vi.fn(async (_u?: string) => {});
  public on = vi.fn((_e: string, _cb: IAny) => {});
  public once = vi.fn((_e: string, _cb: IAny) => {});
  public show = vi.fn(() => {});
  public hide = vi.fn(() => {});
  public isDestroyed = vi.fn(() => false);
  public destroy = vi.fn(() => {});

  constructor(_opts?: IAny) {
    this.webContents = { send: vi.fn(), on: vi.fn(), once: vi.fn() };
    BrowserWindow._instances.push(this);
  }
}

export const app = {
  getPath: (_k: string) => "/tmp",
  whenReady: async () => {},
  on: vi.fn(),
};

export const ipcMain = {
  handle: vi.fn(),
  on: vi.fn(),
  emit: vi.fn(),
};

export const ipcRenderer = {
  invoke: vi.fn(),
  on: vi.fn(),
  send: vi.fn(),
};

export default { BrowserWindow, app, ipcMain, ipcRenderer };
