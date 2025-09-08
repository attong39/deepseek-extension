from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path
import Exception
import e
import print

"""Ultimate Pydantic v2 Fix - giải quyết toàn bộ validation errors."""


def fix_test_architecture_pyproject():
    """Sửa ruff config trong test_architecture."""
    pyproject_path = Path("test_architecture/pyproject.toml")
    if not pyproject_path.exists():
        print("⚠️ test_architecture/pyproject.toml not found")
        return
    content = pyproject_path.read_text(encoding="utf-8")
    if "[tool.ruff]" in content and "lint.isort" not in content:
        print("🔧 Fixing ruff configuration in test_architecture...")
        new_content = content.replace("[tool.ruff]", "[tool.ruff]\n# Ruff v2 configuration")
        if "[tool.ruff.lint]" not in new_content:
            new_content = new_content.replace("ignore = [", "[tool.ruff.lint]\nignore = [")
            new_content = new_content.replace("select = [", "select = [")
            if "[tool.ruff.isort]" in new_content:
                new_content = new_content.replace("[tool.ruff.isort]", "[tool.ruff.lint.isort]")
        pyproject_path.write_text(new_content, encoding="utf-8")
        print("✅ test_architecture pyproject.toml updated")


def create_settings_with_proper_env_prefix():
    """Tạo lại settings với env prefixes chính xác."""
    settings_path = Path("zeta_vn/config/advanced_settings.py")
    backup_path = settings_path.with_suffix(".py.backup_v3")
    if settings_path.exists():
        shutil.copy2(settings_path, backup_path)
        print(f"✅ Backup created: {backup_path}")
    content = '''"""Configuration management module - Pydantic v2 compatible.
Provides centralized configuration management with environment-specific
settings, security configurations, and feature toggles.
"""
class DatabaseSettings(BaseSettings):
    """Database configuration settings."""
    model_config = ConfigDict(
        env_file=".env",
        env_prefix="DATABASE_",
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
    password: str = Field(default="")
    max_connections: int = Field(default=20)
    decode_responses: bool = Field(default=True)
    @property
    def url(self) -> str:
        """Get Redis URL."""
        if self.password:
            return f"redis://:{self.password}@{self.host}:{self.port}/{self.db}"
        return f"redis://{self.host}:{self.port}/{self.db}"
class CelerySettings(BaseSettings):
    """Celery configuration settings."""
    model_config = ConfigDict(
        env_file=".env",
        env_prefix="CELERY_",
        extra="ignore"
    )
    broker_url: str = Field(default="redis://localhost:6379/0")
    result_backend: str = Field(default="redis://localhost:6379/1")
    task_serializer: str = Field(default="json")
    accept_content: list[str] = Field(default=["json"])
    result_serializer: str = Field(default="json")
    timezone: str = Field(default="Asia/Ho_Chi_Minh")
    enable_utc: bool = Field(default=True)
class CorsSettings(BaseSettings):
    """CORS configuration settings."""
    model_config = ConfigDict(
        env_file=".env",
        env_prefix="CORS_",
        extra="ignore"
    )
    origins: list[str] = Field(default=["http://localhost:3000", "http://127.0.0.1:3000"])
    credentials: bool = Field(default=True)
    methods: list[str] = Field(default=["*"])
    headers: list[str] = Field(default=["*"])
    @field_validator("origins", mode="before")
    @classmethod
    def parse_origins(cls, v: Any) -> list[str]:
        """Parse origins from string or list."""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v if isinstance(v, list) else ["http://localhost:3000"]
class SecuritySettings(BaseSettings):
    """Security configuration settings."""
    model_config = ConfigDict(
        env_file=".env",
        env_prefix="SECURITY_",
        extra="ignore"
    )
    secret_key: str = Field(default="change-me-in-production")
    algorithm: str = Field(default="HS256")
    access_token_expire_minutes: int = Field(default=30)
    refresh_token_expire_days: int = Field(default=7)
    allowed_hosts: list[str] = Field(default=["localhost", "127.0.0.1"])
    rate_limit_per_minute: int = Field(default=120)
class LoggingSettings(BaseSettings):
    """Logging configuration settings."""
    model_config = ConfigDict(
        env_file=".env",
        env_prefix="LOG_",
        extra="ignore"
    )
    level: str = Field(default="INFO")
    format: str = Field(default="colored")
    file_path: str = Field(default="./logs/app.log")
    max_bytes: int = Field(default=5242880)  # 5MB
    backup_count: int = Field(default=3)
class StorageSettings(BaseSettings):
    """Storage configuration settings."""
    model_config = ConfigDict(
        env_file=".env",
        env_prefix="STORAGE_",
        extra="ignore"
    )
    type: str = Field(default="local")
    path: str = Field(default="./storage")
    max_upload_size: str = Field(default="50MB")
    upload_allowed_types: list[str] = Field(default=[
        "image/jpeg", "image/png", "image/gif", "image/webp",
        "application/pdf", "text/plain", "text/csv",
        "application/json", "application/xml"
    ])
    @field_validator("upload_allowed_types", mode="before")
    @classmethod
    def parse_upload_types(cls, v: Any) -> list[str]:
        """Parse upload types from string or list."""
        if isinstance(v, str):
            return [t.strip() for t in v.split(",")]
        return v if isinstance(v, list) else []
class MonitoringSettings(BaseSettings):
    """Monitoring configuration settings."""
    model_config = ConfigDict(
        env_file=".env",
        env_prefix="MONITORING_",
        extra="ignore"
    )
    health_check_interval: int = Field(default=60)
    metrics_enabled: bool = Field(default=True)
    tracing_enabled: bool = Field(default=False)
    prometheus_port: int = Field(default=8001)
class DesktopAgentSettings(BaseSettings):
    """Desktop agent configuration settings."""
    model_config = ConfigDict(
        env_file=".env",
        env_prefix="DESKTOP_AGENT_",
        extra="ignore"
    )
    enabled: bool = Field(default=True)
    host: str = Field(default="localhost")
    port: int = Field(default=8001)
    websocket_path: str = Field(default="/ws")
class VectorDbSettings(BaseSettings):
    """Vector database configuration settings."""
    model_config = ConfigDict(
        env_file=".env",
        env_prefix="VECTOR_DB_",
        extra="ignore"
    )
    type: str = Field(default="chroma")
    path: str = Field(default="./storage/vector_db")
    collection_name: str = Field(default="default")
    embedding_dimension: int = Field(default=1536)
class Settings(BaseSettings):
    """Main application settings."""
    model_config = ConfigDict(
        env_file=".env",
        extra="ignore"
    )
    environment: str = Field(default="development")
    debug: bool = Field(default=True)
    api_version: str = Field(default="v1")
    pythonpath: str = Field(default="./zeta_vn;./zeta_vn/app;./zeta_vn/core;./zeta_vn/data")
    _database: DatabaseSettings | None = None
    _redis: RedisSettings | None = None
    _celery: CelerySettings | None = None
    _cors: CorsSettings | None = None
    _security: SecuritySettings | None = None
    _logging: LoggingSettings | None = None
    _storage: StorageSettings | None = None
    _monitoring: MonitoringSettings | None = None
    _desktop_agent: DesktopAgentSettings | None = None
    _vector_db: VectorDbSettings | None = None
    @property
    def database(self) -> DatabaseSettings:
        """Get database settings (lazy-loaded)."""
        if self._database is None:
            self._database = DatabaseSettings()
        return self._database
    @property
    def redis(self) -> RedisSettings:
        """Get Redis settings (lazy-loaded)."""
        if self._redis is None:
            self._redis = RedisSettings()
        return self._redis
    @property
    def celery(self) -> CelerySettings:
        """Get Celery settings (lazy-loaded)."""
        if self._celery is None:
            self._celery = CelerySettings()
        return self._celery
    @property
    def cors(self) -> CorsSettings:
        """Get CORS settings (lazy-loaded)."""
        if self._cors is None:
            self._cors = CorsSettings()
        return self._cors
    @property
    def security(self) -> SecuritySettings:
        """Get security settings (lazy-loaded)."""
        if self._security is None:
            self._security = SecuritySettings()
        return self._security
    @property
    def logging(self) -> LoggingSettings:
        """Get logging settings (lazy-loaded)."""
        if self._logging is None:
            self._logging = LoggingSettings()
        return self._logging
    @property
    def storage(self) -> StorageSettings:
        """Get storage settings (lazy-loaded)."""
        if self._storage is None:
            self._storage = StorageSettings()
        return self._storage
    @property
    def monitoring(self) -> MonitoringSettings:
        """Get monitoring settings (lazy-loaded)."""
        if self._monitoring is None:
            self._monitoring = MonitoringSettings()
        return self._monitoring
    @property
    def desktop_agent(self) -> DesktopAgentSettings:
        """Get desktop agent settings (lazy-loaded)."""
        if self._desktop_agent is None:
            self._desktop_agent = DesktopAgentSettings()
        return self._desktop_agent
    @property
    def vector_db(self) -> VectorDbSettings:
        """Get vector database settings (lazy-loaded)."""
        if self._vector_db is None:
            self._vector_db = VectorDbSettings()
        return self._vector_db
@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
settings = get_settings()
__all__ = [
    "Settings",
    "DatabaseSettings",
    "RedisSettings",
    "CelerySettings",
    "CorsSettings",
    "SecuritySettings",
    "LoggingSettings",
    "StorageSettings",
    "MonitoringSettings",
    "DesktopAgentSettings",
    "VectorDbSettings",
    "get_settings",
    "settings",
]
'''
    settings_path.write_text(content, encoding="utf-8")
    print("✅ Settings file completely rewritten with proper env prefixes")


def test_settings_import():
    """Test if settings can be imported without errors."""
    try:
        result = subprocess.run(
            [
                "uv",
                "run",
                "python",
                "-c",
                "from apps.backend.config.advanced_settings import settings; print('Settings OK')",
            ],
            capture_output=True,
            text=True,
            cwd=Path.cwd(),
        )
        if result.returncode == 0:
            print("✅ Settings import test PASSED")
            return True
        else:
            print(f"❌ Settings import test FAILED: {result.stderr}")
            return False
    except Exception as e:
        print(f"💥 Error testing settings: {e}")
        return False


def main():
    """Main function."""
    print("🚑 ULTIMATE PYDANTIC V2 FIX - FINAL")
    print("=" * 60)
    fix_test_architecture_pyproject()
    create_settings_with_proper_env_prefix()
    if test_settings_import():
        print("\n🎉 ALL FIXES APPLIED SUCCESSFULLY!")
        print("💡 Now run: python scripts/copilot/simple_runner.py")
        return True
    else:
        print("\n❌ Settings import still failing. Manual review needed.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
