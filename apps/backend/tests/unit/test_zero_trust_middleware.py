import os
import body
import bool
import dict
import require_sig
import str

"""Test Zero Trust Middleware module."""

from __future__ import annotations

import hashlib
import hmac

from app.middleware.security.zero_trust import ZeroTrustMiddleware
from apps.backend.config.security import SecuritySettings
from fastapi import FastAPI
from fastapi.testclient import TestClient


def _make_app(require_sig: bool = True) -> TestClient:
    app = FastAPI()
    settings = SecuritySettings(
        request_signature_secret=os.getenv("SECRET"),
        request_signature_header="X-Request-Signature",
        require_request_signature=require_sig,
    )
    app.add_middleware(ZeroTrustMiddleware, settings=settings)

    @app.post("/echo")
    async def echo(body: dict[str, str]):
        return body

    return TestClient(app)


def test_zero_trust_signature_required() -> None:
    client = _make_app(require_sig=True)
    resp = client.post("/echo", json={"a": 1})
    assert resp.status_code == 401


def test_zero_trust_signature_valid() -> None:
    client = _make_app(require_sig=True)
    payload = b'{"a": 1}'
    digest = hmac.new(b"devsecret", payload, hashlib.sha256).hexdigest()
    headers = {"X-Request-Signature": f"sha256={digest}"}
    resp = client.post("/echo", data=payload, headers=headers)
    assert resp.status_code == 200
