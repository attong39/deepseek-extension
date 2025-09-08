import bool
import dir_path
import float
import int
import isinstance
import list
import property
import self
import str
import v
import x
# Author: Duy BG VN
# ZETA AI - Configuration Settings

"""Configuration management module.

Provides centralized configuration management with environment-specific
settings, security configurations, and feature toggles.
"""

from functools import lru_cache
from pathlib import Path

from pydantic import Field, validator
from pydantic_settings import BaseSettings


class DatabaseSettings(BaseSettings):
    """Database configuration settings."""

    host: str = Field(default="localhost", env="DB_HOST")
    port: int = Field(default=5432, env="DB_PORT")
    name: str = Field(default="zeta_db", env="DB_NAME")
    username: str = Field(default="postgres", env="DB_USERNAME")
    password: str = Field(default="", env="DB_PASSWORD")
    pool_size: int = Field(default=10, env="DB_POOL_SIZE")
    max_overflow: int = Field(default=20, env="DB_MAX_OVERFLOW")
    pool_timeout: int = Field(default=30, env="DB_POOL_TIMEOUT")
    pool_recycle: int = Field(default=3600, env="DB_POOL_RECYCLE")
    echo: bool = Field(default=False, env="DB_ECHO")

    @property
    def url(self) -> str:
        """Get database URL."""
        return f"postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.name}"

    class Config:
        env_file = ".env"
        env_prefix = "DB_"


class RedisSettings(BaseSettings):
    """Redis configuration settings."""

    host: str = Field(default="localhost", env="REDIS_HOST")
    port: int = Field(default=6379, env="REDIS_PORT")
    db: int = Field(default=0, env="REDIS_DB")
    password: str | None = Field(default=None, env="REDIS_PASSWORD")
    socket_timeout: int = Field(default=5, env="REDIS_SOCKET_TIMEOUT")
    socket_connect_timeout: int = Field(default=5, env="REDIS_SOCKET_CONNECT_TIMEOUT")
    retry_on_timeout: bool = Field(default=True, env="REDIS_RETRY_ON_TIMEOUT")
    max_connections: int = Field(default=50, env="REDIS_MAX_CONNECTIONS")

    @property
    def url(self) -> str:
        """Get Redis URL."""
        auth = f":{self.password}@" if self.password else ""
        return f"redis://{auth}{self.host}:{self.port}/{self.db}"

    class Config:
        env_file = ".env"
        env_prefix = "REDIS_"


class SecuritySettings(BaseSettings):
    """Security configuration settings."""

    # Provide a development-safe default to avoid import-time ValidationError
    jwt_secret_key: str = Field("dev-secret", env="JWT_SECRET_KEY")
    jwt_algorithm: str = Field(default="HS256", env="JWT_ALGORITHM")
    jwt_expire_minutes: int = Field(default=60, env="JWT_EXPIRE_MINUTES")
    jwt_refresh_expire_days: int = Field(default=7, env="JWT_REFRESH_EXPIRE_DAYS")

    password_min_length: int = Field(default=8, env="PASSWORD_MIN_LENGTH")
    password_require_uppercase: bool = Field(
        default=True, env="PASSWORD_REQUIRE_UPPERCASE"
    )
    password_require_lowercase: bool = Field(
        default=True, env="PASSWORD_REQUIRE_LOWERCASE"
    )
    password_require_numbers: bool = Field(default=True, env="PASSWORD_REQUIRE_NUMBERS")
    password_require_symbols: bool = Field(default=True, env="PASSWORD_REQUIRE_SYMBOLS")

    max_login_attempts: int = Field(default=5, env="MAX_LOGIN_ATTEMPTS")
    account_lockout_duration: int = Field(
        default=900, env="ACCOUNT_LOCKOUT_DURATION"
    )  # 15 minutes

    cors_origins: list[str] = Field(
        default=["http://localhost:3000"], env="CORS_ORIGINS"
    )
    cors_methods: list[str] = Field(
        default=["GET", "POST", "PUT", "DELETE"], env="CORS_METHODS"
    )
    cors_headers: list[str] = Field(default=["*"], env="CORS_HEADERS")

    @validator("cors_origins", pre=True)
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            return [x.strip() for x in v.split(",")]
        return v

    class Config:
        env_file = ".env"


