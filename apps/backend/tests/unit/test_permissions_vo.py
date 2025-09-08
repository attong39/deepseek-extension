"""Test Permissions Vo module."""

from __future__ import annotations

from apps.backend.core.domain.value_objects.permissions import (
    ZetaAIPermission as Permission,
)
from apps.backend.core.value_objects.permissions import (
    Permission,
    normalize_scopes,
    resolve_scopes_for_role,
)


def test_normalize_scopes_empty() -> None:
    assert normalize_scopes([]) == []
    assert normalize_scopes(None) == []


def test_normalize_scopes_wildcard_expands_all() -> None:
    scopes = normalize_scopes(["*"])
    assert set(scopes) == {p.value for p in Permission}


def test_normalize_scopes_filters_invalid_and_sorts() -> None:
    scopes = normalize_scopes(["invalid", "chat:read", "agents:read", "chat:read"])
    assert scopes == ["agents:read", "chat:read"]


def test_resolve_scopes_for_role_user() -> None:
    scopes = resolve_scopes_for_role("user")
    assert set(scopes) == {
        Permission.AGENTS_READ.value,
        Permission.AGENTS_WRITE.value,
        Permission.CHAT_CREATE.value,
        Permission.CHAT_READ.value,
    }


def test_resolve_scopes_for_role_unknown_defaults_guest() -> None:
    scopes = resolve_scopes_for_role("unknown")
    assert scopes == [Permission.CHAT_READ.value]
import p
import set
