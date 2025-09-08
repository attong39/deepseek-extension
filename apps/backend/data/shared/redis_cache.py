"""Redis-based cache implementation for ZETA AI application.





This module provides concrete Redis implementation of the cache interface


for improved performance and data persistence across application restarts.


"""

from __future__ import annotations

import hashlib
import json
import logging
import pickle
from contextlib import asynccontextmanager
from typing import Any

import redis.asyncio as redis
from apps.backend.core.interfaces.storage_interfaces import CacheStorageInterface
from redis.exceptions import ConnectionError
import Exception
import UnicodeDecodeError
import agent_id
import amount
import args
import bool
import bytes
import cache_manager
import cached_result
import conversation_id
import default
import default_ttl
import dict
import e
import endpoint
import field
import float
import func
import hits
import input_hash
import int
import isinstance
import key
import key_prefix
import kwargs
import list
import mapping
import max_connections
import misses
import model
import params_hash
import pattern
import query_hash
import redis_client
import redis_url
import result
import self
import sorted
import staticmethod
import str
import tuple
import user_id

# Setup


logger = logging.getLogger(__name__)


class CacheKeyBuilder:
    """Utility for building consistent cache keys."""

    @staticmethod
    def user_session(user_id: str) -> str:
        """Build user session cache key."""

        return f"session:user:{user_id}"

    @staticmethod
    def agent_data(agent_id: str) -> str:
        """Build agent data cache key."""

        return f"agent:data:{agent_id}"

    @staticmethod
    def conversation(conversation_id: str) -> str:
        """Build conversation cache key."""

        return f"conversation:{conversation_id}"

    @staticmethod
    def memory_search(query_hash: str) -> str:
        """Build memory search cache key."""

        return f"memory:search:{query_hash}"

    @staticmethod
    def api_response(endpoint: str, params_hash: str) -> str:
        """Build API response cache key."""

        return f"api:response:{endpoint}:{params_hash}"

    @staticmethod
    def model_output(model: str, input_hash: str) -> str:
        """Build model output cache key."""

        return f"model:output:{model}:{input_hash}"


