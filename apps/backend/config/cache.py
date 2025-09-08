"""Cache configuration and management.

Provides multi-level caching configuration including Redis, in-memory cache,
and distributed caching strategies for optimal performance.
"""

from __future__ import annotations

import gzip
import json
import logging
import pickle
from functools import lru_cache
from typing import Any

import redis.asyncio as redis
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from redis.asyncio import ConnectionPool
import Exception
import TypeError
import UnicodeDecodeError
import ValueError
import bool
import bytes
import classmethod
import dict
import e
import float
import int
import isinstance
import k
import key
import len
import list
import namespace
import node
import property
import self
import stats
import str
import v

logger = logging.getLogger(__name__)


class RedisCacheSettings(BaseSettings):
    """Redis cache configuration."""

    model_config = SettingsConfigDict(env_prefix="CACHE_REDIS_", env_file=".env")

    host: str = Field(default="localhost")
    port: int = Field(default=6379)
    db: int = Field(default=0)
    password: str | None = Field(default=None)

    # Connection settings
    max_connections: int = Field(default=100)
    socket_timeout: float = Field(default=5.0)
    socket_connect_timeout: float = Field(default=5.0)
    retry_on_timeout: bool = Field(default=True)

    # Performance settings
    encoding: str = Field(default="utf-8")
    decode_responses: bool = Field(default=True)

    # Cluster settings
    cluster_enabled: bool = Field(default=False)
    cluster_nodes: list[str] = Field(default_factory=list)

    @field_validator("cluster_nodes", mode="before")
    @classmethod
    def parse_cluster_nodes(cls, v: Any) -> list[str]:
        if isinstance(v, str):
            return [node.strip() for node in v.split(",") if node.strip()]
        return v

    @property
    def url(self) -> str:
        """Build Redis URL."""
        auth = f":{self.password}@" if self.password else ""
        return f"redis://{auth}{self.host}:{self.port}/{self.db}"


class MemoryCacheSettings(BaseSettings):
    """In-memory cache configuration."""

    model_config = SettingsConfigDict(env_prefix="CACHE_MEMORY_", env_file=".env")

    enabled: bool = Field(default=True)
    max_size: int = Field(default=1000)
    ttl_seconds: int = Field(default=300)
    cleanup_interval: int = Field(default=60)

    # LRU settings
    lru_maxsize: int = Field(default=128)
    lru_typed: bool = Field(default=False)


class DistributedCacheSettings(BaseSettings):
    """Distributed cache configuration."""

    model_config = SettingsConfigDict(env_prefix="CACHE_DISTRIBUTED_", env_file=".env")

    enabled: bool = Field(default=False)
    consistency_level: str = Field(default="eventual")
    replication_factor: int = Field(default=3)

    # Partitioning settings
    partition_strategy: str = Field(default="hash")
    num_partitions: int = Field(default=16)

    @field_validator("consistency_level")
    @classmethod
    def validate_consistency_level(cls, v: str) -> str:
        allowed = ["strong", "eventual", "weak"]
        if v not in allowed:
            raise ValueError(f"Consistency level must be one of {allowed}")
        return v


class CacheSettings(BaseSettings):
    """Main cache configuration."""

    model_config = SettingsConfigDict(env_prefix="CACHE_", env_file=".env")

    enabled: bool = Field(default=True)
    default_ttl: int = Field(default=3600)
    key_prefix: str = Field(default="zeta_ai")

    # Cache levels
    redis: RedisCacheSettings = Field(default_factory=RedisCacheSettings)
    memory: MemoryCacheSettings = Field(default_factory=MemoryCacheSettings)
    distributed: DistributedCacheSettings = Field(
        default_factory=DistributedCacheSettings
    )

    # Strategy settings
    strategy: str = Field(default="multi_level")
    fallback_enabled: bool = Field(default=True)

    # Performance settings
    compression_enabled: bool = Field(default=True)
    compression_threshold: int = Field(default=1024)

    @field_validator("strategy")
    @classmethod
    def validate_strategy(cls, v: str) -> str:
        allowed = ["redis_only", "memory_only", "multi_level", "distributed"]
        if v not in allowed:
            raise ValueError(f"Cache strategy must be one of {allowed}")
        return v


