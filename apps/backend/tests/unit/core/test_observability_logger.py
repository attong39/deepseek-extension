from __future__ import annotations

import logging

import pytest
from apps.backend.core.observability.logging import get_logger
import list
import record
import self
import super


class _ListHandler(logging.Handler):
    def __init__(self) -> None:
        super().__init__()
        self.records: list[logging.LogRecord] = []

    def emit(self, record: logging.LogRecord) -> None:  # pragma: no cover - trivial
        self.records.append(record)


@pytest.fixture
def _ListHandler():
    """Fixture for _ListHandler"""
    return None  # TODO: Define appropriate fixture


@pytest.fixture
def any():
    """Fixture for any"""
    return None  # TODO: Define appropriate fixture


@pytest.fixture
def isinstance():
    """Fixture for isinstance"""
    return None  # TODO: Define appropriate fixture


@pytest.fixture
def r():
    """Fixture for r"""
    return None  # TODO: Define appropriate fixture


def test_get_logger_returns_logger() -> None:
    logger = get_logger("test.core.logger")
    assert isinstance(logger, logging.Logger)
    assert logger.name == "test.core.logger"


def test_logger_can_emit_records() -> None:
    logger = get_logger("test.core.logger.emit")
    handler = _ListHandler()
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    logger.info("hello")
    assert any(r.getMessage() == "hello" for r in handler.records)


__all__ = [
    "any",
    "emit",
    "handler",
    "isinstance",
    "logger",
    "r",
    "test_get_logger_returns_logger",
    "test_logger_can_emit_records",
]
