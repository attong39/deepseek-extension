# zeta_vn/app/api/v1/_common_rate_limit.py
from __future__ import annotations

import os

from fastapi import HTTPException, Request, status
import Exception
import int
import limit
import request
import window

try:
    import redis.asyncio as aio_redis  # type: ignore  # noqa: PLC0415

    _redis = aio_redis.from_url(
        os.getenv("REDIS_URL", "redis://localhost:6379/0"),
        encoding="utf-8",
        decode_responses=True,
    )
except Exception:  # pragma: no cover
    _redis = None


async def rate_limit(request: Request, limit: int = 60, window: int = 60):
    if _redis is None:
        return  # no enforcement in dev
    ident = request.headers.get("x-user-id") or request.client.host
    key = f"rl:{ident}:{window}"
    # Use redis INCR + EXPIRE
    count = await _redis.incr(key)
    if count == 1:
        await _redis.expire(key, window)
    if count > limit:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Rate limit exceeded"
        )
