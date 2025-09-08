from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Any
import os
import time
import uuid

            from fastapi import HTTPException
from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from apps.backend.core.observability.logging import get_logger

"""Consolidated Security Middleware for Zeta AI.
Hợp nhất concerns bảo mật phổ biến (headers, validation, tracing) với cấu hình
linh hoạt qua tham số khởi tạo hoặc biến môi trường.
"""
logger = get_logger(__name__)
class ConsolidatedSecurityMiddleware(BaseHTTPMiddleware):
    """Middleware bảo mật tổng hợp cho Zeta AI."""
    def __init__(
        self,
        app: Any,
        *,
        enable_csrf: bool | None = None,
        enable_xss_protection: bool | None = None,
        enable_content_type_sniffing: bool | None = None,
        max_request_size: int | None = None,
        enable_hsts: bool | None = None,
        enable_rate_limit_headers: bool | None = None,
        content_security_policy: str | None = None,
    ) -> None:
        """Initialize consolidated security middleware.
        Args:
            app: FastAPI/Starlette app instance.
            enable_csrf: Enable CSRF-related headers (X-Frame-Options, X-Content-Type-Options).
            enable_xss_protection: Enable legacy X-XSS-Protection header.
            enable_content_type_sniffing: If False, sets X-Content-Type-Options=nosniff.
            max_request_size: Maximum request size in bytes (uses Content-Length).
            enable_hsts: Enable Strict-Transport-Security header for HTTPS.
            enable_rate_limit_headers: Emit simple rate limit hints headers.
            content_security_policy: Override default Content-Security-Policy.
        """
        super().__init__(app)
        self.enable_csrf = (
            enable_csrf
            if enable_csrf is not None
            else os.getenv("SEC_MW_ENABLE_CSRF", "true").lower() == "true"
        )
        self.enable_xss_protection = (
            enable_xss_protection
            if enable_xss_protection is not None
            else os.getenv("SEC_MW_ENABLE_XSS", "true").lower() == "true"
        )
        self.enable_content_type_sniffing = (
            enable_content_type_sniffing
            if enable_content_type_sniffing is not None
            else os.getenv("SEC_MW_ENABLE_SNIFFING", "false").lower() == "true"
        )
        self.max_request_size = (
            max_request_size
            if max_request_size is not None
            else int(os.getenv("SEC_MW_MAX_REQUEST_SIZE", str(10 * 1024 * 1024)))
        )
        self.enable_hsts = (
            enable_hsts
            if enable_hsts is not None
            else os.getenv("SEC_MW_ENABLE_HSTS", "true").lower() == "true"
        )
        self.enable_rate_limit_headers = (
            enable_rate_limit_headers
            if enable_rate_limit_headers is not None
            else os.getenv("SIMPLE_RATE_LIMIT_HEADERS", "false").lower() == "true"
        )
        self.content_security_policy = content_security_policy or (
            os.getenv(
                "SEC_MW_CSP",
                "default-src 'self'; "
                "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
                "style-src 'self' 'unsafe-inline'; "
                "img-src 'self' data: https:; "
                "connect-src 'self' ws: wss:;",
            )
        )
    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        """Process request through security pipeline."""
        await self._validate_request(request)
        self._set_request_tracing(request)
        response = await call_next(request)
        self._apply_security_headers(response)
        self._apply_response_headers(request, response)
        return response
    async def _validate_request(self, request: Request) -> None:
        """Validate incoming request and log security context."""
        content_length = request.headers.get("content-length")
        if content_length:
            try:
                length = int(content_length)
                if length > self.max_request_size:
                    raise HTTPException(status_code=413, detail="Request too large")
            except ValueError:
                pass
        user_agent = request.headers.get("user-agent", "unknown")
        client_ip = getattr(getattr(request, "client", None), "host", "unknown")
        try:
            logger.debug(
                "Security validation",
                extra={
                    "client_ip": client_ip,
                    "user_agent": user_agent,
                    "method": request.method,
                    "path": request.url.path,
                },
            )
        except Exception:
            pass
    def _set_request_tracing(self, request: Request) -> None:
        """Set up request tracing identifiers."""
        request_id = request.headers.get("x-request-id") or str(uuid.uuid4())
        request.state.request_id = request_id
        correlation_id = request.headers.get("x-correlation-id")
        if correlation_id:
            request.state.correlation_id = correlation_id
        traceparent = request.headers.get("traceparent")
        if traceparent:
            request.state.traceparent = traceparent
    def _apply_security_headers(self, response: Response) -> None:
        """Apply comprehensive security headers on response."""
        if self.enable_csrf:
            response.headers["X-Frame-Options"] = "DENY"
            response.headers["X-Content-Type-Options"] = "nosniff"
        if self.enable_xss_protection:
            response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Content-Security-Policy"] = self.content_security_policy
        if self.enable_hsts:
            response.headers["Strict-Transport-Security"] = (
                "max-age=31536000; includeSubDomains"
            )
        if not self.enable_content_type_sniffing:
            response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
    def _apply_response_headers(self, request: Request, response: Response) -> None:
        """Apply response tracing and operational headers."""
        if hasattr(request.state, "request_id"):
            response.headers["X-Request-ID"] = request.state.request_id  # type: ignore[index]
        if hasattr(request.state, "correlation_id"):
            response.headers["X-Correlation-ID"] = request.state.correlation_id  # type: ignore[index]
        if hasattr(request.state, "traceparent"):
            response.headers["traceparent"] = request.state.traceparent  # type: ignore[index]
        if self.enable_rate_limit_headers:
            response.headers["X-RateLimit-Limit"] = "1000"
            response.headers["X-RateLimit-Remaining"] = "999"
            response.headers["X-RateLimit-Reset"] = str(int(time.time()) + 3600)
        if hasattr(request.state, "start_time"):
            processing_time = time.time() - float(request.state.start_time)  # type: ignore[arg-type]
            response.headers["X-Process-Time"] = f"{processing_time:.6f}"
def setup_security_middleware(app: FastAPI, **kwargs: Any) -> None:
    """Setup consolidated security middleware for the application.
    Args:
        app: FastAPI application instance.
        **kwargs: Additional configuration options for security middleware.
    """
    @app.middleware("http")
    async def add_process_time_header(
        request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        start_time = time.time()
        request.state.start_time = start_time
        return await call_next(request)
    app.add_middleware(ConsolidatedSecurityMiddleware, **kwargs)
    try:
        logger.info("Consolidated security middleware enabled")
    except Exception:
        pass
def attach_headers_middleware(app: FastAPI) -> None:
    """Legacy compatibility function for headers middleware."""
    setup_security_middleware(app, enable_rate_limit_headers=True)
def attach_security_middleware(app: FastAPI) -> None:
    """Legacy compatibility function for security middleware."""
    setup_security_middleware(app)
__all__ = [
    "ConsolidatedSecurityMiddleware",
    "attach_headers_middleware",
    "attach_security_middleware",
    "setup_security_middleware",
]
