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
# apps/backend/app/common/__init__.py
"""Common utilities and shared components for Zeta backend application.

This package provides shared functionality including error handling,
exception definitions, schema validation, and common utilities used
across the application.

Thành phần chính:
- Exception classes for API error handling
- Error handlers for different types of exceptions
- Schema definitions for common data structures
- Validation utilities and helpers

Thiết kế theo nguyên tắc:
- Clean Architecture với reusable components
- Type-first approach với đầy đủ type hints
- Async/await support cho validation operations
- Comprehensive error handling và logging
- Không hard-code values, sử dụng configuration
- Lazy loading để tối ưu performance
"""

from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union

from apps.backend.core.observability.logging import get_logger

if TYPE_CHECKING:
    from .error_handlers import ErrorHandlers
    from .exceptions import Exceptions
    from .schemas import Schemas

# Logger chuẩn của dự án
logger = get_logger(__name__)

# Lazy imports để tối ưu performance
__all__ = [
    # Exception classes
    "APIError",
    "APIMeta",
    "ConflictError",
    "ErrorBody",
    "ErrorResponse",
    "ForbiddenError",
    "NotFoundError",
    "ValidationError",
    
    # Error handlers
    "api_error_handler",
    "body",
    "generic_exception_handler",
    "logger",
    
    # Internal modules
    "error_handlers",
    "exceptions",
    "schemas",
]


async def _validate_imports() -> bool:
    """Validate that all required modules can be imported.
    
    Returns:
        bool: True if all imports are valid, False otherwise.
        
    Raises:
        ImportError: If any required module cannot be imported.
    """
    try:
        # Validate core dependencies
        from . import error_handlers, exceptions, schemas
        logger.info("Common package imports validated successfully")
        return True
    except ImportError as e:
        logger.error(f"Failed to import common module: {e}")
        raise ImportError(f"Common package initialization failed: {e}") from e
    except Exception as e:
        logger.error(f"Unexpected error during common package validation: {e}")
        raise RuntimeError(f"Common package validation failed: {e}") from e


def _setup_lazy_loading() -> None:
    """Setup lazy loading for heavy modules to improve startup performance."""
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
                if module_name == "exceptions":
                    from . import exceptions
                    _lazy_cache[module_name] = exceptions
                elif module_name == "error_handlers":
                    from . import error_handlers
                    _lazy_cache[module_name] = error_handlers
                elif module_name == "schemas":
                    from . import schemas
                    _lazy_cache[module_name] = schemas
                else:
                    raise ImportError(f"Unknown lazy module: {module_name}")
                    
                logger.debug(f"Lazy loaded module: {module_name}")
                
            except ImportError as e:
                logger.error(f"Failed to lazy load {module_name}: {e}")
                raise
                
        return _lazy_cache[module_name]
    
    # Make lazy import available globally in this module
    globals()["_lazy_import"] = _lazy_import


def __getattr__(name: str) -> Any:
    """Lazy loading support for common package attributes.
    
    Args:
        name: Name of the attribute to get.
        
    Returns:
        The requested attribute.
        
    Raises:
        AttributeError: If attribute is not found.
    """
    # Handle lazy loading for heavy modules
    lazy_modules = {
        "error_handlers",
        "exceptions", 
        "schemas"
    }
    
    if name in lazy_modules:
        try:
            return _lazy_import(name)
        except ImportError:
            raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
    
    # Handle specific classes/functions
    if name == "APIError":
        from .exceptions import APIError
        return APIError
    elif name == "ValidationError":
        from .exceptions import ValidationError
        return ValidationError
    elif name == "ConflictError":
        from .exceptions import ConflictError
        return ConflictError
    elif name == "ForbiddenError":
        from .exceptions import ForbiddenError
        return ForbiddenError
    elif name == "NotFoundError":
        from .exceptions import NotFoundError
        return NotFoundError
    elif name == "ErrorResponse":
        from .exceptions import ErrorResponse
        return ErrorResponse
    elif name == "ErrorBody":
        from .exceptions import ErrorBody
        return ErrorBody
    elif name == "APIMeta":
        from .exceptions import APIMeta
        return APIMeta
    elif name == "api_error_handler":
        from .error_handlers import api_error_handler
        return api_error_handler
    elif name == "generic_exception_handler":
        from .error_handlers import generic_exception_handler
        return generic_exception_handler
    elif name == "body":
        from .error_handlers import body
        return body
    
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


async def _initialize_package() -> None:
    """Initialize the common package with validation and setup."""
    try:
        # Validate imports
        await _validate_imports()
        
        # Setup lazy loading
        _setup_lazy_loading()
        
        logger.info("Common package initialized successfully")
        
    except Exception as e:
        logger.critical(f"Failed to initialize common package: {e}")
        raise


# Run initialization
if __name__ != "__main__":
    # Use asyncio to run async initialization
    try:
        asyncio.run(_initialize_package())
    except RuntimeError:
        # Handle case where event loop is already running
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # Schedule for later execution
            loop.create_task(_initialize_package())
        else:
            loop.run_until_complete(_initialize_package())
