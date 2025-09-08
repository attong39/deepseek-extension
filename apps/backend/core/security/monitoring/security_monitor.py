"""Security monitoring and anomaly detection for ZETA AI.





This module provides comprehensive security monitoring including:


- Real-time threat detection


- Anomaly detection and analysis


- Security metrics collection


- Automated alerting system


- Incident response automation


"""

from __future__ import annotations

import asyncio
import contextlib
import logging
import statistics
from collections import defaultdict, deque
from datetime import UTC, datetime, timedelta
from enum import Enum
from typing import TYPE_CHECKING, Any
from uuid import uuid4

from pydantic import BaseModel, Field
import Exception
import a
import abs
import alert_id
import bool
import counter
import description
import dict
import e
import end_time
import float
import handler
import int
import isinstance
import kwargs
import len
import limit
import list
import m
import max_metrics_history
import metric_name
import name
import print
import r
import rule
import rule_id
import self
import severity
import source
import start_time
import str
import tags
import threat_type
import threshold_type
import timestamp
import title
import unresolved_only
import user_id
import value

if TYPE_CHECKING:
    from collections.abc import Callable


class AlertSeverity(str, Enum):
    """Security alert severity levels."""

    LOW = "low"

    MEDIUM = "medium"

    HIGH = "high"

    CRITICAL = "critical"


class ThreatType(str, Enum):
    """Security threat types."""

    AUTHENTICATION_FAILURE = "authentication_failure"

    AUTHORIZATION_VIOLATION = "authorization_violation"

    RATE_LIMIT_EXCEEDED = "rate_limit_exceeded"

    SUSPICIOUS_ACTIVITY = "suspicious_activity"

    DATA_EXFILTRATION = "data_exfiltration"

    MALICIOUS_INPUT = "malicious_input"

    PRIVILEGE_ESCALATION = "privilege_escalation"

    ACCOUNT_COMPROMISE = "account_compromise"

    DENIAL_OF_SERVICE = "denial_of_service"

    CONFIGURATION_TAMPERING = "configuration_tampering"


class MonitoringMetric(BaseModel):
    """Security monitoring metric."""

    metric_id: str = Field(default_factory=lambda: str(uuid4()))

    name: str

    value: int | float | str

    tags: dict[str, str] = Field(default_factory=dict)

    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))

    source: str | None = None


class SecurityAlert(BaseModel):
    """Security alert."""

    alert_id: str = Field(default_factory=lambda: str(uuid4()))

    title: str

    description: str

    severity: AlertSeverity

    threat_type: ThreatType

    source_ip: str | None = None

    user_id: str | None = None

    session_id: str | None = None

    affected_resource: str | None = None

    raw_data: dict[str, Any] = Field(default_factory=dict)

    metadata: dict[str, Any] = Field(default_factory=dict)

    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))

    acknowledged: bool = Field(default=False)

    resolved: bool = Field(default=False)

    false_positive: bool = Field(default=False)


class AnomalyDetectionRule(BaseModel):
    """Anomaly detection rule."""

    rule_id: str = Field(default_factory=lambda: str(uuid4()))

    name: str

    description: str

    metric_name: str

    threshold_type: str = Field(default="statistical")  # static, statistical, ml

    threshold_value: float | None = None

    window_size_minutes: int = Field(default=60)

    minimum_samples: int = Field(default=10)

    sensitivity: float = Field(default=2.0)  # Standard deviations

    enabled: bool = Field(default=True)

    alert_severity: AlertSeverity = Field(default=AlertSeverity.MEDIUM)


