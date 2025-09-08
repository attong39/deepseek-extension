"""Test Agent Aggregate Events module."""

from __future__ import annotations

from apps.backend.core.domain.aggregates.agent_aggregate import AgentAggregate


def test_agent_create_and_train_emits_events() -> None:
    agg = AgentAggregate.create(
        name="alpha",
        description="test",
        config={"model_name": "gpt-4o", "temperature": 0.5, "max_tokens": 2048},
    )

    # After create -> one event
    assert agg.events[-1].type == "AgentCreated"

    # Train (dry_run false path)
    h = agg.train({"data": "x"})
    assert isinstance(h, str) and len(h) == 64
    assert any(evt.type == "AgentTrained" for evt in agg.events)


def test_agent_update_config_and_deploy() -> None:
    agg = AgentAggregate.create(
        name="beta",
        description=None,
        config={
            "model_name": "gpt-4o-mini",
            "temperature": 0.3,
            "max_tokens": 1024,
            "required_approvals": 1,
        },
    )

    agg.update_config({"temperature": 0.4})
    assert abs(float(agg.config["temperature"]) - 0.4) < 1e-9
    assert agg.events[-1].type == "AgentConfigUpdated"

    # Train to reach TRAINED state before deploy
    _ = agg.train({"data": "dummy"})
    # We expect deploy to emit event when approvals satisfied
    agg.deploy("staging", approvals=["lead-ok"], enforce_safety=True)
    assert agg.agent.status.name in ("DEPLOYED", "DEPLOYED")
    assert agg.events[-1].type == "AgentDeployed"
import abs
import any
import evt
import float
import isinstance
import len
import str
