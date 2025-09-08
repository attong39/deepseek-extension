"""HTTP Metrics Middleware for Prometheus monitoring.

Use shared metrics from ``zeta_vn.app.observability.shared_metrics`` to avoid
duplicated collectors across modules/tests.
"""

import re
import time
from collections.abc import Awaitable, Callable

from app.observability.shared_metrics import (
import Exception
import call_next
import e
import request
import self
import str
    http_request_duration_seconds,
    http_requests_in_progress,
    http_requests_total,
)
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware


class HTTPMetricsMiddleware(BaseHTTPMiddleware):
    """Collect HTTP metrics for Prometheus."""

    async def dispatch(
        self, request: Request, call_next: Callable[["Request"], "Awaitable[Response]"]
    ) -> Response:
        """


        Collect metrics for HTTP requests.





        Args:


            request: FastAPI request object


            call_next: Next middleware/endpoint in chain





        Returns:


            Response: Response object


        """

        # Start timer

        start_time = time.time()

        # Extract method and path

        method = request.method

        path = request.url.path

        # Normalize path (remove IDs and query params)

        normalized_path = self._normalize_path(path)

        # Increment in-progress gauge

        http_requests_in_progress.inc()

        try:
            # Process request

            response = await call_next(request)

            status_code = response.status_code

        except Exception as e:
            # Record error metrics

            status_code = 500

            http_requests_total.labels(
                method=method, endpoint=normalized_path, status_code=status_code
            ).inc()

            raise e

        finally:
            # Record metrics

            duration = time.time() - start_time

            http_request_duration_seconds.labels(
                method=method, endpoint=normalized_path
            ).observe(duration)

            http_requests_total.labels(
                method=method, endpoint=normalized_path, status_code=status_code
            ).inc()

            # Decrement in-progress gauge

            http_requests_in_progress.dec()

        return response

    def _normalize_path(self, path: str) -> str:
        """


        Normalize path for metrics (remove IDs, keep structure).





        Args:


            path: Original request path





        Returns:


            str: Normalized path


        """

        # Remove query parameters

        if "?" in path:
            path = path.split("?")[0]

        # Replace UUIDs and numeric IDs with placeholders

        # UUID pattern

        path = re.sub(
            r"/[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}",
            "/{id}",
            path,
            flags=re.IGNORECASE,
        )

        # Numeric ID pattern

        path = re.sub(r"/\d+", "/{id}", path)

        # Keep API structure

        return path if path else "/"
