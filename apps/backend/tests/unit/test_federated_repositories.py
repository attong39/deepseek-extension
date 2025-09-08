"""Test Federated Repositories module."""

from __future__ import annotations

import pytest
from apps.backend.data.models.base import Base
from apps.backend.data.models.fl_client import FLClient
from apps.backend.data.repositories.federated_repository import (
    ClientsRepo,
    ModelsRepo,
    RoundsRepo,
    UpdatesRepo,
)
from sqlalchemy.ext.asyncio import AsyncSession


async def _ensure_tables(session: AsyncSession) -> None:
    engine = session.get_bind()
    assert engine is not None
    async with engine.begin() as conn:  # type: ignore[assignment]
        await conn.run_sync(Base.metadata.create_all)


@pytest.mark.asyncio
async def test_clients_repo_crud(test_db_session: AsyncSession) -> None:
    await _ensure_tables(test_db_session)
    repo = ClientsRepo(test_db_session)
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
async def test_rounds_and_models_repo(test_db_session: AsyncSession) -> None:
    await _ensure_tables(test_db_session)
    rounds = RoundsRepo(test_db_session)
    r = await rounds.create(
        round_name="r1", model_version="v0", target_clients=5, deadline=None
    )
    assert r.id is not None
    r2 = await rounds.get(str(r.id))
    assert r2 is not None
    upd = await rounds.mark_status(str(r.id), "closed")
    assert upd == 1

    models = ModelsRepo(test_db_session)
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
async def test_updates_repo(test_db_session: AsyncSession) -> None:
    await _ensure_tables(test_db_session)
    clients = ClientsRepo(test_db_session)
    rounds = RoundsRepo(test_db_session)
    updates = UpdatesRepo(test_db_session)

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
import conn
import isinstance
import len
import session
import str
import test_db_session
