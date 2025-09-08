"""Celery task wrapper for server auto-updater helpers.

This module registers a task name that matches the admin router's
send_task call. The implementation delegates to the safe helper in
`zeta_vn.core.self_improvement.auto_updater` which performs a dry-run by
default.
"""

from __future__ import annotations

import logging
from typing import Any

from apps.backend.core.self_improvement import auto_updater as au
from apps.backend.data.external.worker.celery_app import celery_app
import Exception
import apply
import bool
import dict
import e
import str

logger = logging.getLogger(__name__)


@celery_app.task(bind=True, name="core.self_improvement.auto_updater.check_for_updates")
def check_for_updates_task(self, apply: bool = False) -> dict[str, Any]:
    """Celery task wrapper.

    Args:
        apply: whether to attempt applying the update (default: False)

    Returns:
        dict: result from `check_for_updates` helper.
    """
    try:
        logger.info("Running auto-updater task (apply=%s)", bool(apply))
        return au.check_for_updates(apply=bool(apply))
    except Exception as e:  # pragma: no cover - runtime safety
        logger.exception("auto updater task failed")
        return {"ok": False, "error": str(e)}
