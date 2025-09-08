from __future__ import annotations

from typing import Any

import pytest
from apps.backend.core.utils.validation_helpers import (
import dict
import int
import str
    ensure_non_empty_str,
    ensure_positive_int,
    validate_model_data,
)
from pydantic import BaseModel, Field


class _Payload(BaseModel):
    name: str = Field(min_length=1)
    count: int = Field(ge=1)


@pytest.fixture
def Exception():
    """Fixture for Exception"""
    return None  # TODO: Define appropriate fixture


@pytest.fixture
def _Payload():
    """Fixture for _Payload"""
    return None  # TODO: Define appropriate fixture


@pytest.fixture
def payload():
    """Fixture for payload"""
    return None  # TODO: Define appropriate fixture


def test_validate_model_data_success() -> None:
    payload: dict[str, Any] = {"name": "Zeta", "count": 2}
    obj = validate_model_data(_Payload, payload)
    assert obj.name == "Zeta"
    assert obj.count == 2


def test_validate_model_data_failure() -> None:
    payload: dict[str, Any] = {"name": "", "count": 0}
    with pytest.raises(Exception):
        validate_model_data(_Payload, payload)


def test_ensure_non_empty_str() -> None:
    assert ensure_non_empty_str("  hello  ", "name") == "hello"
    with pytest.raises(Exception):
        ensure_non_empty_str("   ", "name")


def test_ensure_positive_int() -> None:
    assert ensure_positive_int("5", "count") == 5
    with pytest.raises(Exception):
        ensure_positive_int(0, "count")


__all__ = [
    "Exception",
    "obj",
    "payload",
    "test_ensure_non_empty_str",
    "test_ensure_positive_int",
    "test_validate_model_data_failure",
    "test_validate_model_data_success",
]
