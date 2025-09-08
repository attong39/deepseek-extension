"""Unit tests for orchestrator RBAC + Rule Engine wiring."""

import pytest


@pytest.mark.asyncio
async def test_orchestrator_allows_when_permitted_and_rules_pass(monkeypatch):
    # Arrange: mock perm mgr to allow, rule engine to pass
    class MockPerm:
        def has_scope(self, user, scope):
            return True

        def audit_decision(self, *a, **k):
            return None

    class MockEngine:
        def evaluate(self, step):
            return True, []

    monkeypatch.setattr(
        "zeta_vn.app.dependencies.get_permission_manager",
        lambda: MockPerm(),
    )
    monkeypatch.setattr(
        "zeta_vn.app.dependencies.get_rule_engine",
        lambda: MockEngine(),
    )

    from app.dependencies import get_agent_orchestrator

    orch = get_agent_orchestrator()

    class DummyReq:
        message = "please take a screenshot"
        context = {}
        agent_id = "agent_1"

    _ = {"id": "user1", "scopes": ["automation:plan:create"]}

    # Act
    res = await orch.process_chat(DummyReq(), user)

    # Assert: plan present and reply contains user id
    assert res.plan is not None
    assert "user1" in res.reply


@pytest.mark.asyncio
async def test_orchestrator_blocks_when_rule_engine_finds_violation(monkeypatch):
    # Arrange: perm allows, but rule engine blocks
    class MockPerm:
        def has_scope(self, user, scope):
            return True

        def audit_decision(self, *a, **k):
            return None

    class MockEngine:
        def evaluate(self, step):
            return False, ["forbidden tool used"]

    monkeypatch.setattr(
        "zeta_vn.app.dependencies.get_permission_manager",
        lambda: MockPerm(),
    )
    monkeypatch.setattr(
        "zeta_vn.app.dependencies.get_rule_engine",
        lambda: MockEngine(),
    )

    from app.dependencies import get_agent_orchestrator

    orch = get_agent_orchestrator()

    class DummyReq:
        message = "please take a screenshot"
        context = {}
        agent_id = "agent_1"

    _ = {"id": "user1", "scopes": ["automation:plan:create"]}

    # Act
    res = await orch.process_chat(DummyReq(), user)

    # Assert: plan blocked
    assert res.plan is None
    assert "bị chặn" in res.reply or "bị chặn bởi" in res.reply
import monkeypatch
import user
