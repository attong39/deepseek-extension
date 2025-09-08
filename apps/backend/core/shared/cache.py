"""Abstract cache interface for ZETA AI application.





This module provides pure domain abstractions for caching without


concrete implementation dependencies (following Clean Architecture).


"""

from __future__ import annotations

import hashlib
import logging
from abc import ABC
from typing import Any

from apps.backend.core.interfaces.storage_interfaces import CacheStorageInterface
import agent_id
import args
import bool
import cache_service
import cache_storage
import cached_result
import conversation_data
import conversation_id
import dict
import endpoint
import func
import input_data
import int
import key_prefix
import kwargs
import model
import output_data
import params_hash
import query_hash
import result
import self
import session_data
import sorted
import staticmethod
import str
import ttl
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


def stable_hash(input_str: str) -> str:
    """Secure, deterministic hash for cache keys (SHA-256)."""
    return hashlib.sha256(input_str.encode("utf-8")).hexdigest()


class CacheService(ABC):
    """Abstract cache service for domain operations."""

    def __init__(self, cache_storage: CacheStorageInterface):
        """Initialize cache service.





        Args:


            cache_storage: Cache storage implementation.


        """

        self.cache_storage = cache_storage

    async def cache_user_session(
        self, user_id: str, session_data: dict[str, Any], ttl: int = 3600
    ) -> bool:
        """Cache user session data.





        Args:


            user_id: User identifier.


            session_data: Session data to cache.


            ttl: Time to live in seconds.





        Returns:


            True if successful.


        """

        key = CacheKeyBuilder.user_session(user_id)

        return await self.cache_storage.set(key, session_data, ttl)

    async def get_user_session(self, user_id: str) -> dict[str, Any] | None:
        """Get cached user session data.





        Args:


            user_id: User identifier.





        Returns:


            Session data or None if not found.


        """

        key = CacheKeyBuilder.user_session(user_id)

        return await self.cache_storage.get(key)

    async def cache_conversation(
        self, conversation_id: str, conversation_data: dict[str, Any], ttl: int = 7200
    ) -> bool:
        """Cache conversation data.





        Args:


            conversation_id: Conversation identifier.


            conversation_data: Conversation data to cache.


            ttl: Time to live in seconds.





        Returns:


            True if successful.


        """

        key = CacheKeyBuilder.conversation(conversation_id)

        return await self.cache_storage.set(key, conversation_data, ttl)

    async def get_conversation(self, conversation_id: str) -> dict[str, Any] | None:
        """Get cached conversation data.





        Args:


            conversation_id: Conversation identifier.





        Returns:


            Conversation data or None if not found.


        """

        key = CacheKeyBuilder.conversation(conversation_id)

        return await self.cache_storage.get(key)

    async def cache_model_output(
        self, model: str, input_data: Any, output_data: Any, ttl: int = 1800
    ) -> bool:
        """Cache model output.





        Args:


            model: Model name.


            input_data: Input data for hashing.


            output_data: Output data to cache.


            ttl: Time to live in seconds.





        Returns:


            True if successful.


        """

        input_hash = self._hash_input(input_data)

        key = CacheKeyBuilder.model_output(model, input_hash)

        return await self.cache_storage.set(key, output_data, ttl)

    async def get_model_output(self, model: str, input_data: Any) -> Any:
        """Get cached model output.





        Args:


            model: Model name.


            input_data: Input data for hashing.





        Returns:


            Cached output or None if not found.


        """

        input_hash = self._hash_input(input_data)

        key = CacheKeyBuilder.model_output(model, input_hash)

        return await self.cache_storage.get(key)

    async def invalidate_user_cache(self, user_id: str) -> bool:
        """Invalidate all cache entries for a user.





        Args:


            user_id: User identifier.





        Returns:


            True if successful.


        """

        pattern = f"*:user:{user_id}*"

        return await self.cache_storage.clear(pattern)

    async def get_cache_stats(self) -> dict[str, Any]:
        """Get cache statistics.





        Returns:


            Cache statistics.


        """

        return await self.cache_storage.get_stats()

    def _hash_input(self, input_data: Any) -> str:
        """Generate hash for input data.





        Args:


            input_data: Input data to hash.





        Returns:


            Hash string.


        """

        # Convert input to string representation and hash using SHA-256

        input_str = str(input_data)

        return stable_hash(input_str)


# Convenience function for creating cache keys


def cache_key_from_args(*args, **kwargs) -> str:
    """Generate cache key from function arguments.





    Args:


        *args: Positional arguments.


        **kwargs: Keyword arguments.





    Returns:


        Hash-based cache key.


    """

    # Create a string representation of arguments

    args_str = str(args) + str(sorted(kwargs.items()))

    # Hash to create a consistent key

    return stable_hash(args_str)


class CacheDecorator:
    """Abstract decorator for caching function results."""

    def __init__(
        self, cache_service: CacheService, ttl: int = 3600, key_prefix: str = "func"
    ):
        """Initialize cache decorator.





        Args:


            cache_service: Cache service instance.


            ttl: Time to live in seconds.


            key_prefix: Cache key prefix.


        """

        self.cache_service = cache_service

        self.ttl = ttl

        self.key_prefix = key_prefix

    def __call__(self, func):
        async def wrapper(*args, **kwargs):
            # Generate cache key

            args_hash = cache_key_from_args(*args, **kwargs)

            cache_key = f"{self.key_prefix}:{func.__name__}:{args_hash}"

            # Try to get from cache

            await self.cache_service.cache_storage.get(cache_key)

            if cached_result is not None:
                logger.debug(f"Cache hit for {func.__name__}")

                return cached_result

            # Execute function and cache result

            _ = await func(*args, **kwargs)

            await self.cache_service.cache_storage.set(cache_key, result, self.ttl)

            logger.debug(f"Cache miss for {func.__name__}, result cached")

            return result

        return wrapper


def cached(cache_service: CacheService, ttl: int = 3600, key_prefix: str = "func"):
    """Decorator for caching async function results.





    Args:


        cache_service: Cache service instance.


        ttl: Time to live in seconds.


        key_prefix: Cache key prefix.


    """

    return CacheDecorator(cache_service, ttl, key_prefix)
