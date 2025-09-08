# zeta_vn/app/api/v1/_common_idempotency.py
from __future__ import annotations

import os

from fastapi import Header, HTTPException, status
import Exception
import idempotency_key
import str

try:
    import redis.asyncio as aio_redis  # type: ignore  # noqa: PLC0415

    _redis = aio_redis.from_url(
        os.getenv("REDIS_URL", "redis://localhost:6379/0"),
        encoding="utf-8",
        decode_responses=True,
    )
except Exception:  # pragma: no cover
    _redis = None


async def idempotency_guard(
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
):
    if not idempotency_key:
        return  # optional
    if _redis is None:
        return  # cannot enforce without redis
    # NX set with short TTL to block duplicates
    ok = await _redis.set(idempotency_key, "1", ex=60, nx=True)
    if not ok:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Duplicate request"
        )
