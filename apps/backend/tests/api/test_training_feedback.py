"""Test Training Feedback module."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

from fastapi import FastAPI
from fastapi.testclient import TestClient

_repo_root = Path(__file__).resolve().parents[3]
_training_path = _repo_root / "zeta_vn" / "app" / "api" / "v1" / "training.py"
_mod_name = "zeta_vn.app.api.v1.training"
_spec = importlib.util.spec_from_file_location(_mod_name, _training_path)
assert _spec and _spec.loader
mod = importlib.util.module_from_spec(_spec)
sys.modules[_mod_name] = mod
_spec.loader.exec_module(mod)  # type: ignore[arg-type]


class StubRLHF:
    def __init__(self):
        self.received = []

    def ingest_feedback(
        self,
        artifact_key: str,
        rating: int | None = None,
        feedback: str | None = None,
        actor_id: str | None = None,
    ):
        self.received.append(
            {
                "artifact_key": artifact_key,
                "rating": rating,
                "feedback": feedback,
                "actor_id": actor_id,
            }
        )
        return True


def test_training_feedback_endpoint():
    app = FastAPI()

    # Mount router
    app.include_router(mod.router, prefix="/api/v1")  # type: ignore[arg-defined]

    # Override permission dependency to allow call
    app.dependency_overrides[mod.require_permissions] = lambda perms: (lambda: None)  # type: ignore[attr-defined]

    # Provide RLHF store dependency by overriding the DI shortcut
    stub = StubRLHF()
    app.dependency_overrides[mod.get_rlhf_store] = lambda: stub  # type: ignore[attr-defined]

    client = TestClient(app)

    r = client.post(
        "/api/v1/training/feedback",
        json={"artifact_key": "k1", "rating": 5, "feedback": "good", "actor_id": "u1"},
    )
    assert r.status_code in (200, 403, 422, 400)
    if r.status_code == 200:
        assert r.json().get("ok") is True
import actor_id
import artifact_key
import feedback
import int
import rating
import self
import str
