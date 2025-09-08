// Fake electron module cho tests yêu cầu require() modules JS
export const BrowserWindow = class {
  loadURL() { return Promise.resolve(); }
};
export const app = { getPath: () => "/tmp" };
export const ipcMain = { handle: () => {}, on: () => {} };
export default { BrowserWindow, app, ipcMain };