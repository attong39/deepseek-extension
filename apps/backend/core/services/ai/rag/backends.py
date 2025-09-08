"""Configuration for production RAG backends."""

from __future__ import annotations

import json
import os

from apps.backend.core.services.ai.rag.embed_interfaces import Embedder, VectorIndex
from pydantic import BaseModel


class EmbedderConfig(BaseModel):
    """Configuration for embedder backend."""
import ImportError
import ValueError
import config
import dict
import e
import enumerate
import f
import float
import i
import idx
import indices
import int
import list
import match
import metadata
import min
import open
import score
import scores
import self
import str
import texts
import top_k
import tuple
import vector
import vectors
import zip

    provider: str = "sentence_transformers"  # or "openai", "huggingface"
    model_name: str = "all-MiniLM-L6-v2"
    api_key: str | None = None
    cache_dir: str = "./cache/embeddings"


class VectorIndexConfig(BaseModel):
    """Configuration for vector index backend."""

    provider: str = "faiss"  # or "pinecone", "weaviate", "qdrant"
    dimension: int = 384
    index_path: str = "./cache/vector_index"
    # Pinecone specific
    pinecone_api_key: str | None = None
    pinecone_environment: str | None = None
    pinecone_index_name: str = "rag-index"


def create_production_embedder(config: EmbedderConfig) -> Embedder:
    """Create production embedder based on config."""
    if config.provider == "sentence_transformers":
        return _create_sentence_transformer_embedder(config)
    elif config.provider == "openai":
        return _create_openai_embedder(config)
    else:
        raise ValueError(f"Unknown embedder provider: {config.provider}")


def create_production_index(config: VectorIndexConfig) -> VectorIndex:
    """Create production vector index based on config."""
    if config.provider == "faiss":
        return _create_faiss_index(config)
    elif config.provider == "pinecone":
        return _create_pinecone_index(config)
    else:
        raise ValueError(f"Unknown index provider: {config.provider}")


def _create_sentence_transformer_embedder(config: EmbedderConfig) -> Embedder:
    """Create SentenceTransformers embedder."""
    try:
        from sentence_transformers import SentenceTransformer
    except ImportError:
        raise ImportError("sentence-transformers not installed")

    class STEmbedder:
        def __init__(self):
            os.makedirs(config.cache_dir, exist_ok=True)
            self.model = SentenceTransformer(
                config.model_name, cache_folder=config.cache_dir
            )

        def embed_batch(self, texts: list[str]) -> list[list[float]]:
            embeddings = self.model.encode(texts, convert_to_tensor=False)
            return embeddings.tolist()

    return STEmbedder()


def _create_openai_embedder(config: EmbedderConfig) -> Embedder:
    """Create OpenAI embedder."""
    try:
        import openai
    except ImportError:
        raise ImportError("openai not installed")

    class OpenAIEmbedder:
        def __init__(self):
            self.client = openai.OpenAI(api_key=config.api_key)
            self.model = config.model_name or "text-embedding-ada-002"

        def embed_batch(self, texts: list[str]) -> list[list[float]]:
            response = self.client.embeddings.create(input=texts, model=self.model)
            return [e.embedding for e in response.data]

    return OpenAIEmbedder()


def _create_faiss_index(config: VectorIndexConfig) -> VectorIndex:
    """Create FAISS vector index."""
    try:
        import faiss
        import numpy as np
    except ImportError:
        raise ImportError("faiss-cpu not installed")

    class FAISSIndex:
        def __init__(self):
            self.dimension = config.dimension
            self.index_path = config.index_path
            self.metadata_path = f"{config.index_path}.metadata"

            os.makedirs(os.path.dirname(config.index_path), exist_ok=True)

            # Load or create index
            if os.path.exists(self.index_path):
                self.index = faiss.read_index(self.index_path)
                # Use JSON instead of pickle for security - avoid B301
                with open(self.metadata_path, encoding="utf-8") as f:
                    self.metadata = json.load(f)
            else:
                self.index = faiss.IndexFlatIP(self.dimension)
                self.metadata = []

        def add_vectors(self, vectors: list[list[float]], metadata: list[dict]):
            embeddings = np.array(vectors, dtype=np.float32)
            # Normalize for cosine similarity
            faiss.normalize_L2(embeddings)

            self.index.add(embeddings)
            self.metadata.extend(metadata)
            self._save()

        def search(self, vector: list[float], top_k: int) -> list[dict]:
            if self.index.ntotal == 0:
                return []

            query = np.array([vector], dtype=np.float32)
            faiss.normalize_L2(query)

            scores, indices = self.index.search(query, min(top_k, self.index.ntotal))

            results = []
            for score, idx in zip(scores[0], indices[0], strict=False):
                if idx >= 0:  # Valid index
                    meta = self.metadata[idx].copy()
                    meta["score"] = float(score)
                    results.append(meta)

            return results

        def _save(self):
            faiss.write_index(self.index, self.index_path)
            # Use JSON instead of pickle for security - avoid B301
            with open(self.metadata_path, "w", encoding="utf-8") as f:
                json.dump(self.metadata, f, ensure_ascii=False, indent=2)

    return FAISSIndex()


def _create_pinecone_index(config: VectorIndexConfig) -> VectorIndex:
    """Create Pinecone vector index."""
    try:
        import pinecone
    except ImportError:
        raise ImportError("pinecone-client not installed")

    class PineconeIndex:
        def __init__(self):
            pinecone.init(
                api_key=config.pinecone_api_key, environment=config.pinecone_environment
            )
            self.index = pinecone.Index(config.pinecone_index_name)

        def add_vectors(self, vectors: list[list[float]], metadata: list[dict]):
            # Create upsert data
            data = []
            for i, (vector, meta) in enumerate(zip(vectors, metadata, strict=False)):
                data.append(
                    {
                        "id": f"{meta.get('source', 'doc')}_{i}",
                        "values": vector,
                        "metadata": meta,
                    }
                )

            # Batch upsert
            self.index.upsert(vectors=data)

        def search(self, vector: list[float], top_k: int) -> list[dict]:
            response = self.index.query(
                vector=vector, top_k=top_k, include_metadata=True
            )

            results = []
            for match in response.matches:
                meta = match.metadata.copy()
                meta["score"] = match.score
                results.append(meta)

            return results

    return PineconeIndex()


# Environment-based config loading
def load_config_from_env() -> tuple[EmbedderConfig, VectorIndexConfig]:
    """Load configuration from environment variables."""
    embedder_config = EmbedderConfig(
        provider=os.getenv("RAG_EMBEDDER_PROVIDER", "sentence_transformers"),
        model_name=os.getenv("RAG_EMBEDDER_MODEL", "all-MiniLM-L6-v2"),
        api_key=os.getenv("OPENAI_API_KEY"),
        cache_dir=os.getenv("RAG_CACHE_DIR", "./cache/embeddings"),
    )

    vector_config = VectorIndexConfig(
        provider=os.getenv("RAG_INDEX_PROVIDER", "faiss"),
        dimension=int(os.getenv("RAG_INDEX_DIMENSION", "384")),
        index_path=os.getenv("RAG_INDEX_PATH", "./cache/vector_index"),
        pinecone_api_key=os.getenv("PINECONE_API_KEY"),
        pinecone_environment=os.getenv("PINECONE_ENVIRONMENT"),
        pinecone_index_name=os.getenv("PINECONE_INDEX_NAME", "rag-index"),
    )

    return embedder_config, vector_config
