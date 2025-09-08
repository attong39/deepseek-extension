"""Logging configuration for ZETA AI system.





This module provides centralized logging configuration with structured logging,


multiple handlers, and environment-specific settings.


"""

from __future__ import annotations

import json
import logging
import logging.config
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

from apps.backend.config.settings import get_settings
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
import ImportError
import adapter
import bool
import console_logging
import details
import dict
import dsn
import duration
import event_type
import file_logging
import float
import func_name
import hasattr
import int
import kwargs
import log_entry
import log_level
import log_to_console
import log_to_file
import name
import record
import self
import str
import super
import user_id


class LoggingSettings(BaseSettings):
    """Logging configuration settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Log levels

    log_level: str = Field(default="INFO")

    root_log_level: str = Field(default="WARNING")

    app_log_level: str = Field(default="INFO")

    # Log files

    log_dir: str = Field(default="storage/logs")

    log_file: str = Field(default="zeta.log")

    error_log_file: str = Field(default="error.log")

    access_log_file: str = Field(default="access.log")

    security_log_file: str = Field(default="security.log")

    # Log rotation

    log_rotation_size: int = Field(default=10485760)  # 10MB

    log_backup_count: int = Field(default=5)

    # Log format

    log_format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    detailed_log_format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(funcName)s - %(message)s"
    )

    json_log_format: bool = Field(default=False)

    # Console logging

    console_log_enabled: bool = Field(default=True)

    console_log_level: str = Field(default="INFO")

    # File logging

    file_log_enabled: bool = Field(default=True)

    # External logging

    sentry_dsn: str | None = Field(default=None)

    elastic_log_host: str | None = Field(default=None)

    elastic_log_port: int = Field(default=9200)

    # Performance logging

    performance_log_enabled: bool = Field(default=True)

    slow_query_threshold: float = Field(default=1.0)

    # Security logging

    security_log_enabled: bool = Field(default=True)


def get_logging_settings() -> LoggingSettings:
    """Get logging settings instance."""

    return LoggingSettings()


class ColoredFormatter(logging.Formatter):
    """Colored log formatter for console output."""

    COLORS = {
        "DEBUG": "\033[36m",  # Cyan
        "INFO": "\033[32m",  # Green
        "WARNING": "\033[33m",  # Yellow
        "ERROR": "\033[31m",  # Red
        "CRITICAL": "\033[41m",  # Red background
    }

    RESET = "\033[0m"

    def format(self, record: logging.LogRecord) -> str:
        """Format log record with colors."""

        log_color = self.COLORS.get(record.levelname, self.RESET)

        record.levelname = f"{log_color}{record.levelname}{self.RESET}"

        return super().format(record)


class StructuredFormatter(logging.Formatter):
    """Structured JSON formatter for machine-readable logs."""

    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON."""
        log_entry: dict[str, Any] = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # Add exception info if present
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)

        # Add extra fields
        if hasattr(record, "user_id"):
            log_entry["user_id"] = record.user_id

        if hasattr(record, "request_id"):
            log_entry["request_id"] = record.request_id

        if hasattr(record, "duration"):
            log_entry["duration"] = record.duration

        return json.dumps(log_entry)


def setup_logging(
    log_level: str | None = None,
    log_to_file: bool | None = None,
    log_to_console: bool | None = None,
) -> None:
    """Setup application logging configuration.





    Args:


        log_level: Override log level.


        log_to_file: Override file logging setting.


        log_to_console: Override console logging setting.


    """

    settings = get_logging_settings()

    app_settings = get_settings()

    # Use overrides or default settings

    effective_log_level = log_level or settings.log_level

    effective_file_logging = (
        log_to_file if log_to_file is not None else settings.file_log_enabled
    )

    effective_console_logging = (
        log_to_console if log_to_console is not None else settings.console_log_enabled
    )

    # Create log directory

    log_dir = Path(settings.log_dir)

    log_dir.mkdir(parents=True, exist_ok=True)

    # Configure logging

    logging_config = _get_logging_config(
        settings=settings,
        log_level=effective_log_level,
        file_logging=effective_file_logging,
        console_logging=effective_console_logging,
    )

    logging.config.dictConfig(logging_config)

    # Setup Sentry if configured

    if settings.sentry_dsn and app_settings.ENVIRONMENT != "development":
        _setup_sentry(settings.sentry_dsn)

    # Log startup information

    logger = logging.getLogger(__name__)

    logger.info(
        f"Logging configured - Level: {effective_log_level}, Environment: {app_settings.ENVIRONMENT}"
    )


