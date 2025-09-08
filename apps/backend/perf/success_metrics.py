"""
Success metrics tracking cho performance optimization implementation.

Features:
- ROI measurement và tracking
- Performance improvement quantification
- Implementation progress monitoring
- Business impact analysis
- Automated reporting dashboard
"""

from __future__ import annotations

import json
import logging
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
import Exception
import ValueError
import abs
import all
import automation_percent
import baseline
import baseline_alerts
import baseline_cost
import baseline_hours
import baseline_minutes
import bool
import current
import current_alerts
import current_cost
import current_hours
import current_minutes
import dict
import engineering_hours
import exc
import f
import float
import imp
import int
import investment_details
import len
import list
import lower_is_better
import m
import max
import measurement_data
import metric_name
import metrics
import open
import progress
import property
import self
import storage_path
import str
import sum

logger = logging.getLogger("zeta.perf.success_metrics")


@dataclass
class BaselineMetrics:
    """Baseline performance metrics before optimization."""

    timestamp: datetime

    # Performance metrics
    avg_response_time_ms: float
    p95_response_time_ms: float
    p99_response_time_ms: float
    requests_per_second: float
    error_rate_percent: float

    # Resource metrics
    cpu_usage_percent: float
    memory_usage_percent: float
    disk_io_ops_per_sec: float
    network_throughput_mbps: float

    # Operational metrics
    alert_frequency_per_day: int
    debugging_time_hours_per_incident: float
    system_downtime_minutes_per_month: float

    # Cost metrics
    infrastructure_cost_per_month: float
    engineering_hours_per_month: float


@dataclass
class CurrentMetrics:
    """Current performance metrics after optimization."""

    timestamp: datetime

    # Performance metrics
    avg_response_time_ms: float
    p95_response_time_ms: float
    p99_response_time_ms: float
    requests_per_second: float
    error_rate_percent: float

    # Resource metrics
    cpu_usage_percent: float
    memory_usage_percent: float
    disk_io_ops_per_sec: float
    network_throughput_mbps: float

    # Operational metrics
    alert_frequency_per_day: int
    debugging_time_hours_per_incident: float
    system_downtime_minutes_per_month: float

    # Cost metrics
    infrastructure_cost_per_month: float
    engineering_hours_per_month: float

    # ML/AI metrics
    anomaly_detection_accuracy: float = 0.0
    false_positive_rate: float = 0.0
    prediction_accuracy: float = 0.0
    automation_coverage_percent: float = 0.0


@dataclass
class ImprovementCalculation:
    """Performance improvement calculations."""

    metric_name: str
    baseline_value: float
    current_value: float
    improvement_percent: float
    improvement_absolute: float
    target_achieved: bool
    trend: str  # improving, stable, degrading


@dataclass
class ROIAnalysis:
    """Return on Investment analysis."""

    # Investment costs
    development_hours: float
    infrastructure_costs: float
    training_costs: float
    total_investment: float

    # Returns/savings
    reduced_downtime_savings: float
    reduced_debugging_time_savings: float
    infrastructure_efficiency_savings: float
    automation_savings: float
    total_savings: float

    # ROI calculation
    roi_percent: float
    payback_period_months: float
    net_present_value: float


@dataclass
class ImplementationProgress:
    """Implementation progress tracking."""

    phase: str  # Phase 1, Phase 2, Phase 3
    start_date: datetime
    target_completion_date: datetime
    current_completion_percent: float

    # Phase 1 metrics
    code_quality_improvement: bool = False
    enhanced_metrics_deployed: bool = False
    ml_components_deployed: bool = False

    # Phase 2 metrics
    anomaly_detection_active: bool = False
    predictive_analysis_active: bool = False
    intelligent_alerting_active: bool = False

    # Phase 3 metrics
    enterprise_integrations_complete: bool = False
    advanced_dashboards_deployed: bool = False
    chaos_engineering_enabled: bool = False

    # Overall success criteria
    performance_targets_met: bool = False
    business_kpis_achieved: bool = False
    stakeholder_satisfaction_score: float = 0.0


