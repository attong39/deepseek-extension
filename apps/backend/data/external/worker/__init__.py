"""
from __future__ import annotations

zeta_vn.app.worker package.

Auto-fixed by comprehensive_init_fixer.py
"""

from apps.backend.data.external.worker.celery_app import celery_app

__all__ = [
    "ReleaseMetadata",
    "apply_flag",
    "celery_app",
    "checksum",
    "image",
    "k8s",
    "logger",
    "md",
    "meta",
    "ok",
    "out",
    "path",
    "perform_self_upgrade",
    "plan",
    "prev",
    "release_id",
    "results",
    "settings",
]
# >>> AUTO-GEN (ai_runner)
__all__ = [
    "celery_app",
    "self_upgrade",
]

# <<< AUTO-GEN
