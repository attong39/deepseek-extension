"""Redis configuration for ZETA AI system.

This module provides Redis configuration for caching, sessions,
pub/sub, and distributed locking.
"""

from __future__ import annotations

from pydantic import Field, validator
from pydantic_settings import BaseSettings, SettingsConfigDict
import bool
import host
import int
import isinstance
import list
import node
import str
import v


class RedisSettings(BaseSettings):
    """Redis configuration settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Basic Connection
    redis_url: str = Field(default="redis://localhost:6379/0")
    redis_host: str = Field(default="localhost")
    redis_port: int = Field(default=6379)
    redis_db: int = Field(default=0)
    redis_username: str | None = Field(default=None)
    redis_password: str | None = Field(default=None)

    # SSL/TLS
    redis_ssl: bool = Field(default=False)
    redis_ssl_cert_reqs: str = Field(default="required")
    redis_ssl_ca_certs: str | None = Field(default=None)
    redis_ssl_certfile: str | None = Field(default=None)
    redis_ssl_keyfile: str | None = Field(default=None)

    # Connection Pool
    redis_max_connections: int = Field(default=20)
    redis_retry_on_timeout: bool = Field(default=True)
    redis_health_check_interval: int = Field(default=30)
    redis_socket_connect_timeout: int = Field(default=5)
    redis_socket_timeout: int = Field(default=5)

    # Sentinel (High Availability)
    redis_sentinel_enabled: bool = Field(default=False)
    redis_sentinel_hosts: list[str] = Field(default=[])
    redis_sentinel_service_name: str = Field(default="mymaster")
    redis_sentinel_password: str | None = Field(default=None)

    # Cluster
    redis_cluster_enabled: bool = Field(default=False)
    redis_cluster_nodes: list[str] = Field(default=[])
    redis_cluster_skip_full_coverage_check: bool = Field(default=False)

    # Cache Configuration
    cache_default_ttl: int = Field(default=3600)  # 1 hour
    cache_key_prefix: str = Field(default="zeta:")
    cache_serializer: str = Field(default="json")  # json, pickle, msgpack

    # Session Storage
    session_db: int = Field(default=1)
    session_ttl: int = Field(default=3600)  # 1 hour
    session_key_prefix: str = Field(default="session:")

    # Rate Limiting
    rate_limit_db: int = Field(default=2)
    rate_limit_key_prefix: str = Field(default="rate_limit:")

    # Pub/Sub
    pubsub_db: int = Field(default=3)
    pubsub_pattern_prefix: str = Field(default="zeta:")

    # Distributed Locking
    lock_db: int = Field(default=4)
    lock_default_timeout: int = Field(default=10)
    lock_key_prefix: str = Field(default="lock:")

    # Queue (Celery Backend)
    queue_db: int = Field(default=5)
    queue_key_prefix: str = Field(default="celery:")

    # Analytics/Metrics
    metrics_db: int = Field(default=6)
    metrics_ttl: int = Field(default=86400)  # 24 hours
    metrics_key_prefix: str = Field(default="metrics:")

    # Temporary Storage
    temp_db: int = Field(default=7)
    temp_default_ttl: int = Field(default=300)  # 5 minutes
    temp_key_prefix: str = Field(default="temp:")

    # Memory Management
    redis_maxmemory_policy: str = Field(default="allkeys-lru")
    redis_maxmemory: str | None = Field(default=None)  # e.g., "100mb"

    # Persistence
    redis_save_enabled: bool = Field(default=True)
    redis_save_seconds: int = Field(default=60)
    redis_save_changes: int = Field(default=1000)

    # Monitoring
    enable_redis_monitoring: bool = Field(default=True)
    redis_log_slow_queries: bool = Field(default=True)
    redis_slow_query_threshold_ms: int = Field(default=100)

    @validator("redis_sentinel_hosts", pre=True)
    def parse_sentinel_hosts(cls, v):
        """Parse sentinel hosts from string or list."""
        if isinstance(v, str):
            return [host.strip() for host in v.split(",") if host.strip()]
        return v

    @validator("redis_cluster_nodes", pre=True)
    def parse_cluster_nodes(cls, v):
        """Parse cluster nodes from string or list."""
        if isinstance(v, str):
            return [node.strip() for node in v.split(",") if node.strip()]
        return v


def get_redis_settings() -> RedisSettings:
    """Get Redis settings instance."""
    return RedisSettings()


# Redis Database Allocation
class RedisDB:
    """Redis database number constants."""

    DEFAULT = 0
    SESSION = 1
    RATE_LIMIT = 2
    PUBSUB = 3
    LOCK = 4
    QUEUE = 5
    METRICS = 6
    TEMP = 7
    CACHE = 8
    USER_DATA = 9


# Redis Key Patterns
class RedisKeys:
    """Redis key pattern constants."""

    # Cache patterns
    USER_CACHE = "user:{user_id}"
    AGENT_CACHE = "agent:{agent_id}"
    CONVERSATION_CACHE = "conversation:{conversation_id}"
    MEMORY_CACHE = "memory:{memory_id}"

    # Session patterns
    USER_SESSION = "session:{session_id}"
    API_KEY_SESSION = "api_key:{api_key_hash}"

    # Rate limiting patterns
    USER_RATE_LIMIT = "rate_limit:user:{user_id}:{endpoint}"
    IP_RATE_LIMIT = "rate_limit:ip:{ip_address}:{endpoint}"
    GLOBAL_RATE_LIMIT = "rate_limit:global:{endpoint}"

    # Lock patterns
    USER_LOCK = "lock:user:{user_id}"
    AGENT_LOCK = "lock:agent:{agent_id}"
    CONVERSATION_LOCK = "lock:conversation:{conversation_id}"

    # Queue patterns
    TASK_QUEUE = "queue:task:{task_type}"
    RESULT_QUEUE = "queue:result:{task_id}"

    # Pub/Sub patterns
    USER_NOTIFICATIONS = "notifications:user:{user_id}"
    AGENT_EVENTS = "events:agent:{agent_id}"
    SYSTEM_EVENTS = "events:system"

    # Analytics patterns
    USER_METRICS = "metrics:user:{user_id}:{metric_type}"
    AGENT_METRICS = "metrics:agent:{agent_id}:{metric_type}"
    SYSTEM_METRICS = "metrics:system:{metric_type}"

    # Temporary storage patterns
    EMAIL_VERIFICATION = "temp:email_verification:{token}"
    PASSWORD_RESET = "temp:password_reset:{token}"
    UPLOAD_SESSION = "temp:upload:{session_id}"


# Redis Connection Configurations
REDIS_CONFIGS = {
    "default": {
        "decode_responses": True,
        "encoding": "utf-8",
        "retry_on_timeout": True,
        "health_check_interval": 30,
    },
    "session": {
        "decode_responses": True,
        "encoding": "utf-8",
        "db": RedisDB.SESSION,
    },
    "cache": {
        "decode_responses": True,
        "encoding": "utf-8",
        "db": RedisDB.CACHE,
    },
    "pubsub": {
        "decode_responses": True,
        "encoding": "utf-8",
        "db": RedisDB.PUBSUB,
    },
    "queue": {
        "decode_responses": False,  # Celery handles encoding
        "db": RedisDB.QUEUE,
    },
}
