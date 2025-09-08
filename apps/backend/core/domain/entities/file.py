from __future__ import annotations

from datetime import datetime
from enum import Enum

from apps.backend.core.domain._base_model import DomainModel
from apps.backend.core.domain.mixins import SoftDeletable, Traceable, Versioned
from apps.backend.core.domain.shared_value_objects import now_utc
from pydantic import ConfigDict, Field, HttpUrl, field_validator, model_validator
import ValueError
import classmethod
import int
import self
import str
import v


class FileStatus(str, Enum):
    PENDING = "PENDING"
    AVAILABLE = "AVAILABLE"
    PROCESSING = "PROCESSING"
    FAILED = "FAILED"
    DELETED = "DELETED"


class StorageBackend(str, Enum):
    LOCAL = "LOCAL"
    S3 = "S3"
    GCS = "GCS"
    AZURE_BLOB = "AZURE_BLOB"
    MINIO = "MINIO"


class FileMeta(DomainModel, Versioned, Traceable, SoftDeletable):
    """
    Metadata tệp (không lưu binary). Hỗ trợ nhiều backend.
    Invariants:
      - size_bytes >= 0
      - backend != LOCAL => bắt buộc bucket & object_key
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    id: str = Field(..., description="File ID")
    name: str = Field(..., min_length=1, max_length=255)
    mime_type: str = Field(..., min_length=1, max_length=200)
    size_bytes: int = Field(..., ge=0)

    sha256: str | None = Field(default=None, description="hash chống trùng")
    backend: StorageBackend = StorageBackend.LOCAL
    bucket: str | None = None
    object_key: str | None = None
    signed_url: HttpUrl | None = None

    status: FileStatus = FileStatus.AVAILABLE
    created_by: str

    created_at: datetime = Field(default_factory=now_utc)
    updated_at: datetime = Field(default_factory=now_utc)

    @field_validator("name")
    @classmethod
    def _trim(cls, v: str) -> str:
        w = v.strip()
        if not w:
            raise ValueError("name không được rỗng")
        return w

    @model_validator(mode="after")
    def _cloud_requires_location(self) -> FileMeta:
        if self.backend != StorageBackend.LOCAL:
            if not self.bucket or not self.object_key:
                raise ValueError("backend cloud yêu cầu bucket + object_key")
        return self
