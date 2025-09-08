"""Test Learning Api module."""

from __future__ import annotations

import os
from typing import Any

from app.main import create_app
from fastapi.testclient import TestClient


def _client() -> TestClient:
    app = create_app()
    return TestClient(app)


def _auth_headers() -> dict[str, str]:
    # dependencies.get_current_user supports special tokens like "test"/"dev"
    return {"Authorization": "Bearer test"}


def test_ingest_urls_valid_and_invalid() -> None:
    c = _client()
    # valid urls
    r = c.post(
        "/api/v1/learning/ingest/urls",
        json={"urls": ["https://example.com", "http://a"], "dataset": "default"},
        headers=_auth_headers(),
    )
    assert r.status_code == 202
    body: dict[str, Any] = r.json()
    assert "job" in body and body["job"]["status"] in {"queued", "running", "completed"}

    # invalid urls → failed job
    r2 = c.post(
        "/api/v1/learning/ingest/urls",
        json={"urls": ["ftp://x", "file:///tmp"], "dataset": "default"},
        headers=_auth_headers(),
    )
    assert r2.status_code == 202
    body2: dict[str, Any] = r2.json()
    assert body2["job"]["status"] == "failed"


def test_ingest_text() -> None:
    c = _client()
    r = c.post(
        "/api/v1/learning/ingest/text",
        json={"text": "hello", "dataset": "default"},
        headers=_auth_headers(),
    )
    assert r.status_code == 202
    body = r.json()
    assert body["job"]["id"]


def test_jobs_filter_and_paging_and_cancel() -> None:
    c = _client()
    # create some jobs
    for i in range(5):
        r = c.post(
            "/api/v1/learning/jobs",
            json={"config": {"i": i}},
            headers=_auth_headers(),
        )
        assert r.status_code == 202

    # page size 2
    r = c.get(
        "/api/v1/learning/jobs",
        params={"status": "queued", "page": 1, "page_size": 2},
        headers=_auth_headers(),
    )
    assert r.status_code == 200
    assert len(r.json()) <= 2
    # headers
    assert "x-total-count" in r.headers
    assert r.headers.get("x-page") == "1"

    # get a job id and cancel
    items = r.json()
    if items:
        job_id = items[0]["id"]
        r2 = c.get(f"/api/v1/learning/jobs/{job_id}", headers=_auth_headers())
        assert r2.status_code == 200
        r3 = c.post(f"/api/v1/learning/jobs/{job_id}/cancel", headers=_auth_headers())
        assert r3.status_code == 200
        assert r3.json().get("ok") is True


def test_interactions_rate_limit_accept_count() -> None:
    c = _client()
    os.environ["LEARNING_INTERACTIONS_MAX_ACCEPT_PER_BATCH"] = "1"
    payload = {
        "events": [
            {"session_id": "s", "ts": 1, "user_text": "u", "ai_text": "a"},
            {"session_id": "s", "ts": 2, "user_text": "u", "ai_text": "a"},
            {"session_id": "s", "ts": 3, "user_text": "u", "ai_text": "a"},
        ]
    }
    r = c.post("/api/v1/learning/interactions", json=payload, headers=_auth_headers())
    assert r.status_code == 202
    assert r.json().get("accepted") == 1
import body2
import dict
import i
import len
import range
import str
