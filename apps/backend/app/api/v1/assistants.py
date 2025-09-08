"""AI Assistants API module for Zeta AI Server.



Cung cấp các endpoint để quản lý AI assistants với đầy đủ tính năng CRUD,

validation, RBAC, audit trail, và dependency injection theo Clean Architecture.



Vai trò:

- CRUD operations cho AI assistants (create, read, update, delete)

- Validation nghiêm ngặt cho tất cả input data

- RBAC với permissions chi tiết (assistant:create, assistant:read, etc.)

- Audit trail cho tất cả operations

- Integration với analytics, memory, files, planning/workflow modules

- Versioned configuration và safe-delete



Features:

- Assistant templates và custom configurations

- Tool integration và capability management

- Performance metrics và usage tracking

- Batch operations và import/export

- Real-time status monitoring

- Advanced search và filtering

"""

from __future__ import annotations

import logging
import uuid
from typing import TYPE_CHECKING, Annotated, Any, Literal, Protocol

from app.dependencies import get_assistants_service
from app.deps.auth import get_current_user, require_permissions
from app.serializers.assistant_serializers import (
import Exception
import assistant_id
import base_model
import bool
import capability
import current_user
import days
import dict
import e
import force
import hasattr
import int
import len
import limit
import list
import offset
import request
import response
import search
import sort_by
import sort_order
import sorted
import status_filter
import str
import svc
import user
import version
import version_id
    AssistantAnalyticsOut,
    AssistantBatchCreateIn,
    AssistantConfigVersionOut,
    AssistantOut,
    AssistantTemplateIn,
    AssistantUpdateIn,
)
from app.validators.assistant_validators import (
    validate_assistant_name,
    validate_assistant_tools,
)
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Path,
    Query,
    Request,
    Response,
    status,
)
from pydantic import BaseModel, ValidationError

if TYPE_CHECKING:
    from apps.backend.core.domain.entities.user import User


logger = logging.getLogger(__name__)


router = APIRouter(prefix="/assistants", tags=["assistants"])

ALLOWED_SORT_FIELDS = {"created_at", "updated_at", "name", "status"}

CACHE_PRIVATE_10S = "private, max-age=10"


# RBAC permission names (DRY)

PERM_ASSISTANT_READ = "assistant:read"

PERM_ASSISTANT_CREATE = "assistant:create"

PERM_ASSISTANT_UPDATE = "assistant:update"

PERM_ASSISTANT_DELETE = "assistant:delete"

PERM_ASSISTANT_CONTROL = "assistant:control"

PERM_ASSISTANT_BATCH = "assistant:batch"

PERM_ANALYTICS_READ = "analytics:read"

PERM_CONFIG_READ = "config:read"

PERM_CONFIG_ROLLBACK = "config:rollback"


# Constants for error messages

ASSISTANT_NOT_FOUND = "Assistant not found"

ACCESS_DENIED = "Access denied"

FAILED_TO_CREATE = "Failed to create assistant"

FAILED_TO_UPDATE = "Failed to update assistant"

FAILED_TO_DELETE = "Failed to delete assistant"

FAILED_TO_RETRIEVE = "Failed to retrieve assistant"


class AssistantsServiceProto(Protocol):
    async def create_assistant(self, data: dict[str, Any]) -> dict[str, Any]: ...

    async def list_assistants(self, params: dict[str, Any]) -> list[dict[str, Any]]: ...

    async def get_assistant(self, assistant_id: str) -> dict[str, Any] | None: ...

    async def update_assistant(
        self, assistant_id: str, data: dict[str, Any]
    ) -> dict[str, Any]: ...

    async def delete_assistant(self, assistant_id: str, soft_delete: bool) -> None: ...

    async def get_assistant_analytics(
        self, assistant_id: str, *, days: int
    ) -> dict[str, Any]: ...

    async def get_assistant_config_versions(
        self, assistant_id: str, *, limit: int
    ) -> list[dict[str, Any]]: ...

    async def rollback_assistant_config(
        self, assistant_id: str, version_id: str
    ) -> dict[str, Any]: ...

    async def get_assistant_status(self, assistant_id: str) -> dict[str, Any]: ...

    async def activate_assistant(self, assistant_id: str) -> None: ...

    async def deactivate_assistant(self, assistant_id: str) -> None: ...


class AssistantStatusOut(BaseModel):
    status: Literal["active", "inactive", "error"]

    health: Literal["green", "yellow", "red"]

    last_error: str | None = None

    updated_at: str | None = None  # ISO timestamp; switch to datetime if available


