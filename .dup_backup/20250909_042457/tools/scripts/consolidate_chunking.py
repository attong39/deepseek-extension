#!/usr/bin/env python3
"""
Script tự động hợp nhất và làm sạch chunking code trùng lặp.

Thực hiện theo CHUNKING_CONSOLIDATION_PLAN.md
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path
import Exception
import bool
import cmd
import e
import f
import new_pattern
import old_pattern
import open
import print
import step_func
import step_name
import str


def run_command(cmd: str) -> bool:
    """Chạy command và trả về success status."""
    try:
        result = subprocess.run(cmd, shell=False, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ Error: {cmd}")
            print(f"   stdout: {result.stdout}")
            print(f"   stderr: {result.stderr}")
            return False
        return True
    except Exception as e:
        print(f"❌ Exception running {cmd}: {e}")
        return False


def backup_files() -> bool:
    """Backup các file sẽ bị thay đổi."""
    print("📦 Creating backup...")
    backup_dir = Path("_backup_chunking")
    backup_dir.mkdir(exist_ok=True)

    files_to_backup = [
        "zeta_vn/core/services/rag_chunker.py",
        "zeta_vn/core/services/chunking.py",
        "zeta_vn/core/services/retrieval_service.py",
        "zeta_vn/core/adapters/vector/chunking_service.py",
        "zeta_vn/tests/unit/test_rag_chunker_sentences.py",
        "zeta_vn/tests/unit/test_rag_services.py",
    ]

    for file_path in files_to_backup:
        if Path(file_path).exists():
            dest = backup_dir / Path(file_path).name
            shutil.copy2(file_path, dest)
            print(f"   ✅ Backed up {file_path}")

    return True


def create_unified_chunk_entity() -> bool:
    """Tạo unified Chunk entity trong domain."""
    print("🏗️ Creating unified Chunk entity...")

    chunk_entity_content = '''"""Unified Chunk entity for ZETA AI system."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class Chunk:
    """
    Unified chunk entity cho all chunking needs.
    
    Replaces duplicate Chunk classes across multiple modules.
    """
    text: str
    start: int
    end: int
    index: int
    metadata: dict[str, Any] = field(default_factory=dict)
    
    @property
    def length(self) -> int:
        """Get chunk length in characters."""
        return len(self.text)
        
    @property
    def word_count(self) -> int:
        """Estimate word count."""
        return len(self.text.split())


@dataclass(frozen=True, slots=True)
class ScoredChunk:
    """Chunk với relevance score cho retrieval."""
    chunk: Chunk
    score: float
    
    def __lt__(self, other: ScoredChunk) -> bool:
        """Enable sorting by score."""
        return self.score < other.score


__all__ = ["Chunk", "ScoredChunk"]
'''

    entity_path = Path("zeta_vn/core/domain/entities/Chunk.py")
    entity_path.parent.mkdir(parents=True, exist_ok=True)

    with open(entity_path, "w", encoding="utf-8") as f:
        f.write(chunk_entity_content)

    print(f"   ✅ Created {entity_path}")
    return True


def create_chunking_port() -> bool:
    """Tạo ChunkingPort interface."""
    print("🔌 Creating ChunkingPort interface...")

    port_content = '''"""Chunking port interface for dependency inversion."""

from __future__ import annotations

from typing import Protocol

from apps.backend.core.domain.entities.Chunk import Chunk


class ChunkingPort(Protocol):
    """Port interface for chunking services."""
    
    def chunk(
        self,
        text: str,
        *,
        strategy: str = "sentence",
        chunk_size: int = 1000,
        overlap: int = 100,
    ) -> list[Chunk]:
        """
        Chunk text into smaller pieces.
        
        Args:
            text: Text to chunk
            strategy: Chunking strategy ("simple", "sentence", "semantic", "token")
            chunk_size: Target chunk size
            overlap: Overlap between chunks
            
        Returns:
            List of chunks
        """
        ...
    
    def estimate_chunks(self, text: str, chunk_size: int = 1000) -> int:
        """Estimate number of chunks without actual splitting."""
        ...