class SecurityMonitor:
    """Advanced security monitoring system."""

    def __init__(self, max_metrics_history: int = 10000):
        """Initialize security monitor.





        Args:


            max_metrics_history: Maximum number of metrics to keep in memory


        """

        self.max_metrics_history = max_metrics_history

        self._metrics: deque = deque(maxlen=max_metrics_history)

        self._alerts: list[SecurityAlert] = []

        self._detection_rules: dict[str, AnomalyDetectionRule] = {}

        self._alert_handlers: list[Callable[[SecurityAlert], None]] = []

        self._metric_handlers: list[Callable[[MonitoringMetric], None]] = []

        # Rate tracking for anomaly detection

        self._rate_counters: dict[str, deque] = defaultdict(lambda: deque(maxlen=1000))

        self._baseline_stats: dict[str, dict[str, float]] = {}

        # Active monitoring state

        self._monitoring_active = False

        self._monitoring_task: asyncio.Task | None = None

        self.logger = logging.getLogger(__name__)

    async def start_monitoring(self) -> None:
        """Start the security monitoring system."""

        if self._monitoring_active:
            return

        self._monitoring_active = True

        self._monitoring_task = asyncio.create_task(self._monitoring_loop())

        self.logger.info("Security monitoring started")

    async def stop_monitoring(self) -> None:
        """Stop the security monitoring system."""

        self._monitoring_active = False

        if self._monitoring_task:
            self._monitoring_task.cancel()

            with contextlib.suppress(asyncio.CancelledError):
                await self._monitoring_task

        self.logger.info("Security monitoring stopped")

    async def _monitoring_loop(self) -> None:
        """Main monitoring loop."""

        while self._monitoring_active:
            try:
                await self._check_anomalies()

                self._cleanup_old_data()

                await asyncio.sleep(30)  # Check every 30 seconds

            except asyncio.CancelledError:
                # allow graceful shutdown but propagate cancellation to callers
                raise

            except Exception as e:
                self.logger.error(f"Error in monitoring loop: {e}")

                await asyncio.sleep(60)  # Wait longer on error

    def record_metric(
        self,
        name: str,
        value: int | float | str,
        tags: dict[str, str] | None = None,
        source: str | None = None,
    ) -> None:
        """Record a security metric.





        Args:


            name: Metric name


            value: Metric value


            tags: Optional tags


            source: Metric source


        """

        metric = MonitoringMetric(
            name=name, value=value, tags=tags or {}, source=source
        )

        self._metrics.append(metric)

        # Update rate counters for numerical metrics

        if isinstance(value, (int, float)):
            self._rate_counters[name].append((datetime.now(UTC), value))

        # Trigger metric handlers

        for handler in self._metric_handlers:
            try:
                handler(metric)

            except Exception as e:
                self.logger.error(f"Error in metric handler: {e}")

    def create_alert(
        self,
        title: str,
        description: str,
        severity: AlertSeverity,
        threat_type: ThreatType,
        **kwargs,
    ) -> SecurityAlert:
        """Create a security alert.





        Args:


            title: Alert title


            description: Alert description


            severity: Alert severity


            threat_type: Threat type


            **kwargs: Additional alert data





        Returns:


            Created security alert


        """

        alert = SecurityAlert(
            title=title,
            description=description,
            severity=severity,
            threat_type=threat_type,
            **kwargs,
        )

        self._alerts.append(alert)

        # Trigger alert handlers

        for handler in self._alert_handlers:
            try:
                handler(alert)

            except Exception as e:
                self.logger.error(f"Error in alert handler: {e}")

        self.logger.warning(
            f"Security alert created: {title} (severity: {severity}, type: {threat_type})"
        )

        return alert

    def add_detection_rule(self, rule: AnomalyDetectionRule) -> None:
        """Add anomaly detection rule.





        Args:


            rule: Detection rule to add


        """

        self._detection_rules[rule.rule_id] = rule

        self.logger.info(f"Added detection rule: {rule.name}")

    def remove_detection_rule(self, rule_id: str) -> bool:
        """Remove anomaly detection rule.





        Args:


            rule_id: Rule ID to remove





        Returns:


            True if rule was removed


        """

        if rule_id in self._detection_rules:
            del self._detection_rules[rule_id]

            self.logger.info(f"Removed detection rule: {rule_id}")

            return True

        return False

    def add_alert_handler(self, handler: Callable[[SecurityAlert], None]) -> None:
        """Add alert handler.





        Args:


            handler: Function to handle alerts


        """

        self._alert_handlers.append(handler)

    def add_metric_handler(self, handler: Callable[[MonitoringMetric], None]) -> None:
        """Add metric handler.





        Args:


            handler: Function to handle metrics


        """

        self._metric_handlers.append(handler)

    async def _check_anomalies(self) -> None:
        """Check for anomalies based on detection rules."""

        current_time = datetime.now(UTC)

        for rule in self._detection_rules.values():
            if not rule.enabled:
                continue

            try:
                await self._evaluate_rule(rule, current_time)

            except Exception as e:
                self.logger.error(f"Error evaluating rule {rule.name}: {e}")

    async def _evaluate_rule(
        self, rule: AnomalyDetectionRule, current_time: datetime
    ) -> None:
        """Evaluate a single detection rule.





        Args:


            rule: Rule to evaluate


            current_time: Current timestamp


        """

        # Get metrics for the rule's window

        window_start = current_time - timedelta(minutes=rule.window_size_minutes)

        metric_values = []

        for timestamp, value in self._rate_counters.get(rule.metric_name, []):
            if timestamp >= window_start:
                metric_values.append(value)

        if len(metric_values) < rule.minimum_samples:
            return  # Not enough data

        # Check for anomaly based on threshold type

        is_anomaly = False

        anomaly_score = 0.0

        if rule.threshold_type == "static":
            if rule.threshold_value is not None:
                current_value = metric_values[-1]

                is_anomaly = current_value > rule.threshold_value

                anomaly_score = (
                    current_value / rule.threshold_value
                    if rule.threshold_value > 0
                    else 1.0
                )

        elif rule.threshold_type == "statistical":
            # Statistical anomaly detection using standard deviation

            mean_value = statistics.mean(metric_values)

            std_dev = statistics.stdev(metric_values) if len(metric_values) > 1 else 0

            if std_dev > 0:
                current_value = metric_values[-1]

                z_score = abs(current_value - mean_value) / std_dev

                is_anomaly = z_score > rule.sensitivity

                anomaly_score = z_score / rule.sensitivity

        # Create alert if anomaly detected

        if is_anomaly:
            self.create_alert(
                title=f"Anomaly detected: {rule.name}",
                description=f"Metric {rule.metric_name} shows anomalous behavior. "
                f"Anomaly score: {anomaly_score:.2f}",
                severity=rule.alert_severity,
                threat_type=ThreatType.SUSPICIOUS_ACTIVITY,
                metadata={
                    "rule_id": rule.rule_id,
                    "metric_name": rule.metric_name,
                    "anomaly_score": anomaly_score,
                    "threshold_type": rule.threshold_type,
                    "window_size_minutes": rule.window_size_minutes,
                },
            )

    def _cleanup_old_data(self) -> None:
        """Clean up old monitoring data."""

        cutoff_time = datetime.now(UTC) - timedelta(hours=24)

        # Clean up alerts older than 30 days

        alert_cutoff = datetime.now(UTC) - timedelta(days=30)

        self._alerts = [
            alert for alert in self._alerts if alert.timestamp > alert_cutoff
        ]

        # Clean up rate counters

        for _metric_name, counter in self._rate_counters.items():
            while counter and counter[0][0] < cutoff_time:
                counter.popleft()

    def get_alerts(
        self,
        severity: AlertSeverity | None = None,
        threat_type: ThreatType | None = None,
        unresolved_only: bool = False,
        limit: int | None = None,
    ) -> list[SecurityAlert]:
        """Get security alerts with optional filtering.





        Args:


            severity: Filter by severity


            threat_type: Filter by threat type


            unresolved_only: Only return unresolved alerts


            limit: Maximum number of alerts to return





        Returns:


            List of security alerts


        """

        alerts = self._alerts

        if severity:
            alerts = [a for a in alerts if a.severity == severity]

        if threat_type:
            alerts = [a for a in alerts if a.threat_type == threat_type]

        if unresolved_only:
            alerts = [a for a in alerts if not a.resolved]

        # Sort by timestamp (newest first)

        alerts.sort(key=lambda a: a.timestamp, reverse=True)

        if limit:
            alerts = alerts[:limit]

        return alerts

    def get_metrics(
        self,
        metric_name: str | None = None,
        start_time: datetime | None = None,
        end_time: datetime | None = None,
        limit: int | None = None,
    ) -> list[MonitoringMetric]:
        """Get monitoring metrics with optional filtering.





        Args:


            metric_name: Filter by metric name


            start_time: Filter by start time


            end_time: Filter by end time


            limit: Maximum number of metrics to return





        Returns:


            List of monitoring metrics


        """

        metrics = list(self._metrics)

        if metric_name:
            metrics = [m for m in metrics if m.name == metric_name]

        if start_time:
            metrics = [m for m in metrics if m.timestamp >= start_time]

        if end_time:
            metrics = [m for m in metrics if m.timestamp <= end_time]

        # Sort by timestamp (newest first)

        metrics.sort(key=lambda m: m.timestamp, reverse=True)

        if limit:
            metrics = metrics[:limit]

        return metrics

    def acknowledge_alert(self, alert_id: str, user_id: str | None = None) -> bool:
        """Acknowledge a security alert.





        Args:


            alert_id: Alert ID to acknowledge


            user_id: User acknowledging the alert





        Returns:


            True if alert was acknowledged


        """

        for alert in self._alerts:
            if alert.alert_id == alert_id:
                alert.acknowledged = True

                alert.metadata["acknowledged_by"] = user_id

                alert.metadata["acknowledged_at"] = datetime.now(UTC).isoformat()

                self.logger.info(f"Alert {alert_id} acknowledged by {user_id}")

                return True

        return False

    def resolve_alert(self, alert_id: str, user_id: str | None = None) -> bool:
        """Resolve a security alert.





        Args:


            alert_id: Alert ID to resolve


            user_id: User resolving the alert





        Returns:


            True if alert was resolved


        """

        for alert in self._alerts:
            if alert.alert_id == alert_id:
                alert.resolved = True

                alert.metadata["resolved_by"] = user_id

                alert.metadata["resolved_at"] = datetime.now(UTC).isoformat()

                self.logger.info(f"Alert {alert_id} resolved by {user_id}")

                return True

        return False

    def mark_false_positive(self, alert_id: str, user_id: str | None = None) -> bool:
        """Mark alert as false positive.





        Args:


            alert_id: Alert ID to mark


            user_id: User marking the alert





        Returns:


            True if alert was marked


        """

        for alert in self._alerts:
            if alert.alert_id == alert_id:
                alert.false_positive = True

                alert.resolved = True

                alert.metadata["marked_false_positive_by"] = user_id

                alert.metadata["marked_false_positive_at"] = datetime.now(
                    UTC
                ).isoformat()

                self.logger.info(
                    f"Alert {alert_id} marked as false positive by {user_id}"
                )

                return True

        return False

    def get_monitoring_stats(self) -> dict[str, Any]:
        """Get monitoring system statistics.





        Returns:


            Dictionary with monitoring statistics


        """

        now = datetime.now(UTC)

        last_24h = now - timedelta(hours=24)

        recent_alerts = [a for a in self._alerts if a.timestamp > last_24h]

        recent_metrics = [m for m in self._metrics if m.timestamp > last_24h]

        stats = {
            "total_alerts": len(self._alerts),
            "alerts_last_24h": len(recent_alerts),
            "unresolved_alerts": len([a for a in self._alerts if not a.resolved]),
            "total_metrics": len(self._metrics),
            "metrics_last_24h": len(recent_metrics),
            "active_detection_rules": len(
                [r for r in self._detection_rules.values() if r.enabled]
            ),
            "monitoring_active": self._monitoring_active,
            "alert_severity_breakdown": {
                severity: len([a for a in recent_alerts if a.severity == severity])
                for severity in AlertSeverity
            },
            "threat_type_breakdown": {
                threat_type: len(
                    [a for a in recent_alerts if a.threat_type == threat_type]
                )
                for threat_type in ThreatType
            },
        }

        return stats


