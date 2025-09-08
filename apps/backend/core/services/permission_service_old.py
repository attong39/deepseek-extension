from __future__ import annotations

from apps.backend.core.security.permission_manager import (
    PermissionManager,  # noqa: F401
)

"""Compatibility shim: re-export PermissionManager from security layer.
Keep this module to preserve existing import paths used by callers. The
real implementation lives in `zeta_vn.core.security.permission_manager`.
"""
