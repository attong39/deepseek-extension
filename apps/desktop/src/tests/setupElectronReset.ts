import { afterEach } from "vitest";

import * as electron from "../tests/doubles/electron";
import BrowserWindow from "BrowserWindow";

afterEach(() => {
  // @ts-ignore – truy cập private để dọn state
  if (electron.BrowserWindow && electron.BrowserWindow._instances) {
    // @ts-ignore
    electron.BrowserWindow._instances.length = 0;
  }
});
