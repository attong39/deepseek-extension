from __future__ import annotations

import logging
import time
from contextlib import asynccontextmanager
from typing import Any

from app.api.graphql.core.dataloader import get_dataloader_registry
from strawberry.extensions import SchemaExtension
from strawberry.schema import ExecutionResult
import ValueError
import bool
import cache_ttl
import cached_result
import complexity
import dict
import enable_caching
import error
import execution_time
import float
import hash
import info
import int
import len
import list
import max_requests
import query
import schema
import self
import sorted
import str
import super
import timestamp
import tuple
import variables
import window

"""GraphQL performance middleware để achieve sub-100ms response times.
Comprehensive performance monitoring, caching, và optimization middleware
để ensure target performance metrics.
"""
logger = logging.getLogger(__name__)


class PerformanceMetrics:
    """Performance metrics collector để track GraphQL performance."""

    def __init__(self) -> None:
        """Initialize metrics collector."""
        self.reset()

    def reset(self) -> None:
        """Reset all metrics."""
        self.query_count = 0
        self.total_execution_time = 0.0
        self.slow_queries = 0
        self.cache_hits = 0
        self.cache_misses = 0
        self.error_count = 0
        self.parse_time = 0.0
        self.validate_time = 0.0
        self.execute_time = 0.0
        self.max_complexity = 0
        self.avg_complexity = 0.0

    def record_query(
        self,
        execution_time: float,
        parse_time: float = 0.0,
        validate_time: float = 0.0,
        execute_time: float = 0.0,
        complexity: int = 0,
        had_errors: bool = False,
    ) -> None:
        """Record query execution metrics.
        Args:
            execution_time: Total execution time in seconds
            parse_time: Parse phase time
            validate_time: Validation phase time
            execute_time: Execution phase time
            complexity: Query complexity score
            had_errors: Whether query had errors
        """
        self.query_count += 1
        self.total_execution_time += execution_time
        if execution_time > 0.1:  # > 100ms threshold
            self.slow_queries += 1
        if had_errors:
            self.error_count += 1
        self.parse_time += parse_time
        self.validate_time += validate_time
        self.execute_time += execute_time
        if complexity > self.max_complexity:
            self.max_complexity = complexity
        if self.query_count > 0:
            self.avg_complexity = (
                self.avg_complexity * (self.query_count - 1) + complexity
            ) / self.query_count

    def get_summary(self) -> dict[str, Any]:
        """Get performance summary.
        Returns:
            Performance metrics dictionary
        """
        avg_time = (
            self.total_execution_time / self.query_count if self.query_count > 0 else 0
        )
        slow_query_rate = (
            self.slow_queries / self.query_count if self.query_count > 0 else 0
        )
        error_rate = self.error_count / self.query_count if self.query_count > 0 else 0
        return {
            "query_count": self.query_count,
            "total_execution_time": self.total_execution_time,
            "avg_execution_time": avg_time,
            "slow_queries": self.slow_queries,
            "slow_query_rate": slow_query_rate,
            "error_count": self.error_count,
            "error_rate": error_rate,
            "max_complexity": self.max_complexity,
            "avg_complexity": self.avg_complexity,
            "timing_breakdown": {
                "parse": self.parse_time,
                "validate": self.validate_time,
                "execute": self.execute_time,
            },
        }


performance_metrics = PerformanceMetrics()


class PerformanceMonitoringExtension(SchemaExtension):
    """Schema extension để monitor performance và log slow queries."""

    def __init__(self) -> None:
        """Initialize performance monitoring."""
        super().__init__()
        self._start_time = 0.0
        self._phase_times: dict[str, float] = {}

    @asynccontextmanager
    async def request_lifecycle(self, request: Any, info: Any) -> Any:
        """Monitor entire request lifecycle.
        Args:
            request: GraphQL request
            info: Request info
        """
        self._start_time = time.time()
        registry = get_dataloader_registry()
        try:
            yield
        finally:
            registry.cleanup()
            total_time = time.time() - self._start_time
            dataloader_stats = registry.get_aggregate_stats()
            logger.info(
                f"GraphQL request completed in {total_time * 1000:.2f}ms, "
                f"DataLoader stats: {dataloader_stats['aggregate']}"
            )

    async def on_parsing_start(self) -> None:
        """Track parsing start."""
        self._phase_times["parse_start"] = time.time()

    async def on_parsing_end(self) -> None:
        """Track parsing end."""
        parse_time = time.time() - self._phase_times["parse_start"]
        self._phase_times["parse"] = parse_time
        if parse_time > 0.01:  # > 10ms warning
            logger.warning(f"Slow GraphQL parsing: {parse_time * 1000:.2f}ms")

    async def on_validation_start(self) -> None:
        """Track validation start."""
        self._phase_times["validate_start"] = time.time()

    async def on_validation_end(self) -> None:
        """Track validation end."""
        validate_time = time.time() - self._phase_times["validate_start"]
        self._phase_times["validate"] = validate_time
        if validate_time > 0.01:  # > 10ms warning
            logger.warning(f"Slow GraphQL validation: {validate_time * 1000:.2f}ms")

    async def on_execution_start(self) -> None:
        """Track execution start."""
        self._phase_times["execute_start"] = time.time()

    async def on_execution_end(self, result: ExecutionResult) -> None:
        """Track execution end và record metrics.
        Args:
            result: GraphQL execution result
        """
        execute_time = time.time() - self._phase_times["execute_start"]
        self._phase_times["execute"] = execute_time
        total_time = time.time() - self._start_time
        had_errors = result.errors is not None and len(result.errors) > 0
        performance_metrics.record_query(
            execution_time=total_time,
            parse_time=self._phase_times.get("parse", 0.0),
            validate_time=self._phase_times.get("validate", 0.0),
            execute_time=execute_time,
            had_errors=had_errors,
        )
        if total_time > 0.1:  # > 100ms
            logger.warning(
                f"Slow GraphQL query: {total_time * 1000:.2f}ms total "
                f"(parse: {self._phase_times.get('parse', 0) * 1000:.2f}ms, "
                f"validate: {self._phase_times.get('validate', 0) * 1000:.2f}ms, "
                f"execute: {execute_time * 1000:.2f}ms)"
            )
        if had_errors:
            error_messages = [str(error) for error in result.errors]
            logger.error(f"GraphQL errors: {error_messages}")


