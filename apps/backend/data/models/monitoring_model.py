"""Monitoring model for tracking system health and performance metrics."""

from __future__ import annotations

from apps.backend.data.models.base_model import FullFeaturedBaseModel
from sqlalchemy import JSON, Column, DateTime, Float, Integer, String, Text


class HealthCheck(FullFeaturedBaseModel):
    """Health check model for tracking system health status."""
import self
import str

    __tablename__: str = "health_checks"

    # Check identification
    check_name = Column(
        String(100), nullable=False, index=True, doc="Name of the health check"
    )
    component = Column(
        String(100), nullable=False, index=True, doc="Component being checked"
    )
    check_type = Column(
        String(50),
        nullable=False,
        index=True,
        doc="Type of health check (database, api, service)",
    )

    # Check result
    status = Column(
        String(20),
        nullable=False,
        index=True,
        doc="Health check status (healthy, unhealthy, degraded)",
    )
    response_time_ms = Column(
        Integer, nullable=True, doc="Response time in milliseconds"
    )

    # Check details
    message = Column(Text, nullable=True, doc="Health check message or description")
    error_message = Column(Text, nullable=True, doc="Error message if check failed")
    details = Column(JSON, nullable=True, doc="Additional health check details")

    # Check configuration
    endpoint = Column(String(255), nullable=True, doc="Endpoint URL if applicable")
    timeout_ms = Column(Integer, nullable=True, doc="Timeout used for the check")

    # Metadata
    version = Column(String(50), nullable=True, doc="Version of the component checked")
    environment = Column(
        String(50), nullable=True, doc="Environment where check was performed"
    )
    tags = Column(JSON, nullable=True, doc="Tags for check categorization")

    # Timing
    checked_at = Column(
        DateTime, nullable=False, index=True, doc="When the health check was performed"
    )

    def __repr__(self) -> str:
        """String representation."""
        return f"<HealthCheck(name={self.check_name}, status={self.status})>"


class SystemMetric(FullFeaturedBaseModel):
    """System metric model for tracking system performance metrics."""

    __tablename__: str = "system_metrics"

    # Metric identification
    metric_name = Column(
        String(100), nullable=False, index=True, doc="Name of the metric"
    )
    metric_type = Column(
        String(50),
        nullable=False,
        index=True,
        doc="Type of metric (counter, gauge, histogram, timer)",
    )
    category = Column(
        String(50),
        nullable=False,
        index=True,
        doc="Metric category (cpu, memory, disk, network)",
    )

    # Metric values
    value = Column(Float, nullable=False, doc="Metric value")
    unit = Column(String(20), nullable=True, doc="Unit of measurement")

    # Context
    host = Column(
        String(255), nullable=True, index=True, doc="Host where metric was collected"
    )
    service = Column(
        String(100), nullable=True, index=True, doc="Service that generated the metric"
    )
    component = Column(
        String(100),
        nullable=True,
        index=True,
        doc="Component that generated the metric",
    )

    # Additional data
    dimensions = Column(
        JSON, nullable=True, doc="Metric dimensions for filtering and grouping"
    )
    metadata_info = Column(JSON, nullable=True, doc="Additional metric metadata")

    # Timing
    timestamp = Column(
        DateTime, nullable=False, index=True, doc="When the metric was recorded"
    )

    def __repr__(self) -> str:
        """String representation."""
        return f"<SystemMetric(name={self.metric_name}, value={self.value}, unit={self.unit})>"


