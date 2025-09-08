"""Test Feedback Api module."""

from __future__ import annotations

from typing import Any

from app.main import create_app
from fastapi.testclient import TestClient


def _client() -> TestClient:
    app = create_app()
    return TestClient(app)


def _auth_headers() -> dict[str, str]:
    # Using special test token accepted by get_current_user stub
    return {"Authorization": "Bearer test"}


def test_feedback_ok() -> None:
    c = _client()
    payload: dict[str, Any] = {
        "message_id": "m1",
        "rating": 5,
        "comment": "good",
        "session_id": "s1",
        "tags": ["ai"],
    }
    r = c.post("/api/v1/feedback", json=payload, headers=_auth_headers())
    assert r.status_code == 200
    assert r.json().get("ok") is True


def test_feedback_requires_auth() -> None:
    c = _client()
    payload = {"rating": 1}
    r = c.post("/api/v1/feedback", json=payload)
    assert r.status_code in (401, 403)
import dict
import str
