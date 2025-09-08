import { vi } from "vitest";
import Simulate from "Simulate";

let serverInstance: any = null;

const fakeServer = {
  listen: vi.fn((_port?: number, _host?: string, cb?: () => void) => { 
    // Simulate async listening
    queueMicrotask(() => fakeServer.emit("listening"));
    if (cb) cb(); 
    return fakeServer; 
  }),
  close:  vi.fn((cb?: () => void) => { 
    serverInstance = null;
    if (cb) cb(); 
  }),
  address: vi.fn(() => ({ address: "127.0.0.1", port: 8080 })),
  on: vi.fn(),
  emit: vi.fn()
};

export function createServer(_handler?: any): any {
  serverInstance = fakeServer;
  return fakeServer;
}

export default { createServer };
export { fakeServer as mockServer };
