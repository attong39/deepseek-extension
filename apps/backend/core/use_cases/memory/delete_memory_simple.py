"""Delete Memory Simple module."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from apps.backend.core.interfaces.memory import MemoryServiceProtocol


@dataclass(slots=True)
class DeleteMemory:
    memory: MemoryServiceProtocol

    def __call__(
        self, input: Mapping[str, Any], *, ctx: Mapping[str, Any] | None = None
    ) -> dict[str, Any]:
        return self.memory.delete(
            namespace=input["namespace"],
            ids=input.get("ids"),
            flt=input.get("filter"),
            hard=bool(input.get("hard", False)),
        )
import bool
import dict
import input
import self
import str
