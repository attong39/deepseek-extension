# ZETA AI Desktop

Electron + React + Vite + TypeScript skeleton aligned with GUIDE.md.

- Run dev: starts Vite and Electron together
- Build: Vite build, then package for Windows

## Scripts

- npm run dev
- npm run build:win

## Env

Create `.env` with:

```
VITE_API_URL=http://127.0.0.1:8000
VITE_WS_URL=ws://127.0.0.1:8000/ws/chat
VITE_USE_WS=true
```

## Auth

- Use your server login endpoint to get JWT: POST /api/v1/auth/login with { username, password }
- Token is stored under localStorage key `zeta_token` and sent as Bearer for HTTP; appended as `?token=` for WS

## WebSocket

- If VITE_USE_WS=true, Chat will try WebSocket first, fall back to REST if not connected

## Recommended Stack (summary)

- UI: MUI (Material UI)
- State: Redux Toolkit or React Query
- REST client: generated SDK from OpenAPI (scripts/api_codegen.mjs)
- WS: native WebSocket client (src/services/socket.ts) with heartbeat/backoff
- Automation: nut.js / RobotJS via Electron main process; optional Python bridge for PaddleOCR / PyAutoGUI
- OCR: tesseract.js (quick) or PaddleOCR via IPC for Vietnamese accuracy
- STT: Web Speech API or Whisper for quality
- i18n: react-i18next (vi/en)
- Security: crypto-js (AES) for local storage + JWT for session tokens
- Packaging: electron-builder

## Automation & Native Integration

- Prefer running native automation in Electron main with IPC bridge.
- If Python is required (PaddleOCR/Whisper), spawn a local Python process and communicate via IPC or local HTTP.
- Provide a clear "Panic / Cancel" button in UI that sends an IPC to main to abort automation tasks.

## Useful commands

```bash
npm run dev
npm run api:gen
npm run test
npm run build:win
```

## How to verify CFCP

- After changing a server or core file, run:

```bash
python tools/check_related_files.py --staged
```

This will print suggested FE/server files to check/update.

## Auto-update (electron-updater)

This project ships a minimal wiring for `electron-updater` in `electron/main.ts` and exposes update events via the preload bridge under `window.zeta.update`.

- Events available in renderer:
  - `zeta:update:available` — update metadata when a new release is found
  - `zeta:update:progress` — download progress
  - `zeta:update:downloaded` — update ready to install

- Trigger install from renderer:
  - `await window.zeta.update.install()` — will call `autoUpdater.quitAndInstall()` in main

To test locally, publish a draft release or configure a local update server and run the app; check DevTools console for events.

## Publish workflow

A GitHub Actions workflow `publish-desktop.yml` will build and publish apps/desktop artifacts when you push a tag starting with `v` (e.g. `v0.1.0`). The workflow uses `electron-builder` and `GITHUB_TOKEN` to create a GitHub Release with artifacts. To trigger:

```bash
git tag v0.1.0
git push origin v0.1.0
```

Note: building Windows installers on Linux runners may require Wine; you can restrict targets or run builds on Windows runners for full Windows artifacts.

To build Windows artifacts via CI, there is a workflow `publish-windows.yml` that runs on `windows-latest` runner when a `v*` tag is pushed and publishes the installer to GitHub Releases.

## Publish config

Fill `desktop_ai_zeta/electron-builder.json` `publish` section with your GitHub `owner` and `repo`. Ensure repository has `GITHUB_TOKEN` or `PERSONAL_ACCESS_TOKEN` in Actions secrets to allow publishing releases. Example config is provided in `desktop_ai_zeta/electron/publish.example.json`.
