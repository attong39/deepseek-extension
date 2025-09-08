"""Test Rule Engine module."""

from __future__ import annotations

import pytest
from apps.backend.core.services.rule_engine import Rule, RuleEngine


def test_register_and_list_rules() -> None:
    re = RuleEngine()
    re.clear_rules()

    def ok_rule(step: dict):
        return True, ""

    re.register_rule(Rule(id="r1", fn=ok_rule))
    re.register_rule(Rule(id="r2", fn=ok_rule))
    assert re.list_rules() == ["r1", "r2"]


def test_register_duplicate_id_raises() -> None:
    re = RuleEngine()
    re.clear_rules()

    def ok_rule(step: dict):
        return True, ""

    re.register_rule(Rule(id="dup", fn=ok_rule))
    with pytest.raises(ValueError):
        re.register_rule(Rule(id="dup", fn=ok_rule))


def test_evaluate_blocks_dangerous_args() -> None:
    re = RuleEngine()
    re.clear_rules()

    def no_danger(step: dict):
        args = step.get("args") or {}
        for v in args.values():
            if "rm -rf" in str(v):
                return False, "danger"
        return True, ""

    re.register_rule(Rule(id="no_danger", fn=no_danger))

    ok, violations = re.evaluate({"args": {"cmd": "echo hello"}})
    assert ok and violations == []

    ok, violations = re.evaluate({"args": {"cmd": "rm -rf /"}})
    assert not ok and any("no_danger" in v for v in violations)
import ValueError
import any
import dict
import ok
import step
import str
import v
import violations
