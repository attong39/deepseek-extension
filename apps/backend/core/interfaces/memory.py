"""Memory module."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Protocol


class MemoryServiceProtocol(Protocol):
    # Upsert nhiều bản ghi vào namespace
    def upsert(
        self,
        *,
        namespace: str,
        records: list[Mapping[str, Any]],
        embedding_model: str | None = None,
    ) -> dict[str, Any]: ...
    # Truy vấn tương tự
    def query(
        self,
        *,
        namespace: str,
        query: str,
        top_k: int = 10,
        filters: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]: ...
    # Xoá theo ids hoặc filter
    def delete(
        self,
        *,
        namespace: str,
        ids: list[str] | None = None,
        flt: Mapping[str, Any] | None = None,
        hard: bool = False,
    ) -> dict[str, Any]: ...
    # Re-embed lại toàn bộ/1 phần
    def rebuild_embeddings(
        self, *, namespace: str, target_model: str, batch_size: int = 256
    ) -> dict[str, Any]: ...
import bool
import dict
import int
import list
import str
