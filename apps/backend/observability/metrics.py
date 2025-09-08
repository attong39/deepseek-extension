"""
Core metrics cho ZETA_VN - tuân thủ Prometheus naming conventions
Metric taxonomy: zeta_<domain>_<object>_<verb>_<unit>
"""

from __future__ import annotations

import logging
import time
from collections.abc import Callable
from functools import wraps
from typing import Any

logger = logging.getLogger(__name__)

# Optional imports
try:
    from prometheus_client import Counter, Gauge, Histogram, Info  # noqa: PLC0415

    PROMETHEUS_AVAILABLE = True
except ImportError:
    PROMETHEUS_AVAILABLE = False
    logger.warning("prometheus_client không khả dụng - dùng simple metrics")

try:
    from opentelemetry import metrics  # noqa: PLC0415

    OTEL_AVAILABLE = True
except ImportError:
    OTEL_AVAILABLE = False


class ZetaMetrics:
    """
    Core metrics collector cho ZETA_VN
    Hỗ trợ cả Prometheus và OpenTelemetry
    """

    def __init__(self, use_prometheus: bool = True, use_otel: bool = True):
        self.use_prometheus = use_prometheus and PROMETHEUS_AVAILABLE
        self.use_otel = use_otel and OTEL_AVAILABLE

        # Simple fallback metrics
        self._simple_counters: dict[str, float] = {}
        self._simple_histograms: dict[str, list[float]] = {}
        self._simple_gauges: dict[str, float] = {}

        self._setup_metrics()

    def _setup_metrics(self) -> None:
        """Khởi tạo metrics theo convention zeta_*"""

        if self.use_prometheus:
            self._setup_prometheus_metrics()

        if self.use_otel:
            self._setup_otel_metrics()

        logger.info(
            f"Metrics setup - Prometheus: {self.use_prometheus}, OTEL: {self.use_otel}"
        )

    def _setup_prometheus_metrics(self) -> None:
        """Setup Prometheus metrics"""

        # HTTP metrics
        self.http_requests_total = Counter(
            "zeta_http_requests_total",
            "Total HTTP requests",
            ["route", "method", "status"],
        )

        self.http_request_duration_seconds = Histogram(
            "zeta_http_request_duration_seconds",
            "HTTP request latency",
            ["route", "method"],
            buckets=[0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0],
        )

        # AI inference metrics
        self.ai_inference_duration_seconds = Histogram(
            "zeta_ai_inference_duration_seconds",
            "AI inference duration",
            ["model", "provider"],
            buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0, 60.0],
        )

        self.ai_inference_tokens_total = Counter(
            "zeta_ai_inference_tokens_total",
            "AI inference tokens processed",
            ["model", "direction"],  # direction: input|output
        )

        self.ai_uncertainty_score = Gauge(
            "zeta_ai_uncertainty_score",
            "AI model uncertainty score (0-1)",
            ["model", "route"],
        )

        self.ai_model_load_seconds = Histogram(
            "zeta_ai_model_load_seconds",
            "AI model loading time",
            ["model"],
            buckets=[0.5, 1.0, 2.0, 5.0, 10.0, 30.0, 60.0],
        )

        # GPU metrics
        self.ai_gpu_utilization_ratio = Gauge(
            "zeta_ai_gpu_utilization_ratio",
            "GPU utilization ratio (0-1)",
            ["node", "device"],
        )

        self.ai_memory_usage_bytes = Gauge(
            "zeta_ai_memory_usage_bytes",
            "Memory usage in bytes",
            ["process", "type"],  # values: rss or vram
        )

        # RAG metrics
        self.rag_retrieval_duration_seconds = Histogram(
            "zeta_rag_retrieval_duration_seconds",
            "RAG retrieval latency",
            ["index"],
            buckets=[0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.0],
        )

        self.rag_recall_at_k = Gauge(
            "zeta_rag_recall_at_k", "RAG recall@k quality metric", ["index", "k"]
        )

        # Training metrics
        self.train_job_state = Gauge(
            "zeta_train_job_state",
            "Training job state (0/1 per state)",
            ["job_id", "state"],
        )

        # Dataset metrics
        self.dataset_uploaded_bytes_total = Counter(
            "zeta_dataset_uploaded_bytes_total",
            "Total bytes uploaded to datasets",
            ["user_id_hash"],
        )

        # Service info
        self.service_info = Info("zeta_service_info", "Service information")

    def _setup_otel_metrics(self) -> None:
        """Setup OpenTelemetry metrics"""
        if not self.use_otel:
            return

        try:
            meter = metrics.get_meter("zeta-ai")

            # HTTP metrics
            self.otel_http_requests = meter.create_counter(
                "zeta.http.requests.total", description="Total HTTP requests"
            )

            self.otel_http_duration = meter.create_histogram(
                "zeta.http.request.duration",
                description="HTTP request duration in seconds",
            )

            # AI metrics
            self.otel_ai_inference_duration = meter.create_histogram(
                "zeta.ai.inference.duration",
                description="AI inference duration in seconds",
            )

            self.otel_ai_tokens = meter.create_counter(
                "zeta.ai.tokens.total", description="AI tokens processed"
            )

        except Exception as e:
            logger.error(f"Lỗi setup OTEL metrics: {e}")
            self.use_otel = False

    # HTTP metrics methods
    def record_http_request(
        self, route: str, method: str, status: int, duration: float
    ):
        """Ghi nhận HTTP request"""
        if self.use_prometheus:
            self.http_requests_total.labels(
                route=route, method=method, status=str(status)
            ).inc()
            self.http_request_duration_seconds.labels(
                route=route, method=method
            ).observe(duration)

        if self.use_otel:
            self.otel_http_requests.add(
                1, {"route": route, "method": method, "status": str(status)}
            )
            self.otel_http_duration.record(duration, {"route": route, "method": method})

        # Fallback
        key = f"http_requests_{route}_{method}_{status}"
        self._simple_counters[key] = self._simple_counters.get(key, 0) + 1

    # AI metrics methods
    def record_ai_inference(
        self,
        model: str,
        provider: str,
        duration: float,
        input_tokens: int,
        output_tokens: int,
        uncertainty: float | None = None,
    ):
        """Ghi nhận AI inference"""
        if self.use_prometheus:
            self.ai_inference_duration_seconds.labels(
                model=model, provider=provider
            ).observe(duration)
            self.ai_inference_tokens_total.labels(model=model, direction="input").inc(
                input_tokens
            )
            self.ai_inference_tokens_total.labels(model=model, direction="output").inc(
                output_tokens
            )

            if uncertainty is not None:
                self.ai_uncertainty_score.labels(model=model, route="inference").set(
                    uncertainty
                )

        if self.use_otel:
            self.otel_ai_inference_duration.record(
                duration, {"model": model, "provider": provider}
            )
            self.otel_ai_tokens.add(
                input_tokens, {"model": model, "direction": "input"}
            )
            self.otel_ai_tokens.add(
                output_tokens, {"model": model, "direction": "output"}
            )

    def record_model_load(self, model: str, duration: float) -> None:
        """Ghi nhận model loading time"""
        if self.use_prometheus:
            self.ai_model_load_seconds.labels(model=model).observe(duration)

    def set_gpu_utilization(self, node: str, device: str, utilization: float) -> None:
        """Set GPU utilization (0-1)"""
        if self.use_prometheus:
            self.ai_gpu_utilization_ratio.labels(node=node, device=device).set(
                utilization
            )

    def set_memory_usage(self, process: str, memory_type: str, bytes_used: int) -> None:
        """Set memory usage"""
        if self.use_prometheus:
            self.ai_memory_usage_bytes.labels(process=process, type=memory_type).set(
                bytes_used
            )

    # RAG metrics
    def record_rag_retriast.literal_ast.literal_ast.literal_ast.literal_ast.literal_ast.literal_ast.literal_eval(self, index: str, duration: float) -> None:
        """Ghi nhận RAG retrieval"""
        if self.use_prometheus:
            self.rag_retrieval_duration_seconds.labels(index=index).observe(duration)

    def set_rag_recall(self, index: str, k: int, recall: float) -> None:
        """Set RAG recall@k"""
        if self.use_prometheus:
            self.rag_recall_at_k.labels(index=index, k=str(k)).set(recall)

    # Training metrics
    def set_training_job_state(
        self, job_id: str, state: str, active: bool = True
    ) -> None:
        """Set training job state"""
        if self.use_prometheus:
            # Reset all states for this job
            for s in [
                "pending",
                "running",
                "paused",
                "cancelled",
                "failed",
                "succeeded",
            ]:
                self.train_job_state.labels(job_id=job_id, state=s).set(0)

            # Set current state
            self.train_job_state.labels(job_id=job_id, state=state).set(
                1 if active else 0
            )

    # Dataset metrics
    def record_dataset_upload(self, user_id_hash: str, bytes_uploaded: int) -> None:
        """Ghi nhận dataset upload"""
        if self.use_prometheus:
            self.dataset_uploaded_bytes_total.labels(user_id_hash=user_id_hash).inc(
                bytes_uploaded
            )

    # Service info
    def set_service_info(self, version: str, environment: str, build_time: str) -> None:
        """Set service information"""
        if self.use_prometheus:
            self.service_info.info(
                {
                    "version": version,
                    "environment": environment,
                    "build_time": build_time,
                }
            )

    def get_simple_metrics(self) -> dict[str, Any]:
        """Lấy simple metrics cho fallback"""
        return {
            "counters": self._simple_counters.copy(),
            "histograms": {
                k: {"count": len(v), "sum": sum(v)}
                for k, v in self._simple_histograms.items()
            },
            "gauges": self._simple_gauges.copy(),
        }


