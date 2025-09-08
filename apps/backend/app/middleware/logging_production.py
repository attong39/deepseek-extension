from __future__ import annotations

import json
import logging
import re
import sys
import time
from datetime import UTC, datetime
from typing import Any

import structlog
from apps.backend.config.production import settings
from structlog.types import EventDict
import any
import app
import data
import dict
import event_dict
import getattr
import header
import isinstance
import item
import k
import key
import len
import list
import logger_name
import message
import name
import next
import pattern
import receive
import record
import round
import scope
import self
import send
import sensitive
import str
import text
import v
import value

"""
Production JSON Logging with PII Masking
Structured logging for observability
"""
PII_PATTERNS = [
    re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"),
    re.compile(r"\b(?:\+?1[-.]?)?\(?[0-9]{3}\)?[-.]?[0-9]{3}[-.]?[0-9]{4}\b"),
    re.compile(
        r"\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|3[47][0-9]{13}|3[0-9]{13}|6(?:011|5[0-9]{2})[0-9]{12})\b"
    ),
    re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
]
SENSITIVE_FIELDS = {
    "password",
    "token",
    "secret",
    "key",
    "authorization",
    "cookie",
    "csrf",
    "session",
    "api_key",
    "access_token",
    "refresh_token",
    "jwt",
    "bearer",
    "auth",
    "credential",
    "private_key",
    "public_key",
    "cert",
    "certificate",
}


def mask_pii(text: str) -> str:
    """Mask personally identifiable information in text."""
    if not isinstance(text, str):
        return text
    masked = text
    for pattern in PII_PATTERNS:
        masked = pattern.sub("[PII_MASKED]", masked)
    return masked


def mask_sensitive_dict(data: dict[str, Any]) -> dict[str, Any]:
    """Recursively mask sensitive fields in dictionary."""
    if not isinstance(data, dict):
        return data
    masked = {}
    for key, value in data.items():
        key_lower = key.lower()
        is_sensitive = any(sensitive in key_lower for sensitive in SENSITIVE_FIELDS)
        if is_sensitive:
            if isinstance(value, str) and len(value) > 4:
                masked[key] = f"{value[:2]}***{value[-2:]}"
            else:
                masked[key] = "[MASKED]"
        elif isinstance(value, dict):
            masked[key] = mask_sensitive_dict(value)
        elif isinstance(value, list):
            masked[key] = [
                mask_sensitive_dict(item) if isinstance(item, dict) else item
                for item in value
            ]
        elif isinstance(value, str):
            masked[key] = mask_pii(value)
        else:
            masked[key] = value
    return masked


def add_timestamp(_, __, event_dict: EventDict) -> EventDict:
    """Add timestamp to log event."""
    event_dict["timestamp"] = datetime.now(UTC).isoformat()
    return event_dict


def add_log_level(_, __, event_dict: EventDict) -> EventDict:
    """Add log level to event."""
    if "level" in event_dict:
        event_dict["severity"] = event_dict["level"].upper()
    return event_dict


def mask_sensitive_processor(_, __, event_dict: EventDict) -> EventDict:
    """Mask sensitive data in log events."""
    if "event" in event_dict and isinstance(event_dict["event"], str):
        event_dict["event"] = mask_pii(event_dict["event"])
    for key, value in list(event_dict.items()):
        if isinstance(value, dict):
            event_dict[key] = mask_sensitive_dict(value)
        elif isinstance(value, str):
            if key.lower() in SENSITIVE_FIELDS:
                event_dict[key] = "[MASKED]"
            else:
                event_dict[key] = mask_pii(value)
    return event_dict


def add_service_context(_, __, event_dict: EventDict) -> EventDict:
    """Add service context to logs."""
    event_dict.update(
        {
            "service": settings.app_name,
            "version": settings.app_version,
            "environment": settings.environment,
        }
    )
    return event_dict


