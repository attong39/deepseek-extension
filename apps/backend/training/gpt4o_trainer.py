"""
Lightweight GPT4o trainer service used only for training flows.

This module implements a Trainer service that:
- Checks KB for duplicates via `store.find_similar`.
- Fetches supporting documents via `fetcher.fetch`.
- Calls an LLM provider via `llm.complete` (async).
- Persists artifact to KB via `store.upsert_artifact` with provenance.

Design contract (small):
- llm: async complete(messages, temperature, max_tokens, model) -> str | dict | (str, meta).
- fetcher: fetch(query, limit=...) -> list[dict] (sync or async).
- store (KnowledgeStore): async find_similar(q, threshold=0.9) -> list | [],
                          async upsert_artifact(key, data) -> str.

Keep this module free of ChatService usage — trainer-only.
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import logging
import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from apps.backend.core.services.prompt_library import collect_prompt_suggestions
from apps.backend.core.services.telemetry import TelemetryService
from apps.backend.training import logger as package_logger
import Exception
import NotImplementedError
import RuntimeError
import SYS_CTX
import TRAINER_POLICY
import TimeoutError
import ValueError
import attempt
import bool
import concurrency_semaphore
import d
import dict
import e
import e2
import exc
import fetcher
import float
import int
import isinstance
import len
import limit
import list
import llm
import llm_text
import logger
import max
import mentor_cfg
import prompt_lines
import query
import r
import range
import rules
import self
import store
import str
import telemetry
import tuple
import usage_tokens

# Configure module-specific logger
logger: logging.Logger = package_logger.getChild("gpt4o_trainer")


@dataclass
class MentorConfig:
    """Configuration for the mentor LLM calls.

    Attributes:
        temperature (float): Sampling temperature for LLM. Defaults to 0.0.
        max_tokens (int): Maximum tokens in response. Defaults to 1024.
        model (str): LLM model name. Defaults to "gpt-4o-mini".
        timeout_seconds (int): Timeout for LLM calls in seconds. Defaults to 30.
    """
    temperature: float = 0.0
    max_tokens: int = 1024
    model: str = "gpt-4o-mini"
    timeout_seconds: int = 30


# Policy constant used by trainer prompts so Copilot and code share the same rule
TRAINER_POLICY: str = (
    "You are NOT a user-facing assistant. Never answer end-users directly. "
    "Only produce training artifacts, guidance, evaluation criteria, or prompt libraries."
)

# System context for mentor-style prompts
SYS_CTX: str = (
    "You are a senior mentor helping an AI system learn safely. "
    "Provide step-by-step, actionable guidance, highlight risks, and "
    "prefer lightweight, testable changes. Keep the answer concise. " + TRAINER_POLICY
)


class KnowledgeStoreProtocol:
    """Protocol for knowledge store operations.

    This abstract class defines the interface for finding similar items
    and upserting artifacts in the knowledge base.
    """

    async def find_similar(
        self, q: str, *, threshold: float = 0.9
    ) -> List[Dict[str, Any]]:
        """Find similar items in the knowledge store.

        Args:
            q (str): Query string to search for.
            threshold (float): Similarity threshold. Defaults to 0.9.

        Returns:
            List[Dict[str, Any]]: List of similar items.

        Raises:
            NotImplementedError: If not implemented by subclass.
        """
        raise NotImplementedError()

    async def upsert_artifact(self, key: str, data: Dict[str, Any]) -> str:
        """Upsert an artifact into the knowledge store.

        Args:
            key (str): Unique key for the artifact.
            data (Dict[str, Any]): Artifact data.

        Returns:
            str: Artifact ID.

        Raises:
            NotImplementedError: If not implemented by subclass.
        """
        raise NotImplementedError()


class GPT4oTrainerService:
    """Trainer service that uses an LLM (async), a fetcher, and a KB store.

    Purpose: Only for training pipelines. NEVER used for user-facing chat.

    Attributes:
        llm (Any): LLM provider instance.
        fetcher (Any): Document fetcher instance.
        mentor_cfg (MentorConfig): Configuration for mentor calls.
        telemetry (TelemetryService): Telemetry service instance.
        _sem (Optional[asyncio.Semaphore]): Concurrency semaphore.
    """

    def __init__(
        self,
        llm: Any,
        fetcher: Any,
        mentor_cfg: Optional[MentorConfig] = None,
        telemetry: Optional[TelemetryService] = None,
        concurrency_semaphore: Optional[asyncio.Semaphore] = None,
    ) -> None:
        """Initialize the GPT4oTrainerService.

        Args:
            llm (Any): LLM provider instance.
            fetcher (Any): Document fetcher instance.
            mentor_cfg (Optional[MentorConfig]): Configuration for mentor calls. Defaults to None.
            telemetry (Optional[TelemetryService]): Telemetry service. Defaults to None.
            concurrency_semaphore (Optional[asyncio.Semaphore]): Semaphore for concurrency control. Defaults to None.

        Raises:
            ValueError: If llm or fetcher are None.
        """
        if llm is None:
            raise ValueError("LLM provider must be provided.")
        if fetcher is None:
            raise ValueError("Fetcher must be provided.")
        self.llm = llm
        self.fetcher = fetcher
        self.mentor_cfg = mentor_cfg or MentorConfig()
        self.telemetry = telemetry or TelemetryService()
        self._sem = concurrency_semaphore
        logger.info("GPT4oTrainerService initialized.")

    async def _check_duplicate(self, store: Any, query: str) -> bool:
        """Check for duplicates in the knowledge store.

        Args:
            store (Any): Knowledge store instance.
            query (str): Query string to check.

        Returns:
            bool: True if duplicates found, False otherwise.
        """
        try:
            similar = await store.find_similar(query, threshold=0.9)
            if similar:
                logger.info(f"Duplicate found for query: {query}")
                try:
                    self.telemetry.incr("trainer.skipped_duplicates", 1)
                except Exception as e:
                    logger.warning(f"Telemetry increment failed: {e}")
                return True
        except Exception as e:
            logger.error(f"Error checking duplicates: {e}")
            raise
        return False

    async def _fetch_docs(self, query: str, limit: int) -> List[Dict[str, Any]]:
        """Fetch supporting documents for the query.

        Supports both sync and async fetcher implementations.

        Args:
            query (str): Query string.
            limit (int): Maximum number of documents to fetch.

        Returns:
            List[Dict[str, Any]]: List of fetched documents.

        Raises:
            RuntimeError: If fetching fails.
        """
        try:
            res = self.fetcher.fetch(query, limit=limit)
            if asyncio.iscoroutine(res):
                return await res
            return await asyncio.to_thread(lambda: res)
        except Exception as e:
            logger.error(f"Error fetching docs for query '{query}': {e}")
            raise RuntimeError(f"Failed to fetch documents: {e}") from e

    def _normalize_llm_response(self, raw: Any) -> tuple[str, Optional[int]]:
        """Normalize LLM response to text and usage.

        Args:
            raw (Any): Raw response from LLM.

        Returns:
            tuple[str, Optional[int]]: Normalized text and token usage.
        """
        usage = None
        if isinstance(raw, str):
            text = raw
        elif isinstance(raw, tuple) and len(raw) >= 1:
            text = raw[0]
            if len(raw) > 1 and isinstance(raw[1], dict):
                usage = raw[1].get("usage")
        elif isinstance(raw, dict):
            text = raw.get("text") or raw.get("content") or str(raw)
            usage = raw.get("usage")
        else:
            text = str(raw)
        return text, usage

    async def _call_llm(self, prompt: str) -> tuple[str, Optional[int], int]:
        """Call the LLM with the given prompt.

        Args:
            prompt (str): Prompt to send to LLM.

        Returns:
            tuple[str, Optional[int], int]: Response text, token usage, and duration in ms.

        Raises:
            TimeoutError: If LLM call times out.
            RuntimeError: If LLM call fails.
        """
        start = time.time()
        messages = [
            {"role": "system", "content": SYS_CTX},
            {"role": "user", "content": prompt},
        ]
        call_coro = self.llm.complete(
            messages=messages,
            temperature=self.mentor_cfg.temperature,
            max_tokens=self.mentor_cfg.max_tokens,
            model=self.mentor_cfg.model,
        )
        try:
            if self._sem is not None:
                async with self._sem:
                    raw = await asyncio.wait_for(
                        call_coro, timeout=self.mentor_cfg.timeout_seconds
                    )
            else:
                raw = await asyncio.wait_for(
                    call_coro, timeout=self.mentor_cfg.timeout_seconds
                )
        except TimeoutError:
            logger.error("LLM call timed out.")
            try:
                self.telemetry.incr("trainer.errors.timeout", 1)
            except Exception as e:
                logger.warning(f"Telemetry increment failed: {e}")
            raise
        except Exception as e:
            logger.error(f"LLM call failed: {e}")
            try:
                self.telemetry.incr("trainer.errors.llm", 1)
            except Exception as e2:
                logger.warning(f"Telemetry increment failed: {e2}")
            raise RuntimeError(f"LLM call failed: {e}") from e

        text, usage = self._normalize_llm_response(raw)
        duration_ms = int((time.time() - start) * 1000)
        return text, usage, duration_ms

    async def _persist_artifact(
        self, store: Any, key: str, artifact: Dict[str, Any]
    ) -> str:
        """Persist artifact to the knowledge store with retries.

        Args:
            store (Any): Knowledge store instance.
            key (str): Artifact key.
            artifact (Dict[str, Any]): Artifact data.

        Returns:
            str: Artifact ID.

        Raises:
            RuntimeError: If persistence fails after retries.
        """
        for attempt in range(3):
            try:
                artifact_id = await store.upsert_artifact(key, artifact)
                logger.info(f"Artifact persisted with ID: {artifact_id}")
                return artifact_id
            except Exception as e:
                logger.warning(f"Persist attempt {attempt + 1} failed: {e}")
                await asyncio.sleep(0.2 * (2**attempt))
        logger.error("Failed to persist artifact after retries.")
        try:
            self.telemetry.incr("trainer.errors.persist", 1)
        except Exception as e:
            logger.warning(f"Telemetry increment failed: {e}")
        raise RuntimeError("Failed to persist artifact after retries")

    async def _maybe_persist_suggestions(
        self, store: Any, key: str, query: str, suggestions: List[Dict[str, Any]]
    ) -> None:
        """Persist prompt suggestions if applicable.

        Args:
            store (Any): Knowledge store instance.
            key (str): Base artifact key.
            query (str): Original query.
            suggestions (List[Dict[str, Any]]): List of suggestions.
        """
        try:
            sugg_key = f"{key}_suggestions"
            await store.upsert_artifact(
                sugg_key,
                {"query": query, "suggestions": suggestions, "created_at": time.time()},
            )
            logger.info("Suggestions persisted.")
            try:
                self.telemetry.incr("trainer.suggestions", 1)
            except Exception as e:
                logger.warning(f"Telemetry increment failed: {e}")
        except Exception as e:
            logger.warning(f"Failed to persist suggestions: {e}")

    async def learn_and_persist(
        self, query: str, *, store: Any, limit: int = 5, rules: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Run a training job for the query and persist artifact in store.

        Args:
            query (str): Training query.
            store (Any): Knowledge store instance.
            limit (int): Max documents to fetch. Defaults to 5.
            rules (Optional[List[str]]): Additional rules for prompt. Defaults to None.

        Returns:
            Dict[str, Any]: Result dict with keys: skipped, artifact_id, telemetry, etc.
        """
        if not query or not isinstance(query, str):
            raise ValueError("Query must be a non-empty string.")
        if not isinstance(limit, int) or limit <= 0:
            raise ValueError("Limit must be a positive integer.")
        if rules is not None and not isinstance(rules, list):
            raise ValueError("Rules must be a list of strings or None.")

        # 1) Duplicate check
        if await self._check_duplicate(store, query):
            return {
                "skipped": True,
                "artifact_id": None,
                "telemetry": {"tokens": 0, "time_ms": 0},
            }

        # 2) Fetch docs
        docs = await self._fetch_docs(query, limit)

        # 3) Build prompt
        prompt_lines: List[str] = [
            "You are NOT a user-facing assistant. Produce a concise learning artifact."
        ]
        if rules:
            prompt_lines.extend([f"Rule: {r}" for r in rules])
        prompt_lines.append(f"Query: {query}")
        prompt_lines.append("Sources:")
        for d in docs:
            prompt_lines.append(
                f"- {d.get('title', '?')} ({d.get('source', '?')}): {d.get('text', '')[:200]}"
            )
        prompt = "\n".join(prompt_lines)

        # 4) Call LLM
        try:
            llm_text, usage_tokens, duration_ms = await self._call_llm(prompt)
        except TimeoutError:
            return {
                "skipped": False,
                "artifact_id": None,
                "error": "llm_timeout",
                "telemetry": {"tokens": 0, "time_ms": 0},
            }
        except Exception as exc:
            return {
                "skipped": False,
                "artifact_id": None,
                "error": "llm_error",
                "message": str(exc),
                "telemetry": {"tokens": 0, "time_ms": 0},
            }

        # 5) Persist artifact
        artifact = {
            "query": query,
            "artifact": llm_text,
            "sources": docs,
            "rules": rules or [],
            "created_at": time.time(),
        }
        key_raw = query + json.dumps(artifact, sort_keys=True)
        key = hashlib.sha1(key_raw.encode("utf-8")).hexdigest()
        artifact_id = await self._persist_artifact(store, key, artifact)

        # 6) Telemetry
        try:
            if usage_tokens:
                tokens_real = int(usage_tokens)
                self.telemetry.incr("trainer.tokens_real", tokens_real)
                tokens_est = tokens_real
            else:
                tokens_est = max(1, len(llm_text) // 4)
                self.telemetry.incr("trainer.tokens", tokens_est)
            self.telemetry.timing("trainer.learn_time_ms", duration_ms)
        except Exception as e:
            logger.warning(f"Telemetry failed: {e}")
            tokens_est = max(1, len(llm_text) // 4)

        # 7) Prompt suggestions when confusion detected
        suggestions: List[Dict[str, Any]] = []
        lowered = (llm_text or "").lower()
        if "i don't understand" in lowered or "cannot answer" in lowered:
            try:
                suggestions = await collect_prompt_suggestions(query, docs)
                await self._maybe_persist_suggestions(store, key, query, suggestions)
            except Exception as e:
                logger.warning(f"Failed to collect suggestions: {e}")

        return {
            "skipped": False,
            "artifact_id": artifact_id,
            "key": key,
            "telemetry": {"tokens": tokens_est, "time_ms": duration_ms},
            "suggestions": suggestions,
        }