__all__ = ["ChunkingPort"]
'''

    port_path = Path("zeta_vn/core/domain/ports/chunking_port.py")
    port_path.parent.mkdir(parents=True, exist_ok=True)

    with open(port_path, "w", encoding="utf-8") as f:
        f.write(port_content)

    print(f"   ✅ Created {port_path}")
    return True


def consolidate_chunking_service() -> bool:
    """Hợp nhất tất cả logic chunking vào một service."""
    print("🔧 Consolidating chunking service...")

    # Đọc content từ file gốc
    original_path = Path("zeta_vn/core/services/chunking.py")
    if not original_path.exists():
        print("❌ Original chunking.py not found")
        return False

    with open(original_path, encoding="utf-8") as f:
        f.read()

    # Enhanced content với merged logic
    enhanced_content = '''"""Unified chunking service - consolidates all chunking logic.

Merges functionality from:
- rag_chunker.py (simple character chunking)
- chunking.py (token-aware chunking)
- chunking_service.py (enhanced strategies)
- semantic_chunking.py (semantic strategies)
"""

from __future__ import annotations

from dataclasses import dataclass
import logging
import math
import re
from typing import Literal

from apps.backend.core.domain.entities.Chunk import Chunk
from apps.backend.core.domain.ports.chunking_port import ChunkingPort


logger = logging.getLogger(__name__)

ChunkStrategy = Literal["simple", "sentence", "semantic", "token", "markdown", "code"]


def _try_get_encoding(name: str):  # type: ignore[no-untyped-def]
    """Try to import tiktoken encoding."""
    try:
        import tiktoken  # type: ignore  # noqa: PLC0415
        return tiktoken.get_encoding(name)
    except Exception:
        return None


