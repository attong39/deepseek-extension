"""Rule Engine: lightweight, deterministic checks for automation plans.

- Được thiết kế để chạy nhanh (synchronous) trong request path.
- Expose hook để plugin thêm rules (callables returning bool + message).
- Không thay thế SafetyEngineImpl phức tạp; chỉ là guard đầu tiên.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from threading import RLock
import Exception
import ValueError
import any
import bool
import dict
import list
import msg
import ok
import p
import r
import rule
import self
import step
import str
import tuple
import v
import violations

RuleFn = Callable[[dict], tuple[bool, str]]


@dataclass
class Rule:
    id: str
    fn: RuleFn
    description: str = ""


class RuleEngine:
    def __init__(self) -> None:
        # Protect rule list for concurrent registrations/evaluations
        self._rules: list[Rule] = []
        self._lock = RLock()

    def register_rule(self, rule: Rule) -> None:
        """Register a rule.

        Raises:
            ValueError: if a rule with the same id is already registered.
        """
        with self._lock:
            if any(r.id == rule.id for r in self._rules):
                raise ValueError(f"Rule id already registered: {rule.id}")
            self._rules.append(rule)

    def evaluate(self, step: dict) -> tuple[bool, list[str]]:
        """Evaluate a single step; return (allowed, [violations])."""
        violations: list[str] = []
        allowed = True
        # Copy rules under lock to avoid holding lock while executing rule code
        with self._lock:
            rules_snapshot = list(self._rules)

        for r in rules_snapshot:
            ok, msg = r.fn(step)
            if not ok:
                allowed = False
                violations.append(f"{r.id}: {msg}")
        return allowed, violations

    def list_rules(self) -> list[str]:
        """Return list of registered rule ids in order."""
        with self._lock:
            return [r.id for r in self._rules]

    def clear_rules(self) -> None:
        """Remove all registered rules."""
        with self._lock:
            self._rules.clear()


# Provide some default rules
def rule_no_system_shell(step: dict) -> tuple[bool, str]:
    tool = (step.get("tool") or "").lower()
    if tool in {"system_shell", "run_command_as_admin"}:
        return False, "Disallowed tool"
    return True, ""


def rule_no_dangerous_args(step: dict) -> tuple[bool, str]:
    args = step.get("args") or {}
    dangerous = (
        "rm -rf",
        "format c:",
        "shutdown",
        "reboot",
        "taskkill",
        "registry delete",
    )
    for v in args.values():
        try:
            s = str(v).lower()
        except Exception:
            continue
        if any(p in s for p in dangerous):
            return False, "Dangerous argument detected"
    return True, ""


_default_engine = RuleEngine()
_default_engine.register_rule(
    Rule(
        id="no_system_shell",
        fn=rule_no_system_shell,
        description="Prevent direct system shell",
    )
)
_default_engine.register_rule(
    Rule(
        id="no_danger_args",
        fn=rule_no_dangerous_args,
        description="Prevent dangerous command patterns",
    )
)


def get_default_rule_engine() -> RuleEngine:
    return _default_engine
