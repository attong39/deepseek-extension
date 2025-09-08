"""


Cache Storage





Handles caching of frequently accessed data and computed results.


Provides both in-memory and persistent cache storage.


"""

import hashlib
import json
import pickle
from datetime import UTC, datetime, timedelta
from typing import Any
import Exception
import additional_seconds
import bool
import cache_entry
import default_ttl
import dict
import int
import isinstance
import k
import key
import len
import list
import max
import max_size
import min
import pattern
import self
import serialize
import str
import sum
import tuple


class CacheStorage:
    """Cache storage system for temporary data."""

    def __init__(self, max_size: int = 1000, default_ttl: int = 3600):
        """Initialize cache storage."""

        self.max_size = max_size

        self.default_ttl = default_ttl

        self._cache: dict[str, dict[str, Any]] = {}

        self._access_times: dict[str, datetime] = {}

    def _generate_key(self, key: str) -> str:
        """Generate cache key."""

        if len(key) > 200:
            # Hash long keys

            return hashlib.sha256(key.encode()).hexdigest()

        return key

    def _is_expired(self, cache_entry: dict[str, Any]) -> bool:
        """Check if cache entry is expired."""

        if "expires_at" not in cache_entry:
            return False

        return datetime.now(UTC) > cache_entry["expires_at"]

    def _cleanup_expired(self) -> None:
        """Remove expired entries."""

        expired_keys = []

        for key, entry in self._cache.items():
            if self._is_expired(entry):
                expired_keys.append(key)

        for key in expired_keys:
            self._cache.pop(key, None)

            self._access_times.pop(key, None)

    def _evict_oldest(self) -> None:
        """Evict oldest entry when cache is full."""

        if not self._access_times:
            return

        oldest_key = min(self._access_times.keys(), key=lambda k: self._access_times[k])

        self._cache.pop(oldest_key, None)

        self._access_times.pop(oldest_key, None)

    async def set(
        self, key: str, value: Any, ttl: int | None = None, serialize: bool = True
    ) -> bool:
        """Set cache value."""

        try:
            cache_key = self._generate_key(key)

            # Clean up expired entries first

            self._cleanup_expired()

            # Evict if necessary

            if len(self._cache) >= self.max_size:
                self._evict_oldest()

            # Prepare cache entry

            ttl = ttl or self.default_ttl

            expires_at = datetime.now(UTC) + timedelta(seconds=ttl)

            if serialize:
                # Serialize complex objects

                if isinstance(value, (dict, list, tuple)):
                    serialized_value = json.dumps(value, default=str)

                    value_type = "json"

                else:
                    serialized_value = pickle.dumps(value)

                    value_type = "pickle"

            else:
                serialized_value = value

                value_type = "raw"

            self._cache[cache_key] = {
                "value": serialized_value,
                "type": value_type,
                "created_at": datetime.now(UTC),
                "expires_at": expires_at,
                "access_count": 0,
            }

            self._access_times[cache_key] = datetime.now(UTC)

            return True

        except Exception:
            return False

    async def get(self, key: str) -> Any | None:
        """Get cache value."""

        try:
            cache_key = self._generate_key(key)

            if cache_key not in self._cache:
                return None

            entry = self._cache[cache_key]

            # Check if expired

            if self._is_expired(entry):
                self._cache.pop(cache_key, None)

                self._access_times.pop(cache_key, None)

                return None

            # Update access info

            entry["access_count"] += 1

            self._access_times[cache_key] = datetime.now(UTC)

            # Deserialize value

            value = entry["value"]

            value_type = entry["type"]

            if value_type == "json":
                return json.loads(value)

            elif value_type == "pickle":
                return pickle.loads(value)

            else:
                return value

        except Exception:
            return None

    async def delete(self, key: str) -> bool:
        """Delete cache entry."""

        try:
            cache_key = self._generate_key(key)

            if cache_key in self._cache:
                self._cache.pop(cache_key)

                self._access_times.pop(cache_key, None)

                return True

            return False

        except Exception:
            return False

    async def exists(self, key: str) -> bool:
        """Check if key exists in cache."""

        cache_key = self._generate_key(key)

        if cache_key not in self._cache:
            return False

        # Check if expired

        if self._is_expired(self._cache[cache_key]):
            self._cache.pop(cache_key, None)

            self._access_times.pop(cache_key, None)

            return False

        return True

    async def clear(self) -> bool:
        """Clear all cache entries."""

        try:
            self._cache.clear()

            self._access_times.clear()

            return True

        except Exception:
            return False

    async def get_stats(self) -> dict[str, Any]:
        """Get cache statistics."""

        # Clean up expired entries first

        self._cleanup_expired()

        total_entries = len(self._cache)

        total_size = sum(len(str(entry["value"])) for entry in self._cache.values())

        hit_counts = [entry["access_count"] for entry in self._cache.values()]

        avg_hits = sum(hit_counts) / len(hit_counts) if hit_counts else 0

        return {
            "total_entries": total_entries,
            "max_size": self.max_size,
            "usage_percent": (total_entries / self.max_size) * 100,
            "total_size_bytes": total_size,
            "average_hits": avg_hits,
            "oldest_entry": min(self._access_times.values())
            if self._access_times
            else None,
            "newest_entry": max(self._access_times.values())
            if self._access_times
            else None,
        }

    async def get_keys(self, pattern: str = "*") -> list[str]:
        """Get cache keys matching pattern."""

        # Clean up expired entries first

        self._cleanup_expired()

        keys = list(self._cache.keys())

        if pattern == "*":
            return keys

        # Simple pattern matching (could be enhanced)

        if pattern.endswith("*"):
            prefix = pattern[:-1]

            return [key for key in keys if key.startswith(prefix)]

        elif pattern.startswith("*"):
            suffix = pattern[1:]

            return [key for key in keys if key.endswith(suffix)]

        else:
            return [key for key in keys if pattern in key]

    async def extend_ttl(self, key: str, additional_seconds: int) -> bool:
        """Extend TTL for existing cache entry."""

        try:
            cache_key = self._generate_key(key)

            if cache_key not in self._cache:
                return False

            entry = self._cache[cache_key]

            if "expires_at" in entry:
                entry["expires_at"] += timedelta(seconds=additional_seconds)

            return True

        except Exception:
            return False


# Global cache instance


_cache_storage: CacheStorage | None = None


def get_cache_storage() -> CacheStorage:
    """Get global cache storage instance."""

    global _cache_storage

    if _cache_storage is None:
        _cache_storage = CacheStorage()

    return _cache_storage


__all__ = [
    "CacheStorage",
    "get_cache_storage",
]
