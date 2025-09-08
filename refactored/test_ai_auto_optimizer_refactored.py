"""
🧪 AI-Generated Unit Tests
For refactored function: optimize_performance_bottlenecks
Generated: 2025-09-08 23:55:52
"""

```python
# test_optimize.py
"""
Unit‑tests for the ``optimize`` module.

The public contract we exercise is:

* ``optimize_performance_bottlenecks(records, cfg) -> List[Dict]``
* ``BottleneckType`` – ``CPU``, ``IO`` and ``MEMORY`` (the enum values are
  ``"cpu"``, ``"io"``, ``"mem"``)
* ``OptimizationError`` – raised for configuration/validation problems
* ``OptimizationContext`` – internal mutable container; we only use it
  indirectly (via the public function) but we can monkey‑patch its methods
  to assert that metrics are collected.

The tests are deliberately written against the *behaviour* described in the
module doc‑string rather than a concrete implementation, so they stay valid
even if the internal helpers are refactored again.
"""

from __future__ import annotations

import time
from typing import List, Dict

import pytest

# The module under test – it must be importable from the project root.
# If the file lives in a package, adjust the import accordingly.
from optimize import (
    optimize_performance_bottlenecks,
    BottleneckType,
    OptimizationError,
    OptimizationContext,
)


# --------------------------------------------------------------------------- #
# Fixtures
# --------------------------------------------------------------------------- #
@pytest.fixture
def sample_records() -> List[Dict]:
    """
    A small but varied collection of bottleneck records.
    Each record contains the three possible metrics and an ``id``.
    """
    return [
        {"id": 1, "cpu": 0.95, "io": 0.10, "mem": 0.30},
        {"id": 2, "cpu": 0.45, "io": 0.85, "mem": 0.20},
        {"id": 3, "cpu": 0.20, "io": 0.25, "mem": 0.95},
        {"id": 4, "cpu": 0.70, "io": 0.70, "mem": 0.70},
    ]


@pytest.fixture
def min_cfg() -> Dict:
    """
    The *minimum* valid configuration – the function only requires a
    ``bottleneck_type`` and a ``threshold`` (both mandatory according to the
    documentation).
    """
    return {"bottleneck_type": "cpu", "threshold": 0.5}


# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #
def _expected_optimised(record: Dict, bottleneck: BottleneckType, threshold: float) -> bool:
    """
    Helper that mirrors the optimisation rule used by the library:
    ``record[<bottleneck>] >= threshold`` → ``optimised=True``.
    """
    metric = record[bottleneck.value]  # enum values are the dict keys
    return metric >= threshold


# --------------------------------------------------------------------------- #
# Happy‑path tests
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    "b_type,threshold,expected_flags",
    [
        # CPU – simple threshold
        ("cpu", 0.5, [True, False, False, True]),
        # IO – a higher threshold, more False values
        ("io", 0.75, [False, True, False, True]),
        # MEMORY – threshold at the upper edge
        ("mem", 0.90, [False, False, True, True]),
    ],
)
def test_optimize_happy_path(
    sample_records: List[Dict],
    b_type: str,
    threshold: float,
    expected_flags: List[bool],
) -> None:
    """
    Verify that the function returns a list of the same length, keeps the
    original ``id`` and metric, and adds the correct ``optimised`` flag.
    """
    cfg = {"bottleneck_type": b_type, "threshold": threshold}
    result = optimize_performance_bottlenecks(sample_records, cfg)

    # ------------------------------------------------------------------- #
    # 1️⃣  Length & identity checks
    # ------------------------------------------------------------------- #
    assert isinstance(result, list), "Result should be a list"
    assert len(result) == len(sample_records), "Result length must match input length"

    # ------------------------------------------------------------------- #
    # 2️⃣  Payload validation
    # ------------------------------------------------------------------- #
    for idx, (orig, processed) in enumerate(zip(sample_records, result)):
        # ``id`` must be retained unchanged
        assert processed["id"] == orig["id"], f"Record {idx}: id corrupted"

        # The metric used for optimisation must be present and unchanged
        assert processed[b_type] == orig[b_type], f"Record {idx}: {b_type} metric altered"

        # The ``optimised`` flag must match the expected boolean
        assert processed["optimised"] is expected_flags[idx], (
            f"Record {idx}: expected optimised={expected_flags[idx]}, "
            f"got {processed['optimised']}"
        )


# --------------------------------------------------------------------------- #
# Edge‑case tests – empty input, boundary thresholds, and extreme metric values
# --------------------------------------------------------------------------- #
def test_optimize_empty_records(min_cfg: Dict) -> None:
    """An empty list should result in an empty list – never an error."""
    empty: List[Dict] = []
    assert optimize_performance_bottlenecks(empty, min_cfg) == []


@pytest.mark.parametrize(
    "threshold,expected_flags",
    [
        (0.0, [True, True, True, True]),   # everything meets the lowest possible threshold
        (1.0, [False, False, False, False]),  # nothing can exceed 1.0 (metrics are in [0,1])
    ],
)
def test_optimize_boundary_thresholds(sample_records: List[Dict], threshold: float, expected_flags: List[bool]) -> None:
    """Thresholds at the extremes of the allowed range must behave sensibly."""
    cfg = {"bottleneck_type": "cpu", "threshold": threshold}
    result = optimize_performance_bottlenecks(sample_records, cfg)

    assert [rec["optimised"] for rec in result] == expected_flags


# --------------------------------------------------------------------------- #
# Validation & error handling
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    "bad_cfg,expected_msg",
    [
        ({"threshold": 0.5}, "missing required key 'bottleneck_type'"),
        ({"bottleneck_type": "gpu", "threshold": 0.5}, "unsupported bottleneck type"),
        ({"bottleneck_type": "cpu", "threshold": "high"}, "threshold must be a number"),
        ({"bottleneck_type": "cpu"}, "missing required key 'threshold'"),
    ],
)
def test_optimize_invalid_config(sample_records: List[Dict], bad_cfg: Dict, expected_msg: str) -> None:
    """
    The public API must raise ``OptimizationError`` with a helpful message when
    the configuration dictionary is malformed.
    """
    with pytest.raises(OptimizationError) as excinfo:
        optimize_performance_bottlenecks(sample_records, bad_cfg)

    assert expected_msg in str(excinfo.value)


def test_optimize_non_iterable_records(min_cfg: Dict) -> None:
    """Passing a non‑iterable (e.g. ``None``) for ``records`` should raise a TypeError."""
    with pytest.raises(TypeError, match="records must be an iterable"):
        optimize_performance_bottlenecks(None, min_cfg)  # type: ignore[arg-type]


# --------------------------------------------------------------------------- #
# Integration – ensuring the internal ``OptimizationContext`` collects metrics
# --------------------------------------------------------------------------- #
def test_context_metrics_are_populated(sample_records: List[Dict], monkeypatch: pytest.MonkeyPatch) -> None:
    """
    The function internally creates an ``OptimizationContext`` and stores
    runtime metrics (e.g. ``processed`` count and ``elapsed`` time).  By
    monkey‑patching the dataclass we can inspect the final state without
    changing the production code.
    """
    captured: Dict = {}

    # Save the original ``__init__`` so we can still construct the object.
    original_init = OptimizationContext.__init__

    def fake_init(self, config: Dict, metrics: Dict | None = None, results: List | None = None):
        # Call the real init first – this populates the fields we need.
        original_init(self, config, metrics or {}, results or [])
        # Keep a reference to the instance for later assertions.
        captured["instance"] = self

    monkeypatch.setattr(OptimizationContext, "__init__", fake_init)

    cfg = {"bottleneck_type": "io", "threshold": 0.6}
    _ = optimize_performance_bottlenecks(sample_records, cfg)

    ctx: OptimizationContext = captured["instance"]
    # The library is expected to record at least the following keys:
    assert "processed" in ctx.metrics, "Metric 'processed' not collected"
    assert ctx.metrics["processed"] == len(sample_records), (
        f"Expected {len(sample_records)} processed records, got {ctx.metrics['processed']}"
    )
    assert "elapsed" in ctx.metrics, "Metric 'elapsed' (runtime) not collected"
    assert isinstance(ctx.metrics["elapsed"], float), "Elapsed time must be a float"


# --------------------------------------------------------------------------- #
# Performance test – ensure the implementation scales linearly for large inputs
# --------------------------------------------------------------------------- #
@pytest.mark.timeout(2.0)  # Guard against pathological regressions
def test_optimize_performance_large_dataset(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Generate a synthetic dataset with 50 000 records and verify that the call
    finishes within a reasonable wall‑clock time (2 seconds on CI).  The exact
    threshold does not matter; we focus on runtime behaviour.
    """
    # Build the dataset – a tight loop is fine, the list lives in memory.
    large_dataset = [
        {"id": i, "cpu": i % 100 / 100.0, "io": (i * 3) % 100 / 100.0, "mem": (i * 7) % 100 / 100.0}
        for i in range(50_000)
    ]
    cfg = {"bottleneck_type": "mem", "threshold": 0.5}

    start = time.perf_counter()
    result = optimize_performance_bottlenecks(large_dataset, cfg)
    elapsed = time.perf_counter() - start

    # Basic sanity checks – we still get the same number of rows back.
    assert len(result) == len(large_dataset), "Result size mismatch for large input"

    # The elapsed time is already bounded by the pytest timeout decorator,
    # but we also expose a soft assertion for visibility in test reports.
    assert elapsed < 1.5, f"Optimization took {elapsed:.2f}s, expected <1.5s"


# --------------------------------------------------------------------------- #
# Parametrised round‑trip – ensure the function is deterministic and pure
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    "b_type,threshold",
    [
        ("cpu", 0.3),
        ("io", 0.6),
        ("mem", 0.9),
    ],
)
def test_optimize_idempotent(sample_records: List[Dict], b_type: str, threshold: float) -> None:
    """
    Running ``optimize_performance_bottlenecks`` twice on the *already
    optimised* output must not change the ``optimised`` flag again (the
    function should treat unknown keys gracefully and leave the flag untouched).
    """
    cfg = {"bottleneck_type": b_type, "threshold": threshold}
    first_pass = optimize_performance_bottlenecks(sample_records, cfg)
    second_pass = optimize_performance_bottlenecks(first_pass, cfg)

    # The two passes should be identical – a pure function.
    assert first_pass == second_pass, "Function is not idempotent / pure"


# --------------------------------------------------------------------------- #
# End of test suite
# --------------------------------------------------------------------------- #
``` 

### How to run the tests
```bash
# Install the test requirements (pytest is enough for the suite)
pip install pytest

# Run the full suite
pytest -q test_optimize.py
```

The suite covers:

| Aspect                              | Test(s)                                   |
|-------------------------------------|-------------------------------------------|
| **Happy path**                      | `test_optimize_happy_path`                |
| **Edge cases & boundaries**        | `test_optimize_empty_records`, `test_optimize_boundary_thresholds` |
| **Error handling / validation**    | `test_optimize_invalid_config`, `test_optimize_non_iterable_records` |
| **Input validation**               | same as above                             |
| **Integration between components** | `test_context_metrics_are_populated`      |
| **Performance considerations**     | `test_optimize_performance_large_dataset`, `test_optimize_idempotent` |
| **Idempotence / purity**           | `test_optimize_idempotent`                |

All tests are **self‑contained**, make use of **fixtures**, **parameterisation**, and **monkey‑patching** where necessary, and provide descriptive assertion messages to simplify debugging.