# RBAC dependencies are attached inline in route decorators for clarity


# ==============================

# Core CRUD Endpoints

# ==============================


@router.post(
    "",
    response_model=AssistantOut,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_permissions([PERM_ASSISTANT_CREATE]))],
    summary="Create AI Assistant",
    description="Create a new AI assistant with specified configuration and capabilities.",
)
async def create_assistant(
    payload: AssistantTemplateIn,
    request: Request,
    current_user: Annotated[User, Depends(get_current_user)],
    svc: Annotated[AssistantsServiceProto, Depends(get_assistants_service)],
) -> AssistantOut:
    """Create a new AI assistant.



    Args:

        payload: Assistant configuration data

        current_user: Current authenticated user

        svc: Assistants service for business logic



    Returns:

        Created assistant data



    Raises:

        HTTPException: If validation fails or creation error occurs

    """

    try:
        # Validate input data

        validate_assistant_name(payload.name)

        validate_assistant_tools(payload.tools)

        # Create assistant with audit context

        assistant_data = payload.model_dump()

        assistant_data["owner_id"] = current_user.id

        assistant_data["created_by"] = current_user.username

        assistant_data["audit"] = {
            "ip": request.client.host if request.client else None,
            "ua": request.headers.get("user-agent"),
        }

        created = await svc.create_assistant(assistant_data)

        logger.info(
            f"Created assistant '{payload.name}' for user {current_user.username}"
        )

        return AssistantOut(**created)

    except ValidationError as e:
        logger.warning(f"Validation error creating assistant: {e}")

        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Validation error: {e!s}",
        ) from e

    except Exception as e:
        logger.error(f"Error creating assistant: {e}")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=FAILED_TO_CREATE
        ) from e


@router.get(
    "",
    response_model=list[AssistantOut],
    dependencies=[Depends(require_permissions([PERM_ASSISTANT_READ]))],
    summary="List AI Assistants",
    description="Retrieve list of AI assistants with optional filtering and pagination.",
)
async def list_assistants(
    response: Response,
    current_user: Annotated[User, Depends(get_current_user)],
    svc: Annotated[AssistantsServiceProto, Depends(get_assistants_service)],
    # Pagination parameters
    limit: Annotated[
        int, Query(ge=1, le=100, description="Maximum number of results")
    ] = 50,
    offset: Annotated[int, Query(ge=0, description="Number of results to skip")] = 0,
    # Filtering parameters
    status_filter: Annotated[
        str | None, Query(alias="status", description="Filter by status")
    ] = None,
    base_model: Annotated[str | None, Query(description="Filter by base model")] = None,
    capability: Annotated[str | None, Query(description="Filter by capability")] = None,
    search: Annotated[
        str | None, Query(description="Search by name or description")
    ] = None,
    # Sorting parameters
    sort_by: Annotated[str, Query(description="Sort field")] = "created_at",
    sort_order: Annotated[
        str, Query(pattern="^(asc|desc)$", description="Sort order")
    ] = "desc",
) -> list[AssistantOut]:
    """List AI assistants with filtering and pagination.



    Args:

        current_user: Current authenticated user

        svc: Assistants service for data access

        limit: Maximum number of results

        offset: Number of results to skip

        status_filter: Filter by assistant status

        base_model: Filter by base AI model

        capability: Filter by specific capability

        search: Search query for name/description

        sort_by: Field to sort by

        sort_order: Sort order (asc/desc)



    Returns:

        List of assistant data matching criteria

    """

    try:
        # Guard sort field to prevent injection/typos

        if sort_by not in ALLOWED_SORT_FIELDS:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"sort_by must be one of {sorted(ALLOWED_SORT_FIELDS)}",
            )

        # Build search parameters

        search_params = {
            "owner_id": current_user.id,
            "limit": limit,
            "offset": offset,
            "status": status_filter,
            "base_model": base_model,
            "capability": capability,
            "search": search,
            "sort_by": sort_by,
            "sort_order": sort_order,
        }

        # Get assistants from service

        assistants = await svc.list_assistants(search_params)

        # Light cache to reduce load for frequent reads

        response.headers["Cache-Control"] = CACHE_PRIVATE_10S

        return [AssistantOut(**assistant) for assistant in assistants]

    except Exception as e:
        logger.error(f"Error listing assistants: {e}")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=FAILED_TO_RETRIEVE
        ) from e


