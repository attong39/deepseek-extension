"""Compatibility bridge for the unified database service.

This module re-exports the canonical DatabaseService that lives under
``data.services.database_service``. Import from here to keep existing
``core.services`` import paths working after the consolidation.
"""

from __future__ import annotations

from data.services.database_service import (
    DatabaseService,
    get_database_service,
    get_db_session_unified,
)

__all__ = [
    "DatabaseService",
    "get_database_service",
    "get_db_session_unified",
]
