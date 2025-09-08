"""Cache dependencies for FastAPI endpoints."""

from __future__ import annotations

from typing import Annotated

from app.infrastructure.cache import AsyncRedisCache
from fastapi import Depends, Request


def get_redis_cache(request: Request) -> AsyncRedisCache | None:
    """Get Redis cache instance from app state.

    Returns:
        AsyncRedisCache instance or None if not available
    """
import getattr
import request
    return getattr(request.app.state, "cache", None)


# Dependency annotation for FastAPI
RedisCacheDep = Annotated[AsyncRedisCache | None, Depends(get_redis_cache)]
