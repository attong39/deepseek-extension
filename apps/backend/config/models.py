"""Configuration models for ZETA AI system.





This module provides configuration classes for various system components


including database, Redis, API, and AI service configurations.


"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, Field, field_validator, model_validator
import ValueError
import bool
import dict
import float
import int
import len
import list
import overrides
import property
import self
import str
import v

# Setup


logger = logging.getLogger(__name__)


class DatabaseConfig(BaseModel):
    """Database configuration."""

    # Connection settings

    driver: str = Field("postgresql+asyncpg", description="Database driver")

    host: str = Field("localhost", description="Database host")

    port: int = Field(5432, description="Database port")

    database: str = Field("zeta", description="Database name")

    username: str = Field("postgres", description="Database username")

    password: str = Field("", description="Database password")

    # Pool settings

    pool_size: int = Field(10, description="Connection pool size", ge=1)

    max_overflow: int = Field(20, description="Maximum pool overflow", ge=0)

    pool_timeout: int = Field(30, description="Pool timeout in seconds", ge=1)

    pool_recycle: int = Field(3600, description="Pool recycle time in seconds", ge=300)

    # Connection options

    echo: bool = Field(False, description="Echo SQL queries")

    echo_pool: bool = Field(False, description="Echo pool events")

    # SSL settings

    ssl_mode: str = Field("prefer", description="SSL mode")

    ssl_cert: str | None = Field(None, description="SSL certificate path")

    ssl_key: str | None = Field(None, description="SSL key path")

    ssl_ca: str | None = Field(None, description="SSL CA certificate path")

    @property
    def url(self) -> str:
        """Get database URL."""

        auth = f"{self.username}:{self.password}" if self.password else self.username

        return f"{self.driver}://{auth}@{self.host}:{self.port}/{self.database}"

    @property
    def sync_url(self) -> str:
        """Get synchronous database URL."""

        driver = self.driver.replace("+asyncpg", "").replace("+aiomysql", "")

        auth = f"{self.username}:{self.password}" if self.password else self.username

        return f"{driver}://{auth}@{self.host}:{self.port}/{self.database}"


class RedisConfig(BaseModel):
    """Redis configuration."""

    # Connection settings

    host: str = Field("localhost", description="Redis host")

    port: int = Field(6379, description="Redis port", ge=1, le=65535)

    database: int = Field(0, description="Redis database number", ge=0)

    password: str | None = Field(None, description="Redis password")

    username: str | None = Field(None, description="Redis username")

    # Connection options

    socket_timeout: float = Field(5.0, description="Socket timeout in seconds")

    socket_connect_timeout: float = Field(
        5.0, description="Connection timeout in seconds"
    )

    socket_keepalive: bool = Field(True, description="Enable socket keepalive")

    socket_keepalive_options: dict[str, int] = Field(
        default_factory=dict, description="Socket keepalive options"
    )

    # Pool settings

    max_connections: int = Field(50, description="Maximum connections", ge=1)

    retry_on_timeout: bool = Field(True, description="Retry on timeout")

    health_check_interval: int = Field(
        30, description="Health check interval in seconds"
    )

    # SSL settings

    ssl: bool = Field(False, description="Use SSL")

    ssl_cert_reqs: str = Field("required", description="SSL certificate requirements")

    ssl_ca_certs: str | None = Field(None, description="SSL CA certificates path")

    ssl_certfile: str | None = Field(None, description="SSL certificate file path")

    ssl_keyfile: str | None = Field(None, description="SSL key file path")

    # Cluster settings

    cluster_mode: bool = Field(False, description="Use Redis cluster")

    cluster_nodes: list[str] = Field(
        default_factory=list, description="Cluster node addresses"
    )

    @property
    def url(self) -> str:
        """Get Redis URL."""

        scheme = "rediss" if self.ssl else "redis"

        auth = f"{self.username}:{self.password}@" if self.password else ""

        return f"{scheme}://{auth}{self.host}:{self.port}/{self.database}"


class CeleryConfig(BaseModel):
    """Celery configuration."""

    # Broker settings

    broker_url: str = Field("redis://localhost:6379/0", description="Broker URL")

    result_backend: str = Field(
        "redis://localhost:6379/0", description="Result backend URL"
    )

    # Task settings

    task_serializer: str = Field("json", description="Task serializer")

    result_serializer: str = Field("json", description="Result serializer")

    accept_content: list[str] = Field(["json"], description="Accepted content types")

    result_expires: int = Field(3600, description="Result expiration in seconds")

    # Worker settings

    worker_prefetch_multiplier: int = Field(1, description="Worker prefetch multiplier")

    worker_max_tasks_per_child: int = Field(
        1000, description="Max tasks per worker child"
    )

    worker_disable_rate_limits: bool = Field(False, description="Disable rate limits")

    # Task routing

    task_routes: dict[str, dict[str, str]] = Field(
        default_factory=dict, description="Task routing configuration"
    )

    # Beat settings

    beat_schedule: dict[str, dict[str, Any]] = Field(
        default_factory=dict, description="Beat schedule configuration"
    )

    timezone: str = Field("UTC", description="Timezone for beat scheduler")

    # Monitoring

    worker_send_task_events: bool = Field(True, description="Send task events")

    task_send_sent_event: bool = Field(True, description="Send task sent events")

    # Security

    task_always_eager: bool = Field(
        False, description="Execute tasks eagerly (testing)"
    )

    task_eager_propagates: bool = Field(
        True, description="Propagate exceptions in eager mode"
    )


class APIConfig(BaseModel):
    """API configuration."""

    # Server settings

    host: str = Field("0.0.0.0", description="API host")

    port: int = Field(8000, description="API port", ge=1, le=65535)

    reload: bool = Field(False, description="Auto-reload on changes")

    workers: int = Field(1, description="Number of worker processes", ge=1)

    # CORS settings

    cors_origins: list[str] = Field(["*"], description="CORS allowed origins")

    cors_methods: list[str] = Field(["*"], description="CORS allowed methods")

    cors_headers: list[str] = Field(["*"], description="CORS allowed headers")

    cors_credentials: bool = Field(True, description="Allow CORS credentials")

    # Request/Response settings

    request_timeout: int = Field(60, description="Request timeout in seconds")

    max_request_size: int = Field(
        16 * 1024 * 1024, description="Max request size in bytes"
    )

    response_compression: bool = Field(True, description="Enable response compression")

    # Rate limiting

    rate_limit_enabled: bool = Field(True, description="Enable rate limiting")

    rate_limit_requests: int = Field(100, description="Requests per minute")

    rate_limit_window: int = Field(60, description="Rate limit window in seconds")

    # Security

    security_headers: bool = Field(True, description="Add security headers")

    trusted_hosts: list[str] = Field(["*"], description="Trusted host patterns")

    # Documentation

    docs_url: str | None = Field("/docs", description="Documentation URL")

    redoc_url: str | None = Field("/redoc", description="ReDoc URL")

    openapi_url: str | None = Field("/openapi.json", description="OpenAPI JSON URL")


class LoggingConfig(BaseModel):
    """Logging configuration."""

    # General settings

    level: str = Field("INFO", description="Default log level")

    format: str = Field(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s", description="Log format"
    )

    # File logging

    file_enabled: bool = Field(True, description="Enable file logging")

    file_path: str = Field("logs/app.log", description="Log file path")

    file_max_size: int = Field(
        10 * 1024 * 1024, description="Max log file size in bytes"
    )

    file_backup_count: int = Field(5, description="Number of backup files")

    file_level: str = Field("INFO", description="File log level")

    # Console logging

    console_enabled: bool = Field(True, description="Enable console logging")

    console_level: str = Field("INFO", description="Console log level")

    console_format: str = Field(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        description="Console log format",
    )

    # JSON logging

    json_enabled: bool = Field(False, description="Enable JSON logging")

    json_level: str = Field("INFO", description="JSON log level")

    # Logger-specific levels

    loggers: dict[str, str] = Field(
        default_factory=lambda: {
            "uvicorn": "INFO",
            "sqlalchemy": "WARNING",
            "celery": "INFO",
            "redis": "WARNING",
        },
        description="Logger-specific levels",
    )

    @field_validator("level", "file_level", "console_level", "json_level")
    def validate_log_level(cls, v: str) -> str:
        """Validate log level."""

        valid_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}

        if v.upper() not in valid_levels:
            raise ValueError(f"Invalid log level: {v}. Must be one of {valid_levels}")

        return v.upper()


class SecurityConfig(BaseModel):
    """Security configuration."""

    # JWT settings

    secret_key: str = Field(..., description="Secret key for JWT")

    algorithm: str = Field("HS256", description="JWT algorithm")

    access_token_expire_minutes: int = Field(30, description="Access token expiration")

    refresh_token_expire_days: int = Field(7, description="Refresh token expiration")

    # Password settings

    password_min_length: int = Field(8, description="Minimum password length")

    password_require_uppercase: bool = Field(
        True, description="Require uppercase letter"
    )

    password_require_lowercase: bool = Field(
        True, description="Require lowercase letter"
    )

    password_require_numbers: bool = Field(True, description="Require numbers")

    password_require_symbols: bool = Field(False, description="Require symbols")

    # Session settings

    session_expire_hours: int = Field(24, description="Session expiration hours")

    max_login_attempts: int = Field(5, description="Maximum login attempts")

    lockout_duration_minutes: int = Field(30, description="Account lockout duration")

    # API key settings

    api_key_length: int = Field(32, description="API key length")

    api_key_expire_days: int = Field(90, description="API key expiration days")

    # Encryption

    encryption_key: str | None = Field(
        None, description="Encryption key for sensitive data"
    )

    @field_validator("secret_key")
    def validate_secret_key(cls, v: str) -> str:
        """Validate secret key."""

        if len(v) < 32:
            raise ValueError("Secret key must be at least 32 characters long")

        return v


class AIServiceConfig(BaseModel):
    """AI service configuration."""

    # OpenAI settings

    openai_api_key: str | None = Field(None, description="OpenAI API key")

    openai_model: str = Field("gpt-4-turbo-preview", description="Default OpenAI model")

    openai_max_tokens: int = Field(4000, description="OpenAI max tokens")

    openai_temperature: float = Field(
        0.7, description="OpenAI temperature", ge=0.0, le=2.0
    )

    # Anthropic settings

    anthropic_api_key: str | None = Field(None, description="Anthropic API key")

    anthropic_model: str = Field(
        "claude-3-sonnet-20240229", description="Default Anthropic model"
    )

    anthropic_max_tokens: int = Field(4000, description="Anthropic max tokens")

    anthropic_temperature: float = Field(
        0.7, description="Anthropic temperature", ge=0.0, le=1.0
    )

    # Google Cloud settings

    gcp_project_id: str | None = Field(None, description="Google Cloud project ID")

    gcp_credentials_path: str | None = Field(
        None, description="GCP credentials file path"
    )

    gcp_region: str = Field("us-central1", description="GCP region")

    vertex_ai_model: str = Field("gemini-pro", description="Default Vertex AI model")

    # Request settings

    request_timeout: int = Field(60, description="AI service request timeout")

    max_retries: int = Field(3, description="Maximum retry attempts")

    retry_delay: float = Field(1.0, description="Retry delay in seconds")

    # Rate limiting

    requests_per_minute: int = Field(60, description="Requests per minute")

    concurrent_requests: int = Field(10, description="Maximum concurrent requests")


class StorageConfig(BaseModel):
    """Storage configuration."""

    # Local storage

    local_storage_path: str = Field("storage", description="Local storage directory")

    max_file_size: int = Field(100 * 1024 * 1024, description="Max file size in bytes")

    allowed_extensions: list[str] = Field(
        [".txt", ".pdf", ".doc", ".docx", ".json", ".csv"],
        description="Allowed file extensions",
    )

    # Cloud storage (if configured)

    cloud_provider: Literal["aws", "gcp", "azure"] | None = Field(
        None, description="Cloud storage provider"
    )

    cloud_bucket: str | None = Field(None, description="Cloud storage bucket")

    cloud_region: str | None = Field(None, description="Cloud storage region")

    cloud_credentials_path: str | None = Field(
        None, description="Cloud credentials path"
    )

    # Upload settings

    upload_chunk_size: int = Field(8192, description="Upload chunk size in bytes")

    temp_dir: str = Field("storage/temp", description="Temporary directory")

    cleanup_interval_hours: int = Field(24, description="Cleanup interval in hours")

    @field_validator("local_storage_path", "temp_dir")
    def validate_paths(cls, v: str) -> str:
        """Validate and create storage paths."""

        path = Path(v)

        path.mkdir(parents=True, exist_ok=True)

        return str(path)


class MonitoringConfig(BaseModel):
    """Monitoring and metrics configuration."""

    # Metrics

    metrics_enabled: bool = Field(True, description="Enable metrics collection")

    metrics_endpoint: str = Field("/metrics", description="Metrics endpoint")

    # Health checks

    health_check_enabled: bool = Field(True, description="Enable health checks")

    health_check_endpoint: str = Field("/health", description="Health check endpoint")

    health_check_interval: int = Field(
        30, description="Health check interval in seconds"
    )

    # Performance monitoring

    performance_monitoring: bool = Field(
        True, description="Enable performance monitoring"
    )

    slow_query_threshold: float = Field(
        1.0, description="Slow query threshold in seconds"
    )

    request_tracking: bool = Field(True, description="Track request performance")

    # Alerting

    alerting_enabled: bool = Field(False, description="Enable alerting")

    alert_email: str | None = Field(None, description="Alert email address")

    alert_webhook: str | None = Field(None, description="Alert webhook URL")

    # External monitoring

    sentry_dsn: str | None = Field(None, description="Sentry DSN for error tracking")

    datadog_api_key: str | None = Field(None, description="Datadog API key")


class AppConfig(BaseModel):
    """Main application configuration."""

    # Environment

    environment: Literal["development", "testing", "staging", "production"] = Field(
        "development", description="Application environment"
    )

    debug: bool = Field(False, description="Debug mode")

    testing: bool = Field(False, description="Testing mode")

    # Application info

    app_name: str = Field("ZETA AI", description="Application name")

    app_version: str = Field("1.0.0", description="Application version")

    app_description: str = Field(
        "Advanced AI Assistant with Multi-Agent Capabilities",
        description="Application description",
    )

    # Component configurations

    database: DatabaseConfig = Field(default_factory=lambda: DatabaseConfig())

    redis: RedisConfig = Field(default_factory=lambda: RedisConfig())

    celery: CeleryConfig = Field(default_factory=lambda: CeleryConfig())

    api: APIConfig = Field(default_factory=lambda: APIConfig())

    logging: LoggingConfig = Field(default_factory=lambda: LoggingConfig())

    security: SecurityConfig = Field(..., description="Security configuration")

    ai_services: AIServiceConfig = Field(default_factory=lambda: AIServiceConfig())

    storage: StorageConfig = Field(default_factory=lambda: StorageConfig())

    monitoring: MonitoringConfig = Field(default_factory=lambda: MonitoringConfig())

    # Feature flags

    features: dict[str, bool] = Field(
        default_factory=lambda: {
            "agent_management": True,
            "memory_system": True,
            "conversation_history": True,
            "voice_interaction": True,
            "file_processing": True,
            "admin_panel": True,
            "api_v2": False,
            "experimental_features": False,
        },
        description="Feature flags",
    )

    @model_validator(mode="after")
    def validate_environment_config(self) -> AppConfig:
        """Validate environment-specific configuration."""

        if self.environment == "production":
            # Production-specific validations

            if self.debug:
                raise ValueError("Debug mode must be disabled in production")

            if len(self.security.secret_key) < 64:
                raise ValueError("Production secret key must be at least 64 characters")

        return self

    @property
    def is_production(self) -> bool:
        """Check if running in production."""

        return self.environment == "production"

    @property
    def is_development(self) -> bool:
        """Check if running in development."""

        return self.environment == "development"

    @property
    def is_testing(self) -> bool:
        """Check if running in testing."""

        return self.environment == "testing" or self.testing


# Factory functions


def create_config(**overrides) -> AppConfig:
    """Create application configuration with overrides.





    Args:


        **overrides: Configuration overrides.





    Returns:


        Application configuration.


    """

    return AppConfig(**overrides)


def create_database_config(**overrides) -> DatabaseConfig:
    """Create database configuration with overrides.





    Args:


        **overrides: Configuration overrides.





    Returns:


        Database configuration.


    """

    return DatabaseConfig(**overrides)


def create_redis_config(**overrides) -> RedisConfig:
    """Create Redis configuration with overrides.





    Args:


        **overrides: Configuration overrides.





    Returns:


        Redis configuration.


    """

    return RedisConfig(**overrides)
