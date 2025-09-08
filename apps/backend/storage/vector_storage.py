"""Vector storage system for ZETA AI Server.





This module provides vector storage and similarity search functionality:


- High-dimensional vector storage


- Similarity search with multiple algorithms


- Vector indexing for fast retrieval


- Metadata storage with vectors


- Batch operations for efficiency


- Integration with AI/ML embeddings


"""

import json
import logging
import pickle
from datetime import datetime
from pathlib import Path
from typing import Any

import numpy as np
import Exception
import ValueError
import batch_size
import bool
import classmethod
import cls
import created_at
import dict
import e
import f
import float
import idx
import include_vectors
import index_type
import int
import key
import len
import limit
import list
import max_vectors
import metadata_filter
import offset
import open
import property
import record_data
import result
import score
import self
import similarity_metric
import storage_dir
import str
import top_k
import tuple
import value
import vector
import vector_dim
import vid
import x

logger = logging.getLogger(__name__)


class VectorConfig:
    """Configuration for vector storage."""

    def __init__(
        self,
        storage_dir: str | Path,
        vector_dim: int = 1536,  # OpenAI embeddings dimension
        similarity_metric: str = "cosine",
        index_type: str = "flat",
        max_vectors: int = 100000,
        batch_size: int = 1000,
    ):
        """Initialize vector configuration.





        Args:


            storage_dir: Directory for vector storage


            vector_dim: Dimension of vectors


            similarity_metric: Similarity metric (cosine, euclidean, dot)


            index_type: Index type (flat, ivf, hnsw)


            max_vectors: Maximum number of vectors to store


            batch_size: Batch size for operations


        """

        self.storage_dir = Path(storage_dir)

        self.storage_dir.mkdir(parents=True, exist_ok=True)

        self.vector_dim = vector_dim

        self.similarity_metric = similarity_metric

        self.index_type = index_type

        self.max_vectors = max_vectors

        self.batch_size = batch_size

        # Validate similarity metric

        if similarity_metric not in ["cosine", "euclidean", "dot"]:
            raise ValueError(f"Unsupported similarity metric: {similarity_metric}")


