# 🎯 Tối ưu hóa cấu hình cho Zeta AI Agent

import os
from functools import lru_cache
from typing import Any

from pydantic import BaseModel, Field, field_validator
import ValueError
import bool
import classmethod
import cls
import dict
import float
import int
import isinstance
import kwargs
import list
import origin
import print
import property
import self
import str
import super
import v


class DatabaseSettings(BaseModel):
    """Database configuration settings"""

    url: str = Field(default="sqlite:///zeta_feedback.db", description="Database URL")
    pool_size: int = Field(default=10, ge=1, le=100, description="Connection pool size")
    timeout: int = Field(default=30, ge=5, le=300, description="Connection timeout in seconds")
    echo: bool = Field(default=False, description="Enable SQL query logging")


class ServerSettings(BaseModel):
    """Server configuration settings"""

    host: str = Field(default="127.0.0.1", description="Server host")
    port: int = Field(default=9100, ge=1, le=65535, description="Server port")
    workers: int = Field(default=1, ge=1, le=16, description="Number of worker processes")
    reload: bool = Field(default=False, description="Enable auto-reload in development")
    log_level: str = Field(default="INFO", description="Logging level")

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in valid_levels:
            raise ValueError(f"Log level must be one of {valid_levels}")
        return v.upper()


class CORSSettings(BaseModel):
    """CORS configuration settings"""

    allowed_origins: list[str] = Field(default=["http://localhost:*"], description="Allowed CORS origins")
    allowed_methods: list[str] = Field(
        default=["GET", "POST", "PUT", "DELETE", "OPTIONS"], description="Allowed HTTP methods"
    )
    allowed_headers: list[str] = Field(default=["*"], description="Allowed headers")
    allow_credentials: bool = Field(default=False, description="Allow credentials")
    max_age: int = Field(default=86400, ge=0, description="Preflight cache max age")

    @field_validator("allowed_origins", mode="before")
    @classmethod
    def parse_origins(cls, v: Any) -> list[str]:
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        return v if isinstance(v, list) else [str(v)]


class CacheSettings(BaseModel):
    """Cache configuration settings"""

    redis_url: str | None = Field(default=None, description="Redis URL for caching")
    ttl: int = Field(default=300, ge=60, le=3600, description="Default cache TTL in seconds")
    max_memory_mb: int = Field(default=50, ge=10, le=500, description="Max memory for in-memory cache")
    enabled: bool = Field(default=True, description="Enable caching")


class MetricsSettings(BaseModel):
    """Metrics and monitoring settings"""

    retention_days: int = Field(default=30, ge=1, le=365, description="Metrics retention period")
    buffer_size: int = Field(default=50000, ge=1000, le=1000000, description="Metrics buffer size")
    collection_interval: int = Field(default=30, ge=10, le=300, description="Metrics collection interval")
    export_enabled: bool = Field(default=True, description="Enable Prometheus metrics export")


class SecuritySettings(BaseModel):
    """Security configuration settings"""

    rate_limit_requests: int = Field(default=100, ge=1, description="Requests per minute per IP")
    rate_limit_window: int = Field(default=60, ge=1, description="Rate limit window in seconds")
    max_request_size: int = Field(default=1048576, ge=1024, description="Max request size in bytes")  # 1MB
    max_prompt_length: int = Field(default=2000, ge=100, le=10000, description="Max prompt length")
    max_response_length: int = Field(default=5000, ge=100, le=20000, description="Max response length")
    sanitize_input: bool = Field(default=True, description="Enable input sanitization")


class AISettings(BaseModel):
    """AI model configuration settings"""

    model_timeout: int = Field(default=30, ge=5, le=300, description="Model response timeout")
    max_retries: int = Field(default=3, ge=0, le=10, description="Max retry attempts")
    retry_delay: float = Field(default=1.0, ge=0.1, le=10.0, description="Retry delay in seconds")
    model_endpoints: dict[str, str] = Field(default_factory=dict, description="Model endpoint URLs")


class MonitoringSettings(BaseModel):
    """Monitoring and alerting settings"""

    health_check_interval: int = Field(default=30, ge=10, le=300, description="Health check interval")
    memory_threshold: int = Field(default=90, ge=50, le=95, description="Memory usage alert threshold")
    cpu_threshold: int = Field(default=80, ge=50, le=95, description="CPU usage alert threshold")
    disk_threshold: int = Field(default=90, ge=50, le=95, description="Disk usage alert threshold")
    error_rate_threshold: float = Field(default=0.05, ge=0.0, le=1.0, description="Error rate threshold")


