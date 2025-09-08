from __future__ import annotations

import hashlib
import time
from typing import Any
import Exception
import a
import b
import cache
import dict
import embedder
import float
import i
import int
import len
import list
import metadata
import question
import r
import range
import redis
import reranker
import result
import retriever
import self
import sorted
import str
import sum
import text
import top_k
import ttl_seconds
import x
import zip


class AutoEmbedder:
    """Minimal embedder implementation for production"""

    def embed(self, text: str) -> list[float]:
        # Simple hash-based embedding for demo
        h = hashlib.sha256(text.encode())
        hash_int = int(h.hexdigest()[:16], 16)
        return [float((hash_int >> i) & 1) for i in range(384)]


class InMemoryRetriever:
    """In-memory document retriever"""

    def __init__(self, embedder: AutoEmbedder):
        self.embedder = embedder
        self.docs: list[dict[str, Any]] = []

    def add_document(self, text: str, metadata: dict | None = None):
        """Add document to the retriever"""
        doc = {
            "text": text,
            "embedding": self.embedder.embed(text),
            "metadata": metadata or {},
        }
        self.docs.append(doc)

    def search(self, query: str, top_k: int = 5) -> list[dict[str, Any]]:
        """Search for relevant documents"""
        if not self.docs:
            return [{"text": f"Mock result for: {query}", "metadata": {}}]

        query_emb = self.embedder.embed(query)
        results = []
        for doc in self.docs:
            # Simple cosine similarity
            score = sum(
                a * b for a, b in zip(query_emb, doc["embedding"], strict=False)
            )
            results.append({"doc": doc, "score": score})

        results.sort(key=lambda x: x["score"], reverse=True)
        return [r["doc"] for r in results[:top_k]]


class SimpleReranker:
    """Simple reranker implementation"""

    def rerank(self, query: str, docs: list[dict]) -> list[dict]:
        # Simple reranker based on text length
        return sorted(docs, key=lambda x: len(x.get("text", "")), reverse=True)


class RAGCache:
    """Simple cache implementation for RAG results"""

    def __init__(self, redis=None, ttl_seconds: int = 600):
        self.redis = redis
        self.ttl = ttl_seconds
        self._cache: dict[str, Any] = {}

    def _key(self, query: str) -> str:
        return f"rag:{hashlib.sha256(query.encode()).hexdigest()}"  # SHA256 instead of weak MD5

    def get(self, query: str) -> dict | None:
        """Get cached result"""
        key = self._key(query)
        if self.redis:
            try:
                # Skip async redis for sync version
                pass
            except Exception:
                pass
        return self._cache.get(key)

    def set(self, query: str, result: dict):
        """Set cached result"""
        key = self._key(query)
        if self.redis:
            try:
                # Skip redis for now - can be implemented later
                pass
            except Exception:
                pass
        self._cache[key] = result


class RAGPipeline:
    """Main RAG pipeline orchestrator"""

    def __init__(
        self,
        embedder: AutoEmbedder,
        retriever: InMemoryRetriever,
        reranker: SimpleReranker,
        cache: RAGCache,
    ):
        self.embedder = embedder
        self.retriever = retriever
        self.reranker = reranker
        self.cache = cache
        self._init_demo_data()

    def _init_demo_data(self):
        """Initialize with demo documents"""
        self.retriever.add_document(
            "ZETA_VN là hệ thống trợ lý AI được xây dựng với FastAPI, RAG pipeline, và EventBus.",
            {"source": "guide"},
        )
        self.retriever.add_document(
            "Hệ thống sử dụng async SQLAlchemy, Redis cache, và DI container để đảm bảo hiệu năng cao.",
            {"source": "performance"},
        )
        self.retriever.add_document(
            "Architecture bao gồm domain-driven design với clean architecture patterns.",
            {"source": "architecture"},
        )

    def query(self, question: str) -> dict[str, Any]:
        """Process RAG query"""
        # Check cache first
        cached = self.cache.get(question)
        if cached:
            return cached

        # Search documents
        docs = self.retriever.search(question)

        # Rerank documents
        docs = self.reranker.rerank(question, docs)

        # Generate answer
        if docs:
            answer = (
                f"Dựa trên {len(docs)} tài liệu, đây là câu trả lời cho: {question}"
            )
            sources = [doc.get("text", "")[:100] + "..." for doc in docs[:3]]
        else:
            answer = f"Xin lỗi, tôi chưa có thông tin về: {question}"
            sources = []

        _ = {"answer": answer, "sources": sources, "timestamp": time.time()}

        # Cache result
        self.cache.set(question, result)
        return result
