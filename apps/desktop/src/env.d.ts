/// <reference types="vite/client" />

/**
 * Vite chỉ “lộ” biến môi trường có prefix VITE_ cho renderer.
 * TUYỆT ĐỐI không đặt secret ở đây. Secret để ở electron-main (không có prefix VITE_).
 */
interface ImportMetaEnv {
  readonly VITE_ENV: "development" | "staging" | "production";
  readonly VITE_APP_NAME: string;

  // Kết nối AI Server
  readonly VITE_API_BASE_URL: string; // ví dụ http://localhost:8000
  readonly VITE_WS_URL: string; // ví dụ ws://localhost:8000

  // Dev flags
  readonly VITE_DEV_ALLOW_WS_NO_TOKEN: "true" | "false";
  readonly VITE_APP_ENV: "development" | "production";

  // i18n & tính năng
  readonly VITE_I18N_DEFAULT_LANG: "vi" | "en";
  readonly VITE_FEATURE_OCR: "on" | "off";
  readonly VITE_FEATURE_STT: "on" | "off";

  // Observability / hành vi client
  readonly VITE_TELEMETRY_ENABLED: "true" | "false";
  readonly VITE_SENTRY_DSN?: string;
  readonly VITE_LOG_LEVEL: "debug" | "info" | "warn" | "error";
  readonly VITE_UPDATE_CHANNEL?: "stable" | "beta" | "nightly";

  // Dev tiện lợi (không dùng cho prod)
  readonly VITE_AUTH_DEFAULT_TOKEN?: string;
  readonly VITE_WEBSOCKET_RETRY_MAX?: string; // số lần retry, dạng chuỗi số

  // Metadata build (tùy chọn)
  readonly VITE_BUILD_SHA?: string;
  readonly VITE_BUILD_TIME?: string;

  // Client-side crypto demo key (dev-only; không dùng cho prod secret)
  readonly VITE_CLIENT_AES_KEY?: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}

/**
 * Electron preload có thể inject thêm global an toàn cho renderer.
 * Không cần có cũng không lỗi.
 */
declare global {
  interface Window {
    electron?: {
      ipcRenderer: {
        on: (channel: string, listener: (...args: any[]) => void) => void;
        send: (channel: string, ...args: any[]) => void;
        invoke?: (channel: string, ...args: any[]) => Promise<any>;
      };
    };
    // Cho phép main process truyền API URL động vào renderer (không qua VITE_)
    DESKTOP_API_BASE_URL?: string;

    // Tiếp tục hỗ trợ API preload hiện hữu (không bắt buộc)
    zeta?: {
      version: string;
      ping(): Promise<{ pong: number }>;
      input?: {
        appShortcut(
          appName: string,
          shortcut: string,
          confirm?: boolean,
        ): Promise<{ ok: boolean; error?: string }>;
        panic(enable: boolean): Promise<{ ok: boolean; panic: boolean }>;
      };
      ocr?: {
        paddle(imagePath: string): Promise<{ ok: boolean; text?: string; error?: string }>;
      };
      stt?: {
        whisper: {
          start(): Promise<{ ok: boolean; error?: string }>;
          stop(): Promise<{ ok: boolean; error?: string }>;
        };
      };
      file?: {
        writeTemp(
          bytes: number[],
          suffix?: string,
        ): Promise<{ ok: boolean; path?: string; error?: string }>;
      };
    };
  }
}

export {};
