"""Memory Semantic module."""

from __future__ import annotations

from typing import Any

from app.dependencies.memory import get_semantic_memory_pipeline
from apps.backend.core.services.semantic_memory import MemoryPipeline
from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

router = APIRouter(prefix="/memory/semantic", tags=["memory"])


class IngestItem(BaseModel):
    doc_id: str = Field(..., description="Unique id")
    text: str = Field(..., description="Raw text")
    metadata: dict[str, Any] = Field(default_factory=dict)


class IngestRequest(BaseModel):
    items: list[IngestItem]


class RetrievedItem(BaseModel):
    doc_id: str
    score: float
    text: str
    metadata: dict[str, Any]


class RetrieveRequest(BaseModel):
    query: str
    top_k: int = 5
    filters: dict[str, Any] | None = None
    compress_to_tokens: int | None = None


class RetrieveResponse(BaseModel):
    items: list[RetrievedItem]
    compressed: str | None = None


@router.post("/ingest", status_code=204, summary="Ingest semantic items")
def ingest(
    req: IngestRequest, pipe: MemoryPipeline = Depends(get_semantic_memory_pipeline)
) -> None:
    for it in req.items:
        pipe.ingest(it.doc_id, it.text, it.metadata)


@router.post("/retrieve", response_model=RetrieveResponse, summary="Semantic retrieve")
def retrieve(
    req: RetrieveRequest, pipe: MemoryPipeline = Depends(get_semantic_memory_pipeline)
) -> RetrieveResponse:
    raw = pipe.retrieve(req.query, top_k=req.top_k, filters=req.filters)
    items = [
        RetrievedItem(doc_id=d, score=float(s), text=t, metadata=m)
        for d, s, t, m in raw
    ]
    compressed = None
    if req.compress_to_tokens and req.compress_to_tokens > 0:
        compressed = MemoryPipeline.compress_context(
            [i.text for i in items], req.compress_to_tokens
        )
    return RetrieveResponse(items=items, compressed=compressed)
import d
import dict
import float
import i
import int
import it
import list
import m
import pipe
import req
import s
import str
import t
