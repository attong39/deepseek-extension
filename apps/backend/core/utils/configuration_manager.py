from __future__ import annotations

import json
import os
import threading
from collections.abc import Callable
from pathlib import Path
from typing import Any

from apps.backend.core.observability.logging import get_logger
from apps.backend.core.utils.error_handler import CoreException, handle_core_errors
import Exception
import OSError
import bool
import config_dir
import config_name
import default
import dict
import e
import env_var
import f
import file_path
import float
import int
import key
import l
import len
import list
import listener
import name
import open
import self
import str
import sum
import v
import validator

"""Configuration Manager for Core Components.
Centralizes configuration CRUD with validation hooks, listeners, and
environment overrides. Designed to be lightweight and framework-agnostic.
"""
logger = get_logger(__name__)


class ConfigurationError(CoreException):
    """Configuration-related error."""


class ConfigurationManager:
    """Centralized configuration manager with file persistence.
    Args:
        config_dir: Base directory for configuration JSON files. If omitted,
            uses ``CORE_CONFIG_DIR`` environment variable, falling back to
            ``config`` in the project root.
    """

    def __init__(self, config_dir: str | None = None) -> None:
        self._config_dir = Path(config_dir or os.getenv("CORE_CONFIG_DIR", "config"))
        self._config_dir.mkdir(exist_ok=True)
        self._configs: dict[str, dict[str, Any]] = {}
        self._validators: dict[str, list[Callable[[dict[str, Any]], None]]] = {}
        self._listeners: dict[str, list[Callable[[str, dict[str, Any]], None]]] = {}
        self._lock = threading.RLock()
        self._load_default_configs()

    def _load_default_configs(self) -> None:
        """Load default configuration files into memory and persist them."""
        default_configs = {
            "core": {
                "debug": False,
                "log_level": "INFO",
                "max_workers": 4,
                "timeout": 30,
                "cache_ttl": 300,
                "retry_attempts": 3,
                "batch_size": 100,
            },
            "database": {
                "pool_size": 10,
                "max_overflow": 20,
                "pool_timeout": 30,
                "pool_recycle": 3600,
                "echo": False,
            },
            "api": {
                "host": "0.0.0.0",
                "port": 8000,
                "workers": 1,
                "reload": False,
                "cors_origins": ["*"],
                "rate_limit": 100,
            },
            "security": {
                "jwt_secret": "change-me-in-production",
                "jwt_algorithm": "HS256",
                "jwt_expiration": 3600,
                "password_min_length": 8,
                "session_timeout": 1800,
            },
            "observability": {
                "metrics_enabled": True,
                "tracing_enabled": True,
                "log_format": "json",
                "metrics_interval": 60,
            },
        }
        for config_name, config_data in default_configs.items():
            self._configs[config_name] = config_data
            try:
                self._save_config_file(config_name, config_data)
            except ConfigurationError:
                logger.warning("Failed to save default config %s", config_name)

    def load_config(self, name: str, file_path: str | None = None) -> dict[str, Any]:
        """Load configuration from disk.
        Args:
            name: Logical configuration name (e.g., "core").
            file_path: Optional explicit path to JSON file.
        Returns:
            Parsed configuration mapping; returns defaults if file missing.
        """
        with self._lock:
            if file_path:
                config_path = Path(file_path)
            else:
                config_path = self._config_dir / f"{name}.json"
            if config_path.exists():
                try:
                    with open(config_path, encoding="utf-8") as f:
                        config_data = json.load(f)
                        self._configs[name] = config_data
                        self._notify_listeners(name, config_data)
                        return config_data
                except (OSError, json.JSONDecodeError) as e:
                    logger.error("Failed to load config %s: %s", name, e)
                    raise ConfigurationError(f"Failed to load config '{name}': {e}")
            return self._configs.get(name, {})

    def save_config(self, name: str, config_data: dict[str, Any]) -> None:
        """Validate, persist, and broadcast configuration changes."""
        with self._lock:
            self._validate_config(name, config_data)
            self._configs[name] = config_data
            self._save_config_file(name, config_data)
            self._notify_listeners(name, config_data)

    def get_config(self, name: str, key: str | None = None, default: Any = None) -> Any:
        """Get configuration value.
        Args:
            name: Configuration group name.
            key: Optional key within the group.
            default: Default value if not present.
        Returns:
            Entire mapping when key is None; otherwise the value or default.
        """
        with self._lock:
            config = self._configs.get(name, {})
            if key is None:
                return config
            return config.get(key, default)

    def set_config_value(self, name: str, key: str, value: Any):
        """Set a single configuration value."""
        with self._lock:
            if name not in self._configs:
                self._configs[name] = {}
            self._configs[name][key] = value
            self._save_config_file(name, self._configs[name])
            self._notify_listeners(name, self._configs[name])

    def add_validator(
        self, config_name: str, validator: Callable[[dict[str, Any]], None]
    ) -> None:
        """Register a validator callback for a config group."""
        with self._lock:
            if config_name not in self._validators:
                self._validators[config_name] = []
            self._validators[config_name].append(validator)

    def add_listener(
        self, config_name: str, listener: Callable[[str, dict[str, Any]], None]
    ) -> None:
        """Register a listener invoked on successful saves/loads."""
        with self._lock:
            if config_name not in self._listeners:
                self._listeners[config_name] = []
            self._listeners[config_name].append(listener)

    def get_all_configs(self) -> dict[str, dict[str, Any]]:
        """Get a shallow copy of all configurations."""
        with self._lock:
            return self._configs.copy()

    def reload_config(self, name: str) -> bool:
        """Reload a single configuration from disk.
        Returns:
            True if file existed and was reloaded; False otherwise.
        """
        config_path = self._config_dir / f"{name}.json"
        if config_path.exists():
            self.load_config(name, str(config_path))
            return True
        return False

    def reload_all_configs(self) -> None:
        """Reload all configurations found in memory from disk."""
        with self._lock:
            for name in self._configs.keys():
                self.reload_config(name)

    def _validate_config(self, name: str, config_data: dict[str, Any]) -> None:
        """Validate configuration data using registered validators."""
        if name in self._validators:
            for validator in self._validators[name]:
                try:
                    validator(config_data)
                except Exception as e:
                    logger.error("Validator failed for %s: %s", name, e)
                    raise ConfigurationError(
                        f"Configuration validation failed for '{name}': {e}"
                    )

    def _save_config_file(self, name: str, config_data: dict[str, Any]) -> None:
        """Save configuration to JSON file."""
        config_path = self._config_dir / f"{name}.json"
        try:
            with open(config_path, "w", encoding="utf-8") as f:
                json.dump(config_data, f, indent=2, ensure_ascii=False)
        except OSError as e:
            logger.error("Failed to save config %s: %s", name, e)
            raise ConfigurationError(f"Failed to save config '{name}': {e}")

    def _notify_listeners(self, name: str, config_data: dict[str, Any]) -> None:
        """Notify configuration change listeners."""
        if name in self._listeners:
            for listener in self._listeners[name]:
                try:
                    listener(name, config_data)
                except Exception as e:
                    logger.warning("Listener failed for %s: %s", name, e)

    def get_config_summary(self) -> dict[str, Any]:
        """Get configuration summary."""
        with self._lock:
            return {
                "config_count": len(self._configs),
                "config_names": list(self._configs.keys()),
                "config_dir": str(self._config_dir),
                "validators_count": sum(len(v) for v in self._validators.values()),
                "listeners_count": sum(len(l) for l in self._listeners.values()),
            }


