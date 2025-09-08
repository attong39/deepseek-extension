"""
RAG Engine - CPU-first, GPU-ready

Sentence-Transformers + FAISS for embedding and vector search.
GPU activation via ZETA_USE_GPU=1 environment variable.
"""

from __future__ import annotations

import os
import logging
from typing import Any

import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import Exception
import ImportError
import ValueError
import batch_size
import bool
import dict
import e
import enumerate
import float
import i
import idx
import int
import k
import len
import list
import meta
import model_name
import normalize
import print
import query
import result
import score
import score_threshold
import self
import str
import text
import texts
import tuple
import zip

logger = logging.getLogger(__name__)

# Default model - lightweight and CPU-friendly
DEFAULT_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


class RAGEmbedder:
    """CPU-first embedding engine with GPU fallback."""
    
    def __init__(
        self,
        model_name: str = DEFAULT_MODEL,
        device: str | None = None,
    ) -> None:
        self.model_name = model_name
        
        # Auto-detect device based on environment
        if device is None:
            device = self._get_device()
        
        self.device = device
        logger.info(f"Initializing RAG embedder on {device}")
        
        try:
            self.model = SentenceTransformer(
                model_name,
                device=device,
                trust_remote_code=False,  # Security
            )
            logger.info(f"Loaded model: {model_name}")
        except Exception as e:
            logger.error(f"Failed to load model {model_name}: {e}")
            raise
    
    def _get_device(self) -> str:
        """Auto-detect optimal device."""
        if os.getenv("ZETA_USE_GPU") == "1":
            try:
                import torch
                if torch.cuda.is_available():
                    logger.info("GPU detected and enabled via ZETA_USE_GPU=1")
                    return "cuda"
                else:
                    logger.warning("ZETA_USE_GPU=1 but no CUDA available, using CPU")
            except ImportError:
                logger.warning("PyTorch not available, using CPU")
        
        return "cpu"
    
    def encode(
        self,
        texts: list[str],
        normalize: bool = True,
        batch_size: int = 32,
    ) -> np.ndarray:
        """Encode texts to embeddings."""
        if not texts:
            return np.array([])
        
        try:
            embeddings = self.model.encode(
                texts,
                batch_size=batch_size,
                convert_to_numpy=True,
                normalize_embeddings=normalize,
                show_progress_bar=len(texts) > 100,
            )
            logger.debug(f"Encoded {len(texts)} texts to {embeddings.shape}")
            return embeddings
        except Exception as e:
            logger.error(f"Encoding failed: {e}")
            raise


class RAGIndex:
    """FAISS-based vector index for similarity search."""
    
    def __init__(self, dimension: int = 384) -> None:
        self.dimension = dimension
        self.index = faiss.IndexFlatIP(dimension)  # Inner product (cosine sim)
        self.texts: list[str] = []
        self.metadata: list[dict[str, Any]] = []
        logger.info(f"Initialized FAISS index with dimension {dimension}")
    
    def add(
        self,
        embeddings: np.ndarray,
        texts: list[str],
        metadata: list[dict[str, Any]] | None = None,
    ) -> None:
        """Add embeddings to the index."""
        if embeddings.size == 0:
            return
        
        # Ensure float32 for FAISS
        embeddings = embeddings.astype(np.float32)
        
        # Validate dimensions
        if embeddings.shape[1] != self.dimension:
            raise ValueError(
                f"Embedding dimension {embeddings.shape[1]} doesn't match "
                f"index dimension {self.dimension}"
            )
        
        # Add to FAISS index
        self.index.add(embeddings)
        
        # Store texts and metadata
        self.texts.extend(texts)
        if metadata is None:
            metadata = [{}] * len(texts)
        self.metadata.extend(metadata)
        
        logger.debug(f"Added {len(texts)} documents to index")
    
    def search(
        self,
        query_embedding: np.ndarray,
        k: int = 5,
        score_threshold: float = 0.0,
    ) -> tuple[list[int], list[float], list[str], list[dict[str, Any]]]:
        """Search for similar documents."""
        if self.index.ntotal == 0:
            return [], [], [], []
        
        # Ensure query is 2D and float32
        if query_embedding.ndim == 1:
            query_embedding = query_embedding.reshape(1, -1)
        query_embedding = query_embedding.astype(np.float32)
        
        # Search
        scores, indices = self.index.search(query_embedding, k)
        
        # Filter by score threshold
        valid_mask = scores[0] >= score_threshold
        indices = indices[0][valid_mask]
        scores = scores[0][valid_mask]
        
        # Get corresponding texts and metadata
        result_texts = [self.texts[i] for i in indices]
        result_metadata = [self.metadata[i] for i in indices]
        
        return (
            indices.tolist(),
            scores.tolist(),
            result_texts,
            result_metadata,
        )
    
    def size(self) -> int:
        """Get number of documents in index."""
        return self.index.ntotal


class RAGEngine:
    """Complete RAG engine combining embedding and search."""
    
    def __init__(
        self,
        model_name: str = DEFAULT_MODEL,
        device: str | None = None,
    ) -> None:
        self.embedder = RAGEmbedder(model_name, device)
        
        # Initialize index with model's embedding dimension
        # all-MiniLM-L6-v2 has 384 dimensions
        dimension = 384
        self.index = RAGIndex(dimension)
        
        logger.info("RAG engine initialized")
    
    def add_documents(
        self,
        texts: list[str],
        metadata: list[dict[str, Any]] | None = None,
        batch_size: int = 32,
    ) -> None:
        """Add documents to the RAG index."""
        if not texts:
            return
        
        logger.info(f"Adding {len(texts)} documents to RAG index")
        
        # Encode texts in batches
        embeddings = self.embedder.encode(texts, batch_size=batch_size)
        
        # Add to index
        self.index.add(embeddings, texts, metadata)
        
        logger.info(f"RAG index now contains {self.index.size()} documents")
    
    def search(
        self,
        query: str,
        k: int = 5,
        score_threshold: float = 0.1,
    ) -> list[dict[str, Any]]:
        """Search for relevant documents."""
        if not query.strip():
            return []
        
        # Encode query
        query_embedding = self.embedder.encode([query])
        
        # Search
        indices, scores, texts, metadata = self.index.search(
            query_embedding,
            k=k,
            score_threshold=score_threshold,
        )
        
        # Format results
        results = []
        for i, (idx, score, text, meta) in enumerate(
            zip(indices, scores, texts, metadata)
        ):
            results.append({
                "rank": i + 1,
                "index": idx,
                "score": float(score),
                "text": text,
                "metadata": meta,
            })
        
        logger.debug(f"Found {len(results)} relevant documents for query")
        return results


# Factory function for easy initialization
def create_rag_engine(
    model_name: str = DEFAULT_MODEL,
    device: str | None = None,
) -> RAGEngine:
    """Create a RAG engine with specified configuration."""
    return RAGEngine(model_name, device)


# Example usage for testing
def _test_rag():
    """Test the RAG engine."""
    engine = create_rag_engine()
    
    # Add sample documents
    docs = [
        "Python is a programming language",
        "FastAPI is a web framework for Python",
        "Machine learning uses algorithms to learn patterns",
        "Vector databases store embeddings",
        "RAG combines retrieval and generation",
    ]
    
    engine.add_documents(docs)
    
    # Search
    results = engine.search("Python web development", k=3)
    
    for result in results:
        print(f"Score: {result['score']:.3f} - {result['text']}")


if __name__ == "__main__":
    _test_rag()
