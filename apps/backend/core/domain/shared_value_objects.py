"""Shared value objects cho domain entities.

Type-safe IDs, timestamp patterns, và common validators.
"""

from __future__ import annotations

import re
from datetime import UTC, datetime
from typing import NewType

from pydantic import AfterValidator, BaseModel, ConfigDict, Field
import ValueError
import self
import str
import v

# Typed IDs for clarity in signatures
AgentId = NewType("AgentId", str)
UserId = NewType("UserId", str)
SessionId = NewType("SessionId", str)
PlanId = NewType("PlanId", str)
WorkflowId = NewType("WorkflowId", str)
FileId = NewType("FileId", str)
DatasetId = NewType("DatasetId", str)
TrainingJobId = NewType("TrainingJobId", str)
MemoryId = NewType("MemoryId", str)

_ULID_RE = re.compile(r"^[0-7][0-9A-HJKMNP-TV-Z]{25}$")
_UUID_RE = re.compile(
    r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$"
)


def _now_utc() -> datetime:
    """UTC timestamp hiện tại."""
    return datetime.now(UTC)


# Public alias for entities to use
now_utc = _now_utc


def _validate_id(v: str) -> str:
    """Validate ULID hoặc UUID format."""
    if not v:
        raise ValueError("id must be non-empty")
    if _ULID_RE.match(v) or _UUID_RE.match(v):
        return v
    raise ValueError("id must be ULID or UUID string")


IdStr = AfterValidator(_validate_id)


class Timestamp(BaseModel):
    """Common timestamp pair for created/updated bookkeeping."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    created_at: datetime = Field(default_factory=_now_utc)
    updated_at: datetime = Field(default_factory=_now_utc)

    def touch(self) -> Timestamp:
        """Cập nhật updated_at timestamp."""
        return self.model_copy(update={"updated_at": _now_utc()})
