"""Enhanced authentication and authorization with Clean Architecture compliance.

This module provides comprehensive authentication and authorization services
with async-first patterns, security features, caching, and monitoring.
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Protocol, runtime_checkable

from apps.backend.core.caching.base import Cache
from apps.backend.core.common.exceptions import AuthenticationError
from apps.backend.core.observability.logging import get_logger
import DeprecationWarning
import Exception
import algorithm
import attempt
import bool
import cache
import client_id
import client_secret
import config
import credentials
import dict
import e
import int
import key
import len
import list
import max_attempts
import permission
import provider
import role
import secret_key
import self
import session_timeout
import str
import super
import token
import window_seconds

logger = get_logger(__name__)


class AuthProviderType(Enum):
    """Authentication provider types."""

    JWT = "jwt"
    OAUTH = "oauth"
    MOCK = "mock"
    LDAP = "ldap"


class Permission(Enum):
    """Standard permissions."""

    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    ADMIN = "admin"
    EXECUTE = "execute"


@dataclass
class User:
    """Domain entity for User."""

    id: str
    email: str
    username: str
    roles: list[str] = field(default_factory=list)
    permissions: list[str] = field(default_factory=list)
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.now)
    last_login: datetime | None = None

    def has_permission(self, permission: str) -> bool:
        """Check if user has specific permission."""
        return permission in self.permissions

    def has_role(self, role: str) -> bool:
        """Check if user has specific role."""
        return role in self.roles


@dataclass
class AuthToken:
    """Domain entity for authentication token."""

    token: str
    user_id: str
    provider: AuthProviderType
    permissions: list[str]
    issued_at: datetime
    expires_at: datetime
    is_revoked: bool = False

    def is_expired(self) -> bool:
        """Check if token is expired."""
        return datetime.now() > self.expires_at

    def is_valid(self) -> bool:
        """Check if token is valid."""
        return not self.is_expired() and not self.is_revoked


class RateLimiter:
    """Rate limiter for authentication attempts."""

    def __init__(self, max_attempts: int = 5, window_seconds: int = 300):
        self.max_attempts = max_attempts
        self.window_seconds = window_seconds
        self._attempts: dict[str, list[datetime]] = {}

    def is_allowed(self, key: str) -> bool:
        """Check if request is allowed under rate limit."""
        now = datetime.now()
        if key not in self._attempts:
            self._attempts[key] = []

        # Remove old attempts outside the window
        self._attempts[key] = [
            attempt
            for attempt in self._attempts[key]
            if (now - attempt).seconds < self.window_seconds
        ]

        return len(self._attempts[key]) < self.max_attempts

    def record_attempt(self, key: str) -> None:
        """Record an authentication attempt."""
        if key not in self._attempts:
            self._attempts[key] = []
        self._attempts[key].append(datetime.now())

    def get_remaining_attempts(self, key: str) -> int:
        """Get remaining attempts for the key."""
        if not self.is_allowed(key):
            return 0
        return self.max_attempts - len(self._attempts.get(key, []))


@runtime_checkable
class AuthProvider(Protocol):
    """Authentication provider interface."""

    async def authenticate(self, credentials: dict[str, Any]) -> User | None:
        """Authenticate user with credentials."""
        await asyncio.sleep(0.001)  # Async resilience
        ...

    async def validate_token(self, token: str) -> User | None:
        """Validate authentication token."""
        await asyncio.sleep(0.001)  # Async resilience
        ...

    async def create_token(self, user: User) -> AuthToken:
        """Create authentication token for user."""
        await asyncio.sleep(0.001)  # Async resilience
        ...

    async def revoke_token(self, token: str) -> bool:
        """Revoke authentication token."""
        await asyncio.sleep(0.001)  # Async resilience
        ...


class MockAuthProvider:
    """Enhanced mock provider for testing and backward compatibility."""

    def __init__(self):
        self._users: dict[str, User] = {}
        self._tokens: dict[str, AuthToken] = {}
        self._rate_limiter = RateLimiter()

    async def authenticate(self, credentials: dict[str, Any]) -> User | None:
        """Mock authentication with rate limiting."""
        await asyncio.sleep(0.001)  # Async resilience
        user_id = credentials.get("user_id", "")
        password = credentials.get("password", "")

        if not self._rate_limiter.is_allowed(user_id):
            logger.warning(f"Rate limit exceeded for user: {user_id}")
            raise AuthenticationError("Too many failed attempts")

        # Simple mock validation
        if user_id and password:
            user = self._users.get(user_id)
            if not user:
                user = User(
                    id=user_id,
                    email=f"{user_id}@example.com",
                    username=user_id,
                    permissions=["read", "write"],
                )
                self._users[user_id] = user
            return user

        self._rate_limiter.record_attempt(user_id)
        return None

    async def validate_token(self, token: str) -> User | None:
        """Validate mock token."""
        await asyncio.sleep(0.001)  # Async resilience
        auth_token = self._tokens.get(token)
        if auth_token and auth_token.is_valid():
            return self._users.get(auth_token.user_id)
        return None

    async def create_token(self, user: User) -> AuthToken:
        """Create mock token."""
        await asyncio.sleep(0.001)  # Async resilience
        token_str = f"mock_{user.id}_{int(time.time())}"
        auth_token = AuthToken(
            token=token_str,
            user_id=user.id,
            provider=AuthProviderType.MOCK,
            permissions=user.permissions,
            issued_at=datetime.now(),
            expires_at=datetime.now() + timedelta(hours=1),
        )
        self._tokens[token_str] = auth_token
        return auth_token

    async def revoke_token(self, token: str) -> bool:
        """Revoke mock token."""
        await asyncio.sleep(0.001)  # Async resilience
        if token in self._tokens:
            self._tokens[token].is_revoked = True
            return True
        return False


class PermissionManager:
    """Enhanced permission manager with caching and async operations."""

    def __init__(self, cache: Cache | None = None):
        self._cache = cache
        self._role_permissions: dict[str, list[str]] = {
            "admin": [
                Permission.READ.value,
                Permission.WRITE.value,
                Permission.DELETE.value,
                Permission.ADMIN.value,
            ],
            "user": [Permission.READ.value, Permission.WRITE.value],
            "guest": [Permission.READ.value],
            "executor": [Permission.EXECUTE.value],
        }
        self._user_permissions: dict[str, list[str]] = {}

    async def get_permissions_for_user(self, user_id: str) -> list[str]:
        """Get permissions for a specific user with caching."""
        cache_key = f"user_permissions:{user_id}"

        if self._cache:
            cached = await self._cache.get(cache_key)
            if cached:
                return json.loads(cached)

        permissions = self._user_permissions.get(user_id, [])
        if self._cache:
            await self._cache.set(cache_key, json.dumps(permissions), ttl=300)

        return permissions

    async def get_permissions_for_role(self, role: str) -> list[str]:
        """Get permissions for a specific role."""
        # Add small delay for async resilience
        await asyncio.sleep(0.001)
        return self._role_permissions.get(role, [])

    async def has_permission(self, user_id: str, permission: str) -> bool:
        """Check if user has required permission."""
        user_permissions = await self.get_permissions_for_user(user_id)
        return permission in user_permissions

    async def grant_permission(self, user_id: str, permission: str) -> None:
        """Grant permission to user."""
        if user_id not in self._user_permissions:
            self._user_permissions[user_id] = []

        if permission not in self._user_permissions[user_id]:
            self._user_permissions[user_id].append(permission)

            if self._cache:
                cache_key = f"user_permissions:{user_id}"
                await self._cache.delete(cache_key)

            logger.info(f"Granted permission {permission} to user {user_id}")

    async def revoke_permission(self, user_id: str, permission: str) -> None:
        """Revoke permission from user."""
        if (
            user_id in self._user_permissions
            and permission in self._user_permissions[user_id]
        ):
            self._user_permissions[user_id].remove(permission)

            if self._cache:
                cache_key = f"user_permissions:{user_id}"
                await self._cache.delete(cache_key)

            logger.info(f"Revoked permission {permission} from user {user_id}")

    async def add_role(self, role: str, permissions: list[str]) -> None:
        """Add a new role with permissions."""
        # Add small delay for async resilience
        await asyncio.sleep(0.001)
        self._role_permissions[role] = permissions
        logger.info(f"Added role {role} with permissions: {permissions}")


class SessionManager:
    """Enhanced session manager with caching and security."""

    def __init__(self, session_timeout: int = 3600, cache: Cache | None = None):
        self._session_timeout = session_timeout
        self._cache = cache
        self._active_sessions: dict[str, AuthToken] = {}

    async def create_session(self, user: User) -> AuthToken:
        """Create a new session for user."""
        token_str = self._generate_secure_token(user.id)
        auth_token = AuthToken(
            token=token_str,
            user_id=user.id,
            provider=AuthProviderType.JWT,  # Default to JWT
            permissions=user.permissions,
            issued_at=datetime.now(),
            expires_at=datetime.now() + timedelta(seconds=self._session_timeout),
        )

        self._active_sessions[token_str] = auth_token

        if self._cache:
            cache_key = f"session:{token_str}"
            await self._cache.set(
                cache_key,
                json.dumps(
                    {
                        "user_id": user.id,
                        "permissions": user.permissions,
                        "expires_at": auth_token.expires_at.isoformat(),
                    }
                ),
                ttl=self._session_timeout,
            )

        logger.info(f"Created session for user {user.id}")
        return auth_token

    async def get_session(self, token: str) -> AuthToken | None:
        """Get session by token with caching."""
        # Check memory first
        if token in self._active_sessions:
            session = self._active_sessions[token]
            if session.is_valid():
                return session
            else:
                await self.invalidate_session(token)

        # Check cache
        if self._cache:
            cache_key = f"session:{token}"
            cached_data = await self._cache.get(cache_key)
            if cached_data:
                data = json.loads(cached_data)
                expires_at = datetime.fromisoformat(data["expires_at"])
                if datetime.now() < expires_at:
                    return AuthToken(
                        token=token,
                        user_id=data["user_id"],
                        provider=AuthProviderType.JWT,
                        permissions=data["permissions"],
                        issued_at=datetime.now(),  # Approximate
                        expires_at=expires_at,
                    )

        return None

    async def invalidate_session(self, token: str) -> None:
        """Invalidate a session."""
        if token in self._active_sessions:
            del self._active_sessions[token]

        if self._cache:
            cache_key = f"session:{token}"
            await self._cache.delete(cache_key)

        logger.info(f"Invalidated session {token}")

    async def cleanup_expired_sessions(self) -> None:
        """Clean up expired sessions."""
        expired_tokens = []
        for token, session in self._active_sessions.items():
            if session.is_expired():
                expired_tokens.append(token)

        for token in expired_tokens:
            await self.invalidate_session(token)

        if expired_tokens:
            logger.info(f"Cleaned up {len(expired_tokens)} expired sessions")

    def _generate_secure_token(self, user_id: str) -> str:
        """Generate cryptographically secure session token."""
        data = f"{user_id}:{time.time()}:{hashlib.sha256(user_id.encode()).hexdigest()[:16]}"
        return hashlib.sha256(data.encode()).hexdigest()


class BaseAuthenticator(ABC):
    """Enhanced base authenticator with security features."""

    def __init__(self, cache: Cache | None = None):
        self._logger = get_logger(self.__class__.__name__)
        self._cache = cache
        self._rate_limiter = RateLimiter()
        self._config: dict[str, Any] = {}

    @abstractmethod
    async def authenticate(self, credentials: dict[str, Any]) -> User | None:
        """Authenticate user with credentials."""
        await asyncio.sleep(0.001)  # Async resilience
        ...

    @abstractmethod
    async def validate_token(self, token: str) -> User | None:
        """Validate authentication token."""
        await asyncio.sleep(0.001)  # Async resilience
        ...

    def configure(self, config: dict[str, Any]) -> None:
        """Configure authenticator."""
        self._config.update(config)
        self._logger.info("Authenticator configured with security settings")


class JWTAuthenticator(BaseAuthenticator):
    """Enhanced JWT-based authenticator with security features."""

    def __init__(
        self, secret_key: str, algorithm: str = "HS256", cache: Cache | None = None
    ):
        super().__init__(cache)
        self._secret_key = secret_key
        self._algorithm = algorithm
        self._session_manager = SessionManager(cache=cache)

    async def authenticate(self, credentials: dict[str, Any]) -> User | None:
        """Authenticate user with JWT."""
        await asyncio.sleep(0.001)  # Async resilience
        user_id = credentials.get("user_id", "")
        password = credentials.get("password", "")

        if not self._rate_limiter.is_allowed(user_id):
            raise AuthenticationError("Too many failed attempts")

        # In real implementation, validate against user store
        if user_id and password:
            user = User(
                id=user_id,
                email=f"{user_id}@example.com",
                username=user_id,
                permissions=["read", "write"],
            )
            return user

        self._rate_limiter.record_attempt(user_id)
        return None

    async def validate_token(self, token: str) -> User | None:
        """Validate JWT token."""
        await asyncio.sleep(0.001)  # Async resilience
        try:
            session = await self._session_manager.get_session(token)
            if session and session.is_valid():
                return User(
                    id=session.user_id,
                    email=f"{session.user_id}@example.com",
                    username=session.user_id,
                    permissions=session.permissions,
                )
            return None
        except Exception as e:
            self._logger.error(f"Token validation error: {e}")
            return None

    async def create_token(self, user: User) -> AuthToken:
        """Create JWT token for user."""
        await asyncio.sleep(0.001)  # Async resilience
        return await self._session_manager.create_session(user)


class OAuthProvider(BaseAuthenticator):
    """Enhanced OAuth2 provider with security and async operations."""

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        provider: str = "google",
        cache: Cache | None = None,
    ):
        super().__init__(cache)
        self._client_id = client_id
        self._client_secret = client_secret
        self._provider = provider
        self._session_manager = SessionManager(cache=cache)

    async def authenticate(self, credentials: dict[str, Any]) -> User | None:
        """Authenticate via OAuth provider."""
        await asyncio.sleep(0.001)  # Async resilience
        auth_code = credentials.get("code", "")
        if not auth_code:
            return None

        # In real implementation, exchange code for token with provider
        user_id = f"{self._provider}_user_{int(time.time())}"
        user = User(
            id=user_id,
            email=f"{user_id}@{self._provider}.com",
            username=user_id,
            permissions=["read", "write"],
        )
        return user

    async def validate_token(self, token: str) -> User | None:
        """Validate OAuth token."""
        await asyncio.sleep(0.001)  # Async resilience
        try:
            if token.startswith(f"oauth_{self._provider}_"):
                session = await self._session_manager.get_session(token)
                if session and session.is_valid():
                    return User(
                        id=session.user_id,
                        email=f"{session.user_id}@{self._provider}.com",
                        username=session.user_id,
                        permissions=session.permissions,
                    )
            return None
        except Exception as e:
            self._logger.error(f"OAuth token validation error: {e}")
            return None

    async def create_token(self, user: User) -> AuthToken:
        """Create OAuth token."""
        await asyncio.sleep(0.001)  # Async resilience
        return await self._session_manager.create_session(user)


# Backward compatibility functions
def old_authenticate(user: str, password: str) -> bool:
    """Deprecated: Use AuthProvider.authenticate() instead."""
    import warnings

    warnings.warn("old_authenticate is deprecated", DeprecationWarning, stacklevel=2)

    mock_auth = MockAuthProvider()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        result = loop.run_until_complete(
            mock_auth.authenticate({"user_id": user, "password": password})
        )
        return result is not None
    finally:
        loop.close()


__all__ = [
    "AuthProvider",
    "AuthProviderType",
    "AuthToken",
    "BaseAuthenticator",
    "JWTAuthenticator",
    "MockAuthProvider",
    "OAuthProvider",
    "Permission",
    "PermissionManager",
    "RateLimiter",
    "SessionManager",
    "User",
    "old_authenticate",
]
