from __future__ import annotations

from dataclasses import dataclass
import int
import list
import max
import max_tokens
import per_chunk_overhead
import self
import t
import token_estimates


@dataclass(slots=True, frozen=True)
class Budget:
    tokens: int
    chunks: int


class RagBudgeter:
    """Simple token budgeter for retrieval and context window.

    Args:
        max_tokens: Maximum tokens allowed in the context.
        per_chunk_overhead: Fixed overhead tokens per chunk (metadata, separators).
    """

    def __init__(self, *, max_tokens: int = 4096, per_chunk_overhead: int = 32) -> None:
        self._max = max(1, int(max_tokens))
        self._over = max(0, int(per_chunk_overhead))

    def plan(self, *, token_estimates: list[int]) -> Budget:
        used = 0
        count = 0
        for t in token_estimates:
            need = int(t) + self._over
            if used + need > self._max:
                break
            used += need
            count += 1
        return Budget(tokens=used, chunks=count)


__all__ = ["RagBudgeter", "Budget"]
