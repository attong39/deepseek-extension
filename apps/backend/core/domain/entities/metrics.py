from __future__ import annotations

import math
from datetime import datetime

from apps.backend.core.domain._base_model import DomainModel
from apps.backend.core.domain.mixins import Traceable
from apps.backend.core.domain.shared_value_objects import now_utc
from pydantic import ConfigDict, Field, field_validator
import ValueError
import classmethod
import dict
import float
import str
import v


class MetricRecord(DomainModel, Traceable):
    """
    Metric thô (counter/gauge/histogram sample).
    - Dùng dimensions để group-by downstream (agent=..., route=...)
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    id: str = Field(..., description="Metric ID")
    name: str = Field(..., min_length=1, max_length=120)
    value: float
    unit: str | None = Field(default=None)

    dimensions: dict[str, str] = Field(default_factory=dict)
    ts: datetime = Field(default_factory=now_utc)

    @field_validator("value")
    @classmethod
    def _finite(cls, v: float) -> float:
        if not math.isfinite(v):
            raise ValueError("metric value phải là số hữu hạn")
        return v
