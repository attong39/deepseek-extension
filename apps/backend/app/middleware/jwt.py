"""
JWT Authentication Middleware cho ZETA_AI Autonomous System.

Middleware này cung cấp:
- JWT token validation cho API endpoints
- Security context injection cho autonomous operations
- Rate limiting per user
- Audit logging cho security events
"""

from __future__ import annotations

import logging
import time
from typing import Any

import jwt
from apps.backend.core.security.context import SecurityContext
from fastapi import HTTPException, Request, Response, status
from fastapi.security import HTTPBearer
from starlette.middleware.base import BaseHTTPMiddleware
import Exception
import algorithm
import any
import app
import autonomous_path
import autonomous_paths
import autonomous_rate_limit
import bool
import call_next
import dict
import e
import event_type
import excluded_path
import excluded_paths
import hasattr
import header
import int
import k
import kwargs
import metadata
import path
import rate_limit_per_minute
import request
import secret_key
import self
import set
import str
import super
import v
import value

logger = logging.getLogger(__name__)


class JWTMiddleware(BaseHTTPMiddleware):
    """
    JWT Authentication middleware với hỗ trợ autonomous operations.

    Features:
    - JWT token validation
    - Security context injection
    - Rate limiting per user
    - Autonomous session tracking
    - Audit logging
    """

    def __init__(
        self,
        app,
        secret_key: str,
        algorithm: str = "HS256",
        excluded_paths: set[str] | None = None,
        rate_limit_per_minute: int = 100,
        autonomous_rate_limit: int = 1000,  # Higher limit for autonomous operations
    ):
        super().__init__(app)
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.excluded_paths = excluded_paths or {
            "/health",
            "/metrics",
            "/docs",
            "/openapi.json",
            "/redoc",
        }
        self.rate_limit_per_minute = rate_limit_per_minute
        self.autonomous_rate_limit = autonomous_rate_limit

        # Rate limiting storage (in production, use Redis)
        self._rate_limit_storage: dict[str, dict[str, Any]] = {}

        self.security = HTTPBearer(auto_error=False)

    async def dispatch(self, request: Request, call_next) -> Response:
        """Process incoming request with JWT validation."""
        start_time = time.time()

        try:
            # Skip authentication for excluded paths
            if self._is_excluded_path(request.url.path):
                response = await call_next(request)
                return self._add_security_headers(response)

            # Extract and validate JWT token
            security_context = await self._authenticate_request(request)

            # Check rate limits
            await self._check_rate_limit(security_context, request)

            # Inject security context into request state
            request.state.security_context = security_context

            # Log security event
            await self._log_security_event(request, security_context, "authenticated")

            # Process request
            response = await call_next(request)

            # Add security headers
            response = self._add_security_headers(response)

            # Log successful request
            duration = time.time() - start_time
            logger.debug(
                f"Authenticated request completed: {request.method} {request.url.path} "
                f"user={security_context.user_id} duration={duration:.3f}s"
            )

            return response

        except HTTPException as e:
            # Log authentication failure
            await self._log_security_event(
                request,
                None,
                "auth_failed",
                {"error": str(e.detail), "status_code": e.status_code},
            )
            raise

        except Exception as e:
            logger.error(f"JWT middleware error: {e}")
            await self._log_security_event(
                request, None, "middleware_error", {"error": str(e)}
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Authentication service error",
            )

    async def _authenticate_request(self, request: Request) -> SecurityContext:
        """Extract and validate JWT token from request."""
        # Get Authorization header
        auth_header = request.headers.get("authorization")
        if not auth_header:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing authorization header",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Extract token
        if not auth_header.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authorization header format",
                headers={"WWW-Authenticate": "Bearer"},
            )

        token = auth_header.split(" ")[1]

        # Validate JWT token
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])

            # Extract claims
            user_id = payload.get("sub")
            tenant_id = payload.get("tenant_id", "default")
            scopes = payload.get("scopes", [])
            is_autonomous = payload.get("is_autonomous", False)
            session_id = payload.get("session_id")

            if not user_id:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token: missing user ID",
                )

            # Create security context
            return SecurityContext(
                user_id=user_id,
                tenant_id=tenant_id,
                scopes=set(scopes),
                is_autonomous=is_autonomous,
                session_id=session_id,
                token=token,
            )

        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired"
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )

    async def _check_rate_limit(
        self, security_context: SecurityContext, request: Request
    ) -> None:
        """Check rate limits for user."""
        user_key = f"{security_context.tenant_id}:{security_context.user_id}"
        current_time = time.time()
        current_minute = int(current_time // 60)

        # Get rate limit data
        rate_data = self._rate_limit_storage.get(
            user_key, {"minute": current_minute, "count": 0}
        )

        # Reset counter if new minute
        if rate_data["minute"] != current_minute:
            rate_data = {"minute": current_minute, "count": 0}

        # Check limits
        limit = (
            self.autonomous_rate_limit
            if security_context.is_autonomous
            else self.rate_limit_per_minute
        )

        if rate_data["count"] >= limit:
            await self._log_security_event(
                request,
                security_context,
                "rate_limit_exceeded",
                {"limit": limit, "count": rate_data["count"]},
            )
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Rate limit exceeded: {limit} requests per minute",
            )

        # Increment counter
        rate_data["count"] += 1
        self._rate_limit_storage[user_key] = rate_data

        # Cleanup old entries (keep only last 5 minutes)
        cleanup_cutoff = current_minute - 5
        self._rate_limit_storage = {
            k: v
            for k, v in self._rate_limit_storage.items()
            if v["minute"] > cleanup_cutoff
        }

    def _is_excluded_path(self, path: str) -> bool:
        """Check if path is excluded from authentication."""
        return any(
            path.startswith(excluded_path) for excluded_path in self.excluded_paths
        )

    def _add_security_headers(self, response: Response) -> Response:
        """Add security headers to response."""
        security_headers = {
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "X-XSS-Protection": "1; mode=block",
            "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
            "Referrer-Policy": "strict-origin-when-cross-origin",
        }

        for header, value in security_headers.items():
            response.headers[header] = value

        return response

    async def _log_security_event(
        self,
        request: Request,
        security_context: SecurityContext | None,
        event_type: str,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        """Log security event for audit trail."""
        log_data = {
            "event_type": event_type,
            "method": request.method,
            "path": request.url.path,
            "client_ip": request.client.host if request.client else "unknown",
            "user_agent": request.headers.get("user-agent", "unknown"),
            "timestamp": time.time(),
        }

        if security_context:
            log_data.update(
                {
                    "user_id": security_context.user_id,
                    "tenant_id": security_context.tenant_id,
                    "is_autonomous": security_context.is_autonomous,
                    "session_id": security_context.session_id,
                }
            )

        if metadata:
            log_data["metadata"] = metadata

        # Log at appropriate level
        if event_type in ["auth_failed", "rate_limit_exceeded"]:
            logger.warning(f"Security event: {log_data}")
        elif event_type == "middleware_error":
            logger.error(f"Security event: {log_data}")
        else:
            logger.info(f"Security event: {log_data}")


class JWTAutonomousMiddleware(JWTMiddleware):
    """
    Specialized JWT middleware cho autonomous operations.

    Features:
    - Autonomous session validation
    - Extended permissions for AI agents
    - Specialized rate limiting
    - Autonomous operation logging
    """

    def __init__(
        self, app, secret_key: str, autonomous_paths: set[str] | None = None, **kwargs
    ):
        super().__init__(app, secret_key, **kwargs)
        self.autonomous_paths = autonomous_paths or {
            "/api/v1/autonomous",
            "/api/v1/planning",
            "/api/v1/skills",
            "/api/v1/safety",
        }

    async def _authenticate_request(self, request: Request) -> SecurityContext:
        """Enhanced authentication for autonomous operations."""
        security_context = await super()._authenticate_request(request)

        # Check if this is an autonomous path
        if self._is_autonomous_path(request.url.path):
            if not security_context.is_autonomous:
                await self._log_security_event(
                    request,
                    security_context,
                    "autonomous_access_denied",
                    {"required_autonomous": True},
                )
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Autonomous token required for this endpoint",
                )

            # Validate autonomous session
            await self._validate_autonomous_session(security_context, request)

        return security_context

    def _is_autonomous_path(self, path: str) -> bool:
        """Check if path requires autonomous authentication."""
        return any(
            path.startswith(autonomous_path)
            for autonomous_path in self.autonomous_paths
        )

    async def _validate_autonomous_session(
        self, security_context: SecurityContext, request: Request
    ) -> None:
        """Validate autonomous session state."""
        if not security_context.session_id:
            await self._log_security_event(
                request, security_context, "autonomous_session_missing"
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Autonomous session ID required",
            )

        # Additional autonomous validation logic can be added here
        # For example: check if session is still active, validate permissions, etc.

        logger.debug(
            f"Validated autonomous session: {security_context.session_id} "
            f"for user: {security_context.user_id}"
        )


def create_jwt_middleware(
    secret_key: str, is_autonomous: bool = False, **kwargs
) -> JWTMiddleware:
    """
    Factory function to create appropriate JWT middleware.

    Args:
        secret_key: JWT signing secret
        is_autonomous: Whether to use autonomous-specific middleware
        **kwargs: Additional middleware configuration

    Returns:
        Configured JWT middleware instance
    """
    if is_autonomous:
        return JWTAutonomousMiddleware(None, secret_key, **kwargs)
    else:
        return JWTMiddleware(None, secret_key, **kwargs)


def get_security_context(request: Request) -> SecurityContext:
    """
    Extract security context from request state.

    Args:
        request: FastAPI request object

    Returns:
        Security context injected by JWT middleware

    Raises:
        HTTPException: If security context not found
    """
    if not hasattr(request.state, "security_context"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Security context not found - authentication required",
        )

    return request.state.security_context
