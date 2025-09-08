"""
ZETA_VN Desktop Integration Demo API
Main FastAPI app với tất cả endpoints cho desktop integration
"""

from __future__ import annotations

from app.api.v1 import demo_training, health, logs, rules, uploads, ws
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import dict
import list
import str

# Tạo FastAPI app
app = FastAPI(
    title="ZETA_VN Desktop Integration API",
    description="API cho integration giữa Desktop App và AI Server",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS middleware cho desktop app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all routers
app.include_router(uploads.router)
app.include_router(demo_training.router)
app.include_router(rules.router)
app.include_router(logs.router)
app.include_router(health.router)
app.include_router(ws.router)


@app.get("/")
async def root() -> dict[str, str]:
    """Root endpoint"""
    return {
        "message": "ZETA_VN Desktop Integration API",
        "version": "1.0.0",
        "docs": "/docs",
    }


@app.get("/v1")
async def api_v1_info() -> dict[str, str | list[str]]:
    """API v1 info"""
    return {
        "version": "v1",
        "endpoints": [
            "/v1/uploads - File upload",
            "/v1/demo-training - Training jobs",
            "/v1/rules - AI rules management",
            "/v1/logs - System logs",
            "/v1/health - Health check",
            "/ws/training/{job_id} - Training WebSocket",
            "/ws/notify - Notifications WebSocket",
        ],
    }


if __name__ == "__main__":
    import uvicorn  # noqa: PLC0415

    uvicorn.run(
        "zeta_vn.app.demo_integration_main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )
