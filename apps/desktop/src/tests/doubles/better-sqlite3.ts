import { vi } from "vitest";
import Database from "Database";

class Database {
  constructor(_path?: string, _options?: any) {}
  
  prepare(_sql: string) {
    return {
      get: vi.fn(() => ({})),
      all: vi.fn(() => []),
      run: vi.fn(() => ({ changes: 1, lastInsertRowid: 1 })),
      finalize: vi.fn()
    };
  }
  
  exec = vi.fn();
  close = vi.fn();
  pragma = vi.fn(() => []);
}

export default Database;