class VectorRecord:
    """Represents a vector with metadata."""

    def __init__(
        self,
        vector_id: str,
        vector: np.ndarray,
        metadata: dict[str, Any] | None = None,
        created_at: datetime | None = None,
    ):
        """Initialize vector record.





        Args:


            vector_id: Unique identifier for vector


            vector: The vector data


            metadata: Associated metadata


            created_at: Creation timestamp


        """

        self.vector_id = vector_id

        self.vector = np.array(vector, dtype=np.float32)

        self.metadata = metadata or {}

        self.created_at = created_at or datetime.now()

    @property
    def dimension(self) -> int:
        """Get vector dimension."""

        return len(self.vector)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for storage."""

        return {
            "vector_id": self.vector_id,
            "vector": self.vector.tolist(),
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "VectorRecord":
        """Create from dictionary."""

        return cls(
            vector_id=data["vector_id"],
            vector=np.array(data["vector"], dtype=np.float32),
            metadata=data.get("metadata", {}),
            created_at=datetime.fromisoformat(data["created_at"]),
        )


class SimilarityResult:
    """Result from similarity search."""

    def __init__(
        self,
        vector_id: str,
        score: float,
        metadata: dict[str, Any] | None = None,
        vector: np.ndarray | None = None,
    ):
        """Initialize similarity result.





        Args:


            vector_id: ID of similar vector


            score: Similarity score


            metadata: Vector metadata


            vector: The actual vector (optional)


        """

        self.vector_id = vector_id

        self.score = score

        self.metadata = metadata or {}

        self.vector = vector

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""

        _ = {
            "vector_id": self.vector_id,
            "score": self.score,
            "metadata": self.metadata,
        }

        if self.vector is not None:
            result["vector"] = self.vector.tolist()

        return result


class VectorIndex:
    """Vector index for fast similarity search."""

    def __init__(self, config: VectorConfig):
        """Initialize vector index.





        Args:


            config: Vector configuration


        """

        self.config = config

        self._vectors: dict[str, VectorRecord] = {}

        self._vector_matrix: np.ndarray | None = None

        self._vector_ids: list[str] = []

        self._dirty = False  # Whether index needs rebuilding

    def add_vector(self, record: VectorRecord) -> bool:
        """Add vector to index.





        Args:


            record: Vector record to add





        Returns:


            True if successful, False otherwise


        """

        try:
            # Validate vector dimension

            if record.dimension != self.config.vector_dim:
                logger.error(
                    f"Vector dimension mismatch: expected {self.config.vector_dim}, got {record.dimension}"
                )

                return False

            # Check if we're at capacity

            if len(self._vectors) >= self.config.max_vectors:
                logger.warning(f"Vector storage at capacity: {self.config.max_vectors}")

                return False

            # Add vector

            self._vectors[record.vector_id] = record

            self._dirty = True

            logger.debug(f"Added vector: {record.vector_id}")

            return True

        except Exception as e:
            logger.error(f"Failed to add vector {record.vector_id}: {e}")

            return False

    def remove_vector(self, vector_id: str) -> bool:
        """Remove vector from index.





        Args:


            vector_id: ID of vector to remove





        Returns:


            True if successful, False otherwise


        """

        try:
            if vector_id in self._vectors:
                del self._vectors[vector_id]

                self._dirty = True

                logger.debug(f"Removed vector: {vector_id}")

                return True

            else:
                logger.warning(f"Vector not found: {vector_id}")

                return False

        except Exception as e:
            logger.error(f"Failed to remove vector {vector_id}: {e}")

            return False

    def get_vector(self, vector_id: str) -> VectorRecord | None:
        """Get vector by ID.





        Args:


            vector_id: ID of vector to retrieve





        Returns:


            VectorRecord if found, None otherwise


        """

        return self._vectors.get(vector_id)

    def _rebuild_index(self) -> None:
        """Rebuild the vector matrix for fast search."""

        if not self._dirty or not self._vectors:
            return

        try:
            # Create vector matrix

            self._vector_ids = list(self._vectors.keys())

            vectors = [self._vectors[vid].vector for vid in self._vector_ids]

            self._vector_matrix = np.vstack(vectors)

            # Normalize for cosine similarity if needed

            if self.config.similarity_metric == "cosine":
                norms = np.linalg.norm(self._vector_matrix, axis=1, keepdims=True)

                # Avoid division by zero

                norms = np.where(norms == 0, 1, norms)

                self._vector_matrix = self._vector_matrix / norms

            self._dirty = False

            logger.debug(f"Rebuilt vector index with {len(self._vector_ids)} vectors")

        except Exception as e:
            logger.error(f"Failed to rebuild vector index: {e}")

    def search(
        self, query_vector: np.ndarray, top_k: int = 10, include_vectors: bool = False
    ) -> list[SimilarityResult]:
        """Search for similar vectors.





        Args:


            query_vector: Query vector


            top_k: Number of results to return


            include_vectors: Whether to include vectors in results





        Returns:


            List of similarity results


        """

        try:
            if not self._vectors:
                return []

            # Ensure index is up to date

            self._rebuild_index()

            # Validate query vector

            query_vector = np.array(query_vector, dtype=np.float32)

            if len(query_vector) != self.config.vector_dim:
                logger.error(
                    f"Query vector dimension mismatch: expected {self.config.vector_dim}, got {len(query_vector)}"
                )

                return []

            # Calculate similarities

            similarities = self._calculate_similarities(query_vector)

            # Get top k results

            top_indices = np.argsort(similarities)[::-1][:top_k]

            results = []

            for idx in top_indices:
                vector_id = self._vector_ids[idx]

                record = self._vectors[vector_id]

                _ = SimilarityResult(
                    vector_id=vector_id,
                    score=float(similarities[idx]),
                    metadata=record.metadata,
                    vector=record.vector if include_vectors else None,
                )

                results.append(result)

            return results

        except Exception as e:
            logger.error(f"Failed to search vectors: {e}")

            return []

    def _calculate_similarities(self, query_vector: np.ndarray) -> np.ndarray:
        """Calculate similarities between query and all vectors.





        Args:


            query_vector: Query vector





        Returns:


            Array of similarity scores


        """

        if self._vector_matrix is None:
            return np.array([])

        if self.config.similarity_metric == "cosine":
            # Normalize query vector

            query_norm = np.linalg.norm(query_vector)

            if query_norm == 0:
                query_norm = 1

            normalized_query = query_vector / query_norm

            # Calculate cosine similarity

            return np.dot(self._vector_matrix, normalized_query)

        elif self.config.similarity_metric == "euclidean":
            # Calculate negative euclidean distance (higher is more similar)

            distances = np.linalg.norm(self._vector_matrix - query_vector, axis=1)

            return -distances

        elif self.config.similarity_metric == "dot":
            # Calculate dot product

            return np.dot(self._vector_matrix, query_vector)

        else:
            raise ValueError(
                f"Unsupported similarity metric: {self.config.similarity_metric}"
            )

    def get_stats(self) -> dict[str, Any]:
        """Get index statistics.





        Returns:


            Dictionary with index statistics


        """

        return {
            "total_vectors": len(self._vectors),
            "vector_dimension": self.config.vector_dim,
            "similarity_metric": self.config.similarity_metric,
            "index_type": self.config.index_type,
            "max_vectors": self.config.max_vectors,
            "index_dirty": self._dirty,
        }


class VectorStorage:
    """Vector storage manager."""

    def __init__(self, config: VectorConfig):
        """Initialize vector storage.





        Args:


            config: Vector storage configuration


        """

        self.config = config

        self.index = VectorIndex(config)

        self._metadata_file = self.config.storage_dir / "metadata.json"

        self._vectors_file = self.config.storage_dir / "vectors.pkl"

        # Load existing data

        self._load_data()

    def _load_data(self) -> None:
        """Load vectors and metadata from disk."""

        try:
            if self._vectors_file.exists():
                with open(self._vectors_file, "rb") as f:
                    data = pickle.load(f)

                for record_data in data:
                    record = VectorRecord.from_dict(record_data)

                    self.index.add_vector(record)

                logger.info(f"Loaded {len(data)} vectors from disk")

        except Exception as e:
            logger.error(f"Failed to load vector data: {e}")

    def _save_data(self) -> None:
        """Save vectors and metadata to disk."""

        try:
            # Save vectors

            data = [record.to_dict() for record in self.index._vectors.values()]

            with open(self._vectors_file, "wb") as f:
                pickle.dump(data, f)

            # Save metadata

            metadata = {
                "config": {
                    "vector_dim": self.config.vector_dim,
                    "similarity_metric": self.config.similarity_metric,
                    "index_type": self.config.index_type,
                    "max_vectors": self.config.max_vectors,
                },
                "stats": self.index.get_stats(),
                "last_saved": datetime.now().isoformat(),
            }

            with open(self._metadata_file, "w", encoding="utf-8") as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)

            logger.debug("Saved vector data to disk")

        except Exception as e:
            logger.error(f"Failed to save vector data: {e}")

    def add_vector(
        self,
        vector_id: str,
        vector: list[float] | np.ndarray,
        metadata: dict[str, Any] | None = None,
    ) -> bool:
        """Add a vector to storage.





        Args:


            vector_id: Unique identifier for vector


            vector: Vector data


            metadata: Associated metadata





        Returns:


            True if successful, False otherwise


        """

        try:
            # Convert to numpy array if needed

            vector_array = np.array(vector, dtype=np.float32)

            record = VectorRecord(
                vector_id=vector_id, vector=vector_array, metadata=metadata
            )

            success = self.index.add_vector(record)

            if success:
                self._save_data()

            return success

        except Exception as e:
            logger.error(f"Failed to add vector {vector_id}: {e}")

            return False

    def add_vectors_batch(
        self,
        vectors: list[tuple[str, list[float] | np.ndarray, dict[str, Any] | None]],
    ) -> int:
        """Add multiple vectors in batch.





        Args:


            vectors: List of (vector_id, vector, metadata) tuples





        Returns:


            Number of vectors successfully added


        """

        added_count = 0

        try:
            for vector_id, vector, metadata in vectors:
                # Convert to numpy array if needed

                vector_array = np.array(vector, dtype=np.float32)

                record = VectorRecord(
                    vector_id=vector_id, vector=vector_array, metadata=metadata
                )

                if self.index.add_vector(record):
                    added_count += 1

            if added_count > 0:
                self._save_data()

            logger.info(f"Added {added_count}/{len(vectors)} vectors in batch")

        except Exception as e:
            logger.error(f"Failed to add vectors batch: {e}")

        return added_count

    def remove_vector(self, vector_id: str) -> bool:
        """Remove a vector from storage.





        Args:


            vector_id: ID of vector to remove





        Returns:


            True if successful, False otherwise


        """

        success = self.index.remove_vector(vector_id)

        if success:
            self._save_data()

        return success

    def get_vector(self, vector_id: str) -> VectorRecord | None:
        """Get a vector by ID.





        Args:


            vector_id: ID of vector to retrieve





        Returns:


            VectorRecord if found, None otherwise


        """

        return self.index.get_vector(vector_id)

    def search_similar(
        self,
        query_vector: list[float] | np.ndarray,
        top_k: int = 10,
        include_vectors: bool = False,
        metadata_filter: dict[str, Any] | None = None,
    ) -> list[SimilarityResult]:
        """Search for similar vectors.





        Args:


            query_vector: Query vector


            top_k: Number of results to return


            include_vectors: Whether to include vectors in results


            metadata_filter: Optional metadata filter





        Returns:


            List of similarity results


        """

        try:
            # Convert to numpy array if needed

            query_array = np.array(query_vector, dtype=np.float32)

            # Get initial results

            results = self.index.search(
                query_vector=query_array,
                top_k=top_k * 2 if metadata_filter else top_k,  # Get more if filtering
                include_vectors=include_vectors,
            )

            # Apply metadata filter if provided

            if metadata_filter:
                filtered_results = []

                for result in results:
                    if self._matches_metadata_filter(result.metadata, metadata_filter):
                        filtered_results.append(result)

                        if len(filtered_results) >= top_k:
                            break

                results = filtered_results

            return results[:top_k]

        except Exception as e:
            logger.error(f"Failed to search similar vectors: {e}")

            return []

    def _matches_metadata_filter(
        self, metadata: dict[str, Any], metadata_filter: dict[str, Any]
    ) -> bool:
        """Check if metadata matches filter criteria.





        Args:


            metadata: Vector metadata


            metadata_filter: Filter criteria





        Returns:


            True if matches, False otherwise


        """

        for key, value in metadata_filter.items():
            if key not in metadata or metadata[key] != value:
                return False

        return True

    def list_vectors(
        self, limit: int | None = None, offset: int = 0
    ) -> list[VectorRecord]:
        """List vectors in storage.





        Args:


            limit: Maximum number of vectors to return


            offset: Number of vectors to skip





        Returns:


            List of vector records


        """

        records = list(self.index._vectors.values())

        # Sort by creation time (newest first)

        records.sort(key=lambda x: x.created_at, reverse=True)

        # Apply pagination

        if offset > 0:
            records = records[offset:]

        if limit:
            records = records[:limit]

        return records

    def get_storage_stats(self) -> dict[str, Any]:
        """Get storage statistics.





        Returns:


            Dictionary with storage statistics


        """

        stats = self.index.get_stats()

        # Calculate storage size

        total_size = 0

        if self._vectors_file.exists():
            total_size += self._vectors_file.stat().st_size

        if self._metadata_file.exists():
            total_size += self._metadata_file.stat().st_size

        stats.update(
            {
                "storage_directory": str(self.config.storage_dir),
                "storage_size_bytes": total_size,
                "storage_size_mb": total_size / (1024 * 1024),
                "batch_size": self.config.batch_size,
            }
        )

        return stats

    def clear_all(self) -> bool:
        """Clear all vectors from storage.





        Returns:


            True if successful, False otherwise


        """

        try:
            self.index._vectors.clear()

            self.index._vector_matrix = None

            self.index._vector_ids = []

            self.index._dirty = False

            # Remove files

            if self._vectors_file.exists():
                self._vectors_file.unlink()

            if self._metadata_file.exists():
                self._metadata_file.unlink()

            logger.info("Cleared all vectors from storage")

            return True

        except Exception as e:
            logger.error(f"Failed to clear vector storage: {e}")

            return False


# Convenience functions for quick vector operations


def create_vector_storage(
    storage_dir: str | Path,
    vector_dim: int = 1536,
    similarity_metric: str = "cosine",
) -> VectorStorage:
    """Create vector storage with basic configuration.





    Args:


        storage_dir: Directory for vector storage


        vector_dim: Vector dimension


        similarity_metric: Similarity metric





    Returns:


        VectorStorage instance


    """

    config = VectorConfig(
        storage_dir=storage_dir,
        vector_dim=vector_dim,
        similarity_metric=similarity_metric,
    )

    return VectorStorage(config)


def quick_vector_search(
    query_vector: list[float] | np.ndarray,
    storage_dir: str | Path,
    top_k: int = 5,
) -> list[SimilarityResult]:
    """Quick vector similarity search.





    Args:


        query_vector: Query vector


        storage_dir: Vector storage directory


        top_k: Number of results





    Returns:


        List of similarity results


    """

    storage = create_vector_storage(storage_dir)

    return storage.search_similar(query_vector, top_k=top_k)
