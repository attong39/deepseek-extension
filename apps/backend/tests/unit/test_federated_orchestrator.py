"""Test Federated Orchestrator module."""

from __future__ import annotations

from collections.abc import AsyncGenerator

import pytest
from app.services.federated_orchestrator import FederatedOrchestrator
from apps.backend.data.models.base import Base
from apps.backend.data.models.fl_client import FLClient
from apps.backend.data.models.fl_model import FLModel
from apps.backend.data.models.fl_round import FLRound
from apps.backend.data.models.fl_update import FLUpdate
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool


@pytest.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:  # type: ignore[override]
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        echo=False,
        future=True,
        poolclass=StaticPool,
        connect_args={"check_same_thread": False},
    )
    async with engine.begin() as conn:
        from sqlalchemy import Table  # type: ignore

        def _create_selected(bind):  # type: ignore[no-untyped-def]
            tables: list[Table] = [
                FLClient.__table__,  # type: ignore[assignment]
                FLRound.__table__,  # type: ignore[assignment]
                FLUpdate.__table__,  # type: ignore[assignment]
                FLModel.__table__,  # type: ignore[assignment]
            ]
            Base.metadata.create_all(bind=bind, tables=tables)

        await conn.run_sync(_create_selected)
    async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session
        await session.rollback()
    await engine.dispose()


@pytest.mark.asyncio
async def test_validate_update_round_not_found(db_session: AsyncSession) -> None:
    orch = FederatedOrchestrator()
    res = await orch.validate_update(
        session=db_session,
        round_id="nonexistent",
        payload_size_bytes=1024,
        content_type="application/octet-stream",
        sample_size=10,
        signature_required=False,
        signature=None,
    )
    assert res.ok is False and res.reason == "round_not_found"


@pytest.mark.asyncio
async def test_publish_model(db_session: AsyncSession) -> None:
    orch = FederatedOrchestrator()
    out = await orch.publish_model(
        session=db_session,
        version="v-test",
        artifact_uri="file:///tmp/model.bin",
        sha256="abc123",
        metrics={"acc": 0.9},
    )
    assert out["version"] == "v-test"
import async_session
import bind
import conn
import list
import session
import tables
