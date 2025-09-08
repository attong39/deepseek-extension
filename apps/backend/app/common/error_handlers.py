"""FastAPI exception handlers to normalize API error responses.

This module is self-contained and avoids hard dependencies on sibling packages
by using duck typing when mapping core-layer exceptions.
"""

from __future__ import annotations

import logging
from typing import Any

from fastapi import Request
from fastapi.responses import JSONResponse

from .exceptions import APIError
import Exception
import dict
import exc
import getattr
import isinstance
import public_code
import request
import status
import str
import type

logger = logging.getLogger(__name__)


def api_error_handler(request: Request, exc: APIError) -> JSONResponse:
    """Convert APIError into a stable JSON body with code + detail + meta.

    Response shape:
    {
      "error": {
        "code": "user.not_found",
        "message": "User not found",
        "meta": { ... }
      }
    }
    """

    body: dict[str, Any] = {
        "error": {
            "code": exc.code,
            "message": exc.detail,
            "meta": exc.meta or {},
        }
    }

    logger.info("APIError handled: %s %s", exc.code, request.url.path)

    return JSONResponse(status_code=exc.http_status, content=body)


def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Fallback handler for unhandled exceptions; do not leak internals."""

    # Log with explicit exc_info to include traceback from provided exception
    logger.error(
        "Unhandled exception while handling request %s: %r",
        request.url.path,
        exc,
        exc_info=(type(exc), exc, getattr(exc, "__traceback__", None)),
    )

    body = {
        "error": {
            "code": "internal_error",
            "message": "Internal server error",
            "meta": {},
        }
    }

    return JSONResponse(status_code=500, content=body)


def core_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Map CoreException (core layer) into stable API error response.

    The mapping is conservative: we derive HTTP status primarily from the
    CoreException.code when it matches known codes; otherwise default 500.

    Known code mappings:
    - NOT_FOUND -> 404 (code: "not_found")
    - VALIDATION_ERROR -> 422 (code: "validation_error")
    - PERMISSION_DENIED -> 403 (code: "forbidden")
    - otherwise -> 500 (code: "internal_error")
    """

    code_map = {
        "NOT_FOUND": (404, "not_found"),
        "VALIDATION_ERROR": (422, "validation_error"),
        "PERMISSION_DENIED": (403, "forbidden"),
    }

    # Derive attributes via duck typing to avoid import coupling
    raw_code = getattr(exc, "code", None)
    code_key = raw_code if isinstance(raw_code, str) else ""
    status, public_code = code_map.get(code_key, (500, "internal_error"))
    message = str(exc)
    meta: dict[str, Any] = {}
    try:
        # core exceptions typically expose a details dict
        details = getattr(exc, "details", {})
        meta = details if isinstance(details, dict) else {}
    except Exception:  # pragma: no cover — defensive
        meta = {}

    body: dict[str, Any] = {
        "error": {
            "code": public_code,
            "message": message,
            "meta": meta,
        }
    }

    logger.info(
        "Core-like exception handled: %s %s",
        code_key or "UNKNOWN",
        request.url.path,
    )
    return JSONResponse(status_code=status, content=body)
