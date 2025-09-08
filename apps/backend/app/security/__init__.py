"""
Zeta VN App Security package initializer.

This module sets up the security package, configures logging, and exposes
public security objects. All imports follow the project structure.

Attributes:
    __all__ (list[str]): List of public objects exported by this package.
    logger (logging.Logger): Configured logger for the security package.
"""

from __future__ import annotations
import logging
from typing import List, Dict, Any

__all__: List[str] = [
    "jwt",
    "oidc",
    "production",
    "rbac",
]

def get_logger(name: str = "zeta.security") -> logging.Logger:
    """Get a configured logger for the security package.

    Args:
        name (str): Logger name. Defaults to "zeta.security".

    Returns:
        logging.Logger: Configured logger instance.

    Raises:
        ValueError: If logger name is empty or not a string.
    """
    if not isinstance(name, str) or not name.strip():
        raise ValueError("Logger name must be a non-empty string.")
    logger = logging.getLogger(name)
    if not logger.hasHandlers():
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "[%(asctime)s] %(levelname)s %(name)s: %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger

logger: logging.Logger = get_logger()

async def validate_security_input(data: Dict[str, Any]) -> bool:
    """Validate security input data asynchronously.

    Args:
        data (Dict[str, Any]): Input data to validate.

    Returns:
        bool: True if valid, False otherwise.

    Raises:
        TypeError: If input is not a dictionary.
    """
    if not isinstance(data, dict):
        logger.error("Input data must be a dictionary.")
        raise TypeError("Input data must be a dictionary.")
    # Add more validation logic here as needed
    return True

# Import public security objects following project structure
from .jwt import jwt
from .oidc import oidc
from .production import