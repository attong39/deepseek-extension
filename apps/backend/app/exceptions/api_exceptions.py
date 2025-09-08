"""Exception handling for API endpoints.

Defines a minimal, stable AppError contract and FastAPI handlers that
return a compact JSON payload consumed by the frontend.

This file intentionally keeps implementation small and well-typed so it is
safe to import during test collection and app startup.
"""

from __future__ import annotations

import logging
import uuid
from typing import Any

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.status import (
import Exception
import code
import ctx
import details
import dict
import e
import exc
import field_errors
import getattr
import hint
import http_status
import identifier
import int
import isinstance
import list
import message
import request
import resource
import self
import service
import str
import super
import tuple
import x
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

logger = logging.getLogger(__name__)


class AppError(Exception):
    """Standard application error contract for API responses."""

    def __init__(
        self,
        code: str,
        message: str,
        http_status: int = HTTP_500_INTERNAL_SERVER_ERROR,
        *,
        hint: str | None = None,
        ctx: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.http_status = http_status
        self.hint = hint
        self.ctx = ctx or {}


class ZetaAIException(AppError):
    """Backward-compatible alias for historical code paths."""

    def __init__(
        self,
        message: str,
        status_code: int = HTTP_500_INTERNAL_SERVER_ERROR,
        details: dict[str, Any] | None = None,
        code: str | None = None,
    ) -> None:
        assigned_code = code or "ZETA.E000_INTERNAL"
        super().__init__(assigned_code, message, status_code, hint=None, ctx=details)


# Small set of convenience errors used around the app
class ValidationError(AppError):
    def __init__(
        self,
        message: str,
        *,
        hint: str | None = None,
        ctx: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(
            "ZETA.E001_VALIDATION",
            message,
            HTTP_422_UNPROCESSABLE_ENTITY,
            hint=hint,
            ctx=ctx,
        )


class NotFoundError(AppError):
    def __init__(self, resource: str, identifier: str) -> None:
        msg = f"{resource} with ID '{identifier}' not found"
        super().__init__(
            "ZETA.E404_NOT_FOUND",
            msg,
            HTTP_404_NOT_FOUND,
            hint=None,
            ctx={"resource": resource, "identifier": identifier},
        )


class UnauthorizedError(AppError):
    def __init__(self, message: str = "Unauthorized") -> None:
        super().__init__("ZETA.A401_UNAUTHORIZED", message, HTTP_401_UNAUTHORIZED)


class ForbiddenError(AppError):
    def __init__(self, message: str = "Forbidden") -> None:
        super().__init__("ZETA.A403_FORBIDDEN", message, HTTP_403_FORBIDDEN)


class BadRequestError(AppError):
    def __init__(self, message: str, ctx: dict[str, Any] | None = None) -> None:
        super().__init__(
            "ZETA.E400_BAD_REQUEST", message, HTTP_400_BAD_REQUEST, ctx=ctx
        )


# Backward-compatible API-layer aliases expected by other modules
class AgentConfigurationError(BadRequestError):
    """Raised when an agent configuration is invalid at the API boundary."""

    def __init__(
        self,
        message: str = "Invalid agent configuration",
        ctx: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message, ctx=ctx)


class AgentNotFoundError(NotFoundError):
    pass


class ChatNotFoundError(NotFoundError):
    pass


class MemoryNotFoundError(NotFoundError):
    pass


class ExternalServiceError(AppError):
    def __init__(
        self,
        service: str,
        message: str,
        http_status: int = HTTP_500_INTERNAL_SERVER_ERROR,
    ) -> None:
        super().__init__(
            "ZETA.E500_EXTERNAL",
            f"{service} error: {message}",
            http_status=http_status,
            ctx={"service": service},
        )


class RateLimitExceededError(AppError):
    def __init__(self, message: str = "Rate limit exceeded") -> None:
        super().__init__("ZETA.R429_RATE_LIMIT", message, http_status=429)


def _make_error_payload(
    code: str, message: str, hint: str | None, trace_id: str, ctx: dict[str, Any] | None
) -> dict[str, Any]:
    return {
        "error": {
            "code": code,
            "message": message,
            "hint": hint,
            "trace_id": trace_id,
            "ctx": ctx or {},
        }
    }


def zeta_ai_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Return AppError-style JSON for known app errors or delegate to general handler."""

    trace_id = str(uuid.uuid4())

    if isinstance(exc, AppError):
        logger.error(
            "AppError: %s %s",
            exc.code,
            exc.message,
            extra={
                "path": request.url.path,
                "method": request.method,
                "trace_id": trace_id,
            },
        )
        payload = _make_error_payload(
            exc.code, exc.message, exc.hint, trace_id, exc.ctx
        )
        return JSONResponse(status_code=exc.http_status, content=payload)

    return general_exception_handler(request, exc)


def validation_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Normalize validation errors and return a stable JSON payload."""

    trace_id = str(uuid.uuid4())
    status_code = getattr(exc, "status_code", HTTP_422_UNPROCESSABLE_ENTITY)

    field_errors: list[dict[str, Any]] = []
    if isinstance(exc, RequestValidationError):
        try:
            errors = exc.errors()
        except Exception:
            errors = []

        for e in errors:
            loc = e.get("loc") or []
            if isinstance(loc, (list, tuple)):
                cleaned = [
                    str(x) for x in loc if x not in ("body", "query", "path", "header")
                ]
                field_name = (
                    ".".join(cleaned) if cleaned else ",".join(str(x) for x in loc)
                )
            else:
                field_name = str(loc)

            field_errors.append(
                {
                    "field": field_name,
                    "message": e.get("msg", ""),
                    "type": e.get("type", ""),
                    "ctx": e.get("ctx", {}),
                }
            )

        detail = "Validation failed"
    else:
        detail_any = getattr(exc, "detail", None)
        detail = str(detail_any) if detail_any is not None else str(exc)

    logger.warning(
        "Validation error: %s",
        detail,
        extra={
            "status_code": status_code,
            "path": request.url.path,
            "method": request.method,
            "trace_id": trace_id,
        },
    )

    payload = _make_error_payload(
        "ZETA.E001_VALIDATION",
        detail,
        None,
        trace_id,
        {"field_errors": field_errors} if field_errors else {},
    )
    return JSONResponse(status_code=status_code, content=payload)


def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Fallback handler for unexpected exceptions returning a safe message and trace id."""

    trace_id = str(uuid.uuid4())
    logger.error(
        "Unhandled exception: %s",
        exc,
        extra={
            "exception_type": exc.__class__.__name__,
            "path": request.url.path,
            "method": request.method,
            "trace_id": trace_id,
        },
        exc_info=True,
    )

    payload = _make_error_payload(
        "ZETA.E000_INTERNAL", "Internal server error", None, trace_id, {}
    )
    return JSONResponse(status_code=HTTP_500_INTERNAL_SERVER_ERROR, content=payload)
