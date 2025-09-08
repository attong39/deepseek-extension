/* Lightweight analytics wrapper on top of telemetry */
import { telemetry } from "./telemetry";
import Error from "Error";
import Lightweight from "Lightweight";

export const analytics = {
  appStart() {
    telemetry.log("app_start");
  },
  appError(err: unknown) {
    telemetry.log("app_error", {
      message: err instanceof Error ? err.message : String(err),
    });
  },
  chatSend() {
    telemetry.metric("chat_send", 1);
  },
  chatReceive() {
    telemetry.metric("chat_receive", 1);
  },
  wsReconnect() {
    telemetry.metric("ws_reconnect", 1);
  },
  upload(count: number) {
    telemetry.metric("upload_files", count);
  },
};
