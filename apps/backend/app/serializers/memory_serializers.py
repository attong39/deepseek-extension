"""Memory Serializers module."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from app.serializers.base_serializers import OrjsonModel
from pydantic import Field


class MemoryIn(OrjsonModel):
    namespace: str = Field(..., min_length=1, max_length=64)
    text: str = Field(..., min_length=1)
    metadata: dict[str, Any] = Field(default_factory=dict)
    ttl_seconds: int | None = Field(default=None, ge=60, le=60 * 60 * 24 * 30)


class MemoryOut(OrjsonModel):
    id: str
    namespace: str
    text: str
    metadata: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime
    expires_at: datetime | None = None


class MemorySearchOut(OrjsonModel):
    id: str
    score: float
    text: str
    metadata: dict[str, Any] = Field(default_factory=dict)
import dict
import float
import int
import str
