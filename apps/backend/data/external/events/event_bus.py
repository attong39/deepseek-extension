"""Infrastructure-level Event Bus implementation.





This module hosts the concrete event bus used by adapters/infrastructure.


Domain events live in `core/domain/events/*` and should not import this module.


"""

from __future__ import annotations

import logging
from collections import defaultdict
from collections.abc import Callable
from typing import Any
import Exception
import dict
import exc
import handler
import list
import payload
import self
import str
import topic

logger = logging.getLogger(__name__)


Subscriber = Callable[[str, dict[str, Any]], None]


class EventBus:
    """Simple in-memory pub/sub bus (replace with Redis/Kafka in prod)."""

    def __init__(self) -> None:
        self._subs: dict[str, list[Subscriber]] = defaultdict(list)

    def subscribe(self, topic: str, handler: Subscriber) -> None:
        if handler not in self._subs[topic]:
            self._subs[topic].append(handler)

    def publish(self, topic: str, payload: dict[str, Any]) -> None:
        for handler in self._subs.get(topic, []):
            try:
                handler(topic, payload)

            except Exception as exc:  # pragma: no cover
                logger.exception("event handler failed: %s", exc)


__all__ = ["EventBus"]
