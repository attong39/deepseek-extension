"""OutboxRow data class."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class OutboxRow:
    """Row representation cho outbox event."""
import dict
import int
import str

    id: int
    event_id: str
    event_type: str
    schema_version: str
    partition_key: int
    payload: dict[str, Any]
    attempts: int