class SuccessMetricsTracker:
    """
    Comprehensive success metrics tracking system.

    Tracks implementation progress, performance improvements,
    và business impact của performance optimization initiative.
    """

    def __init__(self, storage_path: str = "perf_success_metrics.json"):
        self.storage_path = Path(storage_path)
        self.baseline: BaselineMetrics | None = None
        self.measurements: list[CurrentMetrics] = []
        self.progress: ImplementationProgress | None = None
        self._load_data()

    @property
    def data_dir(self) -> Path:
        """Get data directory for compatibility."""
        return self.storage_path.parent

    def set_baseline(self, baseline: BaselineMetrics) -> None:
        """Set baseline metrics for comparison."""
        self.baseline = baseline
        logger.info("Baseline metrics set for %s", baseline.timestamp.isoformat())
        self._save_data()

    def record_current_metrics(self, metrics: CurrentMetrics) -> None:
        """Record current performance metrics."""
        self.measurements.append(metrics)
        logger.info("Current metrics recorded for %s", metrics.timestamp.isoformat())
        self._save_data()

    def update_implementation_progress(self, progress: ImplementationProgress) -> None:
        """Update implementation progress."""
        self.progress = progress
        logger.info(
            "Implementation progress updated: Phase %s at %.1f%%",
            progress.phase,
            progress.current_completion_percent,
        )
        self._save_data()

    def calculate_improvements(self) -> list[ImprovementCalculation]:
        """Calculate performance improvements compared to baseline."""
        if not self.baseline or not self.measurements:
            return []

        latest_metrics = self.measurements[-1]
        improvements = []

        # Performance improvements
        improvements.extend(
            [
                self._calculate_improvement(
                    "Average Response Time",
                    self.baseline.avg_response_time_ms,
                    latest_metrics.avg_response_time_ms,
                    lower_is_better=True,
                ),
                self._calculate_improvement(
                    "P95 Response Time",
                    self.baseline.p95_response_time_ms,
                    latest_metrics.p95_response_time_ms,
                    lower_is_better=True,
                ),
                self._calculate_improvement(
                    "Error Rate",
                    self.baseline.error_rate_percent,
                    latest_metrics.error_rate_percent,
                    lower_is_better=True,
                ),
                self._calculate_improvement(
                    "Requests per Second",
                    self.baseline.requests_per_second,
                    latest_metrics.requests_per_second,
                    lower_is_better=False,
                ),
            ]
        )

        # Resource improvements
        improvements.extend(
            [
                self._calculate_improvement(
                    "CPU Usage",
                    self.baseline.cpu_usage_percent,
                    latest_metrics.cpu_usage_percent,
                    lower_is_better=True,
                ),
                self._calculate_improvement(
                    "Memory Usage",
                    self.baseline.memory_usage_percent,
                    latest_metrics.memory_usage_percent,
                    lower_is_better=True,
                ),
            ]
        )

        # Operational improvements
        improvements.extend(
            [
                self._calculate_improvement(
                    "Alert Frequency",
                    self.baseline.alert_frequency_per_day,
                    latest_metrics.alert_frequency_per_day,
                    lower_is_better=True,
                ),
                self._calculate_improvement(
                    "Debugging Time per Incident",
                    self.baseline.debugging_time_hours_per_incident,
                    latest_metrics.debugging_time_hours_per_incident,
                    lower_is_better=True,
                ),
                self._calculate_improvement(
                    "System Downtime",
                    self.baseline.system_downtime_minutes_per_month,
                    latest_metrics.system_downtime_minutes_per_month,
                    lower_is_better=True,
                ),
            ]
        )

        return improvements

    def calculate_roi(self, investment_details: dict[str, float]) -> ROIAnalysis:
        """Calculate ROI based on improvements và investment."""
        if not self.baseline or not self.measurements:
            raise ValueError(
                "Baseline and current metrics required for ROI calculation"
            )

        latest_metrics = self.measurements[-1]

        # Calculate savings from improvements
        downtime_savings = self._calculate_downtime_savings(
            self.baseline.system_downtime_minutes_per_month,
            latest_metrics.system_downtime_minutes_per_month,
        )

        debugging_savings = self._calculate_debugging_savings(
            self.baseline.debugging_time_hours_per_incident,
            latest_metrics.debugging_time_hours_per_incident,
            self.baseline.alert_frequency_per_day,
            latest_metrics.alert_frequency_per_day,
        )

        infrastructure_savings = self._calculate_infrastructure_savings(
            self.baseline.infrastructure_cost_per_month,
            latest_metrics.infrastructure_cost_per_month,
        )

        automation_savings = self._calculate_automation_savings(
            latest_metrics.automation_coverage_percent,
            latest_metrics.engineering_hours_per_month,
        )

        total_savings = (
            downtime_savings
            + debugging_savings
            + infrastructure_savings
            + automation_savings
        )

        total_investment = sum(investment_details.values())

        # Calculate ROI metrics
        roi_percent = ((total_savings - total_investment) / total_investment) * 100
        payback_period_months = (
            total_investment / (total_savings / 12)
            if total_savings > 0
            else float("inf")
        )
        net_present_value = total_savings - total_investment

        return ROIAnalysis(
            development_hours=investment_details.get("development_hours", 0),
            infrastructure_costs=investment_details.get("infrastructure_costs", 0),
            training_costs=investment_details.get("training_costs", 0),
            total_investment=total_investment,
            reduced_downtime_savings=downtime_savings,
            reduced_debugging_time_savings=debugging_savings,
            infrastructure_efficiency_savings=infrastructure_savings,
            automation_savings=automation_savings,
            total_savings=total_savings,
            roi_percent=roi_percent,
            payback_period_months=payback_period_months,
            net_present_value=net_present_value,
        )

    def generate_success_report(self) -> dict[str, Any]:
        """Generate comprehensive success report."""
        report = {
            "report_timestamp": datetime.now(UTC).isoformat(),
            "baseline_set": self.baseline is not None,
            "measurements_count": len(self.measurements),
            "implementation_progress": None,
            "performance_improvements": [],
            "roi_analysis": None,
            "key_achievements": [],
            "recommendations": [],
        }

        if self.progress:
            report["implementation_progress"] = {
                "phase": self.progress.phase,
                "completion_percent": self.progress.current_completion_percent,
                "phase_1_complete": all(
                    [
                        self.progress.code_quality_improvement,
                        self.progress.enhanced_metrics_deployed,
                        self.progress.ml_components_deployed,
                    ]
                ),
                "phase_2_complete": all(
                    [
                        self.progress.anomaly_detection_active,
                        self.progress.predictive_analysis_active,
                        self.progress.intelligent_alerting_active,
                    ]
                ),
                "phase_3_complete": all(
                    [
                        self.progress.enterprise_integrations_complete,
                        self.progress.advanced_dashboards_deployed,
                        self.progress.chaos_engineering_enabled,
                    ]
                ),
            }

        if self.baseline and self.measurements:
            improvements = self.calculate_improvements()
            report["performance_improvements"] = [asdict(imp) for imp in improvements]

            # Key achievements
            significant_improvements = [
                imp
                for imp in improvements
                if abs(imp.improvement_percent) > 10 and imp.trend == "improving"
            ]
            report["key_achievements"] = [
                f"{imp.metric_name}: {imp.improvement_percent:.1f}% improvement"
                for imp in significant_improvements
            ]

            # Recommendations
            degraded_metrics = [imp for imp in improvements if imp.trend == "degrading"]
            if degraded_metrics:
                degraded_names = ", ".join(imp.metric_name for imp in degraded_metrics)
                report["recommendations"].append(
                    f"Address degraded metrics: {degraded_names}"
                )

            if len(significant_improvements) >= 3:
                report["recommendations"].append(
                    "Consider expanding optimization to other systems"
                )
            else:
                report["recommendations"].append(
                    "Continue monitoring and optimization efforts"
                )

        return report

    def _calculate_improvement(
        self,
        metric_name: str,
        baseline: float,
        current: float,
        lower_is_better: bool = True,
    ) -> ImprovementCalculation:
        """Calculate improvement for a single metric."""
        if baseline == 0:
            improvement_percent = 0.0
        else:
            if lower_is_better:
                improvement_percent = ((baseline - current) / baseline) * 100
            else:
                improvement_percent = ((current - baseline) / baseline) * 100

        improvement_absolute = current - baseline

        # Determine trend
        if abs(improvement_percent) < 1:
            trend = "stable"
        elif improvement_percent > 0:
            trend = "improving"
        else:
            trend = "degrading"

        # Target achievement (simplified - 10% improvement target)
        target_achieved = improvement_percent >= 10

        return ImprovementCalculation(
            metric_name=metric_name,
            baseline_value=baseline,
            current_value=current,
            improvement_percent=improvement_percent,
            improvement_absolute=improvement_absolute,
            target_achieved=target_achieved,
            trend=trend,
        )

    def _calculate_downtime_savings(
        self, baseline_minutes: float, current_minutes: float
    ) -> float:
        """Calculate savings from reduced downtime."""
        downtime_reduction_minutes = max(0, baseline_minutes - current_minutes)
        # Assume $1000 per hour of downtime cost
        return (downtime_reduction_minutes / 60) * 1000 * 12  # Annual savings

    def _calculate_debugging_savings(
        self,
        baseline_hours: float,
        current_hours: float,
        baseline_alerts: int,
        current_alerts: int,
    ) -> float:
        """Calculate savings from reduced debugging time."""
        time_per_incident_reduction = max(0, baseline_hours - current_hours)
        alert_reduction = max(0, baseline_alerts - current_alerts)

        # Assume $100/hour engineering cost
        monthly_incidents = (baseline_alerts + current_alerts) / 2 * 30
        annual_savings = time_per_incident_reduction * monthly_incidents * 12 * 100
        annual_savings += alert_reduction * 30 * 12 * baseline_hours * 100

        return annual_savings

    def _calculate_infrastructure_savings(
        self, baseline_cost: float, current_cost: float
    ) -> float:
        """Calculate infrastructure cost savings."""
        monthly_savings = max(0, baseline_cost - current_cost)
        return monthly_savings * 12  # Annual savings

    def _calculate_automation_savings(
        self, automation_percent: float, engineering_hours: float
    ) -> float:
        """Calculate savings from automation."""
        # Assume automation saves time proportional to coverage
        automated_hours = engineering_hours * (automation_percent / 100)
        return automated_hours * 100 * 12  # Annual savings at $100/hour

    def _save_data(self) -> None:
        """Save tracking data to storage."""
        data = {
            "baseline": asdict(self.baseline) if self.baseline else None,
            "measurements": [asdict(m) for m in self.measurements],
            "progress": asdict(self.progress) if self.progress else None,
        }

        try:
            with open(self.storage_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, default=str)
        except Exception as exc:
            logger.error("Failed to save success metrics data: %s", exc)

    def _load_data(self) -> None:
        """Load tracking data from storage."""
        if not self.storage_path.exists():
            return

        try:
            with open(self.storage_path, encoding="utf-8") as f:
                data = json.load(f)

            if data.get("baseline"):
                baseline_data = data["baseline"]
                baseline_data["timestamp"] = datetime.fromisoformat(
                    baseline_data["timestamp"]
                )
                self.baseline = BaselineMetrics(**baseline_data)

            for measurement_data in data.get("measurements", []):
                measurement_data["timestamp"] = datetime.fromisoformat(
                    measurement_data["timestamp"]
                )
                self.measurements.append(CurrentMetrics(**measurement_data))

            if data.get("progress"):
                progress_data = data["progress"]
                progress_data["start_date"] = datetime.fromisoformat(
                    progress_data["start_date"]
                )
                progress_data["target_completion_date"] = datetime.fromisoformat(
                    progress_data["target_completion_date"]
                )
                self.progress = ImplementationProgress(**progress_data)

        except Exception as exc:
            logger.error("Failed to load success metrics data: %s", exc)
