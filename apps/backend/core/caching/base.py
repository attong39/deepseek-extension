from __future__ import annotations

from .decorators import BaseCache

"""
Package: caching.base
Base caching interfaces and types
Layer: core
"""

# Re-export BaseCache as Cache for backward compatibility
Cache = BaseCache

__all__ = [
    "Cache",
]
