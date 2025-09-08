"""
ML-driven performance anomaly detection và predictive optimization.

Features:
- Statistical anomaly detection cho performance metrics
- Predictive scaling recommendations
- Intelligent alerting với context-aware filtering
- Performance trend analysis
- Auto-optimization recommendations
"""

from __future__ import annotations

import logging
import statistics
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any
import abs
import alert
import anomaly_threshold
import baseline
import bool
import cooldown_minutes
import current_data
import data_point
import dict
import dp
import float
import getattr
import hasattr
import int
import len
import list
import max
import metric_name
import min
import min_data_points
import prediction_window_minutes
import property
import range
import self
import str
import sum
import trend
import window_size
import x
import y
import zip

logger = logging.getLogger("zeta.perf.ml_optimization")


@dataclass
class PerformanceDataPoint:
    """Single performance measurement."""

    timestamp: datetime
    cpu_percent: float
    memory_percent: float
    response_time_p95_ms: float
    requests_per_second: float
    error_rate: float
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class AnomalyDetectionResult:
    """Result of anomaly detection analysis."""

    is_anomaly: bool
    confidence: float
    anomaly_type: str
    affected_metrics: list[str]
    severity: str  # low, medium, high, critical
    recommendation: str
    details: dict[str, Any] = field(default_factory=dict)


@dataclass
class PredictionResult:
    """Performance prediction result."""

    metric_name: str
    current_value: float
    predicted_value: float
    prediction_confidence: float
    time_horizon_minutes: int
    trend: str  # improving, stable, degrading
    recommendation: str


class StatisticalAnomalyDetector:
    """
    Statistical anomaly detection using moving averages and standard deviation.

    Simple yet effective approach for detecting performance anomalies.
    """

    def __init__(
        self,
        window_size: int = 50,
        anomaly_threshold: float = 2.0,
        min_data_points: int = 10,
    ):
        self.window_size = window_size
        self.anomaly_threshold = anomaly_threshold
        self.min_data_points = min_data_points
        self.data_history: list[PerformanceDataPoint] = []

    def add_data_point(self, data_point: PerformanceDataPoint) -> None:
        """Add new performance data point to history."""
        self.data_history.append(data_point)

        # Keep only recent data points
        if len(self.data_history) > self.window_size * 2:
            self.data_history = self.data_history[-self.window_size :]

    def detect_anomalies(
        self, current_data: PerformanceDataPoint
    ) -> list[AnomalyDetectionResult]:
        """
        Detect anomalies in current performance data.

        Args:
            current_data: Current performance measurements

        Returns:
            List of detected anomalies
        """
        if len(self.data_history) < self.min_data_points:
            return []

        anomalies = []

        # Check each metric for anomalies
        metrics_to_check = [
            ("cpu_percent", current_data.cpu_percent),
            ("memory_percent", current_data.memory_percent),
            ("response_time_p95_ms", current_data.response_time_p95_ms),
            ("requests_per_second", current_data.requests_per_second),
            ("error_rate", current_data.error_rate),
        ]

        for metric_name, current_value in metrics_to_check:
            historical_values = [
                getattr(dp, metric_name)
                for dp in self.data_history[-self.window_size :]
            ]

            if len(historical_values) < self.min_data_points:
                continue

            mean_value = statistics.mean(historical_values)
            std_dev = (
                statistics.stdev(historical_values) if len(historical_values) > 1 else 0
            )

            if std_dev == 0:
                continue

            z_score = abs(current_value - mean_value) / std_dev

            if z_score > self.anomaly_threshold:
                severity = self._calculate_severity(z_score, metric_name)
                anomaly_type = self._classify_anomaly(
                    metric_name, current_value, mean_value
                )
                recommendation = self._generate_recommendation(
                    metric_name, anomaly_type, severity
                )

                anomaly = AnomalyDetectionResult(
                    is_anomaly=True,
                    confidence=min(z_score / self.anomaly_threshold, 1.0),
                    anomaly_type=anomaly_type,
                    affected_metrics=[metric_name],
                    severity=severity,
                    recommendation=recommendation,
                    details={
                        "z_score": z_score,
                        "current_value": current_value,
                        "baseline_mean": mean_value,
                        "baseline_std": std_dev,
                    },
                )
                anomalies.append(anomaly)

        return anomalies

    def _calculate_severity(self, z_score: float, metric_name: str) -> str:
        """Calculate anomaly severity based on z-score and metric type."""
        # Higher sensitivity for error rates and response times
        if metric_name in ["error_rate", "response_time_p95_ms"]:
            if z_score > 4.0:
                return "critical"
            elif z_score > 3.0:
                return "high"
            elif z_score > 2.5:
                return "medium"
            else:
                return "low"
        else:
            if z_score > 5.0:
                return "critical"
            elif z_score > 4.0:
                return "high"
            elif z_score > 3.0:
                return "medium"
            else:
                return "low"

    def _classify_anomaly(
        self, metric_name: str, current_value: float, baseline: float
    ) -> str:
        """Classify the type of anomaly."""
        if current_value > baseline:
            if metric_name == "requests_per_second":
                return "traffic_spike"
            elif metric_name in ["cpu_percent", "memory_percent"]:
                return "resource_spike"
            elif metric_name == "response_time_p95_ms":
                return "latency_spike"
            elif metric_name == "error_rate":
                return "error_spike"
            else:
                return "metric_increase"
        else:
            if metric_name == "requests_per_second":
                return "traffic_drop"
            else:
                return "metric_decrease"

    def _generate_recommendation(
        self, metric_name: str, anomaly_type: str, severity: str
    ) -> str:
        """Generate optimization recommendation based on anomaly."""
        recommendations = {
            "traffic_spike": "Consider auto-scaling or load balancing",
            "resource_spike": "Check for memory leaks or optimize resource usage",
            "latency_spike": "Review database queries and cache hit rates",
            "error_spike": "Check application logs and error handling",
            "traffic_drop": "Investigate potential service availability issues",
        }

        base_recommendation = recommendations.get(
            anomaly_type, "Monitor and investigate further"
        )

        if severity in ["high", "critical"]:
            return f"URGENT: {base_recommendation}"
        else:
            return base_recommendation


