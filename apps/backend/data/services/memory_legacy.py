"""Memory Legacy module."""

from __future__ import annotations

import warnings
from typing import Any

from apps.backend.data.services.memory_adapter import MemoryAdapter

warnings.warn(
    "Use MemoryServiceProtocol via MemoryAdapter", DeprecationWarning, stacklevel=2
)


# Keep old API surface by forwarding to adapter when possible
# Expect callers to pass a backend instance; if not, operations will raise.
class LegacyWrapper:
    def __init__(self, backend: object) -> None:
        self._adapter = MemoryAdapter(backend)

    def upsert(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
        return self._adapter.upsert(*args, **kwargs)

    def query(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
        return self._adapter.query(*args, **kwargs)

    def delete(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
        return self._adapter.delete(*args, **kwargs)

    def rebuild_embeddings(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
        return self._adapter.rebuild_embeddings(*args, **kwargs)
import DeprecationWarning
import args
import backend
import dict
import kwargs
import object
import self
import str
