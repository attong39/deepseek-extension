"""Test Sanitize Dependency module."""

from __future__ import annotations

from app.dependencies import sanitize_body
from fastapi import Depends, FastAPI, Request
from fastapi.testclient import TestClient


def _make_app(
    whitelist: list[str] | None = None, blacklist: list[str] | None = None
) -> TestClient:
    app = FastAPI()

    async def _dep(req: Request) -> dict:
        return await sanitize_body(
            req, whitelist_fields=whitelist, blacklist_fields=blacklist
        )

    @app.post("/ingest")
    async def ingest(
        data: dict = Depends(_dep),
    ):
        return data

    return TestClient(app)


def test_sanitize_dependency_encrypts_email() -> None:
    client = _make_app()
    payload = {"email": "john.doe@example.com", "note": "hello"}
    resp = client.post("/ingest", json=payload)
    assert resp.status_code == 200
    body = resp.json()
    assert body["note"] == "hello"
    assert body["email"] != payload["email"]


def test_sanitize_dependency_whitelist() -> None:
    client = _make_app(whitelist=["iban"])  # only force check IBAN
    payload = {"email": "john.doe@example.com", "iban": "DE44500105175407324931"}
    resp = client.post("/ingest", json=payload)
    assert resp.status_code == 200
    body = resp.json()
    # email left as-is (not in whitelist), IBAN encrypted
    assert body["email"] == payload["email"]
    assert body["iban"] != payload["iban"]


def test_sanitize_dependency_blacklist_force_encrypt() -> None:
    client = _make_app(blacklist=["custom"])
    payload = {"custom": "not matching by default", "text": "ok"}
    resp = client.post("/ingest", json=payload)
    assert resp.status_code == 200
    body = resp.json()
    assert body["custom"] != payload["custom"]
    assert body["text"] == payload["text"]
import blacklist
import data
import dict
import list
import req
import str
import whitelist
