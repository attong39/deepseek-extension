from __future__ import annotations

import logging
import random
from typing import Any

from apps.backend.core.interfaces.memory_backend import BaseMemoryBackend, MemoryResult
from psycopg_pool import ConnectionPool
import Exception
import RuntimeError
import batch_size
import bool
import conn
import conn_timeout
import cur
import dict
import dsn
import e
import embedding_dim
import embedding_model
import filters
import float
import hasattr
import ids
import int
import key
import len
import list
import map
import max_conn
import min_conn
import namespace
import range
import record
import record_id
import records
import row
import self
import str
import super
import target_model
import top_k
import value

"""Connection Pool Management với psycopg_pool cho PGVector.
Module này cung cấp:
- PGVectorPoolBackend với connection pooling
- Optimized queries với prepared statements
- Connection health monitoring
"""
logger = logging.getLogger(__name__)


class PGVectorPoolBackend(BaseMemoryBackend):
    """PGVector backend với connection pooling và optimization."""

    def __init__(
        self,
        dsn: str,
        min_conn: int = 2,
        max_conn: int = 20,
        conn_timeout: float = 10.0,
        embedding_dim: int = 1536,
    ):
        """Initialize PGVector pool backend.
        Args:
            dsn: PostgreSQL connection string
            min_conn: Minimum pool connections
            max_conn: Maximum pool connections
            conn_timeout: Connection timeout in seconds
            embedding_dim: Vector embedding dimension
        """
        super().__init__()
        self.dsn = dsn
        self.embedding_dim = embedding_dim
        self.pool = ConnectionPool(
            dsn,
            min_size=min_conn,
            max_size=max_conn,
            timeout=conn_timeout,
            prepare_threshold=1,
            check=ConnectionPool.check_connection,
        )
        self._test_connection()
        logger.info(f"Initialized PGVector pool with {min_conn}-{max_conn} connections")

    def _test_connection(self) -> None:
        """Test database connection và setup."""
        with self.pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM pg_extension WHERE extname = 'vector'")
                if not cur.fetchone():
                    raise RuntimeError("pgvector extension not installed")
                cur.execute(f"""
                    CREATE TABLE IF NOT EXISTS embeddings (
                        id TEXT PRIMARY KEY,
                        namespace TEXT NOT NULL,
                        content TEXT,
                        metadata JSONB,
                        embedding VECTOR({self.embedding_dim}),
                        created_at TIMESTAMP DEFAULT NOW()
                    )
                """)
                cur.execute("""
                    CREATE INDEX IF NOT EXISTS idx_embeddings_namespace
                    ON embeddings(namespace)
                """)
                cur.execute("""
                    CREATE INDEX IF NOT EXISTS idx_embeddings_vector
                    ON embeddings USING ivfflat (embedding vector_cosine_ops)
                    WITH (lists = 100)
                """)
            conn.commit()

    def upsert(
        self,
        namespace: str,
        records: list[dict[str, Any]],
        embedding_model: str | None = None,
    ) -> MemoryResult:
        """Upsert records với connection pooling.
        Args:
            namespace: Target namespace
            records: Records to upsert
            embedding_model: Optional embedding model
        Returns:
            Upsert result
        """
        self._validate_namespace(namespace)
        self._validate_records(records)
        with self.pool.connection() as conn:
            with conn.cursor() as cur:
                upsert_sql = """
                    INSERT INTO embeddings (id, namespace, content, metadata, embedding)
                    VALUES (%s, %s, %s, %s, %s::vector)
                    ON CONFLICT (id) DO UPDATE SET
                        content = EXCLUDED.content,
                        metadata = EXCLUDED.metadata,
                        embedding = EXCLUDED.embedding
                """
                processed = 0
                for record in records:
                    try:
                        embedding = self._encode_content(record)
                        if embedding is None:
                            continue
                        cur.execute(
                            upsert_sql,
                            (
                                record["id"],
                                namespace,
                                record.get("content") or record.get("text", ""),
                                record.get("metadata", {}),
                                embedding,
                            ),
                        )
                        processed += 1
                    except Exception as e:
                        logger.error(f"Error processing record {record.get('id')}: {e}")
                        continue
            conn.commit()
        return self._create_result(
            status="success",
            namespace=namespace,
            operation="upsert",
            count=processed,
            metadata={"embedding_model": embedding_model},
        )

    def query(
        self,
        namespace: str,
        query: str,
        top_k: int = 10,
        filters: dict[str, Any] | None = None,
    ) -> MemoryResult:
        """Query với optimized vector search.
        Args:
            namespace: Target namespace
            query: Search query
            top_k: Number of results
            filters: Optional filters
        Returns:
            Query results
        """
        self._validate_namespace(namespace)
        query_embedding = self._encode_query(query)
        if query_embedding is None:
            return self._create_result(
                status="error",
                namespace=namespace,
                operation="query",
                error="Failed to encode query",
            )
        with self.pool.connection() as conn:
            with conn.cursor() as cur:
                where_clauses = ["namespace = %s"]
                params = [namespace]
                if filters:
                    for key, value in filters.items():
                        where_clauses.append("metadata->>%s = %s")
                        params.extend([key, str(value)])
                where_sql = " AND ".join(where_clauses)
                sql = f"""
                    SELECT id, content, metadata,
                           1 - (embedding <=> %s::vector) as similarity
                    FROM embeddings
                    WHERE {where_sql}
                    ORDER BY embedding <=> %s::vector
                    LIMIT %s
                """
                params.extend([query_embedding, query_embedding, top_k])
                cur.execute(sql, params)
                results = []
                for row in cur.fetchall():
                    results.append(
                        {
                            "id": row[0],
                            "content": row[1],
                            "metadata": row[2],
                            "score": float(row[3]),
                        }
                    )
        return self._create_result(
            status="success",
            namespace=namespace,
            operation="query",
            count=len(results),
            data={"results": results},
        )

    def delete(
        self,
        namespace: str,
        ids: list[str] | None = None,
        filters: dict[str, Any] | None = None,
        hard: bool = False,
    ) -> MemoryResult:
        """Delete records với optimized queries.
        Args:
            namespace: Target namespace
            ids: Record IDs to delete
            filters: Optional filters
            hard: Hard delete flag
        Returns:
            Delete result
        """
        self._validate_namespace(namespace)
        with self.pool.connection() as conn:
            with conn.cursor() as cur:
                if ids:
                    placeholders = ",".join(["%s"] * len(ids))
                    sql = f"DELETE FROM embeddings WHERE namespace = %s AND id IN ({placeholders})"
                    params = [namespace] + ids
                elif filters:
                    where_clauses = ["namespace = %s"]
                    params = [namespace]
                    for key, value in filters.items():
                        where_clauses.append("metadata->>%s = %s")
                        params.extend([key, str(value)])
                    where_sql = " AND ".join(where_clauses)
                    sql = f"DELETE FROM embeddings WHERE {where_sql}"
                else:
                    sql = "DELETE FROM embeddings WHERE namespace = %s"
                    params = [namespace]
                cur.execute(sql, params)
                deleted_count = cur.rowcount
            conn.commit()
        return self._create_result(
            status="success",
            namespace=namespace,
            operation="delete",
            count=deleted_count,
        )

    def rebuild_embeddings(
        self, namespace: str, target_model: str, batch_size: int = 256
    ) -> MemoryResult:
        """Rebuild embeddings với batch processing.
        Args:
            namespace: Target namespace
            target_model: Target embedding model
            batch_size: Batch size for processing
        Returns:
            Rebuild result
        """
        self._validate_namespace(namespace)
        with self.pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT COUNT(*) FROM embeddings WHERE namespace = %s", [namespace]
                )
                total_count = cur.fetchone()[0]
                if total_count == 0:
                    return self._create_result(
                        status="success",
                        namespace=namespace,
                        operation="rebuild",
                        count=0,
                        metadata={"message": "No records to rebuild"},
                    )
                processed = 0
                offset = 0
                while offset < total_count:
                    cur.execute(
                        """
                        SELECT id, content FROM embeddings
                        WHERE namespace = %s
                        ORDER BY id
                        LIMIT %s OFFSET %s
                    """,
                        [namespace, batch_size, offset],
                    )
                    batch_records = cur.fetchall()
                    update_sql = """
                        UPDATE embeddings
                        SET embedding = %s::vector
                        WHERE id = %s
                    """
                    for record_id, content in batch_records:
                        if content:
                            embedding = self._encode_content({"content": content})
                            if embedding:
                                cur.execute(update_sql, [embedding, record_id])
                                processed += 1
                    offset += batch_size
            conn.commit()
        return self._create_result(
            status="success",
            namespace=namespace,
            operation="rebuild",
            count=processed,
            metadata={"target_model": target_model, "batch_size": batch_size},
        )

    def _encode_content(self, record: dict[str, Any]) -> str | None:
        """Encode content to vector (placeholder - implement actual embedding).
        Args:
            record: Record with content
        Returns:
            Vector string representation
        """
        content = record.get("content") or record.get("text", "")
        if not content:
            return None
        vector = [random.random() for _ in range(self.embedding_dim)]
        return f"[{','.join(map(str, vector))}]"

    def _encode_query(self, query: str) -> str | None:
        """Encode query to vector.
        Args:
            query: Search query
        Returns:
            Vector string representation
        """
        if not query:
            return None
        vector = [random.random() for _ in range(self.embedding_dim)]
        return f"[{','.join(map(str, vector))}]"

    def get_pool_stats(self) -> dict[str, Any]:
        """Get connection pool statistics.
        Returns:
            Pool statistics
        """
        return {
            "min_size": self.pool.min_size,
            "max_size": self.pool.max_size,
            "current_size": len(self.pool._pool) if hasattr(self.pool, "_pool") else 0,
            "available": self.pool.get_stats().get("available", 0),
            "used": self.pool.get_stats().get("used", 0),
        }

    def __del__(self):
        """Cleanup pool on deletion."""
        if hasattr(self, "pool"):
            self.pool.close()


__all__ = [
    "PGVectorPoolBackend",
    "batch_records",
    "content",
    "delete",
    "deleted_count",
    "embedding",
    "get_pool_stats",
    "logger",
    "offset",
    "params",
    "placeholders",
    "processed",
    "query",
    "query_embedding",
    "rebuild_embeddings",
    "results",
    "sql",
    "total_count",
    "update_sql",
    "upsert",
    "upsert_sql",
    "vector",
    "where_clauses",
    "where_sql",
]
