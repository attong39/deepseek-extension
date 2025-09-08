"""
🧪 AI-Generated Unit Tests
For refactored function: analyze_code_complexity_metrics
Generated: 2025-09-08 23:53:53
"""

**`tests/test_complexity_analyzer.py`**

```python
"""pytest test‑suite for the tiny “Complexity Analyzer” pipeline.

The production module (``complexity_analyzer.py``) is deliberately small –
each logical step lives in its own function and the public entry point is the
``ComplexityAnalyzer`` class.  The tests below cover:

* happy‑path execution (valid files, normal directory layout);
* edge‑cases such as empty files, files containing only comments/whitespace,
  and directories that contain no ``.py`` files;
* error handling – e.g. a non‑existent root, permission errors, and a broken
  file that raises ``OSError`` while being read;
* input validation – the public API should raise ``TypeError``/``ValueError``
  when called with the wrong type or an invalid path;
* integration – the end‑to‑end ``analyze`` method must glue the tiny helper
  functions together and produce a correct ``ProjectSummary``;
* a very‑light performance guard – analysing 200 tiny files must finish
  within a second (the real implementation is O(N) and cheap).

The test‑suite uses only the standard library, ``pytest`` fixtures and
``unittest.mock`` – no external dependency is required.
"""

from __future__ import annotations

import os
import time
from pathlib import Path
from typing import List

import pytest
from unittest import mock

# The module under test – import the public symbols that are part of the
# documented contract.  If the implementation adds more helpers they can be
# imported here as well.
from complexity_analyzer import (
    FileMetrics,
    ProjectSummary,
    ComplexityAnalyzer,
    # The tiny helpers are part of the public API in the refactored design.
    get_python_files,
    compute_loc,
    compute_cyclomatic_complexity,
    compute_maintainability_index,
    analyze_file,
)

# --------------------------------------------------------------------------- #
# Fixtures
# --------------------------------------------------------------------------- #

@pytest.fixture(scope="function")
def tiny_project(tmp_path: Path) -> Path:
    """Create a small, deterministic project tree used by many tests.

    The layout is::

        project/
            a.py            – 3 LOC, 2 control‑flow keywords
            b.py            – empty file (0 LOC, 0 complexity)
            sub/
                c.py        – 5 LOC, 3 control‑flow keywords
                __init__.py – comment‑only file (0 LOC, 0 complexity)
            not_python.txt   – should be ignored completely
    """
    # a.py -------------------------------------------------------------
    (tmp_path / "a.py").write_text(
        "\n".join(
            [
                "# a simple module",
                "def foo(x):",
                "    if x > 0:",
                "        return x",
                "    return -x",
            ]
        )
    )

    # b.py – completely empty
    (tmp_path / "b.py").write_text("")

    # sub/c.py ---------------------------------------------------------
    sub_dir = tmp_path / "sub"
    sub_dir.mkdir()
    (sub_dir / "c.py").write_text(
        "\n".join(
            [
                "for i in range(5):",
                "    try:",
                "        if i % 2 == 0:",
                "            print(i)",
                "    except Exception:",
                "        pass",
                "",
                "# trailing comment",
            ]
        )
    )

    # sub/__init__.py – comment only (should be ignored for LOC)
    (sub_dir / "__init__.py").write_text("# package marker\n")

    # not_python.txt – should be ignored
    (tmp_path / "not_python.txt").write_text("just some text")

    return tmp_path


# --------------------------------------------------------------------------- #
# Helper assertions
# --------------------------------------------------------------------------- #

def assert_file_metrics(
    metrics: FileMetrics,
    *,
    path: Path,
    loc: int,
    cyclomatic_complexity: int,
    maintainability_index: float,
) -> None:
    """Assert that a ``FileMetrics`` instance matches the expected values."""
    assert metrics.path == path, f"Incorrect path – expected {path}, got {metrics.path}"
    assert metrics.loc == loc, f"LOC mismatch for {path.name}: expected {loc}, got {metrics.loc}"
    assert (
        metrics.cyclomatic_complexity == cyclomatic_complexity
    ), (
        f"Cyclomatic complexity mismatch for {path.name}: "
        f"expected {cyclomatic_complexity}, got {metrics.cyclomatic_complexity}"
    )
    # The synthetic maintainability index is a float; we allow a tiny tolerance.
    assert (
        abs(metrics.maintainability_index - maintainability_index) < 1e-6
    ), (
        f"Maintainability index mismatch for {path.name}: "
        f"expected {maintainability_index}, got {metrics.maintainability_index}"
    )


# --------------------------------------------------------------------------- #
# 1️⃣  Happy‑path unit tests for the tiny helpers
# --------------------------------------------------------------------------- #

@pytest.mark.parametrize(
    "content,expected_loc",
    [
        ("", 0),  # empty file
        ("# comment only\n\n# another comment", 0),
        ("print('hello')\n\nx = 5  # inline comment", 2),
        ("def f():\n    pass\n\n# comment\n", 2),
    ],
)
def test_compute_loc_counts_non_empty_non_comment_lines(content: str, expected_loc: int, tmp_path: Path):
    """``compute_loc`` must ignore blank lines and full‑line comments."""
    file_path = tmp_path / "tmp.py"
    file_path.write_text(content)
    assert compute_loc(file_path) == expected_loc, "LOC calculation is wrong"


@pytest.mark.parametrize(
    "content,expected_cc",
    [
        ("", 0),
        ("if x:\n    pass", 1),
        ("for i in range(5):\n    while True:\n        pass", 2),
        ("try:\n    pass\nexcept Exception:\n    pass\nfinally:\n    pass", 3),
        ("def f():\n    if x:\n        for i in []:\n            try:\n                pass\n            except:\n                pass", 4),
    ],
)
def test_compute_cyclomatic_complexity_counts_keywords(content: str, expected_cc: int, tmp_path: Path):
    """Only the four supported keywords contribute to the heuristic CC."""
    file_path = tmp_path / "tmp.py"
    file_path.write_text(content)
    assert compute_cyclomatic_complexity(file_path) == expected_cc, "CC calculation is wrong"


def test_compute_maintainability_index_is_deterministic():
    """The synthetic formula is pure – same inputs must give the same output."""
    loc = 42
    cc = 7
    mi1 = compute_maintainability_index(loc, cc)
    mi2 = compute_maintainability_index(loc, cc)
    assert mi1 == mi2, "Maintainability index should be deterministic"
    # Simple sanity check – higher LOC or CC must not increase the index
    assert compute_maintainability_index(loc + 1, cc) < mi1
    assert compute_maintainability_index(loc, cc + 1) < mi1


def test_analyze_file_returns_correct_metrics(tiny_project: Path):
    """End‑to‑end test of ``analyze_file`` on a known file."""
    a_py = tiny_project / "a.py"
    metrics = analyze_file(a_py)

    # a.py → 3 LOC (comment line ignored)
    #       → cyclomatic: 2 (one ``if`` and the implicit ``def`` does NOT count)
    expected_mi = compute_maintainability_index(loc=3, cyclomatic_complexity=2)

    assert_file_metrics(
        metrics,
        path=a_py.resolve(),
        loc=3,
        cyclomatic_complexity=2,
        maintainability_index=expected_mi,
    )


# --------------------------------------------------------------------------- #
# 2️⃣  ``get_python_files`` – directory traversal edge cases
# --------------------------------------------------------------------------- #

def test_get_python_files_finds_only_py(tmp_path: Path):
    """Only files with a ``.py`` suffix must be yielded."""
    (tmp_path / "good.py").write_text("print('ok')")
    (tmp_path / "bad.txt").write_text("print('no')")
    (tmp_path / ".hidden.py").write_text("print('hidden')")

    found = sorted(p.name for p in get_python_files(tmp_path))
    assert found == [".hidden.py", "good.py"], "Non‑python files were not filtered correctly"


def test_get_python_files_recurses_into_subfolders(tiny_project: Path):
    """Files in nested directories must be discovered."""
    found = {p.relative_to(tiny_project) for p in get_python_files(tiny_project)}
    expected = {
        Path("a.py"),
        Path("b.py"),
        Path("sub", "c.py"),
        Path("sub", "__init__.py"),
    }
    assert found == expected, "Recursive discovery failed"


def test_get_python_files_raises_for_nonexistent_path():
    """A clear ``FileNotFoundError`` should be raised for a missing root."""
    non_existing = Path("/this/does/not/exist")
    with pytest.raises(FileNotFoundError, match="does not exist"):
        list(get_python_files(non_existing))


def test_get_python_files_handles_permission_error(tmp_path: Path, monkeypatch):
    """When ``os.scandir`` raises ``PermissionError`` the generator should surface it."""
    # Create a folder that will raise PermissionError on scandir
    secret = tmp_path / "secret"
    secret.mkdir()
    monkeypatch.setattr(os, "scandir", mock.Mock(side_effect=PermissionError("no access")))
    with pytest.raises(PermissionError, match="no access"):
        list(get_python_files(secret))


# --------------------------------------------------------------------------- #
# 3️⃣  Integration – the public ``ComplexityAnalyzer`` class
# --------------------------------------------------------------------------- #

@pytest.fixture(scope="function")
def analyzer() -> ComplexityAnalyzer:
    """A fresh ``ComplexityAnalyzer`` instance for each test."""
    return ComplexityAnalyzer()


def test_analyzer_analyze_happy_path(analyzer: ComplexityAnalyzer, tiny_project: Path):
    """``analyze`` must return a ``ProjectSummary`` containing one entry per .py file."""
    summary: ProjectSummary = analyzer.analyze(tiny_project)

    # We expect four files (including the comment‑only __init__) – verify count first.
    assert len(summary.file_metrics) == 4, "Unexpected number of FileMetrics entries"

    # Build a lookup for easy assertions.
    lookup = {fm.path.name: fm for fm in summary.file_metrics}

    # a.py – 3 LOC, 2 CC
    expected_a = compute_maintainability_index(3, 2)
    assert_file_metrics(
        lookup["a.py"],
        path=(tiny_project / "a.py").resolve(),
        loc=3,
        cyclomatic_complexity=2,
        maintainability_index=expected_a,
    )

    # b.py – empty file, 0 LOC, 0 CC
    expected_b = compute_maintainability_index(0, 0)
    assert_file_metrics(
        lookup["b.py"],
        path=(tiny_project / "b.py").resolve(),
        loc=0,
        cyclomatic_complexity=0,
        maintainability_index=expected_b,
    )

    # __init__.py – comment only, 0 LOC, 0 CC
    expected_init = compute_maintainability_index(0, 0)
    assert_file_metrics(
        lookup["__init__.py"],
        path=(tiny_project / "sub" / "__init__.py").resolve(),
        loc=0,
        cyclomatic_complexity=0,
        maintainability_index=expected_init,
    )

    # c.py – 5 LOC (blank line ignored), 3 CC (for, try, if)
    expected_c = compute_maintainability_index(5, 3)
    assert_file_metrics(
        lookup["c.py"],
        path=(tiny_project / "sub" / "c.py").resolve(),
        loc=5,
        cyclomatic_complexity=3,
        maintainability_index=expected_c,
    )

    # The summary string representation should contain the project root path.
    assert str(tiny_project) in summary.report, "Report does not embed the root path"


def test_analyzer_input_validation(analyzer: ComplexityAnalyzer):
    """Invalid inputs should raise clear exceptions."""
    with pytest.raises(TypeError, match="Path-like"):
        analyzer.analyze(123)  # not a path

    with pytest.raises(ValueError, match="must be an existing directory"):
        analyzer.analyze(Path("/definitely/does/not/exist"))


def test_analyzer_uses_logging_correctly(analyzer: ComplexityAnalyzer, tiny_project: Path, caplog):
    """The analyzer logs start/finish messages – no regression of log level."""
    caplog.set_level("INFO")
    analyzer.analyze(tiny_project)

    start_msg = f"Starting analysis of {tiny_project}"
    finish_msg = f"Finished analysis of {tiny_project}"
    # The logger used inside the module is ``complexity_analyzer.logger``.
    assert any(start_msg in rec.message for rec in caplog.records), "Start message missing"
    assert any(finish_msg in rec.message for rec in caplog.records), "Finish message missing"


# --------------------------------------------------------------------------- #
# 4️⃣  Performance guard – analysing a bunch of tiny files should be fast
# --------------------------------------------------------------------------- #

def test_analyzer_performance_on_many_files(analyzer: ComplexityAnalyzer, tmp_path: Path):
    """Create 200 trivial .py files and ensure the whole pipeline finishes < 1 s."""
    N = 200
    for i in range(N):
        (tmp_path / f"mod_{i}.py").write_text("x = 1\n")  # 1 LOC, 0 complexity

    start = time.perf_counter()
    summary = analyzer.analyze(tmp_path)
    duration = time.perf_counter() - start

    assert len(summary.file_metrics) == N, "Not all files were processed"
    assert duration < 1.0, f"Analysis took too long ({duration:.3f}s) – expected < 1 s"


# --------------------------------------------------------------------------- #
# 5️⃣  Mock‑based unit test for error handling inside ``analyze_file``
# --------------------------------------------------------------------------- #

def test_analyze_file_propagates_io_error(tmp_path: Path):
    """If reading a file raises ``OSError`` the exception must bubble up."""
    bad_file = tmp_path / "bad.py"
    bad_file.touch()

    # Force ``Path.open`` to raise an OSError for this specific path.
    with mock.patch.object(Path, "open", side_effect=OSError("disk failure")):
        with pytest.raises(OSError, match="disk failure"):
            analyze_file(bad_file)


# --------------------------------------------------------------------------- #
# 6️⃣  Guard‑clause coverage – ensure early‑returns are exercised
# --------------------------------------------------------------------------- #

def test_compute_loc_early_return_on_nonexistent_file(tmp_path: Path):
    """If the file does not exist ``compute_loc`` should raise ``FileNotFoundError``."""
    missing = tmp_path / "does_not_exist.py"
    with pytest.raises(FileNotFoundError):
        compute_loc(missing)


def test_compute_cyclomatic_complexity_early_return_on_nonexistent_file(tmp_path: Path):
    """Same guard‑clause for cyclomatic complexity helper."""
    missing = tmp_path / "does_not_exist.py"
    with pytest.raises(FileNotFoundError):
        compute_cyclomatic_complexity(missing)


# --------------------------------------------------------------------------- #
# End of test suite
# --------------------------------------------------------------------------- #
```

### How to run the suite

```bash
# Install the test runner (only needed once)
pip install pytest

# Execute the tests
pytest -q tests/test_complexity_analyzer.py
```

The suite is **self‑contained** – it creates temporary files/directories on‑the‑fly,
uses only the public API of `complexity_analyzer.py`, and cleans up automatically
thanks to the `tmp_path` fixture.  It exercises happy paths, edge cases,
exception handling, input validation, integration between helpers and the
`ComplexityAnalyzer` class, and includes a lightweight performance guard.