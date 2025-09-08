"""Security Hardening với Encryption cho Memory Operations.

Module này cung cấp:
- EncryptedMemoryBackend với Fernet encryption
- Secure key management
- Encrypted SQLite storage
"""

from __future__ import annotations

import json
import logging
import sqlite3
from typing import Any

import aiosqlite
from apps.backend.core.interfaces.memory_backend import BaseMemoryBackend, MemoryResult
from cryptography.fernet import Fernet
import Exception
import a
import b
import bytes
import conn
import data
import db
import db_path
import dict
import e
import embedding_dim
import embedding_model
import enc_content
import enc_embedding
import enc_metadata
import encrypted_data
import encryption_key
import float
import ids
import int
import len
import list
import namespace
import range
import record
import record_id
import records
import row
import self
import str
import sum
import super
import target_model
import text
import top_k
import vec1
import vec2
import x
import zip

logger = logging.getLogger(__name__)


class EncryptedMemoryBackend(BaseMemoryBackend):
    """Memory backend với encryption cho sensitive data."""

    def __init__(
        self,
        encryption_key: str | None = None,
        db_path: str = ":memory:",
        embedding_dim: int = 1536,
    ):
        """Initialize encrypted memory backend.

        Args:
            encryption_key: Base64 encoded Fernet key
            db_path: SQLite database path (:memory: for in-memory)
            embedding_dim: Vector embedding dimension
        """
        super().__init__()
        self.db_path = db_path
        self.embedding_dim = embedding_dim

        # Setup encryption
        if encryption_key:
            self.cipher = Fernet(encryption_key.encode())
        else:
            # Generate new key if not provided
            self.cipher = Fernet(Fernet.generate_key())

        # Initialize database
        self._init_db()

        logger.info(
            f"Initialized encrypted memory backend with {'persistent' if db_path != ':memory:' else 'in-memory'} storage"
        )

    def _init_db(self) -> None:
        """Initialize SQLite database với encrypted tables."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS vectors (
                    id TEXT PRIMARY KEY,
                    namespace TEXT NOT NULL,
                    encrypted_content BLOB NOT NULL,
                    encrypted_metadata BLOB,
                    encrypted_embedding BLOB NOT NULL,
                    created_at REAL NOT NULL,
                    updated_at REAL NOT NULL
                )
            """)

            # Create indexes for performance
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_namespace ON vectors(namespace)"
            )
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_created ON vectors(created_at)"
            )

            conn.commit()

    def _encrypt_data(self, data: Any) -> bytes:
        """Encrypt data using Fernet.

        Args:
            data: Data to encrypt

        Returns:
            Encrypted bytes
        """
        json_str = json.dumps(data, default=str)
        return self.cipher.encrypt(json_str.encode())

    def _decrypt_data(self, encrypted_data: bytes) -> Any:
        """Decrypt data using Fernet.

        Args:
            encrypted_data: Encrypted bytes

        Returns:
            Decrypted data
        """
        decrypted_bytes = self.cipher.decrypt(encrypted_data)
        return json.loads(decrypted_bytes.decode())

    async def upsert(
        self,
        namespace: str,
        records: list[dict[str, Any]],
        embedding_model: str | None = None,
    ) -> MemoryResult:
        """Async upsert với encryption.

        Args:
            namespace: Target namespace
            records: Records to upsert
            embedding_model: Optional embedding model

        Returns:
            Upsert result
        """
        self._validate_namespace(namespace)
        self._validate_records(records)

        async with aiosqlite.connect(self.db_path) as db:
            processed = 0
            import time

            current_time = time.time()

            for record in records:
                try:
                    # Encrypt content
                    content = record.get("content") or record.get("text", "")
                    encrypted_content = self._encrypt_data(content)

                    # Encrypt metadata
                    metadata = record.get("metadata", {})
                    encrypted_metadata = self._encrypt_data(metadata)

                    # Generate mock embedding (replace with real embedding service)
                    embedding = self._generate_embedding(content)
                    encrypted_embedding = self._encrypt_data(embedding)

                    # Upsert record
                    await db.execute(
                        """
                        INSERT OR REPLACE INTO vectors
                        (id, namespace, encrypted_content, encrypted_metadata,
                         encrypted_embedding, created_at, updated_at)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                        (
                            record["id"],
                            namespace,
                            encrypted_content,
                            encrypted_metadata,
                            encrypted_embedding,
                            current_time,
                            current_time,
                        ),
                    )

                    processed += 1

                except Exception as e:
                    logger.error(f"Error processing record {record.get('id')}: {e}")
                    continue

            await db.commit()

        return self._create_result(
            status="success",
            namespace=namespace,
            operation="upsert",
            count=processed,
            metadata={"encrypted": True, "embedding_model": embedding_model},
        )

    async def query(
        self,
        namespace: str,
        query: str,
        top_k: int = 10,
        filters: dict[str, Any] | None = None,
    ) -> MemoryResult:
        """Async query với decryption.

        Args:
            namespace: Target namespace
            query: Search query
            top_k: Number of results
            filters: Optional filters

        Returns:
            Query results
        """
        self._validate_namespace(namespace)

        # Generate query embedding
        query_embedding = self._generate_embedding(query)

        async with aiosqlite.connect(self.db_path) as db:
            # Get all records in namespace
            cursor = await db.execute(
                """
                SELECT id, encrypted_content, encrypted_metadata, encrypted_embedding
                FROM vectors
                WHERE namespace = ?
                ORDER BY updated_at DESC
            """,
                [namespace],
            )

            rows = await cursor.fetchall()

            # Decrypt and score results
            results = []
            for row in rows:
                try:
                    record_id, enc_content, enc_metadata, enc_embedding = row

                    # Decrypt data
                    content = self._decrypt_data(enc_content)
                    metadata = self._decrypt_data(enc_metadata)
                    embedding = self._decrypt_data(enc_embedding)

                    # Calculate similarity (mock implementation)
                    similarity = self._calculate_similarity(query_embedding, embedding)

                    results.append(
                        {
                            "id": record_id,
                            "content": content,
                            "metadata": metadata,
                            "score": similarity,
                        }
                    )

                except Exception as e:
                    logger.error(f"Error decrypting record {record_id}: {e}")
                    continue

            # Sort by similarity and limit
            results.sort(key=lambda x: x["score"], reverse=True)
            results = results[:top_k]

        return self._create_result(
            status="success",
            namespace=namespace,
            operation="query",
            count=len(results),
            data={"results": results},
        )

    async def delete(
        self,
        namespace: str,
        ids: list[str] | None = None,
        filters: dict[str, Any] | None = None,
    ) -> MemoryResult:
        """Async delete với secure cleanup.

        Args:
            namespace: Target namespace
            ids: Record IDs to delete
            filters: Optional filters
            hard: Hard delete flag

        Returns:
            Delete result
        """
        self._validate_namespace(namespace)

        async with aiosqlite.connect(self.db_path) as db:
            if ids:
                # Delete by IDs
                placeholders = ",".join(["?"] * len(ids))
                sql = f"DELETE FROM vectors WHERE namespace = ? AND id IN ({placeholders})"
                params = [namespace] + ids
            else:
                # Delete all in namespace
                sql = "DELETE FROM vectors WHERE namespace = ?"
                params = [namespace]

            cursor = await db.execute(sql, params)
            deleted_count = cursor.rowcount
            await db.commit()

        return self._create_result(
            status="success",
            namespace=namespace,
            operation="delete",
            count=deleted_count,
        )

    async def rebuild_embeddings(
        self, namespace: str, target_model: str
    ) -> MemoryResult:
        """Rebuild embeddings với encryption.

        Args:
            namespace: Target namespace
            target_model: Target embedding model
            batch_size: Batch size

        Returns:
            Rebuild result
        """
        self._validate_namespace(namespace)

        async with aiosqlite.connect(self.db_path) as db:
            # Get all records
            cursor = await db.execute(
                """
                SELECT id, encrypted_content FROM vectors
                WHERE namespace = ?
            """,
                [namespace],
            )

            rows = await cursor.fetchall()
            processed = 0

            for record_id, enc_content in rows:
                try:
                    # Decrypt content
                    content = self._decrypt_data(enc_content)

                    # Generate new embedding
                    new_embedding = self._generate_embedding(content)
                    encrypted_embedding = self._encrypt_data(new_embedding)

                    # Update record
                    await db.execute(
                        """
                        UPDATE vectors
                        SET encrypted_embedding = ?, updated_at = ?
                        WHERE id = ?
                    """,
                        [encrypted_embedding, __import__("time").time(), record_id],
                    )

                    processed += 1

                except Exception as e:
                    logger.error(f"Error rebuilding embedding for {record_id}: {e}")
                    continue

            await db.commit()

        return self._create_result(
            status="success",
            namespace=namespace,
            operation="rebuild",
            count=processed,
            metadata={"target_model": target_model},
        )

    def _generate_embedding(self, text: str) -> list[float]:
        """Generate embedding vector (mock implementation).

        Args:
            text: Input text

        Returns:
            Embedding vector
        """
        # Mock embedding - replace with actual embedding service
        import hashlib
        import random

        # Use hash for deterministic but random-like results
        hash_obj = hashlib.md5(text.encode())
        hash_int = int(hash_obj.hexdigest(), 16)

        # Generate pseudo-random vector
        random.seed(hash_int)
        return [random.random() for _ in range(self.embedding_dim)]

    def _calculate_similarity(self, vec1: list[float], vec2: list[float]) -> float:
        """Calculate cosine similarity between vectors.

        Args:
            vec1: First vector
            vec2: Second vector

        Returns:
            Similarity score (0-1)
        """
        import math

        # Cosine similarity
        dot_product = sum(a * b for a, b in zip(vec1, vec2, strict=False))
        norm1 = math.sqrt(sum(a * a for a in vec1))
        norm2 = math.sqrt(sum(b * b for b in vec2))

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return dot_product / (norm1 * norm2)

    def get_encryption_key(self) -> str:
        """Get encryption key (for backup/restore).

        Returns:
            Base64 encoded encryption key
        """
        return self.cipher._encryption_key.decode()

    async def get_stats(self) -> dict[str, Any]:
        """Get backend statistics.

        Returns:
            Statistics dictionary
        """
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute("SELECT COUNT(*) FROM vectors")
            total_records = (await cursor.fetchone())[0]

            cursor = await db.execute("SELECT COUNT(DISTINCT namespace) FROM vectors")
            total_namespaces = (await cursor.fetchone())[0]

        return {
            "total_records": total_records,
            "total_namespaces": total_namespaces,
            "encrypted": True,
            "db_path": self.db_path,
            "embedding_dim": self.embedding_dim,
        }
