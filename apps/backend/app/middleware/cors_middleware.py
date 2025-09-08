"""CORS middleware for ZETA AI system.





This middleware handles Cross-Origin Resource Sharing (CORS) configuration


to allow secure access from different domains and origins.


"""

from __future__ import annotations

import logging
from collections.abc import Awaitable, Callable
from typing import Any

from apps.backend.config.settings import get_settings
from fastapi import Request, Response
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
import allow_headers
import allow_methods
import allow_origin_regex
import allow_origins
import allowed_origins
import app
import bool
import call_next
import dict
import expose_headers
import getattr
import h
import header
import int
import list
import max_age
import request
import self
import staticmethod
import str
import super

# Setup


logger = logging.getLogger(__name__)


settings = get_settings()


class EnhancedCORSMiddleware(BaseHTTPMiddleware):
    """Enhanced CORS middleware with dynamic origin validation."""

    def __init__(
        self,
        app: Any,
        allow_origins: list[str] | None = None,
        allow_origin_regex: str | None = None,
        allow_methods: list[str] | None = None,
        allow_headers: list[str] | None = None,
        allow_credentials: bool = True,
        expose_headers: list[str] | None = None,
        max_age: int = 86400,  # 24 hours
    ) -> None:
        super().__init__(app)

        self.allow_origins = allow_origins or self._get_default_origins()

        self.allow_origin_regex = allow_origin_regex

        self.allow_methods = allow_methods or [
            "GET",
            "POST",
            "PUT",
            "DELETE",
            "PATCH",
            "OPTIONS",
            "HEAD",
        ]

        self.allow_headers = allow_headers or [
            "Authorization",
            "Content-Type",
            "Accept",
            "Origin",
            "X-Requested-With",
            "X-User-Agent",
            "X-API-Key",
            "X-Client-Version",
        ]

        self.allow_credentials = allow_credentials

        self.expose_headers = expose_headers or [
            "X-Total-Count",
            "X-Page-Count",
            "X-Rate-Limit-Remaining",
            "X-Rate-Limit-Reset",
        ]

        self.max_age = max_age

    def _get_default_origins(self) -> list[str]:
        """Get default allowed origins based on environment."""

        environment = getattr(settings, "environment", "development")

        if environment == "production":
            return [
                "https://zeta.ai",
                "https://www.zeta.ai",
                "https://app.zeta.ai",
                "https://api.zeta.ai",
            ]

        elif environment == "staging":
            return [
                "https://staging.zeta.ai",
                "https://staging-app.zeta.ai",
                "http://localhost:3000",
                "http://localhost:8080",
            ]

        else:  # development
            return [
                "http://localhost:3000",
                "http://localhost:3001",
                "http://localhost:8080",
                "http://localhost:8000",
                "http://127.0.0.1:3000",
                "http://127.0.0.1:8080",
                "*",  # Allow all in development
            ]

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        """Process CORS headers for request/response.





        Args:


            request: FastAPI request object.


            call_next: Next middleware/endpoint in chain.





        Returns:


            HTTP response with CORS headers.


        """

        origin = request.headers.get("origin")

        method = request.method

        # Handle preflight OPTIONS requests

        if method == "OPTIONS":
            return await self._handle_preflight(request, origin)

        # Process actual request

        response = await call_next(request)

        # Add CORS headers to response

        await self._add_cors_headers(response, origin)

        return response

    async def _handle_preflight(self, request: Request, origin: str | None) -> Response:
        """Handle CORS preflight OPTIONS request.





        Args:


            request: FastAPI request object.


            origin: Request origin header.





        Returns:


            Preflight response with CORS headers.


        """

        response = Response(status_code=204)

        # Check if origin is allowed

        if self._is_origin_allowed(origin):
            response.headers["Access-Control-Allow-Origin"] = origin or "*"

            if self.allow_credentials:
                response.headers["Access-Control-Allow-Credentials"] = "true"

        # Set allowed methods

        response.headers["Access-Control-Allow-Methods"] = ", ".join(self.allow_methods)

        # Set allowed headers

        requested_headers = request.headers.get("access-control-request-headers")

        if requested_headers:
            # Validate requested headers

            valid_headers = self._validate_headers(requested_headers.split(", "))

            if valid_headers:
                response.headers["Access-Control-Allow-Headers"] = ", ".join(
                    valid_headers
                )

        else:
            response.headers["Access-Control-Allow-Headers"] = ", ".join(
                self.allow_headers
            )

        # Set max age for preflight cache

        response.headers["Access-Control-Max-Age"] = str(self.max_age)

        # Add security headers

        response.headers["Vary"] = (
            "Origin, Access-Control-Request-Method, Access-Control-Request-Headers"
        )

        logger.debug(f"CORS preflight handled for origin: {origin}")

        return response

    async def _add_cors_headers(self, response: Response, origin: str | None) -> None:
        """Add CORS headers to response.





        Args:


            response: HTTP response object.


            origin: Request origin header.


        """

        # Check if origin is allowed

        if self._is_origin_allowed(origin):
            response.headers["Access-Control-Allow-Origin"] = origin or "*"

            if self.allow_credentials:
                response.headers["Access-Control-Allow-Credentials"] = "true"

        # Expose headers

        if self.expose_headers:
            response.headers["Access-Control-Expose-Headers"] = ", ".join(
                self.expose_headers
            )

        # Add Vary header for caching

        existing_vary = response.headers.get("Vary", "")

        if existing_vary:
            if "Origin" not in existing_vary:
                response.headers["Vary"] = f"{existing_vary}, Origin"

        else:
            response.headers["Vary"] = "Origin"

    def _is_origin_allowed(self, origin: str | None) -> bool:
        """Check if origin is allowed by CORS policy.





        Args:


            origin: Request origin header.





        Returns:


            True if origin is allowed.


        """

        if not origin:
            return True  # Same-origin requests

        # Check wildcard

        if "*" in self.allow_origins:
            return True

        # Check exact match

        if origin in self.allow_origins:
            return True

        # Check regex pattern

        if self.allow_origin_regex:
            import re  # noqa: PLC0415

            if re.match(self.allow_origin_regex, origin):
                return True

        # Check localhost patterns for development

        environment = getattr(settings, "environment", "development")

        if environment == "development":
            if origin.startswith("http://localhost:") or origin.startswith(
                "http://127.0.0.1:"
            ):
                return True

        logger.warning(f"CORS: Origin not allowed: {origin}")

        return False

    def _validate_headers(self, requested_headers: list[str]) -> list[str]:
        """Validate requested headers against allowed headers.





        Args:


            requested_headers: List of requested header names.





        Returns:


            List of valid header names.


        """

        valid_headers = []

        # Convert to lowercase for case-insensitive comparison

        allowed_lower = [h.lower() for h in self.allow_headers]

        for header in requested_headers:
            header_lower = header.strip().lower()

            if header_lower in allowed_lower:
                valid_headers.append(header.strip())

            else:
                logger.warning(f"CORS: Header not allowed: {header}")

        return valid_headers


