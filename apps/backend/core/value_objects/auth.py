"""Compatibility layer for auth value objects.

Allows imports like `from core.value_objects.auth import LoginRequest` by
re-exporting the canonical definitions from `core.domain.value_objects.auth`.
"""

from __future__ import annotations

from apps.backend.core.domain.value_objects.auth import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
)

# Explicit export list for compatibility
__all__ = [
    "LoginRequest",
    "RegisterRequest",
    "TokenResponse",
]
