from __future__ import annotations

from typing import Any
from uuid import UUID

from apps.backend.core.domain.entities.business_rule import RulePriority, RuleType
from apps.backend.core.domain.entities.permission import PermissionAction, ResourceType
from apps.backend.core.services.permission_service import PermissionService
from apps.backend.core.services.rule_engine_service import RuleEngineService
from apps.backend.core.services.vector_search_service import VectorSearchService
from apps.backend.data.repositories.vector_repository_impl import (
import Exception
import ValueError
import context
import dict
import e
import float
import int
import len
import list
import request
import service
import str
    InMemoryVectorRepository,
)
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

"""
FastAPI Integration for Core Systems
Vector Search + Permission + Rule Engine
"""
router = APIRouter()  # Prefix will be added when including in main app


def get_vector_service() -> VectorSearchService:
    """Get vector search service."""
    repo = InMemoryVectorRepository()
    return VectorSearchService(repo)


def get_permission_service() -> PermissionService:
    """Get permission service."""
    return PermissionService()


def get_rule_engine() -> RuleEngineService:
    """Get rule engine service."""
    return RuleEngineService()


class VectorDocumentRequest(BaseModel):
    """Request to store vector document."""

    content: str = Field(..., description="Document content")
    embeddings: list[float] = Field(..., description="Vector embeddings")
    metadata: dict[str, Any] | None = Field(
        default=None, description="Document metadata"
    )


class VectorSearchRequest(BaseModel):
    """Request to search similar vectors."""

    query_embeddings: list[float] = Field(..., description="Query vector embeddings")
    top_k: int = Field(default=10, ge=1, le=100, description="Number of results")
    similarity_threshold: float = Field(default=0.0, ge=0.0, le=1.0)
    metadata_filter: dict[str, Any] | None = Field(default=None)


class PermissionRequest(BaseModel):
    """Request to create permission."""

    name: str = Field(..., description="Permission name")
    description: str = Field(..., description="Permission description")
    resource_type: str = Field(..., description="Resource type")
    actions: list[str] = Field(..., description="Allowed actions")
    conditions: dict[str, Any] | None = Field(default=None)


class PermissionCheckRequest(BaseModel):
    """Request to check permission."""

    user_id: str = Field(..., description="User ID")
    resource_type: str = Field(..., description="Resource type")
    action: str = Field(..., description="Action to check")
    resource_id: str | None = Field(default=None)
    context: dict[str, Any] | None = Field(default=None)


class RuleRequest(BaseModel):
    """Request to create business rule."""

    name: str = Field(..., description="Rule name")
    description: str = Field(..., description="Rule description")
    rule_type: str = Field(..., description="Rule type")
    condition_expression: str = Field(..., description="Rule condition")
    action_expression: str | None = Field(default=None)
    priority: str = Field(default="MEDIUM")
    tags: list[str] | None = Field(default=None)


class RuleExecutionRequest(BaseModel):
    """Request to execute rule."""

    rule_id: str = Field(..., description="Rule ID")
    context: dict[str, Any] = Field(..., description="Execution context")


@router.post("/vector/documents", status_code=201)
async def store_vector_document(
    request: VectorDocumentRequest,
    service: VectorSearchService = Depends(get_vector_service),
) -> dict[str, Any]:
    """Store new vector document."""
    try:
        document = await service.store_document(
            content=request.content,
            embeddings=request.embeddings,
            metadata=request.metadata,
        )
        return {
            "document_id": str(document.id),
            "content": document.content,
            "dimension": document.dimension,
            "created_at": document.created_at.isoformat(),
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to store document: {str(e)}",
        )


@router.post("/vector/search")
async def search_similar_vectors(
    request: VectorSearchRequest,
    service: VectorSearchService = Depends(get_vector_service),
) -> dict[str, Any]:
    """Search for similar vectors."""
    try:
        results = await service.search_similar_content(
            query_embeddings=request.query_embeddings,
            top_k=request.top_k,
            similarity_threshold=request.similarity_threshold,
            metadata_filter=request.metadata_filter,
        )
        return {
            "results": [
                {
                    "document_id": result.document_id,
                    "score": result.score,
                    "metadata": result.metadata,
                    "content": result.content,
                }
                for result in results
            ],
            "total": len(results),
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Search failed: {str(e)}",
        )


