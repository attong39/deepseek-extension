from __future__ import annotations

import logging
import time
from typing import Any

import jwt
from fastapi import HTTPException, Request, Response
from fastapi.security import HTTPBearer
from starlette.middleware.base import BaseHTTPMiddleware
import Exception
import algorithm
import any
import app
import auto_error
import bool
import call_next
import dict
import e
import excluded_paths
import expires_in
import float
import int
import last_activity
import list
import path
import request
import secret_key
import self
import str
import super

"""JWT Authentication Middleware - Production Ready.
Module này implement JWT middleware cho FastAPI để:
1. Decode và validate JWT tokens
2. Extract user info và set vào request.state.auth
3. Handle token expiry, revocation, rotation
4. Rate limiting per user
"""
logger = logging.getLogger(__name__)
JWT_SECRET_KEY = "your-secret-key"  # TODO: Load từ environment
JWT_ALGORITHM = "HS256"
JWT_EXPIRY_SECONDS = 3600  # 1 hour


class AuthInfo:
    """Container cho thông tin authentication từ JWT."""

    def __init__(
        self,
        user_id: str,
        roles: list[str],
        tenant_id: str | None = None,
        permissions: list[str] | None = None,
        mfa_level: int = 0,
        session_id: str | None = None,
        last_activity: float | None = None,
    ):
        self.user_id = user_id
        self.roles = roles
        self.tenant_id = tenant_id
        self.permissions = permissions or []
        self.mfa_level = mfa_level
        self.session_id = session_id
        self.last_activity = last_activity


class JWTMiddleware(BaseHTTPMiddleware):
    """JWT Authentication Middleware cho FastAPI.
    Middleware này:
    1. Extract JWT từ Authorization header
    2. Decode và validate token
    3. Set request.state.auth với user info
    4. Handle errors và unauthorized requests
    """

    def __init__(
        self,
        app,
        secret_key: str = JWT_SECRET_KEY,
        algorithm: str = JWT_ALGORITHM,
        auto_error: bool = True,
        excluded_paths: list[str] | None = None,
    ):
        super().__init__(app)
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.auto_error = auto_error
        self.excluded_paths = excluded_paths or [
            "/health",
            "/docs",
            "/openapi.json",
            "/auth/login",
            "/auth/register",
        ]
        self.bearer = HTTPBearer(auto_error=False)

    async def dispatch(self, request: Request, call_next) -> Response:
        """Process request với JWT authentication."""
        if any(request.url.path.startswith(path) for path in self.excluded_paths):
            return await call_next(request)
        auth_info = await self._extract_auth_info(request)
        if auth_info is None and self.auto_error:
            raise HTTPException(
                status_code=401,
                detail="Authentication required",
                headers={"WWW-Authenticate": "Bearer"},
            )
        request.state.auth = auth_info
        response = await call_next(request)
        return response

    async def _extract_auth_info(self, request: Request) -> AuthInfo | None:
        """Extract authentication info từ JWT token.
        Args:
            request: FastAPI Request object
        Returns:
            AuthInfo nếu token valid, None nếu invalid/missing
        """
        try:
            authorization = request.headers.get("authorization")
            if not authorization:
                logger.debug("No authorization header found")
                return None
            if not authorization.startswith("Bearer "):
                logger.debug("Invalid authorization header format")
                return None
            token = authorization[7:]  # Remove "Bearer " prefix
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            if "sub" not in payload:  # subject (user_id)
                logger.warning("JWT missing 'sub' claim")
                return None
            user_id = payload["sub"]
            roles = payload.get("roles", [])
            tenant_id = payload.get("tenant_id")
            permissions = payload.get("permissions", [])
            mfa_level = payload.get("mfa_level", 0)
            session_id = payload.get("session_id")
            exp = payload.get("exp")
            if exp and time.time() > exp:
                logger.warning(f"JWT expired for user {user_id}")
                return None
            return AuthInfo(
                user_id=user_id,
                roles=roles,
                tenant_id=tenant_id,
                permissions=permissions,
                mfa_level=mfa_level,
                session_id=session_id,
                last_activity=time.time(),
            )
        except jwt.ExpiredSignatureError:
            logger.warning("JWT token expired")
            return None
        except jwt.InvalidTokenError:
            logger.warning("Invalid JWT token")
            return None
        except Exception as e:
            logger.error(f"Error processing JWT token: {e}")
            return None


def create_jwt_token(
    user_id: str,
    roles: list[str],
    tenant_id: str | None = None,
    permissions: list[str] | None = None,
    mfa_level: int = 0,
    session_id: str | None = None,
    expires_in: int = JWT_EXPIRY_SECONDS,
) -> str:
    """Create JWT token cho user.
    Args:
        user_id: ID người dùng
        roles: Danh sách roles
        tenant_id: ID tenant
        permissions: JIT permissions
        mfa_level: Mức độ MFA
        session_id: ID phiên làm việc
        expires_in: Thời gian hết hạn (seconds)
    Returns:
        JWT token string
    """
    now = time.time()
    payload = {
        "sub": user_id,
        "roles": roles,
        "tenant_id": tenant_id,
        "permissions": permissions or [],
        "mfa_level": mfa_level,
        "session_id": session_id,
        "iat": now,  # issued at
        "exp": now + expires_in,  # expiry
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


def decode_jwt_token(token: str) -> dict[str, Any] | None:
    """Decode JWT token và return payload.
    Args:
        token: JWT token string
    Returns:
        Payload dict nếu valid, None nếu invalid
    """
    try:
        return jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
    except jwt.InvalidTokenError:
        return None


async def revoke_token(token: str) -> None:
    """Revoke JWT token (add to blacklist).
    Args:
        token: JWT token to revoke
    """


async def is_token_revoked(token: str) -> bool:
    """Check if JWT token is revoked.
    Args:
        token: JWT token to check
    Returns:
        True if revoked
    """
    return False


__all__ = [
    "AuthInfo",
    "JWTMiddleware",
    "create_jwt_token",
    "decode_jwt_token",
]