_config_manager = ConfigurationManager()


def _load_env_overrides() -> None:
    """Load configuration overrides from environment variables."""
    env_mappings = {
        "CORE_DEBUG": ("core", "debug"),
        "CORE_LOG_LEVEL": ("core", "log_level"),
        "DATABASE_URL": ("database", "url"),
        "API_HOST": ("api", "host"),
        "API_PORT": ("api", "port"),
        "JWT_SECRET": ("security", "jwt_secret"),
        "METRICS_ENABLED": ("observability", "metrics_enabled"),
    }
    for env_var, (config_name, key) in env_mappings.items():
        value = os.getenv(env_var)
        if value is not None:
            if value.lower() in ("true", "false"):
                value = value.lower() == "true"
            elif value.isdigit():
                value = int(value)
            elif value.replace(".", "").isdigit():
                value = float(value)
            _config_manager.set_config_value(config_name, key, value)


_load_env_overrides()


def get_config_manager() -> ConfigurationManager:
    """Get the global configuration manager instance."""
    return _config_manager


@handle_core_errors
def get_config(name: str, key: str | None = None, default: Any = None) -> Any:
    """Get configuration value (convenience function)."""
    return _config_manager.get_config(name, key, default)


@handle_core_errors
def set_config(name: str, key: str, value: Any):
    """Set configuration value (convenience function)."""
    _config_manager.set_config_value(name, key, value)


def reload_configs():
    """Reload all configurations."""
    _config_manager.reload_all_configs()


__all__ = [
    "ConfigurationError",
    "ConfigurationManager",
    "add_listener",
    "add_validator",
    "config",
    "config_data",
    "config_path",
    "default_configs",
    "env_mappings",
    "get_all_configs",
    "get_config",
    "get_config_manager",
    "get_config_summary",
    "load_config",
    "logger",
    "reload_all_configs",
    "reload_config",
    "reload_configs",
    "save_config",
    "set_config",
    "set_config_value",
    "value",
]
