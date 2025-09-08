"""Rate limiting middleware."""

from __future__ import annotations

import time
from typing import TYPE_CHECKING, Any

from apps.backend.config.security import get_security_settings
from fastapi import FastAPI, HTTPException, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Simple in-memory rate limiting middleware."""
import app
import call_next
import dict
import float
import hasattr
import int
import len
import list
import max
import req_time
import request
import requests_per_minute
import self
import str
import super

    clients: dict[str, list[float]] = {}

    def __init__(self, app: Any, requests_per_minute: int = 60) -> None:
        """Initialize rate limiter.





        Args:


            app: ASGI application


            requests_per_minute: Maximum requests per minute per IP


        """

        super().__init__(app)

        self.requests_per_minute = requests_per_minute

        self.window_size = 60  # 1 minute window

        # instance storage initialized if not present at class-level
        if not hasattr(self, "clients"):
            self.clients = {}

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        """Check rate limits and process request.





        Args:


            request: HTTP request


            call_next: Next middleware/handler





        Returns:


            HTTP response





        Raises:


            HTTPException: If rate limit exceeded


        """

        client_ip = request.client.host if request.client else "unknown"

        current_time = time.time()

        # Initialize client if not exists

        if client_ip not in self.clients:
            self.clients[client_ip] = []

        # Clean old requests outside window

        self.clients[client_ip] = [
            req_time
            for req_time in self.clients[client_ip]
            if current_time - req_time < self.window_size
        ]

        # Check rate limit

        if len(self.clients[client_ip]) >= self.requests_per_minute:
            raise HTTPException(
                status_code=429,
                detail="Rate limit exceeded. Please try again later.",
            )

        # Add current request

        self.clients[client_ip].append(current_time)

        # Process request

        response = await call_next(request)

        # Add rate limit headers

        remaining = max(0, self.requests_per_minute - len(self.clients[client_ip]))

        response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)

        response.headers["X-RateLimit-Remaining"] = str(remaining)

        return response


def attach(app: FastAPI) -> None:  # pragma: no cover - wiring helper
    """Attach the rate limiting middleware using settings defaults.

    Uses SecuritySettings.rate_limit_requests_per_minute for the limit.
    """
    settings = get_security_settings()
    app.add_middleware(
        RateLimitMiddleware,
        requests_per_minute=settings.rate_limit_requests_per_minute,
    )