class CacheManager:
    """Cache management with multi-level strategy."""

    def __init__(self, settings: CacheSettings):
        self.settings = settings
        self.redis_client: redis.Redis | None = None
        self.memory_cache: dict[str, Any] = {}
        self._connection_pool: ConnectionPool | None = None

    async def initialize(self) -> None:
        """Initialize cache connections."""
        if self.settings.enabled and self.settings.redis.host:
            try:
                self._connection_pool = ConnectionPool.from_url(
                    self.settings.redis.url,
                    max_connections=self.settings.redis.max_connections,
                    socket_timeout=self.settings.redis.socket_timeout,
                    socket_connect_timeout=self.settings.redis.socket_connect_timeout,
                    retry_on_timeout=self.settings.redis.retry_on_timeout,
                    decode_responses=False,  # store bytes; we handle (de)serialization
                )
                self.redis_client = redis.Redis(connection_pool=self._connection_pool)
                # Test connection
                await self.redis_client.ping()
                logger.info("Redis cache initialized successfully")
            except Exception as e:  # noqa: BLE001
                logger.error(f"Failed to initialize Redis cache: {e}")
                if not self.settings.fallback_enabled:
                    raise

    async def close(self) -> None:
        """Close cache connections and cleanup."""
        try:
            if self.redis_client is not None:
                await self.redis_client.close()
            if self._connection_pool is not None:
                await self._connection_pool.disconnect(inuse_connections=True)
        except Exception as e:  # noqa: BLE001
            logger.error(f"Error closing cache resources: {e}")
        finally:
            self.redis_client = None
            self._connection_pool = None
            self.memory_cache.clear()

    # ---------------------------- internal helpers ----------------------------
    def _generate_key(self, key: str, namespace: str | None) -> str:
        prefix = self.settings.key_prefix
        ns = f"{namespace}:" if namespace else ""
        return f"{prefix}:{ns}{key}"

    def _serialize_value(self, value: Any) -> bytes:
        """Serialize a value for storage."""
        try:
            serialized = json.dumps(value).encode("utf-8")
        except (TypeError, ValueError):
            # Fallback for complex objects
            serialized = pickle.dumps(value)
        # Apply compression if enabled and threshold met
        if self.settings.compression_enabled and (
            len(serialized) > self.settings.compression_threshold
        ):
            serialized = gzip.compress(serialized)
        return serialized

    def _deserialize_value(self, data: bytes) -> Any:
        """Deserialize a value from storage."""
        try:
            # Try decompression first
            if self.settings.compression_enabled:
                try:
                    data = gzip.decompress(data)
                except gzip.BadGzipFile:
                    pass  # Not compressed
            # Try JSON first
            try:
                return json.loads(data.decode("utf-8"))
            except (json.JSONDecodeError, UnicodeDecodeError):
                return pickle.loads(data)
        except Exception as e:  # noqa: BLE001
            logger.error(f"Failed to deserialize cache value: {e}")
            return None

    def _get_from_memory(self, cache_key: str) -> Any | None:
        if self.settings.memory.enabled and cache_key in self.memory_cache:
            return self.memory_cache[cache_key]
        return None

    async def _get_from_redis(self, cache_key: str) -> Any | None:
        if not self.redis_client:
            return None
        try:
            data = await self.redis_client.get(cache_key)
            if data:
                return self._deserialize_value(data)
        except Exception as e:  # noqa: BLE001
            logger.error(f"Redis get error for key {cache_key}: {e}")
        return None

    # ------------------------------ public API --------------------------------
    async def get(self, key: str, namespace: str | None = None) -> Any | None:
        if not self.settings.enabled:
            return None
        cache_key = self._generate_key(key, namespace)
        try:
            if self.settings.strategy == "multi_level":
                # Check memory cache first
                value = self._get_from_memory(cache_key)
                if value is not None:
                    return value
                # Fallback to Redis
                value = await self._get_from_redis(cache_key)
                if value is not None:
                    if self.settings.memory.enabled:
                        self.memory_cache[cache_key] = value
                    return value
            elif self.settings.strategy == "redis_only":
                return await self._get_from_redis(cache_key)
            elif self.settings.strategy == "memory_only":
                return self._get_from_memory(cache_key)
        except Exception as e:  # noqa: BLE001
            logger.error(f"Cache get error for key {cache_key}: {e}")
        return None

    async def set(
        self, key: str, value: Any, ttl: int | None = None, namespace: str | None = None
    ) -> bool:
        if not self.settings.enabled:
            return False
        cache_key = self._generate_key(key, namespace)
        ttl = ttl or self.settings.default_ttl
        try:
            if self.settings.strategy in ["multi_level", "memory_only"]:
                if self.settings.memory.enabled:
                    self.memory_cache[cache_key] = value
            if self.settings.strategy in ["multi_level", "redis_only"]:
                if self.redis_client:
                    serialized_value = self._serialize_value(value)
                    await self.redis_client.setex(cache_key, ttl, serialized_value)
            return True
        except Exception as e:  # noqa: BLE001
            logger.error(f"Cache set error for key {cache_key}: {e}")
            return False

    async def delete(self, key: str, namespace: str | None = None) -> bool:
        if not self.settings.enabled:
            return False
        cache_key = self._generate_key(key, namespace)
        try:
            if cache_key in self.memory_cache:
                del self.memory_cache[cache_key]
            if self.redis_client:
                await self.redis_client.delete(cache_key)
            return True
        except Exception as e:  # noqa: BLE001
            logger.error(f"Cache delete error for key {cache_key}: {e}")
            return False

    async def clear(self, namespace: str | None = None) -> bool:
        try:
            if namespace:
                pattern = self._generate_key("*", namespace)
            else:
                pattern = f"{self.settings.key_prefix}:*"
            # Memory
            if namespace:
                prefix = pattern.replace("*", "")
                keys_to_delete = [
                    k for k in self.memory_cache.keys() if k.startswith(prefix)
                ]
                for k in keys_to_delete:
                    del self.memory_cache[k]
            else:
                self.memory_cache.clear()
            # Redis
            if self.redis_client:
                keys = await self.redis_client.keys(pattern)
                if keys:
                    await self.redis_client.delete(*keys)
            return True
        except Exception as e:  # noqa: BLE001
            logger.error(f"Cache clear error: {e}")
            return False

    async def get_stats(self) -> dict[str, Any]:
        stats: dict[str, Any] = {
            "enabled": self.settings.enabled,
            "strategy": self.settings.strategy,
            "memory": {
                "enabled": self.settings.memory.enabled,
                "size": len(self.memory_cache),
                "max_size": self.settings.memory.max_size,
            },
            "redis": {"connected": self.redis_client is not None},
        }
        if self.redis_client:
            try:
                redis_info = await self.redis_client.info()
                stats["redis"].update(
                    {
                        "connected_clients": redis_info.get("connected_clients", 0),
                        "used_memory": redis_info.get("used_memory_human", "0B"),
                        "keyspace_hits": redis_info.get("keyspace_hits", 0),
                        "keyspace_misses": redis_info.get("keyspace_misses", 0),
                    }
                )
            except Exception as e:  # noqa: BLE001
                logger.error(f"Failed to get Redis stats: {e}")
        return stats


@lru_cache
def get_cache_settings() -> CacheSettings:
    """Get cached cache settings instance."""
    return CacheSettings()


@lru_cache
def get_cache_manager() -> CacheManager:
    """Get (and lazily create) a CacheManager singleton without globals."""
    settings = get_cache_settings()
    return CacheManager(settings)


async def init_cache() -> None:
    """Initialize cache system."""
    manager = get_cache_manager()
    await manager.initialize()
    logger.info("Cache system initialized successfully")


async def close_cache() -> None:
    """Close cache system."""
    manager = get_cache_manager()
    await manager.close()
    # Clear cached singleton
    get_cache_manager.cache_clear()  # type: ignore[attr-defined]
    logger.info("Cache system closed successfully")
