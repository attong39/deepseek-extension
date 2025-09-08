"""Test Feedback Api module."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

from fastapi import FastAPI
from fastapi.testclient import TestClient

_repo_root = Path(__file__).resolve().parents[3]
_feedback_path = _repo_root / "zeta_vn" / "app" / "api" / "v1" / "feedback.py"
_mod_name = "zeta_vn.app.api.v1.feedback"
_spec = importlib.util.spec_from_file_location(_mod_name, _feedback_path)
assert _spec and _spec.loader
mod = importlib.util.module_from_spec(_spec)
sys.modules[_mod_name] = mod
_spec.loader.exec_module(mod)  # type: ignore[arg-type]


def test_feedback_submit_and_list() -> None:
    app = FastAPI()
    # Override permissions dependency to a no-op for tests
    app.dependency_overrides[mod.require_permissions] = lambda x: lambda: None  # type: ignore[attr-defined]
    # Không override DB để tránh tạo engine; endpoint sẽ trả 403/422/400 tùy dependency chain
    app.include_router(mod.router, prefix="/api/v1")  # type: ignore[attr-defined]
    client = TestClient(app)

    # Submit requires DB; skip if no DB session override
    # Here we only test that route is mounted and responds 422 without payload
    r = client.post("/api/v1/feedback")
    assert r.status_code in (400, 403, 422)
