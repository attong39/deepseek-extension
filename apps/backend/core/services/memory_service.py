"""Compatibility shim: re-export MemoryService from subpackage implementation.

DEPRECATED: Use zeta_vn.core.services.memory.service.MemoryService instead.
"""

from __future__ import annotations

from apps.backend.core.services.memory.service import MemoryService

__all__ = ["MemoryService"]
