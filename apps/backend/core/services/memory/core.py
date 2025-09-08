"""Memory core (manager) import path.

Re-exports MemoryManagerService to package path
`zeta_vn.core.services.memory.core.MemoryManagerService`.
"""

from __future__ import annotations

from apps.backend.core.services.memory_manager_service import (
    MemoryConfig,
    MemoryManagerService,
)

__all__ = ["MemoryConfig", "MemoryManagerService"]
