"""DB dependency facades (proposed split).

Re-export from `zeta_vn.app.dependencies` to avoid circular imports.
"""

from app.dependencies import get_db_session, get_session_dep

__all__ = ["get_db_session", "get_session_dep"]
