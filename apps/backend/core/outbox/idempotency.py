"""Idempotency support cho event handlers.

Cung cấp decorator và store interface để đảm bảo exactly-once processing
cho các event handlers trong Outbox pattern. Hỗ trợ cả sync và async handlers.
"""

from __future__ import annotations

import inspect
from collections.abc import Callable
from dataclasses import dataclass
from functools import wraps
from typing import Any, Protocol
import Exception
import RuntimeError
import ValueError
import args
import bool
import callable
import cfg
import dict
import e
import event
import fn
import kwargs
import message
import result
import self
import store
import str


class ProcessedStore(Protocol):
    """Interface cho store lưu trữ processed messages (sync)."""

    def exists(self, handler: str, key: str) -> bool:
        """Kiểm tra message đã được process chưa."""
        ...

    def put(self, handler: str, key: str) -> None:
        """Đánh dấu message đã được process."""
        ...


class AsyncProcessedStore(Protocol):
    """Interface cho async store lưu trữ processed messages."""

    async def exists(self, handler: str, key: str) -> bool:
        """Kiểm tra message đã được process chưa."""
        ...

    async def put(self, handler: str, key: str) -> None:
        """Đánh dấu message đã được process."""
        ...


@dataclass(frozen=True)
class IdempotencyConfig:
    """Configuration cho idempotency decorator."""

    handler_name: str
    key_from_event: Callable[[dict[str, Any]], str]  # Extract key từ event dict

    def __post_init__(self) -> None:
        """Validate configuration."""
        if not self.handler_name:
            raise ValueError("handler_name không được rỗng")
        if not callable(self.key_from_event):
            raise ValueError("key_from_event phải là callable")


def idempotent(cfg: IdempotencyConfig):  # type: ignore[misc]
    """Decorator để đảm bảo idempotent processing (async-aware).

    Usage:
        @idempotent(IdempotencyConfig(
            handler_name="process_agent_created",
            key_from_event=lambda evt: evt["event_id"]
        ))
        async def process_agent_created(store: AsyncProcessedStore, event: dict):
            # Handler logic
            pass

    Args:
        cfg: Idempotency configuration

    Returns:
        Decorated function với idempotency logic
    """

    def decorator(fn: Callable[..., Any]):
        if inspect.iscoroutinefunction(fn):

            @wraps(fn)
            async def async_wrapper(
                store: AsyncProcessedStore, event: dict[str, Any], *args, **kwargs
            ):
                # Extract message key từ event
                try:
                    message_key = cfg.key_from_event(event)
                except Exception as e:
                    raise ValueError(f"Không thể extract key từ event: {e}") from e

                # Kiểm tra đã process chưa
                if await store.exists(cfg.handler_name, message_key):
                    return {
                        "status": "skipped",
                        "reason": "already_processed",
                        "handler": cfg.handler_name,
                        "key": message_key,
                    }

                # Process message
                try:
                    _ = await fn(store, event, *args, **kwargs)

                    # Đánh dấu đã process thành công
                    await store.put(cfg.handler_name, message_key)

                    return result

                except Exception as e:
                    # Không đánh dấu đã process nếu có lỗi để message có thể retry
                    raise RuntimeError(
                        f"Handler {cfg.handler_name} failed for key {message_key}"
                    ) from e

            return async_wrapper
        else:

            @wraps(fn)
            def sync_wrapper(
                store: ProcessedStore, event: dict[str, Any], *args, **kwargs
            ):
                # Extract message key từ event
                try:
                    message_key = cfg.key_from_event(event)
                except Exception as e:
                    raise ValueError(f"Không thể extract key từ event: {e}") from e

                # Kiểm tra đã process chưa
                if store.exists(cfg.handler_name, message_key):
                    return {
                        "status": "skipped",
                        "reason": "already_processed",
                        "handler": cfg.handler_name,
                        "key": message_key,
                    }

                # Process message
                try:
                    _ = fn(store, event, *args, **kwargs)

                    # Đánh dấu đã process thành công
                    store.put(cfg.handler_name, message_key)

                    return result

                except Exception as e:
                    # Không đánh dấu đã process nếu có lỗi để message có thể retry
                    raise RuntimeError(
                        f"Handler {cfg.handler_name} failed for key {message_key}"
                    ) from e

            return sync_wrapper

    return decorator


# Helper functions để tạo key extractors phổ biến


def event_id_extractor(event: dict) -> str:
    """Extract event_id từ event dict."""
    if "event_id" not in event:
        raise ValueError("Event không có event_id field")
    return str(event["event_id"])


def message_id_extractor(message: dict) -> str:
    """Extract message_id từ message dict."""
    if "message_id" not in message:
        raise ValueError("Message không có message_id field")
    return str(message["message_id"])


def aggregate_version_extractor(event: dict) -> str:
    """Extract aggregate_id + version từ event."""
    if "aggregate_id" not in event or "version" not in event:
        raise ValueError("Event phải có aggregate_id và version")
    return f"{event['aggregate_id']}:{event['version']}"


# Common configurations
USER_EVENT_CONFIG = IdempotencyConfig(
    handler_name="user_event_handler",
    key_from_event=lambda event: event_id_extractor(event),
)

AGENT_EVENT_CONFIG = IdempotencyConfig(
    handler_name="agent_event_handler",
    key_from_event=lambda event: event_id_extractor(event),
)

TRAINING_EVENT_CONFIG = IdempotencyConfig(
    handler_name="training_event_handler",
    key_from_event=lambda event: event_id_extractor(event),
)

MEMORY_EVENT_CONFIG = IdempotencyConfig(
    handler_name="memory_event_handler",
    key_from_event=lambda event: event_id_extractor(event),
)
