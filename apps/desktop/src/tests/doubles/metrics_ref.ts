import { vi } from "vitest";
import API from "../../API/index";
import REF from "REF";

/**
 * REF mutable để module bị test có thể gán lại: `ref.server = http.createServer(...)`.
 * Khởi tạo giá trị mặc định có API tối thiểu để test không null/undefined.
 */
const fakeServer = {
  listen: vi.fn((_port?: number, _host?: string, cb?: () => void) => { cb?.(); return fakeServer; }),
  close:  vi.fn((cb?: () => void) => { cb?.(); }),
  address: vi.fn(() => ({ address: "127.0.0.1", port: 0 })),
  on: vi.fn(),
};

export const ref: { server: any } = { server: fakeServer };
export default { ref };
