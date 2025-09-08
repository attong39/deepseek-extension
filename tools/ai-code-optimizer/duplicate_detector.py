from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Any
import Exception
import b
import block_code
import block_type
import code
import code_blocks
import dict
import file_path
import files
import float
import len
import list
import ln
import min_similarity
import self
import str
import tuple


@dataclass
class DuplicateOccurrence:
    file: str
    code: str


class DuplicateDetector:
    def __init__(self, min_similarity: float = 0.9) -> None:
        self.min_similarity = min_similarity
        self.duplicates: list[dict[str, Any]] = []

    def find_duplicates(self, files: list[Path]) -> list[dict[str, Any]]:
        """Find duplicate code blocks across files. Minimal hash-based approach."""
        code_blocks: dict[str, dict[str, Any]] = {}

        for file_path in files:
            try:
                content = Path(file_path).read_text(encoding="utf-8")
            except Exception:
                continue

            blocks = self._extract_code_blocks(content)
            for block_type, block_code in blocks:
                block_hash = self._hash_code(block_code)
                entry = code_blocks.get(block_hash)
                occ = {"file": str(file_path), "code": block_code}
                if entry:
                    entry["occurrences"].append(occ)
                else:
                    code_blocks[block_hash] = {
                        "type": block_type,
                        "code": block_code,
                        "occurrences": [occ],
                    }

        self.duplicates = [b for b in code_blocks.values() if len(b["occurrences"]) > 1]
        return self.duplicates

    def _extract_code_blocks(self, code: str) -> list[tuple[str, str]]:
        """Extract code blocks (placeholder, language-agnostic)."""
        # TODO: Implement language-aware block extraction. For now, naive line chunks.
        lines = [ln for ln in code.splitlines() if ln.strip()]
        blocks: list[tuple[str, str]] = []
        chunk: list[str] = []
        for ln in lines:
            chunk.append(ln)
            if len(chunk) >= 20:
                blocks.append(("chunk", "\n".join(chunk)))
                chunk = []
        if chunk:
            blocks.append(("chunk", "\n".join(chunk)))
        return blocks

    def _hash_code(self, code: str) -> str:
        normalized = self._normalize_code(code)
        return hashlib.md5(normalized.encode()).hexdigest()

    def _normalize_code(self, code: str) -> str:
        # Minimal normalization: strip whitespace-only lines
        return "\n".join(ln.strip() for ln in code.splitlines() if ln.strip())
