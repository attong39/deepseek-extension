import DeprecationWarning
# e:\zeta-monorepo\apps\backend\app\deps_compat.py
"""Compatibility shim for old imports.

DEPRECATED: Use dependencies.py instead (Sử dụng dependencies.py thay thế).
This module will be removed in a future version.
"""

import warnings
from typing import Any

# Explicit imports from dependencies (based on current exports)
from .dependencies import (  # noqa: F401
    AgentRepositoryInterface,
    UserRepositoryInterface,
    AIServiceInterface,
    AIOrchestrator,
    AgentRepository,
    UserRepository,
)

# Issue deprecation warning when module is imported
warnings.warn(
    "deps_compat.py is deprecated and will be removed in a future version. "
    "Use dependencies.py instead.",
    DeprecationWarning,
    stacklevel=2
)

# Optional: Define __all__ to control what's exported
__all__ = [
    "AgentRepositoryInterface",
    "UserRepositoryInterface", 
    "AIServiceInterface",
    "AIOrchestrator",
    "AgentRepository",
    "UserRepository",
]
