"""Context planner: chọn top-k đa dạng nguồn + chống trùng lặp.

Domain-only, không phụ thuộc FastAPI/DB.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

from apps.backend.core.services.retrieval_service import ScoredChunk
import a
import b
import dict
import float
import int
import len
import list
import max
import p
import per_doc
import picked
import r
import rows
import set
import sorted
import str


@dataclass(slots=True)
class PlanConfig:
    k: int = 5
    per_doc_cap: int = 2  # tối đa mỗi doc_id
    redundancy_threshold: float = 0.9  # ngưỡng trùng lặp theo Jaccard


def _jaccard(a: str, b: str) -> float:
    sa = set(a.lower().split())
    sb = set(b.lower().split())
    if not sa or not sb:
        return 0.0
    inter = len(sa & sb)
    union = max(1, len(sa | sb))
    return inter / union


def plan_context(
    rows: Iterable[ScoredChunk], cfg: PlanConfig | None = None
) -> list[ScoredChunk]:
    cfg = cfg or PlanConfig()
    # sort theo score giảm dần
    sorted_rows = sorted(rows, key=lambda r: r.score, reverse=True)
    picked: list[ScoredChunk] = []
    per_doc: dict[str, int] = {}
    for r in sorted_rows:
        if len(picked) >= cfg.k:
            break
        doc = r.chunk.doc_id
        if per_doc.get(doc, 0) >= cfg.per_doc_cap:
            continue
        # chống trùng lặp đơn giản: bỏ nếu quá giống với bất kỳ đã chọn
        dup = False
        for p in picked:
            if _jaccard(r.chunk.text, p.chunk.text) >= cfg.redundancy_threshold:
                dup = True
                break
        if dup:
            continue
        picked.append(r)
        per_doc[doc] = per_doc.get(doc, 0) + 1
    return picked
