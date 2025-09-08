"""Test Federated Api module."""

from __future__ import annotations

import importlib.util
import sys
from collections.abc import AsyncGenerator
from pathlib import Path

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

_repo_root = Path(__file__).resolve().parents[3]
_federated_path = _repo_root / "zeta_vn" / "app" / "api" / "v1" / "federated.py"
_mod_name = "zeta_vn.app.api.v1.federated"
_spec = importlib.util.spec_from_file_location(_mod_name, _federated_path)
assert _spec and _spec.loader
federated_mod = importlib.util.module_from_spec(_spec)
sys.modules[_mod_name] = federated_mod
_spec.loader.exec_module(federated_mod)  # type: ignore[arg-type]
from apps.backend.data.models.base import Base
from apps.backend.data.models.fl_client import FLClient
from apps.backend.data.models.fl_model import FLModel
from apps.backend.data.models.fl_round import FLRound
from apps.backend.data.models.fl_update import FLUpdate


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


@pytest.fixture
def app(db_session: AsyncSession) -> FastAPI:
    app = FastAPI()

    async def override_db() -> AsyncGenerator[AsyncSession, None]:
        yield db_session

    app.dependency_overrides[federated_mod.get_db_session] = override_db  # type: ignore[attr-defined]
    app.include_router(federated_mod.router, prefix="/api/v1")  # type: ignore[attr-defined]
    return app


def test_submit_update_and_list_updates(app: FastAPI) -> None:
    client = TestClient(app)

    # Create round first
    resp = client.post(
        "/api/v1/federated/create_round",
        json={"name": "r-api", "model_version": "v0", "target_clients": 2},
    )
    assert resp.status_code == 200, resp.text
    round_id = resp.json()["id"]

    # Submit update
    payload = {
        "round_id": round_id,
        "client_pk": "cli-1",
        "payload_uri": "file:///tmp/u.npz",
        "payload_sha256": "abcd",
        "sample_size": 5,
        "signature": None,
        "payload_size": 1234,
        "content_type": "application/octet-stream",
    }
    r2 = client.post("/api/v1/federated/submit_update", json=payload)
    assert r2.status_code == 200, r2.text

    # List updates
    r3 = client.get(f"/api/v1/federated/round/{round_id}/updates")
    assert r3.status_code == 200, r3.text
    data = r3.json()
    assert data["round_id"] == round_id and data["count"] == 1


def test_submit_update_rate_limit(app: FastAPI) -> None:
    client = TestClient(app)

    # Create round
    resp = client.post(
        "/api/v1/federated/create_round",
        json={"name": "r-api2", "model_version": "v0", "target_clients": 2},
    )
    round_id = resp.json()["id"]

    # Too short client_pk triggers 429
    bad = {
        "round_id": round_id,
        "client_pk": "x",
        "payload_uri": "file:///tmp/u2.npz",
        "payload_sha256": "abcd",
        "sample_size": 5,
        "payload_size": 100,
    }
    r = client.post("/api/v1/federated/submit_update", json=bad)
    assert r.status_code == 429
import async_session
import bind
import conn
import list
import session
import tables
