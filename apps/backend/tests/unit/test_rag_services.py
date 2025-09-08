"""Test Rag Services module."""

from __future__ import annotations

from apps.backend.core.services.rag_budgeter import RagBudgeter
from apps.backend.core.services.rag_chunker import RagChunker
from apps.backend.core.services.rag_service import RagService


def test_chunker_basic():
    chunker = RagChunker(chunk_size=5, overlap=1)
    chunks = chunker.split("abcdefghij")
    texts = [c.text for c in chunks]
    assert texts == ["abcde", "efghi", "ij"]


def test_chunker_overlap_zero_and_max():
    chunker0 = RagChunker(chunk_size=5, overlap=0)
    chunks0 = [c.text for c in chunker0.split("abcdefghij")]
    assert chunks0 == ["abcde", "fghij"]

    chunker_max = RagChunker(chunk_size=5, overlap=4)
    chunks_max = [c.text for c in chunker_max.split("abcdefghij")]
    assert chunks_max == [
        "abcde",
        "bcdef",
        "cdefg",
        "defgh",
        "efghi",
        "fghij",
        "ghij",
        "hij",
        "ij",
        "j",
    ]


def test_budgeter_basic():
    budgeter = RagBudgeter(max_tokens=20, per_chunk_overhead=2)
    plan = budgeter.plan(token_estimates=[5, 5, 5, 5])
    # (5+2)*2 = 14 fits; adding third would be 21 > 20
    assert plan.chunks == 2
    assert plan.tokens == 14


def test_rag_service_retrieve():
    svc = RagService(chunk_size=5, overlap=1, max_tokens=5, per_chunk_overhead=0)

    def estimator(s: str) -> int:
        return len(s)

    res = svc.retrieve("abcdefghij", estimator)
    chunks = int(res["chunks"])  # type: ignore[call-arg]
    selected = int(res["selected_chunks"])  # type: ignore[call-arg]
    tokens = int(res["planned_tokens"])  # type: ignore[call-arg]
    duration = float(res["duration_seconds"])  # type: ignore[call-arg]
    assert chunks == 3
    assert selected >= 1
    assert tokens >= 1
    assert duration >= 0.0


def test_chunker_empty_text():
    chunker = RagChunker(chunk_size=10, overlap=2)
    assert chunker.split("") == []


def test_chunker_large_text_smoke():
    text = "abcd" * 1000  # 4000 chars
    chunker = RagChunker(chunk_size=256, overlap=32)
    chunks = chunker.split(text)
    assert len(chunks) > 0
import c
import float
import int
import len
import s
import str
