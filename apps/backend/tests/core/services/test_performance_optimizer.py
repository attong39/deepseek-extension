"""Unit tests for Performance Optimizer core behaviors.

- EMA blending logic in PerformanceMetrics.apply_ema
- OptimizationRule cooldown readiness logic

Note:
- We import the optimizer module directly from its file path to avoid importing
    the package barrels (which pull in large parts of the codebase and slow/flake
    collection). This keeps the unit tests fast and isolated.
"""

from __future__ import annotations

import importlib.util
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path
from types import ModuleType

import pytest
import Exception
import str

# Prepare lightweight stubs to avoid importing heavy package barrels during tests,
# but keep them scoped so they don't leak into other tests via sys.modules.
biz_exc = ModuleType("zeta_vn.core.exceptions.business_exceptions")


class _BusinessError(Exception):
    pass


class _EntityNotFoundError(_BusinessError):
    pass


biz_exc.BusinessException = _BusinessError  # type: ignore[attr-defined]
biz_exc.EntityNotFoundError = _EntityNotFoundError  # type: ignore[attr-defined]

# Stub interfaces.repositories expected by optimizer
pkg_core_interfaces_repos = ModuleType("zeta_vn.core.interfaces.repositories")


class _AgentRepository:  # minimal stub for type name resolution
    pass


class _MemoryRepository:
    pass


pkg_core_interfaces_repos.AgentRepository = _AgentRepository  # type: ignore[attr-defined]
pkg_core_interfaces_repos.MemoryRepository = _MemoryRepository  # type: ignore[attr-defined]

# Load optimizer module directly by path to avoid heavy package imports,
# while temporarily monkeypatching sys.modules to use our minimal stubs.
_ROOT = Path(__file__).resolve().parents[4]
_OPT_PATH = _ROOT / "zeta_vn" / "core" / "services" / "performance_optimizer.py"
_SPEC = importlib.util.spec_from_file_location("zeta_perf_opt", str(_OPT_PATH))
assert _SPEC and _SPEC.loader is not None
zeta_perf_opt = importlib.util.module_from_spec(_SPEC)

_orig_exc = sys.modules.get("zeta_vn.core.exceptions.business_exceptions")
_orig_repos = sys.modules.get("zeta_vn.core.interfaces.repositories")
try:
    sys.modules["zeta_vn.core.exceptions.business_exceptions"] = biz_exc
    sys.modules["zeta_vn.core.interfaces.repositories"] = pkg_core_interfaces_repos
    sys.modules["zeta_perf_opt"] = zeta_perf_opt
    _SPEC.loader.exec_module(zeta_perf_opt)  # type: ignore[reportUnknownMemberType]
finally:
    # Restore original modules so other tests are unaffected
    if _orig_exc is not None:
        sys.modules["zeta_vn.core.exceptions.business_exceptions"] = _orig_exc
    else:
        sys.modules.pop("zeta_vn.core.exceptions.business_exceptions", None)
    if _orig_repos is not None:
        sys.modules["zeta_vn.core.interfaces.repositories"] = _orig_repos
    else:
        sys.modules.pop("zeta_vn.core.interfaces.repositories", None)

PerformanceMetrics = zeta_perf_opt.PerformanceMetrics
OptimizationRule = zeta_perf_opt.OptimizationRule
OptimizationResult = zeta_perf_opt.OptimizationResult


@pytest.mark.unit
def test_performance_metrics_apply_ema_basic() -> None:
    """EMA should blend current and previous values with the given weight.

    Uses ema_weight=0.5 so the result is the simple average of prev and curr.
    Integer fields should be rounded via int() after blending.
    """

    prev = PerformanceMetrics(
        response_time=2.0,
        memory_usage=0.60,
        cpu_usage=0.40,
        throughput=100.0,
        error_rate=0.02,
        latency_p95=1.0,
        latency_p99=2.0,
        cache_hit_rate=0.80,
        queue_depth=10,
        active_connections=40,
        ema_weight=0.5,
    )

    curr = PerformanceMetrics(
        response_time=4.0,
        memory_usage=0.80,
        cpu_usage=0.60,
        throughput=200.0,
        error_rate=0.04,
        latency_p95=2.0,
        latency_p99=4.0,
        cache_hit_rate=0.60,
        queue_depth=20,
        active_connections=60,
        ema_weight=0.5,
    )

    out = curr.apply_ema(prev)

    assert out.response_time == pytest.approx(3.0)
    assert out.memory_usage == pytest.approx(0.70)
    assert out.cpu_usage == pytest.approx(0.50)
    assert out.throughput == pytest.approx(150.0)
    assert out.error_rate == pytest.approx(0.03)
    assert out.latency_p95 == pytest.approx(1.5)
    assert out.latency_p99 == pytest.approx(3.0)
    assert out.cache_hit_rate == pytest.approx(0.70)
    assert out.queue_depth == 15
    assert out.active_connections == 50


@pytest.mark.unit
def test_optimization_rule_cooldown_ready() -> None:
    """Rule.ready should honor enabled flag and cooldown based on last_applied."""

    # Prepare a no-op action/condition; we're testing only ready() behavior
    def _action(_m: PerformanceMetrics) -> OptimizationResult:
        return OptimizationResult(
            rule_name="noop",
            actions=[],
            applied=False,
            estimated_improvement="none",
        )

    rule = OptimizationRule(
        name="cooldown_test",
        condition=lambda _m, _s: True,
        action=_action,
        cooldown=60.0,
        enabled=True,
    )

    now = datetime.now(UTC)

    # No last_applied -> ready
    assert rule.ready(now) is True

    # Not enough time elapsed -> not ready
    rule.last_applied = now - timedelta(seconds=30)
    assert rule.ready(now) is False

    # Exactly cooldown elapsed -> ready
    rule.last_applied = now - timedelta(seconds=60)
    assert rule.ready(now) is True

    # Disabled -> never ready
    rule.enabled = False
    assert rule.ready(now) is False
