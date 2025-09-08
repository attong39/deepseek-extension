import Exception
import ImportError
import bool
import call_next
import client
import conn
import dict
import e
import exc
import getattr
import hasattr
import import_path
import int
import list
import locals
import payload
import prefix
import r
import request
import router_attr
import str
import tags
import ve
# zeta_vn/app/main.py
"""
ZETA_VN FastAPI Application - Clean & Production Ready

Features:
- Lifespan management với DB ping
- Auto-discovery routers với graceful fallback
- Request ID + timing middleware
- Clean exception handling
- Health/readiness endpoints
- Environment-based configuration
"""

from __future__ import annotations

import asyncio
import logging
import os
import time
import uuid
from contextlib import asynccontextmanager

import httpx
from fastapi import Body, FastAPI, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware

# Compatibility check import
try:
    from apps.backend.app.compat.startup_check import report as _compat_report
except ImportError:
    # Fallback nếu compat module chưa có
    def _compat_report():
        return {}

# Optional: DB ping trong lifespan (nếu có SQLAlchemy async engine)
try:
    from apps.backend.app import (
        dependencies as deps,
    )
    from sqlalchemy import text

    _HAS_DB = True
except Exception:  # pragma: no cover
    _HAS_DB = False
    deps = None  # type: ignore


# ------------------------------------------------------------
# App Configs
# ------------------------------------------------------------
PROJECT_NAME = os.getenv("PROJECT_NAME", "ZETA_VN API")
ENV = os.getenv("ENV", "dev")
DEBUG = os.getenv("DEBUG", "0") in {"1", "true", "TRUE"}
API_PREFIX = os.getenv("API_PREFIX", "/api/v1")
DOCS_URL = os.getenv("DOCS_URL", "/docs")
REDOC_URL = os.getenv("REDOC_URL", "/redoc")
ALLOWED_ORIGINS = os.getenv("CORS_ALLOW_ORIGINS", "*").split(",")
TRUSTED_HOSTS = os.getenv("TRUSTED_HOSTS", "*").split(",")

# logging chuẩn
logger = logging.getLogger(PROJECT_NAME)
logging.basicConfig(level=logging.DEBUG if DEBUG else logging.INFO)


# ------------------------------------------------------------
# OpenAPI Tags (có thể tuỳ biến thêm)
# ------------------------------------------------------------
TAGS_METADATA = [
    {"name": "health", "description": "Health & readiness checks."},
    {"name": "agents", "description": "Quản lý AI Agents (domain + service)."},
    {"name": "auth", "description": "Đăng nhập / JWT / quyền truy cập."},
    {"name": "analytics", "description": "Metrics & events."},
    {"name": "assistants", "description": "Assistant endpoints."},
    {"name": "automation", "description": "Tác vụ tự động hoá."},
]


# ------------------------------------------------------------
# Lifespan: warm-up & DB ping
# ------------------------------------------------------------
async def _ping_db() -> bool:
    if not _HAS_DB or deps is None:
        return False
    try:
        # deps._ENGINE được tạo trong app/dependencies.py (create_async_engine)
        async with deps._ENGINE.begin() as conn:  # type: ignore[attr-defined]
            await conn.execute(text("SELECT 1"))
        return True
    except Exception as exc:  # pragma: no cover
        logger.warning("DB ping failed: %s", exc)
        return False


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting %s (env=%s, debug=%s)...", PROJECT_NAME, ENV, DEBUG)

    # ===== STARTUP COMPATIBILITY CHECK =====
    compat_info = _compat_report()
    logger.info(f"NumPy Compatibility Check: {compat_info}")

    # Initialize event system
    try:
        from apps.backend.app.deps import build_outbox_dispatcher, init_event_handlers

        # Initialize event handlers
        init_event_handlers()
        logger.info("Event handlers initialized")

        # Start outbox dispatcher if DB available
        outbox_task = None
        if _HAS_DB:
            try:
                # Create a mock session factory for now
                async def mock_session_factory():
                    return None  # Will be replaced with real session factory

                dispatcher = build_outbox_dispatcher(mock_session_factory)
                outbox_task = asyncio.create_task(dispatcher.run_forever())
                logger.info("Outbox dispatcher started")
            except Exception as e:
                logger.warning(f"Failed to start outbox dispatcher: {e}")

        # Store task in app state for cleanup
        app.state.outbox_task = outbox_task
        app.state.dispatcher = locals().get("dispatcher")

    except Exception as e:
        logger.warning(f"Failed to initialize event system: {e}")

    # Database check
    db_ok = await _ping_db()
    if db_ok:
        logger.info("Database connection: OK")
    else:
        if _HAS_DB:
            logger.warning(
                "Database connection: NOT READY (will continue and retry lazily)"
            )
        else:
            logger.info("No database dependencies found; skipping DB ping.")

    # (tuỳ chọn) Warm-up handlers/routers nhẹ nhàng nếu cần
    await asyncio.sleep(0)  # nhường event loop

    yield

    # Shutdown
    logger.info("Shutting down %s ...", PROJECT_NAME)

    # Stop outbox dispatcher
    if hasattr(app.state, "dispatcher") and app.state.dispatcher:
        app.state.dispatcher.stop()
    if hasattr(app.state, "outbox_task") and app.state.outbox_task:
        app.state.outbox_task.cancel()
        try:
            await app.state.outbox_task
        except asyncio.CancelledError:
            pass
        logger.info("Outbox dispatcher stopped")

    # Không cần đóng engine ở đây vì session_factory/engine lifecycle do deps quản lý


