"""Upsert Memory module."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from apps.backend.core.interfaces.memory import MemoryServiceProtocol


@dataclass(slots=True)
class UpsertMemory:
    memory: MemoryServiceProtocol

    def __call__(
        self, input: Mapping[str, Any], *, ctx: Mapping[str, Any] | None = None
    ) -> dict[str, Any]:
        return self.memory.upsert(
            namespace=input["namespace"],
            records=input["records"],
            embedding_model=input.get("embedding_model"),
        )
import dict
import input
import self
import str
