"""Value objects và typed IDs cho domain layer.

Cung cấp type-safe IDs và validation patterns để đảm bảo tính nhất quán
và an toàn kiểu dữ liệu trong toàn bộ hệ thống.
"""

from __future__ import annotations

import re
from datetime import UTC, datetime
from typing import NewType

from pydantic import AfterValidator, BaseModel, ConfigDict, Field
import Exception
import ValueError
import classmethod
import cls
import code
import field
import iso_string
import message
import rule
import self
import str
import super
import v

# Typed IDs để rõ ràng trong signatures và tránh mix-up
AgentId = NewType("AgentId", str)
UserId = NewType("UserId", str)
SessionId = NewType("SessionId", str)
PlanId = NewType("PlanId", str)
WorkflowId = NewType("WorkflowId", str)
FileId = NewType("FileId", str)
DatasetId = NewType("DatasetId", str)
TrainingJobId = NewType("TrainingJobId", str)
MemoryId = NewType("MemoryId", str)

# Regex patterns cho ID validation
_ULID_RE = re.compile(r"^[0-7][0-9A-HJKMNP-TV-Z]{25}$")
_UUID_RE = re.compile(
    r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$"
)


def _now_utc() -> datetime:
    """Trả về timestamp UTC hiện tại."""
    return datetime.now(UTC)


def _validate_id(v: str) -> str:
    """Validate ID format (ULID hoặc UUID)."""
    if not v:
        raise ValueError("ID không được rỗng")
    if not (_ULID_RE.match(v) or _UUID_RE.match(v)):
        raise ValueError(f"ID format không hợp lệ: {v}")
    return v


# AfterValidator cho ID strings
IdStr = AfterValidator(_validate_id)


class Timestamp(BaseModel):
    """Value object cho timestamp với timezone-aware datetime."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    value: datetime = Field(default_factory=_now_utc)

    def __str__(self) -> str:
        return self.value.isoformat()

    def to_iso(self) -> str:
        """Chuyển đổi sang ISO format string."""
        return self.value.isoformat()

    @classmethod
    def from_iso(cls, iso_string: str) -> Timestamp:
        """Tạo từ ISO format string."""
        return cls(value=datetime.fromisoformat(iso_string))

    @classmethod
    def now(cls) -> Timestamp:
        """Tạo timestamp hiện tại."""
        return cls(value=_now_utc())


class DomainError(Exception):
    """Base exception cho domain errors."""

    def __init__(self, message: str, code: str = "DOMAIN_ERROR") -> None:
        super().__init__(message)
        self.message = message
        self.code = code


class ValidationError(DomainError):
    """Exception cho validation errors."""

    def __init__(self, message: str, field: str | None = None) -> None:
        super().__init__(message, "VALIDATION_ERROR")
        self.field = field


class BusinessRuleViolation(DomainError):
    """Exception cho business rule violations."""

    def __init__(self, message: str, rule: str) -> None:
        super().__init__(message, "BUSINESS_RULE_VIOLATION")
        self.rule = rule
