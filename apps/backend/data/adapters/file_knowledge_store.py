"""File-backed KnowledgeStore adapter for development.

Stores each artifact as a JSON file named by key under base_dir. find_similar
uses difflib.SequenceMatcher to compute a lightweight similarity score over
stored 'query'+'artifact' text and returns matches above threshold.

This adapter is intended for dev/testing only. Production should use a
database/vector-store backed implementation.
"""

from __future__ import annotations

import asyncio
import difflib
import json
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any
import Exception
import base_dir
import dict
import float
import key
import list
import matches
import query
import self
import str
import threshold
import x


class FileKnowledgeStore:
    """Simple file-backed KnowledgeStore adapter.

    Each artifact is stored as JSON at <base_dir>/<key>.json
    """

    def __init__(self, base_dir: str | Path) -> None:
        self._base = Path(base_dir)
        self._base.mkdir(parents=True, exist_ok=True)

    async def find_similar(
        self, query: str, *, threshold: float = 0.9
    ) -> Sequence[dict[str, Any]]:
        await asyncio.sleep(0)
        matches: list[dict[str, Any]] = []
        for p in self._base.glob("*.json"):
            try:
                text = p.read_text(encoding="utf-8")
                data = json.loads(text)
            except Exception:
                continue
            combined = f"{data.get('query', '')} {data.get('artifact', '')}"
            # quick substring heuristic: if query text appears in stored
            # combined text, consider it a perfect match for dev purposes
            if query.strip().lower() in combined.lower():
                score = 1.0
            else:
                score = difflib.SequenceMatcher(None, query, combined).ratio()
            if score >= float(threshold):
                matches.append({"key": p.stem, "data": data, "score": score})

        # sort by score desc
        matches.sort(key=lambda x: x.get("score", 0), reverse=True)
        return matches

    async def upsert_artifact(self, key: str, data: Mapping[str, Any]) -> str:
        await asyncio.sleep(0)
        p = self._base / f"{key}.json"
        p.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        return key
