"""
Metrics Service implementation với Prometheus-style counters.
Support cả in-memory metrics và Prometheus export.
"""

import threading
from collections import defaultdict
from datetime import datetime
from typing import Any, Optional

from core.domain.interfaces import MetricsServiceInterface


class PrometheusStyleMetricsService(MetricsServiceInterface):
    """
    Prometheus-style metrics service.
    Implements counters, histograms, và gauges.
    """

    def __init__(self):
        self._counters: dict[str, dict[Tuple[str, ...], float]] = defaultdict(lambda: defaultdict(float))
        self._histograms: dict[str, dict[Tuple[str, ...], list[float]]] = defaultdict(lambda: defaultdict(list))
        self._gauges: dict[str, dict[Tuple[str, ...], float]] = defaultdict(lambda: defaultdict(float))
        self._lock = threading.RLock()

        # Histogram buckets (in milliseconds for timing metrics)
        self._histogram_buckets = [1, 5, 10, 25, 50, 100, 250, 500, 1000, 2500, 5000, 10000]

    def _labels_to_key(self, labels: Optional[dict[str, str]] = None) -> Tuple[str, ...]:
        """Convert labels dict to sorted tuple for consistent key"""
        if not labels:
            return ()
        return tuple(sorted(labels.items()))

    def increment_counter(self, metric_name: str, labels: Optional[dict[str, str]] = None) -> None:
        """Tăng counter metric"""
        with self._lock:
            key = self._labels_to_key(labels)
            self._counters[metric_name][key] += 1

    def increment_counter_by(self, metric_name: str, value: float, labels: Optional[dict[str, str]] = None) -> None:
        """Tăng counter metric theo value specified"""
        with self._lock:
            key = self._labels_to_key(labels)
            self._counters[metric_name][key] += value

    def record_histogram(self, metric_name: str, value: float, labels: Optional[dict[str, str]] = None) -> None:
        """Record histogram metric"""
        with self._lock:
            key = self._labels_to_key(labels)
            self._histograms[metric_name][key].append(value)

            # Keep only last 1000 values để tránh memory leak
            if len(self._histograms[metric_name][key]) > 1000:
                self._histograms[metric_name][key] = self._histograms[metric_name][key][-1000:]

    def set_gauge(self, metric_name: str, value: float, labels: Optional[dict[str, str]] = None) -> None:
        """Set gauge metric"""
        with self._lock:
            key = self._labels_to_key(labels)
            self._gauges[metric_name][key] = value

    def get_counter_value(self, metric_name: str, labels: Optional[dict[str, str]] = None) -> float:
        """Lấy current value của counter"""
        with self._lock:
            key = self._labels_to_key(labels)
            return self._counters[metric_name][key]

    def get_gauge_value(self, metric_name: str, labels: Optional[dict[str, str]] = None) -> float:
        """Lấy current value của gauge"""
        with self._lock:
            key = self._labels_to_key(labels)
            return self._gauges[metric_name][key]

    def get_histogram_stats(self, metric_name: str, labels: Optional[dict[str, str]] = None) -> dict[str, float]:
        """Lấy histogram statistics (count, sum, percentiles)"""
        with self._lock:
            key = self._labels_to_key(labels)
            values = self._histograms[metric_name][key]

            if not values:
                return {
                    "count": 0,
                    "sum": 0.0,
                    "min": 0.0,
                    "max": 0.0,
                    "avg": 0.0,
                    "p50": 0.0,
                    "p95": 0.0,
                    "p99": 0.0,
                }

            sorted_values = sorted(values)
            count = len(values)

            def percentile(data: list[float], p: float) -> float:
                """Calculate percentile"""
                if not data:
                    return 0.0
                index = int(p * (len(data) - 1))
                return data[index]

            return {
                "count": count,
                "sum": sum(values),
                "min": min(values),
                "max": max(values),
                "avg": sum(values) / count,
                "p50": percentile(sorted_values, 0.5),
                "p95": percentile(sorted_values, 0.95),
                "p99": percentile(sorted_values, 0.99),
            }

    def get_all_metrics(self) -> dict[str, Any]:
        """Lấy tất cả metrics trong format dễ đọc"""
        with self._lock:
            result = {
                "counters": {},
                "histograms": {},
                "gauges": {},
                "timestamp": datetime.utcnow().isoformat(),
            }

            # Process counters
            for metric_name, label_values in self._counters.items():
                result["counters"][metric_name] = {}
                for label_key, value in label_values.items():
                    labels_str = ",".join([f"{k}={v}" for k, v in label_key]) if label_key else "no_labels"
                    result["counters"][metric_name][labels_str] = value

            # Process histograms
            for metric_name, label_values in self._histograms.items():
                result["histograms"][metric_name] = {}
                for label_key, values in label_values.items():
                    labels_str = ",".join([f"{k}={v}" for k, v in label_key]) if label_key else "no_labels"
                    result["histograms"][metric_name][labels_str] = self.get_histogram_stats(metric_name, dict(label_key))

            # Process gauges
            for metric_name, label_values in self._gauges.items():
                result["gauges"][metric_name] = {}
                for label_key, value in label_values.items():
                    labels_str = ",".join([f"{k}={v}" for k, v in label_key]) if label_key else "no_labels"
                    result["gauges"][metric_name][labels_str] = value

            return result

    def export_prometheus_format(self) -> str:
        """Export metrics trong Prometheus format"""
        lines = []
        lines.append(f"# Generated at {datetime.utcnow().isoformat()}")
        lines.append("")

        with self._lock:
            # Export counters
            for metric_name, label_values in self._counters.items():
                lines.append(f"# TYPE {metric_name} counter")
                for label_key, value in label_values.items():
                    if label_key:
                        labels_str = "{" + ",".join([f'{k}="{v}"' for k, v in label_key]) + "}"
                        lines.append(f"{metric_name}{labels_str} {value}")
                    else:
                        lines.append(f"{metric_name} {value}")
                lines.append("")

            # Export histograms
            for metric_name, label_values in self._histograms.items():
                lines.append(f"# TYPE {metric_name} histogram")
                for label_key, values in label_values.items():
                    stats = self.get_histogram_stats(metric_name, dict(label_key))
                    label_dict = dict(label_key) if label_key else {}

                    # Histogram buckets
                    for bucket in self._histogram_buckets:
                        bucket_count = sum(1 for v in values if v <= bucket)
                        bucket_labels = {**label_dict, "le": str(bucket)}
                        labels_str = "{" + ",".join([f'{k}="{v}"' for k, v in bucket_labels.items()]) + "}"
                        lines.append(f"{metric_name}_bucket{labels_str} {bucket_count}")

                    # +Inf bucket
                    inf_labels = {**label_dict, "le": "+Inf"}
                    labels_str = "{" + ",".join([f'{k}="{v}"' for k, v in inf_labels.items()]) + "}"
                    lines.append(f"{metric_name}_bucket{labels_str} {stats['count']}")

                    # Count và sum
                    if label_key:
                        labels_str = "{" + ",".join([f'{k}="{v}"' for k, v in label_key]) + "}"
                        lines.append(f"{metric_name}_count{labels_str} {stats['count']}")
                        lines.append(f"{metric_name}_sum{labels_str} {stats['sum']}")
                    else:
                        lines.append(f"{metric_name}_count {stats['count']}")
                        lines.append(f"{metric_name}_sum {stats['sum']}")
                lines.append("")

            # Export gauges
            for metric_name, label_values in self._gauges.items():
                lines.append(f"# TYPE {metric_name} gauge")
                for label_key, value in label_values.items():
                    if label_key:
                        labels_str = "{" + ",".join([f'{k}="{v}"' for k, v in label_key]) + "}"
                        lines.append(f"{metric_name}{labels_str} {value}")
                    else:
                        lines.append(f"{metric_name} {value}")
                lines.append("")

        return "\n".join(lines)

    def reset_all_metrics(self) -> None:
        """Reset tất cả metrics (useful for testing)"""
        with self._lock:
            self._counters.clear()
            self._histograms.clear()
            self._gauges.clear()

    def get_summary(self) -> dict[str, Any]:
        """Lấy metrics summary"""
        with self._lock:
            return {
                "total_counters": sum(len(label_values) for label_values in self._counters.values()),
                "total_histograms": sum(len(label_values) for label_values in self._histograms.values()),
                "total_gauges": sum(len(label_values) for label_values in self._gauges.values()),
                "counter_metrics": list(self._counters.keys()),
                "histogram_metrics": list(self._histograms.keys()),
                "gauge_metrics": list(self._gauges.keys()),
            }


# Null metrics service for testing/disabled metrics
class NullMetricsService(MetricsServiceInterface):
    """No-op metrics service for testing hoặc khi muốn disable metrics"""

    def increment_counter(self, metric_name: str, labels: Optional[dict[str, str]] = None) -> None:
        pass

    def record_histogram(self, metric_name: str, value: float, labels: Optional[dict[str, str]] = None) -> None:
        pass

    def set_gauge(self, metric_name: str, value: float, labels: Optional[dict[str, str]] = None) -> None:
        pass


# Factory function
def create_metrics_service(enabled: bool = True) -> MetricsServiceInterface:
    """
    Factory function để tạo metrics service.
    
    Args:
        enabled: True để enable metrics, False để sử dụng null implementation
        
    Returns:
        MetricsServiceInterface implementation
    """
    if enabled:
        return PrometheusStyleMetricsService()
    else:
        return NullMetricsService()
