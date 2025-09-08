"""Test Federated Repositories module."""

from __future__ import annotations

from collections.abc import AsyncGenerator

import pytest
from apps.backend.data.models.base import Base
from apps.backend.data.models.fl_client import FLClient
from apps.backend.data.models.fl_model import FLModel
from apps.backend.data.models.fl_round import FLRound
from apps.backend.data.models.fl_update import FLUpdate
from apps.backend.data.repositories.federated_repository import (
    ClientsRepo,
    ModelsRepo,
    RoundsRepo,
    UpdatesRepo,
)
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool


@pytest.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
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
        try:
            yield session
        finally:
            await session.rollback()
    await engine.dispose()


@pytest.mark.asyncio
async def test_clients_repo_crud(db_session: AsyncSession) -> None:
    repo = ClientsRepo(db_session)
    c = await repo.register(
        client_id="c1", reg_token_hash="h123", capabilities={"cpu": "x86"}
    )
    assert isinstance(c, FLClient)
    got = await repo.get_by_client_id("c1")
    assert got is not None
    assert got.client_id == "c1"
    rows = await repo.touch_last_seen("c1")
    assert rows >= 0


@pytest.mark.asyncio
async def test_rounds_and_models_repo(db_session: AsyncSession) -> None:
    rounds = RoundsRepo(db_session)
    r = await rounds.create(
        round_name="r1", model_version="v0", target_clients=5, deadline=None
    )
    assert r.id is not None
    r2 = await rounds.get(str(r.id))
    assert r2 is not None
    upd = await rounds.mark_status(str(r.id), "closed")
    assert upd == 1

    models = ModelsRepo(db_session)
    m = await models.publish(
        version="v1",
        artifact_uri="file:///tmp/model.bin",
        sha256="deadbeef",
        metrics={"n": 1},
    )
    assert m.version == "v1"
    m2 = await models.get_by_version("v1")
    assert m2 is not None and m2.version == "v1"


@pytest.mark.asyncio
async def test_updates_repo(db_session: AsyncSession) -> None:
    clients = ClientsRepo(db_session)
    rounds = RoundsRepo(db_session)
    updates = UpdatesRepo(db_session)

    c = await clients.register(client_id="c2", reg_token_hash="h456", capabilities={})
    r = await rounds.create(
        round_name="r2", model_version="v0", target_clients=3, deadline=None
    )
    u = await updates.submit(
        round_id=str(r.id),
        client_pk=str(c.id),
        payload_uri="file:///tmp/u.npz",
        payload_sha256="beadfeed",
        sample_size=10,
        signature=None,
    )
    assert u.id is not None
    lst = await updates.list_by_round(str(r.id))
    assert len(lst) == 1
    cnt = await updates.count_by_round(str(r.id))
    assert cnt == 1
    changed = await updates.mark_accepted([str(u.id)])
    assert changed == 1
import async_session
import bind
import conn
import isinstance
import len
import list
import session
import str
import tables