class APISettings(BaseSettings):
    """API configuration settings."""

    title: str = Field(default="ZETA AI API", env="API_TITLE")
    description: str = Field(
        default="Vietnamese AI Assistant API", env="API_DESCRIPTION"
    )
    version: str = Field(default="1.0.0", env="API_VERSION")
    host: str = Field(default="0.0.0.0", env="API_HOST")
    port: int = Field(default=8000, env="API_PORT")

    workers: int = Field(default=1, env="API_WORKERS")
    worker_class: str = Field(
        default="uvicorn.workers.UvicornWorker", env="API_WORKER_CLASS"
    )
    worker_timeout: int = Field(default=60, env="API_WORKER_TIMEOUT")
    max_requests: int = Field(default=1000, env="API_MAX_REQUESTS")
    max_requests_jitter: int = Field(default=100, env="API_MAX_REQUESTS_JITTER")

    rate_limit_requests: int = Field(default=100, env="API_RATE_LIMIT_REQUESTS")
    rate_limit_window: int = Field(default=60, env="API_RATE_LIMIT_WINDOW")

    upload_max_size: int = Field(
        default=10 * 1024 * 1024, env="API_UPLOAD_MAX_SIZE"
    )  # 10MB
    upload_allowed_types: list[str] = Field(
        default=[".txt", ".pdf", ".doc", ".docx", ".jpg", ".png", ".mp3", ".wav"],
        env="API_UPLOAD_ALLOWED_TYPES",
    )

    @validator("upload_allowed_types", pre=True)
    def parse_upload_types(cls, v):
        if isinstance(v, str):
            return [x.strip() for x in v.split(",")]
        return v

    class Config:
        env_file = ".env"
        env_prefix = "API_"


class CelerySettings(BaseSettings):
    """Celery configuration settings."""

    broker_url: str = Field(default="redis://localhost:6379/1", env="CELERY_BROKER_URL")
    result_backend: str = Field(
        default="redis://localhost:6379/2", env="CELERY_RESULT_BACKEND"
    )

    task_serializer: str = Field(default="json", env="CELERY_TASK_SERIALIZER")
    result_serializer: str = Field(default="json", env="CELERY_RESULT_SERIALIZER")
    accept_content: list[str] = Field(default=["json"], env="CELERY_ACCEPT_CONTENT")

    timezone: str = Field(default="Asia/Ho_Chi_Minh", env="CELERY_TIMEZONE")
    enable_utc: bool = Field(default=True, env="CELERY_ENABLE_UTC")

    task_track_started: bool = Field(default=True, env="CELERY_TASK_TRACK_STARTED")
    task_time_limit: int = Field(default=300, env="CELERY_TASK_TIME_LIMIT")  # 5 minutes
    task_soft_time_limit: int = Field(
        default=240, env="CELERY_TASK_SOFT_TIME_LIMIT"
    )  # 4 minutes

    worker_concurrency: int = Field(default=4, env="CELERY_WORKER_CONCURRENCY")
    worker_prefetch_multiplier: int = Field(
        default=1, env="CELERY_WORKER_PREFETCH_MULTIPLIER"
    )

    @validator("accept_content", pre=True)
    def parse_accept_content(cls, v):
        if isinstance(v, str):
            return [x.strip() for x in v.split(",")]
        return v

    class Config:
        env_file = ".env"
        env_prefix = "CELERY_"


class LoggingSettings(BaseSettings):
    """Logging configuration settings."""

    level: str = Field(default="INFO", env="LOG_LEVEL")
    format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s", env="LOG_FORMAT"
    )

    file_enabled: bool = Field(default=True, env="LOG_FILE_ENABLED")
    file_path: str = Field(default="logs/app.log", env="LOG_FILE_PATH")
    file_max_size: int = Field(
        default=10 * 1024 * 1024, env="LOG_FILE_MAX_SIZE"
    )  # 10MB
    file_backup_count: int = Field(default=5, env="LOG_FILE_BACKUP_COUNT")

    console_enabled: bool = Field(default=True, env="LOG_CONSOLE_ENABLED")
    json_enabled: bool = Field(default=False, env="LOG_JSON_ENABLED")

    class Config:
        env_file = ".env"
        env_prefix = "LOG_"


