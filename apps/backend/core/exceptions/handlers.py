"""
Centralized Exception Handler for FastAPI.

Provides a global handler for authentication/authorization errors emitted from
the core exceptions package. Designed to be framework-light and pluggable.
"""

from __future__ import annotations

import logging
from datetime import UTC, datetime
from typing import Any

from apps.backend.core.exceptions.auth_exceptions import BaseAuthError
from apps.backend.core.exceptions.business_exceptions import BaseBusinessError
from apps.backend.core.exceptions.repository_exceptions import BaseRepositoryError
from apps.backend.core.exceptions.telemetry import ExceptionTelemetry
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import Exception
import app
import exc
import getattr
import handler
import isinstance
import request
import self
import user_agent

try:
    import structlog

    _struct_logger: Any | None = structlog.get_logger()
except Exception:  # pragma: no cover - optional dependency
    _struct_logger = None


class ExceptionHandler:
    """Global exception handler for ZETA AI Server.

    This class exposes coroutine handlers that can be registered with FastAPI's
    exception system via ``app.add_exception_handler``.
    """

    def __init__(self) -> None:
        self._logger = logging.getLogger(__name__)
        self._slogger = _struct_logger
        self._telemetry = ExceptionTelemetry()

    async def handle_auth_exception(
        self, request: Request, exc: Exception
    ) -> JSONResponse:  # noqa: D401
        """Handle authentication/authorization errors.

        Logs a structured security event (if structlog is available) and
        returns a normalized JSON error response with an appropriate status.
        """

        assert isinstance(exc, BaseAuthError)

        client_ip = getattr(getattr(request, "client", None), "host", None)
        request.headers.get("user-agent", "")
        request_id = request.headers.get("x-request-id")

        # Structured logging if available, otherwise fall back to std logging
        try:
            payload = {
                "event": "auth_exception",
                "error_code": exc.error_code,
                "user_id": getattr(exc, "user_id", None),
                "ip_address": client_ip,
                "user_agent": user_agent,
                "timestamp": getattr(exc, "timestamp", datetime.now(UTC)).isoformat(),
            }
            if self._slogger is not None:
                # structlog preferred API
                self._slogger.bind(request_id=request_id).warning(
                    "auth_exception", **payload
                )
            else:
                self._logger.warning(
                    "auth_exception", extra={"request_id": request_id, **payload}
                )
        except Exception:  # pragma: no cover - logging must not fail response path
            self._logger.exception("Failed to log auth exception")

        # Best-effort telemetry
        try:
            await self._telemetry.track_exception(
                exc, context=getattr(exc, "metadata", {})
            )
        except Exception:
            pass

        status_code = {
            "AUTH_001": 401,  # Authentication failed
            "AUTH_002": 403,  # Authorization failed
            "AUTH_003": 401,  # JWT token error
            "AUTH_004": 428,  # MFA required
            "AUTH_005": 401,  # Session expired
            "AUTH_006": 403,  # Permission denied
            "AUTH_007": 429,  # Rate limit exceeded
        }.get(exc.error_code, 401)

        return JSONResponse(
            status_code=status_code,
            content={
                "error": {
                    "type": "authentication_error",
                    "code": exc.error_code,
                    "message": exc.message,
                    "timestamp": getattr(
                        exc, "timestamp", datetime.now(UTC)
                    ).isoformat(),
                    "request_id": request_id,
                }
            },
        )

    async def handle_business_exception(
        self, request: Request, exc: Exception
    ) -> JSONResponse:
        """Handle business/domain exceptions with standardized response."""

        assert isinstance(exc, BaseBusinessError)

        # Best-effort telemetry
        try:
            await self._telemetry.track_exception(exc, context=exc.context)
        except Exception:
            pass

        request_id = request.headers.get("x-request-id")
        status_code = 400 if exc.severity.name in {"LOW", "MEDIUM"} else 422
        return JSONResponse(
            status_code=status_code,
            content={
                "error": {
                    "type": "business_error",
                    "code": exc.error_code,
                    "message": exc.message,
                    "timestamp": getattr(
                        exc, "timestamp", datetime.now(UTC)
                    ).isoformat(),
                    "request_id": request_id,
                    "context": exc.context,
                    "suggestions": exc.suggestions,
                    "severity": exc.severity.value,
                }
            },
        )

    async def handle_repository_exception(
        self, request: Request, exc: Exception
    ) -> JSONResponse:
        """Handle repository/data layer exceptions with standardized response."""

        assert isinstance(exc, BaseRepositoryError)

        # Best-effort telemetry
        try:
            await self._telemetry.track_exception(
                exc, context={"query": exc.query, "parameters": exc.parameters}
            )
        except Exception:
            pass

        request_id = request.headers.get("x-request-id")
        status_code = 503 if getattr(exc, "retryable", False) else 500
        return JSONResponse(
            status_code=status_code,
            content={
                "error": {
                    "type": "repository_error",
                    "code": exc.error_code,
                    "message": exc.message,
                    "timestamp": getattr(
                        exc, "timestamp", datetime.now(UTC)
                    ).isoformat(),
                    "request_id": request_id,
                    "context": {
                        "query": exc.query,
                        "parameters": exc.parameters,
                        "retryable": getattr(exc, "retryable", False),
                    },
                }
            },
        )


def register_exception_handlers(
    app: FastAPI, handler: ExceptionHandler | None = None
) -> None:
    """Register global exception handlers on the FastAPI app.

    Args:
        app: The FastAPI application instance.
        handler: Optional pre-built ExceptionHandler; if omitted, a new one is created.
    """

    h = handler or ExceptionHandler()
    app.add_exception_handler(BaseAuthError, h.handle_auth_exception)
    app.add_exception_handler(BaseBusinessError, h.handle_business_exception)
    app.add_exception_handler(BaseRepositoryError, h.handle_repository_exception)


__all__ = [
    "ExceptionHandler",
    "register_exception_handlers",
]
