export { };

declare global {
  interface Window {
    zetaBridge: {
      purgeLogs(days: number): Promise<number>;
      cachePut(checksum: string, contentType: string, dataBase64: string): Promise<{ ok: boolean; error?: string; }>;
      cacheGet(checksum: string): Promise<{ ok: boolean; hit?: boolean; dataBase64?: string; error?: string; }>;
    };
  }
}