# ------------------------------------------------------------
# App Instance + Middlewares
# ------------------------------------------------------------
app = FastAPI(
    title=PROJECT_NAME,
    description="ZETA_VN – FastAPI service cho domain/service layer hiện đại (immutability, invariants, UoW, repos).",
    version=os.getenv("APP_VERSION", "0.1.0"),
    openapi_tags=TAGS_METADATA,
    docs_url=DOCS_URL,
    redoc_url=REDOC_URL,
    debug=DEBUG,
    lifespan=lifespan,
    middleware=[
        Middleware(
            CORSMiddleware,
            allow_origins=["*"] if ALLOWED_ORIGINS == ["*"] else ALLOWED_ORIGINS,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
            expose_headers=["X-Request-ID", "X-Process-Time"],
        ),
        Middleware(GZipMiddleware, minimum_size=1024),
    ],
)


# ------------------------------------------------------------
# Request ID + Process Time Middleware
# ------------------------------------------------------------
@app.middleware("http")
async def add_request_id_and_timing(request: Request, call_next):
    req_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
    start = time.perf_counter()

    # gắn vào state để handlers truy cập nếu cần
    request.state.request_id = req_id

    try:
        response: Response = await call_next(request)
    except RequestValidationError as ve:  # cho chắc, dù đã có handler riêng
        response = await validation_exception_handler(request, ve)
    except Exception as exc:
        logger.exception("Unhandled error (req_id=%s): %s", req_id, exc)
        response = JSONResponse(
            status_code=500,
            content={"error": "internal_server_error", "request_id": req_id},
        )

    duration = time.perf_counter() - start
    # set header
    response.headers["X-Request-ID"] = req_id
    response.headers["X-Process-Time"] = f"{duration:.6f}s"
    return response


