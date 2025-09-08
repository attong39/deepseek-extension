from __future__ import annotations

import logging
import re
from typing import Any, Dict, Optional
import Exception
import ValueError
import code
import details
import int
import isinstance
import level
import message
import self
import str
import super

"""
Package: common.exceptions

Custom exception classes for the application.
Layer: core

All exceptions follow these conventions:
- Inherit from ZETACoreException
- Include error codes in format "ZETA-XXX"
- Support structured error data
- Integrate standard project logger for consistent logging

Example usage:
    try:
        raise AuthenticationError("Invalid credentials", {"user_id": 123})
    except AuthenticationError as e:
        logger.error(f"Authentication failed: {e.code} - {e}", extra=e.details)
"""

# Standard project logger
logger = logging.getLogger(__name__)

# Error code registry for documentation and validation
ERROR_CODE_REGISTRY = {
    "ZETA-400": "Validation Error",
    "ZETA-401": "Authentication Error",
    "ZETA-403": "Authorization Error",
    "ZETA-500": "Configuration Error",
    "ZETA-503": "Service Error",
}


class ZETACoreException(Exception):
    """Base exception for ZETA core components.
    
    This class provides a standardized way to handle errors with codes,
    messages, and additional details. It integrates the project's standard
    logger for consistent error reporting.
    
    Args:
        code: Error code in "ZETA-XXX" format (validated against registry)
        message: Human-readable error description
        details: Optional additional error context as a dictionary
    
    Raises:
        ValueError: If the error code format is invalid or not in registry
    
    Example:
        raise ZETACoreException("ZETA-500", "Custom error", {"key": "value"})
    """
    
    def __init__(self, code: str, message: str, details: Optional[Dict[str, Any]] = None) -> None:
        # Validate error code format and registry
        if not re.match(r"^ZETA-\d{3}$", code):
            raise ValueError(f"Invalid error code format: {code}. Must be 'ZETA-XXX'")
        if code not in ERROR_CODE_REGISTRY:
            raise ValueError(f"Unknown error code: {code}. Must be in registry")
        
        self.code = code
        self.details = details or {}
        
        # Validate message is not empty
        if not message or not isinstance(message, str):
            raise ValueError("Message must be a non-empty string")
        
        super().__init__(message)
        
        # Log the exception creation for debugging (optional, can be disabled)
        logger.debug(f"Exception created: {self.code} - {message}", extra=self.details)
    
    def log_error(self, level: int = logging.ERROR) -> None:
        """Log this exception using the project's standard logger.
        
        Args:
            level: Logging level (e.g., logging.ERROR, logging.WARNING)
        """
        logger.log(level, f"{self.code}: {self}", extra=self.details)


class AuthenticationError(ZETACoreException):
    """Raised when authentication fails.
    
    Default code: ZETA-401
    
    Args:
        message: Custom error message (defaults to "Authentication failed")
        details: Optional additional context
    
    Example:
        raise AuthenticationError("Token expired", {"token_id": "abc123"})
    """
    
    def __init__(self, message: str = "Authentication failed", 
                 details: Optional[Dict[str, Any]] = None) -> None:
        super().__init__("ZETA-401", message, details)


class AuthorizationError(ZETACoreException):
    """Raised when authorization fails.
    
    Default code: ZETA-403
    
    Args:
        message: Custom error message (defaults to "Authorization failed")
        details: Optional additional context
    
    Example:
        raise AuthorizationError("Insufficient permissions", {"user_role": "guest"})
    """
    
    def __init__(self, message: str = "Authorization failed",
                 details: Optional[Dict[str, Any]] = None) -> None:
        super().__init__("ZETA-403", message, details)


class ValidationError(ZETACoreException):
    """Raised when validation fails.
    
    Default code: ZETA-400
    
    Args:
        message: Custom error message (defaults to "Validation failed")
        details: Optional additional context
    
    Example:
        raise ValidationError("Invalid email format", {"field": "email", "value": "invalid"})
    """
    
    def __init__(self, message: str = "Validation failed",
                 details: Optional[Dict[str, Any]] = None) -> None:
        super().__init__("ZETA-400", message, details)


class ConfigurationError(ZETACoreException):
    """Raised when configuration is invalid.
    
    Default code: ZETA-500
    
    Args:
        message: Custom error message (defaults to "Configuration error")
        details: Optional additional context
    
    Example:
        raise ConfigurationError("Missing API key", {"config_file": "settings.json"})
    """
    
    def __init__(self, message: str = "Configuration error",
                 details: Optional[Dict[str, Any]] = None) -> None:
        super().__init__("ZETA-500", message, details)


class ServiceError(ZETACoreException):
    """Raised when a service operation fails.
    
    Default code: ZETA-503
    
    Args:
        message: Custom error message (defaults to "Service operation failed")
        details: Optional additional context
    
    Example:
        raise ServiceError("Database connection failed", {"service": "postgres", "host": "localhost"})
    """
    
    def __init__(self, message: str = "Service operation failed",
                 details: Optional[Dict[str, Any]] = None) -> None:
        super().__init__("ZETA-503", message, details)


__all__ = [
    "AuthenticationError",
    "AuthorizationError",
    "ConfigurationError",
    "ServiceError",
    "ValidationError",
    "ZETACoreException",
    "ERROR_CODE_REGISTRY",
]
