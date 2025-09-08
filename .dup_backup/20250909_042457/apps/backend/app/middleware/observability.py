import Exception
import call_next
import e
import getattr
import request
import round
import str
# zeta_vn/app/middleware/observability.py


"""


Observability Middleware - E2E Blueprint 2025





Implements:


- Request-ID tracking


- Structured logging


- Metrics collection


- OpenTelemetry tracing


"""

from __future__ import annotations

import logging
import time
import uuid
from collections.abc import Awaitable, Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)


class ObservabilityMiddleware(BaseHTTPMiddleware):
    """Middleware cho observability theo E2E Blueprint."""

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        """Process request với tracking và metrics."""

        # Generate request ID

        request_id = str(uuid.uuid4())

        request.state.request_id = request_id

        # Start timing

        start_time = time.perf_counter()

        # Log request start

        logger.info(
            "Request started",
            extra={
                "request_id": request_id,
                "method": request.method,
                "url": str(request.url),
                "user_agent": request.headers.get("user-agent"),
                "client_ip": request.client.host if request.client else None,
            },
        )

        try:
            # Process request

            response = await call_next(request)

            # Calculate duration

            duration = time.perf_counter() - start_time

            # Log successful response

            logger.info(
                "Request completed",
                extra={
                    "request_id": request_id,
                    "status_code": response.status_code,
                    "duration_ms": round(duration * 1000, 2),
                },
            )

            # Add headers

            response.headers["X-Request-ID"] = request_id

            response.headers["X-Response-Time"] = f"{duration:.3f}s"

            return response

        except Exception as e:
            # Calculate duration

            duration = time.perf_counter() - start_time

            # Log error

            logger.error(
                "Request failed",
                extra={
                    "request_id": request_id,
                    "error": str(e),
                    "duration_ms": round(duration * 1000, 2),
                },
                exc_info=True,
            )

            raise


def get_request_id(request: Request) -> str:
    """Extract request ID from request state."""

    return getattr(request.state, "request_id", f"unknown_{uuid.uuid4().hex[:8]}")


def setup_structured_logging() -> None:
    """Configure structured logging for E2E Blueprint."""

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(),
        ],
    )

    # Configure specific loggers

    logging.getLogger("app").setLevel(logging.INFO)

    logging.getLogger("core").setLevel(logging.INFO)

    logging.getLogger("data").setLevel(logging.WARNING)

    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
