import Exception
import dict
import e
import file
import float
import getattr
import int
import isinstance
import len
import list
import memory_id
import object
import payload
import q
import r
import request
import request_id
import str
import svc
import top_k
import typed_results
# Author: duy_bg_vn
"""
Memory/RAG API v1 - E2E Blueprint 2025

Enhanced với:
- POST /api/v1/memory/store (ingest với file support)
- POST /api/v1/memory/search (query với filters)
- Request-ID tracking
- Structured logging
"""

from __future__ import annotations

import logging
from collections.abc import Mapping, Sequence
from time import perf_counter
from typing import Annotated, Any, cast

from apps.backend.app.dependencies import get_memory_service
from apps.backend.app.deps.auth import require_permissions
from apps.backend.app.observability.shared_metrics import rag_retrieval_seconds
from apps.backend.app.serializers import memory_serializers as mem_ser
from apps.backend.core.use_cases.memory.delete_memory_simple import DeleteMemory
from apps.backend.core.use_cases.memory.query_memory import QueryMemory
from apps.backend.core.use_cases.memory.upsert_memory import UpsertMemory
from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    Query,
    Request,
    Response,
    UploadFile,
    status,
)
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


router = APIRouter(prefix="/memory", tags=["memory"])


class MemoryStoreIn(BaseModel):
    """Schema cho memory ingest theo E2E Blueprint."""

    source: str = Field(..., description="Nguồn tài liệu")
    text: str | None = Field(None, description="Text content")
    metadata: dict[str, Any] = Field(default_factory=dict, description="Metadata")


class MemorySearchIn(BaseModel):
    """Schema cho memory search với filters."""

    query: str = Field(..., description="Search query")
    k: int = Field(10, description="Số kết quả trả về")
    filters: dict[str, Any] = Field(default_factory=dict, description="Search filters")
    threshold: float = Field(0.7, description="Similarity threshold")


class MemoryMatch(BaseModel):
    """Schema cho memory search result."""

    chunk: str = Field(..., description="Text chunk")
    score: float = Field(..., description="Similarity score")
    source: str = Field(..., description="Source document")
    metadata: dict[str, Any] = Field(..., description="Chunk metadata")


class MemorySearchOut(BaseModel):
    """Enhanced search output."""

    matches: list[MemoryMatch] = Field(..., description="Search results")
    query: str = Field(..., description="Original query")
    total_found: int = Field(..., description="Total results found")


# --- Minimal semantic pipeline endpoints (local-only) ---


# Dependencies (local schemas + passthrough request-id)
class MemoryInSchema(BaseModel):
    content: str


class MemoryOutSchema(BaseModel):
    id: str
    content: str


def get_request_id_dep(request: Request) -> str:
    # Prefer request.state if middleware set it; else header; else fallback
    rid = getattr(getattr(request, "state", object()), "request_id", None)
    if isinstance(rid, str) and rid:
        return rid
    return request.headers.get("x-request-id") or "req_mock_123"


@router.post(
    "/store",
    response_model=mem_ser.MemoryOut,
    response_model_by_alias=True,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_permissions(["memory:write"]))],
)
async def store_document(
    request: MemoryStoreIn,
    svc: Annotated[Any, Depends(get_memory_service)],
    request_id: Annotated[str, Depends(get_request_id_dep)] = "req_default",
) -> dict[str, Any]:
    """
    Enhanced memory store theo E2E Blueprint.

    Flow:
    1. Text split + chunk
    2. Generate embeddings (cached in Redis)
    3. Store in VectorRepo + metadata
    """
    try:
        logger.info(f"[{request_id}] Storing document: source={request.source}")

        # Convert to legacy format for compatibility
        legacy_payload = MemoryInSchema(
            content=request.text or f"Source: {request.source}"
        )

        uc = UpsertMemory(memory=svc)
        m = uc(
            {"namespace": "default", "records": [{"content": legacy_payload.content}]}
        )

        logger.info(f"[{request_id}] Document stored successfully")
        # Normalize to centralized serializer for API contract (output camelCase)
        return mem_ser.MemoryOut(**m).model_dump(by_alias=True)

    except Exception as e:
        logger.error(f"[{request_id}] Store failed: {e!s}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to store document: {e!s}",
        ) from e


@router.post(
    "/store-file",
    response_model=mem_ser.MemoryOut,
    response_model_by_alias=True,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_permissions(["memory:write"]))],
)
async def store_file(
    file: Annotated[UploadFile, File(...)],
    source: str,
    svc: Annotated[Any, Depends(get_memory_service)],
    request_id: Annotated[str, Depends(get_request_id_dep)] = "req_default",
) -> dict[str, Any]:
    """Store file upload vào memory theo Blueprint."""
    try:
        logger.info(f"[{request_id}] Storing file: {file.filename}")

        # Read file content
        content = await file.read()
        text_content = (
            content.decode("utf-8")
            if file.content_type == "text/plain"
            else f"File: {file.filename}"
        )

        # Convert to legacy format
        legacy_payload = MemoryInSchema(content=text_content)

        uc = UpsertMemory(memory=svc)
        m = uc(
            {"namespace": "default", "records": [{"content": legacy_payload.content}]}
        )

        logger.info(f"[{request_id}] File stored successfully")
        return mem_ser.MemoryOut(**m).model_dump(by_alias=True)

    except Exception as e:
        logger.error(f"[{request_id}] File store failed: {e!s}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to store file: {e!s}",
        ) from e


