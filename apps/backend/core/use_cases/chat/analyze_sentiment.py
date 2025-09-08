"""Analyze sentiment use case.

This module implements sentiment analysis for chat messages following Clean Architecture principles.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any
import Exception
import RuntimeError
import ValueError
import chat_id
import chat_repository
import content
import dict
import e
import len
import max
import min
import s
import self
import sentiment_result
import str
import sum
import w
import word

if TYPE_CHECKING:
    from uuid import UUID

    from core.interfaces.repositories import ChatRepository


class AnalyzeSentimentUseCase:
    """Use case for analyzing sentiment of chat messages."""

    def __init__(self, chat_repository: ChatRepository) -> None:
        """Initialize the analyze sentiment use case.

        Args:
            chat_repository: Repository for chat data access.
        """
        self.chat_repository = chat_repository

    async def execute(
        self, content: str, chat_id: UUID | None = None
    ) -> dict[str, Any]:
        """Analyze sentiment of a text message.

        Args:
            content: Text content to analyze.
            chat_id: Optional chat ID for context.

        Returns:
            Dictionary containing sentiment analysis results.

        Raises:
            ValueError: If content is empty.
            RuntimeError: If sentiment analysis fails.
        """
        if not content or not content.strip():
            raise ValueError("Content cannot be empty")

        try:
            self._analyze_message_sentiment(content)

            # Add context information if chat_id is provided
            if chat_id:
                sentiment_result["chat_id"] = str(chat_id)

                # Optionally store in chat context
                chat = await self.chat_repository.get_by_id(chat_id)
                if chat:
                    if "sentiment_history" not in chat.context_data:
                        chat.context_data["sentiment_history"] = []

                    chat.context_data["sentiment_history"].append(
                        {
                            "sentiment": sentiment_result["sentiment"],
                            "confidence": sentiment_result["confidence"],
                            "timestamp": sentiment_result["timestamp"],
                        }
                    )

                    # Keep only last 10 sentiment records
                    if len(chat.context_data["sentiment_history"]) > 10:
                        chat.context_data["sentiment_history"] = chat.context_data[
                            "sentiment_history"
                        ][-10:]

                    await self.chat_repository.update(chat)

            return sentiment_result

        except Exception as e:
            raise RuntimeError(f"Failed to analyze sentiment: {e!s}") from e

    async def analyze_chat_context(self, chat_id: UUID) -> dict[str, Any]:
        """Analyze overall sentiment context of a chat.

        Args:
            chat_id: ID of the chat to analyze.

        Returns:
            Dictionary containing chat sentiment analysis.

        Raises:
            ValueError: If chat is not found.
        """
        chat = await self.chat_repository.get_by_id(chat_id)
        if not chat:
            raise ValueError(f"Chat with ID {chat_id} not found")

        sentiment_history = chat.context_data.get("sentiment_history", [])

        if not sentiment_history:
            return {
                "chat_id": str(chat_id),
                "overall_sentiment": "neutral",
                "confidence": 0.0,
                "sentiment_distribution": {"positive": 0, "neutral": 0, "negative": 0},
                "sentiment_trend": "stable",
                "total_analyzed_messages": 0,
            }

        # Calculate overall statistics
        positive_count = sum(
            1 for s in sentiment_history if s["sentiment"] == "positive"
        )
        negative_count = sum(
            1 for s in sentiment_history if s["sentiment"] == "negative"
        )
        neutral_count = sum(1 for s in sentiment_history if s["sentiment"] == "neutral")

        total = len(sentiment_history)

        # Calculate distribution
        distribution = {
            "positive": positive_count / total,
            "neutral": neutral_count / total,
            "negative": negative_count / total,
        }

        # Determine overall sentiment
        if positive_count > negative_count and positive_count > neutral_count:
            overall_sentiment = "positive"
            confidence = positive_count / total
        elif negative_count > positive_count and negative_count > neutral_count:
            overall_sentiment = "negative"
            confidence = negative_count / total
        else:
            overall_sentiment = "neutral"
            confidence = neutral_count / total

        # Calculate trend (compare first half vs second half)
        mid_point = len(sentiment_history) // 2
        if mid_point > 0:
            first_half_positive = sum(
                1 for s in sentiment_history[:mid_point] if s["sentiment"] == "positive"
            )
            second_half_positive = sum(
                1 for s in sentiment_history[mid_point:] if s["sentiment"] == "positive"
            )

            if second_half_positive > first_half_positive:
                trend = "improving"
            elif second_half_positive < first_half_positive:
                trend = "declining"
            else:
                trend = "stable"
        else:
            trend = "stable"

        return {
            "chat_id": str(chat_id),
            "overall_sentiment": overall_sentiment,
            "confidence": confidence,
            "sentiment_distribution": distribution,
            "sentiment_trend": trend,
            "total_analyzed_messages": total,
            "average_confidence": sum(s["confidence"] for s in sentiment_history)
            / total,
        }

    def _analyze_message_sentiment(self, content: str) -> dict[str, Any]:
        """Analyze sentiment of a single message.

        Args:
            content: Message content to analyze.

        Returns:
            Dictionary containing sentiment analysis results.
        """
        # Simple rule-based sentiment analysis
        # In a real implementation, this would use ML models or external APIs

        positive_words = [
            "tốt",
            "tuyệt",
            "xuất sắc",
            "thích",
            "yêu",
            "vui",
            "hạnh phúc",
            "good",
            "great",
            "excellent",
            "love",
            "like",
            "happy",
            "amazing",
            "wonderful",
            "fantastic",
            "awesome",
            "brilliant",
        ]

        negative_words = [
            "tệ",
            "xấu",
            "ghét",
            "buồn",
            "tức giận",
            "thất vọng",
            "tệ hại",
            "bad",
            "terrible",
            "hate",
            "sad",
            "angry",
            "disappointed",
            "awful",
            "horrible",
            "disgusting",
            "frustrated",
        ]

        neutral_words = [
            "được",
            "bình thường",
            "ok",
            "khá",
            "ổn",
            "okay",
            "fine",
            "normal",
            "average",
            "decent",
        ]

        content_lower = content.lower()

        positive_count = sum(1 for word in positive_words if word in content_lower)
        negative_count = sum(1 for word in negative_words if word in content_lower)
        neutral_count = sum(1 for word in neutral_words if word in content_lower)

        total_count = positive_count + negative_count + neutral_count

        if total_count == 0:
            # No sentiment indicators found
            return {
                "sentiment": "neutral",
                "confidence": 0.5,
                "scores": {"positive": 0.33, "neutral": 0.34, "negative": 0.33},
                "detected_words": {"positive": [], "negative": [], "neutral": []},
                "timestamp": str(__import__("datetime").datetime.now()),
            }

        # Calculate scores
        positive_score = positive_count / total_count if total_count > 0 else 0
        negative_score = negative_count / total_count if total_count > 0 else 0
        neutral_score = neutral_count / total_count if total_count > 0 else 0

        # Determine overall sentiment
        if positive_score > negative_score and positive_score > neutral_score:
            sentiment = "positive"
            confidence = positive_score
        elif negative_score > positive_score and negative_score > neutral_score:
            sentiment = "negative"
            confidence = negative_score
        else:
            sentiment = "neutral"
            confidence = max(neutral_score, 0.5)

        return {
            "sentiment": sentiment,
            "confidence": min(confidence, 1.0),
            "scores": {
                "positive": positive_score,
                "neutral": neutral_score,
                "negative": negative_score,
            },
            "detected_words": {
                "positive": [w for w in positive_words if w in content_lower],
                "negative": [w for w in negative_words if w in content_lower],
                "neutral": [w for w in neutral_words if w in content_lower],
            },
            "timestamp": str(__import__("datetime").datetime.now()),
        }
