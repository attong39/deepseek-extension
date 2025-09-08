# Zeta Tools: OCR & STT (Local)

This folder contains optional Python helpers for local OCR/STT.

## 1) PaddleOCR (CLI)

- Script: `tools/paddle_ocr_cli.py`
- Usage:
  - Windows PowerShell:
    python tools/paddle_ocr_cli.py --image "C:\\path\\image.png" --lang vi --json
- Output JSON: { ok: true, text: "..." } or { ok: false, error: "..." }
- Install (CPU):
  pip install paddlepaddle paddleocr
- GPU (optional):
  - Install appropriate `paddlepaddle-gpu` for your CUDA.
- Notes:
  - On Windows, you may need Microsoft VC++ runtime.

Electron wiring:
- Renderer captures screen → IPC `zeta:file:writeTemp` saves PNG in temp dir → IPC `zeta:ocr:paddle` spawns the CLI with the temp path.
- Timeout 30s + retry x2 built-in.

## 2) Whisper (faster-whisper)

- Script: `tools/whisper_server.py` (FastAPI skeleton)
- Run:
  python tools/whisper_server.py
- Endpoints:
  - POST http://127.0.0.1:8765/stt/start
  - POST http://127.0.0.1:8765/stt/stop
- Install:
  pip install faster-whisper fastapi uvicorn
- Model/runtime hints:
  - `--device auto` and `--compute_type int8_float16` recommended for low-spec.
  - Cache dir can be set via environment (e.g., `XDG_CACHE_HOME`).

Electron wiring:
- IPC `zeta:stt:whisper:start|stop` sends HTTP to the server (skeleton). For streaming partials, extend with WS and forward to renderer via IPC events.

## 3) Security/Packaging

- Always sanitize paths; current setup restricts OCR to OS temp directory.
- Run Python tools inside your app-managed virtualenv. Set `ZETA_PYTHON` env to the interpreter path if needed.
- For packaging on Windows, bundle Python/requirements or instruct users to install dependencies separately.
