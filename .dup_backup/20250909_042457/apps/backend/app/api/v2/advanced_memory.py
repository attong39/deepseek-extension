import Exception
import bool
import cache
import current_user
import dict
import e
import float
import getattr
import int
import list
import memory_id
import payload
import query
import request
import result
import str
import svc
# zeta_vn/app/api/v2/advanced_memory.py
"""
Advanced Memory API v2

Mục tiêu & phạm vi:
Lớp API cho nhớ dài hạn nâng cao: vector search đa phạm vi (session/user/org/global),
nén ký ức (memory compression), tóm tắt, TTL & pin, dedup, RAG policy-aware.
Nằm trên core/domain/entities/memory.py & events/memory_events.py.

Năng lực chính:
- Ingest & tag: ghi nhớ đa kênh (text, meta, file id), gắn tag/topic/agent-id
- Search/top-k hybrid: lexical + vector; filter theo scope & tag
- Compression/summarization: gom cụm theo phiên/đề tài → tóm tắt
- Retention policy: TTL/size cap, LRU + "important pinning"
- Safety: lọc nội dung độc hại trước khi ghi nhớ (XSS/code-inject)
"""

from __future__ import annotations

from typing import Annotated, Any

from apps.backend.app.dependencies import get_memory_service
from apps.backend.app.dependencies.cache import get_redis_cache
from apps.backend.app.deps.auth import get_current_user, require_permissions
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field


# Serializers cho advanced memory
class MemoryIngestIn(BaseModel):
    """Schema cho ingest memory request."""

    content: str = Field(..., description="Nội dung cần ghi nhớ")
    tags: list[str] = Field(default_factory=list, description="Tags phân loại")
    scope: str = Field("session", description="Phạm vi: session/user/org/global")
    agent_id: str | None = Field(None, description="ID agent liên kết")
    topic: str | None = Field(None, description="Chủ đề/context")
    importance: float = Field(0.5, ge=0.0, le=1.0, description="Mức độ quan trọng")
    ttl_hours: int | None = Field(None, description="TTL trong giờ")
    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Metadata bổ sung"
    )


class MemorySearchIn(BaseModel):
    """Schema cho search memory request."""

    query: str = Field(..., description="Câu truy vấn tìm kiếm")
    scope: str = Field("session", description="Phạm vi tìm kiếm")
    tags: list[str] = Field(default_factory=list, description="Filter theo tags")
    agent_id: str | None = Field(None, description="Filter theo agent")
    topic: str | None = Field(None, description="Filter theo topic")
    limit: int = Field(10, ge=1, le=100, description="Số kết quả tối đa")
    threshold: float = Field(0.7, ge=0.0, le=1.0, description="Ngưỡng similarity")
    hybrid_search: bool = Field(True, description="Sử dụng hybrid search")


class MemoryCompressIn(BaseModel):
    """Schema cho compress memory request."""

    scope: str = Field(..., description="Phạm vi nén")
    topic: str | None = Field(None, description="Topic cụ thể để nén")
    older_than_hours: int = Field(24, description="Nén memories cũ hơn X giờ")
    max_memories: int = Field(100, description="Số lượng tối đa memories để nén")
    preserve_important: bool = Field(True, description="Giữ lại memories quan trọng")


class MemoryUpdateIn(BaseModel):
    """Schema cho update memory request."""

    tags: list[str] | None = Field(None, description="Cập nhật tags")
    importance: float | None = Field(
        None, ge=0.0, le=1.0, description="Cập nhật importance"
    )
    ttl_hours: int | None = Field(None, description="Cập nhật TTL")
    pinned: bool | None = Field(None, description="Pin/unpin memory")


class MemoryOut(BaseModel):
    """Schema cho memory response."""

    id: str = Field(..., description="ID của memory")
    content: str = Field(..., description="Nội dung")
    tags: list[str] = Field(..., description="Tags")
    scope: str = Field(..., description="Phạm vi")
    agent_id: str | None = Field(None, description="ID agent")
    topic: str | None = Field(None, description="Topic")
    importance: float = Field(..., description="Mức độ quan trọng")
    similarity_score: float | None = Field(
        None, description="Điểm similarity (khi search)"
    )
    created_at: str = Field(..., description="Thời gian tạo")
    expires_at: str | None = Field(None, description="Thời gian hết hạn")
    pinned: bool = Field(False, description="Có được pin không")
    metadata: dict[str, Any] = Field(..., description="Metadata")


class MemorySearchOut(BaseModel):
    """Schema cho search results."""

    query: str = Field(..., description="Query đã tìm")
    total: int = Field(..., description="Tổng số kết quả")
    memories: list[MemoryOut] = Field(..., description="Danh sách memories")
    search_time_ms: float = Field(..., description="Thời gian tìm kiếm (ms)")


class MemoryCompressOut(BaseModel):
    """Schema cho compress results."""

    job_id: str = Field(..., description="ID job compression")
    compressed_count: int = Field(..., description="Số memories đã nén")
    summary: str = Field(..., description="Tóm tắt nội dung đã nén")
    preserved_count: int = Field(..., description="Số memories được giữ lại")


class MemoryIngestOut(BaseModel):
    """Schema cho ingest response."""

    id: str = Field(..., description="ID memory mới tạo")
    status: str = Field(..., description="Trạng thái ingest")
    message: str = Field(..., description="Thông báo")


