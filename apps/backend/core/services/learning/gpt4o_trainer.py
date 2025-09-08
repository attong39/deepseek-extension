"""GPT-4o mentor/trainer orchestration service.

This service acts as a mediator between external LLM providers (e.g., GPT-4o)
and the system's learning workflows. It can:
- Ask GPT-4o for mentorship suggestions on novel situations
- Summarize and extract insights from online sources
- Orchestrate a simple self-improvement cycle from external knowledge

Design notes:
- Depends only on abstract interfaces (LLMProvider) and a pluggable
    knowledge source fetcher to preserve Clean Architecture boundaries.
- No direct network calls here; concrete adapters live in the data layer.

All public methods are async and fully typed to satisfy mypy --strict.
"""

from __future__ import annotations

import logging
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any, Protocol

from apps.backend.core.interfaces.llm_provider import LLMProvider
import bool
import config
import context
import dict
import fetcher
import float
import int
import it
import limit
import list
import llm
import messages
import min
import query
import rules
import self
import situation
import str

logger = logging.getLogger(__name__)


class KnowledgeFetcher(Protocol):
    """Protocol for fetching online knowledge items by query.

    Implementations may call Wikipedia, ArXiv, or other sources. To keep
    the core layer decoupled, we only define the expected shape here.
    The protocol allows either an async or sync implementation.
    """

    def fetch(self, query: str, *, limit: int = 5) -> list[dict[str, Any]]: ...


@dataclass(slots=True)
class MentorConfig:
    """Configuration controlling mentor behavior.

    Attributes:
        enabled: If False, mentor calls are skipped.
        model: OpenAI model name (e.g., "gpt-4o").
        temperature: Sampling temperature for completions.
        max_tokens: Optional generation cap.
    """

    enabled: bool = True
    model: str = "gpt-4o"
    temperature: float = 0.4
    max_tokens: int | None = 800


class GPT4oTrainerService:
    """High-level mentor/trainer using GPT-4o and online sources.

    This is intentionally lightweight: it turns domain questions and fetched
    documents into chat prompts, then aggregates GPT-4o suggestions.
    """

    def __init__(
        self,
        *,
        llm: LLMProvider,
        fetcher: KnowledgeFetcher,
        config: MentorConfig | None = None,
    ) -> None:
        """Initialize the service.

        Args:
            llm: Abstraction over LLM chat completions (vendor-agnostic).
            fetcher: Online knowledge fetcher implementation.
            config: Optional mentor configuration.
        """

        self._llm = llm
        self._fetcher = fetcher
        self._cfg = config or MentorConfig()

    async def mentor_suggest(
        self, situation: str, context: dict[str, Any] | None = None
    ) -> str:
        """Ask GPT-4o for guidance on a novel situation.

        Args:
            situation: Natural-language description of the problem.
            context: Optional structured context (constraints, goals, metrics).

        Returns:
            A suggestion string produced by GPT-4o (may include bullet points).
        """

        if not self._cfg.enabled:
            logger.info("GPT4oTrainerService.mentor_suggest skipped (disabled)")
            return "Mentor disabled."

        sys_ctx = (
            "You are a senior mentor helping an AI system learn safely. "
            "Provide step-by-step, actionable guidance, highlight risks, and "
            "prefer lightweight, testable changes. Keep the answer concise."
        )
        user_msg = f"Situation: {situation}\nContext: {context or {}}"
        messages: list[dict[str, str]] = [
            {"role": "system", "content": sys_ctx},
            {"role": "user", "content": user_msg},
        ]

        content = await self._llm.complete(
            messages,
            temperature=self._cfg.temperature,
            max_tokens=self._cfg.max_tokens,
            model=self._cfg.model,
        )
        return content or ""

    async def summarize_sources(self, query: str, *, limit: int = 5) -> dict[str, Any]:
        """Fetch and summarize online sources with GPT-4o.

        Args:
            query: Search query/topic.
            limit: Maximum number of documents to include.

        Returns:
            A dict with raw items and a consolidated summary.
        """

        items = self._fetcher.fetch(query, limit=limit)
        if not items:
            return {"items": [], "summary": "No relevant documents found."}

        # Prepare a compact prompt with selected snippets
        snippets = []
        for it in items:
            title = str(it.get("title", "Untitled"))
            src = str(it.get("source", "unknown"))
            text = str(it.get("text", ""))[:2000]
            snippets.append(f"[{src}] {title}:\n{text}")

        sys_ctx = (
            "You are an expert research assistant. Summarize the following "
            "sources into a concise, factual brief with 3-5 key points and "
            "clear caveats. Avoid speculation."
        )
        user_msg = "\n\n".join(snippets)
        messages: list[dict[str, str]] = [
            {"role": "system", "content": sys_ctx},
            {"role": "user", "content": f"Topic: {query}\nSources:\n{user_msg}"},
        ]

        summary = await self._llm.complete(
            messages,
            temperature=0.3,
            max_tokens=min(self._cfg.max_tokens or 600, 900),
            model=self._cfg.model,
        )
        return {"items": items, "summary": summary or ""}

    async def train_from_online_sources(
        self,
        query: str,
        *,
        limit: int = 5,
        rules: Sequence[str] | None = None,
    ) -> dict[str, Any]:
        """End-to-end training: fetch, summarize, and output a knowledge artifact.

        Args:
            query: Topic to learn.
            limit: Max documents.
            rules: Optional governance/safety rules to prepend.

        Returns:
            A dict containing the knowledge artifact and provenance.
        """

        summary_bundle = await self.summarize_sources(query, limit=limit)
        policy = "\n".join(rules or [])
        prompt = (
            "Create a structured learning artifact with: objectives, key insights, "
            "action checklist, and references. Keep it under 400 words.\n" + policy
        )
        messages: list[dict[str, str]] = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": summary_bundle.get("summary", "")},
        ]
        artifact = await self._llm.complete(
            messages,
            temperature=0.4,
            max_tokens=min(self._cfg.max_tokens or 700, 800),
            model=self._cfg.model,
        )
        return {
            "query": query,
            "artifact": artifact or "",
            "provenance": summary_bundle.get("items", []),
        }
