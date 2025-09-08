#!/usr/bin/env python3
"""
Minimal Whisper server using faster-whisper.
Endpoints:
  POST /stt/start -> {ok:true}
  POST /stt/stop  -> {ok:true}
  WebSocket /stt/stream to send audio chunks (not implemented in this skeleton).

Note: This is a stub to be extended per deployment needs.
"""

from __future__ import annotations

import asyncio

import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
import Exception
import i
import range
import ws

app = FastAPI(title="Zeta Whisper Server")

_running = False


@app.post("/stt/start")
async def stt_start():
    global _running
    _running = True
    # Placeholder: load model, spawn worker if needed
    return JSONResponse({"ok": True})


@app.post("/stt/stop")
async def stt_stop():
    global _running
    _running = False
    # Placeholder: teardown resources
    return JSONResponse({"ok": True})


def main():
    uvicorn.run(app, host="127.0.0.1", port=8765)


if __name__ == "__main__":
    main()


# WebSocket stream demo (placed after main guard for clarity but executed on import)
@app.websocket("/stt/stream")
async def stt_stream(ws: WebSocket):
    await ws.accept()
    try:
        # Demo partials every 300ms; in real impl, forward decoder partials
        for i in range(10):
            await asyncio.sleep(0.3)
            await ws.send_text(f"partial-{i}")
        await ws.send_text("[end]")
    except WebSocketDisconnect:
        return
    finally:
        try:
            await ws.close()
        except Exception:
            pass
