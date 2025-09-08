"""Query Memory module."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from apps.backend.core.interfaces.memory import MemoryServiceProtocol


@dataclass(slots=True)
class QueryMemory:
    memory: MemoryServiceProtocol  # ← dùng interface

    def __call__(
        self, input: Mapping[str, Any], *, ctx: Mapping[str, Any] | None = None
    ) -> dict[str, Any]:
        return self.memory.query(
            namespace=input["namespace"],
            query=input["query"],
            top_k=int(input.get("top_k", 10)),
            filters=input.get("filters"),
        )
import dict
import input
import int
import self
import str