class UnifiedChunkingService(ChunkingPort):
    """
    Unified chunking service combining all strategies.
    
    Consolidates logic from multiple duplicate chunking implementations.
    """
    
    def __init__(
        self,
        *,
        default_strategy: ChunkStrategy = "sentence",
        default_chunk_size: int = 1000,
        default_overlap: int = 100,
        encoding_name: str = "cl100k_base",
    ) -> None:
        """Initialize unified chunking service."""
        self.default_strategy = default_strategy
        self.default_chunk_size = default_chunk_size
        self.default_overlap = default_overlap
        self.encoding = _try_get_encoding(encoding_name)
        
        logger.info(
            "UnifiedChunkingService initialized: strategy=%s, size=%d, overlap=%d",
            default_strategy, default_chunk_size, default_overlap
        )
    
    def chunk(
        self,
        text: str,
        *,
        strategy: str = None,
        chunk_size: int = None,
        overlap: int = None,
    ) -> list[Chunk]:
        """Main chunking method with strategy dispatch."""
        if not text.strip():
            return []
        
        strategy = strategy or self.default_strategy
        chunk_size = chunk_size or self.default_chunk_size
        overlap = overlap or self.default_overlap
        
        try:
            if strategy == "simple":
                return self._chunk_simple(text, chunk_size, overlap)
            elif strategy == "sentence":
                return self._chunk_sentence(text, chunk_size, overlap)
            elif strategy == "semantic":
                return self._chunk_semantic(text, chunk_size, overlap)
            elif strategy == "token":
                return self._chunk_token_aware(text, chunk_size, overlap)
            elif strategy == "markdown":
                return self._chunk_markdown(text, chunk_size, overlap)
            elif strategy == "code":
                return self._chunk_code(text, chunk_size, overlap)
            else:
                logger.warning(f"Unknown strategy {strategy}, using sentence")
                return self._chunk_sentence(text, chunk_size, overlap)
        except Exception:
            logger.exception(f"Chunking failed with strategy {strategy}, fallback to simple")
            return self._chunk_simple(text, chunk_size, overlap)
    
    def estimate_chunks(self, text: str, chunk_size: int = None) -> int:
        """Estimate number of chunks."""
        chunk_size = chunk_size or self.default_chunk_size
        return max(1, len(text) // chunk_size)
    
    # Strategy implementations
    
    def _chunk_simple(self, text: str, chunk_size: int, overlap: int) -> list[Chunk]:
        """Simple character-based chunking (from rag_chunker.py)."""
        chunks = []
        start = 0
        index = 0
        step = chunk_size - overlap
        
        while start < len(text):
            end = min(start + chunk_size, len(text))
            chunk_text = text[start:end].strip()
            
            if chunk_text:
                chunks.append(Chunk(
                    text=chunk_text,
                    start=start,
                    end=end,
                    index=index,
                    metadata={"strategy": "simple"}
                ))
                index += 1
            
            start += step
            if start >= len(text):
                break
        
        return chunks
    
    def _chunk_sentence(self, text: str, chunk_size: int, overlap: int) -> list[Chunk]:
        """Sentence-aware chunking."""
        # Split by sentence endings
        sentences = re.split(r'(?<=[.!?])\\s+', text)
        chunks = []
        current_chunk = ""
        current_start = 0
        index = 0
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
                
            # Check if adding sentence exceeds chunk size
            if len(current_chunk) + len(sentence) + 1 > chunk_size and current_chunk:
                # Save current chunk
                chunks.append(Chunk(
                    text=current_chunk.strip(),
                    start=current_start,
                    end=current_start + len(current_chunk),
                    index=index,
                    metadata={"strategy": "sentence"}
                ))
                index += 1
                
                # Start new chunk with overlap
                if overlap > 0:
                    overlap_text = current_chunk[-overlap:] if len(current_chunk) > overlap else current_chunk
                    current_chunk = overlap_text + " " + sentence
                else:
                    current_chunk = sentence
                    current_start = text.find(sentence, current_start)
            else:
                if not current_chunk:
                    current_start = text.find(sentence)
                current_chunk += " " + sentence if current_chunk else sentence
        
        # Add final chunk
        if current_chunk.strip():
            chunks.append(Chunk(
                text=current_chunk.strip(),
                start=current_start,
                end=current_start + len(current_chunk),
                index=index,
                metadata={"strategy": "sentence"}
            ))
        
        return chunks
    
    def _chunk_semantic(self, text: str, chunk_size: int, overlap: int) -> list[Chunk]:
        """Semantic chunking using paragraph boundaries."""
        # Split by double newlines (paragraphs)
        paragraphs = [p.strip() for p in text.split("\\n\\n") if p.strip()]
        
        chunks = []
        current_chunk = ""
        current_start = 0
        index = 0
        
        for paragraph in paragraphs:
            if len(current_chunk) + len(paragraph) + 2 > chunk_size and current_chunk:
                # Save current chunk
                chunks.append(Chunk(
                    text=current_chunk.strip(),
                    start=current_start,
                    end=current_start + len(current_chunk),
                    index=index,
                    metadata={"strategy": "semantic"}
                ))
                index += 1
                
                # Start new chunk
                current_chunk = paragraph
                current_start = text.find(paragraph, current_start)
            else:
                if not current_chunk:
                    current_start = text.find(paragraph)
                current_chunk += "\\n\\n" + paragraph if current_chunk else paragraph
        
        # Add final chunk
        if current_chunk.strip():
            chunks.append(Chunk(
                text=current_chunk.strip(),
                start=current_start,
                end=current_start + len(current_chunk),
                index=index,
                metadata={"strategy": "semantic"}
            ))
        
        return chunks
    
    def _chunk_token_aware(self, text: str, max_tokens: int, overlap: int) -> list[Chunk]:
        """Token-aware chunking with tiktoken (from chunking.py)."""
        if self.encoding is None:
            # Fallback to word-based estimation
            return self._chunk_by_words(text, max_tokens, overlap)
        
        # Encode text to tokens
        token_ids = self.encoding.encode(text)
        chunks = []
        start_idx = 0
        index = 0
        
        while start_idx < len(token_ids):
            # Get token window
            end_idx = min(start_idx + max_tokens, len(token_ids))
            window_tokens = token_ids[start_idx:end_idx]
            
            # Decode back to text
            chunk_text = self.encoding.decode(window_tokens)
            
            # Calculate character positions (approximate)
            char_start = len(self.encoding.decode(token_ids[:start_idx]))
            char_end = char_start + len(chunk_text)
            
            chunks.append(Chunk(
                text=chunk_text,
                start=char_start,
                end=char_end,
                index=index,
                metadata={"strategy": "token", "tokens": len(window_tokens)}
            ))
            
            index += 1
            start_idx += max(1, max_tokens - overlap)
            
            if start_idx >= len(token_ids):
                break
        
        return chunks
    
    def _chunk_by_words(self, text: str, max_tokens: int, overlap: int) -> list[Chunk]:
        """Word-based chunking as fallback for token-aware."""
        words = text.split()
        if not words:
            return []
        
        # Estimate words per chunk (0.75 word/token ratio)
        words_per_chunk = max(1, int(max_tokens * 0.75))
        overlap_words = max(0, int(overlap * 0.75))
        
        chunks = []
        start_word_idx = 0
        index = 0
        
        while start_word_idx < len(words):
            end_word_idx = min(start_word_idx + words_per_chunk, len(words))
            chunk_words = words[start_word_idx:end_word_idx]
            chunk_text = " ".join(chunk_words)
            
            # Approximate character positions
            char_start = len(" ".join(words[:start_word_idx]))
            if start_word_idx > 0:
                char_start += 1  # Account for space
            char_end = char_start + len(chunk_text)
            
            chunks.append(Chunk(
                text=chunk_text,
                start=char_start,
                end=char_end,
                index=index,
                metadata={"strategy": "token_words", "word_count": len(chunk_words)}
            ))
            
            index += 1
            start_word_idx += max(1, words_per_chunk - overlap_words)
        
        return chunks
    
    def _chunk_markdown(self, text: str, chunk_size: int, overlap: int) -> list[Chunk]:
        """Markdown-aware chunking preserving headers."""
        # Split by markdown headers
        sections = re.split(r'(?m)^(#{1,6}\\s+.*?)$', text)
        
        chunks = []
        index = 0
        pos = 0
        
        for section in sections:
            section = section.strip()
            if not section:
                continue
            
            section_start = text.find(section, pos)
            if section_start == -1:
                section_start = pos
            
            if len(section) <= chunk_size:
                # Header level detection
                header_match = re.match(r'^(#{1,6})\\s+', section)
                metadata = {"strategy": "markdown"}
                if header_match:
                    metadata["header_level"] = len(header_match.group(1))
                
                chunks.append(Chunk(
                    text=section,
                    start=section_start,
                    end=section_start + len(section),
                    index=index,
                    metadata=metadata
                ))
                index += 1
            else:
                # Split large sections
                sub_chunks = self._chunk_simple(section, chunk_size, overlap)
                for sub_chunk in sub_chunks:
                    chunks.append(Chunk(
                        text=sub_chunk.text,
                        start=section_start + sub_chunk.start,
                        end=section_start + sub_chunk.end,
                        index=index,
                        metadata={"strategy": "markdown", "sub_chunk": True}
                    ))
                    index += 1
            
            pos = section_start + len(section)
        
        return chunks
    
    def _chunk_code(self, text: str, chunk_size: int, overlap: int) -> list[Chunk]:
        """Code-aware chunking preserving function boundaries."""
        # Try to split by code blocks first
        if "```" in text:
            sections = re.split(r'```.*?```', text, flags=re.DOTALL)
        else:
            # Split by function/class definitions
            sections = re.split(r'(?m)^(def |class |function |var )', text)
        
        chunks = []
        index = 0
        pos = 0
        
        for section in sections:
            section = section.strip()
            if not section:
                continue
            
            section_start = text.find(section, pos)
            if section_start == -1:
                section_start = pos
            
            if len(section) <= chunk_size:
                chunks.append(Chunk(
                    text=section,
                    start=section_start,
                    end=section_start + len(section),
                    index=index,
                    metadata={"strategy": "code"}
                ))
                index += 1
            else:
                # Split large code sections
                sub_chunks = self._chunk_simple(section, chunk_size, overlap)
                for sub_chunk in sub_chunks:
                    chunks.append(Chunk(
                        text=sub_chunk.text,
                        start=section_start + sub_chunk.start,
                        end=section_start + sub_chunk.end,
                        index=index,
                        metadata={"strategy": "code", "sub_chunk": True}
                    ))
                    index += 1
            
            pos = section_start + len(section)
        
        return chunks


# Legacy compatibility aliases
RagChunker = UnifiedChunkingService  # compat with rag_chunker.py
TokenChunker = UnifiedChunkingService  # compat with chunking.py
ChunkingService = UnifiedChunkingService  # compat with adapters


__all__ = [
    "UnifiedChunkingService",
    "ChunkingService",
    "RagChunker",
    "TokenChunker",
    "ChunkStrategy"
]
'''

    # Write consolidated service
    new_path = Path("zeta_vn/core/services/unified_chunking_service.py")
    with open(new_path, "w", encoding="utf-8") as f:
        f.write(enhanced_content)

    print(f"   ✅ Created {new_path}")
    return True


def update_retrieval_service() -> bool:
    """Update retrieval_service.py để remove duplicate Chunk class."""
    print("🔄 Updating retrieval_service.py...")

    file_path = Path("zeta_vn/core/services/retrieval_service.py")
    if not file_path.exists():
        print(f"❌ {file_path} not found")
        return False

    with open(file_path, encoding="utf-8") as f:
        content = f.read()

    # Remove duplicate Chunk and ScoredChunk class definitions
    # Add import from domain entity
    updated_content = content.replace(
        'from dataclasses import dataclass\nimport logging\nimport math\nfrom typing import Protocol\n\n\nlogger = logging.getLogger(__name__)\n\n\n@dataclass(slots=True)\nclass Chunk:\n    """Một đoạn văn bản đã chunk để index/search.\n\n    Args:\n        id: id duy nhất của chunk.\n        doc_id: id tài liệu gốc.\n        text: nội dung chunk.\n        meta: metadata kèm theo.\n    """\n\n    id: str\n    doc_id: str\n    text: str\n    meta: dict[str, str]\n\n\n@dataclass(slots=True)\nclass ScoredChunk:\n    chunk: Chunk\n    score: float',
        "import logging\nimport math\nfrom typing import Protocol\n\nfrom apps.backend.core.domain.entities.Chunk import Chunk, ScoredChunk\n\n\nlogger = logging.getLogger(__name__)",
    )

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(updated_content)

    print(f"   ✅ Updated {file_path}")
    return True


def update_imports_across_codebase() -> bool:
    """Update imports throughout codebase to use unified service."""
    print("🔄 Updating imports across codebase...")

    # Find files that import old chunking modules
    search_patterns = [
        (
            "from apps.backend.core.services.rag_chunker import",
            "from apps.backend.core.services.unified_chunking_service import",
        ),
        (
            "from apps.backend.core.services.chunking import",
            "from apps.backend.core.services.unified_chunking_service import",
        ),
        ("RagChunker", "UnifiedChunkingService"),
        ("TokenChunker", "UnifiedChunkingService"),
    ]

    # Files to update
    update_files = [
        "zeta_vn/tests/unit/test_rag_chunker_sentences.py",
        "zeta_vn/tests/unit/test_rag_services.py",
    ]

    for file_path in update_files:
        path = Path(file_path)
        if not path.exists():
            continue

        with open(path, encoding="utf-8") as f:
            content = f.read()

        # Apply replacements
        for old_pattern, new_pattern in search_patterns:
            content = content.replace(old_pattern, new_pattern)

        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"   ✅ Updated {path}")

    return True


def run_tests() -> bool:
    """Run tests to verify consolidation worked."""
    print("🧪 Running tests...")

    # Run chunking-related tests
    test_commands = [
        "uv run pytest tests/unit/test_rag_chunker_sentences.py -v",
        "uv run pytest tests/unit/test_rag_services.py -v",
        "uv run pytest tests/unit/ -k chunk -v",
    ]

    for cmd in test_commands:
        print(f"   Running: {cmd}")
        if not run_command(cmd):
            print(f"   ❌ Test failed: {cmd}")
            return False
        print(f"   ✅ Passed: {cmd}")

    return True


def clean_up_old_files() -> bool:
    """Delete old duplicate files."""
    print("🧹 Cleaning up old duplicate files...")

    files_to_delete = [
        "zeta_vn/core/services/rag_chunker.py",
        "zeta_vn/core/adapters/vector/chunking_service.py",
    ]

    for file_path in files_to_delete:
        path = Path(file_path)
        if path.exists():
            path.unlink()
            print(f"   ✅ Deleted {path}")
        else:
            print(f"   ⚠️ Not found: {path}")

    return True


def main() -> bool:
    """Main consolidation execution."""
    print("🚀 Starting chunking code consolidation...")

    steps = [
        ("Backup files", backup_files),
        ("Create unified Chunk entity", create_unified_chunk_entity),
        ("Create ChunkingPort interface", create_chunking_port),
        ("Consolidate chunking service", consolidate_chunking_service),
        ("Update retrieval service", update_retrieval_service),
        ("Update imports", update_imports_across_codebase),
        ("Run tests", run_tests),
        ("Clean up old files", clean_up_old_files),
    ]

    for step_name, step_func in steps:
        print(f"\\n📝 {step_name}...")
        if not step_func():
            print(f"❌ Failed: {step_name}")
            return False
        print(f"✅ Completed: {step_name}")

    print("\\n🎉 Chunking consolidation completed successfully!")
    print("\\n📊 Summary:")
    print("  ✅ Created unified Chunk entity")
    print("  ✅ Created ChunkingPort interface")
    print("  ✅ Consolidated all chunking logic")
    print("  ✅ Updated imports across codebase")
    print("  ✅ Tests passing")
    print("  ✅ Cleaned up duplicate files")

    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