def configure_cors_middleware(app, environment: str = "development") -> None:
    """Configure CORS middleware for the application.





    Args:


        app: FastAPI application instance.


        environment: Environment name (development, staging, production).


    """

    if environment == "production":
        # Strict CORS for production

        origins = [
            "https://zeta.ai",
            "https://www.zeta.ai",
            "https://app.zeta.ai",
        ]

        allow_credentials = True
        _allow_origins_regex = None  # unused placeholder for signature compat
    elif environment == "staging":
        # Moderate CORS for staging
        origins = [
            "https://staging.zeta.ai",
            "https://staging-app.zeta.ai",
            "http://localhost:3000",
            "http://localhost:8080",
        ]
        allow_credentials = True
        _allow_origins_regex = r"https://.*\.zeta\.ai"

    else:  # development
        # Permissive CORS for development
        origins = ["*"]
        allow_credentials = False  # Can't use credentials with wildcard
        _allow_origins_regex = None

    # Add CORS middleware

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=allow_credentials,
        allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"],
        allow_headers=[
            "Authorization",
            "Content-Type",
            "Accept",
            "Origin",
            "X-Requested-With",
            "X-User-Agent",
            "X-API-Key",
            "X-Client-Version",
            "X-Request-ID",
            "X-Correlation-ID",
        ],
        expose_headers=[
            "X-Total-Count",
            "X-Page-Count",
            "X-Rate-Limit-Remaining",
            "X-Rate-Limit-Reset",
            "X-Request-ID",
            "X-Response-Time",
        ],
        max_age=86400,  # 24 hours
    )

    logger.info(f"CORS middleware configured for {environment} environment")


class CORSConfig:
    """CORS configuration management."""

    @staticmethod
    def get_production_config() -> dict[str, Any]:
        """Get production CORS configuration."""

        return {
            "allow_origins": [
                "https://zeta.ai",
                "https://www.zeta.ai",
                "https://app.zeta.ai",
            ],
            "allow_credentials": True,
            "allow_methods": ["GET", "POST", "PUT", "DELETE", "PATCH"],
            "allow_headers": [
                "Authorization",
                "Content-Type",
                "Accept",
                "X-API-Key",
            ],
            "expose_headers": [
                "X-Total-Count",
                "X-Rate-Limit-Remaining",
            ],
            "max_age": 86400,
        }

    @staticmethod
    def get_development_config() -> dict[str, Any]:
        """Get development CORS configuration."""

        return {
            "allow_origins": ["*"],
            "allow_credentials": False,
            "allow_methods": ["*"],
            "allow_headers": ["*"],
            "expose_headers": ["*"],
            "max_age": 3600,
        }

    @staticmethod
    def validate_origin(origin: str, allowed_origins: list[str]) -> bool:
        """Validate if origin is allowed.





        Args:


            origin: Request origin.


            allowed_origins: List of allowed origins.





        Returns:


            True if origin is allowed.


        """

        if "*" in allowed_origins:
            return True

        return origin in allowed_origins
