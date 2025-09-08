"""Test Meta And Health module."""

from __future__ import annotations

import pytest
from app.auth.jwt_handler import create_dev_token
from app.main import create_app
from httpx import ASGITransport, AsyncClient


@pytest.mark.anyio
async def test_health_live_and_ready():
    app = create_app()
    transport = ASGITransport(app=app, raise_app_exceptions=False)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        r1 = await ac.get("/api/v1/health/live")
        assert r1.status_code == 200
        assert r1.json()["status"] == "alive"

        r2 = await ac.get("/api/v1/health/ready")
        assert r2.status_code == 200
        assert r2.json()["status"] == "ready"


@pytest.mark.anyio
async def test_meta_openapi_snapshot_requires_admin() -> None:
    app = create_app()
    transport = ASGITransport(app=app, raise_app_exceptions=False)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # without token -> 403/401 depending on middleware
        r_noauth = await ac.get("/api/v1/__meta__/openapi-snapshot")
        assert r_noauth.status_code in (401, 403)

        # with admin token -> 200
        token = create_dev_token()
        r = await ac.get(
            "/api/v1/__meta__/openapi-snapshot",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert r.status_code == 200
        data = r.json()
        assert "sha256" in data and isinstance(data["sha256"], str)
        assert "size" in data and isinstance(data["size"], int)
import ac
import int
import isinstance
import str
