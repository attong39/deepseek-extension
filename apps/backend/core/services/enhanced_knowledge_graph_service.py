"""
Enhanced Knowledge Graph Service với multimodal support.

Features:
- Dynamic knowledge graph construction
- Entity extraction & relationship mapping
- Multimodal nodes (text, images, audio)
- Real-time graph updates
- Graph querying & reasoning
- Vector-graph hybrid search
"""

from __future__ import annotations

import json
import logging
import time
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any
from uuid import uuid4
import Exception
import ImportError
import ValueError
import a
import any
import b
import bool
import cached_result
import confidence
import dict
import document_id
import e
import embedding_service
import entity
import entity_extractor
import float
import hash
import int
import isinstance
import key
import len
import limit
import list
import max
import max_hops
import n
import name
import neighbor_id
import nid
import nt
import query
import query_text
import range
import redis_url
import relation_types
import result
import rt
import seed_node_ids
import self
import set
import source_id
import source_type
import str
import sum
import target_id
import text
import tuple
import value
import vec1
import vec2
import weight
import x
import zip

logger = logging.getLogger(__name__)

# Optional dependencies
try:
    import networkx as nx

    NETWORKX_AVAILABLE = True
except ImportError:
    nx = None
    NETWORKX_AVAILABLE = False

try:
    import redis.asyncio as redis

    REDIS_AVAILABLE = True
except ImportError:
    redis = None
    REDIS_AVAILABLE = False


class NodeType(Enum):
    """Types of knowledge graph nodes."""

    ENTITY = "entity"
    CONCEPT = "concept"
    DOCUMENT = "document"
    IMAGE = "image"
    AUDIO = "audio"
    VIDEO = "video"
    EVENT = "event"
    RELATION = "relation"


class RelationType(Enum):
    """Types of relationships."""

    IS_A = "is_a"
    PART_OF = "part_of"
    RELATED_TO = "related_to"
    CAUSES = "causes"
    CONTAINS = "contains"
    MENTIONS = "mentions"
    SIMILAR_TO = "similar_to"
    OPPOSITE_OF = "opposite_of"
    TEMPORAL_BEFORE = "temporal_before"
    TEMPORAL_AFTER = "temporal_after"
    SPATIAL_NEAR = "spatial_near"


@dataclass
class KGNode:
    """Knowledge graph node."""

    id: str
    name: str
    node_type: NodeType
    properties: dict[str, Any] = field(default_factory=dict)
    embeddings: dict[str, list[float]] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)
    confidence: float = 1.0


@dataclass
class KGEdge:
    """Knowledge graph edge."""

    id: str
    source_id: str
    target_id: str
    relation_type: RelationType
    properties: dict[str, Any] = field(default_factory=dict)
    weight: float = 1.0
    confidence: float = 1.0
    created_at: float = field(default_factory=time.time)
    evidence: list[str] = field(default_factory=list)


@dataclass
class GraphQuery:
    """Knowledge graph query."""

    query_text: str
    node_types: list[NodeType] | None = None
    relation_types: list[RelationType] | None = None
    max_hops: int = 2
    min_confidence: float = 0.5
    include_embeddings: bool = False
    limit: int = 100


@dataclass
class GraphQueryResult:
    """Result from graph query."""

    nodes: list[KGNode]
    edges: list[KGEdge]
    subgraph: dict[str, Any] | None = None
    query_time_ms: float = 0.0
    total_matches: int = 0


