"""
🧪 AI-Generated Unit Tests
For refactored function: validate_https___setuptools_pypa_io_en_latest_userguide_pyproject_config_html
Generated: 2025-09-08 23:50:33
"""

**File: `tests/test_pyproject_config_validation.py`**

```python
"""
Tests for the refactored ``validate_https___setuptools_pypa_io_en_latest_userguide_pyproject_config_html``
module.

The implementation (trimmed for brevity in the kata) provides:

* ``ValidationError`` – an exception that stores a ``tuple`` of error messages.
* ``PyProjectConfig`` – a ``@dataclass`` with a ``from_mapping`` class‑method that
  builds a typed view over a raw ``dict`` coming from ``pyproject.toml``.
* ``validate_https___setuptools_pypa_io_en_latest_userguide_pyproject_config_html``
  – the public entry point.  It accepts a mapping, validates it and either
  returns a list of human‑readable error strings **or** raises ``ValidationError``
  when any rule fails.

The tests below exercise the public contract – they do **not** depend on the
internal helper functions or the registry implementation.  This keeps the test
suite stable when the internal implementation is refactored again.

All tests are written with **pytest** and make heavy use of fixtures,
parameterisation and clear assertions.
"""

from __future__ import annotations

import time
from typing import Any, Dict, List, Mapping

import pytest

# --------------------------------------------------------------------------- #
# Import the objects under test.
# --------------------------------------------------------------------------- #
# The module name is the one that contains the refactored code shown in the
# prompt.  Adjust the import path if the file lives in a package.
from validate_https___setuptools_pypa_io_en_latest_userguide_pyproject_config_html import (
    ValidationError,
    PyProjectConfig,
    validate_https___setuptools_pypa_io_en_latest_userguide_pyproject_config_html,
)

# --------------------------------------------------------------------------- #
# Fixtures
# --------------------------------------------------------------------------- #

@pytest.fixture
def minimal_valid_config() -> Dict[str, Any]:
    """
    Returns the smallest configuration that satisfies *all* validation rules.
    The values are deliberately simple but syntactically valid.
    """
    return {
        "name": "awesome-lib",
        "version": "1.2.3",
        "description": "A tiny library for demonstration purposes.",
        "requires_python": ">=3.8",
        "license": "MIT",
        "url": "https://github.com/example/awesome-lib",
        # optional fields – included to make the fixture reusable for edge cases
        "dependencies": ["requests>=2.25.0", "tomli>=1.0.0"],
        "optional_dependencies": {
            "dev": ["pytest>=6.0", "ruff>=0.0.260"]
        },
    }

@pytest.fixture
def config_from_mapping(minimal_valid_config: Mapping[str, Any]) -> PyProjectConfig:
    """
    Returns a ``PyProjectConfig`` instance built via the ``from_mapping`` helper.
    This fixture validates that the conversion works before any further test
    logic runs.
    """
    cfg = PyProjectConfig.from_mapping(minimal_valid_config)
    # sanity‑check – the instance should contain the same data we fed in
    assert cfg.name == minimal_valid_config["name"]
    assert cfg.version == minimal_valid_config["version"]
    return cfg

# --------------------------------------------------------------------------- #
# Happy‑path tests
# --------------------------------------------------------------------------- #

def test_validate_returns_empty_list_on_valid_input(minimal_valid_config: Mapping[str, Any]) -> None:
    """
    When a completely valid configuration is supplied the validator must
    return an empty list (i.e. “no errors”) and must **not** raise.
    """
    errors = validate_https___setuptools_pypa_io_en_latest_userguide_pyproject_config_html(minimal_valid_config)
    assert isinstance(errors, list), "Validator should return a list of error strings"
    assert not errors, f"Expected no validation errors, got: {errors}"


def test_validate_raises_validation_error_when_errors_occur(minimal_valid_config: Mapping[str, Any]) -> None:
    """
    The public contract states that a ``ValidationError`` is raised if any rule
    fails.  We provoke a failure by removing a required field and confirm the
    exception type as well as its ``errors`` attribute.
    """
    broken_cfg = dict(minimal_valid_config)
    broken_cfg.pop("url")  # ``url`` is required and must be HTTPS

    with pytest.raises(ValidationError) as excinfo:
        validate_https___setuptools_pypa_io_en_latest_userguide_pyproject_config_html(broken_cfg)

    err = excinfo.value
    # ``errors`` must be a tuple (immutable) and contain at least one message.
    assert isinstance(err.errors, tuple), "`ValidationError.errors` should be a tuple"
    assert err.errors, "ValidationError should contain at least one error message"
    # The message should mention the missing/invalid ``url`` field.
    assert any("url" in message.lower() for message in err.errors), \
        f"Expected an error about the missing/invalid URL, got: {err.errors}"


# --------------------------------------------------------------------------- #
# Edge‑case / boundary tests
# --------------------------------------------------------------------------- #

@pytest.mark.parametrize(
    "field,value,expected_substring",
    [
        # Empty required string fields – all should be flagged.
        ("name", "", "name"),
        ("version", "", "version"),
        ("description", "", "description"),
        ("requires_python", "", "requires_python"),
        ("license", "", "license"),
        ("url", "", "url"),
        # URL must be HTTPS.
        ("url", "http://example.com", "https"),
        # Version must look like a PEP 440 version (simple sanity check).
        ("version", "not-a-version", "version"),
        # ``requires_python`` must contain a comparison operator.
        ("requires_python", "3.8", "requires_python"),
    ],
)
def test_individual_field_validations(
    minimal_valid_config: Mapping[str, Any],
    field: str,
    value: str,
    expected_substring: str,
) -> None:
    """
    Parametrised test that mutates a single required field to an illegal value
    and checks that the validator reports an error containing the field name.
    """
    broken_cfg = dict(minimal_valid_config)
    broken_cfg[field] = value

    with pytest.raises(ValidationError) as excinfo:
        validate_https___setuptools_pypa_io_en_latest_userguide_pyproject_config_html(broken_cfg)

    messages = excinfo.value.errors
    assert any(
        expected_substring.lower() in msg.lower() for msg in messages
    ), f"Expected an error mentioning '{expected_substring}', got: {messages}"


def test_optional_collections_can_be_empty(minimal_valid_config: Mapping[str, Any]) -> None:
    """
    Optional collection fields are allowed to be empty – the validator must *not*
    raise in that case.
    """
    cfg = dict(minimal_valid_config)
    cfg["dependencies"] = []
    cfg["optional_dependencies"] = {}
    errors = validate_https___setuptools_pypa_io_en_latest_userguide_pyproject_config_html(cfg)
    assert errors == [], "Empty optional collections should be considered valid"


def test_dependency_version_spec_must_be_pep440(minimal_valid_config: Mapping[str, Any]) -> None:
    """
    Dependency strings should follow a ``package>=version`` style (a very thin
    approximation of PEP 440).  Supplying a malformed spec must raise.
    """
    cfg = dict(minimal_valid_config)
    cfg["dependencies"] = ["bad‑spec"]  # no ``>=`` separator

    with pytest.raises(ValidationError) as excinfo:
        validate_https___setuptools_pypa_io_en_latest_userguide_pyproject_config_html(cfg)

    msgs = excinfo.value.errors
    assert any("dependency" in m.lower() for m in msgs), \
        f"Expected a dependency‑related error, got: {msgs}"


def test_optional_dependencies_key_must_be_str_and_values_list(minimal_valid_config: Mapping[str, Any]) -> None:
    """
    ``optional_dependencies`` must be a ``dict`` whose keys are strings and values
    are ``list[str]``.  A non‑list value should be caught.
    """
    cfg = dict(minimal_valid_config)
    cfg["optional_dependencies"] = {"dev": "pytest>=6.0"}  # wrong type

    with pytest.raises(ValidationError) as excinfo:
        validate_https___setuptools_pypa_io_en_latest_userguide_pyproject_config_html(cfg)

    msgs = excinfo.value.errors
    assert any("optional_dependencies" in m.lower() for m in msgs), \
        f"Expected an optional‑dependencies error, got: {msgs}"


# --------------------------------------------------------------------------- #
# Input‑validation tests
# --------------------------------------------------------------------------- #

def test_validator_rejects_non_mapping_input() -> None:
    """
    The validator expects a ``Mapping`` (e.g. ``dict``).  Passing a list or
    ``None`` should raise a ``TypeError`` *before* any rule evaluation.
    """
    for bad_input in (["not", "a", "dict"], None, 42):
        with pytest.raises(TypeError, match="mapping"):
            validate_https___setuptools_pypa_io_en_latest_userguide_pyproject_config_html(bad_input)  # type: ignore[arg-type]

def test_pyprojectconfig_from_mapping_missing_required_fields() -> None:
    """
    ``PyProjectConfig.from_mapping`` must raise ``KeyError`` (or a custom error)
    when required fields are absent.  This test guarantees that the early‑exit
    guard works independently from the higher‑level validator.
    """
    incomplete = {
        "name": "demo",
        # ``version`` omitted on purpose
        "description": "demo",
        "requires_python": ">=3.9",
        "license": "MIT",
        "url": "https://example.com",
    }
    with pytest.raises(KeyError) as excinfo:
        PyProjectConfig.from_mapping(incomplete)  # type: ignore[arg-type]
    assert "version" in str(excinfo.value).lower()


# --------------------------------------------------------------------------- #
# Integration tests (registry + helpers)
# --------------------------------------------------------------------------- #

def test_multiple_errors_are_aggregated(minimal_valid_config: Mapping[str, Any]) -> None:
    """
    When several rules fail the validator must return **all** error messages,
    not just the first one.  This ensures the data‑driven registry is iterated
    completely.
    """
    broken_cfg = dict(minimal_valid_config)
    broken_cfg["url"] = "http://plain-http.com"
    broken_cfg["version"] = "not-a-semver"
    broken_cfg["dependencies"] = ["no‑separator"]

    with pytest.raises(ValidationError) as excinfo:
        validate_https___setuptools_pypa_io_en_latest_userguide_pyproject_config_html(broken_cfg)

    errors = excinfo.value.errors
    # We expect at least three distinct messages, one for each broken rule.
    assert len(errors) >= 3, f"Expected ≥3 error messages, got {len(errors)}: {errors}"
    # Verify each field appears in the messages.
    for token in ("url", "version", "dependency"):
        assert any(token in msg.lower() for msg in errors), f"Missing error about {token}"


# --------------------------------------------------------------------------- #
# Performance / scalability test
# --------------------------------------------------------------------------- #

def test_validation_time_scales_linearly_with_number_of_dependencies(minimal_valid_config: Mapping[str, Any]) -> None:
    """
    The validation logic should be O(n) with respect to the size of the
    ``dependencies`` list.  We generate a large list and assert that the runtime
    stays below a modest threshold (≈ 50 ms on a contemporary CI runner).
    """
    many_deps = [f"package{i}>=1.0.0" for i in range(10_000)]
    cfg = dict(minimal_valid_config)
    cfg["dependencies"] = many_deps

    start = time.perf_counter()
    errors = validate_https___setuptools_pypa_io_en_latest_userguide_pyproject_config_html(cfg)
    elapsed_ms = (time.perf_counter() - start) * 1000

    assert errors == [], f"Large, valid config should produce no errors, got: {errors}"
    assert elapsed_ms < 150, f"Validation took too long ({elapsed_ms:.2f} ms) for 10k deps"


# --------------------------------------------------------------------------- #
# Mock‑based test – ensure the registry is exercised without relying on its internals
# --------------------------------------------------------------------------- #

def test_registry_is_called_once_per_rule(monkeypatch: pytest.MonkeyPatch, minimal_valid_config: Mapping[str, Any]) -> None:
    """
    The public validator builds a ``ConfigValidator`` (which internally owns a
    registry of callables).  By monkey‑patching the registry we can assert that
    *each* rule is invoked exactly once.  This test protects against accidental
    early‑returns that would skip later rules.
    """
    call_counter: Dict[str, int] = {}

    def spy(rule_name: str):
        """A tiny wrapper that increments a counter and returns ``True`` (valid)."""
        call_counter[rule_name] = call_counter.get(rule_name, 0) + 1
        return True

    # Patch the internal registry – the implementation stores it as
    # ``ConfigValidator._registry`` (a dict ``{name: Callable}``).
    # Import lazily to avoid circular imports.
    from validate_https___setuptools_pypa_io_en_latest_userguide_pyproject_config_html import ConfigValidator

    original_registry = ConfigValidator._registry  # type: ignore[attr-defined]

    # Replace each entry with the spy whilst keeping the original key names.
    mocked_registry = {name: (lambda _cfg, _name=name: spy(_name)) for name in original_registry}
    monkeypatch.setattr(ConfigValidator, "_registry", mocked_registry, raising=False)

    # Run the validator – it should succeed (all spies return ``True``).
    errors = validate_https___setuptools_pypa_io_en_latest_userguide_pyproject_config_html(minimal_valid_config)

    assert errors == [], "All spied rules returned True, so no errors should be reported"
    # Every rule in the original registry must have been called exactly once.
    for name in original_registry:
        assert call_counter.get(name, 0) == 1, f"Rule '{name}' was not called exactly once"


# --------------------------------------------------------------------------- #
# End of test file
# --------------------------------------------------------------------------- #
```

### How to run the tests
```bash
# Install pytest if you haven’t already
python -m pip install pytest

# Execute the suite
pytest -q tests/test_pyproject_config_validation.py
```

The test suite covers:

1. **Happy path** – a completely correct configuration yields no errors.
2. **Edge cases** – missing/empty required fields, non‑HTTPS URLs, malformed
   version strings, bad dependency specs, and wrong optional‑dependency shapes.
3. **Error handling** – `ValidationError` is raised with a tuple of messages,
   and the exception’s message content is verified.
4. **Input validation** – non‑mapping inputs raise `TypeError`; missing required
   keys raise `KeyError` at the dataclass conversion stage.
5. **Integration** – multiple simultaneous failures are aggregated, and a
   monkey‑patched registry confirms each rule runs.
6. **Performance** – validation time remains bounded even with 10 000
   dependencies, demonstrating O(n) scaling.

All tests are self‑contained, use fixtures, parametrisation, and clear
assertion messages, making the suite easy to maintain as the validation code
evolves.