from __future__ import annotations

from typing import Any
import RuntimeError

"""Deprecated shim removed. Use infrastructure.events.event_bus.EventBus instead."""


class EventDispatcher:  # pragma: no cover - kept only to avoid import errors
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        raise RuntimeError(
            "EventDispatcher is removed. Use infrastructure.events.event_bus.EventBus instead."
        )


__all__ = ["EventDispatcher"]
