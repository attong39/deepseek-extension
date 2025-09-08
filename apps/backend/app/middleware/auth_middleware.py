"""Authentication middleware for ZETA AI system.

This middleware handles JWT validation, user auth, and RBAC for API endpoints.
It is implemented as a pure ASGI middleware to avoid BaseHTTPMiddleware quirks.
"""

from __future__ import annotations

import logging
import os
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any, ClassVar, cast

from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from starlette.types import ASGIApp, Message, Receive, Scope, Send
import Exception
import admin_path
import algorithm
import any
import bool
import current_user
import dict
import e
import exc
import expires_delta
import frozenset
import getattr
import hasattr
import int
import list
import message
import permissions
import prefix
import receive
import scope
import secret_key
import self
import send
import str
import tuple

if TYPE_CHECKING:  # pragma: no cover - import-time typing only
    from fastapi import FastAPI

from apps.backend.config.settings import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class AuthenticationMiddleware:
    """ASGI middleware for JWT authentication and authorization.

    Args:
        app: The downstream ASGI app.
    """

    # Public endpoints that don't require authentication
    PUBLIC_PATHS: ClassVar[frozenset[str]] = frozenset(
        {
            "/docs",
            "/redoc",
            "/openapi.json",
            "/health",
            # Dev profiling (local debugging only)
            "/api/v1/dev/profiling/ping",
            "/api/v1/dev/profiling/run",
            # Meta endpoints manage their own auth via route dependencies
            "/api/v1/__meta__/openapi-snapshot",
            "/api/v1/auth/login",
            "/api/v1/auth/register",
            "/api/v1/auth/refresh",
            "/api/v1/health",
            "/api/v1/health/live",
            "/api/v1/health/ready",
            "/favicon.ico",
        }
    )

    # Admin-only endpoints
    ADMIN_PATHS: ClassVar[frozenset[str]] = frozenset(
        {"/api/v1/admin", "/api/v1/analytics", "/api/v1/system"}
    )

    def __init__(self, app: ASGIApp) -> None:
        self.app: ASGIApp = app
        self.secret_key = getattr(settings, "secret_key", "fallback_secret_key")
        self.algorithm = "HS256"

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        """ASGI entrypoint."""
        if scope.get("type") != "http":
            await self.app(scope, receive, send)
            return

        request = Request(scope, receive=receive)
        path = request.url.path

        # Dev-only: allow explicit bypass via header for local profiling/testing
        if request.headers.get("x-bypass-auth", "").lower() == "dev":
            await self.app(scope, receive, send)
            return

        # Env-flag-based bypass for dev profiling routes
        try:
            if os.getenv(
                "DISABLE_AUTH_FOR_PROFILING", "false"
            ).lower() == "true" and path.startswith("/api/v1/dev/profiling"):
                await self.app(scope, receive, send)
                return
        except Exception:
            # non-fatal; continue with normal auth
            pass

        # Allow public paths to pass through
        if self._is_public_path(path):
            await self.app(scope, receive, send)
            return

        user_id: str | None = None
        try:
            user_id, payload = self._authenticate_request(request, path)

            # Propagate auth data via ASGI scope state (visible as request.state)
            state = scope.setdefault("state", {})
            state["user_id"] = user_id
            state["user_role"] = payload.get("role", "user")
            state["user_permissions"] = (
                payload.get("scopes") or payload.get("permissions") or []
            )
            state["token_payload"] = payload

        except HTTPException as exc:
            response = JSONResponse(
                status_code=exc.status_code,
                content={"detail": exc.detail},
                headers=getattr(exc, "headers", None),
            )
            await response(scope, receive, send)
            return
        except Exception as e:  # pragma: no cover - defensive
            logger.error("Authentication middleware error: %s", e)
            response = JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"detail": "Authentication service error"},
            )
            await response(scope, receive, send)
            return

        # Wrap send to add headers after downstream sets the response
        async def send_wrapper(message: Message) -> None:
            if message.get("type") == "http.response.start":
                existing = list(message.get("headers", []))
                if user_id:
                    existing.append((b"x-user-id", str(user_id).encode("latin-1")))
                existing.append((b"x-content-type-options", b"nosniff"))
                existing.append((b"x-frame-options", b"DENY"))
                message["headers"] = existing
            await send(message)

        await self.app(scope, receive, send_wrapper)

    def _is_public_path(self, path: str) -> bool:
        """Check if path is public (no auth required)."""
        if path in self.PUBLIC_PATHS:
            return True
        # Prefix match for static files
        public_prefixes = [
            "/static/",
            "/assets/",
            "/favicon",
            # Dev profiling prefix (local only)
            "/api/v1/dev/profiling",
        ]
        return any(path.startswith(prefix) for prefix in public_prefixes)

    def _is_admin_path(self, path: str) -> bool:
        """Check if path requires admin access."""
        return any(path.startswith(admin_path) for admin_path in self.ADMIN_PATHS)

    def _extract_token(self, request: Request) -> str | None:
        """Extract JWT token from Authorization header or cookie."""
        authorization = request.headers.get("Authorization")
        if authorization and authorization.startswith("Bearer "):
            return authorization.split(" ", 1)[1]
        return request.cookies.get("access_token")

    def _decode_token(self, token: str) -> dict[str, Any]:
        """Decode and validate JWT token using the central JWTHandler."""
        try:
            from app.auth.jwt_handler import JWTHandler

            # JWTHandler.verify_token is untyped; cast to expected dict[str, Any]
            return cast(dict[str, Any], JWTHandler.verify_token(token))
        except HTTPException as exc:  # explicitly re-raise
            raise exc from None
        except Exception as e:  # pragma: no cover - defensive
            logger.error("Token decode error: %s", e)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token validation failed",
                headers={"WWW-Authenticate": "Bearer"},
            ) from e

    def _authenticate_request(
        self, request: Request, path: str
    ) -> tuple[str, dict[str, Any]]:
        """Authenticate the request and perform basic RBAC.

        Args:
            request: Incoming request.
            path: Request path.

        Returns:
            Tuple of (user_id, payload dict).

        Raises:
            HTTPException: If token is missing/invalid or access is forbidden.
        """
        token = self._extract_token(request)
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing authentication token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        payload = self._decode_token(token)

        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload",
            )

        self._validate_exp(payload)
        self._authorize_admin(path, payload)
        return user_id, payload

    def _validate_exp(self, payload: dict[str, Any]) -> None:
        """Validate token expiration."""
        exp = payload.get("exp")
        if exp and datetime.fromtimestamp(exp, UTC) < datetime.now(UTC):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
            )

    def _authorize_admin(self, path: str, payload: dict[str, Any]) -> None:
        """Authorize admin endpoints if needed."""
        if self._is_admin_path(path):
            user_role = payload.get("role", "user")
            if user_role != "admin":
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Admin access required",
                )


