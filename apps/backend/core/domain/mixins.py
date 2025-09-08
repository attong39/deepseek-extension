"""Mixins cho domain entities để tái sử dụng các patterns chung.

Cung cấp các behaviors chung như versioning, ownership, tagging, tracing
và soft deletion cho các domain entities.
"""

from __future__ import annotations

from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, Field
import bool
import int
import list
import self
import set
import str
import tag
import tags
import user_id


def _now_utc() -> datetime:
    """Trả về timestamp UTC hiện tại."""
    return datetime.now(UTC)


class Versioned(BaseModel):
    """Mixin cho optimistic locking với version field."""

    model_config = ConfigDict(frozen=True, extra="forbid")
    version: int = Field(default=1, ge=1, description="Version cho optimistic locking")

    def bump_version(self) -> int:
        """Tăng version number - trả về version mới."""
        return self.version + 1


class Ownable(BaseModel):
    """Mixin cho entities có ownership."""

    model_config = ConfigDict(frozen=True, extra="forbid")
    owner_id: str = Field(description="ID của người sở hữu")
    created_by: str = Field(description="ID của người tạo")

    def is_owned_by(self, user_id: str) -> bool:
        """Kiểm tra entity có thuộc về user không."""
        return self.owner_id == user_id


class Taggable(BaseModel):
    """Mixin cho entities có thể tag."""

    model_config = ConfigDict(frozen=True, extra="forbid")
    tags: list[str] = Field(default_factory=list, description="Danh sách tags")

    def has_tag(self, tag: str) -> bool:
        """Kiểm tra có tag không."""
        return tag in self.tags

    def has_any_tags(self, tags: list[str]) -> bool:
        """Kiểm tra có bất kỳ tag nào trong danh sách không."""
        return bool(set(tags) & set(self.tags))


class Traceable(BaseModel):
    """Mixin cho tracing và audit."""

    model_config = ConfigDict(frozen=True, extra="forbid")
    trace_id: str | None = Field(default=None, description="Trace ID cho observability")
    request_id: str | None = Field(
        default=None, description="Request ID cho correlation"
    )


class SoftDeletable(BaseModel):
    """Mixin cho soft deletion."""

    model_config = ConfigDict(frozen=True, extra="forbid")
    deleted_at: datetime | None = Field(
        default=None, description="Timestamp khi xóa soft"
    )
    is_deleted: bool = Field(default=False, description="Flag đánh dấu đã xóa")

    def is_active(self) -> bool:
        """Kiểm tra entity có active không (chưa bị xóa)."""
        return not self.is_deleted and self.deleted_at is None


class Timestamped(BaseModel):
    """Mixin cho timestamp tracking."""

    model_config = ConfigDict(frozen=True, extra="forbid")
    created_at: datetime = Field(default_factory=_now_utc, description="Timestamp tạo")
    updated_at: datetime = Field(
        default_factory=_now_utc, description="Timestamp cập nhật cuối"
    )


class Auditable(Timestamped, Traceable, Versioned):
    """Mixin kết hợp cho entities cần audit đầy đủ."""

    model_config = ConfigDict(
        frozen=True, extra="forbid", validate_default=True, validate_assignment=True
    )
