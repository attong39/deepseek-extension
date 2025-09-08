#!/usr/bin/env python3
"""
Zeta AI Agent - Metrics Server (Python Assistant)
 - Tries to import dev_server.app if available
 - Fallback FastAPI app that proxies to Ollama's Turbo API (/v1/chat/completions)
"""

import os
import sys
from pathlib import Path
import Exception
import client
import dict
import e
import int
import print
import request
import str

# Add local zeta-ai-agent to path if present (optional)
current_dir = Path(__file__).parent
zeta_agent_dir = current_dir / "zeta-ai-agent"
if zeta_agent_dir.exists():
    sys.path.insert(0, str(zeta_agent_dir))

# Load .env if present
try:
    from dotenv import load_dotenv

    # Load defaults from .env and allow local overrides via .env.local
    load_dotenv()
    load_dotenv(".env.local", override=True)
except Exception:
    pass

# Try to use dev_server.app if provided by local agent module
try:
    from dev_server import app  # type: ignore

    print("✅ Successfully imported app from dev_server")
except Exception as e:
    print(f"❌ Failed to import dev_server: {e}")

    # Fallback: minimal FastAPI app with Ollama proxy
    from typing import Any

    import httpx as _httpx
    from fastapi import Body, FastAPI
    from fastapi.middleware.cors import CORSMiddleware

    app = FastAPI(
        title="Zeta AI Assistant Server",
        description="Fallback Python assistant proxying to Ollama Turbo API",
        version="1.0.0",
    )

    # Basic CORS for local dev (VS Code webviews, localhost)
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

    # Ollama configuration (override via env)
    _OLLAMA_BASE = os.getenv("OLLAMA_BASE_URL", os.getenv("OLLAMA_API_URL", "http://127.0.0.1:11434"))
    _OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "deepseek-coder:6.7b")

    @app.get("/health")
    async def health() -> dict[str, Any]:
        return {
            "status": "ok",
            "message": "Python assistant is running",
            "ollama": {"base_url": _OLLAMA_BASE, "model": _OLLAMA_MODEL},
        }

    @app.get("/metrics")
    async def metrics() -> dict[str, Any]:
        return {"message": "metrics-ok"}

    @app.get("/ai/model")
    async def get_model() -> dict[str, str]:
        return {"model": _OLLAMA_MODEL, "base_url": _OLLAMA_BASE}

    @app.post("/api/ask")
    async def api_ask(request: dict[str, Any] = Body(...)) -> dict[str, Any]:
        message = (request or {}).get("message") or (request or {}).get("prompt") or ""
        model = (request or {}).get("model") or _OLLAMA_MODEL

        # Try forwarding to Ollama Turbo API
        try:
            url = _OLLAMA_BASE.rstrip("/") + "/v1/chat/completions"
            payload = {
                "model": model,
                "messages": [{"role": "user", "content": message or "Xin chào!"}],
                "stream": False,
            }
            async with _httpx.AsyncClient(timeout=30.0) as client:
                resp = await client.post(url, json=payload)
                if resp.status_code == 200:
                    data = resp.json()
                    content = (
                        ((data.get("choices") or [{}])[0].get("message") or {}).get("content")
                        or data.get("response")
                        or ""
                    )
                    return {"response": content, "model": data.get("model", model)}
                else:
                    return {
                        "response": f"[mock:fallback] {message}",
                        "model": model,
                        "error": {"status": resp.status_code, "body": resp.text},
                    }
        except Exception as _exc:
            return {
                "response": f"[mock] {message or 'No message'}",
                "model": model,
                "error": str(_exc),
            }


# Export app for uvicorn
__all__ = ["app"]


if __name__ == "__main__":
    import uvicorn

    host = os.getenv("ZETA_HOST", "127.0.0.1")
    port = int(os.getenv("ZETA_PORT", "9100"))

    print(f"🚀 Starting Zeta AI Assistant Server at http://{host}:{port}")
    print("📋 Available endpoints:")
    print(f"   • Health: http://{host}:{port}/health")
    print(f"   • Metrics: http://{host}:{port}/metrics")
    print(f"   • AI Ask: http://{host}:{port}/api/ask")

    uvicorn.run("metrics_server:app", host=host, port=port, reload=False, log_level="debug")
