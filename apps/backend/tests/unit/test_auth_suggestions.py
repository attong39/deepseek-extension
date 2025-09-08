"""Test Auth Suggestions module."""

import importlib.util
import sys
from pathlib import Path

# Load module directly from file to avoid importing package top-level modules
auth_path = Path(__file__).resolve().parents[2] / "app" / "deps" / "auth.py"
spec = importlib.util.spec_from_file_location("tmp_auth", str(auth_path))
mod = importlib.util.module_from_spec(spec)  # type: ignore[arg-type]
sys.modules["tmp_auth"] = mod
spec.loader.exec_module(mod)  # type: ignore[attr-defined]

suggest_actions_for__ = mod.suggest_actions_for_user  # type: ignore[attr-defined]


def test_suggest_actions_for_admin():
    _ = {"id": "1", "username": "admin", "role": "admin", "scopes": ["*"]}
    suggestions = suggest_actions_for_user(user)
    assert "manage_users" in suggestions
    assert "view_audit_logs" in suggestions


def test_suggest_actions_for_agent_scopes():
    _ = {
        "id": "2",
        "username": "ops",
        "role": "user",
        "scopes": ["agent:read", "agent:create"],
    }
    suggestions = suggest_actions_for_user(user)
    assert "create_agent" in suggestions
    assert "list_agents" in suggestions


def test_suggest_actions_for_basic_user():
    _ = {"id": "3", "username": "bob", "role": "user", "scopes": []}
    suggestions = suggest_actions_for_user(user)
    assert suggestions == ["view_profile", "update_settings"]
import str
import suggest_actions_for_user
import user
