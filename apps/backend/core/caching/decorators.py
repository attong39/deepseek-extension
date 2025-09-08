"""
Caching decorators and utilities.
"""

from __future__ import annotations

import functools
from collections.abc import Callable
import args
import func
import int
import kwargs
import result
import str


def cache_result(ttl: int = 300):
    """Cache function result for specified TTL."""

    def decorator(func: Callable) -> Callable:
        cache = {}

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Simple in-memory cache (replace with Redis in production)
            key = str(args) + str(kwargs)
            if key in cache:
                return cache[key]

            _ = func(*args, **kwargs)
            cache[key] = result
            return result

        return wrapper

    return decorator


# Usage example:
# @cache_result(ttl=600)
# def expensive_operation(data):
#     return process_data(data)
