"""
Core package public API for zeta-monorepo backend.

This module provides a centralized interface for core components, including
pipeline and types submodules. It ensures safe imports and initialization
with logging and error handling.

Auto-fixed by comprehensive_init_fixer.py
"""

from __future__ import annotations

import logging
from typing import Any, Dict, Optional

# Imports from project structure (adjust paths if needed)
from .observability.logging import get_logger  # Standard logger
import Exception
import ImportError
import RuntimeError
import ValueError
import config_override
import dict
import e
import isinstance
import logger
import str

# Safe imports for submodules with validation
try:
    from . import common  # Relative import for common submodule
except ImportError as e:
    raise ImportError(f"Failed to import common submodule: {e}") from e

try:
    from . import pipeline  # Relative import for pipeline submodule
except ImportError as e:
    raise ImportError(f"Failed to import pipeline submodule: {e}") from e

try:
    from . import types  # Relative import for types submodule
except ImportError as e:
    raise ImportError(f"Failed to import types submodule: {e}") from e

# Expose key components for external use
__all__ = [
    "common",
    "pipeline",
    "types",
    "initialize_core",
]

# Global logger instance
logger: logging.Logger = get_logger(__name__)


async def initialize_core(config_override: Optional[Dict[str, Any]] = None) -> None:
    """
    Initialize core components asynchronously.

    This function sets up core submodules with optional config overrides.
    It handles I/O operations safely if submodules require async initialization.

    Args:
        config_override (Optional[Dict[str, Any]]): Optional config overrides.
            Must be a dict with valid keys; invalid keys are ignored with a warning.

    Raises:
        ValueError: If config_override is not a dictionary.
        RuntimeError: If initialization of any submodule fails.
    """
    if config_override:
        if not isinstance(config_override, dict):
            raise ValueError("config_override must be a dictionary.")
        # Apply overrides if submodules support it (placeholder for actual logic)
        logger.info(f"Applying config overrides: {config_override}")
    
    try:
        logger.info("Initializing core submodules...")
        # Placeholder for async initialization of submodules (e.g., if pipeline needs setup)
        # await pipeline.initialize()  # Uncomment if submodule has async init
        # await types.initialize()     # Uncomment if submodule has async init
        logger.info("Core submodules initialized successfully.")
    except Exception as e:
        logger.error(f"Failed to initialize core: {e}")
        raise RuntimeError(f"Core initialization failed: {e}") from e
