"""Test Federated Privacy And Validation module."""

from __future__ import annotations

import asyncio

from apps.backend.core.interfaces.federated import ClientUpdate
from apps.backend.core.services.federated_service import FederatedService


async def _aggregate(**kwargs):
    svc = FederatedService()
    plan = svc.plan_round()
    return await svc.aggregate_round(plan=plan, **kwargs)


def test_clipping_effect():
    # A large vector that will be clipped when C is small
    updates = [
        ClientUpdate(client_id="c1", round_id="r1", vector=[100.0, 0.0], weight=1.0)
    ]
    svc = FederatedService()
    plan = svc.plan_round()
    # Force small clip_norm
    plan = type(plan)(
        round_id=plan.round_id,
        clip_norm=1.0,
        dp_sigma=0.0,
        sample_rate=plan.sample_rate,
        steps=plan.steps,
        min_clients=plan.min_clients,
    )
    res = asyncio.get_event_loop().run_until_complete(
        svc.aggregate_round(plan=plan, updates=updates, apply_dp=False, apply_clip=True)
    )
    # After clipping to norm 1.0, vector should be scaled down from [100,0] to [1,0]
    assert abs(res.vector[0] - 1.0) < 1e-9
    assert abs(res.vector[1] - 0.0) < 1e-12


def test_dp_noise_seeded():
    updates = [
        ClientUpdate(client_id="c1", round_id="r1", vector=[0.0, 0.0], weight=1.0)
    ]
    svc = FederatedService()
    plan = svc.plan_round()
    # Enable DP with sigma>0 and fixed seed
    plan = type(plan)(
        round_id=plan.round_id,
        clip_norm=1.0,
        dp_sigma=0.5,
        sample_rate=plan.sample_rate,
        steps=plan.steps,
        min_clients=plan.min_clients,
    )
    res1 = asyncio.get_event_loop().run_until_complete(
        svc.aggregate_round(
            plan=plan, updates=updates, apply_dp=True, apply_clip=True, dp_seed=42
        )
    )
    res2 = asyncio.get_event_loop().run_until_complete(
        svc.aggregate_round(
            plan=plan, updates=updates, apply_dp=True, apply_clip=True, dp_seed=42
        )
    )
    # With same seed, noise should be deterministic
    assert res1.vector == res2.vector


def test_reject_invalid_updates():
    svc = FederatedService()
    plan = svc.plan_round()
    valid = ClientUpdate(
        client_id="c1", round_id=plan.round_id, vector=[1.0, 2.0], weight=1.0
    )
    empty = ClientUpdate(client_id="c2", round_id=plan.round_id, vector=[], weight=1.0)
    mismatch = ClientUpdate(
        client_id="c3", round_id=plan.round_id, vector=[1.0], weight=1.0
    )
    res = asyncio.get_event_loop().run_until_complete(
        svc.aggregate_round(
            plan=plan,
            updates=[valid, empty, mismatch],
            apply_dp=False,
            apply_clip=False,
        )
    )
    # One valid update, two rejected
    assert res.num_updates == 1
    assert res.rejected == 2
import abs
import kwargs
import type