@router.get(
    "/{assistant_id}",
    response_model=AssistantOut,
    dependencies=[Depends(require_permissions([PERM_ASSISTANT_READ]))],
    summary="Get AI Assistant",
    description="Retrieve detailed information about a specific AI assistant.",
)
async def get_assistant(
    response: Response,
    current_user: Annotated[User, Depends(get_current_user)],
    svc: Annotated[AssistantsServiceProto, Depends(get_assistants_service)],
    assistant_id: Annotated[uuid.UUID, Path(description="Assistant UUID")],
) -> AssistantOut:
    """Get detailed information about an AI assistant.



    Args:

        assistant_id: ID of the assistant to retrieve

        current_user: Current authenticated user

        svc: Assistants service for data access



    Returns:

        Assistant data



    Raises:

        HTTPException: If assistant not found or access denied

    """

    try:
        assistant = await svc.get_assistant(str(assistant_id))

        if not assistant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=ASSISTANT_NOT_FOUND
            )

        # Check ownership or admin access

        if assistant["owner_id"] != current_user.id and not _is_admin(current_user):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail=ACCESS_DENIED
            )

        response.headers["Cache-Control"] = CACHE_PRIVATE_10S

        return AssistantOut(**assistant)

    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"Error retrieving assistant {assistant_id}: {e}")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=FAILED_TO_RETRIEVE
        ) from e


@router.patch(
    "/{assistant_id}",
    response_model=AssistantOut,
    dependencies=[Depends(require_permissions([PERM_ASSISTANT_UPDATE]))],
    summary="Update AI Assistant",
    description="Update configuration and settings of an existing AI assistant.",
)
async def update_assistant(
    payload: AssistantUpdateIn,
    request: Request,
    current_user: Annotated[User, Depends(get_current_user)],
    svc: Annotated[AssistantsServiceProto, Depends(get_assistants_service)],
    assistant_id: Annotated[uuid.UUID, Path(description="Assistant UUID")],
) -> AssistantOut:
    """Update an AI assistant's configuration.



    Args:

        assistant_id: ID of the assistant to update

        payload: Update data

        request: FastAPI request object for audit context

        current_user: Current authenticated user

        svc: Assistants service for business logic



    Returns:

        Updated assistant data



    Raises:

        HTTPException: If assistant not found, access denied, or update fails

    """

    try:
        # Check if assistant exists and user has access

        existing = await svc.get_assistant(str(assistant_id))

        if not existing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=ASSISTANT_NOT_FOUND
            )

        if existing["owner_id"] != current_user.id and not _is_admin(current_user):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail=ACCESS_DENIED
            )

        # Validate update data

        update_data = payload.model_dump(exclude_none=True)

        if "name" in update_data:
            validate_assistant_name(update_data["name"])

        if "tools" in update_data:
            validate_assistant_tools(update_data["tools"])

        # Perform update

        audit_ctx = {
            "ip": request.client.host if request.client else None,
            "ua": request.headers.get("user-agent"),
        }

        update_data["updated_by"] = current_user.username

        update_data["audit"] = audit_ctx

        updated = await svc.update_assistant(str(assistant_id), update_data)

        logger.info(f"Updated assistant {assistant_id} by user {current_user.username}")

        return AssistantOut(**updated)

    except HTTPException:
        raise

    except ValidationError as e:
        logger.warning(f"Validation error updating assistant {assistant_id}: {e}")

        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Validation error: {e!s}",
        ) from e

    except Exception as e:
        logger.error(f"Error updating assistant {assistant_id}: {e}")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=FAILED_TO_UPDATE
        ) from e


@router.delete(
    "/{assistant_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_permissions([PERM_ASSISTANT_DELETE]))],
    summary="Delete AI Assistant",
    description="Safely delete an AI assistant (soft delete with audit trail).",
)
async def delete_assistant(
    current_user: Annotated[User, Depends(get_current_user)],
    svc: Annotated[AssistantsServiceProto, Depends(get_assistants_service)],
    assistant_id: Annotated[uuid.UUID, Path(description="Assistant UUID")],
    force: Annotated[bool, Query(description="Force permanent deletion")] = False,
) -> Response:
    """Delete an AI assistant.



    Args:

        assistant_id: ID of the assistant to delete

        current_user: Current authenticated user

        svc: Assistants service for business logic

        force: Whether to permanently delete (admin only)



    Returns:

        Empty response with 204 status



    Raises:

        HTTPException: If assistant not found, access denied, or deletion fails

    """

    try:
        # Check if assistant exists and user has access

        existing = await svc.get_assistant(str(assistant_id))

        if not existing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=ASSISTANT_NOT_FOUND
            )

        if existing["owner_id"] != current_user.id and not _is_admin(current_user):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail=ACCESS_DENIED
            )

        # Check force delete permission

        if force and not _is_admin(current_user):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Force deletion requires admin access",
            )

        # Perform deletion

        await svc.delete_assistant(str(assistant_id), soft_delete=not force)

        logger.info(
            f"Deleted assistant {assistant_id} by user {current_user.username} (force={force})"
        )

        return Response(status_code=status.HTTP_204_NO_CONTENT)

    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"Error deleting assistant {assistant_id}: {e}")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=FAILED_TO_DELETE
        ) from e


