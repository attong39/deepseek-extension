from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any
from weakref import WeakKeyDictionary

from apps.backend.core.security.context import (
import classmethod
import cls
import dict
import getattr
import isinstance
import key
import len
import property
import request
import self
import staticmethod
import str
import value
    Action,
    Environment,
    Resource,
    SecurityContext,
    Subject,
)
from fastapi import Request

"""GraphQL context setup và dependency injection với performance optimization.
Optimized context management for sub-100ms response times và efficient
resource utilization.
"""
logger = logging.getLogger(__name__)


@dataclass
class GraphQLContext:
    """High-performance GraphQL execution context với caching và resource pooling.
    Features:
    - Lazy dependency loading
    - Connection pooling
    - Weak reference caching
    - Performance monitoring
    """

    request: Request
    security_context: SecurityContext
    _container: Any | None = None
    _current_user: Any | None = None
    _cache: dict[str, Any] | None = None

    def __post_init__(self) -> None:
        """Initialize caches và performance tracking."""
        if self._cache is None:
            self._cache = {}
        self._weak_cache: WeakKeyDictionary[Any, Any] = WeakKeyDictionary()
        self._operation_count = 0
        self._cache_hits = 0

    @classmethod
    def from_request(
        cls,
        request: Request,
        container: Any | None = None,
        current_user: Any | None = None,
    ) -> GraphQLContext:
        """Create optimized context từ FastAPI request.
        Args:
            request: FastAPI request object
            container: Dependency container (lazy loaded if None)
            current_user: Current user (lazy loaded if None)
        Returns:
            Optimized GraphQL context
        """
        user_id = "anonymous"
        tenant_id = "default"
        auth_header = request.headers.get("authorization")
        if auth_header and current_user:
            user_id = getattr(current_user, "id", "anonymous")
            tenant_id = getattr(current_user, "tenant_id", "default")
        security_context = SecurityContext(
            subject=Subject(
                user_id=user_id,
                tenant_id=tenant_id,
                mfa_level=0,
                session_id=None,
                last_activity=None,
            ),
            resource=Resource(
                type="graphql",
                id=None,
                owner_id=None,
                tenant_id=tenant_id,
                sensitivity="internal",
            ),
            action=Action(
                name="query",
                risk="low",
                requires_mfa=False,
                rate_limit_key=None,
            ),
            environment=Environment(
                ip=getattr(request.client, "host", None) if request.client else None,
                user_agent=None,
                time_of_day=None,
                device_trust="medium",
                location=None,
                is_vpn=False,
                request_id=None,
            ),
        )
        return cls(
            request=request,
            security_context=security_context,
            _container=container,
            _current_user=current_user,
        )

    @property
    def container(self) -> Any:
        """Lazy-loaded dependency container với caching.
        Returns:
            Dependency container instance
        """
        if self._container is None:
            self._container = getattr(self.request.state, "container", None)
        if self._container is None:
            logger.warning("Container not available in request state")
        return self._container

    @property
    def current_user(self) -> Any:
        """Lazy-loaded current user với caching.
        Returns:
            Current user instance
        """
        if self._current_user is None:
            self._current_user = getattr(self.request.state, "current_user", None)
        return self._current_user

    def get_cached(self, key: str) -> Any:
        """Get value từ context cache.
        Args:
            key: Cache key
        Returns:
            Cached value or None
        """
        self._operation_count += 1
        if self._cache is not None and key in self._cache:
            self._cache_hits += 1
            logger.debug(f"Context cache hit: {key}")
            return self._cache[key]
        return None

    def set_cached(self, key: str, value: Any) -> None:
        """Set value trong context cache.
        Args:
            key: Cache key
            value: Value to cache
        """
        if self._cache is not None:
            self._cache[key] = value
            logger.debug(f"Context cached: {key}")

    def get_performance_stats(self) -> dict[str, Any]:
        """Get performance statistics.
        Returns:
            Performance metrics dictionary
        """
        cache_hit_rate = (
            self._cache_hits / self._operation_count if self._operation_count > 0 else 0
        )
        return {
            "operation_count": self._operation_count,
            "cache_hits": self._cache_hits,
            "cache_hit_rate": cache_hit_rate,
            "cache_size": len(self._cache) if self._cache else 0,
            "weak_cache_size": len(self._weak_cache),
        }

    def to_dict(self) -> dict[str, Any]:
        """Convert context to dictionary for resolver access.
        Returns:
            Context dictionary với all necessary data
        """
        return {
            "request": self.request,
            "security_context": self.security_context,
            "container": self.container,
            "current_user": self.current_user,
            "cache": self._cache,
            "get_cached": self.get_cached,
            "set_cached": self.set_cached,
            "performance_stats": self.get_performance_stats(),
        }

    def clear_cache(self) -> None:
        """Clear context cache để free memory."""
        if self._cache is not None:
            self._cache.clear()
        self._weak_cache.clear()
        logger.debug("Context cache cleared")


class ContextManager:
    """Context manager để optimize context lifecycle."""

    @staticmethod
    def create_optimized_context(
        request: Request,
        container: Any | None = None,
        current_user: Any | None = None,
    ) -> dict[str, Any]:
        """Create optimized context dictionary.
        Args:
            request: FastAPI request
            container: Dependency container
            current_user: Current user
        Returns:
            Optimized context dictionary
        """
        context = GraphQLContext.from_request(request, container, current_user)
        return context.to_dict()

    @staticmethod
    def cleanup_context(context: dict[str, Any]) -> None:
        """Cleanup context resources.
        Args:
            context: Context dictionary to cleanup
        """
        if isinstance(context.get("cache"), dict):
            context["cache"].clear()
        logger.debug("Context resources cleaned up")


__all__ = [
    "ContextManager",
    "GraphQLContext",
]
