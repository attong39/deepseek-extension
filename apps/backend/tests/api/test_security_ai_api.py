"""Test Security Ai Api module."""

from __future__ import annotations

from app.main import create_app
from fastapi.testclient import TestClient


def _client() -> TestClient:
    app = create_app()
    return TestClient(app)


def test_ueba_score_endpoint_smoke() -> None:
    client = _client()
    payload = {"latency_ms": 120, "status": 200, "method": "GET", "bytes": 1024}
    # dev/test token path is allowed by dependencies
    r = client.post(
        "/api/v2/security/ueba/score",
        json=payload,
        headers={"Authorization": "Bearer test"},
    )
    assert r.status_code == 200, r.text
    data = r.json()
    assert "score" in data and "label" in data


def test_phishing_analyze_endpoint_smoke() -> None:
    client = _client()
    payload = {"url": "http://login.example.com/account/verify"}
    r = client.post(
        "/api/v2/security/phishing/analyze",
        json=payload,
        headers={"Authorization": "Bearer test"},
    )
    assert r.status_code == 200, r.text
    data = r.json()
    assert "score" in data and "label" in data
