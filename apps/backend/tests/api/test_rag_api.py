"""Test Rag Api module."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

from fastapi import FastAPI
from fastapi.testclient import TestClient

_repo_root = Path(__file__).resolve().parents[3]
_rag_path = _repo_root / "zeta_vn" / "app" / "api" / "v1" / "rag.py"
_mod_name = "zeta_vn.app.api.v1.rag"
_spec = importlib.util.spec_from_file_location(_mod_name, _rag_path)
assert _spec and _spec.loader
rag_mod = importlib.util.module_from_spec(_spec)
sys.modules[_mod_name] = rag_mod
_spec.loader.exec_module(rag_mod)  # type: ignore[arg-type]


def test_rag_ingest_and_search() -> None:
    app = FastAPI()
    app.include_router(rag_mod.router, prefix="/api/v1")  # type: ignore[attr-defined]
    client = TestClient(app)

    r = client.post(
        "/api/v1/rag/ingest",
        json={
            "items": [
                {
                    "doc_id": "d1",
                    "text": "FastAPI is a great framework for building APIs.",
                },
                {
                    "doc_id": "d2",
                    "text": "Vector search enables semantic retrieval and RAG.",
                },
            ]
        },
    )
    assert r.status_code == 200 and r.json()["ingested"] == 2

    r2 = client.post(
        "/api/v1/rag/search", json={"query": "semantic retrieval", "top_k": 2}
    )
    assert r2.status_code == 200
    data = r2.json()
    assert data["count"] >= 1
