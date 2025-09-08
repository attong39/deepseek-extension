"""
Hybrid Search Engine combining BM25 + Vector Similarity.

Provides advanced retrieval capabilities with lexical + semantic matching.
"""

from __future__ import annotations

import logging
import math
from collections import Counter, defaultdict
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any

from apps.backend.data.adapters.vector.memory_vector_store import (
import bm25_score
import config
import count
import data
import dict
import doc_id
import doc_scores
import documents
import float
import fused_scores
import int
import len
import list
import max
import query
import result
import self
import str
import term
import text
import tf
import vector_results
import x
    Document,
    SearchResult,
    Vector,
)

logger = logging.getLogger(__name__)


@dataclass
class HybridSearchConfig:
    """Configuration for hybrid search."""

    # Vector search params
    vector_weight: float = 0.6  # Weight for semantic similarity
    vector_top_k: int = 50  # Initial vector candidates

    # BM25 params
    lexical_weight: float = 0.4  # Weight for lexical matching
    k1: float = 1.2  # Term frequency saturation parameter
    b: float = 0.75  # Length normalization parameter

    # Result fusion
    final_top_k: int = 10  # Final results to return
    min_score_threshold: float = 0.1  # Minimum score to include


class BM25Scorer:
    """BM25 scoring for lexical search."""

    def __init__(self, documents: Sequence[Document], config: HybridSearchConfig):
        """Initialize BM25 with document corpus."""
        self.config = config
        self.documents = {doc.id: doc for doc in documents}

        # Build inverted index
        self.inverted_index: dict[str, dict[str, int]] = defaultdict(dict)
        self.doc_lengths: dict[str, int] = {}
        self.avg_doc_length = 0
        self.doc_frequencies: dict[str, int] = defaultdict(int)

        self._build_index()

    def _build_index(self) -> None:
        """Build inverted index and compute statistics."""
        total_length = 0

        for doc in self.documents.values():
            # Simple tokenization (can be enhanced with proper NLP)
            tokens = self._tokenize(doc.text)
            doc_length = len(tokens)

            self.doc_lengths[doc.id] = doc_length
            total_length += doc_length

            # Count term frequencies in document
            term_counts = Counter(tokens)

            for term, count in term_counts.items():
                self.inverted_index[term][doc.id] = count
                self.doc_frequencies[term] += 1

        # Compute average document length
        if self.documents:
            self.avg_doc_length = total_length / len(self.documents)

        logger.debug(
            f"Built BM25 index: {len(self.inverted_index)} terms, "
            f"avg_doc_length={self.avg_doc_length:.1f}"
        )

    def _tokenize(self, text: str) -> list[str]:
        """
        Simple tokenization (can be enhanced).

        In production, consider:
        - Language-specific tokenizers
        - Stemming/lemmatization
        - Stop word removal
        - Spell correction
        """
        import re

        # Lowercase and extract words
        tokens = re.findall(r"\b\w+\b", text.lower())
        return tokens

    def score_query(self, query: str) -> dict[str, float]:
        """
        Score all documents for a query using BM25.

        Args:
            query: Search query text

        Returns:
            Dict mapping document ID to BM25 score
        """
        query_terms = self._tokenize(query)
        doc_scores: dict[str, float] = defaultdict(float)

        for term in query_terms:
            if term not in self.inverted_index:
                continue

            # Compute IDF (Inverse Document Frequency)
            df = self.doc_frequencies[term]  # Documents containing term
            idf = math.log((len(self.documents) - df + 0.5) / (df + 0.5))

            # Score each document containing this term
            for doc_id, tf in self.inverted_index[term].items():
                doc_length = self.doc_lengths[doc_id]

                # BM25 score for this term in this document
                score = (
                    idf
                    * (tf * (self.config.k1 + 1))
                    / (
                        tf
                        + self.config.k1
                        * (
                            1
                            - self.config.b
                            + self.config.b * (doc_length / self.avg_doc_length)
                        )
                    )
                )

                doc_scores[doc_id] += score

        return dict(doc_scores)


