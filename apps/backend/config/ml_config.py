"""Machine Learning configuration for ZETA AI system.

This module provides ML-specific settings including model configurations,
training parameters, and inference settings.
"""

from __future__ import annotations

from pydantic import Field, validator
from pydantic_settings import BaseSettings, SettingsConfigDict
import AttributeError
import bool
import dict
import float
import getattr
import int
import isinstance
import list
import metric
import name
import pattern
import self
import str
import v

DEFAULT_GPT35_TURBO = "gpt-3.5-turbo"


class MLSettings(BaseSettings):
    """Machine Learning configuration settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Model Configuration
    default_model_provider: str = Field(default="openai")
    default_chat_model: str = Field(default="gpt-4")
    default_embedding_model: str = Field(default="text-embedding-ada-002")
    default_completion_model: str = Field(default=DEFAULT_GPT35_TURBO)

    # OpenAI Configuration
    openai_api_key: str | None = Field(default=None)
    openai_organization: str | None = Field(default=None)
    openai_base_url: str = Field(default="https://api.openai.com/v1")
    openai_timeout: int = Field(default=60)
    openai_max_retries: int = Field(default=3)

    # Anthropic Configuration
    anthropic_api_key: str | None = Field(default=None)
    anthropic_base_url: str = Field(default="https://api.anthropic.com")
    anthropic_timeout: int = Field(default=60)
    anthropic_max_retries: int = Field(default=3)

    # Hugging Face Configuration
    huggingface_api_key: str | None = Field(default=None)
    huggingface_base_url: str = Field(default="https://api-inference.huggingface.co")
    huggingface_timeout: int = Field(default=120)
    huggingface_max_retries: int = Field(default=3)

    # Google Cloud AI Configuration
    gcp_project_id: str | None = Field(default=None)
    gcp_credentials_path: str | None = Field(default=None)
    gcp_location: str = Field(default="us-central1")

    # Model Parameters
    default_temperature: float = Field(default=0.7)
    default_max_tokens: int = Field(default=1000)
    default_top_p: float = Field(default=1.0)
    default_frequency_penalty: float = Field(default=0.0)
    default_presence_penalty: float = Field(default=0.0)

    # Chat Configuration
    max_conversation_length: int = Field(default=20)
    max_context_tokens: int = Field(default=4000)
    context_window_overlap: int = Field(default=200)
    enable_conversation_memory: bool = Field(default=True)

    # Streaming & Retrieval feature flags
    fast_streaming: bool = Field(
        default=True, description="Enable low-latency streaming mode"
    )
    hybrid_retrieval: bool = Field(
        default=True, description="Enable hybrid keyword+vector retrieval"
    )

    # Embedding Configuration
    embedding_dimension: int = Field(default=1536)  # OpenAI ada-002
    embedding_batch_size: int = Field(default=100)
    embedding_cache_enabled: bool = Field(default=True)
    embedding_cache_ttl: int = Field(default=3600)  # 1 hour
    # Back-compat/flags alias (handled in environment or app settings)

    # Vector Database Configuration
    vector_db_provider: str = Field(default="pinecone")  # pinecone, chroma, weaviate
    vector_db_index_name: str = Field(default="zeta-embeddings")
    vector_db_metric: str = Field(default="cosine")
    vector_db_dimension: int = Field(default=1536)

    # Pinecone Configuration
    pinecone_api_key: str | None = Field(default=None)
    pinecone_environment: str = Field(default="us-west1-gcp")
    pinecone_index_name: str = Field(default="zeta-ai")

    # Chroma Configuration
    chroma_host: str = Field(default="localhost")
    chroma_port: int = Field(default=8000)
    chroma_collection_name: str = Field(default="zeta_collection")

    # Training Configuration
    enable_training: bool = Field(default=False)
    training_data_path: str = Field(default="storage/training_data")
    model_checkpoint_path: str = Field(default="storage/model_checkpoints")
    training_batch_size: int = Field(default=32)
    training_learning_rate: float = Field(default=0.001)
    training_epochs: int = Field(default=10)

    # Fine-tuning Configuration
    enable_fine_tuning: bool = Field(default=False)
    fine_tuning_provider: str = Field(default="openai")
    fine_tuning_base_model: str = Field(default=DEFAULT_GPT35_TURBO)
    fine_tuning_validation_split: float = Field(default=0.2)

    # Model Evaluation
    enable_model_evaluation: bool = Field(default=True)
    evaluation_metrics: list[str] = Field(
        default=["accuracy", "precision", "recall", "f1"]
    )
    evaluation_frequency: str = Field(default="daily")  # hourly, daily, weekly

    # Caching and Performance
    model_cache_enabled: bool = Field(default=True)
    model_cache_ttl: int = Field(default=1800)  # 30 minutes
    response_cache_enabled: bool = Field(default=True)
    response_cache_ttl: int = Field(default=300)  # 5 minutes
    # RAG Cache
    rag_cache_ttl: int = Field(
        default=900, description="Default TTL for RAG cache (seconds)"
    )

    # Rate Limiting
    requests_per_minute: int = Field(default=60)
    requests_per_hour: int = Field(default=1000)
    requests_per_day: int = Field(default=10000)

    # Error Handling
    max_retries: int = Field(default=3)
    retry_delay: float = Field(default=1.0)
    exponential_backoff: bool = Field(default=True)
    fallback_model: str | None = Field(default=None)

    # Rerank & Long-context
    rerank_min_score: float = Field(
        default=0.2, description="Minimum score to keep a passage after rerank"
    )
    use_long_context_model: bool = Field(
        default=True,
        description="Prefer long-context model when input exceeds default window",
    )
    long_context_model: str = Field(
        default="gpt-4o",
        description="Model identifier for long context (>=128k tokens)",
    )

    # Monitoring and Logging
    log_model_requests: bool = Field(default=True)
    log_model_responses: bool = Field(default=False)
    track_token_usage: bool = Field(default=True)
    track_response_times: bool = Field(default=True)

    # Security
    enable_input_filtering: bool = Field(default=True)
    enable_output_filtering: bool = Field(default=True)
    max_input_length: int = Field(default=10000)
    blocked_patterns: list[str] = Field(default=[])

    # Mixture of Experts (MoE) & Shielding
    moe_default: str = Field(
        default="balanced",
        description="Default MoE strategy: balanced|latency|cost|quality|conservative",
    )
    moe_max_latency_ms: int = Field(default=2000, description="Max target latency")
    moe_cost_budget: float = Field(
        default=0.002, description="Estimated cost budget per request (USD)"
    )
    shielding_level: str = Field(
        default="moderate", description="Self-shielding level: off|moderate|strict"
    )

    # Custom Model Configuration
    custom_models: dict[str, dict] = Field(default={})
    model_aliases: dict[str, str] = Field(default={})

    # Federated Learning / DP Configuration
    fl_enabled: bool = Field(
        default=False, description="Enable Federated Learning features"
    )
    fl_clip_norm: float = Field(
        default=1.0, ge=0.0, description="L2 clipping threshold C"
    )
    fl_dp_sigma: float = Field(
        default=0.0,
        ge=0.0,
        description="Gaussian noise multiplier sigma (0 disables DP)",
    )
    fl_sample_rate: float = Field(
        default=0.1, ge=0.0, le=1.0, description="Client sampling rate per round"
    )
    fl_min_clients: int = Field(
        default=5, ge=1, description="Minimum client updates required per round"
    )
    fl_round_steps: int = Field(
        default=100, ge=1, description="Local training steps per client per round"
    )
    fl_use_secure_aggregation: bool = Field(
        default=False, description="Enable Secure Aggregation (server-side MPC)"
    )

    @validator("evaluation_metrics", pre=True)
    def parse_evaluation_metrics(cls, v):
        """Parse evaluation metrics from string or list."""
        if isinstance(v, str):
            return [metric.strip() for metric in v.split(",") if metric.strip()]
        return v

    @validator("blocked_patterns", pre=True)
    def parse_blocked_patterns(cls, v):
        """Parse blocked patterns from string or list."""
        if isinstance(v, str):
            return [pattern.strip() for pattern in v.split(",") if pattern.strip()]
        return v

    # Note: Uppercase aliases (e.g., LONG_CONTEXT_MODEL) are provided via app settings
    # or environment, not duplicated here to avoid field clashes.

    # --- Read-only UPPERCASE aliases via __getattr__ ---
    def __getattr__(self, name: str):  # pragma: no cover - dynamic alias
        mapping = {
            "LONG_CONTEXT_MODEL": "long_context_model",
            "RAG_CACHE_TTL": "rag_cache_ttl",
            "RERANK_MIN_SCORE": "rerank_min_score",
            "FAST_STREAMING": "fast_streaming",
            "HYBRID_RETRIEVAL": "hybrid_retrieval",
            "EMBEDDING_BATCH_SIZE": "embedding_batch_size",
        }
        if name in mapping:
            return getattr(self, mapping[name])
        raise AttributeError(name)


def get_ml_settings() -> MLSettings:
    """Get ML settings instance."""
    return MLSettings()


# Model Provider Constants
class ModelProvider:
    """Model provider constants."""

    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    HUGGINGFACE = "huggingface"
    GOOGLE = "google"
    CUSTOM = "custom"


# Model Types
class ModelType:
    """Model type constants."""

    CHAT = "chat"
    COMPLETION = "completion"
    EMBEDDING = "embedding"
    IMAGE = "image"
    AUDIO = "audio"
    CLASSIFICATION = "classification"
    GENERATION = "generation"


# Vector Database Providers
class VectorDBProvider:
    """Vector database provider constants."""

    PINECONE = "pinecone"
    CHROMA = "chroma"
    WEAVIATE = "weaviate"
    QDRANT = "qdrant"
    MILVUS = "milvus"


# Evaluation Metrics
class EvaluationMetric:
    """Evaluation metric constants."""

    ACCURACY = "accuracy"
    PRECISION = "precision"
    RECALL = "recall"
    F1_SCORE = "f1"
    ROUGE = "rouge"
    BLEU = "bleu"
    PERPLEXITY = "perplexity"
    COHERENCE = "coherence"


# Default Model Configurations
DEFAULT_MODEL_CONFIGS = {
    ModelProvider.OPENAI: {
        "chat": {
            "model": "gpt-4",
            "temperature": 0.7,
            "max_tokens": 1000,
            "top_p": 1.0,
        },
        "completion": {
            "model": "gpt-3.5-turbo-instruct",
            "temperature": 0.7,
            "max_tokens": 1000,
        },
        "embedding": {
            "model": "text-embedding-ada-002",
            "dimension": 1536,
        },
    },
    ModelProvider.ANTHROPIC: {
        "chat": {
            "model": "claude-3-opus-20240229",
            "max_tokens": 1000,
            "temperature": 0.7,
        },
    },
    ModelProvider.HUGGINGFACE: {
        "chat": {
            "model": "microsoft/DialoGPT-large",
            "max_length": 1000,
            "temperature": 0.7,
        },
        "embedding": {
            "model": "sentence-transformers/all-MiniLM-L6-v2",
            "dimension": 384,
        },
    },
}

# Common prompts and templates
SYSTEM_PROMPTS = {
    "default": "You are a helpful AI assistant.",
    "creative": "You are a creative AI assistant that thinks outside the box.",
    "analytical": "You are an analytical AI assistant that provides detailed analysis.",
    "conversational": "You are a friendly AI assistant that engages in natural conversation.",
}

# Token limits by model
TOKEN_LIMITS = {
    "gpt-4": 8192,
    "gpt-4-32k": 32768,
    "gpt-4o": 128000,
    "gpt-4o-mini": 128000,
    "gpt-3.5-turbo": 4096,
    "gpt-3.5-turbo-16k": 16384,
    "claude-3-opus-20240229": 200000,
    "claude-3-sonnet-20240229": 200000,
    "claude-3-haiku-20240307": 200000,
}
