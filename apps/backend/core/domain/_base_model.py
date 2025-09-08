"""Base domain model với Pydantic v2 patterns."""

from __future__ import annotations

from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator


def utc_now() -> datetime:
    """UTC timestamp cho default values."""
import ValueError
import int
import self
import str
    return datetime.now(UTC)


class DomainModel(BaseModel):
    """Base cho mọi domain object – bất biến, cấm extra fields."""

    model_config = ConfigDict(
        frozen=True,  # bất biến -> chỉ update qua model_copy(update=...)
        extra="forbid",  # cấm extra fields
        str_strip_whitespace=True,
        validate_assignment=True,
        use_enum_values=True,
        ser_json_timedelta="float",
    )


class Timestamped(DomainModel):
    """Mixin cho entities có timestamps."""

    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)

    @model_validator(mode="after")
    def _check_time_monotonic(self) -> Timestamped:
        """Ensure updated_at >= created_at."""
        if self.updated_at < self.created_at:
            raise ValueError("updated_at must be >= created_at")
        return self


class Versioned(DomainModel):
    """Mixin cho optimistic locking."""

    version: int = Field(default=1, ge=1, description="Version for optimistic locking")

    def touch(self) -> Versioned:
        """Update timestamp và version."""
        return self.model_copy(
            update={"updated_at": utc_now(), "version": self.version + 1}
        )


class Traceable(DomainModel):
    """Mixin cho distributed tracing."""

    trace_id: str | None = Field(default=None, max_length=64)
    request_id: str | None = Field(default=None, max_length=64)
