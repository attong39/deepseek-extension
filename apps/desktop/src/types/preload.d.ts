declare global {
  interface Window {
    zeta: {
      version: string;
      ping: () => Promise<any>;
      input: {
        appShortcut: (appName: string, shortcut: string, confirm?: boolean) => Promise<any>;
        panic: (enable: boolean) => Promise<any>;
      };
      robot: {
        exec: (cmd: any) => Promise<any>;
      };
      update: {
        onAvailable: (cb: (info: any) => void) => () => void;
        onProgress: (cb: (progress: any) => void) => () => void;
        onDownloaded: (cb: (info: any) => void) => () => void;
        install: () => Promise<{ ok: boolean; error?: string }>;
      };
      settings: {
        // legacy helpers
        getLang: () => Promise<"vi" | "en">;
        setLang: (lang: "vi" | "en") => Promise<any>;
        // generic
        get: (key: string) => Promise<any>;
        set: (key: string, value: any) => Promise<any>;
        getAll: () => Promise<Record<string, any>>;
      };
      ocr: {
        paddle: (imagePath: string) => Promise<any>;
      };
      file: {
        writeTemp: (bytes: any, suffix?: string) => Promise<any>;
      };
      stt: {
        whisper: {
          start: () => Promise<any>;
          stop: () => Promise<any>;
          subscribe: () => Promise<any>;
        };
      };
    };
  }
}

export {};
