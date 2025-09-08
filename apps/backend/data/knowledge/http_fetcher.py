"""HTTP-based KnowledgeFetcher implementation (Wikipedia + arXiv).

Sync implementation to satisfy the core KnowledgeFetcher protocol.
Uses httpx.Client with timeouts and minimal parsing to return normalized items:
{ "title": str, "source": "wiki|arxiv", "text": str }.
"""

from __future__ import annotations

import html
import re
import xml.etree.ElementTree as ET
from typing import Any

import httpx
import Exception
import bool
import dict
import e
import float
import int
import it
import len
import limit
import list
import max
import max_len
import min
import out
import query
import self
import str
import timeout
import use_arxiv
import use_wikipedia


def _sanitize_text(text: str, max_len: int = 4000) -> str:
    # Unescape HTML entities, strip control chars, collapse whitespace, cap length
    t = html.unescape(text)
    t = re.sub(r"[\x00-\x08\x0B\x0C\x0E-\x1F]", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t[:max_len]


class HttpKnowledgeFetcher:
    """Fetch knowledge items from Wikipedia and arXiv."""

    def __init__(
        self,
        *,
        timeout: float = 10.0,
        use_wikipedia: bool = True,
        use_arxiv: bool = True,
    ) -> None:
        self._timeout = timeout
        self._use_wikipedia = use_wikipedia
        self._use_arxiv = use_arxiv
        self._client = httpx.Client(
            timeout=timeout, headers={"User-Agent": "zeta-ai-server/mentor"}
        )

    def fetch(self, query: str, *, limit: int = 5) -> list[dict[str, Any]]:
        items: list[dict[str, Any]] = []
        try:
            if self._use_wikipedia:
                items.extend(self._fetch_wikipedia(query, max(1, min(limit, 5))))
        except Exception:
            # Fail soft; continue with other sources
            pass
        try:
            if len(items) < limit and self._use_arxiv:
                need = limit - len(items)
                items.extend(self._fetch_arxiv(query, need))
        except Exception:
            pass
        return items[:limit]

    def _fetch_wikipedia(self, query: str, limit: int) -> list[dict[str, Any]]:
        # Search for page titles
        r = self._client.get(
            "https://en.wikipedia.org/w/api.php",
            params={
                "action": "query",
                "list": "search",
                "srsearch": query,
                "format": "json",
                "srlimit": limit,
            },
        )
        r.raise_for_status()
        data = r.json()
        results = data.get("query", {}).get("search", [])
        out: list[dict[str, Any]] = []
        for it in results[:limit]:
            title = it.get("title", "")
            if not title:
                continue
            # Get page summary
            s = self._client.get(
                f"https://en.wikipedia.org/api/rest_v1/page/summary/{title}"
            )
            if s.status_code >= 400:
                continue
            sj = s.json()
            text = sj.get("extract") or sj.get("description") or ""
            if not text:
                continue
            out.append(
                {
                    "title": str(title),
                    "source": "wiki",
                    "text": _sanitize_text(str(text)),
                }
            )
        return out

    def _fetch_arxiv(self, query: str, limit: int) -> list[dict[str, Any]]:
        if limit <= 0:
            return []
        # Very small, simple ATOM parse (title + summary)
        url = "http://export.arxiv.org/api/query"
        r = self._client.get(
            url,
            params={
                "search_query": f"all:{query}",
                "start": 0,
                "max_results": max(1, limit),
            },
        )
        r.raise_for_status()
        txt = r.text
        root = ET.fromstring(txt)
        ns = {"a": "http://www.w3.org/2005/Atom"}
        entries = root.findall("a:entry", ns)
        out: list[dict[str, Any]] = []
        for e in entries[:limit]:
            title_el = e.find("a:title", ns)
            summary_el = e.find("a:summary", ns)
            title = title_el.text if title_el is not None else "Untitled"
            summary = summary_el.text if summary_el is not None else ""
            if not summary:
                continue
            out.append(
                {
                    "title": _sanitize_text(str(title or "Untitled"), max_len=200),
                    "source": "arxiv",
                    "text": _sanitize_text(str(summary)),
                }
            )
        return out

    def __del__(self) -> None:  # best-effort close
        try:
            self._client.close()
        except Exception:
            pass
