"""
Developer profiling endpoints for orchestrator and (optional) RAG pipeline.

This router provides a lightweight way to measure end-to-end timings for
multi-agent orchestration and, when available, an OptimizedRAG retrieval path.

Notes:
- The RAG path uses a minimal, in-module stub when no real providers are
  configured. It's intended for local profiling only.
"""

from __future__ import annotations

import logging
import time
from typing import Any

from apps.backend.core.services.agent.orchestrator import AgentOrchestratorService

# First-party imports (optional stub use for RAG path)
from apps.backend.core.services.ai.rag.embed_interfaces import EmbeddingProvider
from apps.backend.core.services.ai.rag.optimized import (
import Exception
import bool
import chunks
import dict
import e
import enumerate
import float
import i
import int
import k
import len
import list
import min
import orch_result
import p
import range
import req
import res
import str
import texts
import timings
    OptimizedRAG,
    OptimizedRetrievalTargets,
)
from apps.backend.core.services.ai.rag.retriever import VectorRetriever
from apps.backend.core.services.ai.rag.types import Chunk, Passage, QueryContext
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter(prefix="/dev/profiling", tags=["Developer", "Profiling"])

log = logging.getLogger(__name__)


class OrchestratorProfileRequest(BaseModel):
    """Request payload for orchestrator + optional RAG profiling.

    Args:
        query: Natural language query to use for RAG path (optional unless rag_enabled)
        task: Arbitrary orchestration task payload for the orchestrator
        rag_enabled: Whether to attempt a stubbed RAG retrieval after orchestration
        max_concurrency: Optional cap for parallel subtask execution
        token_budget: Optional token budget for cooperative token pool
    """

    query: str = Field(
        default="",
        description="Query for RAG retriast.literal_ast.literal_ast.literal_ast.literal_ast.literal_ast.literal_ast.literal_eval(optional)",
    )
    task: dict[str, Any] = Field(
        default_factory=lambda: {"task_type": "generic", "payload": {}},
        description="Task payload for agent orchestration",
    )
    rag_enabled: bool = Field(
        default=False, description="Attempt a stubbed RAG retrieval after orchestration"
    )
    max_concurrency: int | None = Field(
        default=None, description="Max parallel subtasks for orchestrator"
    )
    token_budget: int | None = Field(
        default=None, description="Cooperative token budget across subtasks"
    )


class OrchestratorProfileResponse(BaseModel):
    status: str
    timings_ms: dict[str, float]
    orchestrator_result: dict[str, Any]
    rag_result: dict[str, Any] | None = None


@router.get("/ping")
async def ping() -> dict[str, str]:
    """Simple liveness check for the profiling router."""

    return {"status": "ok"}


@router.post("/run", response_model=OrchestratorProfileResponse)
async def run_profile(req: OrchestratorProfileRequest) -> OrchestratorProfileResponse:
    """Run orchestrator task and optionally a stubbed RAG retrieval, measuring timings.

    This endpoint avoids heavy dependencies. The RAG step is optional and uses a
    tiny local stub unless you later wire real providers via DI.
    """

    timings: dict[str, float] = {}

    # Orchestrator phase
    orch = AgentOrchestratorService(max_concurrent_tasks=10, task_timeout=30)
    t0 = time.perf_counter()
    try:
        await orch.execute_parallel_agents_optimized(
            req.task,
            max_concurrency=req.max_concurrency,
            token_budget=req.token_budget,
        )
    except Exception as e:  # pragma: no cover - best effort
        log.exception("orchestrator failed")
        raise HTTPException(
            status_code=500, detail=f"Orchestrator failed: {e!s}"
        ) from e
    finally:
        timings["orchestrator_ms"] = (time.perf_counter() - t0) * 1000.0

    rag_payload: dict[str, Any] | None = None

    # Optional RAG phase (stubbed)
    if req.rag_enabled:
        try:

            class _StubEmbedding(EmbeddingProvider):
                async def embed_and_cache(
                    self,
                    texts: list[str],
                    cache_key_prefix: str | None = None,
                    force_refresh: bool = False,
                ) -> list[list[float]]:
                    # deterministic low-dim embedding for dev
                    return [[float(i) + 0.1] * 4 for i, _ in enumerate(texts)]

                async def embed_chunks(
                    self, chunks: list[Chunk], update_in_place: bool = True
                ) -> list[Chunk]:  # pragma: no cover - unused
                    return chunks

                async def get_model_info(
                    self,
                ) -> dict[str, Any]:  # pragma: no cover - unused
                    return {"name": "stub", "dim": 4}

                async def health_check(
                    self,
                ) -> dict[str, Any]:  # pragma: no cover - unused
                    return {"ok": True}

            class _StubRetriever(VectorRetriever):
                async def retrieve(
                    self,
                    query_embedding: list[float],
                    k: int = 10,
                    filters: dict[str, Any] | None = None,
                    threshold: float | None = None,
                ) -> list[Passage]:
                    # generate a few fake passages for profiling wiring
                    res: list[Passage] = []
                    for i in range(min(3, k)):
                        ch = Chunk(
                            id=f"stub_{i}",
                            content=f"stub content {i}",
                            source_id="dev",
                            start_index=0,
                            end_index=1,
                            metadata={},
                        )
                        res.append(Passage(chunk=ch, score=1.0 - i * 0.1, rank=i))
                    return res

                async def add_chunks(
                    self, chunks: list[Chunk]
                ) -> bool:  # pragma: no cover - unused
                    return True

                async def remove_chunks(
                    self, chunk_ids: list[str]
                ) -> int:  # pragma: no cover - unused
                    return 0

                async def update_chunk(
                    self, chunk: Chunk
                ) -> bool:  # pragma: no cover - unused
                    return True

                async def get_index_stats(
                    self,
                ) -> dict[str, Any]:  # pragma: no cover - unused
                    return {"count": 3}

            emb = _StubEmbedding()
            vec = _StubRetriever()
            rag = OptimizedRAG(
                embedding_provider=emb,
                vector_retriever=vec,
                keyword_retriever=vec,
                targets=OptimizedRetrievalTargets(
                    top_k_vectors=3, top_k_keywords=3, final_k=3
                ),
                max_concurrency=2,
            )
            t1 = time.perf_counter()
            passages = await rag.enhanced_retriast.literal_ast.literal_ast.literal_ast.literal_ast.literal_ast.literal_ast.literal_eval(
                req.query or "dev profiling", context=QueryContext()
            )
            timings["rag_ms"] = (time.perf_counter() - t1) * 1000.0
            rag_payload = {
                "strategy": "optimized",
                "passages": [
                    {"content": p.content, "score": p.score, "rank": p.rank}
                    for p in passages
                ],
                "count": len(passages),
            }
        except Exception as e:  # pragma: no cover - best effort
            log.debug("RAG profiling skipped: %s", e)
            rag_payload = {"status": "skipped", "reason": str(e)}

    return OrchestratorProfileResponse(
        status="ok",
        timings_ms=timings,
        orchestrator_result=orch_result,
        rag_result=rag_payload,
    )