class ZetaSettings(BaseModel):
    """Main Zeta AI Agent configuration"""

    # Environment
    environment: str = Field(default="development", description="Environment name")
    debug: bool = Field(default=False, description="Enable debug mode")
    version: str = Field(default="1.0.0", description="Application version")

    # Sub-configurations
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    server: ServerSettings = Field(default_factory=ServerSettings)
    cors: CORSSettings = Field(default_factory=CORSSettings)
    cache: CacheSettings = Field(default_factory=CacheSettings)
    metrics: MetricsSettings = Field(default_factory=MetricsSettings)
    security: SecuritySettings = Field(default_factory=SecuritySettings)
    ai: AISettings = Field(default_factory=AISettings)
    monitoring: MonitoringSettings = Field(default_factory=MonitoringSettings)

    @field_validator("environment")
    @classmethod
    def validate_environment(cls, v: str) -> str:
        valid_envs = ["development", "staging", "production"]
        if v not in valid_envs:
            raise ValueError(f"Environment must be one of {valid_envs}")
        return v

    @property
    def is_production(self) -> bool:
        return self.environment == "production"

    @property
    def is_development(self) -> bool:
        return self.environment == "development"

    @classmethod
    def from_env(cls) -> "ZetaSettings":
        """Load settings from environment variables"""
        return cls(
            environment=os.getenv("ENVIRONMENT", "development"),
            debug=os.getenv("DEBUG", "false").lower() == "true",
            version=os.getenv("VERSION", "1.0.0"),
            database=DatabaseSettings(
                url=os.getenv("DB_URL", "sqlite:///zeta_feedback.db"),
                pool_size=int(os.getenv("DB_POOL_SIZE", "10")),
                timeout=int(os.getenv("DB_TIMEOUT", "30")),
                echo=os.getenv("DB_ECHO", "false").lower() == "true",
            ),
            server=ServerSettings(
                host=os.getenv("SERVER_HOST", "127.0.0.1"),
                port=int(os.getenv("SERVER_PORT", "9100")),
                workers=int(os.getenv("SERVER_WORKERS", "1")),
                reload=os.getenv("SERVER_RELOAD", "false").lower() == "true",
                log_level=os.getenv("SERVER_LOG_LEVEL", "INFO"),
            ),
            cors=CORSSettings(
                allowed_origins=os.getenv("CORS_ALLOWED_ORIGINS", "http://localhost:*").split(","),
                allow_credentials=os.getenv("CORS_ALLOW_CREDENTIALS", "false").lower() == "true",
                max_age=int(os.getenv("CORS_MAX_AGE", "86400")),
            ),
            cache=CacheSettings(
                redis_url=os.getenv("CACHE_REDIS_URL"),
                ttl=int(os.getenv("CACHE_TTL", "300")),
                max_memory_mb=int(os.getenv("CACHE_MAX_MEMORY_MB", "50")),
                enabled=os.getenv("CACHE_ENABLED", "true").lower() == "true",
            ),
            metrics=MetricsSettings(
                retention_days=int(os.getenv("METRICS_RETENTION_DAYS", "30")),
                buffer_size=int(os.getenv("METRICS_BUFFER_SIZE", "50000")),
                collection_interval=int(os.getenv("METRICS_COLLECTION_INTERVAL", "30")),
                export_enabled=os.getenv("METRICS_EXPORT_ENABLED", "true").lower() == "true",
            ),
            security=SecuritySettings(
                rate_limit_requests=int(os.getenv("SECURITY_RATE_LIMIT_REQUESTS", "100")),
                rate_limit_window=int(os.getenv("SECURITY_RATE_LIMIT_WINDOW", "60")),
                max_request_size=int(os.getenv("SECURITY_MAX_REQUEST_SIZE", "1048576")),
                max_prompt_length=int(os.getenv("SECURITY_MAX_PROMPT_LENGTH", "2000")),
                max_response_length=int(os.getenv("SECURITY_MAX_RESPONSE_LENGTH", "5000")),
                sanitize_input=os.getenv("SECURITY_SANITIZE_INPUT", "true").lower() == "true",
            ),
            ai=AISettings(
                model_timeout=int(os.getenv("AI_MODEL_TIMEOUT", "30")),
                max_retries=int(os.getenv("AI_MAX_RETRIES", "3")),
                retry_delay=float(os.getenv("AI_RETRY_DELAY", "1.0")),
                model_endpoints={},  # Can be loaded from separate config
            ),
            monitoring=MonitoringSettings(
                health_check_interval=int(os.getenv("MONITORING_HEALTH_CHECK_INTERVAL", "30")),
                memory_threshold=int(os.getenv("MONITORING_MEMORY_THRESHOLD", "90")),
                cpu_threshold=int(os.getenv("MONITORING_CPU_THRESHOLD", "80")),
                disk_threshold=int(os.getenv("MONITORING_DISK_THRESHOLD", "90")),
                error_rate_threshold=float(os.getenv("MONITORING_ERROR_RATE_THRESHOLD", "0.05")),
            ),
        )


@lru_cache
def get_settings() -> ZetaSettings:
    """Get cached settings instance"""
    return ZetaSettings.from_env()


# Environment-specific settings
class DevelopmentSettings(ZetaSettings):
    """Development environment settings"""

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.debug = True
        self.server.reload = True
        self.server.log_level = "DEBUG"
        self.database.echo = True
        self.security.rate_limit_requests = 1000  # More lenient in dev


class ProductionSettings(ZetaSettings):
    """Production environment settings"""

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.debug = False
        self.server.reload = False
        self.server.log_level = "INFO"
        self.database.echo = False
        self.security.sanitize_input = True
        self.monitoring.health_check_interval = 15  # More frequent in prod


def get_environment_settings() -> ZetaSettings:
    """Get settings based on environment"""
    env = os.getenv("ENVIRONMENT", "development").lower()

    if env == "production":
        return ProductionSettings.from_env()
    elif env == "staging":
        # Staging inherits from production but with some dev features
        settings = ProductionSettings.from_env()
        settings.server.log_level = "DEBUG"
        settings.database.echo = True
        return settings
    else:
        return DevelopmentSettings.from_env()


# Usage example
if __name__ == "__main__":
    settings = get_environment_settings()
    print(f"Environment: {settings.environment}")
    print(f"Debug: {settings.debug}")
    print(f"Database URL: {settings.database.url}")
    print(f"Server: {settings.server.host}:{settings.server.port}")
    print(f"CORS Origins: {settings.cors.allowed_origins}")
