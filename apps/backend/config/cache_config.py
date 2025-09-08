"""


Cache Configuration





Provides caching configuration and utilities for Redis and in-memory caching.


"""

import json
import pickle
from dataclasses import dataclass
from typing import Any
import agent_id
import bool
import bytes
import chat_id
import dict
import file_id
import float
import identifier
import int
import message_id
import property
import self
import staticmethod
import str
import user_id
import value


@dataclass
class CacheConfig:
    """Cache configuration settings."""

    # Redis settings

    redis_url: str = "redis://localhost:6379/0"

    redis_enabled: bool = True

    redis_max_connections: int = 20

    redis_socket_timeout: float = 5.0

    redis_socket_connect_timeout: float = 5.0

    # Default TTL settings

    default_ttl: int = 3600  # 1 hour

    short_ttl: int = 300  # 5 minutes

    long_ttl: int = 86400  # 24 hours

    # Cache key prefixes

    user_prefix: str = "user:"

    chat_prefix: str = "chat:"

    agent_prefix: str = "agent:"

    message_prefix: str = "message:"

    session_prefix: str = "session:"

    # Serialization

    use_compression: bool = True

    serializer: str = "json"  # json, pickle, msgpack

    @property
    def redis_connection_kwargs(self) -> dict[str, Any]:
        """Get Redis connection parameters."""

        return {
            "max_connections": self.redis_max_connections,
            "socket_timeout": self.redis_socket_timeout,
            "socket_connect_timeout": self.redis_socket_connect_timeout,
            "decode_responses": True,
        }


class CacheKey:
    """Cache key generator utilities."""

    @staticmethod
    def user(user_id: str) -> str:
        """Generate user cache key."""

        return f"user:{user_id}"

    @staticmethod
    def user_sessions(user_id: str) -> str:
        """Generate user sessions cache key."""

        return f"user:{user_id}:sessions"

    @staticmethod
    def chat(chat_id: str) -> str:
        """Generate chat cache key."""

        return f"chat:{chat_id}"

    @staticmethod
    def chat_messages(chat_id: str) -> str:
        """Generate chat messages cache key."""

        return f"chat:{chat_id}:messages"

    @staticmethod
    def agent(agent_id: str) -> str:
        """Generate agent cache key."""

        return f"agent:{agent_id}"

    @staticmethod
    def agent_list() -> str:
        """Generate active agents list cache key."""

        return "agents:active"

    @staticmethod
    def message(message_id: str) -> str:
        """Generate message cache key."""

        return f"message:{message_id}"

    @staticmethod
    def user_auth(user_id: str) -> str:
        """Generate user authentication cache key."""

        return f"auth:{user_id}"

    @staticmethod
    def rate_limit(identifier: str) -> str:
        """Generate rate limit cache key."""

        return f"rate_limit:{identifier}"

    @staticmethod
    def file_metadata(file_id: str) -> str:
        """Generate file metadata cache key."""

        return f"file:{file_id}:metadata"


class CacheSerializer:
    """Cache value serialization utilities."""

    @staticmethod
    def serialize_json(value: Any) -> str:
        """Serialize value to JSON string."""

        return json.dumps(value, default=str, ensure_ascii=False)

    @staticmethod
    def deserialize_json(value: str) -> Any:
        """Deserialize JSON string to value."""

        return json.loads(value)

    @staticmethod
    def serialize_pickle(value: Any) -> bytes:
        """Serialize value to pickle bytes."""

        return pickle.dumps(value)

    @staticmethod
    def deserialize_pickle(value: bytes) -> Any:
        """Deserialize pickle bytes to value."""

        return pickle.loads(value)


# Cache TTL presets


class CacheTTL:
    """Predefined cache TTL values."""

    VERY_SHORT = 60  # 1 minute

    SHORT = 300  # 5 minutes

    MEDIUM = 1800  # 30 minutes

    DEFAULT = 3600  # 1 hour

    LONG = 14400  # 4 hours

    VERY_LONG = 86400  # 24 hours

    PERSISTENT = 604800  # 1 week


# Default cache configuration instance


default_cache_config = CacheConfig()


__all__ = [
    "CacheConfig",
    "CacheKey",
    "CacheSerializer",
    "CacheTTL",
    "default_cache_config",
]
