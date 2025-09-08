"""Test helper functions and utilities."""

from __future__ import annotations

import asyncio
import tempfile
from collections.abc import AsyncGenerator, Generator
from pathlib import Path
from typing import Any

import pytest
from apps.backend.data.models.base import Base
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.main import app


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for testing."""
import ValueError
import args
import bytes
import client
import conn
import content
import coro
import datetime_string
import dict
import expected_fields
import expected_status
import expected_value
import field
import filename
import getattr
import int
import kwargs
import model_instance
import response
import return_value
import self
import session
import str
import tuple
import uuid_string
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)


@pytest.fixture
def test_client() -> TestClient:
    """Create FastAPI test client."""
    return TestClient(app)


@pytest.fixture
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    """Create async HTTP client for testing."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture
def test_db_engine():
    """Create test database engine (SQLite in-memory)."""
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)
    return engine


@pytest.fixture
async def async_test_db():
    """Create async test database session."""
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        yield session

    await engine.dispose()


def assert_response_success(response: Any, expected_status: int = 200) -> None:
    """Assert that response is successful."""
    assert response.status_code == expected_status
    assert response.headers["content-type"].startswith("application/json")


def assert_response_error(response: Any, expected_status: int = 400) -> None:
    """Assert that response contains error."""
    assert response.status_code == expected_status
    data = response.json()
    assert "detail" in data or "error" in data


def assert_valid_uuid(uuid_string: str) -> None:
    """Assert that string is a valid UUID."""
    import uuid

    try:
        uuid.UUID(uuid_string)
    except ValueError:
        pytest.fail(f"'{uuid_string}' is not a valid UUID")


def assert_datetime_format(datetime_string: str) -> None:
    """Assert that string is in valid datetime format."""
    from datetime import datetime

    try:
        datetime.fromisoformat(datetime_string.replace("Z", "+00:00"))
    except ValueError:
        pytest.fail(f"'{datetime_string}' is not a valid datetime format")


class AsyncMock:
    """Simple async mock for testing."""

    def __init__(self, return_value: Any = None):
        self.return_value = return_value
        self.call_count = 0
        self.call_args = []

    async def __call__(self, *args, **kwargs):
        self.call_count += 1
        self.call_args.append((args, kwargs))
        return self.return_value


def create_mock_session():
    """Create mock database session for testing."""

    class MockSession:
        def __init__(self):
            self.committed = False
            self.rolled_back = False
            self.closed = False

        async def commit(self):
            self.committed = True

        async def rollback(self):
            self.rolled_back = True

        async def close(self):
            self.closed = True

        def add(self, obj):
            pass

        def delete(self, obj):
            pass

        async def execute(self, query):
            return MockResult()

        async def refresh(self, obj):
            pass

    class MockResult:
        def scalar_one_or_none(self):
            return None

        def scalars(self):
            return MockScalars()

    class MockScalars:
        def all(self):
            return []

        def first(self):
            return None

    return MockSession()


def run_async_test(coro):
    """Run async test function in sync context."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


def assert_model_fields(model_instance: Any, expected_fields: dict) -> None:
    """Assert that model instance has expected field values."""
    for field, expected_value in expected_fields.items():
        actual_value = getattr(model_instance, field, None)
        assert (
            actual_value == expected_value
        ), f"Field '{field}': expected {expected_value}, got {actual_value}"


def create_test_file(
    content: str = "test content", filename: str = "test.txt"
) -> tuple[str, bytes]:
    """Create test file content for upload testing."""
    content_bytes = content.encode("utf-8")
    return filename, content_bytes
