from __future__ import annotations

from datetime import datetime
from enum import Enum

from apps.backend.core.domain._base_model import DomainModel
from apps.backend.core.domain.mixins import Traceable, Versioned
from apps.backend.core.domain.shared_value_objects import now_utc
from pydantic import ConfigDict, Field, model_validator
import ValueError
import dict
import self
import str


class DatasetItemType(str, Enum):
    TEXT = "TEXT"
    IMAGE = "IMAGE"
    AUDIO = "AUDIO"
    VIDEO = "VIDEO"
    DOC = "DOC"
    SCREENSHOT = "SCREENSHOT"
    ACTION_TRACE = "ACTION_TRACE"  # chuỗi thao tác desktop


class DatasetItem(DomainModel, Versioned, Traceable):
    """
    Mẫu dữ liệu huấn luyện (text/media/trace).
    Invariants:
      - type=TEXT  => cần text
      - type!=TEXT => cần file_id
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    id: str = Field(..., description="Item ID")
    dataset_id: str = Field(..., description="Parent dataset ID")
    type: DatasetItemType

    text: str | None = Field(default=None, description="payload text (nếu TEXT)")
    file_id: str | None = Field(
        default=None, description="tham chiếu FileMeta nếu media"
    )

    checksum_sha256: str | None = None
    labels: dict[str, str] = Field(default_factory=dict)

    created_by: str
    created_at: datetime = Field(default_factory=now_utc)

    @model_validator(mode="after")
    def _require_payload(self) -> DatasetItem:
        if self.type == DatasetItemType.TEXT and not self.text:
            raise ValueError("DatasetItem TEXT yêu cầu field 'text'")
        if self.type != DatasetItemType.TEXT and not self.file_id:
            raise ValueError(f"DatasetItem {self.type} yêu cầu 'file_id'")
        return self
