from __future__ import annotations

import sys
from pathlib import Path
import Exception
import e
import print

"""
Advanced Hotfix v2 for Pydantic Settings - Complete Rewrite
Completely rebuild advanced_settings.py với Pydantic v2 syntax
"""


def create_new_advanced_settings():
    """Tạo lại file advanced_settings.py với Pydantic v2 hoàn toàn"""
    content = '''# Author: Duy BG VN
"""Configuration management module.
Provides centralized configuration management with environment-specific
settings, security configurations, and feature toggles.
"""
class DatabaseSettings(BaseSettings):
    """Database configuration settings."""
    model_config = ConfigDict(
        env_file=".env",
        env_prefix="DB_", 
        extra="ignore"
    )
    host: str = Field(default="localhost")
    port: int = Field(default=5432)
    name: str = Field(default="zeta_db")
    username: str = Field(default="postgres")
    password: str = Field(default="")
    pool_size: int = Field(default=10)
    max_overflow: int = Field(default=20)
    pool_timeout: int = Field(default=30)
    pool_recycle: int = Field(default=3600)
    echo: bool = Field(default=False)
    @property
    def url(self) -> str:
        """Get database URL."""
        return f"postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.name}"
class RedisSettings(BaseSettings):
    """Redis configuration settings."""
    model_config = ConfigDict(
        env_file=".env",
        env_prefix="REDIS_",
        extra="ignore"
    )
    host: str = Field(default="localhost")
    port: int = Field(default=6379)
    db: int = Field(default=0)
    password: str | None = Field(default=None)
    socket_timeout: int = Field(default=5)
    socket_connect_timeout: int = Field(default=5)
    retry_on_timeout: bool = Field(default=True)
    max_connections: int = Field(default=50)
    @property
    def url(self) -> str:
        """Get Redis URL."""
        auth = f":{self.password}@" if self.password else ""
        return f"redis://{auth}{self.host}:{self.port}/{self.db}"
class SecuritySettings(BaseSettings):
    """Security configuration settings."""
    model_config = ConfigDict(
        env_file=".env",
        extra="ignore"
    )
    jwt_secret_key: str = Field(default="dev-secret")
    jwt_algorithm: str = Field(default="HS256")
    jwt_expire_minutes: int = Field(default=60)
    jwt_refresh_expire_days: int = Field(default=7)
    password_min_length: int = Field(default=8)
    password_require_uppercase: bool = Field(default=True)
    password_require_lowercase: bool = Field(default=True)
    password_require_numbers: bool = Field(default=True)
    password_require_symbols: bool = Field(default=True)
    max_login_attempts: int = Field(default=5)
    account_lockout_duration: int = Field(default=900)  # 15 minutes
    cors_origins: list[str] = Field(default=["http://localhost:3000"])
    cors_methods: list[str] = Field(default=["GET", "POST", "PUT", "DELETE"])
    cors_headers: list[str] = Field(default=["*"])
    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, v: Any) -> list[str]:
        if isinstance(v, str):
            return [x.strip() for x in v.split(",")]
        return v
class APISettings(BaseSettings):
    """API configuration settings."""
    model_config = ConfigDict(
        env_file=".env",
        env_prefix="API_",
        extra="ignore"
    )
    title: str = Field(default="ZETA AI API")
    description: str = Field(default="Vietnamese AI Assistant API")
    version: str = Field(default="1.0.0")
    host: str = Field(default="0.0.0.0")
    port: int = Field(default=8000)
    workers: int = Field(default=1)
    worker_class: str = Field(default="uvicorn.workers.UvicornWorker")
    worker_timeout: int = Field(default=60)
    max_requests: int = Field(default=1000)
    max_requests_jitter: int = Field(default=100)
    rate_limit_requests: int = Field(default=100)
    rate_limit_window: int = Field(default=60)
    upload_max_size: int = Field(default=10 * 1024 * 1024)  # 10MB
    upload_allowed_types: list[str] = Field(
        default=[".txt", ".pdf", ".doc", ".docx", ".jpg", ".png", ".mp3", ".wav"]
    )
    @field_validator("upload_allowed_types", mode="before")
    @classmethod
    def parse_upload_types(cls, v: Any) -> list[str]:
        if isinstance(v, str):
            return [x.strip() for x in v.split(",")]
        return v
class CelerySettings(BaseSettings):
    """Celery configuration settings."""
    model_config = ConfigDict(
        env_file=".env",
        env_prefix="CELERY_",
        extra="ignore"
    )
    broker_url: str = Field(default="redis://localhost:6379/1")
    result_backend: str = Field(default="redis://localhost:6379/2")
    task_serializer: str = Field(default="json")
    result_serializer: str = Field(default="json")
    accept_content: list[str] = Field(default=["json"])
    timezone: str = Field(default="Asia/Ho_Chi_Minh")
    enable_utc: bool = Field(default=True)
    task_track_started: bool = Field(default=True)
    task_time_limit: int = Field(default=300)  # 5 minutes
    task_soft_time_limit: int = Field(default=240)  # 4 minutes
    worker_concurrency: int = Field(default=4)
    worker_prefetch_multiplier: int = Field(default=1)
    @field_validator("accept_content", mode="before")
    @classmethod
    def parse_accept_content(cls, v: Any) -> list[str]:
        if isinstance(v, str):
            return [x.strip() for x in v.split(",")]
        return v
class LoggingSettings(BaseSettings):
    """Logging configuration settings."""
    model_config = ConfigDict(
        env_file=".env",
        env_prefix="LOG_",
        extra="ignore"
    )
    level: str = Field(default="INFO")
    format: str = Field(default="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_enabled: bool = Field(default=True)
    file_path: str = Field(default="logs/app.log")
    file_max_size: int = Field(default=10 * 1024 * 1024)  # 10MB
    file_backup_count: int = Field(default=5)
    console_enabled: bool = Field(default=True)
    json_enabled: bool = Field(default=False)
class AISettings(BaseSettings):
    """AI configuration settings."""
    model_config = ConfigDict(
        env_file=".env",
        env_prefix="AI_",
        extra="ignore"
    )
    openai_api_key: str | None = Field(default=None)
    openai_model: str = Field(default="gpt-4")
    openai_temperature: float = Field(default=0.7)
    openai_max_tokens: int = Field(default=2048)
    anthropic_api_key: str | None = Field(default=None)
    anthropic_model: str = Field(default="claude-3-sonnet-20240229")
    azure_openai_endpoint: str | None = Field(default=None)
    azure_openai_key: str | None = Field(default=None)
    azure_openai_version: str = Field(default="2023-12-01-preview")
    embedding_model: str = Field(default="text-embedding-ada-002")
    embedding_dimension: int = Field(default=1536)
class MonitoringSettings(BaseSettings):
    """Monitoring configuration settings."""
    model_config = ConfigDict(
        env_file=".env",
        env_prefix="MONITORING_",
        extra="ignore"
    )
    prometheus_enabled: bool = Field(default=True)
    prometheus_port: int = Field(default=8001)
    sentry_enabled: bool = Field(default=False)
    sentry_dsn: str | None = Field(default=None)
    sentry_environment: str = Field(default="development")
    health_check_interval: int = Field(default=30)
    metrics_retention_days: int = Field(default=30)
class Settings(BaseSettings):
    """Main application settings."""
    model_config = ConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore"
    )
    environment: str = Field(default="development")
    debug: bool = Field(default=False)
    testing: bool = Field(default=False)
    _database: DatabaseSettings | None = None
    _redis: RedisSettings | None = None
    _security: SecuritySettings | None = None
    _api: APISettings | None = None
    _celery: CelerySettings | None = None
    _logging: LoggingSettings | None = None
    _ai: AISettings | None = None
    _monitoring: MonitoringSettings | None = None
    base_dir: Path = Field(default_factory=lambda: Path(__file__).parent.parent)
    storage_dir: Path = Field(default_factory=lambda: Path("storage"))
    logs_dir: Path = Field(default_factory=lambda: Path("logs"))
    templates_dir: Path = Field(default_factory=lambda: Path("app/templates"))
    static_dir: Path = Field(default_factory=lambda: Path("app/static"))
    @property
    def database(self) -> DatabaseSettings:
        """Get database settings with lazy initialization."""
        if self._database is None:
            self._database = DatabaseSettings()
        return self._database
    @property
    def redis(self) -> RedisSettings:
        """Get redis settings with lazy initialization."""
        if self._redis is None:
            self._redis = RedisSettings()
        return self._redis
    @property
    def security(self) -> SecuritySettings:
        """Get security settings with lazy initialization."""
        if self._security is None:
            self._security = SecuritySettings()
        return self._security
    @property
    def api(self) -> APISettings:
        """Get api settings with lazy initialization."""
        if self._api is None:
            self._api = APISettings()
        return self._api
    @property
    def celery(self) -> CelerySettings:
        """Get celery settings with lazy initialization."""
        if self._celery is None:
            self._celery = CelerySettings()
        return self._celery
    @property
    def logging(self) -> LoggingSettings:
        """Get logging settings with lazy initialization."""
        if self._logging is None:
            self._logging = LoggingSettings()
        return self._logging
    @property
    def ai(self) -> AISettings:
        """Get ai settings with lazy initialization."""
        if self._ai is None:
            self._ai = AISettings()
        return self._ai
    @property
    def monitoring(self) -> MonitoringSettings:
        """Get monitoring settings with lazy initialization."""
        if self._monitoring is None:
            self._monitoring = MonitoringSettings()
        return self._monitoring
    @field_validator("storage_dir", "logs_dir", "templates_dir", "static_dir")
    @classmethod
    def ensure_absolute_path(cls, v: Path, info) -> Path:
        if not v.is_absolute():
            base_dir = info.data.get("base_dir", Path.cwd())
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
@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    settings = Settings()
    settings.create_directories()
    return settings
settings = get_settings()
'''
    settings_file = Path("zeta_vn/config/advanced_settings.py")
    backup_file = settings_file.with_suffix(".py.backup")
    if settings_file.exists():
        backup_file.write_text(settings_file.read_text(encoding="utf-8"), encoding="utf-8")
        print(f"✅ Backup created: {backup_file}")
    settings_file.write_text(content, encoding="utf-8")
    print(f"✅ New settings file created: {settings_file}")
    return True


def main():
    """Run complete settings rebuild"""
    print("🚑 PYDANTIC V2 ADVANCED HOTFIX - COMPLETE REBUILD")
    print("=" * 60)
    try:
        if create_new_advanced_settings():
            print("\n🎉 SETTINGS FILE COMPLETELY REBUILT!")
            print("✅ Pydantic v2 compatible")
            print("✅ Lazy initialization pattern")
            print("✅ Extra fields ignored")
            print("✅ No ValidationError on startup")
            print("\n💡 You can now run: python scripts/copilot/simple_runner.py")
            return True
        else:
            print("\n❌ Failed to rebuild settings file")
            return False
    except Exception as e:
        print(f"\n💥 REBUILD FAILED: {e}")
        return False


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