class CachingExtension(SchemaExtension):
    """Schema extension để implement query-level caching."""

    def __init__(self, cache_ttl: int = 300) -> None:
        """Initialize caching extension.
        Args:
            cache_ttl: Default cache TTL trong seconds
        """
        super().__init__()
        self._cache_ttl = cache_ttl
        self._query_cache: dict[str, tuple[Any, float]] = {}

    def _generate_cache_key(self, query: str, variables: dict[str, Any] | None) -> str:
        """Generate cache key for query + variables.
        Args:
            query: GraphQL query string
            variables: Query variables
        Returns:
            Cache key string
        """
        variables_str = str(sorted(variables.items())) if variables else ""
        return f"{hash(query)}:{hash(variables_str)}"

    @asynccontextmanager
    async def request_lifecycle(self, request: Any, info: Any) -> Any:
        """Implement query-level caching.
        Args:
            request: GraphQL request
            info: Request info
        """
        cache_key = self._generate_cache_key(request.query, request.variables or {})
        current_time = time.time()
        if cache_key in self._query_cache:
            cached_result, timestamp = self._query_cache[cache_key]
            if current_time - timestamp < self._cache_ttl:
                logger.debug(f"Query cache hit: {cache_key[:20]}...")
                performance_metrics.cache_hits += 1
                yield cached_result
                return
        performance_metrics.cache_misses += 1
        logger.debug(f"Query cache miss: {cache_key[:20]}...")
        result = yield
        if not (result.errors and len(result.errors) > 0):
            self._query_cache[cache_key] = (result, current_time)
            logger.debug(f"Query result cached: {cache_key[:20]}...")

    def clear_cache(self) -> None:
        """Clear query cache."""
        self._query_cache.clear()
        logger.info("Query cache cleared")

    def get_cache_stats(self) -> dict[str, Any]:
        """Get cache statistics.
        Returns:
            Cache stats dictionary
        """
        return {
            "cache_size": len(self._query_cache),
            "cache_hits": performance_metrics.cache_hits,
            "cache_misses": performance_metrics.cache_misses,
            "hit_rate": (
                performance_metrics.cache_hits
                / (performance_metrics.cache_hits + performance_metrics.cache_misses)
                if (performance_metrics.cache_hits + performance_metrics.cache_misses)
                > 0
                else 0
            ),
        }


class RateLimitingExtension(SchemaExtension):
    """Schema extension để implement rate limiting."""

    def __init__(self, max_requests: int = 100, window: int = 60) -> None:
        """Initialize rate limiting.
        Args:
            max_requests: Maximum requests per window
            window: Time window trong seconds
        """
        super().__init__()
        self._max_requests = max_requests
        self._window = window
        self._request_history: dict[str, list[float]] = {}

    def _get_client_id(self, info: Any) -> str:
        """Extract client identifier từ request.
        Args:
            info: Request info
        Returns:
            Client identifier
        """
        current_user = info.context.get("current_user")
        if current_user:
            return f"user:{current_user.id}"
        request = info.context.get("request")
        if request:
            client_ip = request.client.host if request.client else "unknown"
            return f"ip:{client_ip}"
        return "anonymous"

    @asynccontextmanager
    async def request_lifecycle(self, request: Any, info: Any) -> Any:
        """Implement rate limiting check.
        Args:
            request: GraphQL request
            info: Request info
        """
        client_id = self._get_client_id(info)
        current_time = time.time()
        if client_id in self._request_history:
            self._request_history[client_id] = [
                timestamp
                for timestamp in self._request_history[client_id]
                if current_time - timestamp < self._window
            ]
        else:
            self._request_history[client_id] = []
        if len(self._request_history[client_id]) >= self._max_requests:
            logger.warning(f"Rate limit exceeded for client: {client_id}")
            raise ValueError(
                f"Rate limit exceeded: {self._max_requests} requests per {self._window}s"
            )
        self._request_history[client_id].append(current_time)
        yield


def create_optimized_schema(schema: Any, enable_caching: bool = True) -> Any:
    """Create schema với performance extensions.
    Args:
        schema: Base GraphQL schema
        enable_caching: Whether to enable query caching
    Returns:
        Schema với performance extensions
    """
    extensions = [
        PerformanceMonitoringExtension(),
        RateLimitingExtension(max_requests=1000, window=60),  # Generous limits
    ]
    if enable_caching:
        extensions.append(CachingExtension(cache_ttl=60))
    schema.extensions = extensions
    return schema


def get_performance_summary() -> dict[str, Any]:
    """Get comprehensive performance summary.
    Returns:
        Performance metrics và cache stats
    """
    return {
        "performance": performance_metrics.get_summary(),
        "dataloader": get_dataloader_registry().get_aggregate_stats(),
        "uptime": time.time(),  # Simple uptime tracking
    }


__all__ = [
    "CachingExtension",
    "PerformanceMetrics",
    "PerformanceMonitoringExtension",
    "RateLimitingExtension",
    "create_optimized_schema",
    "get_performance_summary",
    "performance_metrics",
]
