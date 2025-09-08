from __future__ import annotations

import asyncio
import hashlib
import json
import logging
from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator
from datetime import datetime, timedelta
from typing import Any
import Exception
import attempt
import bool
import cache_ttl
import callable
import concurrency
import dict
import e
import enable_cache
import float
import int
import isinstance
import len
import list
import max_retries
import min
import name
import param_generator
import param_list
import params
import progress_callback
import r
import range
import rate_limit
import req_time
import retry_delay
import self
import sorted
import str
import use_cache

"""
Base Data Fetcher - Integration Layer
Provides the foundation for all data fetching operations with:
- Async data retrieval patterns
- Caching and performance optimization
- Error handling and retry logic
- Rate limiting and quota management
- Progress tracking and monitoring
"""
logger = logging.getLogger(__name__)


class FetcherError(Exception):
    """Base exception for fetcher errors."""


class DataValidationError(FetcherError):
    """Raised when fetched data doesn't pass validation."""


class QuotaExceededError(FetcherError):
    """Raised when data source quota is exceeded."""


class BaseFetcher(ABC):
    """
    Base class for all data fetchers.
    Provides common functionality for:
    - Async data retrieval
    - Result caching
    - Error handling and retries
    - Progress tracking
    - Rate limiting
    """

    def __init__(
        self,
        name: str,
        cache_ttl: int = 3600,  # 1 hour default
        max_retries: int = 3,
        retry_delay: float = 1.0,
        rate_limit: int = 100,  # requests per minute
        enable_cache: bool = True,
    ):
        self.name = name
        self.cache_ttl = cache_ttl
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.rate_limit = rate_limit
        self.enable_cache = enable_cache
        self._cache: dict[str, dict[str, Any]] = {}
        self._request_times: list[datetime] = []
        self.stats = {
            "requests_made": 0,
            "cache_hits": 0,
            "cache_misses": 0,
            "errors": 0,
            "total_items_fetched": 0,
        }

    async def __aenter__(self) -> BaseFetcher:
        """Async context manager entry."""
        await self.initialize()
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Async context manager exit."""
        await self.cleanup()

    async def initialize(self) -> None:
        """Initialize the fetcher."""
        logger.info(f"✅ {self.name} fetcher initialized")

    async def cleanup(self) -> None:
        """Clean up resources."""
        logger.info(f"🧹 {self.name} fetcher cleaned up")

    def _generate_cache_key(self, **params: Any) -> str:
        """Generate a cache key from parameters."""
        sorted_params = sorted(params.items())
        key_string = f"{self.name}:{json.dumps(sorted_params, sort_keys=True)}"
        return hashlib.md5(key_string.encode()).hexdigest()

    def _is_cache_valid(self, cache_entry: dict[str, Any]) -> bool:
        """Check if cache entry is still valid."""
        if not self.enable_cache:
            return False
        cached_at = datetime.fromisoformat(cache_entry["cached_at"])
        expiry_time = cached_at + timedelta(seconds=self.cache_ttl)
        return datetime.now() < expiry_time

    async def _check_rate_limit(self) -> None:
        """Check and enforce rate limiting."""
        now = datetime.now()
        self._request_times = [
            req_time
            for req_time in self._request_times
            if now - req_time < timedelta(minutes=1)
        ]
        if len(self._request_times) >= self.rate_limit:
            oldest_request = min(self._request_times)
            wait_time = 60 - (now - oldest_request).total_seconds()
            if wait_time > 0:
                logger.warning(
                    f"⏳ Rate limit reached for {self.name}, waiting {wait_time:.1f}s"
                )
                await asyncio.sleep(wait_time)
        self._request_times.append(now)

    @abstractmethod
    async def _fetch_data(self, **params: Any) -> Any:
        """
        Implement actual data fetching logic.
        This method should be overridden by subclasses to provide
        specific data fetching functionality.
        """

    @abstractmethod
    def _validate_data(self, data: Any) -> bool:
        """
        Validate fetched data.
        Should return True if data is valid, False otherwise.
        """

    async def fetch(self, use_cache: bool = True, **params: Any) -> Any:
        """
        Fetch data with caching and error handling.
        Args:
            use_cache: Whether to use cached results
            **params: Parameters for data fetching
        Returns:
            Fetched data
        Raises:
            FetcherError: If fetching fails after retries
        """
        cache_key = self._generate_cache_key(**params)
        if use_cache and self.enable_cache and cache_key in self._cache:
            cache_entry = self._cache[cache_key]
            if self._is_cache_valid(cache_entry):
                self.stats["cache_hits"] += 1
                logger.debug(f"💾 Cache hit for {self.name}: {cache_key[:8]}...")
                return cache_entry["data"]
        self.stats["cache_misses"] += 1
        for attempt in range(self.max_retries + 1):
            try:
                await self._check_rate_limit()
                logger.debug(
                    f"🔄 Fetching data for {self.name} (attempt {attempt + 1})"
                )
                data = await self._fetch_data(**params)
                if not self._validate_data(data):
                    raise DataValidationError("Fetched data failed validation")
                if self.enable_cache:
                    self._cache[cache_key] = {
                        "data": data,
                        "cached_at": datetime.now().isoformat(),
                        "params": params,
                    }
                self.stats["requests_made"] += 1
                if isinstance(data, list):
                    self.stats["total_items_fetched"] += len(data)
                else:
                    self.stats["total_items_fetched"] += 1
                logger.debug(f"✅ Successfully fetched data for {self.name}")
                return data
            except Exception as e:
                logger.warning(f"⚠️ Attempt {attempt + 1} failed for {self.name}: {e}")
                if attempt < self.max_retries:
                    delay = self.retry_delay * (2**attempt)  # Exponential backoff
                    await asyncio.sleep(delay)
                    continue
                self.stats["errors"] += 1
                raise FetcherError(
                    f"Failed to fetch data after {self.max_retries + 1} attempts: {e}"
                ) from e

    async def fetch_batch(
        self,
        param_list: list[dict[str, Any]],
        concurrency: int = 5,
        use_cache: bool = True,
        progress_callback: callable | None = None,
    ) -> list[Any]:
        """
        Fetch multiple data items concurrently.
        Args:
            param_list: List of parameter dictionaries for each fetch
            concurrency: Number of concurrent fetches
            use_cache: Whether to use cached results
            progress_callback: Optional callback for progress updates
        Returns:
            List of fetched results
        """
        semaphore = asyncio.Semaphore(concurrency)
        results = []
        completed = 0

        async def fetch_with_semaphore(params: dict[str, Any]) -> Any:
            nonlocal completed
            async with semaphore:
                try:
                    result = await self.fetch(use_cache=use_cache, **params)
                    completed += 1
                    if progress_callback:
                        progress_callback(completed, len(param_list), params)
                    return result
                except Exception as e:
                    logger.error(f"❌ Batch fetch failed for {params}: {e}")
                    return None

        tasks = [fetch_with_semaphore(params) for params in param_list]
        logger.info(
            f"🚀 Starting batch fetch: {len(param_list)} items, concurrency={concurrency}"
        )
        results = await asyncio.gather(*tasks, return_exceptions=True)
        successful_results = [
            r for r in results if r is not None and not isinstance(r, Exception)
        ]
        logger.info(
            f"✅ Batch fetch completed: {len(successful_results)}/{len(param_list)} successful"
        )
        return successful_results

    async def fetch_stream(
        self,
        param_generator: AsyncGenerator[dict[str, Any], None],
        use_cache: bool = True,
    ) -> AsyncGenerator[Any, None]:
        """
        Stream data fetching for large datasets.
        Args:
            param_generator: Async generator yielding fetch parameters
            use_cache: Whether to use cached results
        Yields:
            Fetched data items
        """
        async for params in param_generator:
            try:
                data = await self.fetch(use_cache=use_cache, **params)
                yield data
            except Exception as e:
                logger.error(f"❌ Stream fetch failed for {params}: {e}")
                continue

    def clear_cache(self) -> None:
        """Clear all cached data."""
        cache_size = len(self._cache)
        self._cache.clear()
        logger.info(f"🗑️ Cleared {cache_size} cache entries for {self.name}")

    def get_stats(self) -> dict[str, Any]:
        """Get fetcher statistics."""
        cache_hit_rate = (
            self.stats["cache_hits"]
            / (self.stats["cache_hits"] + self.stats["cache_misses"])
            if (self.stats["cache_hits"] + self.stats["cache_misses"]) > 0
            else 0.0
        )
        return {
            **self.stats,
            "cache_hit_rate": cache_hit_rate,
            "cache_size": len(self._cache),
            "name": self.name,
        }


__all__ = [
    "BaseFetcher",
    "DataValidationError",
    "FetcherError",
    "QuotaExceededError",
    "cache_entry",
    "cache_hit_rate",
    "cache_key",
    "cache_size",
    "cached_at",
    "clear_cache",
    "completed",
    "data",
    "delay",
    "expiry_time",
    "get_stats",
    "key_string",
    "logger",
    "now",
    "oldest_request",
    "result",
    "results",
    "semaphore",
    "sorted_params",
    "successful_results",
    "tasks",
    "wait_time",
]
