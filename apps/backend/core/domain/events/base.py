"""
Domain Events - Composition Pattern (no inheritance conflicts)
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import asdict, dataclass, field, is_dataclass
from datetime import UTC, datetime
from typing import Any, Generic, TypeVar, cast
from uuid import uuid4
import KeyError
import TypeError
import ValueError
import causation_id
import cls
import correlation_id
import dict
import ev
import hasattr
import int
import isinstance
import obj
import producer
import str
import tenant_id
import type
import version

# ----- Payload registry (composition, no inheritance) -----
T = TypeVar("T")  # payload type

_EVENT_PAYLOAD_REGISTRY: dict[str, type[Any]] = {}


def register_event(event_type: str) -> Callable[[type[Any]], type[Any]]:
    """
    Decorator: đăng ký payload dataclass cho event_type.
    Ví dụ:
        @register_event("AgentCreated")
        @dataclass(frozen=True)
        class AgentCreated: ...
    """

    def _wrap(cls: type[Any]) -> type[Any]:
        _EVENT_PAYLOAD_REGISTRY[event_type] = cls
        cls.__event_type__ = event_type
        return cls

    return _wrap


def get_payload_cls(event_type: str) -> type[Any]:
    try:
        return _EVENT_PAYLOAD_REGISTRY[event_type]
    except KeyError:
        raise KeyError(f"Unregistered event_type: {event_type}")


# ----- Meta + Envelope (composition) -----
@dataclass(frozen=True)
class EventMeta:
    id: str = field(default_factory=lambda: uuid4().hex)
    occurred_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    tenant_id: str | None = None
    correlation_id: str | None = None
    causation_id: str | None = None
    producer: str | None = None
    version: int = 1


@dataclass(frozen=True)
class DomainEvent(Generic[T]):
    """
    Composition pattern:
    - type: tên sự kiện (string)
    - meta: siêu dữ liệu chuẩn
    - data: payload (dataclass thuần), không kế thừa gì cả
    """

    type: str
    meta: EventMeta
    data: T


def make_event(
    event_type: str,
    data: T,
    *,
    tenant_id: str | None = None,
    correlation_id: str | None = None,
    causation_id: str | None = None,
    producer: str | None = None,
    version: int = 1,
) -> DomainEvent[T]:
    return DomainEvent(
        type=event_type,
        meta=EventMeta(
            tenant_id=tenant_id,
            correlation_id=correlation_id,
            causation_id=causation_id,
            producer=producer,
            version=version,
        ),
        data=data,
    )


# ----- (De)serialization helpers for Outbox/EventBus -----
def serialize_event(ev: DomainEvent[Any]) -> dict[str, Any]:
    payload = ev.data
    if is_dataclass(payload) and not isinstance(payload, type):
        payload_dict = asdict(payload)  # type: ignore[arg-type]
    elif hasattr(payload, "model_dump"):  # pydantic payload (optional)
        payload_dict = payload.model_dump()  # type: ignore[attr-defined]
    else:
        raise TypeError("Event payload must be a dataclass or Pydantic model.")
    return {
        "schema": "evt.v1",
        "type": ev.type,
        "meta": asdict(ev.meta),
        "data": payload_dict,
    }


def deserialize_event(obj: dict[str, Any]) -> DomainEvent[Any]:
    if obj.get("schema") != "evt.v1":
        raise ValueError("Unknown event schema")
    event_type = cast(str, obj["type"])
    meta = EventMeta(**obj["meta"])
    payload_cls = get_payload_cls(event_type)
    data = payload_cls(**obj["data"])
    return DomainEvent(type=event_type, meta=meta, data=data)


# Public registry alias cho các nơi khác dùng (OutboxDispatcher)
EVENT_REGISTRY = _EVENT_PAYLOAD_REGISTRY

__all__ = [
    "register_event",
    "get_payload_cls",
    "EventMeta",
    "DomainEvent",
    "make_event",
    "serialize_event",
    "deserialize_event",
    "EVENT_REGISTRY",
]
