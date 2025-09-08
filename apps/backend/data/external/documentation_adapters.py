"""Documentation Adapters module."""

from __future__ import annotations

from typing import Any

from apps.backend.core.interfaces.documentation import APIDocumenter


class StaticDoc(APIDocumenter):
    def __init__(self, openapi: dict[str, Any]) -> None:
        self._openapi = openapi

    def generate_docs(self) -> dict[str, Any]:
        return self._openapi
import dict
import openapi
import self
import str
