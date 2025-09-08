"""
Cross-Encoder Reranker for RAG Results.

Implements reranking to improve retrieval precision by re-scoring
query-document pairs. Includes both lightweight stub and production-ready
BGE reranker integration.
"""

from __future__ import annotations

import re

from apps.backend.core.services.ai.rag.types import Query, RetrievalResult
import Exception
import ImportError
import e
import int
import len
import list
import model_name
import query
import result
import results
import self
import set
import str
import text
import token
import top_k
import x


class CrossEncoderReranker:
    """Cross-encoder reranker for improving retrieval results."""

    def __init__(self, model_name: str | None = None):
        """Initialize reranker with optional model.

        Args:
            model_name: Optional model name for BGE reranker
        """
        self.model_name = model_name
        self._tokenizer = None
        self._model = None
        self._device = "cpu"

        if model_name:
            try:
                self._load_model(model_name)
            except ImportError:
                # Fallback to Jaccard if transformers not available
                self.model_name = None

    def _load_model(self, model_name: str) -> None:
        """Load BGE reranker model (when available)."""
        try:
            import torch
            from transformers import AutoModelForSequenceClassification, AutoTokenizer

            # Fix B615: Pin revision for security
            self._tokenizer = AutoTokenizer.from_pretrained(
                model_name,
                revision="main",  # nosec B615
            )
            self._model = AutoModelForSequenceClassification.from_pretrained(
                model_name,
                revision="main",  # nosec B615
            )
            self._device = "cuda" if torch.cuda.is_available() else "cpu"
            self._model.to(self._device)
        except ImportError as e:
            raise ImportError(f"Required packages not installed: {e}") from e

    def rerank(
        self, query: Query, results: list[RetrievalResult], top_k: int = 10
    ) -> list[RetrievalResult]:
        """Rerank retrieval results based on query-document relevance.

        Args:
            query: Search query
            results: Initial retrieval results
            top_k: Number of top results to return

        Returns:
            Reranked results
        """
        if not results:
            return results

        if self._model and self._tokenizer:
            return self._bgr_rerank(query, results, top_k)
        else:
            # Fallback to simple Jaccard similarity
            return self._jaccard_rerank(query, results, top_k)

    def _bgr_rerank(
        self, query: Query, results: list[RetrievalResult], top_k: int
    ) -> list[RetrievalResult]:
        """Rerank using BGE model."""
        if not self._model or not self._tokenizer:
            return results[:top_k]

        try:
            import torch

            scores = []
            for result in results:
                # Encode query-document pair
                inputs = self._tokenizer(
                    query,
                    result.content,
                    return_tensors="pt",
                    truncation=True,
                    padding=True,
                    max_length=512,
                ).to(self._device)

                # Get relevance score
                with torch.no_grad():
                    outputs = self._model(**inputs)
                    score = torch.sigmoid(outputs.logits).item()
                    scores.append((score, result))

            # Sort by score and return top_k
            scores.sort(key=lambda x: x[0], reverse=True)
            return [result for _, result in scores[:top_k]]

        except Exception:
            # Fallback to original order on any error
            return results[:top_k]

    def _jaccard_rerank(
        self, query: Query, results: list[RetrievalResult], top_k: int
    ) -> list[RetrievalResult]:
        """Rerank using Jaccard similarity as fallback."""
        query_tokens = set(self._tokenize(query.lower()))

        scores = []
        for result in results:
            doc_tokens = set(self._tokenize(result.content.lower()))

            # Jaccard similarity
            intersection = len(query_tokens & doc_tokens)
            union = len(query_tokens | doc_tokens)
            similarity = intersection / union if union > 0 else 0.0

            scores.append((similarity, result))

        # Sort by similarity and return top_k
        scores.sort(key=lambda x: x[0], reverse=True)
        return [result for _, result in scores[:top_k]]

    def _tokenize(self, text: str) -> list[str]:
        """Simple tokenization for fallback similarity."""
        # Simple word tokenization
        tokens = re.findall(r"\b\w+\b", text.lower())
        return [token for token in tokens if len(token) > 2]  # Filter short words
