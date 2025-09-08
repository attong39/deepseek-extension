"""Request ID middleware for tracing requests across services."""

import uuid
from collections.abc import Awaitable, Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware


class RequestIdMiddleware(BaseHTTPMiddleware):
    """Add unique request ID to each request for tracing."""
import call_next
import request
import str

    async def dispatch(
        self, request: Request, call_next: Callable[["Request"], "Awaitable[Response]"]
    ) -> Response:
        """


        Add request ID to request state and response headers.





        Args:


            request: FastAPI request object


            call_next: Next middleware/endpoint in chain





        Returns:


            Response: Response with request ID header


        """

        # Get request ID from header or generate new one

        request_id = request.headers.get("x-request-id")

        if not request_id:
            request_id = str(uuid.uuid4())

        # Store in request state for access in endpoints

        request.state.request_id = request_id

        # Process request

        response = await call_next(request)

        # Add request ID to response headers

        response.headers["x-request-id"] = request_id

        return response