class RedisCacheManager(CacheStorageInterface):
    """Redis-based cache manager implementing CacheStorageInterface."""

    def __init__(
        self,
        redis_url: str = "redis://localhost:6379/0",
        default_ttl: int = 3600,
        max_connections: int = 20,
    ):
        """Initialize Redis cache manager.





        Args:


            redis_url: Redis connection URL.


            default_ttl: Default time to live in seconds.


            max_connections: Maximum Redis connections.


        """

        self.redis_url = redis_url

        self.default_ttl = default_ttl

        self.max_connections = max_connections

        self._redis: redis.Redis | None = None

        self._connected = False

    async def connect(self) -> None:
        """Connect to Redis."""

        try:
            self._redis = redis.from_url(
                self.redis_url,
                encoding="utf-8",
                decode_responses=False,  # We'll handle encoding ourselves
                max_connections=self.max_connections,
                retry_on_timeout=True,
                socket_connect_timeout=5,
                socket_timeout=5,
            )

            # Test connection

            await self._redis.ping()

            self._connected = True

            logger.info("Cache manager connected to Redis")

        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")

            self._connected = False

            raise

    async def disconnect(self) -> None:
        """Disconnect from Redis."""

        if self._redis:
            await self._redis.close()

            self._connected = False

            logger.info("Cache manager disconnected from Redis")

    @asynccontextmanager
    async def _ensure_connection(self):
        """Ensure Redis connection is active."""

        if not self._connected or not self._redis:
            await self.connect()

        try:
            yield self._redis

        except ConnectionError:
            logger.warning("Redis connection lost, attempting to reconnect")

            await self.connect()

            yield self._redis

    async def get(self, key: str) -> Any:
        """Get value from cache.





        Args:


            key: Cache key.





        Returns:


            Cached value or None if not found.


        """

        try:
            async with self._ensure_connection() as redis_client:
                value = await redis_client.get(key)

                if value is None:
                    return None

                # Deserialize value

                try:
                    # Try JSON first

                    return json.loads(value)

                except (json.JSONDecodeError, UnicodeDecodeError):
                    try:
                        # Try pickle

                        return pickle.loads(value)

                    except Exception:
                        # Return raw value

                        return value

        except Exception as e:
            logger.error(f"Failed to get cache key {key}: {e}")

            return None

    async def set(self, key: str, value: Any, ttl: int | None = None) -> bool:
        """Set value in cache.





        Args:


            key: Cache key.


            value: Value to cache.


            ttl: Time to live in seconds.





        Returns:


            True if successful.


        """

        try:
            async with self._ensure_connection() as redis_client:
                # Serialize value

                if isinstance(value, (dict, list, tuple)):
                    serialized_value = json.dumps(value, ensure_ascii=False)

                else:
                    serialized_value = pickle.dumps(value)

                # Set value with TTL

                ttl_seconds = ttl or self.default_ttl

                await redis_client.setex(key, ttl_seconds, serialized_value)

                logger.debug(f"Cache set: {key} (TTL: {ttl_seconds}s)")

                return True

        except Exception as e:
            logger.error(f"Failed to set cache key {key}: {e}")

            return False

    async def delete(self, key: str) -> bool:
        """Delete key from cache.





        Args:


            key: Cache key to delete.





        Returns:


            True if successful.


        """

        try:
            async with self._ensure_connection() as redis_client:
                _ = await redis_client.delete(key)

                logger.debug(f"Cache delete: {key}")

                return result > 0

        except Exception as e:
            logger.error(f"Failed to delete cache key {key}: {e}")

            return False

    async def exists(self, key: str) -> bool:
        """Check if key exists in cache.





        Args:


            key: Cache key to check.





        Returns:


            True if key exists.


        """

        try:
            async with self._ensure_connection() as redis_client:
                return await redis_client.exists(key) > 0

        except Exception as e:
            logger.error(f"Failed to check cache key {key}: {e}")

            return False

    async def clear(self, pattern: str | None = None) -> bool:
        """Clear cache entries.





        Args:


            pattern: Optional key pattern to match.





        Returns:


            True if successful.


        """

        try:
            if pattern:
                return await self.clear_pattern(pattern) > 0

            else:
                async with self._ensure_connection() as redis_client:
                    await redis_client.flushdb()

                    return True

        except Exception as e:
            logger.error(f"Failed to clear cache: {e}")

            return False

    async def get_stats(self) -> dict[str, Any]:
        """Get cache statistics.





        Returns:


            Cache statistics including hit rate, memory usage, etc.


        """

        try:
            async with self._ensure_connection() as redis_client:
                info = await redis_client.info()

                return {
                    "connected": self._connected,
                    "redis_version": info.get("redis_version", "unknown"),
                    "used_memory": info.get("used_memory_human", "0B"),
                    "connected_clients": info.get("connected_clients", 0),
                    "total_commands_processed": info.get("total_commands_processed", 0),
                    "keyspace_hits": info.get("keyspace_hits", 0),
                    "keyspace_misses": info.get("keyspace_misses", 0),
                    "hit_rate": self._calculate_hit_rate(
                        info.get("keyspace_hits", 0), info.get("keyspace_misses", 0)
                    ),
                }

        except Exception as e:
            logger.error(f"Failed to get cache stats: {e}")

            return {"connected": False, "error": str(e)}

    # Additional Redis-specific methods

    async def expire(self, key: str, ttl: int) -> bool:
        """Set expiration for cache key.





        Args:


            key: Cache key.


            ttl: Time to live in seconds.





        Returns:


            True if expiration set successfully.


        """

        try:
            async with self._ensure_connection() as redis_client:
                return await redis_client.expire(key, ttl)

        except Exception as e:
            logger.error(f"Failed to set expiration for cache key {key}: {e}")

            return False

    async def ttl(self, key: str) -> int:
        """Get time to live for cache key.





        Args:


            key: Cache key.





        Returns:


            TTL in seconds, -1 if no expiration, -2 if key doesn't exist.


        """

        try:
            async with self._ensure_connection() as redis_client:
                return await redis_client.ttl(key)

        except Exception as e:
            logger.error(f"Failed to get TTL for cache key {key}: {e}")

            return -2

    async def keys(self, pattern: str = "*") -> list[str]:
        """Get keys matching pattern.





        Args:


            pattern: Key pattern (supports wildcards).





        Returns:


            List of matching keys.


        """

        try:
            async with self._ensure_connection() as redis_client:
                keys = await redis_client.keys(pattern)

                return [
                    key.decode("utf-8") if isinstance(key, bytes) else key
                    for key in keys
                ]

        except Exception as e:
            logger.error(f"Failed to get keys with pattern {pattern}: {e}")

            return []

    async def clear_pattern(self, pattern: str) -> int:
        """Clear all keys matching pattern.





        Args:


            pattern: Key pattern to clear.





        Returns:


            Number of keys deleted.


        """

        try:
            async with self._ensure_connection() as redis_client:
                keys = await self.keys(pattern)

                if keys:
                    return await redis_client.delete(*keys)

                return 0

        except Exception as e:
            logger.error(f"Failed to clear keys with pattern {pattern}: {e}")

            return 0

    async def increment(self, key: str, amount: int = 1) -> int:
        """Increment counter value.





        Args:


            key: Counter key.


            amount: Amount to increment.





        Returns:


            New counter value.


        """

        try:
            async with self._ensure_connection() as redis_client:
                return await redis_client.incrby(key, amount)

        except Exception as e:
            logger.error(f"Failed to increment counter {key}: {e}")

            return 0

    async def hash_set(
        self, key: str, mapping: dict[str, Any], ttl: int | None = None
    ) -> bool:
        """Set hash field values.





        Args:


            key: Hash key.


            mapping: Field-value mapping.


            ttl: Optional expiration time.





        Returns:


            True if set successfully.


        """

        try:
            async with self._ensure_connection() as redis_client:
                # Serialize values

                serialized_mapping = {}

                for field, value in mapping.items():
                    if isinstance(value, (dict, list, tuple)):
                        serialized_mapping[field] = json.dumps(
                            value, ensure_ascii=False
                        )

                    elif not isinstance(value, (str, bytes, int, float)):
                        serialized_mapping[field] = pickle.dumps(value)

                    else:
                        serialized_mapping[field] = value

                await redis_client.hset(key, mapping=serialized_mapping)

                if ttl:
                    await redis_client.expire(key, ttl)

                return True

        except Exception as e:
            logger.error(f"Failed to set hash {key}: {e}")

            return False

    async def hash_get(self, key: str, field: str, default: Any = None) -> Any:
        """Get hash field value.





        Args:


            key: Hash key.


            field: Field name.


            default: Default value if field not found.





        Returns:


            Field value or default.


        """

        try:
            async with self._ensure_connection() as redis_client:
                value = await redis_client.hget(key, field)

                if value is None:
                    return default

                # Try to deserialize

                try:
                    return json.loads(value)

                except (json.JSONDecodeError, UnicodeDecodeError):
                    try:
                        return pickle.loads(value)

                    except Exception:
                        return value

        except Exception as e:
            logger.error(f"Failed to get hash field {key}.{field}: {e}")

            return default

    async def list_push(self, key: str, *values: Any, ttl: int | None = None) -> int:
        """Push values to list.





        Args:


            key: List key.


            values: Values to push.


            ttl: Optional expiration time.





        Returns:


            New list length.


        """

        try:
            async with self._ensure_connection() as redis_client:
                # Serialize values

                serialized_values = []

                for value in values:
                    if isinstance(value, (dict, list, tuple)):
                        serialized_values.append(json.dumps(value, ensure_ascii=False))

                    elif not isinstance(value, (str, bytes, int, float)):
                        serialized_values.append(pickle.dumps(value))

                    else:
                        serialized_values.append(value)

                length = await redis_client.lpush(key, *serialized_values)

                if ttl:
                    await redis_client.expire(key, ttl)

                return length

        except Exception as e:
            logger.error(f"Failed to push to list {key}: {e}")

            return 0

    def _calculate_hit_rate(self, hits: int, misses: int) -> float:
        """Calculate cache hit rate."""

        total = hits + misses

        return (hits / total * 100) if total > 0 else 0.0


