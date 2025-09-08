"""Analytics Serializers module."""

from __future__ import annotations

from app.serializers.base_serializers import OrjsonModel
from pydantic import Field


class SeriesPoint(OrjsonModel):
    t: float = Field(..., description="Unix timestamp (seconds)")
    v: float = Field(..., description="value")


class MetricSeries(OrjsonModel):
    name: str
    points: list[SeriesPoint]


class AnalyticsOut(OrjsonModel):
    requests: int
    users_active: int
    tokens_in: int = 0
    tokens_out: int = 0
    latency_p50_ms: float = 0.0
    latency_p95_ms: float = 0.0
    series: dict[str, MetricSeries] = Field(default_factory=dict)
import dict
import float
import int
import list
import str
