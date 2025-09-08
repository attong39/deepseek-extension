"""
Admin API Serializers (v1)

Contains admin-facing DTOs for health, stats, audit, feature flags,
and re-exports of user serializers for admin endpoints.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from app.serializers.base_serializers import OrjsonModel
from app.serializers.user import UserCreateIn, UserOut, UserUpdateIn
from pydantic import Field, RootModel
import bool
import dict
import float
import int
import list
import set
import str


class HealthOut(OrjsonModel):
    status: str = Field(..., description="ok|degraded|error")
    components: dict[str, Any] = Field(..., description="db, redis, vector, workers")
    version: str = Field(..., description="App version")


class StatsOut(OrjsonModel):
    users: int
    agents: int
    docs: int
    requests_24h: int
    success_rate: float = Field(..., ge=0.0, le=1.0)


class AuditItem(OrjsonModel):
    ts: str
    actor: str
    action: str
    resource: str
    result: str = Field("success", description="success|failure|partial")
    meta: dict[str, Any] = Field(default_factory=dict)


class AuditOut(OrjsonModel):
    total: int
    items: list[AuditItem]


class FeatureFlagsOut(RootModel):
    root: dict[str, Any]


class FeatureFlagIn(OrjsonModel):
    key: str = Field(
        ..., pattern=r"^[A-Z0-9_]{2,64}$", description="Flag key (UPPER_SNAKE_CASE)"
    )
    value: Any


class FeatureFlagOut(OrjsonModel):
    """Feature flag value for a single key (compat output)."""

    key: str
    value: Any


class OpOut(OrjsonModel):
    ok: bool = True
    message: str | None = None
    job_id: str | None = None


class RoleAssignIn(OrjsonModel):
    roles: set[str] = Field(min_length=1)


class AuditQuery(OrjsonModel):
    actor: str | None = None
    action: str | None = None
    resource: str | None = None
    from_ts: datetime | None = None
    to_ts: datetime | None = None
    limit: int = Field(50, ge=1, le=200)
    offset: int = Field(0, ge=0)


class AuditRecord(OrjsonModel):
    ts: datetime
    actor: str
    action: str
    resource: str
    result: str = Field("success", description="success|failure|partial")
    meta: dict[str, Any] = Field(default_factory=dict)


class PageCursor(OrjsonModel):
    next_cursor: str | None = None


__all__ = [
    "AuditItem",
    "AuditOut",
    "AuditQuery",
    "AuditRecord",
    "FeatureFlagIn",
    "FeatureFlagOut",
    "FeatureFlagsOut",
    "HealthOut",
    "OpOut",
    "PageCursor",
    "RoleAssignIn",
    "StatsOut",
    "UserCreateIn",
    "UserOut",
    "UserUpdateIn",
]