class AISettings(BaseSettings):
    """AI configuration settings."""

    openai_api_key: str | None = Field(default=None, env="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-4", env="OPENAI_MODEL")
    openai_temperature: float = Field(default=0.7, env="OPENAI_TEMPERATURE")
    openai_max_tokens: int = Field(default=2048, env="OPENAI_MAX_TOKENS")

    anthropic_api_key: str | None = Field(default=None, env="ANTHROPIC_API_KEY")
    anthropic_model: str = Field(
        default="claude-3-sonnet-20240229", env="ANTHROPIC_MODEL"
    )

    azure_openai_endpoint: str | None = Field(default=None, env="AZURE_OPENAI_ENDPOINT")
    azure_openai_key: str | None = Field(default=None, env="AZURE_OPENAI_KEY")
    azure_openai_version: str = Field(
        default="2023-12-01-preview", env="AZURE_OPENAI_VERSION"
    )

    embedding_model: str = Field(
        default="text-embedding-ada-002", env="EMBEDDING_MODEL"
    )
    embedding_dimension: int = Field(default=1536, env="EMBEDDING_DIMENSION")

    class Config:
        env_file = ".env"
        env_prefix = "AI_"


class MonitoringSettings(BaseSettings):
    """Monitoring configuration settings."""

    prometheus_enabled: bool = Field(default=True, env="PROMETHEUS_ENABLED")
    prometheus_port: int = Field(default=8001, env="PROMETHEUS_PORT")

    sentry_enabled: bool = Field(default=False, env="SENTRY_ENABLED")
    sentry_dsn: str | None = Field(default=None, env="SENTRY_DSN")
    sentry_environment: str = Field(default="development", env="SENTRY_ENVIRONMENT")

    health_check_interval: int = Field(default=30, env="HEALTH_CHECK_INTERVAL")
    metrics_retention_days: int = Field(default=30, env="METRICS_RETENTION_DAYS")

    class Config:
        env_file = ".env"
        env_prefix = "MONITORING_"


class Settings(BaseSettings):
    """Main application settings."""

    environment: str = Field(default="development", env="ENVIRONMENT")
    debug: bool = Field(default=False, env="DEBUG")
    testing: bool = Field(default=False, env="TESTING")

    # Sub-configurations
    database: DatabaseSettings = DatabaseSettings()
    redis: RedisSettings = RedisSettings()
    security: SecuritySettings = SecuritySettings()
    api: APISettings = APISettings()
    celery: CelerySettings = CelerySettings()
    logging: LoggingSettings = LoggingSettings()
    ai: AISettings = AISettings()
    monitoring: MonitoringSettings = MonitoringSettings()

    # Application paths
    base_dir: Path = Field(default_factory=lambda: Path(__file__).parent.parent)
    storage_dir: Path = Field(default_factory=lambda: Path("storage"))
    logs_dir: Path = Field(default_factory=lambda: Path("logs"))
    templates_dir: Path = Field(default_factory=lambda: Path("app/templates"))
    static_dir: Path = Field(default_factory=lambda: Path("app/static"))

    @validator("storage_dir", "logs_dir", "templates_dir", "static_dir")
    def ensure_absolute_path(cls, v, values):
        if not v.is_absolute():
            base_dir = values.get("base_dir", Path.cwd())
            return base_dir / v
        return v

    def create_directories(self) -> None:
        """Create necessary directories."""
        for dir_path in [self.storage_dir, self.logs_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)

    @property
    def is_production(self) -> bool:
        """Check if running in production."""
        return self.environment.lower() == "production"

    @property
    def is_development(self) -> bool:
        """Check if running in development."""
        return self.environment.lower() == "development"

    @property
    def is_testing(self) -> bool:
        """Check if running in testing mode."""
        return self.testing or self.environment.lower() == "testing"

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    settings = Settings()
    settings.create_directories()
    return settings


# Export for easy import
settings = get_settings()
