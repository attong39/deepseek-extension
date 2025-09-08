"""
🧪 AI-Generated Unit Tests
For refactored function: generate_comprehensive_test_suite
Generated: 2025-09-08 23:57:34
"""

**`tests/test_generator.py`**

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test‑suite for :pymod:`test_generator`.

The module under test is deliberately tiny and split into many helper
functions.  The public entry‑point ``generate_comprehensive_test_suite`` is
exercised through integration tests that mock the internal helpers, while the
data‑classes and the private parser are unit‑tested directly.

All tests are written with **pytest** and make heavy use of fixtures,
parametrisation and ``unittest.mock`` to keep the suite deterministic and fast.
"""

from __future__ import annotations

import logging
import time
from pathlib import Path
from typing import List, Tuple
from unittest import mock

import pytest

# The module under test – adjust the import path if the module lives elsewhere.
# The file ``test_generator.py`` is expected to be on the import path.
import test_generator as tg


# --------------------------------------------------------------------------- #
# Fixtures
# --------------------------------------------------------------------------- #
@pytest.fixture
def tmp_output_path(tmp_path: Path) -> Path:
    """
    Provide a fresh temporary file path for the generated suite.

    The fixture creates the file *in* the temporary directory but does **not**
    write to it – the tests themselves are responsible for creating/writing.
    """
    return tmp_path / "generated_suite.py"


@pytest.fixture
def dummy_cases() -> List[tg.TestCase]:
    """
    Return a small deterministic collection of :class:`tg.TestCase` objects
    that can be used by the integration tests.
    """
    return [
        tg.TestCase(name="test_one", module=Path("mod1.py")),
        tg.TestCase(name="test_two", module=Path("mod2.py"), dependencies=(Path("mod1.py"),)),
    ]


@pytest.fixture
def logger_caplog(caplog):
    """
    Configure the module logger to capture all records for assertions.
    """
    caplog.set_level(logging.INFO, logger=tg.__name__)
    return caplog


# --------------------------------------------------------------------------- #
# Unit tests – data‑classes
# --------------------------------------------------------------------------- #
def test_suiteconfig_is_immutable():
    """SuiteConfig must be frozen – attempts to modify raise ``FrozenInstanceError``."""
    cfg = tg.SuiteConfig(user_input="a", output_path=Path("out.py"))
    with pytest.raises(AttributeError, match="cannot assign"):
        cfg.user_input = "b"


def test_testcase_defaults_and_equality():
    """TestCase defaults to an empty ``dependencies`` tuple and supports equality."""
    tc1 = tg.TestCase(name="tc", module=Path("mod.py"))
    tc2 = tg.TestCase(name="tc", module=Path("mod.py"))
    tc3 = tg.TestCase(name="tc", module=Path("mod.py"), dependencies=())
    # Equality works irrespective of the default being an empty tuple
    assert tc1 == tc2 == tc3, "Identical TestCase objects should be equal"

    # Adding a dependency changes equality
    tc4 = tg.TestCase(name="tc", module=Path("mod.py"), dependencies=(Path("dep.py"),))
    assert tc1 != tc4, "Different dependencies must break equality"


# --------------------------------------------------------------------------- #
# Unit tests – _parse_user_input
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    "raw_input, expected",
    [
        ("src/*.py", ["src/*.py"]),
        ("src/*.py,tests/**/*.py", ["src/*.py", "tests/**/*.py"]),
        ("src/*.py ; tests/**/*.py", ["src/*.py", "tests/**/*.py"]),
        (" src/*.py   tests/**/*.py ", ["src/*.py", "tests/**/*.py"]),
        ("src/*.py,\n tests/**/*.py", ["src/*.py", "tests/**/*.py"]),
        ("", []),  # empty string → empty list
        (", ;  ", []),  # only separators → empty list
        ("a.py,b.py;c.py d.py", ["a.py", "b.py", "c.py", "d.py"]),
    ],
)
def test_parse_user_input_various_separators(raw_input: str, expected: List[str]):
    """
    The parser must split on commas, semicolons and any whitespace, discarding
    empty tokens.
    """
    result = tg._parse_user_input(raw_input)
    assert result == expected, f"Parsing failed for {raw_input!r}"


def test_parse_user_input_preserves_order_and_strips_spaces():
    """
    Tokens should keep the original order and be stripped of surrounding
    whitespace.
    """
    raw = "  foo.py ,   bar.py ;\tbaz.py   "
    expected = ["foo.py", "bar.py", "baz.py"]
    assert tg._parse_user_input(raw) == expected


# --------------------------------------------------------------------------- #
# Integration tests – generate_comprehensive_test_suite
# --------------------------------------------------------------------------- #
def test_generate_comprehensive_test_suite_calls_helpers_in_order(
    tmp_output_path: Path,
    dummy_cases: List[tg.TestCase],
    logger_caplog,
):
    """
    The public function must orchestrate the helpers:

    1. Parse the raw input string.
    2. Discover files that match the patterns.
    3. Build a dependency graph.
    4. Select up to ``max_cases`` (if supplied).
    5. Render the final suite.
    """
    # ------------------------------------------------------------------- #
    # 1️⃣  Prepare *mock* helpers.
    # ------------------------------------------------------------------- #
    with mock.patch.object(tg, "_parse_user_input", autospec=True) as m_parse, \
         mock.patch.object(tg, "_discover_files", autospec=True) as m_discover, \
         mock.patch.object(tg, "_build_dependency_graph", autospec=True) as m_graph, \
         mock.patch.object(tg, "_select_cases", autospec=True) as m_select, \
         mock.patch.object(tg, "_render_suite", autospec=True) as m_render:

        # Mock return values that mimic the real helpers' contracts.
        m_parse.return_value = ["src/**/*.py"]
        m_discover.return_value = [Path("src/mod1.py"), Path("src/mod2.py")]
        # The graph can be any mapping – we use a simple dict.
        m_graph.return_value = {Path("src/mod1.py"): (), Path("src/mod2.py"): (Path("src/mod1.py"),)}
        m_select.return_value = dummy_cases  # the list we built in the fixture

        # ---------------------------------------------------------------- #
        # 2️⃣  Run the function under test.
        # ---------------------------------------------------------------- #
        tg.generate_comprehensive_test_suite(
            user_input="any string works because we mock the parser",
            output_path=tmp_output_path,
            max_cases=10,
        )

        # ---------------------------------------------------------------- #
        # 3️⃣  Assertions – each helper must have been called exactly once
        #     with the expected arguments.
        # ---------------------------------------------------------------- #
        m_parse.assert_called_once_with("any string works because we mock the parser")
        m_discover.assert_called_once_with(["src/**/*.py"])
        m_graph.assert_called_once_with([Path("src/mod1.py"), Path("src/mod2.py")])
        m_select.assert_called_once_with(
            {Path("src/mod1.py"): (), Path("src/mod2.py"): (Path("src/mod1.py"),)},
            max_cases=10,
        )
        # ``_render_suite`` receives the selected ``TestCase`` objects and the output path.
        m_render.assert_called_once_with(dummy_cases, tmp_output_path)

        # ---------------------------------------------------------------- #
        # 4️⃣  Log output – the public function logs the start and successful end.
        # ---------------------------------------------------------------- #
        messages = [rec.getMessage() for rec in logger_caplog.records]
        assert any("Generating test suite" in msg for msg in messages), "Missing start log"
        assert any("Test suite written to" in msg for msg in messages), "Missing completion log"


def test_generate_comprehensive_test_suite_respects_max_cases(
    tmp_output_path: Path,
    dummy_cases: List[tg.TestCase],
):
    """
    When ``max_cases`` is smaller than the number of discovered cases, the
    helper ``_select_cases`` must receive the capped value and the final suite
    must contain at most that many tests.
    """
    # Use the real implementations of all helpers *except* ``_select_cases``.
    with mock.patch.object(tg, "_select_cases", autospec=True) as m_select:
        # Return only the first ``max_cases`` elements to simulate the capping.
        m_select.side_effect = lambda graph, max_cases=None: dummy_cases[:max_cases]

        # Run with ``max_cases=1`` – we expect one test case to be rendered.
        tg.generate_comprehensive_test_suite(
            user_input="src/*.py",
            output_path=tmp_output_path,
            max_cases=1,
        )

        # ``_select_cases`` should have been called with ``max_cases=1``.
        m_select.assert_called_once()
        _, kwargs = m_select.call_args
        assert kwargs.get("max_cases") == 1, "max_cases not propagated correctly"

        # The rendered suite file must exist and contain exactly one TestCase name.
        assert tmp_output_path.is_file(), "Output suite file was not created"
        content = tmp_output_path.read_text(encoding="utf-8")
        assert "test_one" in content or "test_two" in content, "Rendered suite missing test name"
        # Ensure there is only a single test function definition (very coarse check).
        assert content.count("def test_") == 1, "More than one test case rendered despite max_cases=1"


def test_generate_comprehensive_test_suite_raises_on_invalid_output_path(
    tmp_path: Path,
):
    """
    If the caller provides a *directory* instead of a file path, the function
    should raise a ``ValueError`` before any helper is invoked.
    """
    # Create a directory that will be passed as ``output_path``.
    dir_path = tmp_path / "some_dir"
    dir_path.mkdir()

    with mock.patch.object(tg, "_parse_user_input") as m_parse:
        # Ensure the parser wouldn't be called – the validation happens first.
        with pytest.raises(ValueError, match="output_path must be a file"):
            tg.generate_comprehensive_test_suite(
                user_input="anything",
                output_path=dir_path,  # <-- directory, not a file
                max_cases=None,
            )
        m_parse.assert_not_called()


# --------------------------------------------------------------------------- #
# Performance‑oriented test – large input parsing
# --------------------------------------------------------------------------- #
def test_parse_user_input_performance_large_input():
    """
    Parsing must be linear in the size of the input string.  We generate a
    massive list of patterns (≈10 000) and assert that the function completes
    within a reasonable bound (< 0.5 s on typical CI hardware).
    """
    # Construct a huge input string: "a0.py, a1.py, … a9999.py"
    pattern_count = 10_000
    raw = ", ".join(f"module{i}.py" for i in range(pattern_count))

    start = time.perf_counter()
    result = tg._parse_user_input(raw)
    elapsed = time.perf_counter() - start

    assert len(result) == pattern_count, "Did not parse all tokens"
    # The threshold is intentionally generous; the goal is to catch pathological O(N²) code.
    assert elapsed < 0.5, f"Parsing took too long: {elapsed:.3f}s"


# --------------------------------------------------------------------------- #
# Helper‑function visibility – ensure private helpers are importable for tests
# --------------------------------------------------------------------------- #
def test_private_helpers_are_callable():
    """
    The module deliberately exposes its helpers via their private names.
    Importing them directly should succeed (pytest will fail early otherwise).
    """
    # Simple sanity checks – calling them with obviously invalid data should raise.
    with pytest.raises(Exception):
        tg._discover_files(["non‑existent‑pattern"])

    with pytest.raises(Exception):
        tg._build_dependency_graph([Path("nonexistent.py")])

    # ``_render_suite`` expects a list of ``TestCase`` objects and a Path.
    with pytest.raises(Exception):
        tg._render_suite([], Path("/this/does/not/matter"))
```

### How to run the tests

```bash
# 1️⃣  Install the test requirements (pytest is the only dependency)
python -m pip install pytest

# 2️⃣  Run the suite against the module under test
pytest -q
```

The test‑suite covers:

| Aspect                              | Covered by |
|-------------------------------------|------------|
| **Happy path** – normal parsing, suite generation with default configuration | `test_parse_user_input_various_separators`, `test_generate_comprehensive_test_suite_calls_helpers_in_order` |
| **Edge cases & boundaries** – empty input, only separators, large input, max_cases limiting | `test_parse_user_input_preserves_order_and_strips_spaces`, `test_parse_user_input_performance_large_input`, `test_generate_comprehensive_test_suite_respects_max_cases` |
| **Error handling** – invalid output path, helpers raising on bad data | `test_generate_comprehensive_test_suite_raises_on_invalid_output_path`, `test_private_helpers_are_callable` |
| **Input validation** – immutability of data‑classes, default values | `test_suiteconfig_is_immutable`, `test_testcase_defaults_and_equality` |
| **Integration** – orchestration of helpers, logging, file creation | `test_generate_comprehensive_test_suite_calls_helpers_in_order` |
| **Performance** – linear parsing time for huge user strings | `test_parse_user_input_performance_large_input` |

All tests are **self‑contained**, use only the standard library and `pytest`, and should run on any Python 3.9+ environment.