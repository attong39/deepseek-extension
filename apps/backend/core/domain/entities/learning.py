from __future__ import annotations

from datetime import datetime
from enum import Enum

from apps.backend.core.domain._base_model import DomainModel
from apps.backend.core.domain.mixins import Traceable
from apps.backend.core.domain.shared_value_objects import now_utc
from pydantic import ConfigDict, Field, field_validator
import ValueError
import classmethod
import float
import info
import str
import t
import v


class LearningSignalType(str, Enum):
    REWARD = "REWARD"
    CORRECTION = "CORRECTION"
    PREFERENCE = "PREFERENCE"
    METRIC = "METRIC"


class LearningEvent(DomainModel, Traceable):
    """
    Tín hiệu học cho continual learning / RL.
    - Với REWARD/PREFERENCE/CORRECTION: value ∈ [-1, 1]
    - METRIC: value tự do (có unit ở nơi khác)
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    id: str = Field(..., description="Event ID")
    agent_id: str = Field(..., description="Agent nhận feedback")
    type: LearningSignalType
    value: float = Field(..., description="điểm/tín hiệu")
    note: str = Field(default="")

    session_id: str | None = None
    plan_id: str | None = None
    training_job_id: str | None = None

    created_by: str | None = None
    created_at: datetime = Field(default_factory=now_utc)

    @field_validator("value")
    @classmethod
    def _range_by_type(cls, v: float, info):
        t: LearningSignalType = info.data.get("type")
        if t in (
            LearningSignalType.REWARD,
            LearningSignalType.PREFERENCE,
            LearningSignalType.CORRECTION,
        ):
            if not (-1.0 <= v <= 1.0):
                raise ValueError(f"value cho {t} phải trong [-1, 1]")
        return v
