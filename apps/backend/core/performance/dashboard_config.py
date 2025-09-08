"""
Performance Dashboard Configuration - Real-time monitoring và alerting.

Cấu hình:
- Grafana dashboards cho performance metrics
- Prometheus alerting rules
- Performance KPIs và thresholds
- Auto-scaling triggers
- Performance regression detection
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any
import color
import dict
import enumerate
import float
import group_name
import i
import int
import len
import list
import metric_groups
import metric_name
import panel
import self
import set
import severity
import str
import threshold
import thresholds
import zip


class AlertSeverity(Enum):
    """Alert severity levels."""

    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"
    EMERGENCY = "emergency"


class MetricType(Enum):
    """Types of performance metrics."""

    LATENCY = "latency"
    THROUGHPUT = "throughput"
    ERROR_RATE = "error_rate"
    RESOURCE_USAGE = "resource_usage"
    CACHE_HIT_RATE = "cache_hit_rate"


@dataclass(slots=True)
class PerformanceThreshold:
    """Performance threshold configuration."""

    metric_name: str
    threshold_value: float
    comparison_operator: str  # >, <, >=, <=, ==
    severity: AlertSeverity
    duration_seconds: int = 60  # How long threshold must be breached
    description: str = ""


@dataclass(slots=True)
class DashboardPanel:
    """Grafana dashboard panel configuration."""

    title: str
    metric_query: str
    panel_type: str  # graph, singlestat, table, etc.
    unit: str = ""
    thresholds: list[float] = field(default_factory=list)
    colors: list[str] = field(default_factory=list)
    grid_pos: dict[str, int] = field(default_factory=dict)


@dataclass(slots=True)
class PerformanceDashboardConfig:
    """Complete performance dashboard configuration."""

    # Dashboard metadata
    dashboard_title: str = "ZETA Performance Monitoring"
    refresh_interval: str = "30s"
    time_range: str = "1h"

    # Performance thresholds
    thresholds: list[PerformanceThreshold] = field(default_factory=list)

    # Dashboard panels
    panels: list[DashboardPanel] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Initialize default thresholds and panels."""
        if not self.thresholds:
            self._setup_default_thresholds()

        if not self.panels:
            self._setup_default_panels()

    def _setup_default_thresholds(self) -> None:
        """Setup default performance thresholds."""
        self.thresholds.extend(
            [
                # Latency thresholds
                PerformanceThreshold(
                    metric_name="api_request_duration_p95",
                    threshold_value=2000.0,  # 2 seconds
                    comparison_operator=">",
                    severity=AlertSeverity.WARNING,
                    duration_seconds=120,
                    description="API P95 latency exceeding 2 seconds",
                ),
                PerformanceThreshold(
                    metric_name="api_request_duration_p95",
                    threshold_value=5000.0,  # 5 seconds
                    comparison_operator=">",
                    severity=AlertSeverity.CRITICAL,
                    duration_seconds=60,
                    description="API P95 latency exceeding 5 seconds",
                ),
                # Throughput thresholds
                PerformanceThreshold(
                    metric_name="api_requests_per_second",
                    threshold_value=100.0,
                    comparison_operator="<",
                    severity=AlertSeverity.WARNING,
                    duration_seconds=300,
                    description="API throughput below 100 RPS",
                ),
                # Error rate thresholds
                PerformanceThreshold(
                    metric_name="api_error_rate_percent",
                    threshold_value=5.0,
                    comparison_operator=">",
                    severity=AlertSeverity.WARNING,
                    duration_seconds=60,
                    description="API error rate exceeding 5%",
                ),
                PerformanceThreshold(
                    metric_name="api_error_rate_percent",
                    threshold_value=10.0,
                    comparison_operator=">",
                    severity=AlertSeverity.CRITICAL,
                    duration_seconds=30,
                    description="API error rate exceeding 10%",
                ),
                # Resource usage thresholds
                PerformanceThreshold(
                    metric_name="system_cpu_percent",
                    threshold_value=80.0,
                    comparison_operator=">",
                    severity=AlertSeverity.WARNING,
                    duration_seconds=300,
                    description="CPU usage exceeding 80%",
                ),
                PerformanceThreshold(
                    metric_name="system_memory_percent",
                    threshold_value=85.0,
                    comparison_operator=">",
                    severity=AlertSeverity.WARNING,
                    duration_seconds=300,
                    description="Memory usage exceeding 85%",
                ),
                # Cache performance thresholds
                PerformanceThreshold(
                    metric_name="cache_hit_rate_percent",
                    threshold_value=80.0,
                    comparison_operator="<",
                    severity=AlertSeverity.WARNING,
                    duration_seconds=600,
                    description="Cache hit rate below 80%",
                ),
            ]
        )

    def _setup_default_panels(self) -> None:
        """Setup default dashboard panels."""
        self.panels.extend(
            [
                # API Latency Panel
                DashboardPanel(
                    title="API Response Time (P95)",
                    metric_query="histogram_quantile(0.95, rate(api_request_duration_seconds_bucket[5m]))",
                    panel_type="graph",
                    unit="ms",
                    thresholds=[2000, 5000],
                    colors=["green", "yellow", "red"],
                    grid_pos={"h": 8, "w": 12, "x": 0, "y": 0},
                ),
                # Throughput Panel
                DashboardPanel(
                    title="API Requests per Second",
                    metric_query="rate(api_requests_total[5m])",
                    panel_type="graph",
                    unit="reqps",
                    thresholds=[100],
                    colors=["green", "red"],
                    grid_pos={"h": 8, "w": 12, "x": 12, "y": 0},
                ),
                # Error Rate Panel
                DashboardPanel(
                    title="API Error Rate",
                    metric_query='rate(api_requests_total{status=~"5.."}[5m]) / rate(api_requests_total[5m]) * 100',
                    panel_type="singlestat",
                    unit="percent",
                    thresholds=[5, 10],
                    colors=["green", "yellow", "red"],
                    grid_pos={"h": 8, "w": 6, "x": 0, "y": 8},
                ),
                # CPU Usage Panel
                DashboardPanel(
                    title="CPU Usage",
                    metric_query="system_cpu_percent",
                    panel_type="graph",
                    unit="percent",
                    thresholds=[80, 90],
                    colors=["green", "yellow", "red"],
                    grid_pos={"h": 8, "w": 6, "x": 6, "y": 8},
                ),
                # Memory Usage Panel
                DashboardPanel(
                    title="Memory Usage",
                    metric_query="system_memory_percent",
                    panel_type="graph",
                    unit="percent",
                    thresholds=[85, 95],
                    colors=["green", "yellow", "red"],
                    grid_pos={"h": 8, "w": 6, "x": 12, "y": 8},
                ),
                # Cache Hit Rate Panel
                DashboardPanel(
                    title="Cache Hit Rate",
                    metric_query="cache_hits_total / (cache_hits_total + cache_misses_total) * 100",
                    panel_type="singlestat",
                    unit="percent",
                    thresholds=[80, 90],
                    colors=["red", "yellow", "green"],
                    grid_pos={"h": 8, "w": 6, "x": 18, "y": 8},
                ),
                # Performance Optimization Events
                DashboardPanel(
                    title="Performance Optimizations",
                    metric_query="increase(perf_optimize_applied_total[1h])",
                    panel_type="table",
                    unit="short",
                    grid_pos={"h": 8, "w": 12, "x": 0, "y": 16},
                ),
                # Bottleneck Detection
                DashboardPanel(
                    title="Detected Bottlenecks",
                    metric_query="increase(performance_bottleneck_detected_total[1h])",
                    panel_type="table",
                    unit="short",
                    grid_pos={"h": 8, "w": 12, "x": 12, "y": 16},
                ),
            ]
        )

    def to_grafana_json(self) -> dict[str, Any]:
        """Export configuration as Grafana dashboard JSON."""
        dashboard = {
            "dashboard": {
                "id": None,
                "title": self.dashboard_title,
                "tags": ["performance", "zeta", "monitoring"],
                "timezone": "UTC",
                "refresh": self.refresh_interval,
                "time": {
                    "from": f"now-{self.time_range}",
                    "to": "now",
                },
                "panels": [],
                "templating": {"list": []},
                "annotations": {"list": []},
                "schemaVersion": 30,
                "version": 1,
            }
        }

        # Convert panels to Grafana format
        for i, panel in enumerate(self.panels):
            grafana_panel = {
                "id": i + 1,
                "title": panel.title,
                "type": panel.panel_type,
                "gridPos": panel.grid_pos,
                "targets": [
                    {
                        "expr": panel.metric_query,
                        "format": "time_series",
                        "legendFormat": "",
                    }
                ],
                "yAxes": [
                    {
                        "unit": panel.unit,
                        "min": 0,
                    },
                    {"show": False},
                ],
                "thresholds": {
                    "mode": "absolute",
                    "steps": [
                        {"color": color, "value": threshold}
                        for threshold, color in zip(
                            panel.thresholds, panel.colors, strict=False
                        )
                    ],
                },
                "fieldConfig": {
                    "defaults": {
                        "unit": panel.unit,
                        "thresholds": {
                            "mode": "absolute",
                            "steps": [
                                {"color": color, "value": threshold}
                                for threshold, color in zip(
                                    panel.thresholds, panel.colors, strict=False
                                )
                            ],
                        },
                    }
                },
            }
            dashboard["dashboard"]["panels"].append(grafana_panel)

        return dashboard

    def to_prometheus_rules(self) -> dict[str, Any]:
        """Export thresholds as Prometheus alerting rules."""
        groups = []

        # Group thresholds by metric type
        metric_groups: dict[str, list[PerformanceThreshold]] = {}
        for threshold in self.thresholds:
            metric_type = self._get_metric_type(threshold.metric_name)
            if metric_type not in metric_groups:
                metric_groups[metric_type] = []
            metric_groups[metric_type].append(threshold)

        # Create rule groups
        for group_name, thresholds in metric_groups.items():
            rules = []
            for threshold in thresholds:
                rule = {
                    "alert": f"{threshold.metric_name}_{threshold.severity.value}",
                    "expr": f"{threshold.metric_name} {threshold.comparison_operator} {threshold.threshold_value}",
                    "for": f"{threshold.duration_seconds}s",
                    "labels": {
                        "severity": threshold.severity.value,
                        "metric_type": group_name,
                    },
                    "annotations": {
                        "summary": threshold.description,
                        "description": f"{threshold.metric_name} is {threshold.comparison_operator} {threshold.threshold_value} for more than {threshold.duration_seconds} seconds",
                    },
                }
                rules.append(rule)

            groups.append(
                {
                    "name": f"zeta_performance_{group_name}",
                    "rules": rules,
                }
            )

        return {"groups": groups}

    def _get_metric_type(self, metric_name: str) -> str:
        """Determine metric type from metric name."""
        if "latency" in metric_name or "duration" in metric_name:
            return "latency"
        elif "rate" in metric_name or "per_second" in metric_name:
            return "throughput"
        elif "error" in metric_name:
            return "error_rate"
        elif "cpu" in metric_name or "memory" in metric_name:
            return "resource_usage"
        elif "cache" in metric_name:
            return "cache_performance"
        else:
            return "general"

    def get_alert_summary(self) -> dict[str, int]:
        """Get summary of configured alerts by severity."""
        summary = {severity.value: 0 for severity in AlertSeverity}

        for threshold in self.thresholds:
            summary[threshold.severity.value] += 1

        return summary

    def validate_configuration(self) -> list[str]:
        """Validate the dashboard configuration."""
        errors = []

        # Validate thresholds
        for threshold in self.thresholds:
            if threshold.comparison_operator not in [">", "<", ">=", "<=", "=="]:
                errors.append(
                    f"Invalid comparison operator for {threshold.metric_name}: {threshold.comparison_operator}"
                )

            if threshold.duration_seconds <= 0:
                errors.append(f"Duration must be positive for {threshold.metric_name}")

        # Validate panels
        panel_titles = [panel.title for panel in self.panels]
        if len(panel_titles) != len(set(panel_titles)):
            errors.append("Duplicate panel titles found")

        # Validate grid positions
        positions = [
            (panel.grid_pos.get("x", 0), panel.grid_pos.get("y", 0))
            for panel in self.panels
        ]
        if len(positions) != len(set(positions)):
            errors.append("Overlapping panel positions found")

        return errors


# Default configuration instance
DEFAULT_PERFORMANCE_DASHBOARD = PerformanceDashboardConfig()