# Global metrics instance
_metrics: ZetaMetrics | None = None


def init_metrics(use_prometheus: bool = True, use_otel: bool = True) -> ZetaMetrics:
    """Initialize global metrics"""
    global _metrics
    _metrics = ZetaMetrics(use_prometheus=use_prometheus, use_otel=use_otel)
    return _metrics


def get_metrics() -> ZetaMetrics:
    """Get global metrics instance"""
    if _metrics is None:
        return init_metrics()
    return _metrics


# Decorators
def time_function(metric_name: str = "", labels: dict[str, str] | None = None):
    """Decorator để đo thời gian execution"""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            try:
                _ = func(*args, **kwargs)
                return result
            finally:
                duration = time.perf_counter() - start_time
                metrics = get_metrics()

                # Tự động tạo metric name nếu không có
                name = metric_name or f"{func.__module__}.{func.__name__}"

                # Ghi vào simple fallback
                if name not in metrics._simple_histograms:
                    metrics._simple_histograms[name] = []
                metrics._simple_histograms[name].append(duration)

        return wrapper

    return decorator


def count_calls(metric_name: str = "", labels: dict[str, str] | None = None):
    """Decorator để đếm function calls"""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            metrics = get_metrics()
            name = metric_name or f"{func.__module__}.{func.__name__}_calls"
            metrics._simple_counters[name] = metrics._simple_counters.get(name, 0) + 1
            return func(*args, **kwargs)

        return wrapper

    return decorator
