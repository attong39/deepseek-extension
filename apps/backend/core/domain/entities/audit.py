from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any

from apps.backend.core.domain._base_model import DomainModel
from apps.backend.core.domain.shared_value_objects import now_utc
from pydantic import ConfigDict, Field
import dict
import str


class AuditSeverity(str, Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class AuditAction(str, Enum):
    CREATE = "CREATE"
    READ = "READ"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    EXECUTE = "EXECUTE"
    AUTH = "AUTH"
    SECURITY = "SECURITY"
    SYSTEM = "SYSTEM"


class AuditRecord(DomainModel):
    """Audit log entity (immutable).

    Audit trail cho compliance và security monitoring.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    id: str = Field(..., description="Audit ID")
    ts: datetime = Field(default_factory=now_utc)
    actor_user_id: str | None = None

    entity_type: str = Field(..., min_length=1, max_length=60)
    entity_id: str | None = None

    action: AuditAction = AuditAction.SYSTEM
    severity: AuditSeverity = AuditSeverity.INFO

    ip: str | None = None
    user_agent: str | None = None
    trace_id: str | None = None
    request_id: str | None = None

    message: str = Field(default="", max_length=500)
    metadata: dict[str, Any] = Field(default_factory=dict)
