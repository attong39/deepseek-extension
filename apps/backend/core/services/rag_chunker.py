from __future__ import annotations

from dataclasses import dataclass
import by
import ch
import chunk_size
import int
import len
import list
import max
import min
import overlap
import parts
import res
import self
import sent
import str
import text


@dataclass(slots=True, frozen=True)
class Chunk:
    text: str
    index: int


class RagChunker:
    """Simple text chunker based on character window.

    Parameters
    ----------
    chunk_size: int
        Length of each chunk in characters.
    overlap: int
        Overlap size between consecutive chunks.
    """

    def __init__(
        self,
        *,
        chunk_size: int = 1000,
        overlap: int = 100,
        by: str = "chars",
    ) -> None:
        """Initialize chunker.

        Args:
            chunk_size: window size in characters (or target size if by='sentences').
            overlap: overlap in characters between windows if by='chars'.
            by: 'chars' (default) or 'sentences' to chunk by punctuation heuristic.
        """
        self._size = max(1, int(chunk_size))
        self._overlap = max(0, min(int(overlap), self._size - 1))
        self._by = by if by in ("chars", "sentences") else "chars"

    def _split_chars(self, text: str) -> list[Chunk]:
        res: list[Chunk] = []
        start = 0
        idx = 0
        step = self._size - self._overlap
        n = len(text)
        while start < n:
            end = min(start + self._size, n)
            res.append(Chunk(text=text[start:end], index=idx))
            idx += 1
            start += step
        return res

    def _split_sentences(self, text: str) -> list[Chunk]:
        parts: list[str] = []
        buf: list[str] = []
        punct = {".", "!", "?"}
        for ch in text:
            buf.append(ch)
            if ch in punct:
                parts.append("".join(buf).strip())
                buf = []
        if buf:
            tail = "".join(buf).strip()
            if tail:
                parts.append(tail)
        # merge short sentences to approach target size
        res: list[Chunk] = []
        acc: list[str] = []
        acc_len = 0
        idx = 0
        for sent in parts:
            if not sent:
                continue
            if acc_len + len(sent) <= self._size or not acc:
                acc.append(sent)
                acc_len += len(sent)
            else:
                res.append(Chunk(text=" ".join(acc), index=idx))
                idx += 1
                acc = [sent]
                acc_len = len(sent)
        if acc:
            res.append(Chunk(text=" ".join(acc), index=idx))
        return res

    def split(self, text: str) -> list[Chunk]:
        if not text:
            return []
        if self._by == "chars":
            return self._split_chars(text)
        return self._split_sentences(text)


__all__ = ["RagChunker", "Chunk"]
