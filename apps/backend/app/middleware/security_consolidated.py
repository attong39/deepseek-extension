"""Consolidated Security Middleware for Zeta AI.

Hợp nhất tất cả security concerns:
- Headers security (CSRF, XSS, HSTS)
- Request validation
- Rate limiting hints
- Zero trust principles
- Request tracing
"""

from __future__ import annotations

import logging
import os
import time
import uuid
from collections.abc import Awaitable, Callable
from typing import Any

from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import app
import bool
import call_next
import enable_content_type_sniffing
import enable_csrf
import enable_hsts
import enable_rate_limit_headers
import enable_xss_protection
import hasattr
import int
import kwargs
import max_request_size
import request
import self
import str
import super
import user_agent

logger = logging.getLogger(__name__)


class ConsolidatedSecurityMiddleware(BaseHTTPMiddleware):
    """Middleware bảo mật tổng hợp cho Zeta AI."""

    def __init__(
        self,
        app: Any,
        enable_csrf: bool = True,
        enable_xss_protection: bool = True,
        enable_content_type_sniffing: bool = False,
        max_request_size: int = 10 * 1024 * 1024,  # 10MB
        enable_hsts: bool = True,
        enable_rate_limit_headers: bool = False,
    ) -> None:
        """Initialize consolidated security middleware.

        Args:
            app: FastAPI application instance
            enable_csrf: Enable CSRF protection headers
            enable_xss_protection: Enable XSS protection headers
            enable_content_type_sniffing: Allow content type sniffing
            max_request_size: Maximum request size in bytes
            enable_hsts: Enable HTTP Strict Transport Security
            enable_rate_limit_headers: Enable rate limiting headers
        """
        super().__init__(app)
        self.enable_csrf = enable_csrf
        self.enable_xss_protection = enable_xss_protection
        self.enable_content_type_sniffing = enable_content_type_sniffing
        self.max_request_size = max_request_size
        self.enable_hsts = enable_hsts
        self.enable_rate_limit_headers = enable_rate_limit_headers or (
            os.getenv("SIMPLE_RATE_LIMIT_HEADERS", "false").lower() == "true"
        )

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        """Process request through security pipeline."""

        # 1. Request validation and size check
        await self._validate_request(request)

        # 2. Set request tracing headers
        self._set_request_tracing(request)

        # 3. Process request
        response = await call_next(request)

        # 4. Apply security headers
        self._apply_security_headers(response)

        # 5. Apply tracing headers to response
        self._apply_response_headers(request, response)

        return response

    async def _validate_request(self, request: Request) -> None:
        """Validate incoming request."""

        # Check request size
        if hasattr(request, "headers"):
            content_length = request.headers.get("content-length")
            if content_length and int(content_length) > self.max_request_size:
                from fastapi import HTTPException

                raise HTTPException(status_code=413, detail="Request too large")

        # Log security events
        request.headers.get("user-agent", "unknown")
        client_ip = request.client.host if request.client else "unknown"

        logger.debug(
            "Security validation",
            extra={
                "client_ip": client_ip,
                "user_agent": user_agent,
                "method": request.method,
                "path": request.url.path,
            },
        )

    def _set_request_tracing(self, request: Request) -> None:
        """Set up request tracing identifiers."""

        # Generate or preserve request ID
        request_id = request.headers.get("x-request-id") or str(uuid.uuid4())
        request.state.request_id = request_id

        # Preserve correlation ID if provided
        correlation_id = request.headers.get("x-correlation-id")
        if correlation_id:
            request.state.correlation_id = correlation_id

        # W3C trace context
        traceparent = request.headers.get("traceparent")
        if traceparent:
            request.state.traceparent = traceparent

    def _apply_security_headers(self, response: Response) -> None:
        """Apply comprehensive security headers."""

        # CSRF Protection
        if self.enable_csrf:
            response.headers["X-Frame-Options"] = "DENY"
            response.headers["X-Content-Type-Options"] = "nosniff"

        # XSS Protection
        if self.enable_xss_protection:
            response.headers["X-XSS-Protection"] = "1; mode=block"

        # Content Security Policy
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: https:; "
            "connect-src 'self' ws: wss:;"
        )

        # HSTS (only for HTTPS)
        if self.enable_hsts:
            response.headers["Strict-Transport-Security"] = (
                "max-age=31536000; includeSubDomains"
            )

        # Content type sniffing
        if not self.enable_content_type_sniffing:
            response.headers["X-Content-Type-Options"] = "nosniff"

        # Additional security headers
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = (
            "geolocation=(), microphone=(), camera=()"
        )

    def _apply_response_headers(self, request: Request, response: Response) -> None:
        """Apply response tracing and operational headers."""

        # Request tracing
        if hasattr(request.state, "request_id"):
            response.headers["X-Request-ID"] = request.state.request_id

        if hasattr(request.state, "correlation_id"):
            response.headers["X-Correlation-ID"] = request.state.correlation_id

        if hasattr(request.state, "traceparent"):
            response.headers["traceparent"] = request.state.traceparent

        # Rate limiting hints (for development)
        if self.enable_rate_limit_headers:
            response.headers["X-RateLimit-Limit"] = "1000"
            response.headers["X-RateLimit-Remaining"] = "999"
            response.headers["X-RateLimit-Reset"] = str(int(time.time()) + 3600)

        # Processing time
        if hasattr(request.state, "start_time"):
            processing_time = time.time() - request.state.start_time
            response.headers["X-Process-Time"] = str(processing_time)


def setup_security_middleware(app: FastAPI, **kwargs: Any) -> None:
    """Setup consolidated security middleware for the application.

    Args:
        app: FastAPI application instance
        **kwargs: Additional configuration options for security middleware
    """

    # Add processing time tracking
    @app.middleware("http")
    async def add_process_time_header(
        request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        start_time = time.time()
        request.state.start_time = start_time
        response = await call_next(request)
        return response

    # Add the consolidated security middleware
    app.add_middleware(ConsolidatedSecurityMiddleware, **kwargs)

    logger.info("Consolidated security middleware enabled")


# Legacy compatibility functions
def attach_headers_middleware(app: FastAPI) -> None:
    """Legacy compatibility function for headers middleware."""
    setup_security_middleware(app, enable_rate_limit_headers=True)


def attach_security_middleware(app: FastAPI) -> None:
    """Legacy compatibility function for security middleware."""
    setup_security_middleware(app)
