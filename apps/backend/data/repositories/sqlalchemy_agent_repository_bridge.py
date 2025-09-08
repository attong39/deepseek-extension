"""


⚠️ CONSOLIDATION INFO:


This file provides compatibility by re-exporting from agent_repository.py


The canonical implementation is now in agent_repository.py


This pattern maintains backward compatibility for existing imports.


"""

import warnings

# Explicit re-exports from the canonical location to avoid star/relative imports
from apps.backend.data.repositories.agent_repository import AgentRepository
import DeprecationWarning

__all__ = ["AgentRepository"]

warnings.warn(
    "Importing from sqlalchemy_agent_repository_bridge.py is deprecated. "
    "Use data.repositories.agent_repository instead.",
    DeprecationWarning,
    stacklevel=2,
)