class JSONFormatter(logging.Formatter):
    """Custom JSON formatter for standard logging."""

    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON."""
        log_data = {
            "timestamp": datetime.fromtimestamp(record.created, tz=UTC).isoformat(),
            "level": record.levelname,
            "severity": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "service": settings.app_name,
            "version": settings.app_version,
            "environment": settings.environment,
        }
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        extra_fields = {
            k: v
            for k, v in record.__dict__.items()
            if k
            not in {
                "name",
                "msg",
                "args",
                "levelname",
                "levelno",
                "pathname",
                "filename",
                "module",
                "lineno",
                "funcName",
                "created",
                "msecs",
                "relativeCreated",
                "thread",
                "threadName",
                "processName",
                "process",
                "getMessage",
                "exc_info",
                "exc_text",
                "stack_info",
            }
        }
        if extra_fields:
            log_data["extra"] = mask_sensitive_dict(extra_fields)
        log_data["message"] = mask_pii(log_data["message"])
        return json.dumps(log_data, ensure_ascii=False, default=str)


def setup_production_logging() -> None:
    """Setup production logging configuration."""
    if settings.log_format == "json":
        structlog.configure(
            processors=[
                structlog.stdlib.filter_by_level,
                structlog.stdlib.add_logger_name,
                structlog.stdlib.add_log_level,
                add_timestamp,
                add_log_level,
                add_service_context,
                mask_sensitive_processor,
                structlog.processors.JSONRenderer(),
            ],
            context_class=dict,
            logger_factory=structlog.stdlib.LoggerFactory(),
            cache_logger_on_first_use=True,
        )
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(JSONFormatter())
        root_logger = logging.getLogger()
        root_logger.handlers.clear()
        root_logger.addHandler(handler)
        root_logger.setLevel(getattr(logging, settings.log_level.upper()))
        for logger_name in ["uvicorn", "uvicorn.access", "fastapi"]:
            logger = logging.getLogger(logger_name)
            logger.handlers.clear()
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
    else:
        logging.basicConfig(
            level=getattr(logging, settings.log_level.upper()),
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[logging.StreamHandler(sys.stdout)],
        )


def get_logger(name: str) -> structlog.BoundLogger | logging.Logger:
    """Get a logger instance."""
    if settings.log_format == "json":
        return structlog.get_logger(name)
    else:
        return logging.getLogger(name)


class LoggingMiddleware:
    """Middleware to log HTTP requests."""

    def __init__(self, app):
        self.app = app
        self.logger = get_logger("http")

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        start_time = time.time()
        method = scope.get("method", "")
        path = scope.get("path", "")
        query_string = scope.get("query_string", b"").decode()
        client = scope.get("client", ("", 0))
        request_info = {
            "method": method,
            "path": path,
            "query": query_string,
            "client_ip": client[0] if client else "unknown",
            "user_agent": next(
                (
                    header[1].decode()
                    for header in scope.get("headers", [])
                    if header[0] == b"user-agent"
                ),
                "unknown",
            ),
        }

        async def send_wrapper(message):
            if message["type"] == "http.response.start":
                status_code = message["status"]
                duration = time.time() - start_time
                response_info = {
                    "status_code": status_code,
                    "duration_ms": round(duration * 1000, 2),
                }
                log_level = (
                    "error"
                    if status_code >= 500
                    else "warning"
                    if status_code >= 400
                    else "info"
                )
                if settings.log_format == "json":
                    self.logger.log(
                        log_level,
                        "HTTP request completed",
                        request=request_info,
                        response=response_info,
                    )
                else:
                    self.logger.log(
                        getattr(logging, log_level.upper()),
                        f"{method} {path} - {status_code} - {duration * 1000:.2f}ms",
                    )
            await send(message)

        await self.app(scope, receive, send_wrapper)


__all__ = [
    "JSONFormatter",
    "LoggingMiddleware",
    "PII_PATTERNS",
    "SENSITIVE_FIELDS",
    "add_log_level",
    "add_service_context",
    "add_timestamp",
    "client",
    "duration",
    "extra_fields",
    "format",
    "get_logger",
    "handler",
    "is_sensitive",
    "key_lower",
    "log_data",
    "log_level",
    "logger",
    "mask_pii",
    "mask_sensitive_dict",
    "mask_sensitive_processor",
    "masked",
    "method",
    "path",
    "query_string",
    "request_info",
    "response_info",
    "root_logger",
    "setup_production_logging",
    "start_time",
    "status_code",
]