@router.post(
    "/search",
    response_model=list[mem_ser.MemorySearchOut],
    response_model_by_alias=True,
    dependencies=[Depends(require_permissions(["memory:read"]))],
)
async def search_memory(
    request: MemorySearchIn,
    svc: Annotated[Any, Depends(get_memory_service)],
    request_id: Annotated[str, Depends(get_request_id_dep)] = "req_default",
) -> list[mem_ser.MemorySearchOut]:
    """
    Enhanced memory search với filters theo Blueprint.

    Flow:
    1. Generate query embedding (cached)
    2. Vector similarity search
    3. Apply filters
    4. Return top-k matches
    """
    try:
        logger.info(
            f"[{request_id}] Searching memory: query='{request.query}', k={request.k}"
        )

        # Measure RAG retrieval latency (vector similarity search flow)
        _t0 = perf_counter()
        uc = QueryMemory(memory=svc)
        results_any = uc(
            {
                "namespace": "default",
                "query": request.query,
                "top_k": request.k,
                "filters": request.filters,
            }
        )
        # Adapter may return a mapping with key 'results' or a raw list
        results_list: Sequence[Mapping[str, Any]]
        if isinstance(results_any, Mapping) and isinstance(
            results_any.get("results"), list
        ):
            results_list = cast(Sequence[Mapping[str, Any]], results_any.get("results"))
        elif isinstance(results_any, list):
            results_list = cast(Sequence[Mapping[str, Any]], results_any)
        else:
            results_list = []
        rag_retrieval_seconds.observe(perf_counter() - _t0)

        # Convert to centralized serializer list format
        matches = [
            mem_ser.MemorySearchOut(
                id=r.get("id", ""),
                score=r.get("score", 0.0),
                text=r.get("content", ""),
                metadata=r.get("metadata", {}),
            )
            for r in results_list
        ]

        logger.info(f"[{request_id}] Search completed: found={len(matches)}")
        return matches

    except Exception as e:
        logger.error(f"[{request_id}] Search failed: {e!s}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Memory search failed: {e!s}",
        ) from e


# Legacy endpoints for backward compatibility
@router.post(
    "",
    response_model=mem_ser.MemoryOut,
    response_model_by_alias=True,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_permissions(["memory:create"]))],
)
async def store_memory(
    payload: MemoryInSchema, svc: Any = Depends(get_memory_service)
) -> dict[str, Any]:
    """Legacy endpoint - use /store instead."""
    uc = UpsertMemory(memory=svc)
    m = uc({"namespace": "default", "records": [{"content": payload.content}]})
    return mem_ser.MemoryOut(**m).model_dump(by_alias=True)


@router.get(
    "/{memory_id}",
    response_model=mem_ser.MemoryOut,
    response_model_by_alias=True,
    dependencies=[Depends(require_permissions(["memory:read"]))],
)
async def get_memory(
    memory_id: str, svc: Any = Depends(get_memory_service)
) -> dict[str, Any]:
    # Try to get via adapter use-case (fallback to query by id)
    ucq = QueryMemory(memory=svc)
    out_any = ucq({"namespace": "default", "query": memory_id, "top_k": 1})
    items: list[Mapping[str, Any]]
    if isinstance(out_any, Mapping) and isinstance(out_any.get("results"), list):
        items = cast(list[Mapping[str, Any]], out_any.get("results"))
    elif isinstance(out_any, list):
        items = cast(list[Mapping[str, Any]], out_any)
    else:
        items = []
    if not items:
        raise HTTPException(status_code=404, detail="Memory not found")
    # normalize result
    first = items[0]
    return mem_ser.MemoryOut(**dict(first)).model_dump(by_alias=True)


@router.get(
    "/search",
    response_model=list[dict[str, Any]],
    dependencies=[Depends(require_permissions(["memory:read"]))],
)
async def search_memory_legacy(
    q: str = Query(..., min_length=1),
    top_k: int = Query(5, ge=1, le=50),
    svc: Any = Depends(get_memory_service),
) -> list[dict[str, Any]]:
    """Legacy search endpoint - use POST /search instead."""
    uc = QueryMemory(memory=svc)
    results_any = uc({"namespace": "default", "query": q, "top_k": top_k})
    # Normalize to list[dict[str, Any]] for typing safety
    items2: list[Mapping[str, Any]]
    if isinstance(results_any, Mapping) and isinstance(
        results_any.get("results"), list
    ):
        items2 = cast(list[Mapping[str, Any]], results_any.get("results"))
    elif isinstance(results_any, list):
        items2 = cast(list[Mapping[str, Any]], results_any)
    else:
        items2 = []
    typed_results: list[dict[str, Any]] = [dict(r) for r in items2]
    return typed_results


@router.delete(
    "/{memory_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
    response_class=Response,
    dependencies=[Depends(require_permissions(["memory:delete"]))],
)
async def delete_memory(
    memory_id: str, svc: Any = Depends(get_memory_service)
) -> Response:
    deleter = DeleteMemory(memory=svc)
    out = deleter({"namespace": "default", "ids": [memory_id]})
    # interpret adapter result
    ok = out.get("status") == "ok"
    if not ok:
        raise HTTPException(status_code=404, detail="Memory not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
