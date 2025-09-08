from __future__ import annotations

import logging
from collections.abc import Awaitable, Callable
from functools import wraps
from time import perf_counter
from typing import Any, TypeVar
from uuid import UUID

import strawberry
from app.api.graphql.schema import (
import Exception
import RuntimeError
import agent_id
import arg
import args
import dict
import e
import float
import func
import func_name
import hasattr
import input
import int
import kwargs
import len
import limit
import list
import offset
import operation_name
import param_name
import permission
import required_permissions
import schema_class
import str
import target_ms
import ttl
import tuple
import type
    AgentType,
    CreateAgentInput,
    UpdateAgentInput,
)
from apps.backend.core.exceptions.validation_exceptions import ValidationError
from apps.backend.core.interfaces.cache import CacheManager
from apps.backend.core.performance.monitoring import PerformanceMonitor
from apps.backend.core.use_cases.agent.create_agent import CreateAgent
from apps.backend.core.use_cases.agent.get_agent import GetAgent
from apps.backend.core.use_cases.agent.update_agent import UpdateAgent
from fastapi import HTTPException

"""Enhanced GraphQL resolvers với performance optimization và clean code principles.
Author: duy_bg_vn
Focus: Production-ready resolvers với comprehensive monitoring, caching, và error handling.
"""
logger = logging.getLogger(__name__)
F = TypeVar("F", bound=Callable[..., Awaitable[Any]])


def performance_monitor(
    operation_name: str, target_ms: float = 100
) -> Callable[[F], F]:
    """Decorator để monitor performance của GraphQL resolvers.
    Args:
        operation_name: Tên operation để tracking
        target_ms: Target performance in milliseconds
    Raises:
        Warning log nếu vượt quá target performance
    """

    def decorator(func: F) -> F:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            start_time = perf_counter()
            operation_context = f"{operation_name}.{func.__name__}"
            try:
                result = await func(*args, **kwargs)
                duration_ms = (perf_counter() - start_time) * 1000
                if duration_ms > target_ms:
                    logger.warning(
                        f"Performance target exceeded: {operation_context} "
                        f"took {duration_ms:.2f}ms (target: {target_ms}ms)"
                    )
                else:
                    logger.debug(
                        f"Performance OK: {operation_context} took {duration_ms:.2f}ms"
                    )
                PerformanceMonitor.record_operation(
                    operation=operation_context, duration_ms=duration_ms, success=True
                )
                return result
            except Exception as e:
                duration_ms = (perf_counter() - start_time) * 1000
                PerformanceMonitor.record_operation(
                    operation=operation_context,
                    duration_ms=duration_ms,
                    success=False,
                    error_type=type(e).__name__,
                )
                logger.error(
                    f"Operation failed: {operation_context} after {duration_ms:.2f}ms: {e}"
                )
                raise

        return wrapper  # type: ignore

    return decorator


def cache_result(ttl: int = 300, vary_by: list[str] | None = None) -> Callable[[F], F]:
    """Decorator để cache kết quả GraphQL resolvers.
    Args:
        ttl: Time to live in seconds
        vary_by: List of parameter names để vary cache key
    """
    if vary_by is None:
        vary_by = []

    def decorator(func: F) -> F:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            cache_key_parts = [func.__name__]
            for param_name in vary_by:
                if param_name in kwargs:
                    cache_key_parts.append(f"{param_name}:{kwargs[param_name]}")
            cache_key = ":".join(cache_key_parts)
            cache_manager = CacheManager.get_instance()
            cached_result = await cache_manager.get(cache_key)
            if cached_result is not None:
                logger.debug(f"Cache hit for {cache_key}")
                return cached_result
            result = await func(*args, **kwargs)
            await cache_manager.set(cache_key, result, ttl=ttl)
            logger.debug(f"Cache miss for {cache_key}, result cached")
            return result

        return wrapper  # type: ignore

    return decorator


def security_check(required_permissions: list[str]) -> Callable[[F], F]:
    """Decorator để validate permissions cho GraphQL resolvers.
    Args:
        required_permissions: List of required permissions
    """

    def decorator(func: F) -> F:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            info = None
            for arg in args:
                if hasattr(arg, "context"):
                    info = arg
                    break
            if not info or not hasattr(info, "context"):
                raise HTTPException(
                    status_code=401, detail="Authentication context missing"
                )
            security_context = info.context.get("security_context")
            if not security_context:
                raise HTTPException(status_code=401, detail="Security context missing")
            for permission in required_permissions:
                if not security_context.has_permission(permission):
                    logger.warning(
                        f"Permission denied: {security_context.user_id} "
                        f"lacks {permission} for {func.__name__}"
                    )
                    raise HTTPException(
                        status_code=403,
                        detail=f"Permission denied: {permission} required",
                    )
            return await func(*args, **kwargs)

        return wrapper  # type: ignore

    return decorator