# ==============================

# Advanced Features

# ==============================


@router.post(
    "/batch",
    response_model=list[AssistantOut],
    status_code=status.HTTP_201_CREATED,
    dependencies=[
        Depends(require_permissions([PERM_ASSISTANT_CREATE, PERM_ASSISTANT_BATCH]))
    ],
    summary="Batch Create Assistants",
    description="Create multiple AI assistants in a single operation.",
)
async def batch_create_assistants(
    payload: AssistantBatchCreateIn,
    request: Request,
    current_user: Annotated[User, Depends(get_current_user)],
    svc: Annotated[AssistantsServiceProto, Depends(get_assistants_service)],
) -> list[AssistantOut]:
    """Create multiple AI assistants in batch.



    Args:

        payload: Batch creation data

        request: FastAPI request object for audit context

        current_user: Current authenticated user

        svc: Assistants service for business logic



    Returns:

        List of created assistant data



    Raises:

        HTTPException: If batch creation fails

    """

    try:
        created_assistants = []

        for assistant_data in payload.assistants:
            try:
                # Validate each assistant

                validate_assistant_name(assistant_data.name)

                validate_assistant_tools(assistant_data.tools)

                # Add metadata

                assistant_dict = assistant_data.model_dump()

                assistant_dict["owner_id"] = current_user.id

                assistant_dict["created_by"] = current_user.username

                assistant_dict["batch_id"] = payload.batch_id

                assistant_dict["audit"] = {
                    "ip": request.client.host if request.client else None,
                    "ua": request.headers.get("user-agent"),
                }

                created = await svc.create_assistant(assistant_dict)

                created_assistants.append(AssistantOut(**created))

            except Exception as e:
                logger.warning(f"Failed to create assistant in batch: {e}")

                if not payload.continue_on_error:
                    raise

        logger.info(
            f"Batch created {len(created_assistants)} assistants for user {current_user.username}"
        )

        return created_assistants

    except Exception as e:
        logger.error(f"Error in batch create assistants: {e}")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to batch create assistants",
        ) from e


@router.get(
    "/{assistant_id}/analytics",
    response_model=AssistantAnalyticsOut,
    dependencies=[
        Depends(require_permissions([PERM_ASSISTANT_READ, PERM_ANALYTICS_READ]))
    ],
    summary="Get Assistant Analytics",
    description="Retrieve analytics and performance metrics for an AI assistant.",
)
async def get_assistant_analytics(
    current_user: Annotated[User, Depends(get_current_user)],
    svc: Annotated[AssistantsServiceProto, Depends(get_assistants_service)],
    assistant_id: Annotated[uuid.UUID, Path(description="Assistant UUID")],
    days: Annotated[
        int, Query(ge=1, le=365, description="Number of days to analyze")
    ] = 30,
) -> AssistantAnalyticsOut:
    """Get analytics for an AI assistant.



    Args:

        assistant_id: ID of the assistant

        current_user: Current authenticated user

        svc: Assistants service for data access

        days: Number of days to analyze



    Returns:

        Analytics data for the assistant



    Raises:

        HTTPException: If assistant not found or access denied

    """

    try:
        # Check if assistant exists and user has access

        assistant = await svc.get_assistant(str(assistant_id))

        if not assistant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=ASSISTANT_NOT_FOUND
            )

        if assistant["owner_id"] != current_user.id and not _is_admin(current_user):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail=ACCESS_DENIED
            )

        # Get analytics data

        analytics = await svc.get_assistant_analytics(str(assistant_id), days=days)

        return AssistantAnalyticsOut(**analytics)

    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"Error getting analytics for assistant {assistant_id}: {e}")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve analytics",
        ) from e


