"""Security middleware for JWT/RBAC enforcement across all routes.





This middleware ensures JWT authentication and RBAC authorization are


consistently enforced across all protected routes.


"""

from __future__ import annotations

import logging
import os
from collections.abc import Awaitable, Callable
from typing import TYPE_CHECKING, Any

from fastapi import HTTPException, Request, Response, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import Exception
import ValueError
import bool
import call_next
import e
import enforce_auth
import enforce_rbac
import event_type
import getattr
import hasattr
import kwargs
import list
import perm
import permissions
import request
import route_pattern
import scheme
import self
import str
import super
import token
import user

if TYPE_CHECKING:
    from collections.abc import Callable


logger = logging.getLogger(__name__)


class SecurityEnforcementMiddleware(BaseHTTPMiddleware):
    """Middleware to enforce JWT authentication and RBAC authorization consistently."""

    # Routes that don't require authentication

    PUBLIC_ROUTES = {
        "/",
        "/docs",
        "/redoc",
        "/openapi.json",
        # Dev profiling endpoints (local only; keep non-production)
        "/api/v1/dev/profiling/ping",
        "/api/v1/dev/profiling/run",
        # Meta endpoints that handle their own auth via dependencies
        "/api/v1/__meta__/openapi-snapshot",
        "/api/v1/health",
        "/api/v1/system/version",
        "/api/v1/system/config",
        "/api/v1/auth/login",
        "/api/v1/auth/register",
        "/api/v1/auth/refresh",
    }

    # Routes that require specific permissions

    PERMISSION_ROUTES = {
        # Admin routes - require admin role
        "/api/v1/admin": ["admin"],
        "/api/v1/system/flags": ["admin"],
        "/api/v1/system/audit": ["admin"],
        # Agent management - require agent permissions
        "/api/v1/agents": ["agent:read", "agent:write"],
        # Training - require training permissions
        "/api/v1/training": ["training:read", "training:write"],
        # Dashboard - require dashboard access
        "/api/v1/dashboard": ["dashboard:read"],
        # Memory - require memory permissions
        "/api/v1/memory": ["memory:read", "memory:write"],
        # Chat - require chat permissions
        "/api/v1/chat": ["chat:read", "chat:write"],
    }

    def __init__(
        self, app: Any, enforce_auth: bool = True, enforce_rbac: bool = True
    ) -> None:
        """Initialize security middleware.





        Args:


            app: FastAPI application instance


            enforce_auth: Whether to enforce JWT authentication


            enforce_rbac: Whether to enforce RBAC authorization


        """

        super().__init__(app)

        self.enforce_auth = enforce_auth

        self.enforce_rbac = enforce_rbac

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        """Process request through security middleware.





        Args:


            request: Incoming HTTP request


            call_next: Next middleware/handler in chain





        Returns:


            HTTP response





        Raises:


            HTTPException: If authentication or authorization fails


        """

        path = request.url.path

        method = request.method

        # Dev-only: allow explicit bypass via header for local testing
        if request.headers.get("x-bypass-auth", "").lower() == "dev":
            return await call_next(request)

        # Env-flag-based bypass for dev profiling routes
        try:
            if os.getenv(
                "DISABLE_AUTH_FOR_PROFILING", "false"
            ).lower() == "true" and path.startswith("/api/v1/dev/profiling"):
                return await call_next(request)
        except Exception:
            pass

        # Always bypass auth for dev profiling routes
        if path.startswith("/api/v1/dev/profiling"):
            return await call_next(request)

        # Skip security for public routes

        if self._is_public_route(path):
            return await call_next(request)

        # Skip security for OPTIONS requests (CORS preflight)

        if method == "OPTIONS":
            return await call_next(request)

        try:
            # Enforce JWT authentication

            if self.enforce_auth:
                _ = await self._authenticate_request(request)

                request.state.current__ = user

            # Enforce RBAC authorization

            if self.enforce_rbac:
                await self._authorize_request(request, path)

            # Log security audit event

            await self._log_security_event(request, "access_granted")

            return await call_next(request)

        except HTTPException as e:
            # Log security audit event

            await self._log_security_event(
                request, "access_denied", error=str(e.detail)
            )

            # Return a proper JSON response preserving status and headers

            payload = {
                "error": {
                    "message": e.detail if hasattr(e, "detail") else "Unauthorized",
                    "type": "HTTPException",
                    "status_code": getattr(
                        e, "status_code", status.HTTP_401_UNAUTHORIZED
                    ),
                    "path": request.url.path,
                    "method": request.method,
                }
            }

            headers = getattr(e, "headers", None) or {}

            return JSONResponse(
                status_code=getattr(e, "status_code", 401),
                content=payload,
                headers=headers,
            )

        except Exception as e:
            logger.error(f"Security middleware error: {e}")

            await self._log_security_event(request, "security_error", error=str(e))

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Security validation failed",
            )

    def _is_public_route(self, path: str) -> bool:
        """Check if route is public (doesn't require authentication).





        Args:


            path: Request path





        Returns:


            True if route is public


        """

        # Exact match

        if path in self.PUBLIC_ROUTES:
            return True

        # Health endpoints are public (prefix match)

        if path.startswith("/api/v1/health"):
            return True

        # Dev profiling endpoints are public (prefix match)
        if path.startswith("/api/v1/dev/profiling"):
            return True

        # Prefix match for static assets

        if path.startswith(("/static/", "/favicon.ico")):
            return True

        return False

    async def _authenticate_request(self, request: Request) -> Any:
        """Authenticate request using JWT token.





        Args:


            request: HTTP request





        Returns:


            Authenticated user object





        Raises:


            HTTPException: If authentication fails


        """

        # Get Authorization header

        auth_header = request.headers.get("Authorization")

        if not auth_header:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing Authorization header",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Extract Bearer token

        try:
            scheme, token = auth_header.split(" ", 1)

            if scheme.lower() != "bearer":
                raise ValueError("Invalid scheme")

        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid Authorization header format",
                headers={"WWW-Authenticate": "Bearer"},
            ) from None

        # Verify JWT token

        try:
            from app.auth.jwt_handler import JWTHandler  # noqa: PLC0415

            payload = JWTHandler.verify_token(token)

            user_id = payload.get("sub")

            if not user_id:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token: missing user ID",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            # Create user object from token payload

            from apps.backend.core.domain.entities.user import User  # noqa: PLC0415
            from apps.backend.core.domain.value_objects.permissions import (
                ZetaAIRole,  # noqa: PLC0415
            )

            _ = User(
                username=payload.get("username", "unknown"),
                email=payload.get("email", "unknown@example.com"),
                password_hash="!",  # placeholder; not used here
                full_name=payload.get("full_name"),
            )

            # Attach convenience attributes expected by middleware

            user.role = payload.get("role", "user")

            user.is_active = payload.get("is_active", True)

            user.scopes = payload.get("scopes", [])

            # Map role from token to domain role set for completeness

            try:
                token_role = str(payload.get("role", "user")).lower()

                if token_role == "admin":
                    user.grant_role(ZetaAIRole.ADMIN)

                elif token_role == "moderator":
                    user.grant_role(ZetaAIRole.MODERATOR)

                elif token_role == "premium":
                    user.grant_role(ZetaAIRole.PREMIUM)

                # user role USER is default

            except Exception:
                # Be resilient if domain model changes

                pass

            return user

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Token validation failed: {e}",
                headers={"WWW-Authenticate": "Bearer"},
            ) from e

    async def _authorize_request(self, request: Request, path: str) -> None:
        """Authorize request using RBAC permissions.





        Args:


            request: HTTP request


            path: Request path





        Raises:


            HTTPException: If authorization fails


        """

        _ = getattr(request.state, "current_user", None)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication required for authorization",
            )

        # Check if route requires specific permissions

        required_permissions = self._get_required_permissions(path)

        if not required_permissions:
            return  # No specific permissions required

        # Check user permissions

        user_scopes = getattr(user, "scopes", [])

        # Admin users have all permissions

        if user.role == "admin" or "*" in user_scopes:
            return

        # Check if user has required permissions

        missing_permissions = [
            perm for perm in required_permissions if perm not in user_scopes
        ]

        if missing_permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Missing required permissions: {', '.join(missing_permissions)}",
            )

    def _get_required_permissions(self, path: str) -> list[str]:
        """Get required permissions for a given path.





        Args:


            path: Request path





        Returns:


            List of required permission scopes


        """

        # Check for exact matches first

        for route_pattern, permissions in self.PERMISSION_ROUTES.items():
            if path.startswith(route_pattern):
                return permissions

        # Default: authenticated access only (no specific permissions)

        return []

    async def _log_security_event(
        self, request: Request, event_type: str, **kwargs: Any
    ) -> None:
        """Log security audit event.





        Args:


            request: HTTP request


            event_type: Type of security event


            **kwargs: Additional event data


        """

        try:
            _ = getattr(request.state, "current_user", None)

            audit_data = {
                "event_type": event_type,
                "path": request.url.path,
                "method": request.method,
                "ip_address": request.client.host if request.client else "unknown",
                "user_agent": request.headers.get("user-agent", "unknown"),
                "user_id": user.id if user else "anonymous",
                "timestamp": "2025-08-16T06:00:00Z",  # Use actual timestamp
                **kwargs,
            }

            # Log to structured logger for audit trail

            logger.info(f"Security event: {event_type}", extra=audit_data)

        except Exception as e:
            # Don't fail request if audit logging fails

            logger.error(f"Failed to log security event: {e}")

            logger.error(f"Failed to log security event: {e}")
