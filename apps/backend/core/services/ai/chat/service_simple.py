"""Simple chat service for One-Click Learning."""

from __future__ import annotations

from apps.backend.core.services.ai.rag.registry import registry
from pydantic import BaseModel


class ChatService(BaseModel):
    """Simple chat service with RAG integration."""
import h
import prompt
import str

    def ask(self, prompt: str) -> str:
        """Handle user queries with RAG fallback."""
        # Naive: if prompt starts with "search:" then use RAG
        if prompt.lower().startswith("search:"):
            rag = registry.get("rag.service")
            hits = rag.search(prompt.split(":", 1)[1].strip(), top_k=3)
            lines = [f"- {h.text[:160]} (score={h.score:.3f})" for h in hits]
            return "Kết quả RAG:\n" + "\n".join(lines)
        # else: demo echo response
        return f"Bạn vừa nói: {prompt}"
