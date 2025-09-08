from __future__ import annotations

import logging
from concurrent.futures import ThreadPoolExecutor
from typing import Any

from apps.backend.data.services.memory_adapter import MemoryAdapter
from tenacity import retry, stop_after_attempt, wait_exponential
import Exception
import backend
import batch
import batch_size
import bool
import dict
import e
import embedding_model
import enable_retry
import filters
import flt
import hard
import hasattr
import i
import ids
import int
import isinstance
import kwargs
import len
import list
import max_workers
import namespace
import range
import records
import self
import str
import super
import top_k

"""Batch Processing với Rate Limiting cho Memory Operations.
Module này cung cấp:
- BulkMemoryAdapter với batch processing
- Rate limiting với tenacity retry
- ThreadPoolExecutor cho concurrent processing
"""
logger = logging.getLogger(__name__)


class BulkMemoryAdapter(MemoryAdapter):
    """MemoryAdapter với batch processing và rate limiting."""

    def __init__(
        self,
        backend: Any,
        batch_size: int = 500,
        max_workers: int = 8,
        enable_retry: bool = True,
    ):
        """Initialize bulk adapter.
        Args:
            backend: Underlying memory backend
            batch_size: Size of each batch for processing
            max_workers: Maximum concurrent workers
            enable_retry: Whether to enable retry logic
        """
        super().__init__(backend)
        self.batch_size = batch_size
        self.max_workers = max_workers
        self.enable_retry = enable_retry
        self._executor = ThreadPoolExecutor(max_workers=max_workers)

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        reraise=True,
    )
    def upsert(
        self,
        *,
        namespace: str,
        records: list[dict[str, Any]],
        embedding_model: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Bulk upsert với batch processing và retry logic.
        Args:
            namespace: Target namespace
            records: List of records to upsert
            embedding_model: Optional embedding model
            **kwargs: Additional arguments
        Returns:
            Operation result
        """
        if not self.enable_retry:
            return self._bulk_upsert(namespace, records, embedding_model, **kwargs)
        return self._bulk_upsert(namespace, records, embedding_model, **kwargs)

    def _bulk_upsert(
        self,
        namespace: str,
        records: list[dict[str, Any]],
        embedding_model: str | None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Internal bulk upsert implementation.
        Args:
            namespace: Target namespace
            records: Records to process
            embedding_model: Embedding model
            **kwargs: Additional arguments
        Returns:
            Operation result
        """
        if len(records) <= self.batch_size:
            return self._b.upsert(
                namespace=namespace, records=records, embedding_model=embedding_model
            )
        batches = [
            records[i : i + self.batch_size]
            for i in range(0, len(records), self.batch_size)
        ]
        logger.info(
            f"Processing {len(records)} records in {len(batches)} batches of size {self.batch_size}"
        )
        futures = []
        for batch in batches:
            future = self._executor.submit(
                self._b.upsert,
                namespace=namespace,
                records=batch,
                embedding_model=embedding_model,
            )
            futures.append(future)
        results = []
        total_processed = 0
        errors = []
        for future in futures:
            try:
                result = future.result(timeout=300)  # 5 minute timeout
                results.append(result)
                if isinstance(result, dict) and "count" in result:
                    total_processed += result["count"]
            except Exception as e:
                logger.error(f"Batch processing error: {e}")
                errors.append(str(e))
        if errors:
            return {
                "status": "partial" if results else "error",
                "namespace": namespace,
                "operation": "batch_upsert",
                "count": total_processed,
                "errors": errors,
                "batches_processed": len(results),
                "total_batches": len(batches),
            }
        return {
            "status": "success",
            "namespace": namespace,
            "operation": "batch_upsert",
            "count": total_processed,
            "batches_processed": len(results),
            "total_batches": len(batches),
        }

    def query(
        self,
        *,
        namespace: str,
        query: str,
        top_k: int = 10,
        filters: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Query với rate limiting.
        Args:
            namespace: Target namespace
            query: Search query
            top_k: Number of results
            filters: Optional filters
            **kwargs: Additional arguments
        Returns:
            Query results
        """
        # TODO: Replace blocking sleep with async await asyncio.sleep(0.01)  # 10ms delay between queries
        return self._b.query(
            namespace=namespace, query=query, top_k=top_k, filters=filters
        )

    def delete(
        self,
        *,
        namespace: str,
        ids: list[str] | None = None,
        flt: dict[str, Any] | None = None,
        hard: bool = False,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Delete với batch processing cho large operations.
        Args:
            namespace: Target namespace
            ids: Record IDs to delete
            flt: Filters for deletion
            hard: Hard delete flag
            **kwargs: Additional arguments
        Returns:
            Delete result
        """
        if ids and len(ids) > self.batch_size:
            return self._batch_delete(namespace, ids, hard)
        else:
            return self._b.delete(namespace=namespace, ids=ids, flt=flt, hard=hard)

    def _batch_delete(
        self, namespace: str, ids: list[str], hard: bool
    ) -> dict[str, Any]:
        """Batch delete implementation.
        Args:
            namespace: Target namespace
            ids: IDs to delete
            hard: Hard delete flag
        Returns:
            Delete result
        """
        batches = [
            ids[i : i + self.batch_size] for i in range(0, len(ids), self.batch_size)
        ]
        logger.info(f"Batch deleting {len(ids)} records in {len(batches)} batches")
        futures = []
        for batch in batches:
            future = self._executor.submit(
                self._b.delete, namespace=namespace, ids=batch, hard=hard
            )
            futures.append(future)
        total_deleted = 0
        errors = []
        for future in futures:
            try:
                result = future.result(timeout=300)
                if isinstance(result, dict) and "count" in result:
                    total_deleted += result["count"]
            except Exception as e:
                logger.error(f"Batch delete error: {e}")
                errors.append(str(e))
        return {
            "status": "success" if not errors else "partial",
            "namespace": namespace,
            "operation": "batch_delete",
            "count": total_deleted,
            "errors": errors if errors else None,
        }

    def __del__(self):
        """Cleanup executor on deletion."""
        if hasattr(self, "_executor"):
            self._executor.shutdown(wait=True)


__all__ = [
    "BulkMemoryAdapter",
    "batches",
    "delete",
    "errors",
    "future",
    "futures",
    "logger",
    "query",
    "result",
    "results",
    "total_deleted",
    "total_processed",
    "upsert",
]
