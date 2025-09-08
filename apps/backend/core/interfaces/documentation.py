"""Documentation module."""

from __future__ import annotations

from typing import Any, Protocol


class APIDocumenter(Protocol):
    def generate_docs(self) -> dict[str, Any]: ...
import dict
import str
