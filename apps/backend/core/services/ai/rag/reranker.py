"""Re-ranking interfaces for improving retrieval quality.

Defines abstract interfaces for re-ranking retrieved passages to improve
relevance and quality of RAG results.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any
import Exception
import bool
import details
import dict
import float
import int
import list
import message
import reranker_name
import self
import str
import super

if TYPE_CHECKING:
    from apps.backend.core.services.ai.rag.types import Passage, RerankingResult


class BaseReranker(ABC):
    """Abstract base class for passage re-ranking."""

    @abstractmethod
    async def rerank(
        self,
        query: str,
        passages: list[Passage],
        top_k: int | None = None,
    ) -> list[Passage]:
        """Re-rank passages based on relevance to query.

        Args:
            query: Original query text
            passages: List of passages to re-rank
            top_k: Number of top passages to return (None = all)

        Returns:
            Re-ranked list of passages with updated scores

        Raises:
            RerankingError: If re-ranking fails
        """

    @abstractmethod
    async def score_relevance(
        self,
        query: str,
        passage: Passage,
    ) -> float:
        """Score a single passage's relevance to query.

        Args:
            query: Query text
            passage: Passage to score

        Returns:
            Relevance score (higher = more relevant)
        """

    @abstractmethod
    def get_model_info(self) -> dict[str, Any]:
        """Get information about the re-ranking model.

        Returns:
            Model information dictionary
        """


class SemanticReranker(BaseReranker):
    """Interface for semantic similarity-based re-ranking."""

    @abstractmethod
    async def rerank_semantic(
        self,
        query: str,
        passages: list[Passage],
        similarity_threshold: float = 0.0,
        top_k: int | None = None,
    ) -> RerankingResult:
        """Re-rank using semantic similarity models.

        Args:
            query: Query text
            passages: Passages to re-rank
            similarity_threshold: Minimum similarity threshold
            top_k: Number of results to return

        Returns:
            Complete re-ranking result with scores and metadata
        """

    @abstractmethod
    async def compute_semantic_scores(
        self,
        query: str,
        passages: list[Passage],
    ) -> list[float]:
        """Compute semantic similarity scores for all passages.

        Args:
            query: Query text
            passages: List of passages

        Returns:
            List of similarity scores aligned with passages
        """


class CrossEncoderReranker(BaseReranker):
    """Interface for cross-encoder based re-ranking."""

    @abstractmethod
    async def rerank_cross_encoder(
        self,
        query: str,
        passages: list[Passage],
        batch_size: int = 32,
        top_k: int | None = None,
    ) -> list[Passage]:
        """Re-rank using cross-encoder models.

        Args:
            query: Query text
            passages: Passages to re-rank
            batch_size: Batch size for processing
            top_k: Number of results to return

        Returns:
            Re-ranked passages with cross-encoder scores
        """

    @abstractmethod
    async def batch_score(
        self,
        query: str,
        passages: list[Passage],
        batch_size: int = 32,
    ) -> list[float]:
        """Score passages in batches for efficiency.

        Args:
            query: Query text
            passages: Passages to score
            batch_size: Batch size for processing

        Returns:
            List of scores for each passage
        """


class HybridReranker(BaseReranker):
    """Interface for combining multiple re-ranking strategies."""

    @abstractmethod
    async def rerank_hybrid(
        self,
        query: str,
        passages: list[Passage],
        weights: dict[str, float] | None = None,
        top_k: int | None = None,
    ) -> RerankingResult:
        """Re-rank using multiple strategies with weighted combination.

        Args:
            query: Query text
            passages: Passages to re-rank
            weights: Weights for different re-ranking strategies
            top_k: Number of results to return

        Returns:
            Hybrid re-ranking result
        """

    @abstractmethod
    async def add_reranker(
        self,
        name: str,
        reranker: BaseReranker,
        weight: float = 1.0,
    ) -> None:
        """Add a re-ranker to the hybrid system.

        Args:
            name: Name for the re-ranker
            reranker: Re-ranker instance
            weight: Weight for this re-ranker's scores
        """

    @abstractmethod
    async def remove_reranker(self, name: str) -> bool:
        """Remove a re-ranker from the hybrid system.

        Args:
            name: Name of re-ranker to remove

        Returns:
            True if removed successfully
        """

    @abstractmethod
    async def list_rerankers(self) -> list[str]:
        """List available re-rankers.

        Returns:
            List of re-ranker names
        """


class ContextualReranker(BaseReranker):
    """Interface for context-aware re-ranking."""

    @abstractmethod
    async def rerank_with_context(
        self,
        query: str,
        passages: list[Passage],
        user_context: dict[str, Any],
        conversation_history: list[str] | None = None,
        top_k: int | None = None,
    ) -> RerankingResult:
        """Re-rank considering user context and conversation history.

        Args:
            query: Query text
            passages: Passages to re-rank
            user_context: User context information
            conversation_history: Previous conversation turns
            top_k: Number of results to return

        Returns:
            Context-aware re-ranking result
        """

    @abstractmethod
    async def update_user_profile(
        self,
        user_id: str,
        preferences: dict[str, Any],
    ) -> None:
        """Update user profile for personalized re-ranking.

        Args:
            user_id: User identifier
            preferences: User preferences and profile data
        """

    @abstractmethod
    async def get_user_profile(
        self,
        user_id: str,
    ) -> dict[str, Any] | None:
        """Get user profile for re-ranking.

        Args:
            user_id: User identifier

        Returns:
            User profile data or None if not found
        """


class DiversityReranker(BaseReranker):
    """Interface for diversity-aware re-ranking."""

    @abstractmethod
    async def rerank_for_diversity(
        self,
        query: str,
        passages: list[Passage],
        similarity_threshold: float = 0.8,
        top_k: int | None = None,
    ) -> list[Passage]:
        """Re-rank to maximize relevance while ensuring diversity.

        Args:
            query: Query text
            passages: Passages to re-rank
            diversity_lambda: Balance between relevance and diversity
            similarity_threshold: Threshold for considering passages similar
            top_k: Number of results to return

        Returns:
            Diversified re-ranked passages
        """

    @abstractmethod
    async def compute_diversity_scores(
        self,
        passages: list[Passage],
        method: str = "cosine",
    ) -> list[list[float]]:
        """Compute pairwise diversity scores between passages.

        Args:
            passages: List of passages
            method: Diversity computation method

        Returns:
            Matrix of pairwise diversity scores
        """

    @abstractmethod
    async def maximal_marginal_relevance(
        self,
        query: str,
        passages: list[Passage],
        lambda_param: float = 0.5,
        top_k: int = 10,
    ) -> list[Passage]:
        """Apply Maximal Marginal Relevance for diversification.

        Args:
            query: Query text
            passages: Candidate passages
            lambda_param: Balance parameter (1.0 = only relevance, 0.0 = only diversity)
            top_k: Number of results to return

        Returns:
            MMR-selected passages
        """


class AdaptiveReranker(BaseReranker):
    """Interface for adaptive re-ranking that learns from feedback."""

    @abstractmethod
    async def rerank_adaptive(
        self,
        query: str,
        passages: list[Passage],
        feedback_history: list[dict[str, Any]] | None = None,
        top_k: int | None = None,
    ) -> RerankingResult:
        """Re-rank with adaptive learning from user feedback.

        Args:
            query: Query text
            passages: Passages to re-rank
            feedback_history: Historical user feedback
            top_k: Number of results to return

        Returns:
            Adaptive re-ranking result
        """

    @abstractmethod
    async def update_from_feedback(
        self,
        query: str,
        passages: list[Passage],
        feedback: dict[str, Any],
    ) -> None:
        """Update re-ranker based on user feedback.

        Args:
            query: Original query
            passages: Passages that were ranked
            feedback: User feedback (clicks, ratings, etc.)
        """

    @abstractmethod
    async def get_adaptation_stats(self) -> dict[str, Any]:
        """Get statistics about adaptation performance.

        Returns:
            Adaptation statistics
        """


class MultiModalReranker(BaseReranker):
    """Interface for multi-modal re-ranking."""

    @abstractmethod
    async def rerank_multimodal(
        self,
        query: str,
        passages: list[Passage],
        query_modalities: list[str],
        top_k: int | None = None,
    ) -> list[Passage]:
        """Re-rank considering multiple modalities.

        Args:
            query: Query text
            passages: Passages to re-rank (may contain multi-modal content)
            query_modalities: Modalities present in query
            top_k: Number of results to return

        Returns:
            Multi-modal re-ranked passages
        """

    @abstractmethod
    async def score_modality_relevance(
        self,
        query: str,
        passage: Passage,
        modality: str,
    ) -> float:
        """Score relevance for a specific modality.

        Args:
            query: Query text
            passage: Passage to score
            modality: Modality to score (text, image, audio, etc.)

        Returns:
            Modality-specific relevance score
        """


class RerankingError(Exception):
    """Exception raised when re-ranking operations fail."""

    def __init__(
        self,
        message: str,
        reranker_name: str | None = None,
        details: dict[str, Any] | None = None,
    ):
        """Initialize re-ranking error.

        Args:
            message: Error message
            reranker_name: Optional re-ranker name that failed
            details: Optional error details
        """
        super().__init__(message)
        self.reranker_name = reranker_name
        self.details = details or {}


class RerankerFactory(ABC):
    """Factory for creating different types of re-rankers."""

    @abstractmethod
    async def create_semantic_reranker(
        self,
        model_name: str,
        **kwargs: Any,
    ) -> SemanticReranker:
        """Create a semantic re-ranker.

        Args:
            model_name: Name of the semantic model to use
            **kwargs: Additional model parameters

        Returns:
            Configured semantic re-ranker
        """

    @abstractmethod
    async def create_cross_encoder_reranker(
        self,
        model_name: str,
        **kwargs: Any,
    ) -> CrossEncoderReranker:
        """Create a cross-encoder re-ranker.

        Args:
            model_name: Name of the cross-encoder model
            **kwargs: Additional model parameters

        Returns:
            Configured cross-encoder re-ranker
        """

    @abstractmethod
    async def create_hybrid_reranker(
        self,
        rerankers: dict[str, BaseReranker],
        weights: dict[str, float] | None = None,
        **kwargs: Any,
    ) -> HybridReranker:
        """Create a hybrid re-ranker.

        Args:
            rerankers: Dictionary of re-rankers to combine
            weights: Weights for each re-ranker
            **kwargs: Additional parameters

        Returns:
            Configured hybrid re-ranker
        """

    @abstractmethod
    async def create_contextual_reranker(
        self,
        base_reranker: BaseReranker,
        context_weight: float = 0.3,
        **kwargs: Any,
    ) -> ContextualReranker:
        """Create a contextual re-ranker.

        Args:
            base_reranker: Base re-ranker to wrap
            context_weight: Weight for context features
            **kwargs: Additional parameters

        Returns:
            Configured contextual re-ranker
        """
