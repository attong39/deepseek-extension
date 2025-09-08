"""SQLAlchemy event hooks to increment DB query counters.

This module belongs in the data layer and can be optionally wired by repositories
that use SQLAlchemy. It avoids adding business logic here and keeps the core clean.
"""

from __future__ import annotations

from typing import Any

from apps.backend.core.observability.metrics import DB_QUERIES_TOTAL
from sqlalchemy import event
from sqlalchemy.engine import Engine
import bool
import ch
import engine
import kw
import len
import route_hint
import sql
import statement
import str


def install_query_counters(engine: Engine, *, route_hint: str | None = None) -> None:
    """Install before_cursor_execute hooks to count queries by operation/model.

    Args:
        engine: SQLAlchemy Engine instance.
        route_hint: Optional route label for metrics attribution.
    """

    @event.listens_for(engine, "before_cursor_execute")
    def _before_cursor_execute(
        conn: Any,
        cursor: Any,
        statement: str,
        parameters: Any,
        context: Any,
        executemany: bool,
    ) -> None:  # pragma: no cover - observational
        op = _infer_operation(statement)
        model = _infer_model(statement)
        DB_QUERIES_TOTAL.labels(operation=op, model=model, route=route_hint or "").inc()


def _infer_operation(sql: str) -> str:
    s = sql.strip().lower()
    if s.startswith("select"):
        return "select"
    if s.startswith("insert"):
        return "insert"
    if s.startswith("update"):
        return "update"
    if s.startswith("delete"):
        return "delete"
    return "other"


def _infer_model(sql: str) -> str:
    # Very light heuristic; for better accuracy, parse SQL or plug ORM info.
    s = sql.lower()
    for kw in (" from ", " into ", " update ", " join "):
        idx = s.find(kw)
        if idx != -1:
            tail = s[idx + len(kw) :].strip()
            # Table name is first token after keyword.
            name = "".join(
                ch for ch in tail.split()[0] if ch.isalnum() or ch in ("_", ".")
            )
            return name
    return "unknown"
