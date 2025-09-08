"""
Enhanced Model Router với intelligent model selection.

Features:
- Dynamic model routing based on task type, cost, performance
- Load balancing between local and cloud models
- Fallback strategies
- Cost optimization
- Performance monitoring
"""

from __future__ import annotations

import asyncio
import logging
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Literal
import attempt
import bool
import cost
import dict
import float
import int
import latency_ms
import len
import list
import m
import max
import max_retries
import range
import requirements
import selection
import self
import sorted
import str
import success
import tokens_processed
import x

logger = logging.getLogger(__name__)


class ModelType(Enum):
    """Types of AI models."""

    LANGUAGE = "language"
    EMBEDDING = "embedding"
    VISION = "vision"
    AUDIO = "audio"
    MULTIMODAL = "multimodal"


class ModelProvider(Enum):
    """Model providers."""

    LOCAL = "local"
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    AZURE = "azure"
    HUGGINGFACE = "huggingface"


@dataclass
class ModelCapability:
    """Model capability definition."""

    max_tokens: int = 4096
    supports_streaming: bool = False
    supports_function_calling: bool = False
    supports_vision: bool = False
    supports_audio: bool = False
    languages: list[str] = field(default_factory=lambda: ["en"])
    cost_per_1k_tokens: float = 0.0
    avg_latency_ms: float = 1000.0
    quality_score: float = 0.8  # 0-1 scale


@dataclass
class ModelMetrics:
    """Real-time model metrics."""

    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    avg_latency_ms: float = 0.0
    total_tokens_processed: int = 0
    total_cost: float = 0.0
    last_used: float = 0.0
    current_load: int = 0  # Current concurrent requests


@dataclass
class ModelConfig:
    """Model configuration."""

    id: str
    name: str
    provider: ModelProvider
    model_type: ModelType
    endpoint: str = ""
    api_key: str = ""
    capabilities: ModelCapability = field(default_factory=ModelCapability)
    metrics: ModelMetrics = field(default_factory=ModelMetrics)
    enabled: bool = True
    max_concurrent: int = 10
    priority: int = 50  # 0-100, higher = preferred
    fallback_models: list[str] = field(default_factory=list)


@dataclass
class TaskRequirements:
    """Task requirements for model selection."""

    model_type: ModelType
    max_tokens: int = 4096
    requires_streaming: bool = False
    requires_function_calling: bool = False
    requires_vision: bool = False
    requires_audio: bool = False
    language: str = "en"
    cost_sensitivity: Literal["low", "medium", "high"] = "medium"
    latency_sensitivity: Literal["low", "medium", "high"] = "medium"
    quality_requirement: float = 0.7  # Minimum quality score


