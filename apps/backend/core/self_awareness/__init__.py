"""
from __future__ import annotations

zeta_vn.core.self_awareness package.

Auto-fixed by comprehensive_init_fixer.py
"""

from apps.backend.core.self_awareness.health_monitor import (
    HealthMonitor,
    HealthReport,
    MetricsHealth,
    RepositoryHealth,
    RestartCallback,
    WebSocketHealth,
)

__all__ = [
    "HealthMonitor",
    "HealthReport",
    "MetricsHealth",
    "RepositoryHealth",
    "RestartCallback",
    "WebSocketHealth",
    "active_connections",
    "avg_outbox_lag",
    "cpu_usage",
    "critical_failures",
    "db_ok",
    "db_uptime",
    "disk_usage",
    "error_rate",
    "get_health_summary",
    "get_recent_history",
    "latest",
    "memory_usage",
    "outbox_lag",
    "recent_reports",
    "recovery_actions",
    "report",
    "restart_details",
    "stop_monitoring",
    "system_metrics",
    "timestamp",
    "ws_ok",
    "ws_uptime",
]
# >>> AUTO-GEN (ai_runner)
__all__ = [
    "health_monitor",
]

# <<< AUTO-GEN
