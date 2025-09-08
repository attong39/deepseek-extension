"""
Hybrid Retriever combining Vector + Lexical Search.

Implements state-of-the-art hybrid retrieval with:
- Vector search via embeddings
- Lexical search via TF-IDF
- Score normalization and fusion
- Configurable alpha weighting
"""

from __future__ import annotations

from apps.backend.core.services.ai.rag.embed_interfaces import Embedder, VectorIndex
from apps.backend.core.services.ai.rag.lexical_index import LexicalIndex
from apps.backend.core.services.ai.rag.types import Chunk, Query, RetrievalResult
import ValueError
import alpha
import chunk
import chunk_idx_str
import chunks
import combined_score
import combined_scores
import dict
import doc_id
import embedder
import float
import h
import hit
import index
import int
import len
import lexical_index
import lexical_scores
import list
import max
import max_val
import meta
import min
import min_val
import norm_score
import query
import result
import results
import score
import self
import sorted
import str
import text
import val
import vector_scores
import x
import zip


def _min_max_normalize(values: list[float]) -> list[float]:
    """
    Min-max normalization to [0, 1] range.

    Args:
        values: List of numeric values to normalize

    Returns:
        Normalized values in [0, 1] range
    """
    if not values:
        return values

    min_val, max_val = min(values), max(values)

    # Handle edge case where all values are the same
    if max_val - min_val < 1e-9:
        return [1.0] * len(values)

    return [(val - min_val) / (max_val - min_val) for val in values]


class HybridRetriever:
    """
    Hybrid retrieval combining vector and lexical search.

    The hybrid approach uses:
    1. Vector search for semantic similarity
    2. Lexical search for exact term matching
    3. Score normalization and weighted fusion
    4. Configurable alpha for vector vs lexical weight

    Best practices:
    - alpha=0.6-0.7 works well for most domains
    - Higher alpha favors semantic similarity
    - Lower alpha favors exact term matching
    """

    def __init__(
        self,
        embedder: Embedder,
        index: VectorIndex,
        lexical_index: LexicalIndex,
        alpha: float = 0.6,
    ):
        """
        Initialize hybrid retriever.

        Args:
            embedder: Text embedding model
            index: Vector similarity index
            lexical_index: TF-IDF lexical index
            alpha: Weight for vector search (0.0 = lexical only, 1.0 = vector only)
        """
        self.embedder = embedder
        self.vector_index = index
        self.lexical_index = lexical_index
        self.alpha = alpha

        if not 0.0 <= alpha <= 1.0:
            raise ValueError(f"Alpha must be in [0, 1], got {alpha}")

    def add_chunks_to_lexical(self, chunks: list[Chunk]) -> None:
        """
        Add chunks to lexical index for hybrid search.

        Args:
            chunks: List of text chunks to index
        """
        for chunk in chunks:
            key = f"{chunk.doc_id}:{chunk.idx}"
            self.lexical_index.add(key, chunk.text, chunk.meta)

    def retrieve(self, query: Query) -> list[RetrievalResult]:
        """
        Perform hybrid retrieval combining vector and lexical search.

        Args:
            query: Search query with text and parameters

        Returns:
            List of retrieval results ranked by hybrid score
        """
        # Get more candidates than needed for better fusion
        candidate_k = query.top_k * 2

        # 1. Vector search
        query_embedding = self.embedder.embed_text(query.text)
        vector_hits = self.vector_index.search(query_embedding, top_k=candidate_k)

        # 2. Lexical search
        lexical_hits = self.lexical_index.search(query.text, top_k=candidate_k)

        # 3. Create score mappings
        vector_scores: dict[str, float] = {}
        lexical_scores: dict[str, float] = {}

        # Map vector hits
        for hit in vector_hits:
            key = f"{hit.doc_id}:{hit.chunk_idx}"
            vector_scores[key] = hit.score

        # Map lexical hits
        for key, score in lexical_hits:
            lexical_scores[key] = score

        # 4. Normalize scores to [0, 1] range
        if vector_scores:
            normalized_vector = _min_max_normalize(list(vector_scores.values()))
            for key, norm_score in zip(
                vector_scores.keys(), normalized_vector, strict=False
            ):
                vector_scores[key] = norm_score

        if lexical_scores:
            normalized_lexical = _min_max_normalize(list(lexical_scores.values()))
            for key, norm_score in zip(
                lexical_scores.keys(), normalized_lexical, strict=False
            ):
                lexical_scores[key] = norm_score

        # 5. Combine scores with weighted fusion
        combined_scores: dict[str, float] = {}

        # Add vector contribution
        for key, score in vector_scores.items():
            combined_scores[key] = combined_scores.get(key, 0.0) + self.alpha * score

        # Add lexical contribution
        for key, score in lexical_scores.items():
            combined_scores[key] = (
                combined_scores.get(key, 0.0) + (1.0 - self.alpha) * score
            )

        # 6. Create unified results
        vector_hits_dict = {f"{h.doc_id}:{h.chunk_idx}": h for h in vector_hits}
        results: list[RetrievalResult] = []

        # Sort by combined score and take top-k
        sorted_items = sorted(
            combined_scores.items(), key=lambda x: x[1], reverse=True
        )[: query.top_k]

        for key, combined_score in sorted_items:
            if key in vector_hits_dict:
                # Use existing vector hit result
                _ = vector_hits_dict[key]
                result.score = combined_score  # Update with hybrid score
                results.append(result)
            else:
                # Create result from lexical hit
                doc_id, chunk_idx_str = key.rsplit(":", 1)
                text, meta = self.lexical_index.get_document(key)

                if text is not None:
                    _ = RetrievalResult(
                        doc_id=doc_id,
                        chunk_idx=int(chunk_idx_str),
                        text=text,
                        score=combined_score,
                        meta=meta,
                    )
                    results.append(result)

        return results

    def get_stats(self) -> dict[str, int]:
        """Get retriever statistics."""
        return {
            "lexical_docs": self.lexical_index.size(),
            "lexical_vocab": self.lexical_index.vocabulary_size(),
            "alpha": self.alpha,
        }

    def set_alpha(self, alpha: float) -> None:
        """Update alpha parameter for vector/lexical weighting."""
        if not 0.0 <= alpha <= 1.0:
            raise ValueError(f"Alpha must be in [0, 1], got {alpha}")
        self.alpha = alpha
