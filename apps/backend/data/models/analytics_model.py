"""Analytics model for tracking system metrics and user behavior."""

from __future__ import annotations

from apps.backend.data.models.base_model import FullFeaturedBaseModel
from sqlalchemy import JSON, Column, DateTime, Float, Integer, String


class AnalyticsEvent(FullFeaturedBaseModel):
    """Analytics event tracking model."""
import self
import str

    __tablename__: str = "analytics_events"

    event_type = Column(
        String(100), nullable=False, index=True, doc="Type of event being tracked"
    )
    event_name = Column(
        String(255), nullable=False, index=True, doc="Name of the specific event"
    )
    user_id = Column(
        String(36),
        nullable=True,
        index=True,
        doc="ID of the user who triggered the event",
    )
    session_id = Column(
        String(36), nullable=True, index=True, doc="Session ID when event occurred"
    )
    agent_id = Column(
        String(36),
        nullable=True,
        index=True,
        doc="Agent ID if event relates to an agent",
    )

    # Event data
    properties = Column(
        JSON, nullable=True, doc="Event-specific properties and metadata"
    )
    context = Column(JSON, nullable=True, doc="Context information when event occurred")

    # Metrics
    value = Column(Float, nullable=True, doc="Numeric value associated with the event")
    duration_ms = Column(
        Integer, nullable=True, doc="Duration of the event in milliseconds"
    )

    # Timestamps
    timestamp = Column(
        DateTime, nullable=False, index=True, doc="When the event occurred"
    )

    def __repr__(self) -> str:
        """String representation."""
        return f"<AnalyticsEvent(id={self.id}, type={self.event_type}, name={self.event_name})>"


class PerformanceMetric(FullFeaturedBaseModel):
    """Performance metrics tracking model."""

    __tablename__: str = "performance_metrics"

    metric_name = Column(
        String(100), nullable=False, index=True, doc="Name of the performance metric"
    )
    metric_type = Column(
        String(50),
        nullable=False,
        index=True,
        doc="Type of metric (counter, gauge, histogram)",
    )

    # Values
    value = Column(Float, nullable=False, doc="Metric value")
    tags = Column(JSON, nullable=True, doc="Tags for metric filtering and grouping")

    # Context
    component = Column(
        String(100),
        nullable=True,
        index=True,
        doc="Component that generated the metric",
    )
    endpoint = Column(
        String(255), nullable=True, index=True, doc="API endpoint if applicable"
    )
    method = Column(
        String(20), nullable=True, index=True, doc="HTTP method if applicable"
    )

    # Timestamps
    timestamp = Column(
        DateTime, nullable=False, index=True, doc="When the metric was recorded"
    )

    def __repr__(self) -> str:
        """String representation."""
        return f"<PerformanceMetric(name={self.metric_name}, value={self.value})>"


class UsageStats(FullFeaturedBaseModel):
    """Usage statistics aggregation model."""

    __tablename__: str = "usage_stats"

    period_type = Column(
        String(20),
        nullable=False,
        index=True,
        doc="Type of aggregation period (daily, weekly, monthly)",
    )
    period_start = Column(
        DateTime, nullable=False, index=True, doc="Start of the aggregation period"
    )
    period_end = Column(
        DateTime, nullable=False, index=True, doc="End of the aggregation period"
    )

    # Aggregated stats
    total_requests = Column(
        Integer, nullable=False, default=0, doc="Total number of requests in period"
    )
    total_users = Column(
        Integer, nullable=False, default=0, doc="Total number of unique users in period"
    )
    total_agents = Column(
        Integer,
        nullable=False,
        default=0,
        doc="Total number of agents active in period",
    )
    total_conversations = Column(
        Integer, nullable=False, default=0, doc="Total conversations in period"
    )
    total_messages = Column(
        Integer, nullable=False, default=0, doc="Total messages in period"
    )

    # Performance stats
    avg_response_time = Column(
        Float, nullable=True, doc="Average response time in milliseconds"
    )
    error_rate = Column(Float, nullable=True, doc="Error rate as percentage (0-100)")

    # Additional metrics
    metrics = Column(JSON, nullable=True, doc="Additional aggregated metrics")

    def __repr__(self) -> str:
        """String representation."""
        return f"<UsageStats(period={self.period_type}, start={self.period_start})>"
