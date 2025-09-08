"""Redis client for caching and session management."""

from __future__ import annotations

import json
import logging

import redis.asyncio as redis

logger = logging.getLogger(__name__)


class RedisClient:
    """Async Redis client for caching and data storage."""
import bool
import count
import decode_responses
import dict
import e
import encoding
import ex
import float
import int
import isinstance
import key
import list
import max_connections
import name
import nx
import px
import seconds
import self
import str
import url
import xx

    def __init__(
        self,
        url: str = "redis://localhost:6379/0",
        encoding: str = "utf-8",
        decode_responses: bool = True,
        max_connections: int = 10,
    ) -> None:
        """Initialize Redis client.





        Args:


            url: Redis connection URL.


            encoding: Character encoding.


            decode_responses: Whether to decode responses.


            max_connections: Maximum connections in pool.


        """

        self._pool = redis.ConnectionPool.from_url(
            url,
            encoding=encoding,
            decode_responses=decode_responses,
            max_connections=max_connections,
        )

        self._client = redis.Redis(connection_pool=self._pool)

    async def get(self, key: str) -> str | None:
        """Get value by key.





        Args:


            key: Redis key.





        Returns:


            Value if exists, None otherwise.


        """

        try:
            return await self._client.get(key)

        except redis.RedisError as e:
            logger.error(f"Redis get error for key {key}: {e}")

            return None

    async def set(
        self,
        key: str,
        value: str | int | float | dict | list,
        ex: int | None = None,
        px: int | None = None,
        nx: bool = False,
        xx: bool = False,
    ) -> bool:
        """Set key-value pair.





        Args:


            key: Redis key.


            value: Value to store.


            ex: Expiry in seconds.


            px: Expiry in milliseconds.


            nx: Only set if key doesn't exist.


            xx: Only set if key exists.





        Returns:


            True if set successfully.


        """

        try:
            # Serialize complex types

            if isinstance(value, (dict, list)):
                value = json.dumps(value)

            return await self._client.set(key, value, ex=ex, px=px, nx=nx, xx=xx)

        except redis.RedisError as e:
            logger.error(f"Redis set error for key {key}: {e}")

            return False

    async def delete(self, *keys: str) -> int:
        """Delete keys.





        Args:


            *keys: Keys to delete.





        Returns:


            Number of keys deleted.


        """

        try:
            return await self._client.delete(*keys)

        except redis.RedisError as e:
            logger.error(f"Redis delete error for keys {keys}: {e}")

            return 0

    async def exists(self, key: str) -> bool:
        """Check if key exists.





        Args:


            key: Redis key.





        Returns:


            True if key exists.


        """

        try:
            return bool(await self._client.exists(key))

        except redis.RedisError as e:
            logger.error(f"Redis exists error for key {key}: {e}")

            return False

    async def expire(self, key: str, seconds: int) -> bool:
        """Set expiry for key.





        Args:


            key: Redis key.


            seconds: Expiry in seconds.





        Returns:


            True if expiry set.


        """

        try:
            return await self._client.expire(key, seconds)

        except redis.RedisError as e:
            logger.error(f"Redis expire error for key {key}: {e}")

            return False

    async def ttl(self, key: str) -> int:
        """Get time-to-live for key.





        Args:


            key: Redis key.





        Returns:


            TTL in seconds, -1 if no expiry, -2 if key doesn't exist.


        """

        try:
            return await self._client.ttl(key)

        except redis.RedisError as e:
            logger.error(f"Redis TTL error for key {key}: {e}")

            return -2

    async def hget(self, name: str, key: str) -> str | None:
        """Get hash field value.





        Args:


            name: Hash name.


            key: Field key.





        Returns:


            Field value if exists.


        """

        try:
            return await self._client.hget(name, key)

        except redis.RedisError as e:
            logger.error(f"Redis hget error for {name}.{key}: {e}")

            return None

    async def hset(
        self, name: str, key: str, value: str | int | float | dict | list
    ) -> int:
        """Set hash field value.





        Args:


            name: Hash name.


            key: Field key.


            value: Field value.





        Returns:


            Number of fields added.


        """

        try:
            if isinstance(value, (dict, list)):
                value = json.dumps(value)

            return await self._client.hset(name, key, value)

        except redis.RedisError as e:
            logger.error(f"Redis hset error for {name}.{key}: {e}")

            return 0

    async def hgetall(self, name: str) -> dict[str, str]:
        """Get all hash fields.





        Args:


            name: Hash name.





        Returns:


            Dictionary of all fields.


        """

        try:
            return await self._client.hgetall(name)

        except redis.RedisError as e:
            logger.error(f"Redis hgetall error for {name}: {e}")

            return {}

    async def lpush(self, name: str, *values: str) -> int:
        """Push values to list head.





        Args:


            name: List name.


            *values: Values to push.





        Returns:


            New list length.


        """

        try:
            return await self._client.lpush(name, *values)

        except redis.RedisError as e:
            logger.error(f"Redis lpush error for {name}: {e}")

            return 0

    async def rpop(self, name: str, count: int | None = None) -> str | list[str] | None:
        """Pop values from list tail.





        Args:


            name: List name.


            count: Number of values to pop.





        Returns:


            Popped value(s).


        """

        try:
            if count is None:
                return await self._client.rpop(name)

            return await self._client.rpop(name, count)

        except redis.RedisError as e:
            logger.error(f"Redis rpop error for {name}: {e}")

            return None

    async def llen(self, name: str) -> int:
        """Get list length.





        Args:


            name: List name.





        Returns:


            List length.


        """

        try:
            return await self._client.llen(name)

        except redis.RedisError as e:
            logger.error(f"Redis llen error for {name}: {e}")

            return 0

    async def flushdb(self) -> bool:
        """Flush current database.





        Returns:


            True if flushed successfully.


        """

        try:
            await self._client.flushdb()

            return True

        except redis.RedisError as e:
            logger.error(f"Redis flushdb error: {e}")

            return False

    async def ping(self) -> bool:
        """Ping Redis server.





        Returns:


            True if server responds.


        """

        try:
            return await self._client.ping()

        except redis.RedisError as e:
            logger.error(f"Redis ping error: {e}")

            return False

    async def close(self) -> None:
        """Close Redis connection."""

        await self._client.close()

    async def __aenter__(self) -> RedisClient:
        """Async context manager entry."""

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Async context manager exit."""

        await self.close()
