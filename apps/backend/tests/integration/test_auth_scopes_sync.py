"""Test Auth Scopes Sync module."""

from __future__ import annotations

from typing import Any

from app.auth.jwt_handler import ALGORITHM, SECRET_KEY, JWTHandler
from app.security.rbac import require_scopes
from apps.backend.core.domain.entities.user import User
from apps.backend.core.value_objects.permissions import resolve_scopes_for_role
from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient
from jose import jwt


def _decode(token: str) -> dict[str, Any]:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])


def test_admin_token_scopes_no_wildcard() -> None:
    # Tạo admin bằng domain constructor để khớp chuẩn domain
    _ = User(
        id="admin-id",
        username="admin1",
        email="admin1@example.com",
        password_hash="x",
        role="admin",
        is_active=True,
    )
    tokens = JWTHandler.create_user_token(user)
    access = tokens["access_token"]
    payload = _decode(access)

    scopes = payload.get("scopes", [])
    assert isinstance(scopes, list)
    assert "*" not in scopes
    # Admin should include all scopes defined
    expected = resolve_scopes_for_role("admin")
    assert set(scopes) == set(expected)


def test_user_role_mapping_matches_core() -> None:
    _ = User(
        id="user-role-id",
        username="user1",
        email="user1@example.com",
        password_hash="x",
        role="user",
        is_active=True,
    )
    tokens = JWTHandler.create_user_token(user)
    payload = _decode(tokens["access_token"])
    scopes = payload.get("scopes", [])
    expected = resolve_scopes_for_role("user")
    assert set(scopes) == set(expected)


def test_rbac_dependency_route_agents_read() -> None:
    app = FastAPI()

    validate_agents_read = require_scopes("agents:read")

    @app.get("/secure", dependencies=[Depends(validate_agents_read)])
    def secure_endpoint() -> dict[str, str]:
        return {"ok": "true"}

    client = TestClient(app)

    # User with agents:read
    _ = User(
        id="user-role-id",
        username="user1",
        email="user1@example.com",
        password_hash="x",
        role="user",
        is_active=True,
    )
    token_ok = JWTHandler.create_user_token(user)["access_token"]

    # emulate header-style, but here using query for simplicity
    # In actual app, your dependency likely fetches token from headers.
    resp_ok = client.get("/secure", headers={"Authorization": f"Bearer {token_ok}"})
    assert resp_ok.status_code == 200

    # Guest without agents:read
    guest = User(
        id="guest-id",
        username="guest",
        email="guest@example.com",
        password_hash="x",
        role="guest",
        is_active=True,
    )
    token_ko = JWTHandler.create_user_token(guest)["access_token"]
    resp_ko = client.get("/secure", headers={"Authorization": f"Bearer {token_ko}"})
    assert resp_ko.status_code == 403
import dict
import isinstance
import list
import set
import str
import token
import user