class EnhancedModelRouter:
    """
    Enhanced Model Router với intelligent selection.

    Features:
    - Task-based model selection
    - Load balancing
    - Cost optimization
    - Performance monitoring
    - Automatic fallback
    """

    def __init__(self) -> None:
        """Initialize model router."""
        self.models: dict[str, ModelConfig] = {}
        self.selection_history: list[dict[str, Any]] = []
        self.lock = asyncio.Lock()

        # Default model configurations
        self._init_default_models()

    def _init_default_models(self) -> None:
        """Initialize default model configurations."""
        # Local models
        self.add_model(
            ModelConfig(
                id="llama_3_1_8b_local",
                name="Llama 3.1 8B (Local)",
                provider=ModelProvider.LOCAL,
                model_type=ModelType.LANGUAGE,
                capabilities=ModelCapability(
                    max_tokens=8192,
                    supports_streaming=True,
                    supports_function_calling=True,
                    languages=["en", "vi"],
                    cost_per_1k_tokens=0.0,  # Free local
                    avg_latency_ms=800,
                    quality_score=0.85,
                ),
                priority=90,  # High priority for local
                max_concurrent=3,
                fallback_models=["gpt_4o_mini", "claude_3_haiku"],
            )
        )

        # OpenAI models
        self.add_model(
            ModelConfig(
                id="gpt_4o",
                name="GPT-4o",
                provider=ModelProvider.OPENAI,
                model_type=ModelType.MULTIMODAL,
                capabilities=ModelCapability(
                    max_tokens=128000,
                    supports_streaming=True,
                    supports_function_calling=True,
                    supports_vision=True,
                    supports_audio=True,
                    languages=["en", "vi", "zh", "es", "fr"],
                    cost_per_1k_tokens=0.005,
                    avg_latency_ms=1200,
                    quality_score=0.95,
                ),
                priority=80,
                fallback_models=["claude_3_5_sonnet", "gpt_4o_mini"],
            )
        )

        self.add_model(
            ModelConfig(
                id="gpt_4o_mini",
                name="GPT-4o Mini",
                provider=ModelProvider.OPENAI,
                model_type=ModelType.LANGUAGE,
                capabilities=ModelCapability(
                    max_tokens=128000,
                    supports_streaming=True,
                    supports_function_calling=True,
                    supports_vision=True,
                    languages=["en", "vi", "zh", "es", "fr"],
                    cost_per_1k_tokens=0.00015,
                    avg_latency_ms=600,
                    quality_score=0.85,
                ),
                priority=75,
                fallback_models=["claude_3_haiku", "llama_3_1_8b_local"],
            )
        )

        # Anthropic models
        self.add_model(
            ModelConfig(
                id="claude_3_5_sonnet",
                name="Claude 3.5 Sonnet",
                provider=ModelProvider.ANTHROPIC,
                model_type=ModelType.LANGUAGE,
                capabilities=ModelCapability(
                    max_tokens=200000,
                    supports_streaming=True,
                    supports_function_calling=True,
                    supports_vision=True,
                    languages=["en", "vi", "zh", "es", "fr"],
                    cost_per_1k_tokens=0.003,
                    avg_latency_ms=1000,
                    quality_score=0.95,
                ),
                priority=85,
                fallback_models=["gpt_4o", "claude_3_haiku"],
            )
        )

        self.add_model(
            ModelConfig(
                id="claude_3_haiku",
                name="Claude 3 Haiku",
                provider=ModelProvider.ANTHROPIC,
                model_type=ModelType.LANGUAGE,
                capabilities=ModelCapability(
                    max_tokens=200000,
                    supports_streaming=True,
                    supports_function_calling=False,
                    supports_vision=True,
                    languages=["en", "vi", "zh", "es", "fr"],
                    cost_per_1k_tokens=0.00025,
                    avg_latency_ms=400,
                    quality_score=0.80,
                ),
                priority=70,
                fallback_models=["gpt_4o_mini", "llama_3_1_8b_local"],
            )
        )

        # Embedding models
        self.add_model(
            ModelConfig(
                id="text_embedding_3_large",
                name="OpenAI Text Embedding 3 Large",
                provider=ModelProvider.OPENAI,
                model_type=ModelType.EMBEDDING,
                capabilities=ModelCapability(
                    max_tokens=8191,
                    languages=["en", "vi", "zh", "es", "fr"],
                    cost_per_1k_tokens=0.00013,
                    avg_latency_ms=300,
                    quality_score=0.90,
                ),
                priority=85,
            )
        )

        self.add_model(
            ModelConfig(
                id="bge_large_local",
                name="BGE Large (Local)",
                provider=ModelProvider.LOCAL,
                model_type=ModelType.EMBEDDING,
                capabilities=ModelCapability(
                    max_tokens=512,
                    languages=["en", "vi", "zh"],
                    cost_per_1k_tokens=0.0,
                    avg_latency_ms=200,
                    quality_score=0.85,
                ),
                priority=90,
                fallback_models=["text_embedding_3_large"],
            )
        )

    def add_model(self, model: ModelConfig) -> None:
        """Add or update a model configuration."""
        self.models[model.id] = model
        logger.info(f"Added model: {model.name} ({model.id})")

    def remove_model(self, model_id: str) -> None:
        """Remove a model configuration."""
        if model_id in self.models:
            del self.models[model_id]
            logger.info(f"Removed model: {model_id}")

    def get_model(self, model_id: str) -> ModelConfig | None:
        """Get model configuration by ID."""
        return self.models.get(model_id)

    async def select_model(
        self,
        requirements: TaskRequirements,
        exclude_models: list[str] | None = None,
    ) -> ModelConfig | None:
        """
        Select best model for task requirements.

        Args:
            requirements: Task requirements
            exclude_models: Models to exclude from selection

        Returns:
            Best matching model or None if no suitable model found
        """
        exclude_models = exclude_models or []
        candidates = []

        # Filter models by requirements
        for model in self.models.values():
            if not model.enabled or model.id in exclude_models:
                continue

            if not self._model_meets_requirements(model, requirements):
                continue

            # Check if model is available (not overloaded)
            if model.metrics.current_load >= model.max_concurrent:
                continue

            candidates.append(model)

        if not candidates:
            logger.warning("No suitable models found for requirements")
            return None

        # Score and rank candidates
        scored_candidates = []
        for model in candidates:
            score = self._calculate_model_score(model, requirements)
            scored_candidates.append((score, model))

        # Sort by score (descending)
        scored_candidates.sort(key=lambda x: x[0], reverse=True)

        # Select best model
        best_model = scored_candidates[0][1]

        # Update selection history
        self.selection_history.append(
            {
                "timestamp": time.time(),
                "selected_model": best_model.id,
                "requirements": requirements,
                "score": scored_candidates[0][0],
                "candidates_count": len(candidates),
            }
        )

        # Keep only last 1000 selections
        if len(self.selection_history) > 1000:
            self.selection_history = self.selection_history[-1000:]

        logger.info(
            f"Selected model: {best_model.name} (score: {scored_candidates[0][0]:.3f})"
        )
        return best_model

    def _model_meets_requirements(
        self, model: ModelConfig, requirements: TaskRequirements
    ) -> bool:
        """Check if model meets basic requirements."""
        caps = model.capabilities

        # Model type match
        if model.model_type != requirements.model_type:
            # Allow multimodal models for any type
            if model.model_type != ModelType.MULTIMODAL:
                return False

        # Token limit
        if caps.max_tokens < requirements.max_tokens:
            return False

        # Feature requirements
        if requirements.requires_streaming and not caps.supports_streaming:
            return False

        if (
            requirements.requires_function_calling
            and not caps.supports_function_calling
        ):
            return False

        if requirements.requires_vision and not caps.supports_vision:
            return False

        if requirements.requires_audio and not caps.supports_audio:
            return False

        # Language support
        if requirements.language not in caps.languages:
            return False

        # Quality requirement
        if caps.quality_score < requirements.quality_requirement:
            return False

        return True

    def _calculate_model_score(
        self, model: ModelConfig, requirements: TaskRequirements
    ) -> float:
        """Calculate selection score for model."""
        score = 0.0
        caps = model.capabilities
        metrics = model.metrics

        # Base priority score (0-1)
        score += model.priority / 100.0

        # Quality score (0-1)
        score += caps.quality_score

        # Cost efficiency score (0-1, inverted)
        if requirements.cost_sensitivity == "high":
            cost_weight = 0.8
        elif requirements.cost_sensitivity == "medium":
            cost_weight = 0.5
        else:
            cost_weight = 0.2

        # Local models get max cost score
        if model.provider == ModelProvider.LOCAL:
            cost_score = 1.0
        else:
            # Normalize cost (assuming max cost is $0.01 per 1k tokens)
            cost_score = max(0, 1.0 - (caps.cost_per_1k_tokens / 0.01))
        score += cost_score * cost_weight

        # Latency score (0-1, inverted)
        if requirements.latency_sensitivity == "high":
            latency_weight = 0.8
        elif requirements.latency_sensitivity == "medium":
            latency_weight = 0.5
        else:
            latency_weight = 0.2

        # Normalize latency (assuming max latency is 5000ms)
        latency_score = max(0, 1.0 - (caps.avg_latency_ms / 5000))
        score += latency_score * latency_weight

        # Reliability score (0-1)
        if metrics.total_requests > 0:
            reliability_score = metrics.successful_requests / metrics.total_requests
            score += reliability_score * 0.3

        # Load balancing - prefer less loaded models
        load_factor = model.metrics.current_load / model.max_concurrent
        load_score = 1.0 - load_factor
        score += load_score * 0.2

        # Recent usage penalty to encourage diversity
        time_since_last_use = time.time() - metrics.last_used
        if time_since_last_use > 3600:  # 1 hour
            score += 0.1  # Small bonus for unused models

        return score

    async def get_model_with_fallback(
        self,
        requirements: TaskRequirements,
        max_retries: int = 3,
    ) -> ModelConfig | None:
        """
        Get model with automatic fallback on failure.

        Args:
            requirements: Task requirements
            max_retries: Maximum retry attempts

        Returns:
            Available model or None if all fail
        """
        exclude_models = []

        for attempt in range(max_retries):
            model = await self.select_model(requirements, exclude_models)

            if model is None:
                logger.error(f"No model available (attempt {attempt + 1})")
                break

            # Test model availability
            if await self._test_model_availability(model):
                return model

            # Add to exclusion list and try fallbacks
            exclude_models.append(model.id)
            exclude_models.extend(model.fallback_models)

            logger.warning(f"Model {model.id} unavailable, trying fallback...")

        return None

    async def _test_model_availability(self, model: ModelConfig) -> bool:
        """Test if model is currently available."""
        # For local models, check if service is running
        if model.provider == ModelProvider.LOCAL:
            # Could ping local service endpoint
            return True  # Assume available for now

        # For cloud models, could test with a simple API call
        # For now, just check if not overloaded
        return model.metrics.current_load < model.max_concurrent

    async def update_model_metrics(
        self,
        model_id: str,
        latency_ms: float,
        success: bool,
        tokens_processed: int = 0,
        cost: float = 0.0,
    ) -> None:
        """Update model performance metrics."""
        async with self.lock:
            if model_id not in self.models:
                return

            model = self.models[model_id]
            metrics = model.metrics

            # Update counters
            metrics.total_requests += 1
            if success:
                metrics.successful_requests += 1
            else:
                metrics.failed_requests += 1

            # Update averages
            if metrics.total_requests == 1:
                metrics.avg_latency_ms = latency_ms
            else:
                # Exponential moving average
                alpha = 0.1  # Learning rate
                metrics.avg_latency_ms = (
                    alpha * latency_ms + (1 - alpha) * metrics.avg_latency_ms
                )

            # Update totals
            metrics.total_tokens_processed += tokens_processed
            metrics.total_cost += cost
            metrics.last_used = time.time()

    async def increment_load(self, model_id: str) -> None:
        """Increment current load for model."""
        async with self.lock:
            if model_id in self.models:
                self.models[model_id].metrics.current_load += 1

    async def decrement_load(self, model_id: str) -> None:
        """Decrement current load for model."""
        async with self.lock:
            if model_id in self.models:
                model = self.models[model_id]
                model.metrics.current_load = max(0, model.metrics.current_load - 1)

    def get_models_by_type(self, model_type: ModelType) -> list[ModelConfig]:
        """Get all models of a specific type."""
        return [
            model
            for model in self.models.values()
            if model.model_type == model_type and model.enabled
        ]

    def get_available_models(self) -> list[ModelConfig]:
        """Get all currently available models."""
        return [
            model
            for model in self.models.values()
            if model.enabled and model.metrics.current_load < model.max_concurrent
        ]

    def get_router_stats(self) -> dict[str, Any]:
        """Get router statistics."""
        total_models = len(self.models)
        enabled_models = len([m for m in self.models.values() if m.enabled])
        available_models = len(self.get_available_models())

        # Provider distribution
        provider_counts = {}
        for model in self.models.values():
            provider = model.provider.value
            provider_counts[provider] = provider_counts.get(provider, 0) + 1

        # Type distribution
        type_counts = {}
        for model in self.models.values():
            model_type = model.model_type.value
            type_counts[model_type] = type_counts.get(model_type, 0) + 1

        # Selection history stats
        recent_selections = self.selection_history[-100:]  # Last 100
        popular_models = {}
        for selection in recent_selections:
            model_id = selection["selected_model"]
            popular_models[model_id] = popular_models.get(model_id, 0) + 1

        return {
            "total_models": total_models,
            "enabled_models": enabled_models,
            "available_models": available_models,
            "provider_distribution": provider_counts,
            "type_distribution": type_counts,
            "popular_models": dict(
                sorted(popular_models.items(), key=lambda x: x[1], reverse=True)[:5]
            ),
            "selection_history_count": len(self.selection_history),
            "model_health": {
                model_id: {
                    "success_rate": (
                        model.metrics.successful_requests
                        / model.metrics.total_requests
                        * 100
                        if model.metrics.total_requests > 0
                        else 0
                    ),
                    "avg_latency_ms": model.metrics.avg_latency_ms,
                    "current_load": model.metrics.current_load,
                    "total_cost": model.metrics.total_cost,
                }
                for model_id, model in self.models.items()
                if model.metrics.total_requests > 0
            },
        }


# Global router instance
_router_instance: EnhancedModelRouter | None = None


def get_model_router() -> EnhancedModelRouter:
    """Get global model router instance."""
    global _router_instance
    if _router_instance is None:
        _router_instance = EnhancedModelRouter()
    return _router_instance


__all__ = [
    "EnhancedModelRouter",
    "ModelType",
    "ModelProvider",
    "ModelConfig",
    "ModelCapability",
    "ModelMetrics",
    "TaskRequirements",
    "get_model_router",
]
