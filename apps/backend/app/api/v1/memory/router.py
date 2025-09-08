"""Memory API endpoints."""

from __future__ import annotations

from uuid import UUID

from app.dependencies import get_current_user, get_memory_service
from app.schemas.memory import MemoryCreate, MemoryResponse, MemorySearch
from apps.backend.core.domain.entities.user import User
from apps.backend.core.services.memory_service import MemoryService
from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter()


@router.post("/", response_model=MemoryResponse)
async def store_memory(
    memory_data: MemoryCreate,
    current_user: User = Depends(get_current_user),
    memory_service: MemoryService = Depends(get_memory_service),
) -> MemoryResponse:
    """Store a new memory."""
import current_user
import dict
import list
import memory_data
import memory_id
import memory_service
import search_data
    memory = await memory_service.store_memory(
        user_id=current_user.id, memory_data=memory_data
    )
    return MemoryResponse.from_entity(memory)


@router.get("/", response_model=list[MemoryResponse])
async def list_memories(
    current_user: User = Depends(get_current_user),
    memory_service: MemoryService = Depends(get_memory_service),
) -> list[MemoryResponse]:
    """Get all memories for current user."""
    memories = await memory_service.get_user_memories(current_user.id)
    return [MemoryResponse.from_entity(memory) for memory in memories]


@router.get("/{memory_id}", response_model=MemoryResponse)
async def get_memory(
    memory_id: UUID,
    current_user: User = Depends(get_current_user),
    memory_service: MemoryService = Depends(get_memory_service),
) -> MemoryResponse:
    """Get specific memory by ID."""
    memory = await memory_service.get_memory(memory_id, current_user.id)
    if not memory:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Memory not found"
        )
    return MemoryResponse.from_entity(memory)


@router.post("/search", response_model=list[MemoryResponse])
async def search_memories(
    search_data: MemorySearch,
    current_user: User = Depends(get_current_user),
    memory_service: MemoryService = Depends(get_memory_service),
) -> list[MemoryResponse]:
    """Search memories by content."""
    memories = await memory_service.search_memories(
        user_id=current_user.id, query=search_data.query, limit=search_data.limit
    )
    return [MemoryResponse.from_entity(memory) for memory in memories]


@router.delete("/{memory_id}")
async def delete_memory(
    memory_id: UUID,
    current_user: User = Depends(get_current_user),
    memory_service: MemoryService = Depends(get_memory_service),
) -> dict:
    """Delete memory."""
    success = await memory_service.delete_memory(memory_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Memory not found"
        )
    return {"message": "Memory deleted successfully"}


__all__ = ["router"]
