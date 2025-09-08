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
# apps/backend/app/auth/__init__.py
"""Authentication and authorization package for Zeta backend application.

This package provides comprehensive authentication and authorization services
including JWT token management, user authentication, permission handling,
and security middleware integration.

Thành phần chính:
- JWT token handling and validation
- User authentication and session management
- Permission-based access control
- Security middleware for request protection
- Database integration for auth data

Thiết kế theo nguyên tắc:
- Clean Architecture với separation of concerns
- Type-first approach với đầy đủ type hints
- Async/await support cho I/O operations
- Comprehensive input validation và error handling
- Không hard-code values, sử dụng configuration
- Logger integration theo chuẩn dự án
"""

from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union

from apps.backend.core.observability.logging import get_logger

if TYPE_CHECKING:
    from .auth_db import AuthDatabase
    from .auth_dependencies import AuthDependencies
    from .dependencies import Dependencies
    from .jwt_dependencies import JWTDependencies
    from .jwt_handler import JWTHandler
    from .logging_config import LoggingConfig
    from .security_middleware import SecurityMiddleware

# Logger chuẩn của dự án
logger = get_logger(__name__)

# Lazy imports để tối ưu performance
__all__ = [
    # Core authentication components
    "CurrentUserDep",
    "JWTHandler",
    "PERMISSION_ROUTES",
    "PUBLIC_ROUTES",
    "SecurityContextDep",
    "SecurityEnforcementMiddleware",
    
    # Dependencies and configuration
    "action",
    "agent_id",
    "audit_data",
    "auth_header",
    "build_agent_resource",
    "build_file_resource",
    "build_memory_resource",
    "client_ip",
    "context",
    "create_user_token",
    "decode",
    "email",
    "environment",
    "file_id",
    "get_current_user",
    "get_security_context",
    "headers",
    "is_active",
    "is_allowed",
    "logger",
    "memory_id",
    "method",
    "missing_permissions",
    "path",
    "payload",
    "permission_dependency",
    "permission_manager",
    "request_id",
    "require_all_permissions",
    "require_any_permission",
    "require_permission",
    "required_permissions",
    "resource",
    "role",
    "scopes",
    "security",
    "subject",
    "token",
    "token_role",
    "user",
    "user_agent",
    "user_id",
    "user_scopes",
    "username",
    "verify_token",
    
    # Internal modules
    "auth_db",
    "auth_dependencies",
    "dependencies",
    "dependencies_fixed",
    "jwt_dependencies",
    "jwt_handler",
    "logging_config",
    "security_middleware",
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
        from . import auth_dependencies, jwt_handler, security_middleware
        logger.info("Auth package imports validated successfully")
        return True
    except ImportError as e:
        logger.error(f"Failed to import auth module: {e}")
        raise ImportError(f"Auth package initialization failed: {e}") from e
    except Exception as e:
        logger.error(f"Unexpected error during auth package validation: {e}")
        raise RuntimeError(f"Auth package validation failed: {e}") from e


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
                if module_name == "auth_db":
                    from . import auth_db
                    _lazy_cache[module_name] = auth_db
                elif module_name == "jwt_handler":
                    from . import jwt_handler
                    _lazy_cache[module_name] = jwt_handler
                elif module_name == "security_middleware":
                    from . import security_middleware
                    _lazy_cache[module_name] = security_middleware
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
    """Lazy loading support for auth package attributes.
    
    Args:
        name: Name of the attribute to get.
        
    Returns:
        The requested attribute.
        
    Raises:
        AttributeError: If attribute is not found.
    """
    # Handle lazy loading for heavy modules
    lazy_modules = {
        "auth_db",
        "auth_dependencies", 
        "dependencies",
        "dependencies_fixed",
        "jwt_dependencies",
        "jwt_handler",
        "logging_config",
        "security_middleware"
    }
    
    if name in lazy_modules:
        try:
            return _lazy_import(name)
        except ImportError:
            raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
    
    # Handle specific functions/objects
    if name == "CurrentUserDep":
        from .auth_dependencies import CurrentUserDep
        return CurrentUserDep
    elif name == "JWTHandler":
        from .jwt_handler import JWTHandler
        return JWTHandler
    elif name == "SecurityEnforcementMiddleware":
        from .security_middleware import SecurityEnforcementMiddleware
        return SecurityEnforcementMiddleware
    elif name == "get_current_user":
        from .auth_dependencies import get_current_user
        return get_current_user
    elif name == "get_security_context":
        from .auth_dependencies import get_security_context
        return get_security_context
    elif name == "create_user_token":
        from .jwt_handler import create_user_token
        return create_user_token
    elif name == "verify_token":
        from .jwt_handler import verify_token
        return verify_token
    
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


# Initialize package
async def _initialize_package() -> None:
    """Initialize the auth package with validation and setup."""
    try:
        # Validate imports
        await _validate_imports()
        
        # Setup lazy loading
        _setup_lazy_loading()
        
        logger.info("Auth package initialized successfully")
        
    except Exception as e:
        logger.critical(f"Failed to initialize auth package: {e}")
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
