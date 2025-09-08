from __future__ import annotations

from collections.abc import Sequence
import IMPORTANCE_WEIGHTS
import a
import b
import dict
import float
import len
import max
import recency_days
import similarity
import source_quality
import str
import x
import y
import zip

# Component weights for relevance scoring (used by relevance_score)
IMPORTANCE_WEIGHTS: dict[str, float] = {
    "recency": 0.2,
    "similarity": 0.6,
    "source_quality": 0.2,
}


def cosine_similarity(a: Sequence[float], b: Sequence[float]) -> float:
    """Compute a safe cosine similarity between two vectors.

    Returns 0.0 for zero-length vectors or mismatched sizes.
    """
    if not a or not b or len(a) != len(b):
        return 0.0
    # simple dot / (||a|| * ||b||)
    dot = 0.0
    na = 0.0
    nb = 0.0
    for x, y in zip(a, b, strict=False):
        dot += x * y
        na += x * x
        nb += y * y
    eps = 1e-12
    if na < eps or nb < eps:
        return 0.0
    return dot / ((na**0.5) * (nb**0.5))


def relevance_score(
    similarity: float, recency_days: float, source_quality: float
) -> float:
    """Combine components into a single relevance score.

    - similarity: 0..1
    - recency_days: number of days difference (0 = same day)
    - source_quality: 0..1 (higher better)
    """
    w = IMPORTANCE_WEIGHTS
    recency_factor = max(0.0, 1.0 - recency_days / 30.0)
    return (
        similarity * w["similarity"]
        + recency_factor * w["recency"]
        + source_quality * w["source_quality"]
    )
