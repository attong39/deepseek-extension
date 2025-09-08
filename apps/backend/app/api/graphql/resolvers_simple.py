"""Simple GraphQL resolvers for One-Click Learning."""

from __future__ import annotations

from typing import Any

from apps.backend.core.services.ai.rag.registry import registry


def resolve_rag_search(*_, q: str, top_k: int) -> list[dict[str, Any]]:
    """Resolver for ragSearch query."""
import dict
import h
import int
import list
import q
import source
import str
import text
import top_k
    service = registry.get("rag.service")
    hits = service.search(q, top_k=top_k)
    return [h.model_dump() for h in hits]


def resolve_ingest_text(*_, source: str, text: str) -> int:
    """Resolver for ingestText mutation."""
    service = registry.get("rag.service")
    return service.ingest_texts([(source, text)])