# ------------------------------------------------------------
# Exception Handlers
# ------------------------------------------------------------
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    req_id = getattr(request.state, "request_id", None) or "n/a"
    logger.debug("ValidationError (req_id=%s): %s", req_id, exc)
    return JSONResponse(
        status_code=422,
        content={
            "error": "validation_error",
            "details": exc.errors(),
            "request_id": req_id,
        },
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    req_id = getattr(request.state, "request_id", None) or "n/a"
    logger.exception("UnhandledException (req_id=%s): %s", req_id, exc)
    return JSONResponse(
        status_code=500,
        content={"error": "internal_server_error", "request_id": req_id},
    )


# ------------------------------------------------------------
# Routers – auto-include nếu module tồn tại
# ------------------------------------------------------------
def _maybe_include_router(
    import_path: str,
    router_attr: str = "router",
    prefix: str | None = None,
    tags: list[str] | None = None,
) -> None:
    """
    import_path: ví dụ 'zeta_vn.app.api.v1.agents'
    router_attr: tên biến router trong module
    """
    try:
        module = __import__(import_path, fromlist=["*"])
        router = getattr(module, router_attr, None)
        if router is None:
            logger.debug("Module %s không có '%s', bỏ qua.", import_path, router_attr)
            return
        app.include_router(router, prefix=(prefix or API_PREFIX), tags=tags)
        logger.info(
            "Included router: %s (prefix=%s)", import_path, prefix or API_PREFIX
        )
    except Exception as exc:  # pragma: no cover
        logger.debug("Không thể include %s: %s", import_path, exc)


# Include các nhóm API phổ biến
_maybe_include_router("zeta_vn.app.api.v1.agents")
_maybe_include_router("zeta_vn.app.api.v1.agents_demo")  # Demo agents - no DB required
_maybe_include_router("zeta_vn.app.api.v1.auth")
_maybe_include_router("zeta_vn.app.api.v1.analytics")
_maybe_include_router("zeta_vn.app.api.v1.assistants")
_maybe_include_router("zeta_vn.app.api.v1.automation")

# Security and policy endpoints (RC v1.1.0)
_maybe_include_router("zeta_vn.app.api.v1.security.policy_router")

# Outbox admin endpoints
_maybe_include_router("zeta_vn.app.api.v1.endpoints.admin_outbox")


# ------------------------------------------------------------
# Health / Ready / Root
# ------------------------------------------------------------
@app.get("/", tags=["health"], response_class=JSONResponse)
async def root_info(request: Request):
    return {
        "name": PROJECT_NAME,
        "version": app.version,
        "env": ENV,
        "docs": DOCS_URL,
        "redoc": REDOC_URL,
        "request_id": getattr(request.state, "request_id", None),
        "routers_included": [
            r.path
            for r in app.routes
            if getattr(r, "path", None) and r.path.startswith(API_PREFIX)
        ],
    }


@app.get("/healthz", tags=["health"], response_class=JSONResponse)
async def healthz():
    db = await _ping_db()
    return {"status": "ok", "db": "ok" if db else "skip"}


@app.get("/readyz", tags=["health"], response_class=JSONResponse)
async def readyz():
    # Strict hơn healthz: yêu cầu DB (nếu có cấu hình)
    if _HAS_DB:
        ok = await _ping_db()
        if not ok:
            return JSONResponse(
                status_code=503, content={"status": "not_ready", "db": "down"}
            )
        return {"status": "ready", "db": "ok"}
    return {"status": "ready", "db": "n/a"}


# ------------------------------------------------------------
# Uvicorn Entrypoint (chạy trực tiếp: python -m zeta_vn.app.main)
# ------------------------------------------------------------

# ------------------------------------------------------------
# Minimal Assistant Endpoint (Ollama Turbo proxy)
# ------------------------------------------------------------
OLLAMA_BASE = os.getenv(
    "OLLAMA_BASE_URL", os.getenv("OLLAMA_API_URL", "http://127.0.0.1:11434")
)
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "deepseek-coder:6.7b")


@app.post("/api/ask", tags=["assistants"], response_class=JSONResponse)
async def api_ask(payload: dict = Body(...)):
    """
    Simple assistant endpoint proxying to Ollama OpenAI-compatible Turbo API.
    Expects: { "message": str, "model"?: str }
    Returns: { "response": str, "model": str }
    """
    message = (payload or {}).get("message") or (payload or {}).get("prompt") or ""
    model = (payload or {}).get("model") or OLLAMA_MODEL

    url = OLLAMA_BASE.rstrip("/") + "/v1/chat/completions"
    req = {
        "model": model,
        "messages": [{"role": "user", "content": message or "Xin chào!"}],
        "stream": False,
    }
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
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
            return JSONResponse(
                status_code=resp.status_code,
                content={
                    "error": "ollama_error",
                    "status": resp.status_code,
                    "body": resp.text,
                },
            )
    except Exception as exc:
        logger.warning("/api/ask proxy failed: %s", exc)
        return JSONResponse(
            status_code=502,
            content={"error": "upstream_unavailable", "message": str(exc)},
        )


def _get_port() -> int:
    try:
        return int(os.getenv("PORT", "8000"))
    except Exception:
        return 8000


if __name__ == "__main__":  # pragma: no cover
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=_get_port(),
        reload=DEBUG,
        log_level="debug" if DEBUG else "info",
        workers=int(os.getenv("WEB_CONCURRENCY", "1")),
    )
