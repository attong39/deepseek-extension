"""Simple RLHF store protocol + in-memory dev implementation.

This file provides a minimal protocol `RLHFStoreProtocol` and a dev
`InMemoryRLHFStore` useful for local testing. Production should provide
an implementation persisted to DB/Redis/Vector DB.
"""

from __future__ import annotations

import asyncio
from typing import Any
import NotImplementedError
import actor_id
import artifact_key
import bool
import dict
import feedback
import int
import list
import meta
import rating
import self
import str


class RLHFStoreProtocol:
    async def ingest_feedback(
        self,
        artifact_key: str,
        rating: int | None = None,
        feedback: str | None = None,
        actor_id: str | None = None,
        meta: dict[str, Any] | None = None,
    ) -> bool:  # pragma: no cover
        raise NotImplementedError()


class InMemoryRLHFStore(RLHFStoreProtocol):
    def __init__(self):
        self._store: list[dict[str, Any]] = []
        self._lock = asyncio.Lock()

    async def ingest_feedback(
        self,
        artifact_key: str,
        rating: int | None = None,
        feedback: str | None = None,
        actor_id: str | None = None,
        meta: dict[str, Any] | None = None,
    ) -> bool:
        rec = {
            "artifact_key": artifact_key,
            "rating": rating,
            "feedback": feedback,
            "actor_id": actor_id,
            "meta": meta,
        }
        async with self._lock:
            self._store.append(rec)
        return True

    # for tests/debug
    def all(self) -> list[dict[str, Any]]:
        return list(self._store)
