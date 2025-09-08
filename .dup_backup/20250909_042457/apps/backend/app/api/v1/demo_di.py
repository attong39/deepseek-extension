import Exception
import agent
import agent_data
import agent_id
import agent_repository
import agent_service
import container
import dict
import dir
import e
import hasattr
import len
import list
import method
import pagination
import service_health
import session
import str
import type
import user
import user_id
import user_repository
import user_service
# zeta_vn/app/api/v1/demo_di.py

"""

Demo Router with Advanced DI Integration for ZETA AI Server

Author: Duy BG VN



🎯 DEMONSTRATION ENDPOINTS:

- Complete DI container integration

- Repository & service injection

- Authentication & authorization

- Request scoping

- Health checks

- Error handling patterns

"""

from typing import Any

from apps.backend.app.dependencies import (
    AgentRepositoryDep,
    AgentService,
    Container,
    CurrentUserId,
    DatabaseSession,
    OptionalUserId,
    PaginationParams,
    UserRepositoryDep,
    UserService,
    validate_user_access,
)
from fastapi import APIRouter, HTTPException, status

router = APIRouter(prefix="/demo", tags=["Demo DI System"])


@router.get("/health", response_model=dict[str, Any])
async def check_di_health(container: Container) -> dict[str, Any]:
    """

    Check health of all DI-managed services.



    Returns:

        Dict[str, Any]: Health status of all services

    """

    try:
        health_results = await container.health_check_all()

        overall_status = "healthy"

        for service_health in health_results.values():
            if service_health.get("status") != "healthy":
                overall_status = "degraded"

                break

        return {
            "status": overall_status,
            "timestamp": "2024-01-01T00:00:00Z",  # In real app, use datetime.utcnow()
            "services": health_results,
            "di_container": {
                "status": "healthy",
                "registered_services": len(container._singletons)
                + len(container._factories),
            },
        }

    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": "2024-01-01T00:00:00Z",
        }


@router.get("/auth/profile")
async def get_user_profile(
    user_id: CurrentUserId, user_service: UserService
) -> dict[str, Any]:
    """

    Get current user profile using DI-injected service.



    Args:

        user_id: Current authenticated user ID

        user_service: Injected user service



    Returns:

        Dict[str, Any]: User profile information

    """

    try:
        _ = await user_service.get_user(user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        return {
            "user": user,
            "authenticated": True,
            "injection_type": type(user_service).__name__,
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get user profile: {e}",
        )


@router.get("/auth/optional")
async def get_optional_profile(
    user_id: OptionalUserId, user_service: UserService
) -> dict[str, Any]:
    """

    Get profile information with optional authentication.



    Args:

        user_id: Optional user ID (None if not authenticated)

        user_service: Injected user service



    Returns:

        Dict[str, Any]: Profile or public information

    """

    if user_id:
        try:
            _ = await user_service.get_user(user_id)

            return {
                "authenticated": True,
                "user": user,
                "message": "Authenticated user profile",
            }

        except Exception as e:
            return {
                "authenticated": True,
                "error": f"Failed to load profile: {e}",
                "message": "Authentication valid but profile unavailable",
            }

    return {
        "authenticated": False,
        "message": "Public access - no authentication provided",
        "public_info": {
            "app_name": "ZETA AI Server",
            "version": "2.0.0",
            "features": ["DI Container", "Authentication", "Service Layer"],
        },
    }


@router.get("/agents")
async def list_user_agents(
    user_id: CurrentUserId, agent_service: AgentService, pagination: PaginationParams
) -> dict[str, Any]:
    """

    List agents owned by current user with pagination.



    Args:

        user_id: Current authenticated user ID

        agent_service: Injected agent service

        pagination: Pagination parameters



    Returns:

        Dict[str, Any]: List of user's agents

    """

    try:
        agents = await agent_service.list_user_agents(user_id)

        # Apply pagination

        skip = pagination["skip"]

        limit = pagination["limit"]

        total = len(agents) if agents else 0

        paginated_agents = agents[skip : skip + limit] if agents else []

        return {
            "agents": paginated_agents,
            "pagination": {
                "skip": skip,
                "limit": limit,
                "total": total,
                "returned": len(paginated_agents),
            },
            "owner_id": user_id,
            "service_type": type(agent_service).__name__,
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list agents: {e}",
        )


@router.post("/agents")
async def create_agent(
    user_id: CurrentUserId, agent_service: AgentService, agent_data: dict[str, Any]
) -> dict[str, Any]:
    """

    Create a new agent using DI-injected service.



    Args:

        user_id: Current authenticated user ID

        agent_service: Injected agent service

        agent_data: Agent creation data



    Returns:

        Dict[str, Any]: Created agent information

    """

    try:
        # Add owner information

        agent_data["owner_id"] = user_id

        agent_data["status"] = agent_data.get("status", "active")

        _ = await agent_service.create_agent(agent_data)

        return {
            "agent": agent,
            "message": "Agent created successfully",
            "service_type": type(agent_service).__name__,
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create agent: {e}",
        )


@router.get("/agents/{agent_id}")
async def get_agent(
    agent_id: str, user_id: CurrentUserId, agent_service: AgentService
) -> dict[str, Any]:
    """

    Get specific agent with access validation.



    Args:

        agent_id: Agent ID to retrieve

        user_id: Current authenticated user ID

        agent_service: Injected agent service



    Returns:

        Dict[str, Any]: Agent information

    """

    try:
        _ = await agent_service.get_agent(agent_id)

        if not agent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Agent not found"
            )

        # Validate user access

        validate_user_access(user_id, agent.get("owner_id", ""))

        return {
            "agent": agent,
            "access_validated": True,
            "service_type": type(agent_service).__name__,
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get agent: {e}",
        )