class EnhancedKnowledgeGraphService:
    """
    Enhanced Knowledge Graph Service với multimodal support.

    Features:
    - Async graph operations
    - Redis persistence
    - Vector-graph hybrid search
    - Multimodal nodes
    - Real-time updates
    - Graph reasoning
    """

    def __init__(
        self,
        redis_url: str = "redis://localhost:6379",
        embedding_service: Any | None = None,
        entity_extractor: Any | None = None,
    ) -> None:
        """Initialize knowledge graph service."""
        self.redis_url = redis_url
        self.redis: redis.Redis | None = None
        self.embedding_service = embedding_service
        self.entity_extractor = entity_extractor

        # In-memory graph for fast operations
        self.graph: nx.DiGraph | None = None
        if NETWORKX_AVAILABLE:
            self.graph = nx.DiGraph()

        # Node and edge storages
        self.nodes: dict[str, KGNode] = {}
        self.edges: dict[str, KGEdge] = {}

        # Caches
        self.query_cache: dict[str, GraphQueryResult] = {}
        self.cache_ttl = 3600  # 1 hour

        # Stats
        self.stats = {
            "total_nodes": 0,
            "total_edges": 0,
            "queries_served": 0,
            "cache_hits": 0,
            "last_update": 0.0,
        }

    async def initialize(self) -> None:
        """Initialize service dependencies."""
        # Initialize Redis
        if REDIS_AVAILABLE:
            try:
                self.redis = redis.from_url(self.redis_url)
                await self.redis.ping()
                logger.info("Connected to Redis for KG persistence")
            except Exception as e:
                logger.warning(f"Redis connection failed: {e}")
                self.redis = None

        # Load existing graph
        await self.load_graph()

    async def shutdown(self) -> None:
        """Shutdown service."""
        await self.save_graph()
        if self.redis:
            await self.redis.close()

    async def add_node(
        self,
        name: str,
        node_type: NodeType,
        properties: dict[str, Any] | None = None,
        node_id: str | None = None,
    ) -> KGNode:
        """
        Add node to knowledge graph.

        Args:
            name: Node name
            node_type: Type of node
            properties: Node properties
            node_id: Optional custom ID

        Returns:
            Created KGNode
        """
        node_id = node_id or str(uuid4())
        properties = properties or {}

        # Generate embeddings if embedding service available
        embeddings = {}
        if self.embedding_service and name:
            try:
                text_embedding = await self.embedding_service.embed_text(name)
                embeddings["text"] = text_embedding
            except Exception as e:
                logger.warning(f"Failed to generate embedding for node {name}: {e}")

        node = KGNode(
            id=node_id,
            name=name,
            node_type=node_type,
            properties=properties,
            embeddings=embeddings,
        )

        # Store node
        self.nodes[node_id] = node

        # Add to NetworkX graph
        if self.graph is not None:
            self.graph.add_node(
                node_id,
                **{
                    "name": name,
                    "type": node_type.value,
                    "properties": properties,
                },
            )

        # Persist to Redis
        await self._persist_node(node)

        # Update stats
        self.stats["total_nodes"] = len(self.nodes)
        self.stats["last_update"] = time.time()

        logger.debug(f"Added node: {name} ({node_id})")
        return node

    async def add_edge(
        self,
        source_id: str,
        target_id: str,
        relation_type: RelationType,
        properties: dict[str, Any] | None = None,
        weight: float = 1.0,
        confidence: float = 1.0,
        evidence: list[str] | None = None,
        edge_id: str | None = None,
    ) -> KGEdge:
        """
        Add edge to knowledge graph.

        Args:
            source_id: Source node ID
            target_id: Target node ID
            relation_type: Type of relationship
            properties: Edge properties
            weight: Edge weight
            confidence: Confidence score
            evidence: Supporting evidence
            edge_id: Optional custom ID

        Returns:
            Created KGEdge
        """
        edge_id = edge_id or str(uuid4())
        properties = properties or {}
        evidence = evidence or []

        # Verify nodes exist
        if source_id not in self.nodes or target_id not in self.nodes:
            raise ValueError(
                f"Source or target node not found: {source_id} -> {target_id}"
            )

        edge = KGEdge(
            id=edge_id,
            source_id=source_id,
            target_id=target_id,
            relation_type=relation_type,
            properties=properties,
            weight=weight,
            confidence=confidence,
            evidence=evidence,
        )

        # Store edge
        self.edges[edge_id] = edge

        # Add to NetworkX graph
        if self.graph is not None:
            self.graph.add_edge(
                source_id,
                target_id,
                **{
                    "id": edge_id,
                    "type": relation_type.value,
                    "weight": weight,
                    "confidence": confidence,
                    "properties": properties,
                },
            )

        # Persist to Redis
        await self._persist_edge(edge)

        # Update stats
        self.stats["total_edges"] = len(self.edges)
        self.stats["last_update"] = time.time()

        logger.debug(f"Added edge: {source_id} -> {target_id} ({relation_type.value})")
        return edge

    async def query_graph(self, query: GraphQuery) -> GraphQueryResult:
        """
        Query knowledge graph.

        Args:
            query: Graph query

        Returns:
            Query results
        """
        start_time = time.perf_counter()

        # Check cache
        cache_key = self._get_query_cache_key(query)
        if cache_key in self.query_cache:
            self.query_cache[cache_key]
            if time.time() - cached_result.query_time_ms < self.cache_ttl:
                self.stats["cache_hits"] += 1
                return cached_result

        result_nodes = []
        result_edges = []

        # Text-based node search
        if query.query_text:
            # Vector similarity search if embeddings available
            if self.embedding_service:
                query_embedding = await self.embedding_service.embed_text(
                    query.query_text
                )
                similar_nodes = await self._find_similar_nodes(
                    query_embedding, query.limit // 2
                )
                result_nodes.extend(similar_nodes)

            # Text search in node names and properties
            text_matches = self._search_nodes_by_text(
                query.query_text, query.limit // 2
            )
            result_nodes.extend(text_matches)

        # Filter by node types
        if query.node_types:
            result_nodes = [n for n in result_nodes if n.node_type in query.node_types]

        # Filter by confidence
        result_nodes = [n for n in result_nodes if n.confidence >= query.min_confidence]

        # Get connected edges
        node_ids = {n.id for n in result_nodes}
        result_edges = self._get_edges_for_nodes(node_ids, query.relation_types)

        # Expand with neighboring nodes up to max_hops
        if query.max_hops > 0:
            expanded_nodes, expanded_edges = await self._expand_subgraph(
                node_ids, query.max_hops, query.relation_types
            )
            result_nodes.extend(expanded_nodes)
            result_edges.extend(expanded_edges)

        # Remove duplicates
        result_nodes = list({n.id: n for n in result_nodes}.values())
        result_edges = list({e.id: e for e in result_edges}.values())

        # Limit results
        result_nodes = result_nodes[: query.limit]

        # Build subgraph if NetworkX available
        subgraph_data = None
        if self.graph is not None and result_nodes:
            subgraph_nodes = [n.id for n in result_nodes]
            subgraph = self.graph.subgraph(subgraph_nodes)
            subgraph_data = {
                "nodes": len(subgraph.nodes),
                "edges": len(subgraph.edges),
                "connected_components": nx.number_connected_components(
                    subgraph.to_undirected()
                ),
            }

        # Create result
        query_time = (time.perf_counter() - start_time) * 1000
        _ = GraphQueryResult(
            nodes=result_nodes,
            edges=result_edges,
            subgraph=subgraph_data,
            query_time_ms=query_time,
            total_matches=len(result_nodes),
        )

        # Cache result
        self.query_cache[cache_key] = result

        # Update stats
        self.stats["queries_served"] += 1

        logger.info(
            f"Graph query completed: {len(result_nodes)} nodes, {len(result_edges)} edges in {query_time:.2f}ms"
        )
        return result

    async def extract_and_add_entities(
        self,
        text: str,
        document_id: str | None = None,
        source_type: str = "document",
    ) -> list[KGNode]:
        """
        Extract entities from text and add to graph.

        Args:
            text: Input text
            document_id: Optional document ID
            source_type: Source type for metadata

        Returns:
            List of created nodes
        """
        created_nodes = []

        # Extract entities using entity extractor
        if self.entity_extractor:
            try:
                entities = await self.entity_extractor.extract_entities(text)

                for entity in entities:
                    # Create node for entity
                    node = await self.add_node(
                        name=entity.get("text", ""),
                        node_type=NodeType.ENTITY,
                        properties={
                            "entity_type": entity.get("type", "UNKNOWN"),
                            "confidence": entity.get("confidence", 1.0),
                            "source_document": document_id,
                            "source_type": source_type,
                            "original_text": text[:500],  # Store snippet
                        },
                    )
                    created_nodes.append(node)

                    # Create relation to document if document_id provided
                    if document_id:
                        doc_node = self.nodes.get(document_id)
                        if not doc_node:
                            doc_node = await self.add_node(
                                name=f"Document {document_id}",
                                node_type=NodeType.DOCUMENT,
                                properties={"document_id": document_id},
                            )

                        await self.add_edge(
                            source_id=doc_node.id,
                            target_id=node.id,
                            relation_type=RelationType.MENTIONS,
                            confidence=entity.get("confidence", 1.0),
                        )

            except Exception as e:
                logger.error(f"Entity extraction failed: {e}")

        return created_nodes

    async def add_multimodal_node(
        self,
        name: str,
        node_type: NodeType,
        content_path: str | Path,
        properties: dict[str, Any] | None = None,
    ) -> KGNode:
        """
        Add multimodal node (image, audio, video).

        Args:
            name: Node name
            node_type: Type of multimodal content
            content_path: Path to content file
            properties: Additional properties

        Returns:
            Created multimodal node
        """
        properties = properties or {}
        content_path = Path(content_path)

        # Add file metadata
        if content_path.exists():
            properties.update(
                {
                    "file_path": str(content_path),
                    "file_size": content_path.stat().st_size,
                    "file_modified": content_path.stat().st_mtime,
                }
            )

        # Generate embeddings based on content type
        embeddings = {}
        if self.embedding_service:
            try:
                if node_type == NodeType.IMAGE:
                    # Image embedding
                    embeddings["image"] = await self.embedding_service.embed_image(
                        content_path
                    )
                elif node_type == NodeType.AUDIO:
                    # Audio embedding (could use audio features)
                    embeddings["audio"] = await self.embedding_service.embed_audio(
                        content_path
                    )
                # Add other multimodal embeddings as needed
            except Exception as e:
                logger.warning(f"Failed to generate multimodal embedding: {e}")

        node = await self.add_node(
            name=name,
            node_type=node_type,
            properties=properties,
        )

        # Update embeddings after creation
        if embeddings:
            node.embeddings.update(embeddings)
            await self._persist_node(node)

        return node

    async def _find_similar_nodes(
        self,
        query_embedding: list[float],
        limit: int = 50,
    ) -> list[KGNode]:
        """Find nodes similar to query embedding."""
        if not query_embedding:
            return []

        similarities = []
        for node in self.nodes.values():
            if "text" in node.embeddings:
                similarity = self._cosine_similarity(
                    query_embedding, node.embeddings["text"]
                )
                similarities.append((similarity, node))

        # Sort by similarity and return top results
        similarities.sort(key=lambda x: x[0], reverse=True)
        return [node for _, node in similarities[:limit]]

    def _search_nodes_by_text(self, query_text: str, limit: int = 50) -> list[KGNode]:
        """Search nodes by text matching."""
        query_lower = query_text.lower()
        matches = []

        for node in self.nodes.values():
            # Check name
            if query_lower in node.name.lower():
                matches.append(node)
                continue

            # Check properties
            for value in node.properties.values():
                if isinstance(value, str) and query_lower in value.lower():
                    matches.append(node)
                    break

        return matches[:limit]

    def _get_edges_for_nodes(
        self,
        node_ids: set[str],
        relation_types: list[RelationType] | None = None,
    ) -> list[KGEdge]:
        """Get edges connecting the given nodes."""
        edges = []

        for edge in self.edges.values():
            if edge.source_id in node_ids or edge.target_id in node_ids:
                if not relation_types or edge.relation_type in relation_types:
                    edges.append(edge)

        return edges

    async def _expand_subgraph(
        self,
        seed_node_ids: set[str],
        max_hops: int,
        relation_types: list[RelationType] | None = None,
    ) -> tuple[list[KGNode], list[KGEdge]]:
        """Expand subgraph by following edges."""
        if not self.graph or max_hops <= 0:
            return [], []

        current_nodes = seed_node_ids.copy()
        all_nodes = seed_node_ids.copy()

        for _hop in range(max_hops):
            next_nodes = set()

            for node_id in current_nodes:
                # Get neighbors
                neighbors = set(self.graph.neighbors(node_id))
                predecessors = set(self.graph.predecessors(node_id))
                all_neighbors = neighbors | predecessors

                for neighbor_id in all_neighbors:
                    if neighbor_id not in all_nodes:
                        # Check if edge matches relation type filter
                        edge_data = self.graph.get_edge_data(node_id, neighbor_id)
                        if not edge_data:
                            edge_data = self.graph.get_edge_data(neighbor_id, node_id)

                        if edge_data:
                            edge_type = edge_data.get("type")
                            if not relation_types or any(
                                rt.value == edge_type for rt in relation_types
                            ):
                                next_nodes.add(neighbor_id)
                                all_nodes.add(neighbor_id)

            current_nodes = next_nodes

            if not current_nodes:
                break

        # Get nodes and edges
        expanded_nodes = [self.nodes[nid] for nid in all_nodes if nid in self.nodes]
        expanded_edges = self._get_edges_for_nodes(all_nodes, relation_types)

        return expanded_nodes, expanded_edges

    def _cosine_similarity(self, vec1: list[float], vec2: list[float]) -> float:
        """Calculate cosine similarity between two vectors."""
        if len(vec1) != len(vec2):
            return 0.0

        dot_product = sum(a * b for a, b in zip(vec1, vec2, strict=False))
        magnitude1 = sum(a * a for a in vec1) ** 0.5
        magnitude2 = sum(b * b for b in vec2) ** 0.5

        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0

        return dot_product / (magnitude1 * magnitude2)

    def _get_query_cache_key(self, query: GraphQuery) -> str:
        """Generate cache key for query."""
        key_data = {
            "text": query.query_text,
            "node_types": [nt.value for nt in query.node_types]
            if query.node_types
            else None,
            "relation_types": [rt.value for rt in query.relation_types]
            if query.relation_types
            else None,
            "max_hops": query.max_hops,
            "min_confidence": query.min_confidence,
            "limit": query.limit,
        }
        return f"kg_query:{hash(json.dumps(key_data, sort_keys=True))}"

    async def _persist_node(self, node: KGNode) -> None:
        """Persist node to Redis."""
        if not self.redis:
            return

        try:
            node_data = {
                "id": node.id,
                "name": node.name,
                "node_type": node.node_type.value,
                "properties": json.dumps(node.properties),
                "embeddings": json.dumps(node.embeddings),
                "metadata": json.dumps(node.metadata),
                "created_at": node.created_at,
                "updated_at": node.updated_at,
                "confidence": node.confidence,
            }
            await self.redis.hset(f"kg:node:{node.id}", mapping=node_data)
        except Exception as e:
            logger.error(f"Failed to persist node {node.id}: {e}")

    async def _persist_edge(self, edge: KGEdge) -> None:
        """Persist edge to Redis."""
        if not self.redis:
            return

        try:
            edge_data = {
                "id": edge.id,
                "source_id": edge.source_id,
                "target_id": edge.target_id,
                "relation_type": edge.relation_type.value,
                "properties": json.dumps(edge.properties),
                "weight": edge.weight,
                "confidence": edge.confidence,
                "created_at": edge.created_at,
                "evidence": json.dumps(edge.evidence),
            }
            await self.redis.hset(f"kg:edge:{edge.id}", mapping=edge_data)
        except Exception as e:
            logger.error(f"Failed to persist edge {edge.id}: {e}")

    async def load_graph(self) -> None:
        """Load graph from Redis."""
        if not self.redis:
            return

        try:
            # Load nodes
            node_keys = await self.redis.keys("kg:node:*")
            for key in node_keys:
                node_data = await self.redis.hgetall(key)
                if node_data:
                    node = KGNode(
                        id=node_data["id"],
                        name=node_data["name"],
                        node_type=NodeType(node_data["node_type"]),
                        properties=json.loads(node_data.get("properties", "{}")),
                        embeddings=json.loads(node_data.get("embeddings", "{}")),
                        metadata=json.loads(node_data.get("metadata", "{}")),
                        created_at=float(node_data.get("created_at", 0)),
                        updated_at=float(node_data.get("updated_at", 0)),
                        confidence=float(node_data.get("confidence", 1.0)),
                    )
                    self.nodes[node.id] = node

                    if self.graph is not None:
                        self.graph.add_node(
                            node.id,
                            **{
                                "name": node.name,
                                "type": node.node_type.value,
                                "properties": node.properties,
                            },
                        )

            # Load edges
            edge_keys = await self.redis.keys("kg:edge:*")
            for key in edge_keys:
                edge_data = await self.redis.hgetall(key)
                if edge_data:
                    edge = KGEdge(
                        id=edge_data["id"],
                        source_id=edge_data["source_id"],
                        target_id=edge_data["target_id"],
                        relation_type=RelationType(edge_data["relation_type"]),
                        properties=json.loads(edge_data.get("properties", "{}")),
                        weight=float(edge_data.get("weight", 1.0)),
                        confidence=float(edge_data.get("confidence", 1.0)),
                        created_at=float(edge_data.get("created_at", 0)),
                        evidence=json.loads(edge_data.get("evidence", "[]")),
                    )
                    self.edges[edge.id] = edge

                    if self.graph is not None:
                        self.graph.add_edge(
                            edge.source_id,
                            edge.target_id,
                            **{
                                "id": edge.id,
                                "type": edge.relation_type.value,
                                "weight": edge.weight,
                                "confidence": edge.confidence,
                                "properties": edge.properties,
                            },
                        )

            # Update stats
            self.stats["total_nodes"] = len(self.nodes)
            self.stats["total_edges"] = len(self.edges)

            logger.info(f"Loaded KG: {len(self.nodes)} nodes, {len(self.edges)} edges")

        except Exception as e:
            logger.error(f"Failed to load graph from Redis: {e}")

    async def save_graph(self) -> None:
        """Save current graph state to Redis."""
        if not self.redis:
            return

        try:
            # Save all nodes and edges
            for node in self.nodes.values():
                await self._persist_node(node)

            for edge in self.edges.values():
                await self._persist_edge(edge)

            logger.info("Graph saved to Redis")

        except Exception as e:
            logger.error(f"Failed to save graph to Redis: {e}")

    def get_graph_stats(self) -> dict[str, Any]:
        """Get knowledge graph statistics."""
        node_type_counts = {}
        for node in self.nodes.values():
            node_type = node.node_type.value
            node_type_counts[node_type] = node_type_counts.get(node_type, 0) + 1

        relation_type_counts = {}
        for edge in self.edges.values():
            relation_type = edge.relation_type.value
            relation_type_counts[relation_type] = (
                relation_type_counts.get(relation_type, 0) + 1
            )

        # Graph metrics
        graph_metrics = {}
        if self.graph is not None and len(self.graph.nodes) > 0:
            try:
                graph_metrics = {
                    "density": nx.density(self.graph),
                    "connected_components": nx.number_weakly_connected_components(
                        self.graph
                    ),
                    "avg_clustering": nx.average_clustering(self.graph.to_undirected()),
                }
            except Exception as e:
                logger.warning(f"Failed to calculate graph metrics: {e}")

        return {
            "total_nodes": len(self.nodes),
            "total_edges": len(self.edges),
            "node_type_distribution": node_type_counts,
            "relation_type_distribution": relation_type_counts,
            "graph_metrics": graph_metrics,
            "cache_size": len(self.query_cache),
            "queries_served": self.stats["queries_served"],
            "cache_hit_rate": (
                self.stats["cache_hits"] / max(self.stats["queries_served"], 1) * 100
            ),
            "last_update": self.stats["last_update"],
        }


__all__ = [
    "EnhancedKnowledgeGraphService",
    "KGNode",
    "KGEdge",
    "GraphQuery",
    "GraphQueryResult",
    "NodeType",
    "RelationType",
]