class SimplePerformancePredictor:
    """
    Simple trend-based performance predictor.

    Uses recent trends to predict near-future performance.
    """

    def __init__(self, prediction_window_minutes: int = 30):
        self.prediction_window_minutes = prediction_window_minutes
        self.data_history: list[PerformanceDataPoint] = []

    @property
    def history_size(self) -> int:
        """Get current history size for compatibility."""
        return len(self.data_history)

    def add_data_point(self, data_point: PerformanceDataPoint) -> None:
        """Add data point for trend analysis."""
        self.data_history.append(data_point)

        # Keep only last hour of data
        cutoff_time = datetime.now() - timedelta(hours=1)
        self.data_history = [
            dp for dp in self.data_history if dp.timestamp > cutoff_time
        ]

    def predict_performance(self, metric_name: str) -> PredictionResult | None:
        """
        Predict future performance based on recent trends.

        Args:
            metric_name: Name of metric to predict

        Returns:
            Prediction result or None if insufficient data
        """
        if len(self.data_history) < 5:
            return None

        # Get recent values for the metric
        recent_values = []
        for dp in self.data_history[-10:]:  # Last 10 data points
            if hasattr(dp, metric_name):
                recent_values.append(getattr(dp, metric_name))

        if len(recent_values) < 3:
            return None

        # Calculate trend using simple linear regression
        current_value = recent_values[-1]
        trend_slope = self._calculate_trend_slope(recent_values)

        # Predict value after prediction window
        predicted_value = current_value + (trend_slope * self.prediction_window_minutes)

        # Calculate confidence based on data consistency
        confidence = self._calculate_prediction_confidence(recent_values)

        # Classify trend
        trend_classification = self._classify_trend(trend_slope, metric_name)

        # Generate recommendation
        recommendation = self._generate_prediction_recommendation(
            metric_name, trend_classification, predicted_value
        )

        return PredictionResult(
            metric_name=metric_name,
            current_value=current_value,
            predicted_value=predicted_value,
            prediction_confidence=confidence,
            time_horizon_minutes=self.prediction_window_minutes,
            trend=trend_classification,
            recommendation=recommendation,
        )

    def _calculate_trend_slope(self, values: list[float]) -> float:
        """Calculate simple trend slope."""
        if len(values) < 2:
            return 0.0

        # Simple linear regression slope calculation
        x_values = list(range(len(values)))
        n = len(values)

        sum_x = sum(x_values)
        sum_y = sum(values)
        sum_xy = sum(x * y for x, y in zip(x_values, values, strict=True))
        sum_x2 = sum(x * x for x in x_values)

        denominator = n * sum_x2 - sum_x * sum_x
        if denominator == 0:
            return 0.0

        slope = (n * sum_xy - sum_x * sum_y) / denominator
        return slope

    def _calculate_prediction_confidence(self, values: list[float]) -> float:
        """Calculate prediction confidence based on data variance."""
        if len(values) < 2:
            return 0.0

        variance = statistics.variance(values)
        mean_value = statistics.mean(values)

        if mean_value == 0:
            return 0.0

        # Lower coefficient of variation = higher confidence
        cv = (variance**0.5) / abs(mean_value)
        confidence = max(0.0, min(1.0, 1.0 - cv))

        return confidence

    def _classify_trend(self, slope: float, metric_name: str) -> str:
        """Classify trend direction."""
        threshold = 0.1  # Minimum slope to consider significant

        if abs(slope) < threshold:
            return "stable"
        elif slope > 0:
            # Increasing trend
            if metric_name in [
                "error_rate",
                "response_time_p95_ms",
                "cpu_percent",
                "memory_percent",
            ]:
                return "degrading"  # These metrics increasing is bad
            else:
                return "improving"  # These metrics increasing is good
        else:
            # Decreasing trend
            if metric_name in [
                "error_rate",
                "response_time_p95_ms",
                "cpu_percent",
                "memory_percent",
            ]:
                return "improving"  # These metrics decreasing is good
            else:
                return "degrading"  # These metrics decreasing is bad

    def _generate_prediction_recommendation(
        self, metric_name: str, trend: str, predicted_value: float
    ) -> str:
        """Generate recommendation based on prediction."""
        if trend == "stable":
            return "Performance is stable, continue monitoring"
        elif trend == "improving":
            return "Performance is improving, maintain current optimizations"
        else:  # degrading
            if metric_name == "cpu_percent" and predicted_value > 80:
                return "CPU usage trending high, consider scaling or optimization"
            elif metric_name == "memory_percent" and predicted_value > 85:
                return "Memory usage trending high, check for leaks"
            elif metric_name == "response_time_p95_ms" and predicted_value > 1000:
                return "Response time degrading, review performance bottlenecks"
            elif metric_name == "error_rate" and predicted_value > 5:
                return "Error rate increasing, check application health"
            else:
                return f"{metric_name} trending worse, investigate causes"


