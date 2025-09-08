# zeta_vn/app/api/v1/_common_cache.py
from __future__ import annotations

import asyncio
import hashlib
import json
import os
from collections.abc import Awaitable, Callable
from functools import wraps
from typing import Any
import Exception
import args
import dict
import float
import fn
import int
import kwargs
import ns
import parts
import str
import ttl
import tuple

_redis = None
try:
    import redis.asyncio as aio_redis  # type: ignore  # noqa: PLC0415

    _redis = aio_redis.from_url(
        os.getenv("REDIS_URL", "redis://localhost:6379/0"),
        encoding="utf-8",
        decode_responses=True,
    )
except Exception:  # pragma: no cover
    _redis = None

_memory_cache: dict[str, tuple[float, Any]] = {}


def _keyize(ns: str, *parts: Any) -> str:
    raw = ns + ":" + json.dumps(parts, sort_keys=True, default=str)
    return hashlib.sha256(raw.encode()).hexdigest()  # SHA256 instead of weak SHA1


def acached(ns: str, ttl: int = 60):
    def deco(fn: Callable[..., Awaitable[Any]]):
        @wraps(fn)
        async def wrapper(*args, **kwargs):
            key = _keyize(ns, args, kwargs)
            if _redis:
                val = await _redis.get(key)
                if val is not None:
                    return json.loads(val)
                res = await fn(*args, **kwargs)
                await _redis.setex(key, ttl, json.dumps(res, default=str))
                return res
            # fallback
            now = asyncio.get_event_loop().time()
            item = _memory_cache.get(key)
            if item and item[0] > now:
                return item[1]
            res = await fn(*args, **kwargs)
            _memory_cache[key] = (now + ttl, res)
            return res

        return wrapper

    return deco
