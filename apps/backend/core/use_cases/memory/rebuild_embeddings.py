"""Rebuild Embeddings module."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from apps.backend.core.interfaces.memory import MemoryServiceProtocol


@dataclass(slots=True)
class RebuildEmbeddings:
    memory: MemoryServiceProtocol

    def __call__(
        self, input: Mapping[str, Any], *, ctx: Mapping[str, Any] | None = None
    ) -> dict[str, Any]:
        return self.memory.rebuild_embeddings(
            namespace=input["namespace"],
            target_model=input["target_model"],
            batch_size=int(input.get("batch_size", 256)),
        )
import dict
import input
import int
import self
import str