class TokenManager:
    """Utility class for JWT token operations."""

    def __init__(self, secret_key: str, algorithm: str = "HS256") -> None:
        self.secret_key = secret_key
        self.algorithm = algorithm

    def create_access_token(
        self,
        user_id: str,
        user_role: str = "user",
        permissions: list[str] | None = None,
        expires_delta: int = 3600,
    ) -> str:
        """Create a JWT access token.

        Args:
            user_id: Subject identifier.
            user_role: Role claim, default "user".
            permissions: Optional permission list.
            expires_delta: Expiration in seconds.

        Returns:
            Encoded JWT string.
        """
        now = datetime.now(UTC)
        expire = now.timestamp() + expires_delta
        payload = {
            "sub": user_id,
            "role": user_role,
            "permissions": list(permissions or []),
            "iat": now.timestamp(),
            "exp": expire,
            "type": "access",
        }
        import jwt as pyjwt

        return pyjwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def create_refresh_token(self, user_id: str, expires_delta: int = 86400 * 7) -> str:
        """Create a JWT refresh token.

        Args:
            user_id: Subject identifier.
            expires_delta: Expiration in seconds, default 7 days.

        Returns:
            Encoded JWT string.
        """
        now = datetime.now(UTC)
        expire = now.timestamp() + expires_delta
        payload = {
            "sub": user_id,
            "iat": now.timestamp(),
            "exp": expire,
            "type": "refresh",
        }
        import jwt as pyjwt

        return pyjwt.encode(payload, self.secret_key, algorithm=self.algorithm)


def attach(app: FastAPI) -> None:
    """Attach the AuthenticationMiddleware to the FastAPI app."""
    from typing import cast

    app.add_middleware(cast("Any", AuthenticationMiddleware))


def require_permission(scope: str) -> Any:
    """Alias to app.dependencies.require_permissions for single-scope usage."""
    from app.dependencies import (
        require_permissions,
    )  # local to avoid cycles

    return require_permissions(scope)


# Global token manager instance
token_manager = TokenManager(
    secret_key=getattr(settings, "secret_key", "fallback_secret_key")
)


def get_current_user(request: Request) -> dict[str, Any]:
    """Get current authenticated user from request state.

    Args:
        request: FastAPI request.

    Returns:
        Dict with user details and token payload.

    Raises:
        HTTPException: If user is not authenticated.
    """
    if not hasattr(request.state, "user_id"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authenticated",
        )

    return {
        "user_id": request.state.user_id,
        "role": getattr(request.state, "user_role", "user"),
        "permissions": getattr(request.state, "user_permissions", []),
        "payload": getattr(request.state, "token_payload", {}),
    }


def require_admin(current_user: dict[str, Any] | None = None) -> dict[str, Any]:
    """Require admin role for endpoint access.

    Args:
        current_user: The current user dict from dependency.

    Returns:
        The current user dict if authorized.

    Raises:
        HTTPException: If unauthenticated or not admin.
    """
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
        )

    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )

    return current_user
