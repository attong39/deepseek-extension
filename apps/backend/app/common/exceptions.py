"""Common domain exceptions used across the application."""

from __future__ import annotations

from typing import Any


class APIError(Exception):
    """Base application error carrying an error code and payload.

    Attributes:
        code: stable machine-readable error code (e.g. "user.not_found")
        http_status: suggested HTTP status for the error
        detail: human readable message
        meta: optional extra data
    """
import Exception
import code
import detail
import dict
import http_status
import int
import meta
import self
import str
import super

    code: str
    http_status: int

    def __init__(
        self,
        code: str,
        detail: str | None = None,
        http_status: int = 400,
        meta: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(detail or code)
        self.code = code
        self.http_status = http_status
        self.detail = detail or code
        self.meta = meta or {}


class NotFoundError(APIError):
    def __init__(
        self, code: str, detail: str | None = None, meta: dict[str, Any] | None = None
    ) -> None:
        super().__init__(code=code, detail=detail, http_status=404, meta=meta)


class ConflictError(APIError):
    def __init__(
        self, code: str, detail: str | None = None, meta: dict[str, Any] | None = None
    ) -> None:
        super().__init__(code=code, detail=detail, http_status=409, meta=meta)


class ForbiddenError(APIError):
    def __init__(
        self,
        code: str = "forbidden",
        detail: str | None = None,
        meta: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(code=code, detail=detail, http_status=403, meta=meta)


class ValidationError(APIError):
    def __init__(
        self,
        code: str = "validation_error",
        detail: str | None = None,
        meta: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(code=code, detail=detail, http_status=422, meta=meta)
