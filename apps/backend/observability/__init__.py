"""
from __future__ import annotations

zeta_vn.observability package.

Auto-fixed by comprehensive_init_fixer.py
"""

__all__ = [
    "AlertRouter",
    "OTEL_AVAILABLE",
    "PROMETHEUS_AVAILABLE",
    "SLO",
    "ZetaMetrics",
    "ZetaOTelConfig",
    "compute_error_budget",
    "config",
    "count_calls",
    "data",
    "decorator",
    "duration",
    "get_meter",
    "get_metrics",
    "get_simple_metrics",
    "get_tracer",
    "init_metrics",
    "initialize_observability",
    "key",
    "logger",
    "meter",
    "meter_provider",
    "metrics",
    "name",
    "otlp_exporter",
    "otlp_reader",
    "payload",
    "prometheus_reader",
    "provider",
    "readers",
    "record_ai_inference",
    "record_dataset_upload",
    "record_http_request",
    "record_model_load",
    "record_rag_retrieval",
    "req",
    "resource",
    "result",
    "send_pagerduty",
    "send_slack",
    "set_gpu_utilization",
    "set_memory_usage",
    "set_rag_recall",
    "set_service_info",
    "set_training_job_state",
    "setup_auto_instrumentation",
    "setup_otel_metrics",
    "setup_otel_tracing",
    "span_processor",
    "start_time",
    "time_function",
    "tracer_provider",
    "wrapper",
]
# >>> AUTO-GEN (ai_runner)
__all__ = [
    "alert_router",
    "metrics",
    "otel_init",
    "sla_slo_dashboard",
]

# <<< AUTO-GEN