class HybridSearchEngine:
    """
    Hybrid search engine combining BM25 + Vector similarity.

    Features:
    - Lexical matching with BM25 scoring
    - Semantic matching with vector similarity
    - Score fusion and re-ranking
    - Configurable weights and parameters
    """

    def __init__(self, config: HybridSearchConfig | None = None):
        """Initialize hybrid search engine."""
        self.config = config or HybridSearchConfig()
        self.bm25_scorer: BM25Scorer | None = None

    def update_corpus(self, documents: Sequence[Document]) -> None:
        """Update the search corpus with new documents."""
        if documents:
            self.bm25_scorer = BM25Scorer(documents, self.config)
            logger.info(f"Updated hybrid search corpus with {len(documents)} documents")

    def search(
        self,
        query: str,
        query_vector: Vector,
        vector_results: Sequence[SearchResult],
    ) -> list[SearchResult]:
        """
        Perform hybrid search combining lexical and semantic results.

        Args:
            query: Text query for lexical search
            query_vector: Query vector for semantic search
            vector_results: Pre-computed vector similarity results

        Returns:
            Fused and re-ranked search results
        """
        if not self.bm25_scorer:
            logger.warning("BM25 scorer not initialized, returning vector results only")
            return list(vector_results[: self.config.final_top_k])

        # Get BM25 scores for all documents
        bm25_scores = self.bm25_scorer.score_query(query)

        # Create unified scoring
        fused_scores: dict[str, dict[str, Any]] = {}

        # Add vector scores
        for result in vector_results:
            fused_scores[result.id] = {
                "vector_score": result.similarity,
                "bm25_score": bm25_scores.get(result.id, 0.0),
                "content": result.content,
                "metadata": result.metadata,
            }

        # Add pure BM25 results (might not be in vector results)
        for doc_id, bm25_score in bm25_scores.items():
            if doc_id not in fused_scores and bm25_score > 0:
                # Get document content
                doc = self.bm25_scorer.documents.get(doc_id)
                if doc:
                    fused_scores[doc_id] = {
                        "vector_score": 0.0,  # No semantic similarity
                        "bm25_score": bm25_score,
                        "content": doc.text,
                        "metadata": doc.metadata,
                    }

        # Fusion: Normalize and combine scores
        final_results = []

        # Normalize scores to [0, 1] range
        if fused_scores:
            max_vector = max(
                (data["vector_score"] for data in fused_scores.values()), default=1.0
            )
            max_bm25 = max(
                (data["bm25_score"] for data in fused_scores.values()), default=1.0
            )

            for doc_id, data in fused_scores.items():
                # Normalize scores
                norm_vector = data["vector_score"] / max_vector if max_vector > 0 else 0
                norm_bm25 = data["bm25_score"] / max_bm25 if max_bm25 > 0 else 0

                # Weighted fusion
                combined_score = (
                    self.config.vector_weight * norm_vector
                    + self.config.lexical_weight * norm_bm25
                )

                # Filter by minimum threshold
                if combined_score >= self.config.min_score_threshold:
                    _ = SearchResult(
                        id=doc_id,
                        similarity=combined_score,
                        content=data["content"],
                        metadata=data["metadata"],
                    )
                    final_results.append(result)

        # Sort by combined score and return top-k
        final_results.sort(key=lambda x: x.similarity, reverse=True)
        return final_results[: self.config.final_top_k]

    def get_stats(self) -> dict[str, Any]:
        """Get search engine statistics."""
        stats = {
            "config": {
                "vector_weight": self.config.vector_weight,
                "lexical_weight": self.config.lexical_weight,
                "final_top_k": self.config.final_top_k,
            },
            "bm25_ready": self.bm25_scorer is not None,
        }

        if self.bm25_scorer:
            stats.update(
                {
                    "corpus_size": len(self.bm25_scorer.documents),
                    "vocabulary_size": len(self.bm25_scorer.inverted_index),
                    "avg_doc_length": self.bm25_scorer.avg_doc_length,
                }
            )

        return stats
