from __future__ import annotations

import asyncio
import json
import pickle
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any, Literal

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import Exception
import RuntimeError
import ValueError
import bool
import content
import dict
import dimension
import distance
import distances
import doc
import e
import enable_gpu
import enumerate
import f
import float
import hasattr
import hash
import i
import idx
import index_type
import indices
import int
import key
import len
import limit
import list
import logger
import max
import max_memory_mb
import metric_name
import min
import model_name
import new_value
import open
import query_vector
import search_mode
import self
import storage_path
import str
import text
import thread_pool_size
import threshold
import tuple
import zip

"""
FAISS Vector Store - Enterprise-grade vector storage and retrieval.
Features:
- High-performance similarity search với FAISS
- Advanced indexing strategies và optimization
- Comprehensive metrics và monitoring
- Async operations với performance optimization
- Enterprise security và error handling
- Resource management và memory optimization
"""
INDEX_FILENAME = "index.faiss"
DOCUMENTS_FILENAME = "documents.pkl"
METRICS_FILENAME = "metrics.json"
IndexType = Literal["Flat", "IVF", "HNSW", "PQ"]
SearchMode = Literal["exact", "approximate", "hybrid"]


class FAISSVectorStore:
    """
    Enterprise-grade FAISS vector store với advanced features.
    Features:
    - Multiple index types (Flat, IVF, HNSW, PQ) for different use cases
    - Intelligent caching và memory management
    - Performance monitoring với detailed metrics
    - Batch operations for high throughput
    - Error recovery và data integrity checks
    - Async operations với thread pool optimization
    """

    def __init__(
        self,
        model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
        index_type: IndexType = "IVF",
        storage_path: str = "./data/vector_store",
        dimension: int = 384,
        max_memory_mb: int = 1024,
        enable_gpu: bool = False,
        thread_pool_size: int = 4,
    ) -> None:
        self.model_name = model_name
        self.index_type = index_type
        self.storage_path = Path(storage_path)
        self.dimension = dimension
        self.max_memory_mb = max_memory_mb
        self.enable_gpu = enable_gpu
        self.model: SentenceTransformer | None = None
        self.index: faiss.Index | None = None
        self.documents: dict[str, dict[str, Any]] = {}
        self.id_to_position: dict[str, int] = {}
        self.position_to_id: dict[int, str] = {}
        self.thread_pool = ThreadPoolExecutor(max_workers=thread_pool_size)
        self.metrics = {
            "total_documents": 0,
            "total_searches": 0,
            "total_additions": 0,
            "total_deletions": 0,
            "cache_hits": 0,
            "cache_misses": 0,
            "average_search_time_ms": 0.0,
            "average_add_time_ms": 0.0,
            "memory_usage_mb": 0.0,
            "last_reindex_time": None,
            "uptime_seconds": 0.0,
            "error_count": 0,
            "last_backup_time": None,
        }
        self.batch_size = 100
        self.reindex_threshold = 1000
        self.cache_size = 1000
        self.backup_interval_hours = 24
        self.start_time = time.time()
        self.vector_cache: dict[str, list[float]] = {}
        self.search_cache: dict[str, list[dict[str, Any]]] = {}
        self.index_config = {
            "Flat": {"description": "Exact search, best quality"},
            "IVF": {"nlist": 100, "description": "Inverted file, good balance"},
            "HNSW": {
                "M": 16,
                "efConstruction": 200,
                "description": "Hierarchical NSW, fast search",
            },
            "PQ": {
                "m": 8,
                "nbits": 8,
                "description": "Product quantization, memory efficient",
            },
        }

    async def initialize(self) -> None:
        """
        Initialize vector store với comprehensive setup.
        Raises:
            RuntimeError: If initialization fails
        """
        logger.info("🚀 Initializing Enterprise FAISS Vector Store...")
        logger.info(f"   Model: {self.model_name}")
        logger.info(f"   Index Type: {self.index_type}")
        logger.info(f"   Storage: {self.storage_path}")
        logger.info(f"   Dimension: {self.dimension}")
        logger.info(f"   Max Memory: {self.max_memory_mb}MB")
        logger.info(f"   GPU Enabled: {self.enable_gpu}")
        try:
            self.storage_path.mkdir(parents=True, exist_ok=True)
            await self._load_model()
            await self._load_or_create_index()
            await self._load_documents()
            if self.enable_gpu and hasattr(faiss, "StandardGpuResources"):
                await self._setup_gpu()
            self._maintenance_task = asyncio.create_task(self._background_maintenance())
            logger.info("✅ Vector store initialized successfully!")
            logger.info(f"   Documents: {self.metrics['total_documents']}")
            logger.info(f"   Memory Usage: {self.metrics['memory_usage_mb']:.1f}MB")
        except Exception as e:
            logger.error(f"❌ Failed to initialize vector store: {e}")
            raise RuntimeError(f"Vector store initialization failed: {str(e)}") from e

    async def close(self) -> None:
        """Close vector store với proper cleanup."""
        logger.info("💾 Closing FAISS Vector Store...")
        try:
            await self._save_index()
            await self._save_documents()
            await self._save_metrics()
            self.thread_pool.shutdown(wait=True)
            self.vector_cache.clear()
            self.search_cache.clear()
            logger.info("✅ Vector store closed successfully")
        except Exception as e:
            logger.error(f"❌ Error closing vector store: {e}")
            raise RuntimeError(f"Failed to close vector store: {str(e)}") from e

    def is_healthy(self) -> bool:
        """Check vector store health status."""
        return (
            self.model is not None
            and self.index is not None
            and self.index.ntotal >= 0
            and not self.thread_pool._shutdown
        )

    async def vectorize_text(self, text: str) -> list[float]:
        """
        Convert text to vector với caching và optimization.
        Args:
            text: Text to vectorize
        Returns:
            Vector representation
        Raises:
            RuntimeError: If vectorization fails
        """
        if not self.model:
            raise RuntimeError("Model not initialized")
        if not text or not text.strip():
            raise ValueError("Text cannot be empty")
        text_hash = str(hash(text))
        if text_hash in self.vector_cache:
            self.metrics["cache_hits"] += 1
            return self.vector_cache[text_hash]
        try:
            loop = asyncio.get_event_loop()
            embedding = await loop.run_in_executor(
                self.thread_pool, self.model.encode, text
            )
            vector = embedding.tolist()
            if len(self.vector_cache) < self.cache_size:
                self.vector_cache[text_hash] = vector
            self.metrics["cache_misses"] += 1
            return vector
        except Exception as e:
            self.metrics["error_count"] += 1
            logger.error(f"❌ Vectorization failed: {e}")
            raise RuntimeError(f"Failed to vectorize text: {str(e)}") from e

    async def add_document(
        self, doc_id: str, content: str, metadata: dict[str, Any] | None = None
    ) -> None:
        """
        Add document với comprehensive validation và optimization.
        Args:
            doc_id: Unique document identifier
            content: Document content
            metadata: Optional document metadata
        Raises:
            ValueError: If parameters are invalid
            RuntimeError: If addition fails
        """
        if not doc_id or not doc_id.strip():
            raise ValueError("Document ID cannot be empty")
        if not content or not content.strip():
            raise ValueError("Document content cannot be empty")
        if doc_id in self.documents:
            raise ValueError(f"Document {doc_id} already exists")
        start_time = time.time()
        metadata = metadata or {}
        logger.info(f"📄 Adding document: {doc_id} ({len(content)} chars)")
        try:
            vector = await self.vectorize_text(content)
            vector_np = np.array([vector], dtype=np.float32)
            document = {
                "id": doc_id,
                "content": content,
                "metadata": {
                    **metadata,
                    "added_at": time.time(),
                    "content_length": len(content),
                    "content_hash": hash(content),
                },
                "vector": vector,
            }
            self.documents[doc_id] = document
            position = self.index.ntotal
            self.index.add(vector_np)
            self.id_to_position[doc_id] = position
            self.position_to_id[position] = doc_id
            self.metrics["total_documents"] += 1
            self.metrics["total_additions"] += 1
            add_time = (time.time() - start_time) * 1000
            self._update_average_metric("average_add_time_ms", add_time)
            logger.info(
                f"✅ Document added: {doc_id} (position: {position}, {add_time:.2f}ms)"
            )
            if self.metrics["total_additions"] % self.reindex_threshold == 0:
                self._reindex_task = asyncio.create_task(self._schedule_reindex())
        except Exception as e:
            self.metrics["error_count"] += 1
            logger.error(f"❌ Failed to add document {doc_id}: {e}")
            raise RuntimeError(f"Failed to add document: {str(e)}") from e

    async def delete_document(self, doc_id: str) -> bool:
        """
        Delete document với proper cleanup.
        Args:
            doc_id: Document ID to delete
        Returns:
            True if deleted, False if not found
        Raises:
            RuntimeError: If deletion fails
        """
        if not doc_id or doc_id not in self.documents:
            return False
        logger.info(f"🗑️ Deleting document: {doc_id}")
        try:
            del self.documents[doc_id]
            if doc_id in self.id_to_position:
                position = self.id_to_position[doc_id]
                del self.id_to_position[doc_id]
                if position in self.position_to_id:
                    del self.position_to_id[position]
            self.metrics["total_documents"] -= 1
            self.metrics["total_deletions"] += 1
            self._clear_document_cache(doc_id)
            logger.info(f"✅ Document deleted: {doc_id}")
            if self.metrics["total_deletions"] % 100 == 0:
                self._cleanup_task = asyncio.create_task(self._schedule_reindex())
            return True
        except Exception as e:
            self.metrics["error_count"] += 1
            logger.error(f"❌ Failed to delete document {doc_id}: {e}")
            raise RuntimeError(f"Failed to delete document: {str(e)}") from e

    async def search_similar(
        self,
        query_vector: list[float],
        limit: int = 10,
        threshold: float = 0.0,
        search_mode: SearchMode = "approximate",
    ) -> list[dict[str, Any]]:
        """
        Advanced similarity search với multiple strategies.
        Args:
            query_vector: Query vector for search
            limit: Maximum results to return
            threshold: Minimum similarity threshold
            search_mode: Search strategy (exact/approximate/hybrid)
        Returns:
            List of similar documents với scores và metadata
        Raises:
            ValueError: If parameters are invalid
            RuntimeError: If search fails
        """
        if not query_vector:
            raise ValueError("Query vector cannot be empty")
        if limit <= 0 or limit > 10000:
            raise ValueError("Limit must be between 1 and 10000")
        if threshold < 0.0 or threshold > 1.0:
            raise ValueError("Threshold must be between 0.0 and 1.0")
        start_time = time.time()
        cache_key = f"{hash(str(query_vector))}_{limit}_{threshold}_{search_mode}"
        if cache_key in self.search_cache:
            self.metrics["cache_hits"] += 1
            return self.search_cache[cache_key]
        logger.debug(
            f"🔍 Searching với {search_mode} mode (limit: {limit}, threshold: {threshold})"
        )
        try:
            query_np = np.array([query_vector], dtype=np.float32)
            if search_mode == "exact":
                distances, indices = await self._exact_search(query_np, limit)
            elif search_mode == "approximate":
                distances, indices = await self._approximate_search(query_np, limit)
            else:  # hybrid
                distances, indices = await self._hybrid_search(query_np, limit)
            results = []
            for i, (distance, idx) in enumerate(
                zip(distances[0], indices[0], strict=False)
            ):
                if idx == -1:  # Invalid index
                    continue
                similarity = max(0.0, 1.0 - distance)
                if similarity < threshold:
                    continue
                doc_id = self.position_to_id.get(idx)
                if not doc_id or doc_id not in self.documents:
                    continue
                document = self.documents[doc_id]
                result = {
                    "id": doc_id,
                    "content": document["content"],
                    "metadata": document["metadata"],
                    "score": similarity,
                    "distance": float(distance),
                    "rank": len(results) + 1,
                }
                results.append(result)
            search_time = (time.time() - start_time) * 1000
            self.metrics["total_searches"] += 1
            self.metrics["cache_misses"] += 1
            self._update_average_metric("average_search_time_ms", search_time)
            if len(self.search_cache) < self.cache_size:
                self.search_cache[cache_key] = results
            logger.debug(
                f"✅ Search completed: {len(results)} results in {search_time:.2f}ms"
            )
            return results
        except Exception as e:
            self.metrics["error_count"] += 1
            logger.error(f"❌ Search failed: {e}")
            raise RuntimeError(f"Search operation failed: {str(e)}") from e

    async def get_statistics(self) -> dict[str, Any]:
        """
        Get comprehensive vector store statistics.
        Returns:
            Detailed statistics dictionary
        """
        self.metrics["uptime_seconds"] = time.time() - self.start_time
        self.metrics["memory_usage_mb"] = await self._calculate_memory_usage()
        total_operations = (
            self.metrics["total_searches"]
            + self.metrics["total_additions"]
            + self.metrics["total_deletions"]
        )
        cache_hit_rate = 0.0
        if self.metrics["cache_hits"] + self.metrics["cache_misses"] > 0:
            cache_hit_rate = self.metrics["cache_hits"] / (
                self.metrics["cache_hits"] + self.metrics["cache_misses"]
            )
        enhanced_stats = {
            **self.metrics,
            "index_type": self.index_type,
            "model_name": self.model_name,
            "dimension": self.dimension,
            "total_operations": total_operations,
            "cache_hit_rate": cache_hit_rate,
            "documents_per_mb": (
                self.metrics["total_documents"]
                / max(1, self.metrics["memory_usage_mb"])
            ),
            "should_reindex": self.metrics["total_deletions"]
            > self.reindex_threshold / 2,
            "health_status": "healthy" if self.is_healthy() else "unhealthy",
            "index_efficiency": self._calculate_index_efficiency(),
            "storage_path": str(self.storage_path),
            "thread_pool_active": not self.thread_pool._shutdown,
        }
        return enhanced_stats

    async def reindex(self) -> None:
        """
        Perform full reindex for optimization.
        Raises:
            RuntimeError: If reindexing fails
        """
        logger.info("🔄 Starting vector store reindexing...")
        start_time = time.time()
        try:
            new_index = await self._create_optimized_index()
            if self.documents:
                vectors = []
                doc_ids = []
                for doc_id, doc in self.documents.items():
                    vectors.append(doc["vector"])
                    doc_ids.append(doc_id)
                if vectors:
                    vectors_np = np.array(vectors, dtype=np.float32)
                    new_index.add(vectors_np)
                    self.id_to_position.clear()
                    self.position_to_id.clear()
                    for i, doc_id in enumerate(doc_ids):
                        self.id_to_position[doc_id] = i
                        self.position_to_id[i] = doc_id
            self.index = new_index
            self.search_cache.clear()
            reindex_time = time.time() - start_time
            self.metrics["last_reindex_time"] = time.time()
            logger.info(f"✅ Reindexing completed in {reindex_time:.2f}s")
        except Exception as e:
            logger.error(f"❌ Reindexing failed: {e}")
            raise RuntimeError(f"Failed to reindex: {str(e)}") from e

    async def backup(self, backup_path: str | None = None) -> str:
        """
        Create backup of vector store.
        Args:
            backup_path: Optional custom backup path
        Returns:
            Path to created backup
        Raises:
            RuntimeError: If backup fails
        """
        if backup_path is None:
            timestamp = int(time.time())
            backup_path = str(self.storage_path / f"backup_{timestamp}")
        logger.info(f"💾 Creating backup: {backup_path}")
        try:
            backup_dir = Path(backup_path)
            backup_dir.mkdir(parents=True, exist_ok=True)
            await self._save_index(backup_dir / INDEX_FILENAME)
            await self._save_documents(backup_dir / DOCUMENTS_FILENAME)
            await self._save_metrics(backup_dir / METRICS_FILENAME)
            config = {
                "model_name": self.model_name,
                "index_type": self.index_type,
                "dimension": self.dimension,
                "backup_timestamp": time.time(),
            }
            with open(backup_dir / "config.json", "w") as f:
                json.dump(config, f, indent=2)
            self.metrics["last_backup_time"] = time.time()
            logger.info(f"✅ Backup created: {backup_path}")
            return backup_path
        except Exception as e:
            logger.error(f"❌ Backup failed: {e}")
            raise RuntimeError(f"Failed to create backup: {str(e)}") from e

    async def _load_model(self) -> None:
        """Load embedding model."""
        logger.info(f"📥 Loading model: {self.model_name}")
        try:
            loop = asyncio.get_event_loop()
            self.model = await loop.run_in_executor(
                self.thread_pool, SentenceTransformer, self.model_name
            )
            test_vector = await self.vectorize_text("test")
            actual_dimension = len(test_vector)
            if actual_dimension != self.dimension:
                logger.warning(
                    f"⚠️ Dimension mismatch: expected {self.dimension}, got {actual_dimension}"
                )
                self.dimension = actual_dimension
            logger.info(f"✅ Model loaded successfully (dimension: {self.dimension})")
        except Exception as e:
            raise RuntimeError(f"Failed to load model: {str(e)}") from e

    async def _load_or_create_index(self) -> None:
        """Load existing index or create new one."""
        index_path = self.storage_path / INDEX_FILENAME
        if index_path.exists():
            logger.info("📥 Loading existing FAISS index...")
            try:
                self.index = faiss.read_index(str(index_path))
                logger.info(f"✅ Index loaded: {self.index.ntotal} vectors")
                return
            except Exception as e:
                logger.warning(f"⚠️ Failed to load index: {e}")
        logger.info("🆕 Creating new FAISS index...")
        self.index = await self._create_optimized_index()
        logger.info("✅ New index created")

    async def _create_optimized_index(self) -> faiss.Index:
        """Create optimized FAISS index based on type."""
        if self.index_type == "Flat":
            return faiss.IndexFlatIP(self.dimension)
        elif self.index_type == "IVF":
            quantizer = faiss.IndexFlatIP(self.dimension)
            return faiss.IndexIVFFlat(quantizer, self.dimension, 100)
        elif self.index_type == "HNSW":
            return faiss.IndexHNSWFlat(self.dimension, 32)
        elif self.index_type == "PQ":
            return faiss.IndexPQ(self.dimension, 8, 8)
        else:
            raise ValueError(f"Unsupported index type: {self.index_type}")

    async def _load_documents(self) -> None:
        """Load existing documents."""
        docs_path = self.storage_path / DOCUMENTS_FILENAME
        if docs_path.exists():
            logger.info("📥 Loading documents...")
            try:
                with open(docs_path, "rb") as f:
                    data = pickle.load(f)
                self.documents = data.get("documents", {})
                self.id_to_position = data.get("id_to_position", {})
                self.position_to_id = data.get("position_to_id", {})
                self.metrics["total_documents"] = len(self.documents)
                logger.info(f"✅ Loaded {len(self.documents)} documents")
            except Exception as e:
                logger.error(f"❌ Failed to load documents: {e}")

    async def _save_index(self, path: Path | None = None) -> None:
        """Save FAISS index."""
        if path is None:
            path = self.storage_path / INDEX_FILENAME
        if self.index:
            faiss.write_index(self.index, str(path))

    async def _save_documents(self, path: Path | None = None) -> None:
        """Save documents và mappings."""
        if path is None:
            path = self.storage_path / DOCUMENTS_FILENAME
        data = {
            "documents": self.documents,
            "id_to_position": self.id_to_position,
            "position_to_id": self.position_to_id,
        }
        with open(path, "wb") as f:
            pickle.dump(data, f)

    async def _save_metrics(self, path: Path | None = None) -> None:
        """Save performance metrics."""
        if path is None:
            path = self.storage_path / METRICS_FILENAME
        with open(path, "w") as f:
            json.dump(self.metrics, f, indent=2, default=str)

    async def _exact_search(
        self, query_np: np.ndarray, limit: int
    ) -> tuple[np.ndarray, np.ndarray]:
        """Perform exact search."""
        return self.index.search(query_np, limit)

    async def _approximate_search(
        self, query_np: np.ndarray, limit: int
    ) -> tuple[np.ndarray, np.ndarray]:
        """Perform approximate search với optimization."""
        if hasattr(self.index, "nprobe"):
            old_nprobe = self.index.nprobe
            self.index.nprobe = min(10, self.index.nlist)
            result = self.index.search(query_np, limit)
            self.index.nprobe = old_nprobe
            return result
        else:
            return self.index.search(query_np, limit)

    async def _hybrid_search(
        self, query_np: np.ndarray, limit: int
    ) -> tuple[np.ndarray, np.ndarray]:
        """Perform hybrid search combining strategies."""
        return await self._approximate_search(query_np, limit)

    async def _setup_gpu(self) -> None:
        """Setup GPU acceleration if available."""
        try:
            gpu_res = faiss.StandardGpuResources()
            self.index = faiss.index_cpu_to_gpu(gpu_res, 0, self.index)
            logger.info("✅ GPU acceleration enabled")
        except Exception as e:
            logger.warning(f"⚠️ GPU setup failed: {e}")

    async def _background_maintenance(self) -> None:
        """Background maintenance tasks."""
        while True:
            try:
                await asyncio.sleep(3600)  # Run every hour
                self.metrics["memory_usage_mb"] = await self._calculate_memory_usage()
                if (
                    self.metrics["last_backup_time"] is None
                    or time.time() - self.metrics["last_backup_time"]
                    > self.backup_interval_hours * 3600
                ):
                    await self.backup()
            except Exception as e:
                logger.error(f"❌ Background maintenance error: {e}")

    async def _calculate_memory_usage(self) -> float:
        """Calculate approximate memory usage in MB."""
        total_size = 0
        total_size += len(pickle.dumps(self.documents))
        if self.index:
            total_size += self.index.ntotal * self.dimension * 4  # 4 bytes per float
        total_size += len(pickle.dumps(self.vector_cache))
        total_size += len(pickle.dumps(self.search_cache))
        return total_size / (1024 * 1024)

    def _calculate_index_efficiency(self) -> float:
        """Calculate index efficiency score."""
        if self.metrics["total_documents"] == 0:
            return 1.0
        base_efficiency = 1.0
        if self.metrics["average_search_time_ms"] > 100:
            base_efficiency *= 0.8
        elif self.metrics["average_search_time_ms"] > 50:
            base_efficiency *= 0.9
        return base_efficiency

    def _update_average_metric(self, metric_name: str, new_value: float) -> None:
        """Update average metric với exponential moving average."""
        current_avg = self.metrics.get(metric_name, 0.0)
        if current_avg == 0:
            self.metrics[metric_name] = new_value
        else:
            alpha = 0.1
            self.metrics[metric_name] = (alpha * new_value) + (
                (1 - alpha) * current_avg
            )

    def _clear_document_cache(self, doc_id: str) -> None:
        """Clear cache entries related to document."""
        keys_to_remove = []
        for key in self.search_cache.keys():
            keys_to_remove.append(key)
        for key in keys_to_remove:
            del self.search_cache[key]

    async def _schedule_reindex(self) -> None:
        """Schedule reindex operation."""
        logger.info("📅 Scheduling reindex operation...")
        await asyncio.sleep(1)  # Small delay
        await self.reindex()


__all__ = [
    "DOCUMENTS_FILENAME",
    "FAISSVectorStore",
    "INDEX_FILENAME",
    "IndexType",
    "METRICS_FILENAME",
    "SearchMode",
    "actual_dimension",
    "add_time",
    "alpha",
    "backup_dir",
    "backup_path",
    "base_efficiency",
    "cache_hit_rate",
    "cache_key",
    "config",
    "current_avg",
    "data",
    "doc_id",
    "doc_ids",
    "docs_path",
    "document",
    "embedding",
    "enhanced_stats",
    "gpu_res",
    "index_path",
    "is_healthy",
    "keys_to_remove",
    "loop",
    "metadata",
    "new_index",
    "old_nprobe",
    "path",
    "position",
    "quantizer",
    "query_np",
    "reindex_time",
    "result",
    "results",
    "search_time",
    "similarity",
    "start_time",
    "test_vector",
    "text_hash",
    "timestamp",
    "total_operations",
    "total_size",
    "vector",
    "vector_np",
    "vectors",
    "vectors_np",
]
