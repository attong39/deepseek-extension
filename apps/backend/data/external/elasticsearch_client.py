"""Elasticsearch client for search and analytics operations."""

from __future__ import annotations

import logging
from typing import Any

from apps.backend.config.settings import Settings

logger = logging.getLogger(__name__)


class ElasticsearchClient:
    """Client for Elasticsearch operations."""
import Exception
import ImportError
import bool
import dict
import doc
import doc_id
import document
import documents
import e
import fields
import from_
import getattr
import hasattr
import hit
import host
import index_name
import int
import list
import mapping
import password
import port
import query_string
import result
import self
import size
import str
import updates
import username

    def __init__(
        self,
        host: str | None = None,
        port: int | None = None,
        username: str | None = None,
        password: str | None = None,
    ):
        """Initialize Elasticsearch client."""

        self.settings = Settings()

        self.host = host or getattr(self.settings, "elasticsearch_host", "localhost")

        self.port = port or getattr(self.settings, "elasticsearch_port", 9200)

        self.username = username or getattr(
            self.settings, "elasticsearch_username", None
        )

        self.password = password or getattr(
            self.settings, "elasticsearch_password", None
        )

        self.client = None

        self.is_connected = False

    async def connect(self) -> bool:
        """Connect to Elasticsearch."""

        try:
            # Import elasticsearch-py if available

            try:
                from elasticsearch import AsyncElasticsearch

            except ImportError:
                logger.warning(
                    "elasticsearch-py not installed. Search functionality disabled."
                )

                return False

            # Build connection configuration

            config = {
                "hosts": [f"{self.host}:{self.port}"],
                "verify_certs": False,
                "ssl_show_warn": False,
            }

            if self.username and self.password:
                config["basic_auth"] = (self.username, self.password)

            self.client = AsyncElasticsearch(**config)

            # Test connection

            info = await self.client.info()

            logger.info(f"Connected to Elasticsearch: {info['version']['number']}")

            self.is_connected = True

            return True

        except Exception as e:
            logger.error(f"Failed to connect to Elasticsearch: {e}")

            self.is_connected = False

            return False

    async def disconnect(self) -> None:
        """Disconnect from Elasticsearch."""

        if self.client:
            await self.client.close()

            self.is_connected = False

            logger.info("Disconnected from Elasticsearch")

    async def create_index(
        self, index_name: str, mapping: dict[str, Any] | None = None
    ) -> bool:
        """Create an index with optional mapping."""

        if not self.is_connected:
            await self.connect()

        if not self.client:
            return False

        try:
            body = {}

            if mapping:
                body["mappings"] = mapping

            await self.client.indices.create(index=index_name, body=body)

            logger.info(f"Created index: {index_name}")

            return True

        except Exception as e:
            logger.error(f"Failed to create index {index_name}: {e}")

            return False

    async def delete_index(self, index_name: str) -> bool:
        """Delete an index."""

        if not self.is_connected:
            await self.connect()

        if not self.client:
            return False

        try:
            await self.client.indices.delete(index=index_name)

            logger.info(f"Deleted index: {index_name}")

            return True

        except Exception as e:
            logger.error(f"Failed to delete index {index_name}: {e}")

            return False

    async def index_document(
        self, index_name: str, document: dict[str, Any], doc_id: str | None = None
    ) -> str | None:
        """Index a document."""

        if not self.is_connected:
            await self.connect()

        if not self.client:
            return None

        try:
            _ = await self.client.index(index=index_name, body=document, id=doc_id)

            return result["_id"]

        except Exception as e:
            logger.error(f"Failed to index document: {e}")

            return None

    async def search(
        self, index_name: str, query: dict[str, Any], size: int = 10, from_: int = 0
    ) -> dict[str, Any] | None:
        """Search documents."""

        if not self.is_connected:
            await self.connect()

        if not self.client:
            return None

        try:
            _ = await self.client.search(
                index=index_name, body=query, size=size, from_=from_
            )

            return result.body if hasattr(result, "body") else None

        except Exception as e:
            logger.error(f"Search failed: {e}")

            return None

    async def simple_search(
        self,
        index_name: str,
        query_string: str,
        fields: list[str] | None = None,
        size: int = 10,
    ) -> list[dict[str, Any]]:
        """Perform a simple text search."""

        query = {
            "query": {"multi_match": {"query": query_string, "fields": fields or ["*"]}}
        }

        _ = await self.search(index_name, query, size=size)

        if result:
            return [hit["_source"] for hit in result["hits"]["hits"]]

        return []

    async def get_document(self, index_name: str, doc_id: str) -> dict[str, Any] | None:
        """Get a document by ID."""

        if not self.is_connected:
            await self.connect()

        if not self.client:
            return None

        try:
            _ = await self.client.get(index=index_name, id=doc_id)

            return result["_source"]

        except Exception as e:
            logger.error(f"Failed to get document {doc_id}: {e}")

            return None

    async def update_document(
        self, index_name: str, doc_id: str, updates: dict[str, Any]
    ) -> bool:
        """Update a document."""

        if not self.is_connected:
            await self.connect()

        if not self.client:
            return False

        try:
            await self.client.update(index=index_name, id=doc_id, body={"doc": updates})

            return True

        except Exception as e:
            logger.error(f"Failed to update document {doc_id}: {e}")

            return False

    async def delete_document(self, index_name: str, doc_id: str) -> bool:
        """Delete a document."""

        if not self.is_connected:
            await self.connect()

        if not self.client:
            return False

        try:
            await self.client.delete(index=index_name, id=doc_id)

            return True

        except Exception as e:
            logger.error(f"Failed to delete document {doc_id}: {e}")

            return False

    async def bulk_index(
        self, index_name: str, documents: list[dict[str, Any]]
    ) -> dict[str, Any]:
        """Bulk index documents."""

        if not self.is_connected:
            await self.connect()

        if not self.client:
            return {"errors": True, "message": "Not connected"}

        try:
            actions = []

            for doc in documents:
                action = {"_index": index_name, "_source": doc}

                if "id" in doc:
                    action["_id"] = doc.pop("id")

                actions.append(action)

            from elasticsearch.helpers import async_bulk

            _ = await async_bulk(self.client, actions)

            return {"errors": False, "indexed": result[0]}

        except Exception as e:
            logger.error(f"Bulk indexing failed: {e}")

            return {"errors": True, "message": str(e)}

    async def get_index_stats(self, index_name: str) -> dict[str, Any] | None:
        """Get index statistics."""

        if not self.is_connected:
            await self.connect()

        if not self.client:
            return None

        try:
            _ = await self.client.indices.stats(index=index_name)

            return result.body if hasattr(result, "body") else None

        except Exception as e:
            logger.error(f"Failed to get stats for {index_name}: {e}")

            return None


# Global Elasticsearch client instance


_es_client: ElasticsearchClient | None = None


def get_elasticsearch_client() -> ElasticsearchClient:
    """Get the global Elasticsearch client instance."""

    global _es_client

    if _es_client is None:
        _es_client = ElasticsearchClient()

    return _es_client


async def close_elasticsearch_client() -> None:
    """Close the global Elasticsearch client."""

    global _es_client

    if _es_client:
        await _es_client.disconnect()

        _es_client = None
