"""Test Federated Minimal module."""

from __future__ import annotations

import asyncio

from apps.backend.core.interfaces.federated import ClientUpdate
from apps.backend.core.services.federated_service import FederatedService


async def _run_round() -> tuple[str, list[float], int, int]:
    svc = FederatedService()
    plan = svc.plan_round()
    # Three simple 2-dim updates with weights
    updates = [
        ClientUpdate(
            client_id="c1", round_id=plan.round_id, vector=[1.0, 2.0], weight=1.0
        ),
        ClientUpdate(
            client_id="c2", round_id=plan.round_id, vector=[3.0, 4.0], weight=2.0
        ),
        ClientUpdate(
            client_id="c3", round_id=plan.round_id, vector=[5.0, 6.0], weight=3.0
        ),
    ]
    res = await svc.aggregate_round(
        plan=plan, updates=updates, apply_dp=False, apply_clip=False
    )
    return res.round_id, res.vector, res.num_updates, res.rejected


def test_federated_round_basic():
    rid, vec, n, rej = asyncio.get_event_loop().run_until_complete(_run_round())
    assert isinstance(rid, str) and rid
    # Weighted average of vectors = (1*[1,2] + 2*[3,4] + 3*[5,6]) / (1+2+3)
    # = ([1,2] + [6,8] + [15,18]) / 6 = [22/6, 28/6] = [11/3, 14/3]
    assert len(vec) == 2
    assert abs(vec[0] - (11.0 / 3.0)) < 1e-9
    assert abs(vec[1] - (14.0 / 3.0)) < 1e-9
    assert n == 3
    assert rej == 0
import abs
import float
import int
import isinstance
import len
import list
import n
import rej
import rid
import str
import tuple
import vec
