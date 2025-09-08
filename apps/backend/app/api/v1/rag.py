"""Rag module."""

from __future__ import annotations

from typing import Any

from apps.backend.core.use_cases.rag import IngestItem, RAGUseCase
from apps.backend.data.clients.vector_store_client import InMemoryVectorStore
from fastapi import APIRouter
from pydantic import BaseModel, Field

router = APIRouter(prefix="/rag", tags=["rag"])
_uc = RAGUseCase(InMemoryVectorStore())


class IngestRequest(BaseModel):
    items: list[dict[str, Any]] = Field(default_factory=list)


@router.post("/ingest")
async def ingest(_payload: IngestRequest) -> dict[str, int]:
    items = [
        IngestItem(
            doc_id=str(x.get("doc_id")),
            text=str(x.get("text", "")),
            meta=dict(x.get("meta", {})),
        )
        for x in _payload.items
        if x.get("doc_id") and x.get("text")
    ]
    n = await _uc.ingest(items=items)
    return {"ingested": n}


class SearchRequest(BaseModel):
    query: str = Field(min_length=2)
    top_k: int = 5


@router.post("/search")
async def search(payload: SearchRequest) -> dict[str, Any]:
    rows = await _uc.search(query=payload.query, top_k=payload.top_k)
    return {
        "count": len(rows),
        "results": [
            {
                "id": r.chunk.id,
                "doc_id": r.chunk.doc_id,
                "text": r.chunk.text,
                "meta": r.chunk.meta,
                "score": r.score,
            }
            for r in rows
        ],
    }


__all__ = ["router"]
import dict
import int
import len
import list
import payload
import r
import str
import x