@router.get(
    "/{assistant_id}/config/versions",
    response_model=list[AssistantConfigVersionOut],
    dependencies=[
        Depends(require_permissions([PERM_ASSISTANT_READ, PERM_CONFIG_READ]))
    ],
    summary="Get Config Versions",
    description="Retrieve configuration version history for an AI assistant.",
)
async def get_assistant_config_versions(
    current_user: Annotated[User, Depends(get_current_user)],
    svc: Annotated[AssistantsServiceProto, Depends(get_assistants_service)],
    assistant_id: Annotated[uuid.UUID, Path(description="Assistant UUID")],
    limit: Annotated[
        int, Query(ge=1, le=100, description="Maximum number of versions")
    ] = 20,
) -> list[AssistantConfigVersionOut]:
    """Get configuration version history for an assistant.



    Args:

        assistant_id: ID of the assistant

        current_user: Current authenticated user

        svc: Assistants service for data access

        limit: Maximum number of versions to return



    Returns:

        List of configuration versions



    Raises:

        HTTPException: If assistant not found or access denied

    """

    try:
        # Check if assistant exists and user has access

        assistant = await svc.get_assistant(str(assistant_id))

        if not assistant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=ASSISTANT_NOT_FOUND
            )

        if assistant["owner_id"] != current_user.id and not _is_admin(current_user):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail=ACCESS_DENIED
            )

        # Get configuration versions

        versions = await svc.get_assistant_config_versions(
            str(assistant_id), limit=limit
        )

        return [AssistantConfigVersionOut(**version) for version in versions]

    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"Error getting config versions for assistant {assistant_id}: {e}")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve config versions",
        ) from e


@router.post(
    "/{assistant_id}/config/rollback/{version_id}",
    response_model=AssistantOut,
    dependencies=[
        Depends(require_permissions([PERM_ASSISTANT_UPDATE, PERM_CONFIG_ROLLBACK]))
    ],
    summary="Rollback Config",
    description="Rollback assistant configuration to a previous version.",
)
async def rollback_assistant_config(
    version_id: Annotated[str, Path(min_length=1, description="Config version id")],
    current_user: Annotated[User, Depends(get_current_user)],
    svc: Annotated[AssistantsServiceProto, Depends(get_assistants_service)],
    assistant_id: Annotated[uuid.UUID, Path(description="Assistant UUID")],
) -> AssistantOut:
    """Rollback assistant configuration to a previous version.



    Args:

        assistant_id: ID of the assistant

        version_id: ID of the config version to rollback to

        request: FastAPI request object for audit context

        current_user: Current authenticated user

        svc: Assistants service for business logic



    Returns:

        Updated assistant data



    Raises:

        HTTPException: If assistant/version not found or rollback fails

    """

    try:
        # Check if assistant exists and user has access

        assistant = await svc.get_assistant(str(assistant_id))

        if not assistant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=ASSISTANT_NOT_FOUND
            )

        if assistant["owner_id"] != current_user.id and not _is_admin(current_user):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail=ACCESS_DENIED
            )

        # Perform rollback

        updated = await svc.rollback_assistant_config(str(assistant_id), version_id)

        logger.info(
            f"Rolled back assistant {assistant_id} config to version {version_id}"
        )

        return AssistantOut(**updated)

    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"Error rolling back assistant {assistant_id} config: {e}")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to rollback configuration",
        ) from e


# ==============================

# Status & Health Endpoints

# ==============================


