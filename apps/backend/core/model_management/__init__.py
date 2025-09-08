"""
from __future__ import annotations

zeta_vn.core.model_management package.

Auto-fixed by comprehensive_init_fixer.py
"""

from apps.backend.core.model_management.router import (
    ModelRequest,
    ModelRouter,
    ModelSpec,
    get_coding_model,
    get_edge_model,
    get_model_router,
    get_realtime_model,
    get_student_model,
    get_teacher_model,
    get_vision_model,
    select_optimal_model,
)

__all__ = [
    "GuardedModelRouter",
    "ModelRequest",
    "ModelRouter",
    "ModelSpec",
    "actual_id",
    "best_candidate",
    "candidates",
    "chosen",
    "config",
    "config_path",
    "context",
    "context_score",
    "cost",
    "cost_score",
    "estimate_cost",
    "filtered",
    "get_coding_model",
    "get_edge_model",
    "get_model_router",
    "get_model_spec",
    "get_realtime_model",
    "get_student_model",
    "get_teacher_model",
    "get_vision_model",
    "is_external",
    "latency_score",
    "list_models",
    "logger",
    "max_context",
    "max_cost",
    "max_latency",
    "model_id",
    "models",
    "request",
    "router",
    "safe_req",
    "score",
    "scored",
    "scored_candidates",
    "select_model",
    "select_model_guarded",
    "select_model_safe",
    "select_optimal_model",
    "selected_model",
    "sens",
    "sensitive_context",
    "spec",
    "total_tokens",
]
# >>> AUTO-GEN (ai_runner)
__all__ = [
    "router",
    "router_guard",
]

# <<< AUTO-GEN
