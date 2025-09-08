"""
from __future__ import annotations

zeta_vn.data.migrations package.

Auto-fixed by comprehensive_init_fixer.py
"""

import sys

__all__ = [
    "ANALYTICS_EVENTS_TABLE",
    "ARCHIVED_FALSE",
    "AUDIT_LOGS_TABLE",
    "COMPLETED_EXECUTIONS",
    "CONVERSATIONS_TABLE",
    "CRITICAL_SEVERITY",
    "FAILED_STATUS",
    "HIGH_IMPORTANCE",
    "HIGH_THREAT",
    "JSONB_EMPTY",
    "MESSAGES_TABLE",
    "MESSAGE_ATTACHMENTS_TABLE",
    "PERFORMANCE_METRICS_TABLE",
    "RECENT_EVENTS",
    "RUNNING_STATUSES",
    "SECURITY_EVENTS_TABLE",
    "STATUS_ACTIVE",
    "SYSTEM_EVENTS_TABLE",
    "USERS_TABLE",
    "USER_SESSIONS_TABLE",
    "branch_labels",
    "depends_on",
    "down_revision",
    "downgrade",
    "revision",
    "upgrade",
]
# >>> AUTO-GEN (ai_runner)
__all__ = [
    "001_add_outbox_tables",
    "001_initial_schema",
    "002_agent_tables",
    "003_chat_tables",
    "004_memory_tables",
    "005_analytics_tables",
    "006_audit_tables",
    "007_indexes",
    "008_perf_targeted_indexes",
    "009_training_models",
    "010_fl_tables",
    "011_release_table",
    "012_add_authz_tables",
]

# <<< AUTO-GEN
