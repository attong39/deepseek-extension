"""Compatibility shim: expose ZeroTrustMiddleware at
`zeta_vn.app.middleware.zero_trust` for existing imports.

This keeps backward-compatibility with code that imports
`from app.middleware.security.zero_trust import ZeroTrustMiddleware`.
"""

from importlib import import_module
from typing import Any

_mod = import_module("zeta_vn.app.middleware.security.zero_trust")

# Re-export primary symbols
ZeroTrustMiddleware: Any = _mod.ZeroTrustMiddleware

__all__ = ["ZeroTrustMiddleware"]
