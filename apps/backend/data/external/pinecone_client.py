"""


Pinecone Vector Database Client.





Provides interface to Pinecone vector database for similarity search and storage.


"""

import asyncio
import logging
import os
from datetime import UTC, datetime
from typing import Any
import Exception
import ImportError
import ValueError
import api_key
import batch_size
import bool
import delete_all
import dict
import dimension
import e
import environment
import filter_conditions
import float
import i
import ids
import include_metadata
import include_values
import int
import len
import list
import metadata
import metadata_config
import metric
import namespace
import range
import replicas
import self
import set_metadata
import shards
import str
import timeout
import top_k
import tuple
import vector
import vector_id
import vectors

try:
    import pinecone

    PINECONE_AVAILABLE = True


except ImportError:
    PINECONE_AVAILABLE = False

    pinecone = None


logger = logging.getLogger(__name__)


class PineconeClient:
    """Client for interacting with Pinecone vector database."""

    def __init__(
        self,
        api_key: str | None = None,
        environment: str | None = None,
        index_name: str = "zeta-ai-vectors",
    ):
        """


        Initialize Pinecone client.





        Args:


            api_key: Pinecone API key


            environment: Pinecone environment


            index_name: Default index name


        """

        if not PINECONE_AVAILABLE:
            raise ImportError(
                "Pinecone package not installed. Install with: pip install pinecone-client"
            )

        self.api_key = api_key or os.getenv("PINECONE_API_KEY")

        self.environment = environment or os.getenv(
            "PINECONE_ENVIRONMENT", "us-east1-gcp"
        )

        self.index_name = index_name

        self.index = None

        if not self.api_key:
            raise ValueError("Pinecone API key is required")

        # Initialize Pinecone

        pinecone.init(api_key=self.api_key, environment=self.environment)

    async def create_index(
        self,
        index_name: str,
        dimension: int,
        metric: str = "cosine",
        replicas: int = 1,
        shards: int = 1,
        metadata_config: dict[str, Any] | None = None,
    ) -> bool:
        """


        Create a new Pinecone index.





        Args:


            index_name: Name of the index


            dimension: Vector dimension


            metric: Distance metric (cosine, euclidean, dotproduct)


            replicas: Number of replicas


            shards: Number of shards


            metadata_config: Metadata configuration





        Returns:


            True if index created successfully


        """

        try:
            if index_name in pinecone.list_indexes():
                logger.info(f"Index {index_name} already exists")

                return True

            create_request = {
                "name": index_name,
                "dimension": dimension,
                "metric": metric,
                "replicas": replicas,
                "shards": shards,
            }

            if metadata_config:
                create_request["metadata_config"] = metadata_config

            pinecone.create_index(**create_request)

            # Wait for index to be ready

            await self._wait_for_index_ready(index_name)

            logger.info(f"Index {index_name} created successfully")

            return True

        except Exception as e:
            logger.error(f"Error creating index {index_name}: {e}")

            return False

    async def connect_to_index(self, index_name: str | None = None) -> bool:
        """


        Connect to a Pinecone index.





        Args:


            index_name: Index name to connect to





        Returns:


            True if connection successful


        """

        index_name = index_name or self.index_name

        try:
            if index_name not in pinecone.list_indexes():
                logger.error(f"Index {index_name} does not exist")

                return False

            self.index = pinecone.Index(index_name)

            self.index_name = index_name

            logger.info(f"Connected to index {index_name}")

            return True

        except Exception as e:
            logger.error(f"Error connecting to index {index_name}: {e}")

            return False

    async def upsert_vectors(
        self,
        vectors: list[tuple[str, list[float], dict[str, Any] | None]],
        namespace: str = "",
        batch_size: int = 100,
    ) -> dict[str, Any]:
        """


        Upsert vectors to the index.





        Args:


            vectors: List of (id, vector, metadata) tuples


            namespace: Namespace for the vectors


            batch_size: Batch size for upsert operations





        Returns:


            Upsert results


        """

        if not self.index:
            await self.connect_to_index()

        if not self.index:
            raise ValueError("No index connected")

        try:
            upserted_count = 0

            # Process in batches

            for i in range(0, len(vectors), batch_size):
                batch = vectors[i : i + batch_size]

                # Prepare batch data

                batch_data = []

                for vector_id, vector, metadata in batch:
                    item = {"id": vector_id, "values": vector}

                    if metadata:
                        item["metadata"] = metadata

                    batch_data.append(item)

                # Upsert batch

                response = self.index.upsert(vectors=batch_data, namespace=namespace)
                upserted_count += response.get("upserted_count", 0)

                # Add delay between batches

                if i + batch_size < len(vectors):
                    await asyncio.sleep(0.1)

            return {
                "upserted_count": upserted_count,
                "total_vectors": len(vectors),
                "namespace": namespace,
                "timestamp": datetime.now(UTC).isoformat(),
            }

        except Exception as e:
            logger.error(f"Error upserting vectors: {e}")

            raise

    async def query_vectors(
        self,
        vector: list[float],
        top_k: int = 10,
        namespace: str = "",
        filter_conditions: dict[str, Any] | None = None,
        include_metadata: bool = True,
        include_values: bool = False,
    ) -> dict[str, Any]:
        """


        Query vectors by similarity.





        Args:


            vector: Query vector


            top_k: Number of results to return


            namespace: Namespace to query


            filter_conditions: Metadata filters


            include_metadata: Include metadata in results


            include_values: Include vector values in results





        Returns:


            Query results with matches


        """

        if not self.index:
            await self.connect_to_index()

        if not self.index:
            raise ValueError("No index connected")

        try:
            query_params = {
                "vector": vector,
                "top_k": top_k,
                "namespace": namespace,
                "include_metadata": include_metadata,
                "include_values": include_values,
            }

            if filter_conditions:
                query_params["filter"] = filter_conditions

            response = self.index.query(**query_params)

            return {
                "matches": response.get("matches", []),
                "namespace": namespace,
                "query_timestamp": datetime.now(UTC).isoformat(),
            }

        except Exception as e:
            logger.error(f"Error querying vectors: {e}")

            raise

    async def query_by_id(
        self,
        vector_id: str,
        top_k: int = 10,
        namespace: str = "",
        filter_conditions: dict[str, Any] | None = None,
        include_metadata: bool = True,
        include_values: bool = False,
    ) -> dict[str, Any]:
        """


        Query vectors by ID similarity.





        Args:


            vector_id: ID of the vector to use as query


            top_k: Number of results to return


            namespace: Namespace to query


            filter_conditions: Metadata filters


            include_metadata: Include metadata in results


            include_values: Include vector values in results





        Returns:


            Query results with matches


        """

        if not self.index:
            await self.connect_to_index()

        if not self.index:
            raise ValueError("No index connected")

        try:
            query_params = {
                "id": vector_id,
                "top_k": top_k,
                "namespace": namespace,
                "include_metadata": include_metadata,
                "include_values": include_values,
            }

            if filter_conditions:
                query_params["filter"] = filter_conditions

            response = self.index.query(**query_params)

            return {
                "matches": response.get("matches", []),
                "namespace": namespace,
                "query_id": vector_id,
                "query_timestamp": datetime.now(UTC).isoformat(),
            }

        except Exception as e:
            logger.error(f"Error querying by ID {vector_id}: {e}")

            raise

    async def fetch_vectors(
        self, ids: list[str], namespace: str = ""
    ) -> dict[str, Any]:
        """


        Fetch vectors by IDs.





        Args:


            ids: List of vector IDs


            namespace: Namespace to fetch from





        Returns:


            Fetched vectors


        """

        if not self.index:
            await self.connect_to_index()

        if not self.index:
            raise ValueError("No index connected")

        try:
            response = self.index.fetch(ids=ids, namespace=namespace)

            return {
                "vectors": response.get("vectors", {}),
                "namespace": namespace,
                "fetched_count": len(response.get("vectors", {})),
                "timestamp": datetime.now(UTC).isoformat(),
            }

        except Exception as e:
            logger.error(f"Error fetching vectors: {e}")

            raise

    async def delete_vectors(
        self,
        ids: list[str] | None = None,
        delete_all: bool = False,
        namespace: str = "",
        filter_conditions: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """


        Delete vectors from the index.





        Args:


            ids: List of vector IDs to delete


            delete_all: Delete all vectors in namespace


            namespace: Namespace to delete from


            filter_conditions: Delete vectors matching filter





        Returns:


            Delete operation results


        """

        if not self.index:
            await self.connect_to_index()

        if not self.index:
            raise ValueError("No index connected")

        try:
            delete_params = {"namespace": namespace}

            if delete_all:
                delete_params["delete_all"] = True

            elif ids:
                delete_params["ids"] = ids

            elif filter_conditions:
                delete_params["filter"] = filter_conditions

            else:
                raise ValueError("Must specify ids, filter, or delete_all=True")

            self.index.delete(**delete_params)

            return {
                "deleted": True,
                "namespace": namespace,
                "timestamp": datetime.now(UTC).isoformat(),
            }

        except Exception as e:
            logger.error(f"Error deleting vectors: {e}")

            raise

    async def get_index_stats(self, namespace: str = "") -> dict[str, Any]:
        """


        Get index statistics.





        Args:


            namespace: Namespace to get stats for





        Returns:


            Index statistics


        """

        if not self.index:
            await self.connect_to_index()

        if not self.index:
            raise ValueError("No index connected")

        try:
            stats = self.index.describe_index_stats()

            return {
                "total_vector_count": stats.get("total_vector_count", 0),
                "dimension": stats.get("dimension", 0),
                "index_fullness": stats.get("index_fullness", 0.0),
                "namespaces": stats.get("namespaces", {}),
                "timestamp": datetime.now(UTC).isoformat(),
            }

        except Exception as e:
            logger.error(f"Error getting index stats: {e}")

            raise

    async def list_indexes(self) -> list[str]:
        """


        List all available indexes.





        Returns:


            List of index names


        """

        try:
            return pinecone.list_indexes()

        except Exception as e:
            logger.error(f"Error listing indexes: {e}")

            return []

    async def delete_index(self, index_name: str) -> bool:
        """


        Delete an index.





        Args:


            index_name: Name of index to delete





        Returns:


            True if deletion successful


        """

        try:
            pinecone.delete_index(index_name)

            logger.info(f"Index {index_name} deleted successfully")

            return True

        except Exception as e:
            logger.error(f"Error deleting index {index_name}: {e}")

            return False

    async def _wait_for_index_ready(self, index_name: str, timeout: int = 300) -> bool:
        """


        Wait for index to be ready.





        Args:


            index_name: Index name to wait for


            timeout: Timeout in seconds





        Returns:


            True if index is ready


        """

        start_time = datetime.now()

        while (datetime.now() - start_time).seconds < timeout:
            try:
                description = pinecone.describe_index(index_name)

                if description.status.ready:
                    return True

                await asyncio.sleep(5)

            except Exception:
                await asyncio.sleep(5)

        return False

    async def update_vector(
        self,
        vector_id: str,
        values: list[float] | None = None,
        set_metadata: dict[str, Any] | None = None,
        namespace: str = "",
    ) -> dict[str, Any]:
        """


        Update a vector in the index.





        Args:


            vector_id: ID of vector to update


            values: New vector values


            set_metadata: Metadata to set


            namespace: Namespace of the vector





        Returns:


            Update operation results


        """

        if not self.index:
            await self.connect_to_index()

        if not self.index:
            raise ValueError("No index connected")

        try:
            update_params = {"id": vector_id, "namespace": namespace}

            if values:
                update_params["values"] = values

            if set_metadata:
                update_params["set_metadata"] = set_metadata

            self.index.update(**update_params)

            return {
                "updated": True,
                "vector_id": vector_id,
                "namespace": namespace,
                "timestamp": datetime.now(UTC).isoformat(),
            }

        except Exception as e:
            logger.error(f"Error updating vector {vector_id}: {e}")

            raise

    async def search_by_metadata(
        self,
        filter_conditions: dict[str, Any],
        top_k: int = 10,
        namespace: str = "",
        include_metadata: bool = True,
        include_values: bool = False,
    ) -> dict[str, Any]:
        """


        Search vectors by metadata filters only.





        Args:


            filter_conditions: Metadata filter conditions


            top_k: Number of results to return


            namespace: Namespace to search


            include_metadata: Include metadata in results


            include_values: Include vector values in results





        Returns:


            Search results matching filters


        """

        # This is a workaround since Pinecone doesn't have metadata-only search

        # We'll use a zero vector and rely on filters

        zero_vector = [0.0] * 1536  # Assuming 1536 dimensions, adjust as needed

        return await self.query_vectors(
            vector=zero_vector,
            top_k=top_k,
            namespace=namespace,
            filter_conditions=filter_conditions,
            include_metadata=include_metadata,
            include_values=include_values,
        )
