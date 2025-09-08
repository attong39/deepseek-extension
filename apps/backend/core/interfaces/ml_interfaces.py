"""Machine Learning interfaces.

This module defines abstract interfaces for machine learning operations
including model inference, training, and feature extraction.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any
import bool
import dict
import float
import int
import list
import str


class MLModelInterface(ABC):
    """Interface for machine learning model operations."""

    @abstractmethod
    async def predict(
        self,
        inputs: dict[str, Any] | list[dict[str, Any]],
    ) -> dict[str, Any] | list[dict[str, Any]]:
        """Make predictions using the model.

        Args:
            inputs: Input data for prediction.

        Returns:
            Prediction results.
        """

    @abstractmethod
    async def predict_batch(
        self,
        inputs: list[dict[str, Any]],
        batch_size: int = 32,
    ) -> list[dict[str, Any]]:
        """Make batch predictions.

        Args:
            inputs: List of input data.
            batch_size: Batch size for processing.

        Returns:
            List of prediction results.
        """

    @abstractmethod
    async def get_model_info(self) -> dict[str, Any]:
        """Get model information and metadata.

        Returns:
            Model information including version, parameters, etc.
        """

    @abstractmethod
    async def validate_input(self, inputs: dict[str, Any]) -> bool:
        """Validate input data format.

        Args:
            inputs: Input data to validate.

        Returns:
            True if input is valid.
        """


class TextClassificationInterface(ABC):
    """Interface for text classification models."""

    @abstractmethod
    async def classify_text(
        self,
        text: str,
        labels: list[str] | None = None,
    ) -> dict[str, float]:
        """Classify text into categories.

        Args:
            text: Input text to classify.
            labels: Optional list of candidate labels.

        Returns:
            Classification scores for each label.
        """

    @abstractmethod
    async def classify_batch(
        self,
        texts: list[str],
        labels: list[str] | None = None,
    ) -> list[dict[str, float]]:
        """Classify multiple texts.

        Args:
            texts: List of input texts.
            labels: Optional list of candidate labels.

        Returns:
            List of classification results.
        """

    @abstractmethod
    async def get_confidence_threshold(self) -> float:
        """Get confidence threshold for predictions.

        Returns:
            Confidence threshold value.
        """


class TextEmbeddingInterface(ABC):
    """Interface for text embedding models."""

    @abstractmethod
    async def encode_text(
        self,
        text: str,
        normalize: bool = True,
    ) -> list[float]:
        """Generate embedding for text.

        Args:
            text: Input text to encode.
            normalize: Whether to normalize the embedding.

        Returns:
            Text embedding vector.
        """

    @abstractmethod
    async def encode_batch(
        self,
        texts: list[str],
        normalize: bool = True,
        batch_size: int = 32,
    ) -> list[list[float]]:
        """Generate embeddings for multiple texts.

        Args:
            texts: List of input texts.
            normalize: Whether to normalize embeddings.
            batch_size: Batch size for processing.

        Returns:
            List of embedding vectors.
        """

    @abstractmethod
    async def compute_similarity(
        self,
        embedding1: list[float],
        embedding2: list[float],
    ) -> float:
        """Compute similarity between two embeddings.

        Args:
            embedding1: First embedding vector.
            embedding2: Second embedding vector.

        Returns:
            Similarity score.
        """

    @abstractmethod
    async def get_embedding_dimension(self) -> int:
        """Get embedding vector dimension.

        Returns:
            Embedding dimension.
        """


class SentimentAnalysisInterface(ABC):
    """Interface for sentiment analysis models."""

    @abstractmethod
    async def analyze_sentiment(
        self,
        text: str,
    ) -> dict[str, Any]:
        """Analyze sentiment of text.

        Args:
            text: Input text to analyze.

        Returns:
            Sentiment analysis result with score and label.
        """

    @abstractmethod
    async def analyze_batch(
        self,
        texts: list[str],
    ) -> list[dict[str, Any]]:
        """Analyze sentiment for multiple texts.

        Args:
            texts: List of input texts.

        Returns:
            List of sentiment analysis results.
        """

    @abstractmethod
    async def get_sentiment_labels(self) -> list[str]:
        """Get available sentiment labels.

        Returns:
            List of sentiment labels.
        """


class NamedEntityRecognitionInterface(ABC):
    """Interface for named entity recognition models."""

    @abstractmethod
    async def extract_entities(
        self,
        text: str,
    ) -> list[dict[str, Any]]:
        """Extract named entities from text.

        Args:
            text: Input text to process.

        Returns:
            List of extracted entities with labels and positions.
        """

    @abstractmethod
    async def extract_batch(
        self,
        texts: list[str],
    ) -> list[list[dict[str, Any]]]:
        """Extract entities from multiple texts.

        Args:
            texts: List of input texts.

        Returns:
            List of entity extraction results.
        """

    @abstractmethod
    async def get_entity_types(self) -> list[str]:
        """Get supported entity types.

        Returns:
            List of entity type labels.
        """


class QuestionAnsweringInterface(ABC):
    """Interface for question answering models."""

    @abstractmethod
    async def answer_question(
        self,
        question: str,
        context: str,
    ) -> dict[str, Any]:
        """Answer question based on context.

        Args:
            question: Question to answer.
            context: Context text containing the answer.

        Returns:
            Answer with confidence score and position.
        """

    @abstractmethod
    async def answer_batch(
        self,
        questions: list[str],
        contexts: list[str],
    ) -> list[dict[str, Any]]:
        """Answer multiple questions.

        Args:
            questions: List of questions.
            contexts: List of context texts.

        Returns:
            List of answers.
        """

    @abstractmethod
    async def validate_context(self, context: str) -> bool:
        """Validate if context is suitable for QA.

        Args:
            context: Context text to validate.

        Returns:
            True if context is valid.
        """


class LanguageGenerationInterface(ABC):
    """Interface for language generation models."""

    @abstractmethod
    async def generate_text(
        self,
        prompt: str,
        max_length: int = 512,
        temperature: float = 0.7,
        top_p: float = 0.9,
    ) -> str:
        """Generate text from prompt.

        Args:
            prompt: Input prompt.
            max_length: Maximum output length.
            temperature: Sampling temperature.
            top_p: Top-p sampling parameter.

        Returns:
            Generated text.
        """

    @abstractmethod
    async def generate_batch(
        self,
        prompts: list[str],
        max_length: int = 512,
        temperature: float = 0.7,
    ) -> list[str]:
        """Generate text for multiple prompts.

        Args:
            prompts: List of input prompts.
            max_length: Maximum output length.
            temperature: Sampling temperature.

        Returns:
            List of generated texts.
        """

    @abstractmethod
    async def stream_generation(
        self,
        prompt: str,
        max_length: int = 512,
        temperature: float = 0.7,
    ) -> Any:  # AsyncGenerator[str, None] would be ideal but avoiding import
        """Stream text generation.

        Args:
            prompt: Input prompt.
            max_length: Maximum output length.
            temperature: Sampling temperature.

        Returns:
            Async generator yielding text chunks.
        """


class TextSummarizationInterface(ABC):
    """Interface for text summarization models."""

    @abstractmethod
    async def summarize_text(
        self,
        text: str,
        max_length: int | None = None,
        min_length: int | None = None,
    ) -> str:
        """Summarize input text.

        Args:
            text: Input text to summarize.
            max_length: Maximum summary length.
            min_length: Minimum summary length.

        Returns:
            Text summary.
        """

    @abstractmethod
    async def summarize_batch(
        self,
        texts: list[str],
        max_length: int | None = None,
    ) -> list[str]:
        """Summarize multiple texts.

        Args:
            texts: List of input texts.
            max_length: Maximum summary length.

        Returns:
            List of summaries.
        """

    @abstractmethod
    async def extract_key_points(
        self,
        text: str,
        num_points: int = 5,
    ) -> list[str]:
        """Extract key points from text.

        Args:
            text: Input text.
            num_points: Number of key points to extract.

        Returns:
            List of key points.
        """


class ModelTrainingInterface(ABC):
    """Interface for model training operations."""

    @abstractmethod
    async def train_model(
        self,
        training_data: list[dict[str, Any]],
        validation_data: list[dict[str, Any]] | None = None,
        config: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Train model with provided data.

        Args:
            training_data: Training dataset.
            validation_data: Optional validation dataset.
            config: Training configuration.

        Returns:
            Training results and metrics.
        """

    @abstractmethod
    async def evaluate_model(
        self,
        test_data: list[dict[str, Any]],
        metrics: list[str] | None = None,
    ) -> dict[str, float]:
        """Evaluate model performance.

        Args:
            test_data: Test dataset.
            metrics: List of metrics to compute.

        Returns:
            Evaluation metrics.
        """

    @abstractmethod
    async def save_model(
        self,
        model_path: str,
        metadata: dict[str, Any] | None = None,
    ) -> bool:
        """Save trained model.

        Args:
            model_path: Path to save model.
            metadata: Optional model metadata.

        Returns:
            True if successful.
        """

    @abstractmethod
    async def load_model(self, model_path: str) -> bool:
        """Load trained model.

        Args:
            model_path: Path to load model from.

        Returns:
            True if successful.
        """


class FeatureExtractionInterface(ABC):
    """Interface for feature extraction operations."""

    @abstractmethod
    async def extract_features(
        self,
        data: dict[str, Any],
        feature_config: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Extract features from data.

        Args:
            data: Input data.
            feature_config: Feature extraction configuration.

        Returns:
            Extracted features.
        """

    @abstractmethod
    async def extract_batch(
        self,
        data_batch: list[dict[str, Any]],
        feature_config: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        """Extract features from batch of data.

        Args:
            data_batch: List of input data.
            feature_config: Feature extraction configuration.

        Returns:
            List of extracted features.
        """

    @abstractmethod
    async def get_feature_names(self) -> list[str]:
        """Get names of extracted features.

        Returns:
            List of feature names.
        """

    @abstractmethod
    async def validate_features(
        self,
        features: dict[str, Any],
    ) -> bool:
        """Validate extracted features.

        Args:
            features: Features to validate.

        Returns:
            True if features are valid.
        """