def _get_logging_config(
    settings: LoggingSettings,
    log_level: str,
    file_logging: bool,
    console_logging: bool,
) -> dict[str, Any]:
    """Get logging configuration dictionary.





    Args:


        settings: Logging settings.


        log_level: Log level.


        file_logging: Enable file logging.


        console_logging: Enable console logging.





    Returns:


        Logging configuration dictionary.


    """

    handlers = []

    handler_configs = {}

    # Constants to avoid literal duplication
    ROTATING_FILE_HANDLER = "logging.handlers.RotatingFileHandler"

    # Console handler

    if console_logging:
        handlers.append("console")

        handler_configs["console"] = {
            "class": "logging.StreamHandler",
            "level": settings.console_log_level,
            "formatter": "colored" if sys.stderr.isatty() else "standard",
            "stream": "ext://sys.stdout",
        }

    # File handlers

    if file_logging:
        # Main log file

        handlers.append("file")

        handler_configs["file"] = {
            "class": ROTATING_FILE_HANDLER,
            "level": log_level,
            "formatter": "json" if settings.json_log_format else "detailed",
            "filename": os.path.join(settings.log_dir, settings.log_file),
            "maxBytes": settings.log_rotation_size,
            "backupCount": settings.log_backup_count,
            "encoding": "utf-8",
        }

        # Error log file

        handlers.append("error_file")

        handler_configs["error_file"] = {
            "class": ROTATING_FILE_HANDLER,
            "level": "ERROR",
            "formatter": "json" if settings.json_log_format else "detailed",
            "filename": os.path.join(settings.log_dir, settings.error_log_file),
            "maxBytes": settings.log_rotation_size,
            "backupCount": settings.log_backup_count,
            "encoding": "utf-8",
        }

        # Security log file

    if settings.security_log_enabled:
        handler_configs["security_file"] = {
            "class": ROTATING_FILE_HANDLER,
            "level": "INFO",
            "formatter": "json" if settings.json_log_format else "detailed",
            "filename": os.path.join(settings.log_dir, settings.security_log_file),
            "maxBytes": settings.log_rotation_size,
            "backupCount": settings.log_backup_count,
            "encoding": "utf-8",
        }

    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": settings.log_format,
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
            "detailed": {
                "format": settings.detailed_log_format,
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
            "colored": {
                "()": ColoredFormatter,
                "format": settings.log_format,
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
            "json": {
                "()": StructuredFormatter,
            },
        },
        "handlers": handler_configs,
        "loggers": {
            "": {  # Root logger
                "level": settings.root_log_level,
                "handlers": handlers,
            },
            "app": {
                "level": settings.app_log_level,
                "handlers": handlers,
                "propagate": False,
            },
            "core": {
                "level": log_level,
                "handlers": handlers,
                "propagate": False,
            },
            "data": {
                "level": log_level,
                "handlers": handlers,
                "propagate": False,
            },
            "security": {
                "level": "INFO",
                "handlers": ["security_file"]
                if settings.security_log_enabled and file_logging
                else handlers,
                "propagate": False,
            },
            "uvicorn": {
                "level": "INFO",
                "handlers": handlers,
                "propagate": False,
            },
            "uvicorn.access": {
                "level": "INFO",
                "handlers": handlers,
                "propagate": False,
            },
            "sqlalchemy": {
                "level": "WARNING",
                "handlers": handlers,
                "propagate": False,
            },
            "alembic": {
                "level": "INFO",
                "handlers": handlers,
                "propagate": False,
            },
        },
    }


def _setup_sentry(dsn: str) -> None:
    """Setup Sentry error tracking.





    Args:


        dsn: Sentry DSN.


    """

    try:
        import sentry_sdk  # noqa: PLC0415 - optional dependency
        from sentry_sdk.integrations.fastapi import (
            FastApiIntegration,  # noqa: PLC0415 - optional
        )
        from sentry_sdk.integrations.logging import (
            LoggingIntegration,  # noqa: PLC0415 - optional
        )
        from sentry_sdk.integrations.sqlalchemy import (
            SqlalchemyIntegration,  # noqa: PLC0415 - optional
        )

        sentry_logging = LoggingIntegration(
            level=logging.INFO,  # Capture info and above as breadcrumbs
            event_level=logging.ERROR,  # Send errors as events
        )

        sentry_sdk.init(
            dsn=dsn,
            integrations=[
                sentry_logging,
                SqlalchemyIntegration(),
                FastApiIntegration(),
            ],
            traces_sample_rate=0.1,
            attach_stacktrace=True,
            send_default_pii=False,
        )

        logging.getLogger(__name__).info("Sentry error tracking initialized")

    except ImportError:
        logging.getLogger(__name__).warning("Sentry SDK not available")


def get_logger(name: str, **kwargs: Any) -> logging.Logger | logging.LoggerAdapter:
    """Get a logger with optional context.





    Args:


        name: Logger name.


        **kwargs: Additional context to include in log records.





    Returns:


        Logger instance.


    """

    base_logger = logging.getLogger(name)

    if kwargs:
        # Create a LoggerAdapter to add context
        adapter: logging.LoggerAdapter = logging.LoggerAdapter(base_logger, kwargs)
        return adapter.logger  # Return the underlying logger for type compatibility

    return base_logger


def log_performance(func_name: str, duration: float, **kwargs: Any) -> None:
    """Log performance metrics.





    Args:


        func_name: Function name.


        duration: Execution duration in seconds.


        **kwargs: Additional metrics.


    """

    settings = get_logging_settings()

    if not settings.performance_log_enabled:
        return

    logger = logging.getLogger("performance")

    # Log slow operations

    if duration > settings.slow_query_threshold:
        extra = {"duration": duration, "function": func_name, **kwargs}

        logger.warning(
            f"Slow operation detected: {func_name} took {duration:.3f}s", extra=extra
        )

    else:
        extra = {"duration": duration, "function": func_name, **kwargs}

        logger.debug(f"Performance: {func_name} took {duration:.3f}s", extra=extra)


def log_security_event(
    event_type: str, user_id: str | None = None, **details: Any
) -> None:
    """Log security-related events.





    Args:


        event_type: Type of security event.


        user_id: User ID if applicable.


        **details: Additional event details.


    """

    settings = get_logging_settings()

    if not settings.security_log_enabled:
        return

    logger = logging.getLogger("security")

    extra = {"event_type": event_type, "user_id": user_id, **details}

    logger.info(f"Security event: {event_type}", extra=extra)


# Initialize logging on import in non-test environments


if "pytest" not in sys.modules:
    setup_logging()
