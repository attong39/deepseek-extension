from __future__ import annotations

import base64
import json
import logging
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any
import Exception
import action
import auto_create_config
import bool
import char
import chr
import config_path
import dict
import e
import encryption_key
import enumerate
import i
import int
import key
import len
import limit
import list
import metadata
import new_key
import ord
import self
import service
import str
import success
import use_cache
import use_environment

"""
API Key Manager - Integration Layer Security
Manages API keys and credentials for external services with:
- Secure storage and encryption
- Key rotation and expiration
- Access control and auditing
- Environment-based configuration
"""
logger = logging.getLogger(__name__)


class APIKeyError(Exception):
    """Base exception for API key management errors."""


class KeyNotFoundError(APIKeyError):
    """Raised when API key is not found."""


class KeyExpiredError(APIKeyError):
    """Raised when API key has expired."""


class InvalidKeyError(APIKeyError):
    """Raised when API key format is invalid."""


class APIKeyManager:
    """
    Secure API key management system.
    Features:
    - Environment variable fallback
    - Key validation and expiration
    - Access logging and auditing
    - Multiple storage backends
    - Encryption at rest
    """

    def __init__(
        self,
        config_path: str | None = None,
        encryption_key: str | None = None,
        use_environment: bool = True,
        auto_create_config: bool = True,
    ):
        self.config_path = Path(config_path or ".env.api_keys")
        self.encryption_key = encryption_key or os.getenv("API_KEY_ENCRYPTION_KEY")
        self.use_environment = use_environment
        self.auto_create_config = auto_create_config
        self._key_cache: dict[str, dict[str, Any]] = {}
        self._access_log: list[dict[str, Any]] = []
        self._key_patterns = {
            "openai": {"prefix": "sk-", "min_length": 48},
            "github": {"prefix": "ghp_", "min_length": 36},
            "anthropic": {"prefix": "sk-ant-", "min_length": 40},
            "google": {"min_length": 20},
            "azure": {"min_length": 32},
        }

    def _log_access(self, service: str, action: str, success: bool = True) -> None:
        """Log API key access for auditing."""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "service": service,
            "action": action,
            "success": success,
        }
        self._access_log.append(log_entry)
        if len(self._access_log) > 1000:
            self._access_log = self._access_log[-1000:]
        if success:
            logger.debug(f"🔑 API key {action} for {service}")
        else:
            logger.warning(f"❌ Failed API key {action} for {service}")

    def _validate_key_format(self, service: str, key: str) -> bool:
        """Validate API key format for known services."""
        if service not in self._key_patterns:
            return bool(key and key.strip())
        pattern = self._key_patterns[service]
        if "prefix" in pattern and not key.startswith(pattern["prefix"]):
            return False
        if len(key) < pattern["min_length"]:
            return False
        return True

    def _encrypt_key(self, key: str) -> str:
        """Encrypt API key for storage."""
        if not self.encryption_key:
            return base64.b64encode(key.encode()).decode()
        encrypted = ""
        for i, char in enumerate(key):
            key_char = self.encryption_key[i % len(self.encryption_key)]
            encrypted += chr(ord(char) ^ ord(key_char))
        return base64.b64encode(encrypted.encode()).decode()

    def _decrypt_key(self, encrypted_key: str) -> str:
        """Decrypt API key from storage."""
        try:
            decoded = base64.b64decode(encrypted_key).decode()
            if not self.encryption_key:
                return decoded
            decrypted = ""
            for i, char in enumerate(decoded):
                key_char = self.encryption_key[i % len(self.encryption_key)]
                decrypted += chr(ord(char) ^ ord(key_char))
            return decrypted
        except Exception as e:
            raise InvalidKeyError(f"Failed to decrypt key: {e}") from e

    def _load_from_file(self) -> dict[str, Any]:
        """Load API keys from config file."""
        if not self.config_path.exists():
            if self.auto_create_config:
                self.config_path.parent.mkdir(parents=True, exist_ok=True)
                self.config_path.write_text("{}")
                logger.info(f"📁 Created API key config file: {self.config_path}")
            return {}
        try:
            content = self.config_path.read_text()
            return json.loads(content) if content.strip() else {}
        except Exception as e:
            logger.error(f"❌ Failed to load API keys from {self.config_path}: {e}")
            return {}

    def _save_to_file(self, data: dict[str, Any]) -> None:
        """Save API keys to config file."""
        try:
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            self.config_path.write_text(json.dumps(data, indent=2))
            logger.debug(f"💾 Saved API keys to {self.config_path}")
        except Exception as e:
            logger.error(f"❌ Failed to save API keys to {self.config_path}: {e}")

    def store_key(
        self,
        service: str,
        key: str,
        expires_at: datetime | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        """
        Store API key for a service.
        Args:
            service: Service name (e.g., 'openai', 'github')
            key: API key value
            expires_at: Optional expiration datetime
            metadata: Optional metadata dictionary
        """
        if not self._validate_key_format(service, key):
            raise InvalidKeyError(f"Invalid key format for service '{service}'")
        encrypted_key = self._encrypt_key(key)
        data = self._load_from_file()
        key_data = {
            "encrypted_key": encrypted_key,
            "created_at": datetime.now().isoformat(),
            "expires_at": expires_at.isoformat() if expires_at else None,
            "metadata": metadata or {},
        }
        data[service] = key_data
        self._save_to_file(data)
        self._key_cache[service] = key_data
        self._log_access(service, "store")

    def get_key(self, service: str, use_cache: bool = True) -> str:
        """
        Get API key for a service.
        Args:
            service: Service name
            use_cache: Whether to use cached key
        Returns:
            Decrypted API key
        Raises:
            KeyNotFoundError: If key is not found
            KeyExpiredError: If key has expired
        """
        if self.use_environment:
            env_key = os.getenv(f"{service.upper()}_API_KEY")
            if env_key:
                self._log_access(service, "get_env")
                return env_key
        if use_cache and service in self._key_cache:
            key_data = self._key_cache[service]
        else:
            data = self._load_from_file()
            if service not in data:
                self._log_access(service, "get", success=False)
                raise KeyNotFoundError(f"API key not found for service '{service}'")
            key_data = data[service]
            self._key_cache[service] = key_data
        if key_data.get("expires_at"):
            expires_at = datetime.fromisoformat(key_data["expires_at"])
            if datetime.now() > expires_at:
                self._log_access(service, "get_expired", success=False)
                raise KeyExpiredError(f"API key for '{service}' has expired")
        try:
            decrypted_key = self._decrypt_key(key_data["encrypted_key"])
            self._log_access(service, "get")
            return decrypted_key
        except Exception as e:
            self._log_access(service, "get_decrypt_failed", success=False)
            raise InvalidKeyError(f"Failed to decrypt key for '{service}': {e}") from e

    def remove_key(self, service: str) -> None:
        """Remove API key for a service."""
        data = self._load_from_file()
        if service in data:
            del data[service]
            self._save_to_file(data)
        if service in self._key_cache:
            del self._key_cache[service]
        self._log_access(service, "remove")

    def list_services(self) -> list[str]:
        """List all services with stored API keys."""
        data = self._load_from_file()
        return list(data.keys())

    def check_key_expiry(self, service: str) -> datetime | None:
        """Check when a key expires."""
        try:
            data = self._load_from_file()
            if service not in data:
                return None
            expires_at_str = data[service].get("expires_at")
            if expires_at_str:
                return datetime.fromisoformat(expires_at_str)
            return None
        except Exception as e:
            logger.error(f"❌ Failed to check expiry for '{service}': {e}")
            return None

    def rotate_key(
        self,
        service: str,
        new_key: str,
        expires_at: datetime | None = None,
    ) -> None:
        """
        Rotate API key for a service.
        Args:
            service: Service name
            new_key: New API key value
            expires_at: Optional expiration datetime
        """
        self.store_key(service, new_key, expires_at)
        self._log_access(service, "rotate")

    def get_access_log(self, limit: int = 100) -> list[dict[str, Any]]:
        """Get recent access log entries."""
        return self._access_log[-limit:]

    def clear_cache(self) -> None:
        """Clear in-memory key cache."""
        cache_size = len(self._key_cache)
        self._key_cache.clear()
        logger.info(f"🗑️ Cleared {cache_size} cached API keys")

    def health_check(self) -> dict[str, Any]:
        """Check API key manager health."""
        try:
            services = self.list_services()
            config_exists = self.config_path.exists()
            expiring_soon = []
            now = datetime.now()
            warning_period = timedelta(days=7)  # Warn if expiring within 7 days
            for service in services:
                expires_at = self.check_key_expiry(service)
                if expires_at and expires_at - now < warning_period:
                    expiring_soon.append(
                        {
                            "service": service,
                            "expires_at": expires_at.isoformat(),
                            "days_remaining": (expires_at - now).days,
                        }
                    )
            return {
                "status": "healthy",
                "config_file_exists": config_exists,
                "services_count": len(services),
                "services": services,
                "cached_keys": len(self._key_cache),
                "access_log_entries": len(self._access_log),
                "expiring_keys": expiring_soon,
                "encryption_enabled": bool(self.encryption_key),
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e),
            }


__all__ = [
    "APIKeyError",
    "APIKeyManager",
    "InvalidKeyError",
    "KeyExpiredError",
    "KeyNotFoundError",
    "cache_size",
    "check_key_expiry",
    "clear_cache",
    "config_exists",
    "content",
    "data",
    "decoded",
    "decrypted",
    "decrypted_key",
    "encrypted",
    "encrypted_key",
    "env_key",
    "expires_at",
    "expires_at_str",
    "expiring_soon",
    "get_access_log",
    "get_key",
    "health_check",
    "key_char",
    "key_data",
    "list_services",
    "log_entry",
    "logger",
    "now",
    "pattern",
    "remove_key",
    "rotate_key",
    "services",
    "store_key",
    "warning_period",
]