@router.get("/repositories/info")
async def get_repository_info(
    user_repository: UserRepositoryDep, agent_repository: AgentRepositoryDep
) -> dict[str, Any]:
    """

    Get information about injected repositories.



    Args:

        user_repository: Injected user repository

        agent_repository: Injected agent repository



    Returns:

        Dict[str, Any]: Repository type information

    """

    return {
        "repositories": {
            "user_repository": {
                "type": type(user_repository).__name__,
                "module": type(user_repository).__module__,
                "available_methods": [
                    method
                    for method in dir(user_repository)
                    if not method.startswith("_")
                ][:5],  # First 5 methods only
            },
            "agent_repository": {
                "type": type(agent_repository).__name__,
                "module": type(agent_repository).__module__,
                "available_methods": [
                    method
                    for method in dir(agent_repository)
                    if not method.startswith("_")
                ][:5],  # First 5 methods only
            },
        },
        "injection_successful": True,
        "message": "Repository DI working correctly",
    }


@router.get("/database/info")
async def get_database_info(session: DatabaseSession) -> dict[str, Any]:
    """

    Get database session information.



    Args:

        session: Injected database session



    Returns:

        Dict[str, Any]: Database session information

    """

    return {
        "database": {
            "session_type": type(session).__name__,
            "session_module": type(session).__module__,
            "is_async": hasattr(session, "execute"),
            "connection_available": session is not None,
        },
        "injection_successful": True,
        "message": "Database session DI working correctly",
    }


@router.get("/container/status")
async def get_container_status(container: Container) -> dict[str, Any]:
    """

    Get detailed DI container status.



    Args:

        container: Injected DI container



    Returns:

        Dict[str, Any]: Container status and statistics

    """

    return {
        "container": {
            "type": type(container).__name__,
            "singletons_count": len(container._singletons),
            "factories_count": len(container._factories),
            "transient_factories_count": len(container._transient_factories),
            "scoped_factories_count": len(container._scoped_factories),
            "lifecycle_services_count": len(container._lifecycle_services),
        },
        "registered_services": {
            "singletons": list(container._singletons.keys()),
            "factories": list(container._factories.keys()),
            "transient": list(container._transient_factories.keys()),
            "scoped": list(container._scoped_factories.keys()),
            "lifecycle": list(container._lifecycle_services.keys()),
        },
        "dependency_graph": container._dependency_graph,
        "message": "DI container status retrieved successfully",
    }


@router.post("/demo/error")
async def trigger_error() -> None:
    """

    Endpoint to test error handling in DI system.



    Raises:

        HTTPException: Always raises an error for testing

    """

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="This is a demo error to test DI error handling",
    )


@router.get("/")
async def demo_home() -> dict[str, Any]:
    """

    Demo home endpoint showing DI capabilities.



    Returns:

        Dict[str, Any]: Demo information and available endpoints

    """

    return {
        "message": "ZETA AI Server - Advanced DI Demo",
        "version": "2.0.0",
        "features": [
            "Dependency Injection Container",
            "Service Registration & Resolution",
            "Request Scoping",
            "Lifecycle Management",
            "Health Monitoring",
            "Type-Safe Dependencies",
        ],
        "endpoints": {
            "GET /demo/": "This endpoint",
            "GET /demo/health": "DI services health check",
            "GET /demo/auth/profile": "Authenticated user profile",
            "GET /demo/auth/optional": "Optional authentication demo",
            "GET /demo/agents": "List user agents with pagination",
            "POST /demo/agents": "Create new agent",
            "GET /demo/agents/{agent_id}": "Get specific agent",
            "GET /demo/repositories/info": "Repository injection info",
            "GET /demo/database/info": "Database session info",
            "GET /demo/container/status": "DI container status",
            "POST /demo/error": "Error handling demo",
        },
        "authentication": {
            "required": ["/demo/auth/profile", "/demo/agents/*"],
            "optional": ["/demo/auth/optional"],
            "none": [
                "/demo/",
                "/demo/health",
                "/demo/repositories/info",
                "/demo/database/info",
                "/demo/container/status",
            ],
        },
        "instructions": {
            "authentication": "Use 'Bearer test' header for demo authentication",
            "pagination": "Use ?skip=0&limit=10 for pagination",
            "errors": "All endpoints include proper error handling",
        },
    }
