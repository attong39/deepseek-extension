from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar
from uuid import UUID

import strawberry
from apps.backend.core.exceptions.validation_exceptions import ValidationError
from pydantic import BaseModel
from pydantic import ValidationError as PydanticValidationError
import Exception
import PermissionError
import ValueError
import admin_override
import arg
import args
import bool
import callable
import check_ownership
import dict
import e
import error
import factory
import getattr
import hasattr
import info
import input_data
import int
import isinstance
import key
import kwargs
import operation
import resource_id
import resource_owner_id
import self
import str

"""Base GraphQL resolvers với shared logic và performance optimization.
Centralized authentication, validation, error handling, và caching patterns
để eliminate code duplication và improve performance.
"""
logger = logging.getLogger(__name__)
T = TypeVar("T")
InputT = TypeVar("InputT", bound=BaseModel)
OutputT = TypeVar("OutputT")


class BaseResolver(ABC, Generic[T]):
    """Base resolver với shared patterns để eliminate duplication.
    Provides:
    - Authentication & authorization
    - Input validation với Pydantic v2
    - Comprehensive error handling
    - Performance monitoring
    - Caching integration
    """

    def __init__(self) -> None:
        """Initialize base resolver với shared dependencies."""
        self._cache: dict[str, Any] = {}
        self._logger = logging.getLogger(self.__class__.__name__)

    async def _get_context(self, info: strawberry.Info) -> dict[str, Any]:
        """Extract và validate GraphQL context.
        Args:
            info: GraphQL resolver info
        Returns:
            Validated context dictionary
        Raises:
            PermissionError: If context is invalid
        """
        context = info.context
        if not isinstance(context, dict):
            raise PermissionError("Invalid GraphQL context")
        container = context.get("container")
        current_user = context.get("current_user")
        if not container:
            raise PermissionError("Missing dependency container")
        return {
            "container": container,
            "current_user": current_user,
            "security_context": context.get("security_context"),
        }

    async def _require_authentication(self, info: strawberry.Info) -> dict[str, Any]:
        """Require user authentication.
        Args:
            info: GraphQL resolver info
        Returns:
            Validated context với authenticated user
        Raises:
            PermissionError: If user not authenticated
        """
        context = await self._get_context(info)
        if not context.get("current_user"):
            raise PermissionError("Authentication required")
        return context

    async def _validate_input(self, input_data: InputT) -> InputT:
        """Validate input data với Pydantic v2.
        Args:
            input_data: Input data to validate
        Returns:
            Validated input data
        Raises:
            ValidationError: If validation fails
        """
        try:
            if hasattr(input_data, "model_validate"):
                return input_data.model_validate(input_data.model_dump())
            return input_data
        except PydanticValidationError as e:
            self._logger.warning(f"Input validation failed: {e}")
            raise ValidationError(f"Invalid input: {e}")

    async def _check_ownership(
        self, resource_owner_id: str, current_user: Any, admin_override: bool = True
    ) -> bool:
        """Check resource ownership permissions.
        Args:
            resource_owner_id: ID of resource owner
            current_user: Current authenticated user
            admin_override: Allow admin access regardless of ownership
        Returns:
            True if access allowed
        Raises:
            PermissionError: If access denied
        """
        if resource_owner_id == current_user.id:
            return True
        if admin_override and getattr(current_user, "is_admin", False):
            return True
        raise PermissionError("Access denied: insufficient permissions")

    async def _handle_error(self, error: Exception, operation: str) -> None:
        """Centralized error handling với logging.
        Args:
            error: Exception that occurred
            operation: Name of operation that failed
        """
        if isinstance(error, (ValidationError, PermissionError)):
            self._logger.warning(f"{operation} failed: {error}")
            raise
        else:
            self._logger.error(f"{operation} error: {error}", exc_info=True)
            raise ValueError(f"Operation failed: {str(error)}")

    def _cache_key(self, *args: Any) -> str:
        """Generate cache key từ arguments.
        Args:
            *args: Arguments to hash
        Returns:
            Cache key string
        """
        return "|".join(str(arg) for arg in args)

    async def _with_cache(self, key: str, factory: callable, ttl: int = 300) -> Any:
        """Execute operation với caching support.
        Args:
            key: Cache key
            factory: Function to call if cache miss
            ttl: Time to live in seconds
        Returns:
            Cached or fresh result
        """
        if key in self._cache:
            self._logger.debug(f"Cache hit for key: {key}")
            return self._cache[key]
        result = await factory()
        self._cache[key] = result
        self._logger.debug(f"Cache miss for key: {key}, result cached")
        return result


class CRUDResolver(BaseResolver[T]):
    """Base CRUD resolver với standard operations.
    Provides common CRUD patterns:
    - create_resource
    - get_resource
    - update_resource
    - delete_resource
    - list_resources
    """

    @abstractmethod
    async def _get_repository(self, container: Any) -> Any:
        """Get repository instance từ container.
        Args:
            container: Dependency container
        Returns:
            Repository instance
        """

    @abstractmethod
    def _entity_to_graphql(self, entity: Any) -> Any:
        """Convert domain entity to GraphQL type.
        Args:
            entity: Domain entity
        Returns:
            GraphQL type instance
        """

    async def create_resource(
        self, input_data: InputT, info: strawberry.Info, **kwargs: Any
    ) -> OutputT:
        """Generic create operation.
        Args:
            input_data: Creation input
            info: GraphQL info
            **kwargs: Additional arguments
        Returns:
            Created resource
        """
        try:
            context = await self._require_authentication(info)
            validated_input = await self._validate_input(input_data)
            repo = await self._get_repository(context["container"])
            entity = await self._create_entity(repo, validated_input, context, **kwargs)
            result = self._entity_to_graphql(entity)
            self._logger.info(
                f"Resource created successfully: {getattr(entity, 'id', 'unknown')}"
            )
            return result
        except Exception as e:
            await self._handle_error(e, "create_resource")

    async def get_resource(
        self,
        resource_id: UUID,
        info: strawberry.Info,
        check_ownership: bool = True,
        **kwargs: Any,
    ) -> OutputT | None:
        """Generic get operation với caching.
        Args:
            resource_id: Resource ID
            info: GraphQL info
            check_ownership: Whether to check ownership
            **kwargs: Additional arguments
        Returns:
            Resource if found and accessible
        """
        try:
            context = await self._require_authentication(info)
            cache_key = self._cache_key(
                "get_resource", resource_id, context["current_user"].id
            )

            async def fetch_resource():
                repo = await self._get_repository(context["container"])
                entity = await repo.get_by_id(str(resource_id))
                if not entity:
                    return None
                if check_ownership:
                    await self._check_ownership(
                        entity.owner_id, context["current_user"]
                    )
                return self._entity_to_graphql(entity)

            return await self._with_cache(cache_key, fetch_resource)
        except Exception as e:
            await self._handle_error(e, "get_resource")
            return None

    @abstractmethod
    async def _create_entity(
        self, repo: Any, input_data: InputT, context: dict[str, Any], **kwargs: Any
    ) -> Any:
        """Create entity implementation - must be overridden.
        Args:
            repo: Repository instance
            input_data: Validated input
            context: Request context
            **kwargs: Additional arguments
        Returns:
            Created entity
        """


__all__ = [
    "BaseResolver",
    "CRUDResolver",
]
