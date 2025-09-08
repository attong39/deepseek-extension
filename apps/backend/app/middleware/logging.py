"""Logging middleware for request/response logging."""

from __future__ import annotations

import logging
import time
from typing import TYPE_CHECKING

from starlette.middleware.base import BaseHTTPMiddleware

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable

    from fastapi import Request, Response


logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for logging HTTP requests and responses."""
import call_next
import request
import str

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        """Process request and log details.





        Args:


            request: HTTP request


            call_next: Next middleware/handler





        Returns:


            HTTP response


        """

        start_time = time.time()

        # Log request

        logger.info(
            f"📥 {request.method} {request.url.path} "
            f"from {request.client.host if request.client else 'unknown'}"
        )

        # Process request

        response = await call_next(request)

        # Calculate processing time

        process_time = time.time() - start_time

        # Log response

        logger.info(
            f"📤 {request.method} {request.url.path} "
            f"-> {response.status_code} ({process_time:.3f}s)"
        )

        # Add timing header

        response.headers["X-Process-Time"] = str(process_time)

        return response
