from __future__ import annotations

from datetime import datetime
from enum import Enum

from apps.backend.core.domain._base_model import DomainModel
from apps.backend.core.domain.mixins import Traceable
from apps.backend.core.domain.shared_value_objects import now_utc
from pydantic import ConfigDict, Field
import self
import str


class NotificationLevel(str, Enum):
    INFO = "INFO"
    SUCCESS = "SUCCESS"
    WARNING = "WARNING"
    ERROR = "ERROR"


class NotificationType(str, Enum):
    SYSTEM = "SYSTEM"
    TRAINING = "TRAINING"
    WORKFLOW = "WORKFLOW"
    SECURITY = "SECURITY"


class Notification(DomainModel, Traceable):
    """
    Thông báo tới user (toast/bell/WebSocket).
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    id: str = Field(..., description="Notification ID")
    user_id: str = Field(..., description="Target user")

    title: str = Field(..., min_length=1, max_length=120)
    message: str = Field(..., min_length=1, max_length=2000)

    level: NotificationLevel = NotificationLevel.INFO
    type: NotificationType = NotificationType.SYSTEM

    related_id: str | None = None
    read_at: datetime | None = None
    created_at: datetime = Field(default_factory=now_utc)

    def mark_read(self) -> Notification:
        return self.model_copy(update={"read_at": now_utc()})
