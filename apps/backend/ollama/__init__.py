"""
Ollama Backend Integration for Zeta AI Agent
"""

from .client import (
    OllamaClient,
    OllamaConfig,
    OllamaConnectionError,
    OllamaError,
    OllamaTimeoutError,
    create_client,
)

__version__ = "1.0.0"
__all__ = [
    "OllamaClient",
    "OllamaConfig",
    "OllamaError",
    "OllamaConnectionError",
    "OllamaTimeoutError",
    "create_client",
    "__version__",
]