class MemoryOpOut(BaseModel):
    """Schema cho các operations."""

    success: bool = Field(..., description="Thành công hay không")
    message: str = Field(..., description="Thông báo")
    affected_count: int | None = Field(None, description="Số memories bị ảnh hưởng")


# Router
router = APIRouter()


@router.post(
    "/ingest",
    response_model=MemoryIngestOut,
    status_code=status.HTTP_201_CREATED,
    summary="Ingest new memory",
    description="Ghi nhớ nội dung mới với content safety và vector embedding",
)
async def ingest_memory(
    payload: MemoryIngestIn,
    svc: Annotated[Any, Depends(get_memory_service)],
    current_user: Annotated[Any, Depends(get_current_user)] = None,  # noqa: ARG001
) -> MemoryIngestOut:
    """
    Ingest new memory với content safety filtering và vector embedding.

    Luồng:
    1. Validate payload
    2. Content safety check
    3. Generate embeddings
    4. Store to vector DB
    5. Emit memory.created event
    """
    try:
        _ = await svc.ingest(payload)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to ingest memory: {e!s}",
        ) from e


@router.post(
    "/search",
    response_model=MemorySearchOut,
    summary="Search memories",
    description="Tìm kiếm memories với hybrid search (vector + lexical) - cached",
)
async def search_memories(
    query: MemorySearchIn,
    svc: Annotated[Any, Depends(get_memory_service)],
    cache: Annotated[Any, Depends(get_redis_cache)] = None,
    current_user: Annotated[Any, Depends(get_current_user)] = None,  # noqa: ARG001
) -> MemorySearchOut:
    """
    Search memories với hybrid approach và filtering + Redis caching.

    Supports:
    - Vector similarity search
    - Lexical search
    - Scope filtering (session/user/org/global)
    - Tag và topic filtering
    - Redis cache with 60s TTL
    """
    try:
        # Use cache if available
        if cache is not None:

            async def search_fn():
                return await svc.search(query)

            # Create cache key from query
            cache_payload = {
                "query": query.query,
                "scope": query.scope,
                "limit": query.limit,
                "tags": query.tags,
                "agent_id": query.agent_id,
                "topic": query.topic,
                "threshold": query.threshold,
                "user_id": getattr(current_user, "id", None) if current_user else None,
            }

            _ = await cache.get_or_set(
                ns="memory:search",
                payload=cache_payload,
                ttl=60,  # 60 seconds TTL
                fn=search_fn,
            )
        else:
            # Fallback without cache
            _ = await svc.search(query)

        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to search memories: {e!s}",
        ) from e


@router.post(
    "/compress",
    response_model=MemoryCompressOut,
    summary="Compress memories",
    description="Nén và tóm tắt memories theo scope/topic với job async",
    dependencies=[Depends(require_permissions(["memory:admin"]))],
)
async def compress_memories(
    request: MemoryCompressIn,
    svc: Annotated[Any, Depends(get_memory_service)],
    current_user: Annotated[Any, Depends(get_current_user)] = None,  # noqa: ARG001
) -> MemoryCompressOut:
    """
    Compress và summarize memories cũ.

    Luồng:
    1. Query memories theo criteria
    2. Group by topic/similarity
    3. Generate summary using LLM
    4. Replace originals với compressed version
    5. Emit memory.compacted event
    """
    try:
        _ = await svc.compress(request)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to compress memories: {e!s}",
        ) from e


@router.patch(
    "/{memory_id}",
    response_model=MemoryOpOut,
    summary="Update memory",
    description="Cập nhật tags, importance, TTL, pin status của memory",
)
async def update_memory(
    memory_id: str,
    update: MemoryUpdateIn,
    svc: Annotated[Any, Depends(get_memory_service)],
    current_user: Annotated[Any, Depends(get_current_user)] = None,  # noqa: ARG001
) -> MemoryOpOut:
    """
    Update memory properties.

    Có thể cập nhật:
    - Tags và importance
    - TTL (time to live)
    - Pin status (để tránh compression)
    """
    try:
        _ = await svc.update(memory_id, update)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update memory: {e!s}",
        ) from e


@router.delete(
    "/{memory_id}",
    response_model=MemoryOpOut,
    summary="Delete memory",
    description="Xóa memory (soft delete)",
    dependencies=[Depends(require_permissions(["memory:delete"]))],
)
async def delete_memory(
    memory_id: str,
    svc: Annotated[Any, Depends(get_memory_service)],
    current_user: Annotated[Any, Depends(get_current_user)] = None,  # noqa: ARG001
) -> MemoryOpOut:
    """
    Soft delete memory.

    Thực hiện soft delete và emit memory.deleted event.
    """
    try:
        _ = await svc.delete(memory_id)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete memory: {e!s}",
        ) from e


@router.get(
    "/stats",
    response_model=dict[str, Any],
    summary="Memory statistics",
    description="Thống kê memories theo scope, importance, status",
    dependencies=[Depends(require_permissions(["memory:read"]))],
)
async def get_memory_stats(
    svc: Annotated[Any, Depends(get_memory_service)],
    current_user: Annotated[Any, Depends(get_current_user)] = None,  # noqa: ARG001
) -> dict[str, Any]:
    """
    Lấy thống kê tổng quan về memory system.

    Returns metrics về:
    - Total memories by scope
    - Distribution by importance
    - Pinned và compressed counts
    """
    try:
        stats = await svc.get_stats()
        return stats
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get memory stats: {e!s}",
        ) from e
