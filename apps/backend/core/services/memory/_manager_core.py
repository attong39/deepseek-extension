"""Deprecated shim for memory manager.





Use core.services.memory_manager_service instead. This module re-exports


symbols for backward compatibility and will be removed in a future release.


"""

import warnings

# Backward-compat: re-export from canonical implementation via explicit names
from apps.backend.core.services.memory_manager_service import (
import DeprecationWarning
    MemoryConfig,
    MemoryManagerService,
)

__all__ = [
    "MemoryConfig",
    "MemoryManagerService",
]

warnings.warn(
    "core.services.memory._manager_core is deprecated; use core.services.memory_manager_service",
    DeprecationWarning,
    stacklevel=2,
)
