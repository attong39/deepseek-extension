"""
Main entry point cho ứng dụng FastAPI trong môi trường production.

File này khởi tạo FastAPI app với các middleware bảo mật, routers, và logging chuẩn.
Tuân thủ Clean Architecture: app/ layer chỉ orchestrate, không chứa business logic.
"""

from __future__ import annotations

import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from starlette.middleware.base import BaseHTTPMiddleware
from uvicorn import run

from app.api.v1.router import api_v1_router  # Router chính từ app/api/v1/
from app.middlewares.rate_limit import (
import Exception
import ValueError
import call_next
import dict
import exc
import request
import str
    RateLimitMiddleware,  # Middleware rate-limiting (Redis-based)
)
from app.middlewares.security import (
    SecurityHeadersMiddleware,  # Middleware security headers
)
from app.middlewares.tracing import (
    TracingMiddleware,  # Middleware tracing headers + request_id
)
from config.settings import Settings  # Giả sử config module có Settings class với .env
from core.observability.logging import (
    setup_logging,  # Logger chuẩn dự án; fallback nếu không có
)


class RequestIDMiddleware(BaseHTTPMiddleware):
    """
    Middleware để thêm request_id vào mỗi request cho tracing.

    Args:
        app: FastAPI app instance.

    Returns:
        None
    """

    async def dispatch(self, request: Request, call_next) -> Response:
        request_id = request.headers.get("X-Request-ID", "unknown")
        logging.getLogger().extra = {"request_id": request_id}  # Inject vào logger
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Lifespan event cho FastAPI: khởi tạo và dọn dẹp resources async.

    Yields:
        None
    """
    # Khởi tạo: setup DB connections, caches, etc. (qua DI từ core/services)
    logging.info("Starting FastAPI app in production mode.")
    yield
    # Dọn dẹp: close connections
    logging.info("Shutting down FastAPI app.")


def create_app(settings: Settings) -> FastAPI:
    """
    Tạo và cấu hình FastAPI app instance.

    Args:
        settings: Cấu hình từ Settings class (không hard-code).

    Returns:
        FastAPI: App instance đã cấu hình.

    Raises:
        ValueError: Nếu settings không hợp lệ.
    """
    if not settings:
        raise ValueError("Settings phải được cung cấp và hợp lệ.")

    app = FastAPI(
        title="ZETA_VN API",
        version="1.0.0",
        description="API cho ZETA_VN với kiến trúc Clean và async.",
        lifespan=lifespan,
        docs_url="/docs"
        if settings.debug
        else None,  # Tắt docs trong prod nếu không debug
        redoc_url="/redoc" if settings.debug else None,
    )

    # Middleware bảo mật và tracing
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.allowed_hosts)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(
        SecurityHeadersMiddleware
    )  # Thêm headers bảo mật (CSP, HSTS, etc.)
    app.add_middleware(
        RateLimitMiddleware, redis_url=settings.redis_url
    )  # Rate-limiting với Redis
    app.add_middleware(TracingMiddleware)  # Tracing headers
    app.add_middleware(RequestIDMiddleware)  # Request ID cho logging

    # Exception handlers
    @app.exception_handler(ValidationError)
    async def validation_exception_handler(
        request: Request, exc: ValidationError
    ) -> JSONResponse:
        logging.error(
            f"Validation error: {exc}",
            extra={"request_id": request.headers.get("X-Request-ID")},
        )
        return JSONResponse(status_code=422, content={"detail": exc.errors()})

    @app.exception_handler(Exception)
    async def general_exception_handler(
        request: Request, exc: Exception
    ) -> JSONResponse:
        logging.error(
            f"Unexpected error: {exc}",
            exc_info=True,
            extra={"request_id": request.headers.get("X-Request-ID")},
        )
        return JSONResponse(
            status_code=500, content={"detail": "Internal server error"}
        )

    # Include routers
    app.include_router(api_v1_router, prefix="/api/v1", tags=["v1"])

    # Health check endpoint (không cần auth)
    @app.get("/health", summary="Health check")
    async def health_check() -> dict[str, str]:
        """Endpoint kiểm tra sức khỏe app."""
        return {"status": "ok"}

    return app


def main() -> None:
    """
    Entry point chính để chạy app với uvicorn trong production.

    Sử dụng async driver và config từ settings.
    """
    settings = Settings()  # Load từ .env
    setup_logging(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(request_id)s - %(message)s",
    )  # Setup logger chuẩn

    app = create_app(settings)
    run(
        app,
        host=settings.host,
        port=settings.port,
        workers=settings.workers,
        loop="uvloop",  # Async loop tối ưu
        http="httptools",  # HTTP parser nhanh
        access_log=True,
    )


if __name__ == "__main__":
    main()