def validate_input(schema_class: type) -> Callable[[F], F]:
    """Decorator để validate input data cho GraphQL resolvers.
    Args:
        schema_class: Pydantic schema class for validation
    """

    def decorator(func: F) -> F:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            input_data = _extract_input_data(args, kwargs)
            if input_data is None:
                raise ValidationError("Input data missing for validation")
            _validate_with_schema(input_data, schema_class, func.__name__)
            return await func(*args, **kwargs)

        return wrapper  # type: ignore

    return decorator


def _extract_input_data(args: tuple[Any, ...], kwargs: dict[str, Any]) -> Any:
    """Extract input data from function arguments."""
    input_data = kwargs.get("input")
    if input_data is not None:
        return input_data
    for arg in args:
        if hasattr(arg, "__dict__") and not hasattr(arg, "context"):
            return arg
    return None


def _validate_with_schema(input_data: Any, schema_class: type, func_name: str) -> None:
    """Validate input data with Pydantic schema."""
    try:
        if hasattr(input_data, "__dict__"):
            input_dict = input_data.__dict__
        else:
            input_dict = input_data
        schema_class(**input_dict)
    except Exception as e:
        logger.warning(f"Input validation failed for {func_name}: {e}")
        raise ValidationError(f"Input validation failed: {e}")


