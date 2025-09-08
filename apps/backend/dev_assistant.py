"""
Zeta AI - Minimal Python Assistant Server
 - FastAPI app exposing /health and /api/ask
 - Proxies to Ollama OpenAI-compatible Turbo API (/v1/chat/completions)
"""

from __future__ import annotations

import os
from typing import Any

import httpx
from fastapi import Body, FastAPI
from fastapi.middleware.cors import CORSMiddleware
import Exception
import client
import dict
import exc
import payload
import str

app = FastAPI(
    title="Zeta AI - Python Assistant",
    description="Minimal assistant server proxying to Ollama Turbo API",
    version="1.0.0",
)

# Allow local dev origins and VS Code webviews
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "vscode-webview:*",
        "https://vscode-webview.net",
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    max_age=86400,
)

OLLAMA_BASE = os.getenv(
    "OLLAMA_BASE_URL", os.getenv("OLLAMA_API_URL", "http://127.0.0.1:11434")
)
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "deepseek-coder:6.7b")


@app.get("/health")
async def health() -> dict[str, Any]:
    return {
        "status": "ok",
        "message": "Python assistant is running",
        "ollama": {"base_url": OLLAMA_BASE, "model": OLLAMA_MODEL},
    }


@app.post("/api/ask")
async def api_ask(payload: dict[str, Any] = Body(...)) -> dict[str, Any]:
    message = (payload or {}).get("message") or (payload or {}).get("prompt") or ""
    model = (payload or {}).get("model") or OLLAMA_MODEL

    # Forward to Ollama OpenAI-compatible Turbo API
    url = OLLAMA_BASE.rstrip("/") + "/v1/chat/completions"
    req = {
        "model": model,
        "messages": [{"role": "user", "content": message or "Xin chào!"}],
        "stream": False,
    }
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            resp = await client.post(url, json=req)
            if resp.status_code == 200:
                data = resp.json()
                content = (
                    ((data.get("choices") or [{}])[0].get("message") or {}).get(
                        "content"
                    )
                    or data.get("response")
                    or ""
                )
                return {"response": content, "model": data.get("model", model)}
            return {
                "response": f"[fallback] {message}",
                "model": model,
                "error": {"status": resp.status_code, "body": resp.text},
            }
    except Exception as exc:
        return {
            "response": f"[mock] {message or 'No message'}",
            "model": model,
            "error": str(exc),
        }


__all__ = ["app"]
