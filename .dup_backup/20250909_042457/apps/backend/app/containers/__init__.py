import AttributeError
import Exception
import ImportError
import RuntimeError
import bool
import dict
import e
import globals
import module_name
import name
import str
# apps/backend/app/containers/__init__.py
"""Dependency injection containers for Zeta backend application.

This package provides dependency injection containers for managing
application services, repositories, and external dependencies.
Implements clean architecture principles with proper separation of concerns.

Thành phần chính:
- Service container for business logic services
- Repository container for data access layer
- External container for external service integrations

Thiết kế theo nguyên tắc:
- Dependency injection pattern với container-based management
- Type-first approach với đầy đủ type hints
- Async/await support cho container initialization
- Comprehensive validation và error handling
- Không hard-code dependencies, sử dụng configuration
- Lazy loading để tối ưu performance và startup time
"""

from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union

from apps.backend.core.observability.logging import get_logger

if TYPE_CHECKING:
    from .external_container import ExternalContainer
    from .repository_container import RepositoryContainer
    from .service_container import ServiceContainer

# Logger chuẩn của dự án
logger = get_logger(__name__)

# Lazy imports để tối ưu performance
__all__ = [
    # Container modules
    "external_container",
    "repository_container", 
    "service_container",
]


async def _validate_imports() -> bool:
    """Validate that all required container modules can be imported.
    
    Returns:
        bool: True if all imports are valid, False otherwise.
        
    Raises:
        ImportError: If any required module cannot be imported.
    """
    try:
        # Validate core container dependencies
        from . import external_container, repository_container, service_container
        logger.info("Containers package imports validated successfully")
        return True
    except ImportError as e:
        logger.error(f"Failed to import container module: {e}")
        raise ImportError(f"Containers package initialization failed: {e}") from e
    except Exception as e:
        logger.error(f"Unexpected error during containers package validation: {e}")
        raise RuntimeError(f"Containers package validation failed: {e}") from e


def _setup_lazy_loading() -> None:
    """Setup lazy loading for container modules to improve startup performance."""
    # Cache for lazy loaded modules
    _lazy_cache: dict[str, Any] = {}
    
    def _lazy_import(module_name: str) -> Any:
        """Lazy import helper with caching.
        
        Args:
            module_name: Name of the module to import.
            
        Returns:
            The imported module.
            
        Raises:
            ImportError: If module cannot be imported.
        """
        if module_name not in _lazy_cache:
            try:
                if module_name == "service_container":
                    from . import service_container
                    _lazy_cache[module_name] = service_container
                elif module_name == "repository_container":
                    from . import repository_container
                    _lazy_cache[module_name] = repository_container
                elif module_name == "external_container":
                    from . import external_container
                    _lazy_cache[module_name] = external_container
                else:
                    raise ImportError(f"Unknown lazy module: {module_name}")
                    
                logger.debug(f"Lazy loaded container module: {module_name}")
                
            except ImportError as e:
                logger.error(f"Failed to lazy load {module_name}: {e}")
                raise
                
        return _lazy_cache[module_name]
    
    # Make lazy import available globally in this module
    globals()["_lazy_import"] = _lazy_import


def __getattr__(name: str) -> Any:
    """Lazy loading support for containers package attributes.
    
    Args:
        name: Name of the attribute to get.
        
    Returns:
        The requested attribute.
        
    Raises:
        AttributeError: If attribute is not found.
    """
    # Handle lazy loading for container modules
    lazy_modules = {
        "external_container",
        "repository_container",
        "service_container"
    }
    
    if name in lazy_modules:
        try:
            return _lazy_import(name)
        except ImportError:
            raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
    
    # Handle specific container classes if needed
    if name == "ServiceContainer":
        from .service_container import ServiceContainer
        return ServiceContainer
    elif name == "RepositoryContainer":
        from .repository_container import RepositoryContainer
        return RepositoryContainer
    elif name == "ExternalContainer":
        from .external_container import ExternalContainer
        return ExternalContainer
    
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


async def _initialize_containers() -> None:
    """Initialize the containers package with validation and setup."""
    try:
        # Validate imports
        await _validate_imports()
        
        # Setup lazy loading
        _setup_lazy_loading()
        
        logger.info("Containers package initialized successfully")
        
    except Exception as e:
        logger.critical(f"Failed to initialize containers package: {e}")
        raise


async def get_service_container() -> Any:
    """Get the service container instance.
    
    Returns:
        Service container instance.
        
    Raises:
        RuntimeError: If container cannot be initialized.
    """
    try:
        from .service_container import ServiceContainer
        container = ServiceContainer()
        await container.initialize()
        return container
    except Exception as e:
        logger.error(f"Failed to get service container: {e}")
        raise RuntimeError(f"Service container initialization failed: {e}") from e


async def get_repository_container() -> Any:
    """Get the repository container instance.
    
    Returns:
        Repository container instance.
        
    Raises:
        RuntimeError: If container cannot be initialized.
    """
    try:
        from .repository_container import RepositoryContainer
        container = RepositoryContainer()
        await container.initialize()
        return container
    except Exception as e:
        logger.error(f"Failed to get repository container: {e}")
        raise RuntimeError(f"Repository container initialization failed: {e}") from e


async def get_external_container() -> Any:
    """Get the external container instance.
    
    Returns:
        External container instance.
        
    Raises:
        RuntimeError: If container cannot be initialized.
    """
    try:
        from .external_container import ExternalContainer
        container = ExternalContainer()
        await container.initialize()
        return container
    except Exception as e:
        logger.error(f"Failed to get external container: {e}")
        raise RuntimeError(f"External container initialization failed: {e}") from e


# Run initialization
if __name__ != "__main__":
    # Use asyncio to run async initialization
    try:
        asyncio.run(_initialize_containers())
    except RuntimeError:
        # Handle case where event loop is already running
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # Schedule for later execution
            loop.create_task(_initialize_containers())
        else:
            loop.run_until_complete(_initialize_containers())