# Cache key utilities


def cache_key_from_args(*args, **kwargs) -> str:
    """Generate cache key from function arguments."""

    # Create a string representation of arguments

    args_str = str(args) + str(sorted(kwargs.items()))

    # Hash to create a consistent key

    return hashlib.sha256(args_str.encode()).hexdigest()


class CacheDecorator:
    """Decorator for caching function results."""

    def __init__(
        self,
        cache_manager: CacheStorageInterface,
        ttl: int = 3600,
        key_prefix: str = "func",
    ):
        """Initialize cache decorator.





        Args:


            cache_manager: Cache manager instance.


            ttl: Time to live in seconds.


            key_prefix: Cache key prefix.


        """

        self.cache_manager = cache_manager

        self.ttl = ttl

        self.key_prefix = key_prefix

    def __call__(self, func):
        async def wrapper(*args, **kwargs):
            # Generate cache key

            args_hash = cache_key_from_args(*args, **kwargs)

            cache_key = f"{self.key_prefix}:{func.__name__}:{args_hash}"

            # Try to get from cache

            await self.cache_manager.get(cache_key)

            if cached_result is not None:
                logger.debug(f"Cache hit for {func.__name__}")

                return cached_result

            # Execute function and cache result

            _ = await func(*args, **kwargs)

            await self.cache_manager.set(cache_key, result, self.ttl)

            logger.debug(f"Cache miss for {func.__name__}, result cached")

            return result

        return wrapper


def cached(
    cache_manager: CacheStorageInterface, ttl: int = 3600, key_prefix: str = "func"
):
    """Decorator for caching async function results.





    Args:


        cache_manager: Cache manager instance.


        ttl: Time to live in seconds.


        key_prefix: Cache key prefix.


    """

    return CacheDecorator(cache_manager, ttl, key_prefix)
