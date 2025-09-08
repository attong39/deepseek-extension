from __future__ import annotations

import hashlib
import time
from datetime import datetime, timedelta
from typing import Any

import jwt
from apps.backend.config.production import Settings
from passlib.context import CryptContext
import any
import bool
import c
import data
import dict
import expires_delta
import float
import hashed_password
import int
import key
import len
import limit
import list
import mask_char
import max
import password
import plain_password
import req
import req_time
import request_headers
import requests
import role
import self
import staticmethod
import str
import subject
import token
import tuple
import window

"""
Production JWT Authentication & Security
Supports OAuth2 Password flow with RBAC
"""
settings = Settings()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a password with bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(
    subject: str, role: str = "user", expires_delta: timedelta | None = None
) -> str:
    """Create a JWT access token."""
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.jwt_exp_minutes)
    payload: dict[str, Any] = {
        "sub": subject,
        "role": role,
        "iat": datetime.utcnow(),
        "exp": expire,
        "type": "access",
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def decode_access_token(token: str) -> dict[str, Any] | None:
    """Decode and validate JWT access token."""
    try:
        payload = jwt.decode(
            token, settings.jwt_secret, algorithms=[settings.jwt_algorithm]
        )
        if payload.get("type") != "access":
            return None
        return payload
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, jwt.DecodeError):
        return None


def hash_token(token: str) -> str:
    """Hash a token for storage (session tracking)."""
    return hashlib.sha256(token.encode()).hexdigest()


class SecurityUtils:
    """Security utility functions."""

    @staticmethod
    def is_strong_password(password: str) -> tuple[bool, str]:
        """Check if password meets security requirements."""
        if len(password) < 8:
            return False, "Password must be at least 8 characters long"
        if not any(c.isupper() for c in password):
            return False, "Password must contain at least one uppercase letter"
        if not any(c.islower() for c in password):
            return False, "Password must contain at least one lowercase letter"
        if not any(c.isdigit() for c in password):
            return False, "Password must contain at least one digit"
        special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        if not any(c in special_chars for c in password):
            return False, "Password must contain at least one special character"
        return True, "Password is strong"

    @staticmethod
    def mask_sensitive_data(data: str, mask_char: str = "*") -> str:
        """Mask sensitive data for logging."""
        if len(data) <= 4:
            return mask_char * len(data)
        visible_chars = 2
        masked_length = len(data) - (2 * visible_chars)
        return data[:visible_chars] + mask_char * masked_length + data[-visible_chars:]

    @staticmethod
    def get_client_ip(request_headers: dict[str, str]) -> str:
        """Extract client IP from request headers."""
        forwarded_for = request_headers.get("x-forwarded-for")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        real_ip = request_headers.get("x-real-ip")
        if real_ip:
            return real_ip
        return request_headers.get("remote-addr", "unknown")


class RateLimiter:
    """Simple in-memory rate limiter."""

    def __init__(self):
        self._requests: dict[str, list[float]] = {}

    def is_allowed(
        self, key: str, limit: int = 100, window: int = 60
    ) -> tuple[bool, dict[str, Any]]:
        """Check if request is allowed under rate limit."""
        now = time.time()
        window_start = now - window
        if key in self._requests:
            self._requests[key] = [
                req_time for req_time in self._requests[key] if req_time > window_start
            ]
        else:
            self._requests[key] = []
        current_count = len(self._requests[key])
        allowed = current_count < limit
        if allowed:
            self._requests[key].append(now)
        return allowed, {
            "limit": limit,
            "remaining": max(0, limit - current_count - (1 if allowed else 0)),
            "reset_time": int(window_start + window),
            "retry_after": int(window) if not allowed else 0,
        }

    def clear_key(self, key: str) -> None:
        """Clear rate limit for a specific key."""
        self._requests.pop(key, None)

    def get_stats(self) -> dict[str, Any]:
        """Get rate limiter statistics."""
        now = time.time()
        active_keys = 0
        total_requests = 0
        for key, requests in self._requests.items():
            recent_requests = [req for req in requests if now - req < 300]
            if recent_requests:
                active_keys += 1
                total_requests += len(recent_requests)
        return {
            "active_keys": active_keys,
            "total_recent_requests": total_requests,
            "timestamp": now,
        }


rate_limiter = RateLimiter()
__all__ = [
    "RateLimiter",
    "SecurityUtils",
    "active_keys",
    "allowed",
    "clear_key",
    "create_access_token",
    "current_count",
    "decode_access_token",
    "expire",
    "forwarded_for",
    "get_client_ip",
    "get_stats",
    "hash_password",
    "hash_token",
    "is_allowed",
    "is_strong_password",
    "mask_sensitive_data",
    "masked_length",
    "now",
    "payload",
    "pwd_context",
    "rate_limiter",
    "real_ip",
    "recent_requests",
    "settings",
    "special_chars",
    "total_requests",
    "verify_password",
    "visible_chars",
    "window_start",
]
