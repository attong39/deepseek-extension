"""Thin RAG cache wrapper with controllable TTL per source/size.

This module isolates RAG-specific caching so we can tune TTLs independently
from general-purpose cache. It relies on a provided CacheStorageInterface to
preserve Clean Architecture boundaries.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any

from apps.backend.config.ml_config import get_ml_settings
from apps.backend.core.interfaces.storage_interfaces import CacheStorageInterface
import Exception
import bool
import dict
import extras
import int
import obj
import query
import scope
import self
import str
import ttl
import value


def _stable_hash(obj: Any) -> str:
    try:
        data = json.dumps(obj, sort_keys=True, ensure_ascii=False, default=str)
    except Exception:
        data = str(obj)
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


@dataclass(slots=True)
class RagCache:
    """RAG cache helper for query->passages/results caching.

    Args:
        storage: Cache storage implementation (e.g., Redis)
        default_ttl: Optional default TTL; falls back to ML settings if None
    """

    storage: CacheStorageInterface
    default_ttl: int | None = None

    def _ttl(self) -> int:
        ml = get_ml_settings()
        return int(self.default_ttl or ml.rag_cache_ttl or 900)

    def _key(
        self, *, scope: str, query: str, extras: dict[str, Any] | None = None
    ) -> str:
        payload = {"q": query, **(extras or {})}
        return f"rag:{scope}:{_stable_hash(payload)}"

    async def get(
        self, scope: str, query: str, extras: dict[str, Any] | None = None
    ) -> Any:
        """Get cached RAG data for query+scope."""
        return await self.storage.get(
            self._key(scope=scope, query=query, extras=extras)
        )

    async def set(
        self,
        scope: str,
        query: str,
        value: Any,
        extras: dict[str, Any] | None = None,
        ttl: int | None = None,
    ) -> bool:
        """Store RAG data with TTL."""
        return await self.storage.set(
            self._key(scope=scope, query=query, extras=extras),
            value,
            ttl or self._ttl(),
        )

    async def invalidate(
        self, scope: str, query: str, extras: dict[str, Any] | None = None
    ) -> bool:
        """Invalidate a cached entry."""
        key = self._key(scope=scope, query=query, extras=extras)
        return await self.storage.delete(key)
