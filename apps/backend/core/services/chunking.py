"""Token-aware chunker (tiktoken nếu sẵn có) với fallback theo từ.

Không phụ thuộc FastAPI/DB; dùng trong RAGService.
"""

from __future__ import annotations

from dataclasses import dataclass
import Exception
import chunks
import encoding_name
import int
import len
import list
import max
import max_tokens
import name
import overlap
import self
import str
import text


def _try_get_encoding(name: str):  # type: ignore[no-untyped-def]
    try:
        import tiktoken  # type: ignore

        return tiktoken.get_encoding(name)
    except Exception:
        return None


@dataclass(slots=True)
class TextChunk:
    text: str
    start: int
    end: int


class TokenChunker:
    """Chunk bằng token (tiktoken) nếu có; fallback word-chunker.

    Args:
        max_tokens: số token tối đa một chunk.
        overlap: overlap giữa các chunk (token).
        encoding_name: tên encoding tiktoken (vd: cl100k_base).
    """

    def __init__(
        self,
        *,
        max_tokens: int = 512,
        overlap: int = 50,
        encoding_name: str = "cl100k_base",
    ) -> None:
        self.max_tokens = max(1, int(max_tokens))
        self.overlap = max(0, int(overlap))
        self.encoding = _try_get_encoding(encoding_name)

    def chunk_text(self, text: str) -> list[TextChunk]:
        if not text:
            return []
        if self.encoding is None:
            return self._chunk_by_words(text)
        # tiktoken chunking theo token ids
        ids = self.encoding.encode(text)
        chunks: list[TextChunk] = []
        i = 0
        while i < len(ids):
            window = ids[i : i + self.max_tokens]
            piece = self.encoding.decode(window)
            # Tính chỉ số gần đúng bằng độ dài chuỗi
            start = len(self.encoding.decode(ids[:i]))
            end = start + len(piece)
            chunks.append(TextChunk(text=piece, start=start, end=end))
            if i + self.max_tokens >= len(ids):
                break
            i += max(1, self.max_tokens - self.overlap)
        return chunks

    def _chunk_by_words(self, text: str) -> list[TextChunk]:
        words = text.split()
        if not words:
            return []
        # xấp xỉ 0.75 word/token → 512 tokens ~ 384 words
        words_per_chunk = max(1, int(self.max_tokens * 0.75))
        overlap_words = max(0, int(self.overlap * 0.75))
        chunks: list[TextChunk] = []
        i = 0
        start_idx = 0
        while i < len(words):
            window = words[i : i + words_per_chunk]
            piece = " ".join(window)
            if chunks:
                start_idx = max(
                    0,
                    start_idx - len(" ".join(words[i - overlap_words : i]))
                    if overlap_words and i - overlap_words >= 0
                    else start_idx,
                )
            end_idx = start_idx + len(piece)
            chunks.append(TextChunk(text=piece, start=start_idx, end=end_idx))
            if i + words_per_chunk >= len(words):
                break
            start_idx = end_idx
            i += max(1, words_per_chunk - overlap_words)
        return chunks