@strawberry.type
class OptimizedAgentResolvers:
    """Production-ready GraphQL resolvers với comprehensive optimizations.
    Features:
    - Performance monitoring với automatic alerting
    - Intelligent caching với adaptive TTL
    - Comprehensive security validation
    - Input validation với detailed error messages
    - Structured logging cho debugging
    """

    @performance_monitor("agent_creation", target_ms=150)
    @security_check(required_permissions=["agent:create"])
    @validate_input(CreateAgentInput)
    @strawberry.mutation
    async def create_agent(
        self,
        input: CreateAgentInput,
        info: strawberry.Info,
    ) -> AgentType:
        """Create new agent với comprehensive validation và monitoring.
        Args:
            input: Agent creation data
            info: GraphQL resolver context
        Returns:
            Created agent data
        Raises:
            ValidationError: If input validation fails
            HTTPException: If security validation fails
            RuntimeError: If agent creation fails
        """
        try:
            container = info.context.get("container")
            if not container:
                raise RuntimeError("Dependency container missing from context")
            security_context = info.context.get("security_context")
            if not security_context:
                raise RuntimeError("Security context missing")
            if len(input.name) < 2:
                raise ValidationError("Agent name must be at least 2 characters")
            if input.model_type not in ["gpt-4", "gpt-3.5-turbo", "claude-3"]:
                raise ValidationError(f"Unsupported model type: {input.model_type}")
            agent_repo = await container.get_agent_repository()
            create_agent_use_case = CreateAgent(agent_repo)
            agent_data = {
                "name": input.name,
                "description": input.description,
                "model_type": input.model_type,
                "capabilities": input.capabilities or [],
                "owner_id": security_context.user_id,
                "status": "active",
            }
            created_agent = await create_agent_use_case.execute(agent_data)
            logger.info(
                f"Agent created successfully: {created_agent.id} by user {security_context.user_id}"
            )
            return AgentType(
                id=created_agent.id,
                name=created_agent.name,
                description=created_agent.description,
                model_type=created_agent.model_type,
                capabilities=created_agent.capabilities,
                status=created_agent.status,
                created_at=created_agent.created_at,
                updated_at=created_agent.updated_at,
                created_by=security_context.user_id,
            )
        except ValidationError:
            raise
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Unexpected error in create_agent: {e}", exc_info=True)
            raise RuntimeError(f"Agent creation failed: {str(e)}")

    @performance_monitor("agent_retrieval", target_ms=50)
    @cache_result(ttl=300, vary_by=["agent_id"])
    @security_check(required_permissions=["agent:read"])
    @strawberry.query
    async def get_agent(
        self,
        agent_id: UUID,
        info: strawberry.Info,
    ) -> AgentType | None:
        """Get agent by ID với caching và security validation.
        Args:
            agent_id: UUID of agent to retrieve
            info: GraphQL resolver context
        Returns:
            Agent data if found, None otherwise
        Raises:
            HTTPException: If security validation fails
            RuntimeError: If retrieval fails
        """
        try:
            container = info.context.get("container")
            if not container:
                raise RuntimeError("Dependency container missing")
            security_context = info.context.get("security_context")
            agent_repo = await container.get_agent_repository()
            get_agent_use_case = GetAgent(agent_repo)
            agent = await get_agent_use_case.execute(
                agent_id=agent_id, requester_id=security_context.user_id
            )
            if not agent:
                logger.debug(f"Agent {agent_id} not found or not accessible")
                return None
            return AgentType(
                id=agent.id,
                name=agent.name,
                description=agent.description,
                model_type=agent.model_type,
                capabilities=agent.capabilities,
                status=agent.status,
                created_at=agent.created_at,
                updated_at=agent.updated_at,
                created_by=agent.owner_id,
            )
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error retrieving agent {agent_id}: {e}", exc_info=True)
            raise RuntimeError(f"Agent retrieval failed: {str(e)}")

    @performance_monitor("agent_update", target_ms=100)
    @security_check(required_permissions=["agent:update"])
    @validate_input(UpdateAgentInput)
    @strawberry.mutation
    async def update_agent(
        self,
        agent_id: UUID,
        input: UpdateAgentInput,
        info: strawberry.Info,
    ) -> AgentType:
        """Update existing agent với validation và cache invalidation.
        Args:
            agent_id: UUID of agent to update
            input: Agent update data
            info: GraphQL resolver context
        Returns:
            Updated agent data
        Raises:
            ValidationError: If input validation fails
            HTTPException: If security validation fails
            RuntimeError: If update fails
        """
        try:
            container = info.context.get("container")
            security_context = info.context.get("security_context")
            agent_repo = await container.get_agent_repository()
            update_agent_use_case = UpdateAgent(agent_repo)
            update_data = {}
            if input.name is not None:
                update_data["name"] = input.name
            if input.description is not None:
                update_data["description"] = input.description
            if input.capabilities is not None:
                update_data["capabilities"] = input.capabilities
            updated_agent = await update_agent_use_case.execute(
                agent_id=agent_id,
                update_data=update_data,
                requester_id=security_context.user_id,
            )
            cache_manager = CacheManager.get_instance()
            await cache_manager.delete(f"get_agent:agent_id:{agent_id}")
            logger.info(
                f"Agent {agent_id} updated successfully by {security_context.user_id}"
            )
            return AgentType(
                id=updated_agent.id,
                name=updated_agent.name,
                description=updated_agent.description,
                model_type=updated_agent.model_type,
                capabilities=updated_agent.capabilities,
                status=updated_agent.status,
                created_at=updated_agent.created_at,
                updated_at=updated_agent.updated_at,
                created_by=updated_agent.owner_id,
            )
        except ValidationError:
            raise
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error updating agent {agent_id}: {e}", exc_info=True)
            raise RuntimeError(f"Agent update failed: {str(e)}")

    @performance_monitor("agent_list", target_ms=200)
    @cache_result(ttl=60, vary_by=["limit", "offset", "user_id"])
    @security_check(required_permissions=["agent:list"])
    @strawberry.query
    async def list_agents(
        self,
        info: strawberry.Info,
        limit: int = 20,
        offset: int = 0,
    ) -> list[AgentType]:
        """List agents với pagination và user-specific filtering.
        Args:
            limit: Maximum number of agents to return
            offset: Number of agents to skip
            info: GraphQL resolver context
        Returns:
            List of accessible agents
        Raises:
            HTTPException: If security validation fails
            ValidationError: If pagination parameters invalid
            RuntimeError: If listing fails
        """
        try:
            if limit < 1 or limit > 100:
                raise ValidationError("Limit must be between 1 and 100")
            if offset < 0:
                raise ValidationError("Offset must be non-negative")
            container = info.context.get("container")
            security_context = info.context.get("security_context")
            agent_repo = await container.get_agent_repository()
            agents = await agent_repo.list_by_user(
                user_id=security_context.user_id, limit=limit, offset=offset
            )
            return [
                AgentType(
                    id=agent.id,
                    name=agent.name,
                    description=agent.description,
                    model_type=agent.model_type,
                    capabilities=agent.capabilities,
                    status=agent.status,
                    created_at=agent.created_at,
                    updated_at=agent.updated_at,
                    created_by=agent.owner_id,
                )
                for agent in agents
            ]
        except (ValidationError, HTTPException):
            raise
        except Exception as e:
            logger.error(f"Error listing agents: {e}", exc_info=True)
            raise RuntimeError(f"Agent listing failed: {str(e)}")


__all__ = [
    "OptimizedAgentResolvers",
]