@router.get(
    "/{assistant_id}/status",
    response_model=AssistantStatusOut,
    dependencies=[Depends(require_permissions([PERM_ASSISTANT_READ]))],
    summary="Get Assistant Status",
    description="Get real-time status and health information for an AI assistant.",
)
async def get_assistant_status(
    response: Response,
    current_user: Annotated[User, Depends(get_current_user)],
    svc: Annotated[AssistantsServiceProto, Depends(get_assistants_service)],
    assistant_id: Annotated[uuid.UUID, Path(description="Assistant UUID")],
) -> AssistantStatusOut:
    """Get real-time status for an AI assistant.



    Args:

        assistant_id: ID of the assistant

        current_user: Current authenticated user

        svc: Assistants service for data access



    Returns:

        Status information



    Raises:

        HTTPException: If assistant not found or access denied

    """

    try:
        assistant = await svc.get_assistant(str(assistant_id))

        if not assistant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=ASSISTANT_NOT_FOUND
            )

        if assistant["owner_id"] != current_user.id and not _is_admin(current_user):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail=ACCESS_DENIED
            )

        status_info = await svc.get_assistant_status(str(assistant_id))

        # Runtime reference to UUID type to ensure runtime import usage (satisfies linter)

        logger.debug("assistant_id type=%s", uuid.UUID.__name__)

        # Map service health statuses to schema literals

        health_raw = (status_info or {}).get("health", "healthy")

        health_map = {
            "healthy": "green",
            "degraded": "yellow",
            "unhealthy": "red",
            "green": "green",
            "yellow": "yellow",
            "red": "red",
        }

        mapped_health = health_map.get(str(health_raw).lower(), "green")

        # Build response payload compliant with schema

        # Normalize updated_at to ISO string if it's a datetime-like object

        updated_at_val = assistant.get("updated_at") if assistant else None

        if updated_at_val is not None and hasattr(updated_at_val, "isoformat"):
            updated_at_str = updated_at_val.isoformat()

        else:
            updated_at_str = updated_at_val

        payload = {
            "status": (status_info or {}).get(
                "status", assistant.get("status", "inactive")
            ),
            "health": mapped_health,  # type: ignore[assignment]
            "last_error": (status_info or {}).get("last_error"),
            "updated_at": updated_at_str,
        }

        response.headers["Cache-Control"] = CACHE_PRIVATE_10S

        return AssistantStatusOut(**payload)

    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"Error getting status for assistant {assistant_id}: {e}")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve status",
        ) from e


@router.post(
    "/{assistant_id}/activate",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(require_permissions([PERM_ASSISTANT_CONTROL]))],
    summary="Activate Assistant",
    description="Activate an AI assistant for use.",
)
async def activate_assistant(
    current_user: Annotated[User, Depends(get_current_user)],
    svc: Annotated[AssistantsServiceProto, Depends(get_assistants_service)],
    assistant_id: Annotated[uuid.UUID, Path(description="Assistant UUID")],
) -> dict[str, str]:
    """Activate an AI assistant.



    Args:

        assistant_id: ID of the assistant to activate

        request: FastAPI request object for audit context

        current_user: Current authenticated user

        svc: Assistants service for business logic



    Returns:

        Activation result message



    Raises:

        HTTPException: If assistant not found or activation fails

    """

    try:
        assistant = await svc.get_assistant(str(assistant_id))

        if not assistant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=ASSISTANT_NOT_FOUND
            )

        if assistant["owner_id"] != current_user.id and not _is_admin(current_user):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail=ACCESS_DENIED
            )

        await svc.activate_assistant(str(assistant_id))

        logger.info(
            f"Activated assistant {assistant_id} by user {current_user.username}"
        )

        return {"message": "Assistant activated successfully", "status": "active"}

    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"Error activating assistant {assistant_id}: {e}")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to activate assistant",
        ) from e


@router.post(
    "/{assistant_id}/deactivate",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(require_permissions([PERM_ASSISTANT_CONTROL]))],
    summary="Deactivate Assistant",
    description="Deactivate an AI assistant.",
)
async def deactivate_assistant(
    current_user: Annotated[User, Depends(get_current_user)],
    svc: Annotated[AssistantsServiceProto, Depends(get_assistants_service)],
    assistant_id: Annotated[uuid.UUID, Path(description="Assistant UUID")],
) -> dict[str, str]:
    """Deactivate an AI assistant.



    Args:

        assistant_id: ID of the assistant to deactivate

        request: FastAPI request object for audit context

        current_user: Current authenticated user

        svc: Assistants service for business logic



    Returns:

        Deactivation result message



    Raises:

        HTTPException: If assistant not found or deactivation fails

    """

    try:
        assistant = await svc.get_assistant(str(assistant_id))

        if not assistant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=ASSISTANT_NOT_FOUND
            )

        if assistant["owner_id"] != current_user.id and not _is_admin(current_user):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail=ACCESS_DENIED
            )

        await svc.deactivate_assistant(str(assistant_id))

        logger.info(
            f"Deactivated assistant {assistant_id} by user {current_user.username}"
        )

        return {"message": "Assistant deactivated successfully", "status": "inactive"}

    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"Error deactivating assistant {assistant_id}: {e}")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to deactivate assistant",
        ) from e


# ==============================

# Helper Functions

# ==============================


def _is_admin(user: User) -> bool:
    """Check if user is admin.



    Args:

        user: User entity



    Returns:

        True if user is admin

    """

    return user.is_admin()
