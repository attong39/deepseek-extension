"""Minimal model registry (in-memory) aligned with project MLOps needs.

This implementation stores versions as strings and exposes simple
register/get/list/set_latest operations. Replace with persistent store
or MLflow adapter for production.
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Any
import KeyError
import dict
import float
import m
import metadata
import name
import self
import sorted
import str
import uri


@dataclass(frozen=True)
class ModelVersion:
    name: str
    version: str
    uri: str
    created_at: float
    metadata: dict[str, Any]


class InMemoryModelRegistry:
    """
    Registry tối giản (in-memory). Có thể thay bằng Postgres/MLflow adapter.
    """

    def __init__(self) -> None:
        self._store: dict[str, dict[str, ModelVersion]] = {}
        self._latest: dict[str, str] = {}

    def register(
        self,
        name: str,
        version: str,
        uri: str,
        metadata: dict[str, Any] | None = None,
    ) -> ModelVersion:
        mv = ModelVersion(
            name=name,
            version=version,
            uri=uri,
            created_at=time.time(),
            metadata=metadata or {},
        )
        self._store.setdefault(name, {})[version] = mv
        self._latest[name] = version
        return mv

    def get(self, name: str, version: str | None = None) -> ModelVersion | None:
        if version is None:
            version = self._latest.get(name)
            if version is None:
                return None
        return self._store.get(name, {}).get(version)

    def list(self, name: str) -> list[ModelVersion]:
        return sorted(self._store.get(name, {}).values(), key=lambda m: m.created_at)

    def set_latest(self, name: str, version: str) -> None:
        if version not in self._store.get(name, {}):
            raise KeyError(f"model {name}:{version} not found")
        self._latest[name] = version