class Alert(FullFeaturedBaseModel):
    """Alert model for tracking system alerts and notifications."""

    __tablename__: str = "alerts"

    # Alert identification
    alert_name = Column(
        String(255), nullable=False, index=True, doc="Name of the alert"
    )
    alert_type = Column(
        String(50),
        nullable=False,
        index=True,
        doc="Type of alert (metric, health, custom)",
    )
    severity = Column(
        String(20),
        nullable=False,
        index=True,
        doc="Alert severity (low, medium, high, critical)",
    )

    # Alert details
    title = Column(String(500), nullable=False, doc="Alert title")
    description = Column(Text, nullable=False, doc="Alert description")
    message = Column(Text, nullable=True, doc="Detailed alert message")

    # Alert source
    source_component = Column(
        String(100), nullable=True, index=True, doc="Component that triggered the alert"
    )
    source_service = Column(
        String(100), nullable=True, index=True, doc="Service that triggered the alert"
    )
    metric_name = Column(
        String(100), nullable=True, index=True, doc="Metric that triggered the alert"
    )

    # Alert state
    status = Column(
        String(20),
        nullable=False,
        default="open",
        index=True,
        doc="Alert status (open, acknowledged, resolved)",
    )
    acknowledged_at = Column(
        DateTime, nullable=True, doc="When the alert was acknowledged"
    )
    acknowledged_by = Column(
        String(36), nullable=True, doc="Who acknowledged the alert"
    )
    resolved_at = Column(DateTime, nullable=True, doc="When the alert was resolved")
    resolved_by = Column(String(36), nullable=True, doc="Who resolved the alert")

    # Alert conditions
    threshold_value = Column(
        Float, nullable=True, doc="Threshold value that triggered the alert"
    )
    actual_value = Column(
        Float, nullable=True, doc="Actual value when alert was triggered"
    )
    condition = Column(
        String(50),
        nullable=True,
        doc="Alert condition (greater_than, less_than, equals)",
    )

    # Notification
    notification_sent = Column(
        String(20),
        nullable=False,
        default="pending",
        doc="Notification status (pending, sent, failed)",
    )
    notification_channels = Column(
        JSON, nullable=True, doc="Channels where notifications were sent"
    )

    # Additional data
    alert_data = Column(JSON, nullable=True, doc="Additional alert data")
    tags = Column(JSON, nullable=True, doc="Tags for alert categorization")

    # Timing
    triggered_at = Column(
        DateTime, nullable=False, index=True, doc="When the alert was triggered"
    )

    def __repr__(self) -> str:
        """String representation."""
        return f"<Alert(name={self.alert_name}, severity={self.severity}, status={self.status})>"


class ServiceStatus(FullFeaturedBaseModel):
    """Service status model for tracking overall service health."""

    __tablename__: str = "service_status"

    # Service identification
    service_name = Column(
        String(100), nullable=False, index=True, doc="Name of the service"
    )
    component = Column(String(100), nullable=True, index=True, doc="Service component")
    version = Column(String(50), nullable=True, doc="Service version")

    # Status information
    status = Column(
        String(20),
        nullable=False,
        index=True,
        doc="Service status (operational, degraded, outage)",
    )
    health_score = Column(Integer, nullable=True, doc="Overall health score (0-100)")

    # Service details
    description = Column(Text, nullable=True, doc="Service description")
    status_message = Column(Text, nullable=True, doc="Current status message")

    # Metrics summary
    uptime_percentage = Column(
        Float, nullable=True, doc="Uptime percentage for the period"
    )
    avg_response_time_ms = Column(
        Integer, nullable=True, doc="Average response time in milliseconds"
    )
    error_rate = Column(Float, nullable=True, doc="Error rate as percentage")

    # Dependencies
    dependencies = Column(
        JSON, nullable=True, doc="Service dependencies and their status"
    )
    dependent_services = Column(
        JSON, nullable=True, doc="Services that depend on this service"
    )

    # Metadata
    environment = Column(
        String(50), nullable=True, doc="Environment (dev, staging, prod)"
    )
    tags = Column(JSON, nullable=True, doc="Tags for service categorization")

    # Timing
    last_updated = Column(
        DateTime, nullable=False, index=True, doc="When the status was last updated"
    )

    def __repr__(self) -> str:
        """String representation."""
        return f"<ServiceStatus(service={self.service_name}, status={self.status})>"
