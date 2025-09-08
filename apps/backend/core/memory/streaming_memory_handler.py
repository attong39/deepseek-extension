from __future__ import annotations

import json
import logging
from collections.abc import AsyncGenerator
from typing import Any

from apps.backend.core.interfaces.memory_backend import MemoryBackend
from fastapi import Request
from fastapi.responses import StreamingResponse
import Exception
import backend
import batch_size
import dict
import e
import filters
import generator
import i
import ids
import int
import len
import list
import min
import namespace
import query
import range
import records
import result_item
import self
import str
import target_model
import top_k

"""Streaming Response Handler cho Memory Operations.
Module này cung cấp:
- StreamingMemoryHandler với FastAPI StreamingResponse
- Async generators cho large result sets
- Memory-efficient streaming cho queries
"""
logger = logging.getLogger(__name__)
STREAMING_MEDIA_TYPE = "text/plain"
STREAMING_HEADERS = {
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Access-Control-Allow-Origin": "*",
}


class StreamingMemoryHandler:
    """Handler cho streaming memory responses."""

    def __init__(self, backend: MemoryBackend, chunk_size: int = 100):
        """Initialize streaming handler.
        Args:
            backend: Memory backend instance
            chunk_size: Size of each streaming chunk
        """
        self.backend = backend
        self.chunk_size = chunk_size

    def stream_query_results(
        self,
        namespace: str,
        query: str,
        top_k: int = 1000,
        filters: dict[str, Any] | None = None,
        request: Request | None = None,
    ) -> StreamingResponse:
        """Stream query results as JSON lines."""
        return self._create_streaming_response(
            self._generate_query_results(namespace, query, top_k, filters)
        )

    async def _generate_query_results(
        self, namespace: str, query: str, top_k: int, filters: dict[str, Any] | None
    ) -> AsyncGenerator[str, None]:
        """Generate streaming JSON lines for query results."""
        try:
            metadata = {
                "namespace": namespace,
                "query": query,
                "top_k": top_k,
                "filters": filters,
                "status": "streaming",
            }
            yield f"data: {json.dumps(metadata)}\n\n"
            total_processed = 0
            while total_processed < top_k:
                chunk_size = min(self.chunk_size, top_k - total_processed)
                result = await self.backend.query(
                    namespace=namespace, query=query, top_k=chunk_size, filters=filters
                )
                if not result.data or not result.data.get("results"):
                    break
                results = result.data["results"]
                for result_item in results:
                    if total_processed >= top_k:
                        break
                    yield f"data: {json.dumps(result_item)}\n\n"
                    total_processed += 1
                if len(results) < chunk_size:
                    break
            final_metadata = {
                "status": "completed",
                "total_processed": total_processed,
                "namespace": namespace,
            }
            yield f"data: {json.dumps(final_metadata)}\n\n"
        except Exception as e:
            logger.error(f"Error in streaming query: {e}")
            error_data = {"status": "error", "error": str(e), "namespace": namespace}
            yield f"data: {json.dumps(error_data)}\n\n"

    def stream_bulk_upsert(
        self,
        namespace: str,
        records: list[dict[str, Any]],
        batch_size: int = 50,
        request: Request | None = None,
    ) -> StreamingResponse:
        """Stream bulk upsert progress."""
        return self._create_streaming_response(
            self._generate_bulk_upsert_progress(namespace, records, batch_size)
        )

    async def _generate_bulk_upsert_progress(
        self, namespace: str, records: list[dict[str, Any]], batch_size: int
    ) -> AsyncGenerator[str, None]:
        """Generate streaming progress for bulk upsert."""
        try:
            total_records = len(records)
            processed = 0
            batches_processed = 0
            metadata = {
                "namespace": namespace,
                "total_records": total_records,
                "batch_size": batch_size,
                "status": "starting",
            }
            yield f"data: {json.dumps(metadata)}\n\n"
            for i in range(0, total_records, batch_size):
                batch = records[i : i + batch_size]
                batch_num = batches_processed + 1
                try:
                    result = await self.backend.upsert(
                        namespace=namespace, records=batch
                    )
                    processed += len(batch)
                    batches_processed += 1
                    progress = {
                        "status": "processing",
                        "batch": batch_num,
                        "processed": processed,
                        "total": total_records,
                        "success": result.status == "success",
                        "batch_count": len(batch),
                    }
                    yield f"data: {json.dumps(progress)}\n\n"
                except Exception as e:
                    logger.error(f"Error processing batch {batch_num}: {e}")
                    error_progress = {
                        "status": "error",
                        "batch": batch_num,
                        "error": str(e),
                        "processed": processed,
                        "total": total_records,
                    }
                    yield f"data: {json.dumps(error_progress)}\n\n"
                    continue
            final_status = {
                "status": "completed",
                "total_processed": processed,
                "total_records": total_records,
                "batches_processed": batches_processed,
                "namespace": namespace,
            }
            yield f"data: {json.dumps(final_status)}\n\n"
        except Exception as e:
            logger.error(f"Error in streaming upsert: {e}")
            error_data = {"status": "error", "error": str(e), "namespace": namespace}
            yield f"data: {json.dumps(error_data)}\n\n"

    def stream_delete_operation(
        self,
        namespace: str,
        ids: list[str] | None = None,
        filters: dict[str, Any] | None = None,
        request: Request | None = None,
    ) -> StreamingResponse:
        """Stream delete operation progress."""
        return self._create_streaming_response(
            self._generate_delete_progress(namespace, ids, filters)
        )

    async def _generate_delete_progress(
        self,
        namespace: str,
        ids: list[str] | None,
        filters: dict[str, Any] | None,
    ) -> AsyncGenerator[str, None]:
        """Generate streaming delete progress."""
        try:
            metadata = {
                "namespace": namespace,
                "operation": "delete",
                "ids_count": len(ids) if ids else 0,
                "has_filters": filters is not None,
                "status": "starting",
            }
            yield f"data: {json.dumps(metadata)}\n\n"
            result = await self.backend.delete(
                namespace=namespace, ids=ids, filters=filters
            )
            progress = {
                "status": "completed",
                "deleted_count": result.count,
                "namespace": namespace,
                "operation": "delete",
            }
            yield f"data: {json.dumps(progress)}\n\n"
        except Exception as e:
            logger.error(f"Error in streaming delete: {e}")
            error_data = {
                "status": "error",
                "error": str(e),
                "namespace": namespace,
                "operation": "delete",
            }
            yield f"data: {json.dumps(error_data)}\n\n"

    def stream_rebuild_embeddings(
        self,
        namespace: str,
        target_model: str,
        batch_size: int = 100,
        request: Request | None = None,
    ) -> StreamingResponse:
        """Stream embedding rebuild progress."""
        return self._create_streaming_response(
            self._generate_rebuild_progress(namespace, target_model)
        )

    async def _generate_rebuild_progress(
        self, namespace: str, target_model: str
    ) -> AsyncGenerator[str, None]:
        """Generate streaming rebuild progress."""
        try:
            metadata = {
                "namespace": namespace,
                "operation": "rebuild_embeddings",
                "target_model": target_model,
                "status": "starting",
            }
            yield f"data: {json.dumps(metadata)}\n\n"
            result = await self.backend.rebuild_embeddings(
                namespace=namespace, target_model=target_model
            )
            progress = {
                "status": "completed",
                "processed_count": result.count,
                "namespace": namespace,
                "target_model": target_model,
                "operation": "rebuild_embeddings",
            }
            yield f"data: {json.dumps(progress)}\n\n"
        except Exception as e:
            logger.error(f"Error in streaming rebuild: {e}")
            error_data = {
                "status": "error",
                "error": str(e),
                "namespace": namespace,
                "operation": "rebuild_embeddings",
            }
            yield f"data: {json.dumps(error_data)}\n\n"

    def _create_streaming_response(self, generator):
        """Create streaming response."""
        return StreamingResponse(
            generator, media_type=STREAMING_MEDIA_TYPE, headers=STREAMING_HEADERS
        )


__all__ = [
    "STREAMING_HEADERS",
    "STREAMING_MEDIA_TYPE",
    "StreamingMemoryHandler",
    "batch",
    "batch_num",
    "batches_processed",
    "chunk_size",
    "error_data",
    "error_progress",
    "final_metadata",
    "final_status",
    "logger",
    "metadata",
    "processed",
    "progress",
    "result",
    "results",
    "stream_bulk_upsert",
    "stream_delete_operation",
    "stream_query_results",
    "stream_rebuild_embeddings",
    "total_processed",
    "total_records",
]
