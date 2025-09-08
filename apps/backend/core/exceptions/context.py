"""
Exception context management for better error tracking.
"""

from __future__ import annotations

import uuid
from contextlib import asynccontextmanager
from datetime import UTC, datetime
from typing import Any
import Exception
import context_data
import dict
import exc
import hasattr
import isinstance
import list
import metadata
import operation
import self
import str


class ExceptionContext:
    """Context manager for exception handling.

    Keeps a simple stack of operation contexts that can be merged into any
    raised exception under the attribute ``context``.
    """

    def __init__(self) -> None:
        self.context_stack: list[dict[str, Any]] = []

    @asynccontextmanager
    async def operation_context(
        self,
        operation: str,
        metadata: dict[str, Any] | None = None,
    ):
        """Async context manager for operations.

        Args:
            operation: Logical operation name.
            metadata: Optional metadata to associate.
        """
        context_id = str(uuid.uuid4())
        context_data: dict[str, Any] = {
            "context_id": context_id,
            "operation": operation,
            "metadata": metadata or {},
            "start_time": datetime.now(UTC),
        }
        self.context_stack.append(context_data)
        try:
            yield context_data
        except Exception as exc:  # noqa: BLE001 - we re-raise immediately
            # Enrich exception with context
            try:
                if hasattr(exc, "context") and isinstance(exc.context, dict):
                    exc.context.update(context_data)  # type: ignore[reportUnknownMemberType]
                else:
                    exc.context = context_data  # type: ignore[reportUnknownMemberType]
            finally:
                raise
        finally:
            # Pop safety: ensure we remove the same object
            if self.context_stack and self.context_stack[-1] is context_data:
                self.context_stack.pop()