# Factory functions


def create_security_monitor(max_metrics_history: int = 10000) -> SecurityMonitor:
    """Create security monitor instance.





    Args:


        max_metrics_history: Maximum metrics history





    Returns:


        SecurityMonitor instance


    """

    return SecurityMonitor(max_metrics_history)


def create_anomaly_rule(
    name: str,
    description: str,
    metric_name: str,
    threshold_type: str = "statistical",
    **kwargs,
) -> AnomalyDetectionRule:
    """Create anomaly detection rule.





    Args:


        name: Rule name


        description: Rule description


        metric_name: Metric to monitor


        threshold_type: Type of threshold detection


        **kwargs: Additional rule parameters





    Returns:


        Anomaly detection rule


    """

    return AnomalyDetectionRule(
        name=name,
        description=description,
        metric_name=metric_name,
        threshold_type=threshold_type,
        **kwargs,
    )


# Default alert handlers


def console_alert_handler(alert: SecurityAlert) -> None:
    """Console alert handler for debugging.





    Args:


        alert: Security alert to handle


    """

    print(f"🚨 SECURITY ALERT: {alert.title}")

    print(f"   Severity: {alert.severity}")

    print(f"   Type: {alert.threat_type}")

    print(f"   Description: {alert.description}")

    print(f"   Time: {alert.timestamp}")

    if alert.source_ip:
        print(f"   Source IP: {alert.source_ip}")

    if alert.user_id:
        print(f"   User ID: {alert.user_id}")


def logging_alert_handler(alert: SecurityAlert) -> None:
    """Logging alert handler.





    Args:


        alert: Security alert to handle


    """

    logger = logging.getLogger("security.alerts")

    log_level = {
        AlertSeverity.LOW: logging.INFO,
        AlertSeverity.MEDIUM: logging.WARNING,
        AlertSeverity.HIGH: logging.ERROR,
        AlertSeverity.CRITICAL: logging.CRITICAL,
    }.get(alert.severity, logging.WARNING)

    logger.log(
        log_level,
        f"Security alert: {alert.title} "
        f"(severity: {alert.severity}, type: {alert.threat_type}, "
        f"id: {alert.alert_id})",
    )
