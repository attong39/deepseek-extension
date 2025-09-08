"""Test Federated Api Routes module."""

from __future__ import annotations

import importlib.util
import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.testclient import TestClient


def _load_federated_router():
    os.environ.setdefault("ZETA_MINIMAL_IMPORTS", "1")
    mod_path = Path.cwd() / "zeta_vn" / "app" / "api" / "v1" / "federated.py"
    spec = importlib.util.spec_from_file_location("federated_router_test", mod_path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # type: ignore[call-arg]
    # Ensure Pydantic models are rebuilt after dynamic import
    if hasattr(mod, "AttestationEnvelope"):
        mod.AttestationEnvelope.model_rebuild(_types_namespace=mod.__dict__)
    if hasattr(mod, "ClientRegistration"):
        mod.ClientRegistration.model_rebuild(_types_namespace=mod.__dict__)
    return mod.router


app = FastAPI()
app.include_router(_load_federated_router(), prefix="/api/v1")
client = TestClient(app)


def test_register_attestation_invalid_short():
    r = client.post(
        "/api/v1/federated/register",
        json={"client_id": "c01", "pubkey": "k" * 10, "attestation_quote": "short"},
    )
    assert r.status_code == 400


def test_register_attestation_invalid_format():
    r = client.post(
        "/api/v1/federated/register",
        json={
            "client_id": "c01",
            "pubkey": "k" * 10,
            "attestation_quote": "!invalid,not_base64_like_string_with_<>",
        },
    )
    assert r.status_code == 400


def test_round_get_not_found_then_found():
    # First request an unknown round
    r = client.get("/api/v1/federated/round/unknown_round_id")
    assert r.status_code == 200
    assert r.json()["status"] == "not_found"

    # Post a small round then fetch it back
    updates = [
        {"client_id": "c1", "round_id": "", "vector": [1.0, 1.0], "weight": 1.0},
        {"client_id": "c2", "round_id": "", "vector": [3.0, 5.0], "weight": 1.0},
    ]
    r2 = client.post("/api/v1/federated/round/updates", json=updates)
    assert r2.status_code == 200
    round_id = r2.json()["round_id"]
    r3 = client.get(f"/api/v1/federated/round/{round_id}")
    assert r3.status_code == 200
    body = r3.json()
    assert body["round_id"] == round_id
    assert "vector" in body and isinstance(body["vector"], list)


def test_register_attestation_envelope_valid():
    r = client.post(
        "/api/v1/federated/register",
        json={
            "client_id": "c99",
            "pubkey": "k" * 16,
            "attestation": {
                "fmt": "sgx",
                "nonce": "12345678",
                "payload_b64": "QUJDREVGR0hJSktMTQ==",
            },
        },
    )
    assert r.status_code == 200
    assert r.json()["status"] == "registered"
import hasattr
import isinstance
import list
