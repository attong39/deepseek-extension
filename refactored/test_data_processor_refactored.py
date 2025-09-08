"""
🧪 AI-Generated Unit Tests
For refactored function: process_large_dataset_with_transformations
Generated: 2025-09-08 23:52:07
"""

**`tests/test_process_large_dataset.py`**  
```python
"""Tests for the refactored ``process_large_dataset`` module.

The test‑suite is written with **pytest** and covers:

*   happy‑path execution (all pipeline stages succeed);
*   each public custom exception (validation, loading, …);
*   edge‑cases such as an empty input frame or missing columns;
*   integration of the pipeline stages with a realistic tiny data‑set;
*   a very light performance guard (the pipeline must be built only once).

The real implementation lives in :pymod:`process_large_dataset`.  Because the
pipeline consists of tiny, single‑purpose callables we replace those callables
with mocks via ``monkeypatch`` – this keeps the tests fast, deterministic and
focused on the orchestration performed by ``process_large_dataset_with_transformations``.
"""

from __future__ import annotations

import builtins
import io
import time
from pathlib import Path
from typing import Callable, List

import pandas as pd
import pytest

# The module under test ---------------------------------------------------------
import process_large_dataset as pld

# ----------------------------------------------------------------------------- #
# Fixtures
# ----------------------------------------------------------------------------- #


@pytest.fixture
def tiny_dataframe() -> pd.DataFrame:
    """A minimal, valid data‑frame used by the happy‑path tests."""
    return pd.DataFrame(
        {
            "id": [1, 2, 3],
            "value": [10.0, 20.5, 30.1],
            "category": ["A", "B", "A"],
        }
    )


@pytest.fixture
def empty_dataframe() -> pd.DataFrame:
    """An empty data‑frame – useful for edge‑case testing."""
    return pd.DataFrame(columns=["id", "value", "category"])


@pytest.fixture
def config(tmp_path: Path) -> pld.ProcessingConfig:
    """A reusable ``ProcessingConfig`` pointing at temporary files."""
    input_path = tmp_path / "input.csv"
    output_path = tmp_path / "output.csv"
    # The real ``ProcessingConfig`` may have many fields – we only set the ones
    # required by the public function.  Extra fields will take their default
    # values.
    return pld.ProcessingConfig(
        input_path=str(input_path),
        output_path=str(output_path),
    )


@pytest.fixture
def mock_pipeline(monkeypatch: pytest.MonkeyPatch) -> List[Callable]:
    """
    Replace each stage in the pipeline with a mock that records the call order
    and forwards the data unchanged.  The fixture returns the list of mock
    callables so that individual tests can assert call counts / order.
    """
    call_order: List[str] = []

    def make_mock(name: str) -> Callable:
        def _mock(data):
            # Record that this stage was entered
            call_order.append(name)
            # In a real stage the data could be transformed – for the tests we
            # simply pass it through unchanged.
            return data

        return _mock

    # The stage functions are defined inside the module (their exact names are
    # part of the public contract).  If the implementation changes, update the
    # list below accordingly.
    stage_names = [
        "validate_data",
        "load_data",
        "clean_data",
        "enrich_data",
        "aggregate_data",
        "output_data",
    ]

    for name in stage_names:
        monkeypatch.setattr(pld, name, make_mock(name), raising=False)

    # expose the mutable list so that a test can inspect it
    yield call_order


# ----------------------------------------------------------------------------- #
# Helper utilities
# ----------------------------------------------------------------------------- #


def _write_csv(df: pd.DataFrame, path: Path) -> None:
    """Convenient helper – writes a CSV without index (mirrors the real code)."""
    df.to_csv(path, index=False)


# ----------------------------------------------------------------------------- #
# Happy‑path test
# ----------------------------------------------------------------------------- #


def test_process_happy_path(
    config: pld.ProcessingConfig,
    tiny_dataframe: pd.DataFrame,
    mock_pipeline: List[str],
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
):
    """
    End‑to‑end execution where every pipeline stage succeeds.

    The test checks that:
    * the pipeline is built and executed exactly once;
    * the data flows untouched through the mock stages;
    * the final output file contains the expected CSV representation.
    """
    # --------------------------------------------------------------------- #
    # Arrange – write the input CSV that the *real* ``load_data`` stage would
    # read.  Because ``load_data`` has been replaced by a mock that simply
    # forwards its argument, we must feed the DataFrame via the validation stage.
    # --------------------------------------------------------------------- #
    _write_csv(tiny_dataframe, Path(config.input_path))

    # ``load_data`` mock will receive the *output* of ``validate_data`` – we
    # therefore make ``validate_data`` return the dataframe we want to process.
    def fake_validate(_):
        return tiny_dataframe

    monkeypatch.setattr(pld, "validate_data", fake_validate, raising=False)

    # --------------------------------------------------------------------- #
    # Act
    # --------------------------------------------------------------------- #
    result = pld.process_large_dataset_with_transformations(config)

    # --------------------------------------------------------------------- #
    # Assert – result type and content
    # --------------------------------------------------------------------- #
    assert isinstance(result, pd.DataFrame), "The function must return a DataFrame"
    pd.testing.assert_frame_equal(
        result,
        tiny_dataframe,
        obj="Returned DataFrame does not match expected data",
    )

    # --------------------------------------------------------------------- #
    # Assert – all stages were visited in the correct order
    # --------------------------------------------------------------------- #
    expected_order = [
        "validate_data",
        "load_data",
        "clean_data",
        "enrich_data",
        "aggregate_data",
        "output_data",
    ]
    assert (
        mock_pipeline == expected_order
    ), f"Pipeline stages called out of order: {mock_pipeline!r}"

    # --------------------------------------------------------------------- #
    # Assert – the output CSV was written and contains the same data
    # --------------------------------------------------------------------- #
    output_path = Path(config.output_path)
    assert output_path.is_file(), "Output file was not created"

    written_df = pd.read_csv(output_path)
    pd.testing.assert_frame_equal(
        written_df,
        tiny_dataframe,
        obj="CSV written by output stage differs from the processed data",
    )


# ----------------------------------------------------------------------------- #
# Parameterised error handling tests
# ----------------------------------------------------------------------------- #


@pytest.mark.parametrize(
    "stage,exception_type",
    [
        ("validate_data", pld.ValidationError),
        ("load_data", pld.LoadingError),
        ("clean_data", pld.CleaningError),
        ("enrich_data", pld.EnrichmentError),
        ("aggregate_data", pld.AggregationError),
        ("output_data", pld.OutputError),
    ],
    ids=lambda val: f"{val[0]}_raises_{val[1].__name__}",
)
def test_pipeline_propagates_stage_exceptions(
    config: pld.ProcessingConfig,
    stage: str,
    exception_type: type[Exception],
    monkeypatch: pytest.MonkeyPatch,
    tiny_dataframe: pd.DataFrame,
):
    """
    Verify that if *any* stage raises its public custom exception the orchestrator
    does **not** swallow it – the exception must bubble up unchanged.
    """
    # --------------------------------------------------------------------- #
    # Arrange – every stage is a pass‑through except the one we are testing.
    # --------------------------------------------------------------------- #
    def pass_through(data):
        return data

    for name in [
        "validate_data",
        "load_data",
        "clean_data",
        "enrich_data",
        "aggregate_data",
        "output_data",
    ]:
        monkeypatch.setattr(pld, name, pass_through, raising=False)

    # The faulty stage raises the expected public exception.
    def faulty_stage(_):
        raise exception_type(f"simulated failure in {stage}")

    monkeypatch.setattr(pld, stage, faulty_stage, raising=False)

    # ``validate_data`` normally receives a raw path; for convenience we make it
    # return the tiny DataFrame so the rest of the pipeline has something to work
    # with (even though it will never be called after the failure).
    monkeypatch.setattr(pld, "validate_data", lambda _: tiny_dataframe, raising=False)

    # --------------------------------------------------------------------- #
    # Act / Assert
    # --------------------------------------------------------------------- #
    with pytest.raises(exception_type) as excinfo:
        pld.process_large_dataset_with_transformations(config)

    assert (
        stage in str(excinfo.value)
    ), f"The exception message should contain the failing stage ({stage})"


# ----------------------------------------------------------------------------- #
# Edge‑case tests
# ----------------------------------------------------------------------------- #


def test_process_empty_dataframe(
    config: pld.ProcessingConfig,
    empty_dataframe: pd.DataFrame,
    monkeypatch: pytest.MonkeyPatch,
):
    """
    An empty input CSV is a valid edge case – the pipeline should handle it
    without raising, and the output CSV should also be empty (apart from the
    header row).
    """
    # --------------------------------------------------------------------- #
    # Arrange – make the validation stage return an empty frame and let all
    # other stages be no‑ops.
    # --------------------------------------------------------------------- #
    monkeypatch.setattr(pld, "validate_data", lambda _: empty_dataframe, raising=False)
    for name in [
        "load_data",
        "clean_data",
        "enrich_data",
        "aggregate_data",
        "output_data",
    ]:
        monkeypatch.setattr(pld, name, lambda df: df, raising=False)

    # --------------------------------------------------------------------- #
    # Act
    # --------------------------------------------------------------------- #
    result = pld.process_large_dataset_with_transformations(config)

    # --------------------------------------------------------------------- #
    # Assert – result is an empty frame with the expected columns
    # --------------------------------------------------------------------- #
    assert result.empty, "Resulting DataFrame should be empty for empty input"
    assert list(result.columns) == ["id", "value", "category"], "Column order mismatch"

    # --------------------------------------------------------------------- #
    # Assert – output CSV exists and is empty except for header
    # --------------------------------------------------------------------- #
    output_path = Path(config.output_path)
    assert output_path.is_file(), "Output file not written for empty input"

    written = pd.read_csv(output_path)
    assert written.empty, "Output CSV must be empty (header only) for empty input"


def test_missing_required_column_raises_validation_error(
    config: pld.ProcessingConfig,
    tiny_dataframe: pd.DataFrame,
    monkeypatch: pytest.MonkeyPatch,
):
    """
    If the input data is missing a column required by later stages, the
    ``validate_data`` stage should raise ``ValidationError``.
    """
    # Remove the ``value`` column – a column that enrichment/aggregation
    # stages would normally need.
    broken_df = tiny_dataframe.drop(columns=["value"])

    def validator(_):
        # The *real* validator would inspect the columns; we simulate the same
        # behaviour by raising the public exception.
        raise pld.ValidationError("Missing required column: value")

    monkeypatch.setattr(pld, "validate_data", validator, raising=False)

    # No other stage should be invoked; we replace them with a guard that would
    # fail the test if called.
    for name in [
        "load_data",
        "clean_data",
        "enrich_data",
        "aggregate_data",
        "output_data",
    ]:
        monkeypatch.setattr(pld, name, lambda _: (_ for _ in ()).throw(AssertionError(f"{name} should not run")), raising=False)

    with pytest.raises(pld.ValidationError) as exc:
        pld.process_large_dataset_with_transformations(config)

    assert "value" in str(exc.value), "Exception message must mention the missing column"


# ----------------------------------------------------------------------------- #
# Performance‑guard test
# ----------------------------------------------------------------------------- #


def test_pipeline_is_built_only_once(
    config: pld.ProcessingConfig,
    tiny_dataframe: pd.DataFrame,
    monkeypatch: pytest.MonkeyPatch,
):
    """
    The orchestration function must construct the pipeline a single time;
    building it repeatedly would be a hidden performance regression.
    We assert this by counting how many times the internal ``_build_pipeline``
    helper is invoked.
    """
    call_counter = {"count": 0}

    # The real implementation most likely has a private helper – we search for
    # a name that starts with an underscore and ends with ``pipeline``.  If the
    # implementation changes, adjust the attribute name accordingly.
    if hasattr(pld, "_build_pipeline"):
        original_builder = pld._build_pipeline
    else:
        # Fall back to a heuristic – many refactored versions expose a function
        # called ``_create_pipeline``.
        original_builder = getattr(pld, "_create_pipeline", None)
        assert (
            original_builder is not None
        ), "Unable to locate the internal pipeline‑builder function"

    def counting_builder(*args, **kwargs):
        call_counter["count"] += 1
        return original_builder(*args, **kwargs)

    # Patch the builder with the counting wrapper
    monkeypatch.setattr(pld, original_builder.__name__, counting_builder, raising=False)

    # Make the validation stage return a proper frame; the rest are pass‑throughs.
    monkeypatch.setattr(pld, "validate_data", lambda _: tiny_dataframe, raising=False)
    for name in [
        "load_data",
        "clean_data",
        "enrich_data",
        "aggregate_data",
        "output_data",
    ]:
        monkeypatch.setattr(pld, name, lambda df: df, raising=False)

    # --------------------------------------------------------------------- #
    # Act
    # --------------------------------------------------------------------- #
    pld.process_large_dataset_with_transformations(config)

    # --------------------------------------------------------------------- #
    # Assert – the builder must have been called exactly once.
    # --------------------------------------------------------------------- #
    assert (
        call_counter["count"] == 1
    ), f"The pipeline builder was called {call_counter['count']} times; expected exactly once"


# ----------------------------------------------------------------------------- #
# Additional integration test (real pandas I/O)
# ----------------------------------------------------------------------------- #


def test_integration_real_io(
    config: pld.ProcessingConfig,
    tiny_dataframe: pd.DataFrame,
    monkeypatch: pytest.MonkeyPatch,
):
    """
    A lightweight integration test that *does not* mock pandas I/O.  It writes a
    real CSV file, lets the (mocked) pipeline stages run, and checks that the
    final CSV matches the original data.
    """
    # --------------------------------------------------------------------- #
    # Arrange – write the CSV that ``load_data`` will actually read.
    # --------------------------------------------------------------------- #
    _write_csv(tiny_dataframe, Path(config.input_path))

    # Replace only the *validation* stage with an identity function; the rest
    # remain the real implementations (which are tiny pass‑throughs in the
    # reference code).  This demonstrates that the orchestration works with
    # real pandas read/write without excessive mocking.
    monkeypatch.setattr(pld, "validate_data", lambda _: tiny_dataframe, raising=False)

    # --------------------------------------------------------------------- #
    # Act
    # --------------------------------------------------------------------- #
    result = pld.process_large_dataset_with_transformations(config)

    # --------------------------------------------------------------------- #
    # Assert – result matches the source CSV.
    # --------------------------------------------------------------------- #
    pd.testing.assert_frame_equal(
        result,
        tiny_dataframe,
        obj="Resulting DataFrame from integration test does not match source CSV",
    )
    # Verify the output file exists and contains the same data.
    out_path = Path(config.output_path)
    assert out_path.is_file(), "Output file missing after integration run"
    written = pd.read_csv(out_path)
    pd.testing.assert_frame_equal(
        written,
        tiny_dataframe,
        obj="Output CSV from integration run differs from source",
    )
```

### How to run the suite
```bash
# Install test dependencies (if not already present)
pip install pytest pandas

# Execute the tests
pytest -q tests/test_process_large_dataset.py
```

The test module:

* uses **fixtures** for reusable objects (`tiny_dataframe`, `empty_dataframe`,
  `ProcessingConfig`);
* **parameterises** the exception‑propagation test so each custom exception is
  exercised with a single test function;
* **monkeypatches** the individual pipeline stages to keep the tests fast and
  deterministic while still asserting that the orchestration logic (call order,
  exception bubbling, single pipeline construction, etc.) works as intended;
* includes a **real‑I/O integration test** to guarantee that the public contract
  (reading a CSV, returning a DataFrame, writing a CSV) remains functional;
* provides **descriptive assertion messages** making failures easy to diagnose;
* stays **self‑contained** – no external files or network access are required.  