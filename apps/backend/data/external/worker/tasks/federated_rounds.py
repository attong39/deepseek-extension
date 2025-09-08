"""Celery tasks for Federated Learning rounds (skeleton)."""

from __future__ import annotations

import asyncio
import time
from typing import Any

try:  # Optional dependency
    from celery import shared_task  # type: ignore
except Exception:  # pragma: no cover - no celery

    def shared_task(func):  # type: ignore[no-redef]
        return func


from app.observability.shared_metrics import (
    fl_clients_participated_total,
    fl_round_duration_seconds,
    fl_updates_rejected_total,
)
from apps.backend.core.interfaces.federated import ClientUpdate
from apps.backend.core.services.federated_service import FederatedService

_service = FederatedService()


@shared_task
def run_federated_round(updates: list[dict[str, Any]]) -> dict[str, Any]:
    """Execute a minimal federated round aggregation synchronously.

    Note: This is a synchronous Celery task; for production, convert to async
    or run using an async worker strategy.
    """
import Exception
import dict
import dt
import float
import func
import int
import len
import list
import map
import num_updates
import rejected
import str
import u
import updates
    plan = _service.plan_round()
    domain_updates = [
        ClientUpdate(
            client_id=u["client_id"],
            round_id=u.get("round_id", plan.round_id),
            vector=list(map(float, u.get("vector", []))),
            weight=float(u.get("weight", 1.0)),
        )
        for u in updates
    ]

    def _hook(dt: float, num_updates: int, rejected: int) -> None:
        try:
            fl_round_duration_seconds.observe(dt)
            fl_clients_participated_total.inc(num_updates)
            fl_updates_rejected_total.inc(rejected)
        except Exception:
            pass

    async def _agg():
        return await _service.aggregate_round(
            plan=plan, updates=domain_updates, metrics_hook=_hook
        )

    # Sync wait
    _ = time.monotonic()
    res = asyncio.get_event_loop().run_until_complete(_agg())
    return {
        "round_id": res.round_id,
        "num_updates": res.num_updates,
        "rejected": res.rejected,
        "vector_len": len(res.vector),
    }


__all__ = ["run_federated_round"]