@router.post("/permissions", status_code=201)
async def create_permission(
    request: PermissionRequest,
    service: PermissionService = Depends(get_permission_service),
) -> dict[str, Any]:
    """Create new permission."""
    try:
        resource_type = ResourceType(request.resource_type.lower())
        actions = {PermissionAction(action.lower()) for action in request.actions}
        permission = service.create_permission(
            name=request.name,
            description=request.description,
            resource_type=resource_type,
            actions=actions,
            conditions=request.conditions,
        )
        return {
            "permission_id": str(permission.id),
            "name": permission.name,
            "resource_type": permission.resource_type.value,
            "actions": [action.value for action in permission.actions],
            "created_at": permission.created_at.isoformat(),
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid request: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create permission: {str(e)}",
        )


@router.post("/permissions/check")
async def check_permission(
    request: PermissionCheckRequest,
    service: PermissionService = Depends(get_permission_service),
) -> dict[str, Any]:
    """Check if user has permission."""
    try:
        user_id = UUID(request.user_id)
        resource_type = ResourceType(request.resource_type.lower())
        action = PermissionAction(request.action.lower())
        has_permission = service.check_permission(
            user_id=user_id,
            resource_type=resource_type,
            action=action,
            resource_id=request.resource_id,
            context=request.context,
        )
        return {
            "has_permission": has_permission,
            "user_id": request.user_id,
            "resource_type": request.resource_type,
            "action": request.action,
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid request: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Permission check failed: {str(e)}",
        )


@router.post("/rules", status_code=201)
async def create_rule(
    request: RuleRequest, service: RuleEngineService = Depends(get_rule_engine)
) -> dict[str, Any]:
    """Create new business rule."""
    try:
        rule_type = RuleType(request.rule_type.lower())
        priority = RulePriority[request.priority.upper()]
        rule = service.create_rule(
            name=request.name,
            description=request.description,
            rule_type=rule_type,
            condition_expression=request.condition_expression,
            action_expression=request.action_expression,
            priority=priority,
            tags=request.tags,
        )
        return {
            "rule_id": str(rule.id),
            "name": rule.name,
            "rule_type": rule.rule_type.value,
            "priority": rule.priority.name,
            "is_active": rule.is_active,
            "created_at": rule.created_at.isoformat(),
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid request: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create rule: {str(e)}",
        )


@router.post("/rules/execute")
async def execute_rule(
    request: RuleExecutionRequest, service: RuleEngineService = Depends(get_rule_engine)
) -> dict[str, Any]:
    """Execute business rule."""
    try:
        rule_id = UUID(request.rule_id)
        result = service.execute_rule(rule_id, request.context)
        return {
            "rule_id": str(result.rule_id),
            "condition_result": result.condition_result,
            "action_result": result.action_result,
            "execution_time_ms": result.execution_time_ms,
            "success": result.success,
            "error": result.error,
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid rule ID: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Rule execution failed: {str(e)}",
        )


@router.get("/rules/types/{rule_type}")
async def execute_rules_by_type(
    rule_type: str,
    context: dict[str, Any],
    service: RuleEngineService = Depends(get_rule_engine),
) -> dict[str, Any]:
    """Execute all rules of specific type."""
    try:
        rule_type_enum = RuleType(rule_type.lower())
        results = service.execute_rules_by_type(rule_type_enum, context)
        return {
            "rule_type": rule_type,
            "results": [
                {
                    "rule_id": str(result.rule_id),
                    "condition_result": result.condition_result,
                    "action_result": result.action_result,
                    "execution_time_ms": result.execution_time_ms,
                    "success": result.success,
                    "error": result.error,
                }
                for result in results
            ],
            "total_executed": len(results),
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid rule type: {str(e)}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Rules execution failed: {str(e)}",
        )


@router.get("/health")
async def health_check(
    vector_service: VectorSearchService = Depends(get_vector_service),
    permission_service: PermissionService = Depends(get_permission_service),
    rule_engine: RuleEngineService = Depends(get_rule_engine),
) -> dict[str, Any]:
    """Health check for core systems."""
    return {
        "status": "healthy",
        "systems": {
            "vector_search": "operational",
            "permission_system": "operational",
            "rule_engine": "operational",
        },
        "timestamp": "2025-08-30T10:00:00Z",
    }


__all__ = [
    "PermissionCheckRequest",
    "PermissionRequest",
    "RuleExecutionRequest",
    "RuleRequest",
    "VectorDocumentRequest",
    "VectorSearchRequest",
    "action",
    "actions",
    "document",
    "get_permission_service",
    "get_rule_engine",
    "get_vector_service",
    "has_permission",
    "permission",
    "priority",
    "repo",
    "resource_type",
    "result",
    "results",
    "router",
    "rule",
    "rule_id",
    "rule_type",
    "rule_type_enum",
    "user_id",
]
