"""
GraphQL directives for performance optimization and security.

Custom directives to achieve sub-100ms response times with:
- Rate limiting
- Caching
- Authentication
- Field-level permissions
- Query complexity analysis

Auto-fixed by comprehensive_init_fixer.py
"""

from __future__ import annotations

import functools
import logging
import time
from collections.abc import Callable
from threading import Lock

import strawberry
from strawberry.schema_directive import Location
import Any
import Exception
import PermissionError
import ValueError
import admin_override
import any
import arg
import args
import bool
import cached_result
import dict
import e
import float
import getattr
import hasattr
import hash
import int
import kwargs
import len
import level
import list
import max_calls
import name
import owner_field
import resolver
import role
import roles
import self
import str
import timestamp
import ttl
import tuple
import warn_threshold
import window

# Define package metadata
__version__: str = "1.0.0"
__author__: str = "zeta_vn team"
__layer__: str = "application"
__clean_architecture__: bool = True

# Configure logger for the directives package using a centralized setup function
def _setup_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """
    Set up a logger with standardized configuration.

    Args:
        name (str): The name of the logger.
        level (int): The logging level. Defaults to logging.INFO.

    Returns:
        logging.Logger: The configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger

# Initialize the package logger
logger: logging.Logger = _setup_logger(__name__)


@strawberry.schema_directive(locations=[Location.FIELD_DEFINITION])
class cached:
    """Cache directive to improve response times.

    Usage:
        @strawberry.field
        @cached(ttl=300)
        async def expensive_field(self) -> str:
            return await slow_operation()
    """

    ttl: int = 300  # Cache TTL in seconds

    def __init__(self, ttl: int = 300) -> None:
        """Initialize the cached directive.

        Args:
            ttl (int): Cache TTL in seconds. Defaults to 300.
        """
        if ttl <= 0:
            raise ValueError("TTL must be a positive integer.")
        self.ttl = ttl
        self._cache: dict[str, tuple[Any, float]] = {}
        self._lock = Lock()

    def __call__(self, resolver: Callable) -> Callable:
        """Apply caching to field resolver.

        Args:
            resolver: Field resolver function.

        Returns:
            Cached resolver.
        """
        @functools.wraps(resolver)
        async def cached_resolver(*args, **kwargs) -> Any:
            cache_key = f"{resolver.__name__}:{hash(str(args) + str(kwargs))}"

            # Thread-safe cache access
            with self._lock:
                if cache_key in self._cache:
                    cached_result, timestamp = self._cache[cache_key]
                    if time.time() - timestamp < self.ttl:
                        logger.debug(f"Cache hit: {cache_key}")
                        return cached_result

            result = await resolver(*args, **kwargs)

            with self._lock:
                self._cache[cache_key] = (result, time.time())
                # Optional: Add cache eviction for old entries

            logger.debug(f"Cache miss: {cache_key}, result cached")
            return result

        return cached_resolver


@strawberry.schema_directive(locations=[Location.FIELD_DEFINITION])
class auth:
    """Authentication directive for field-level security.

    Usage:
        @strawberry.field
        @auth(required=True)
        async def protected_field(self, info) -> str:
            return "secret data"
    """

    required: bool = True
    roles: list[str] = strawberry.field(default_factory=list)

    def __call__(self, resolver: Callable) -> Callable:
        """Apply authentication check to field.

        Args:
            resolver: Field resolver function.

        Returns:
            Protected resolver.
        """
        @functools.wraps(resolver)
        async def auth_resolver(*args, **kwargs) -> Any:
            info = None
            for arg in args:
                if hasattr(arg, "context"):
                    info = arg
                    break
            if not info:
                raise PermissionError("GraphQL info not found")
            current_user = info.context.get("current_user")
            if self.required and not current_user:
                raise PermissionError("Authentication required")
            if self.roles and current_user:
                user_roles = getattr(current_user, "roles", [])
                if not any(role in user_roles for role in self.roles):
                    raise PermissionError(f"Required roles: {self.roles}")
            return await resolver(*args, **kwargs)

        return auth_resolver


@strawberry.schema_directive(locations=[Location.FIELD_DEFINITION])
class rate_limit:
    """Rate limiting directive to prevent abuse.

    Usage:
        @strawberry.field
        @rate_limit(max_calls=10, window=60)
        async def expensive_operation(self) -> str:
            return await cpu_intensive_task()
    """

    max_calls: int = 100
    window: int = 60  # Time window in seconds

    def __init__(self, max_calls: int = 100, window: int = 60) -> None:
        """Initialize the rate_limit directive.

        Args:
            max_calls (int): Maximum calls allowed. Defaults to 100.
            window (int): Time window in seconds. Defaults to 60.
        """
        if max_calls <= 0 or window <= 0:
            raise ValueError("max_calls and window must be positive integers.")
        self.max_calls = max_calls
        self.window = window
        self._call_history: dict[str, list[float]] = {}
        self._lock = Lock()

    def __call__(self, resolver: Callable) -> Callable:
        """Apply rate limiting to field.

        Args:
            resolver: Field resolver function.

        Returns:
            Rate limited resolver.
        """
        @functools.wraps(resolver)
        async def rate_limited_resolver(*args, **kwargs) -> Any:
            user_id = "anonymous"
            for arg in args:
                if hasattr(arg, "context"):
                    current_user = arg.context.get("current_user")
                    if current_user:
                        user_id = getattr(current_user, "id", "anonymous")
                    break
            rate_key = f"{resolver.__name__}:{user_id}"
            current_time = time.time()
            with self._lock:
                if rate_key in self._call_history:
                    self._call_history[rate_key] = [
                        timestamp
                        for timestamp in self._call_history[rate_key]
                        if current_time - timestamp < self.window
                    ]
                else:
                    self._call_history[rate_key] = []
                if len(self._call_history[rate_key]) >= self.max_calls:
                    raise ValueError(
                        f"Rate limit exceeded: {self.max_calls} calls per {self.window}s"
                    )
                self._call_history[rate_key].append(current_time)
            return await resolver(*args, **kwargs)

        return rate_limited_resolver


@strawberry.schema_directive(locations=[Location.FIELD_DEFINITION])
class timed:
    """Performance monitoring directive.

    Usage:
        @strawberry.field
        @timed(warn_threshold=100)
        async def monitored_field(self) -> str:
            return await operation()
    """

    warn_threshold: int = 100  # Warning threshold in milliseconds

    def __call__(self, resolver: Callable) -> Callable:
        """Apply performance monitoring to field.

        Args:
            resolver: Field resolver function.

        Returns:
            Monitored resolver.
        """
        @functools.wraps(resolver)
        async def timed_resolver(*args, **kwargs) -> Any:
            start_time = time.time()
            try:
                result = await resolver(*args, **kwargs)
                execution_time = (time.time() - start_time) * 1000  # Convert to ms
                if execution_time > self.warn_threshold:
                    logger.warning(
                        f"Slow resolver: {resolver.__name__} took {execution_time:.2f}ms"
                    )
                else:
                    logger.debug(
                        f"Resolver timing: {resolver.__name__} took {execution_time:.2f}ms"
                    )
                return result
            except Exception as e:
                execution_time = (time.time() - start_time) * 1000
                logger.error(
                    f"Resolver error: {resolver.__name__} failed after {execution_time:.2f}ms: {e}"
                )
                raise

        return timed_resolver


@strawberry.schema_directive(locations=[Location.FIELD_DEFINITION])
class owner_only:
    """Ownership directive for resource access control.

    Usage:
        @strawberry.field
        @owner_only(owner_field="owner_id")
        async def sensitive_data(self) -> str:
            return self.private_info
    """

    owner_field: str = "owner_id"
    admin_override: bool = True

    def __call__(self, resolver: Callable) -> Callable:
        """Apply ownership check to field.

        Args:
            resolver: Field resolver function.

        Returns:
            Protected resolver.
        """
        @functools.wraps(resolver)
        async def owner_resolver(*args, **kwargs) -> Any:
            info = None
            resource = None
            for arg in args:
                if hasattr(arg, "context"):
                    info = arg
                elif hasattr(arg, self.owner_field):
                    resource = arg
            if not info or not resource:
                raise PermissionError("Unable to verify ownership")
            current_user = info.context.get("current_user")
            if not current_user:
                raise PermissionError("Authentication required")
            resource_owner = getattr(resource, self.owner_field, None)
            if resource_owner != current_user.id:
                if not (
                    self.admin_override and getattr(current_user, "is_admin", False)
                ):
                    raise PermissionError("Access denied: not resource owner")
            return await resolver(*args, **kwargs)

        return owner_resolver


def cache_field(ttl: int = 300) -> cached:
    """Shorthand for @cached directive."""
    return cached(ttl=ttl)


def require_auth(roles: list[str] | None = None) -> auth:
    """Shorthand for @auth directive."""
    return auth(required=True, roles=roles or [])


def limit_calls(max_calls: int = 100, window: int = 60) -> rate_limit:
    """Shorthand for @rate_limit directive."""
    return rate_limit(max_calls=max_calls, window=window)


def monitor_performance(warn_threshold: int = 100) -> timed:
    """Shorthand for @timed directive."""
    return timed(warn_threshold=warn_threshold)


def require_ownership(owner_field: str = "owner_id", admin_override: bool = True) -> owner_only:
    """Shorthand for @owner_only directive."""
    return owner_only(owner_field=owner_field, admin_override=admin_override)


__all__: list[str] = [
    "auth",
    "cache_field",
    "cached",
    "limit_calls",
    "monitor_performance",
    "owner_only",
    "rate_limit",
    "require_auth",
    "require_ownership",
    "timed",
]