class IntelligentAlertManager:
    """
    Context-aware alert management với intelligent filtering.

    Reduces false positives and alert fatigue.
    """

    def __init__(self, cooldown_minutes: int = 15):
        self.cooldown_minutes = cooldown_minutes
        self.recent_alerts: dict[str, datetime] = {}
        self.alert_history: list[dict[str, Any]] = []

        # Severity weights for alert prioritization
        self.severity_weights = {
            "low": 1.0,
            "medium": 2.0,
            "high": 3.0,
            "critical": 5.0,
        }

    def should_alert(self, anomaly: AnomalyDetectionResult) -> bool:
        """
        Determine if an alert should be sent based on context.

        Args:
            anomaly: Detected anomaly

        Returns:
            True if alert should be sent
        """
        alert_key = f"{anomaly.anomaly_type}_{anomaly.severity}"

        # Check cooldown period
        if alert_key in self.recent_alerts:
            time_since_last = datetime.now() - self.recent_alerts[alert_key]
            if time_since_last.total_seconds() < self.cooldown_minutes * 60:
                return False

        # Check severity threshold
        if anomaly.severity == "low" and anomaly.confidence < 0.8:
            return False

        # Record alert
        self.recent_alerts[alert_key] = datetime.now()
        self.alert_history.append(
            {
                "timestamp": datetime.now(),
                "anomaly_type": anomaly.anomaly_type,
                "severity": anomaly.severity,
                "confidence": anomaly.confidence,
            }
        )

        return True

    def get_alert_summary(self) -> dict[str, Any]:
        """Get summary of recent alerts."""
        recent_alerts = [
            alert
            for alert in self.alert_history
            if datetime.now() - alert["timestamp"] < timedelta(hours=24)
        ]

        severity_counts = {}
        for alert in recent_alerts:
            severity = alert["severity"]
            severity_counts[severity] = severity_counts.get(severity, 0) + 1

        return {
            "total_alerts_24h": len(recent_alerts),
            "severity_breakdown": severity_counts,
            "active_cooldowns": len(self.recent_alerts),
        }
