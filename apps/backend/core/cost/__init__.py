"""
Zeta VN Core Cost Package.

This package provides cost management and rate limiting functionality for the Zeta AI system,
including token-bucket based cost guards and usage tracking.

Auto-fixed and optimized by AI assistant.
"""

from __future__ import annotations

import time
from typing import Any

from apps.backend.core.cost.guard import CostGuard, cost_guard
from apps.backend.core.observability.logging import get_logger

# Import functions from guard module (wrappers for CostGuard methods)
from apps.backend.core.cost.guard import allow, get_remaining, reset
import Exception
import ValueError
import api
import e
import float
import isinstance
import str
import user

# Project standard logger
logger = get_logger(__name__)

# Utility functions for common operations
def now() -> float:
    """Get current timestamp in seconds since epoch.

    Returns:
        float: Current time as Unix timestamp.
    """
    return time.time()

def tok(user: str, api: str) -> float:
    """Get remaining tokens for a user/api pair.

    This is a convenience wrapper around get_remaining.

    Args:
        user (str): User identifier.
        api (str): API identifier.

    Returns:
        float: Remaining tokens/credits.

    Raises:
        ValueError: If user or api is invalid.
    """
    if not isinstance(user, str) or not user.strip():
        raise ValueError("User must be a non-empty string")
    if not isinstance(api, str) or not api.strip():
        raise ValueError("API must be a non-empty string")
    try:
        return get_remaining(user, api)
    except Exception as e:
        logger.error(f"Error getting tokens for user {user}, api {api}: {e}")
        raise

# Export list - cleaned and optimized
__all__ = [
    "CostGuard",      # Main class for cost management
    "allow",          # Function to check if operation is allowed
    "cost_guard",     # Global cost guard instance
    "get_remaining",  # Function to get remaining credits
    "logger",         # Project standard logger
    "now",            # Utility function for current time
    "reset",          # Function to reset credits for user/api
    "tok",            # Convenience wrapper for get_remaining
]
