from __future__ import annotations

import math
import re
from collections import Counter
from typing import Any
import a
import any
import b
import ch
import chunks
import dict
import doc_id
import filters
import float
import int
import k
import len
import list
import max
import max_tokens
import metadata
import query
import scored
import self
import staticmethod
import str
import sum
import t
import text
import top_k
import tuple
import v
import vec
import words
import x

_TOKEN_RE = re.compile(r"\w+", flags=re.UNICODE)


def _tokenize(text: str) -> list[str]:
    return [t.lower() for t in _TOKEN_RE.findall(text or "")]


class _SimpleEmbedder:
    """TF vector (L2-normalized) – stdlib-only."""

    def embed(self, text: str) -> dict[str, float]:
        toks = _tokenize(text)
        if not toks:
            return {}
        cnt = Counter(toks)
        vec: dict[str, float] = {k: float(v) for k, v in cnt.items()}
        norm = math.sqrt(sum(v * v for v in vec.values()))
        if norm <= 0.0:
            return {}
        for k in vec:
            vec[k] /= norm
        return vec


def _cosine(a: dict[str, float], b: dict[str, float]) -> float:
    if not a or not b:
        return 0.0
    if len(a) > len(b):
        a, b = b, a
    s = 0.0
    for k, v in a.items():
        bv = b.get(k)
        if bv is not None:
            s += v * bv
    return float(s)


class MemoryPipeline:
    """Local semantic pipeline: ingest → retrieve → compress (process-local)."""

    def __init__(self) -> None:
        self._emb = _SimpleEmbedder()
        self._vecs: dict[str, dict[str, float]] = {}
        self._meta: dict[str, dict[str, Any]] = {}
        self._texts: dict[str, str] = {}

    def ingest(
        self, doc_id: str, text: str, metadata: dict[str, Any] | None = None
    ) -> None:
        meta = metadata or {}
        self._vecs[doc_id] = self._emb.embed(text)
        self._meta[doc_id] = meta
        self._texts[doc_id] = text

    def retrieve(
        self, query: str, top_k: int = 5, filters: dict[str, Any] | None = None
    ) -> list[tuple[str, float, str, dict[str, Any]]]:
        qv = self._emb.embed(query)
        scored: list[tuple[str, float, str, dict[str, Any]]] = []
        for doc_id, vec in self._vecs.items():
            meta = self._meta.get(doc_id, {})
            if filters and any(meta.get(k) != v for k, v in filters.items()):
                continue
            score = _cosine(qv, vec)
            if score > 0.0:
                scored.append((doc_id, score, self._texts.get(doc_id, ""), meta))
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[: max(0, top_k)]

    @staticmethod
    def compress_context(chunks: list[str], max_tokens: int) -> str:
        if max_tokens <= 0:
            return ""
        words: list[str] = []
        for ch in chunks:
            ws = ch.split()
            if not ws:
                continue
            if len(words) + len(ws) <= max_tokens:
                words.extend(ws)
            else:
                remain = max_tokens - len(words)
                if remain > 0:
                    words.extend(ws[:remain])
                break
        return " ".join(words)


__all__ = ["MemoryPipeline"]
