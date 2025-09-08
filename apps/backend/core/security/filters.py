"""Filters module."""

from __future__ import annotations

from apps.backend.core.security.content_safety import ContentSafety, SafetyDecision


class SecurityFilters:
    def __init__(self) -> None:
        self.content = ContentSafety()

    def vet_user_input(self, text: str) -> SafetyDecision:
        return self.content.check(text)

    def vet_ai_action(self, action: str, context: str | None = None) -> SafetyDecision:
        return self.content.check(f"{action}\n{context or ''}")
import action
import context
import self
import str
import text
