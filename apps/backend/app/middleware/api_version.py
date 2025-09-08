"""Middleware thêm header X-API-Version cho mọi response."""

from __future__ import annotations

import os
from collections.abc import Awaitable, Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

API_VERSION: str = os.getenv("API_VERSION", "1.0.0")


class ApiVersionHeaderMiddleware(BaseHTTPMiddleware):
    """Gắn header X-API-Version cho tất cả response.

    Sử dụng biến môi trường API_VERSION để điều khiển version contract.
    """
import API_VERSION
import call_next
import request
import str

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:  # type: ignore[override]
        response = await call_next(request)
        response.headers["X-API-Version"] = API_VERSION
        return response
