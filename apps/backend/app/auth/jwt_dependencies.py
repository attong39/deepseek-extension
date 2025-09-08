from __future__ import annotations

import asyncio
import logging
from datetime import UTC, datetime, timedelta
from typing import Any

import jwt
from app.security.jwt import ALGORITHM, SECRET_KEY
from cachetools import TTLCache
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPBearer
from pydantic import BaseModel, Field
import Exception
import KeyError
import config
import dict
import e
import hash
import int
import refresh_token
import request
import self
import str
import token

"""JWT dependencies với hiệu suất cao và async support.
Module này cung cấp:
- JWTBearer class với cache và async decoding
- Token validation với metadata caching
- Refresh token handling
"""
logger = logging.getLogger(__name__)
security = HTTPBearer()


class JWTConfig(BaseModel):
    """Configuration cho JWT handling."""

    secret_key: str = Field(default=SECRET_KEY)
    algorithm: str = Field(default=ALGORITHM)
    access_token_expire_minutes: int = Field(default=30)
    refresh_token_expire_days: int = Field(default=7)
    cache_ttl_seconds: int = Field(default=300)  # 5 minutes
    cache_maxsize: int = Field(default=1000)


class JWTBearer:
    """JWT Bearer authentication với cache và async support."""

    def __init__(self, config: JWTConfig = None):
        self.config = config or JWTConfig()
        self._token_cache = TTLCache(
            maxsize=self.config.cache_maxsize, ttl=self.config.cache_ttl_seconds
        )
        self._claims_cache = TTLCache(maxsize=100, ttl=3600)  # 1 hour

    async def decode_async(self, token: str) -> dict[str, Any]:
        """Async JWT decoding với cache support.
        Args:
            token: JWT token string
        Returns:
            Decoded payload
        Raises:
            HTTPException: Nếu token invalid hoặc expired
        """
        if token in self._token_cache:
            cached_payload = self._token_cache[token]
            logger.debug("JWT token served from cache")
            return cached_payload
        try:
            loop = asyncio.get_event_loop()
            payload = await loop.run_in_executor(
                None, jwt.decode, token, self.config.secret_key, [self.config.algorithm]
            )
            exp = payload.get("exp")
            if exp and datetime.fromtimestamp(exp, tz=UTC) < datetime.now(UTC):
                raise jwt.ExpiredSignatureError("Token has expired")
            self._token_cache[token] = payload
            logger.info("JWT token decoded and cached", token_hash=hash(token) % 1000)
            return payload
        except jwt.ExpiredSignatureError:
            logger.warning("JWT token expired", token_hash=hash(token) % 1000)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except jwt.InvalidTokenError as e:
            logger.warning("Invalid JWT token", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except Exception as e:
            logger.error("JWT decode error", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Token validation failed",
            )

    async def __call__(self, request: Request) -> dict[str, Any]:
        """Extract và validate JWT token từ request.
        Args:
            request: FastAPI request
        Returns:
            Decoded token payload
        """
        credentials = await security(request)
        if not credentials:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing authentication token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return await self.decode_async(credentials.credentials)


jwt_bearer = JWTBearer()


def get_current_user_via_jwt(
    payload: dict[str, Any] = Depends(jwt_bearer),
) -> dict[str, Any]:
    """Extract user info từ JWT payload.
    Args:
        payload: Decoded JWT payload
    Returns:
        User information dict
    """
    try:
        user_id = payload.get("sub")
        username = payload.get("username")
        email = payload.get("email")
        roles = payload.get("roles", [])
        tenant_id = payload.get("tenant_id", "default")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload",
            )
        return {
            "user_id": user_id,
            "username": username,
            "email": email,
            "roles": roles,
            "tenant_id": tenant_id,
        }
    except KeyError as e:
        logger.error("Missing required field in JWT payload", field=str(e))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token structure",
        )


def create_refresh_token(user_id: str, tenant_id: str = "default") -> str:
    """Tạo refresh token với expiry dài hơn.
    Args:
        user_id: User ID
        tenant_id: Tenant ID
    Returns:
        Encoded refresh token
    """
    expire = datetime.now(UTC) + timedelta(days=7)
    payload = {
        "sub": user_id,
        "tenant_id": tenant_id,
        "type": "refresh",
        "exp": expire,
        "iat": datetime.now(UTC),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def validate_refresh_token(refresh_token: str) -> dict[str, Any]:
    """Validate refresh token và return payload.
    Args:
        refresh_token: Refresh token string
    Returns:
        Decoded payload nếu valid
    Raises:
        HTTPException: Nếu token invalid
    """
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type",
            )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token expired",
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )


__all__ = [
    "JWTBearer",
    "JWTConfig",
    "cached_payload",
    "create_refresh_token",
    "credentials",
    "email",
    "exp",
    "expire",
    "get_current_user_via_jwt",
    "jwt_bearer",
    "logger",
    "loop",
    "payload",
    "roles",
    "security",
    "tenant_id",
    "user_id",
    "username",
    "validate_refresh_token",
]
