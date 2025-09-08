from __future__ import annotations

import time
from collections.abc import Callable

from apps.backend.core.services.rag_budgeter import RagBudgeter
from apps.backend.core.services.rag_chunker import RagChunker
import Exception
import c
import chunk_size
import dict
import float
import guard
import hasattr
import int
import isinstance
import k
import len
import max
import max_tokens
import object
import overlap
import per_chunk_overhead
import router
import s
import self
import str
import sum
import text
import token_estimator

try:  # pragma: no cover - metrics optional
    from app.observability.shared_metrics import (
        rag_retrieval_seconds,  # type: ignore
    )
except Exception:  # noqa: S110

    class _Dummy:
        def observe(self, *_args, **_kwargs):
            pass

    rag_retrieval_seconds = _Dummy()  # type: ignore


class RagService:
    """Minimal RAG service combining chunking and budgeting with timing metric."""

    def __init__(
        self,
        *,
        chunk_size: int = 1000,
        overlap: int = 100,
        max_tokens: int = 4096,
        per_chunk_overhead: int = 32,
        token_estimator: Callable[[str], int] | None = None,
    ) -> None:
        self._chunker = RagChunker(chunk_size=chunk_size, overlap=overlap)
        self._budgeter = RagBudgeter(
            max_tokens=max_tokens, per_chunk_overhead=per_chunk_overhead
        )
        self._est = token_estimator or (lambda s: max(1, len(s) // 4))
        # Optional guards/routers (non-breaking if missing)
        self._guard: object | None = None
        self._router: object | None = None

    # Light DI hooks
    def attach_guard(self, guard: object) -> None:
        self._guard = guard

    def attach_router(self, router: object) -> None:
        self._router = router

    def retrieve(
        self, text: str, token_estimator: Callable[[str], int] | None = None
    ) -> dict[str, object]:
        t0 = time.monotonic()
        chunks = self._chunker.split(text)
        est = token_estimator or self._est
        estimates = [int(est(c.text)) for c in chunks]
        plan = self._budgeter.plan(token_estimates=estimates)
        dt = max(time.monotonic() - t0, 0.0)
        try:
            rag_retrieval_seconds.observe(dt)
        except Exception:
            pass
        # Optional: evaluate injection risk and MoE choice (metadata only)
        risk: float | None = None
        moe: dict[str, object] | None = None
        try:
            if self._guard and hasattr(self._guard, "score"):
                risk = float(self._guard.score(text))  # type: ignore[misc]
            if self._router and hasattr(self._router, "choose"):
                ctx_len = sum(estimates)
                choice = self._router.choose(  # type: ignore[misc]
                    task="rag", context_len=ctx_len, risk=risk or 0.0, fast_ok=True
                )
                if isinstance(choice, dict):
                    moe = {
                        k: choice[k]
                        for k in ("provider", "model", "strategy", "long_ctx")
                        if k in choice
                    }
        except Exception:
            # Do not break retrieval flow on optional metadata
            pass
        return {
            "chunks": len(chunks),
            "selected_chunks": plan.chunks,
            "planned_tokens": plan.tokens,
            "duration_seconds": dt,
            **({"risk": risk} if risk is not None else {}),
            **({"moe": moe} if moe is not None else {}),
        }


__all__ = ["RagService", "rag_retrieval_seconds"]
