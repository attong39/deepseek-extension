"""
Knowledge Graph Service with Temporal Memory and RAG Integration
"""
from __future__ import annotations
from typing import Dict, List, Optional, Any, Set, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from enum import Enum
import uuid
from collections import defaultdict, deque
import json
import math

from pydantic import BaseModel, Field
from prometheus_client import Counter, Histogram, Gauge
import ValueError
import any
import bool
import boost
import concept
import context
import cost
import current_id
import dict
import distance
import e
import edge
import edge_types
import end_id
import entity_id
import event
import float
import i
import int
import key
import len
import max_depth
import max_distance
import min
import neighbor
import neighbor_id
import node_id
import path
import range
import self
import set
import sorted
import source
import start_id
import str
import target
import temporal_window_hours
import term
import v
import value
import x


# Prometheus metrics
kg_queries_total = Counter(
    "zeta_kg_queries_total",
    "Total knowledge graph queries",
    ["query_type", "status"]
)

kg_query_duration = Histogram(
    "zeta_kg_query_duration_seconds",
    "Knowledge graph query duration",
    ["query_type"]
)

kg_nodes_total = Gauge(
    "zeta_kg_nodes_total",
    "Total nodes in knowledge graph"
)

kg_edges_total = Gauge(
    "zeta_kg_edges_total", 
    "Total edges in knowledge graph"
)

rag_retrievals_total = Counter(
    "zeta_rag_retrievals_total",
    "Total RAG retrievals with knowledge graph",
    ["retrieval_type", "hit_count"]
)


class NodeType(str, Enum):
    """Knowledge graph node types"""
    CONCEPT = "concept"
    ENTITY = "entity"
    DOCUMENT = "document"
    USER = "user"
    SESSION = "session"
    QUERY = "query"
    RESPONSE = "response"
    TASK = "task"
    AGENT = "agent"


class EdgeType(str, Enum):
    """Knowledge graph edge types"""
    RELATED_TO = "related_to"
    PART_OF = "part_of"
    DEPENDS_ON = "depends_on"
    SIMILAR_TO = "similar_to"
    DERIVED_FROM = "derived_from"
    PRECEDES = "precedes"
    FOLLOWS = "follows"
    CONTAINS = "contains"
    REFERENCES = "references"
    CAUSES = "causes"


@dataclass
class KnowledgeNode:
    """Node in the knowledge graph"""
    node_id: str
    node_type: NodeType
    name: str
    properties: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    embeddings: Optional[List[float]] = None
    access_count: int = 0
    last_accessed: Optional[datetime] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert node to dictionary"""
        return {
            "node_id": self.node_id,
            "node_type": self.node_type.value,
            "name": self.name,
            "properties": self.properties,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "access_count": self.access_count,
            "last_accessed": self.last_accessed.isoformat() if self.last_accessed else None
        }


@dataclass
class KnowledgeEdge:
    """Edge in the knowledge graph"""
    edge_id: str
    source_id: str
    target_id: str
    edge_type: EdgeType
    weight: float = 1.0
    properties: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    confidence: float = 1.0
    temporal_decay: float = 1.0  # For time-based importance decay
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert edge to dictionary"""
        return {
            "edge_id": self.edge_id,
            "source_id": self.source_id,
            "target_id": self.target_id,
            "edge_type": self.edge_type.value,
            "weight": self.weight,
            "properties": self.properties,
            "created_at": self.created_at.isoformat(),
            "confidence": self.confidence,
            "temporal_decay": self.temporal_decay
        }


@dataclass
class TemporalEvent:
    """Event in temporal memory"""
    event_id: str
    timestamp: datetime
    event_type: str
    entity_id: str
    data: Dict[str, Any] = field(default_factory=dict)
    context: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert event to dictionary"""
        return {
            "event_id": self.event_id,
            "timestamp": self.timestamp.isoformat(),
            "event_type": self.event_type,
            "entity_id": self.entity_id,
            "data": self.data,
            "context": self.context
        }


class PathResult(BaseModel):
    """Result from BFS path finding"""
    path: List[str] = Field(description="Node IDs in the path")
    distance: int = Field(description="Path length")
    cost: float = Field(description="Total path cost")
    nodes: List[Dict[str, Any]] = Field(description="Node details in path")
    edges: List[Dict[str, Any]] = Field(description="Edge details in path")


class RetrievalContext(BaseModel):
    """Context for RAG retrieval enhancement"""
    query: str
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    max_results: int = 10
    temporal_window_hours: Optional[int] = 24
    include_related: bool = True
    boost_factors: Dict[str, float] = Field(default_factory=dict)


class KnowledgeGraphService:
    """In-memory knowledge graph with temporal capabilities"""
    
    def __init__(self, temporal_window_hours: int = 168):  # 1 week default
        self.nodes: Dict[str, KnowledgeNode] = {}
        self.edges: Dict[str, KnowledgeEdge] = {}
        self.adjacency: Dict[str, Set[str]] = defaultdict(set)  # For fast traversal
        self.reverse_adjacency: Dict[str, Set[str]] = defaultdict(set)
        self.temporal_events: deque = deque(maxlen=10000)  # Ring buffer for events
        self.temporal_window_hours = temporal_window_hours
        
        # Indexes for fast lookup
        self.type_index: Dict[NodeType, Set[str]] = defaultdict(set)
        self.property_index: Dict[str, Dict[Any, Set[str]]] = defaultdict(lambda: defaultdict(set))
        
    def add_node(self, node: KnowledgeNode) -> None:
        """Add node to the graph"""
        self.nodes[node.node_id] = node
        self.type_index[node.node_type].add(node.node_id)
        
        # Index properties for fast search
        for key, value in node.properties.items():
            self.property_index[key][value].add(node.node_id)
        
        kg_nodes_total.set(len(self.nodes))
    
    def add_edge(self, edge: KnowledgeEdge) -> None:
        """Add edge to the graph"""
        # Validate nodes exist
        if edge.source_id not in self.nodes or edge.target_id not in self.nodes:
            raise ValueError("Source or target node does not exist")
        
        self.edges[edge.edge_id] = edge
        self.adjacency[edge.source_id].add(edge.target_id)
        self.reverse_adjacency[edge.target_id].add(edge.source_id)
        
        kg_edges_total.set(len(self.edges))
    
    def get_node(self, node_id: str) -> Optional[KnowledgeNode]:
        """Get node by ID"""
        node = self.nodes.get(node_id)
        if node:
            node.access_count += 1
            node.last_accessed = datetime.now(timezone.utc)
        return node
    
    def bfs_shortest_path(
        self, 
        start_id: str, 
        end_id: str, 
        max_depth: int = 6
    ) -> Optional[PathResult]:
        """Find shortest path between two nodes using BFS"""
        start_time = datetime.now(timezone.utc)
        
        try:
            if start_id not in self.nodes or end_id not in self.nodes:
                return None
            
            if start_id == end_id:
                node = self.nodes[start_id]
                return PathResult(
                    path=[start_id],
                    distance=0,
                    cost=0.0,
                    nodes=[node.to_dict()],
                    edges=[]
                )
            
            # BFS with path tracking
            queue = deque([(start_id, [start_id], 0.0)])
            visited = {start_id}
            
            while queue:
                current_id, path, cost = queue.popleft()
                
                if len(path) > max_depth:
                    continue
                
                # Check all neighbors
                for neighbor_id in self.adjacency[current_id]:
                    if neighbor_id in visited:
                        continue
                    
                    new_path = path + [neighbor_id]
                    
                    # Find edge cost
                    edge_cost = 1.0  # Default cost
                    for edge in self.edges.values():
                        if (edge.source_id == current_id and edge.target_id == neighbor_id):
                            edge_cost = 1.0 / edge.weight  # Lower weight = higher cost
                            break
                    
                    new_cost = cost + edge_cost
                    
                    if neighbor_id == end_id:
                        # Found target, build result
                        nodes = [self.nodes[node_id].to_dict() for node_id in new_path]
                        edges = []
                        
                        # Collect edges in path
                        for i in range(len(new_path) - 1):
                            source, target = new_path[i], new_path[i + 1]
                            for edge in self.edges.values():
                                if edge.source_id == source and edge.target_id == target:
                                    edges.append(edge.to_dict())
                                    break
                        
                        return PathResult(
                            path=new_path,
                            distance=len(new_path) - 1,
                            cost=new_cost,
                            nodes=nodes,
                            edges=edges
                        )
                    
                    visited.add(neighbor_id)
                    queue.append((neighbor_id, new_path, new_cost))
            
            return None  # No path found
            
        finally:
            # Record metrics
            duration = (datetime.now(timezone.utc) - start_time).total_seconds()
            kg_query_duration.labels(query_type="bfs_path").observe(duration)
            kg_queries_total.labels(query_type="bfs_path", status="completed").inc()
    
    def enhance_rag_retrieval(self, context: RetrievalContext) -> Dict[str, Any]:
        """Enhance RAG retrieval with knowledge graph context"""
        start_time = datetime.now(timezone.utc)
        
        try:
            enhancement = {
                "query": context.query,
                "related_concepts": [],
                "temporal_context": [],
                "user_context": [],
                "boost_terms": [],
                "expansion_queries": []
            }
            
            # Find query-related nodes
            query_terms = context.query.lower().split()
            related_nodes = []
            
            # Search for nodes matching query terms
            for term in query_terms:
                for node in self.nodes.values():
                    if (term in node.name.lower() or 
                        any(term in str(v).lower() for v in node.properties.values())):
                        related_nodes.append(node)
            
            # Get related concepts through graph traversal
            concept_scores = defaultdict(float)
            for node in related_nodes[:5]:  # Limit to top 5 matches
                neighbors = self.get_neighbors(node.node_id, max_distance=2)
                for neighbor, edge, distance in neighbors:
                    # Score based on edge weight and distance
                    score = edge.weight / (distance + 1)
                    concept_scores[neighbor.name] += score
            
            # Sort and add top concepts
            top_concepts = sorted(concept_scores.items(), key=lambda x: x[1], reverse=True)[:10]
            enhancement["related_concepts"] = [
                {"concept": concept, "relevance_score": score}
                for concept, score in top_concepts
            ]
            
            # Add temporal context if user provided
            if context.user_id:
                user_timeline = self.get_temporal_timeline(
                    context.user_id,
                    start_time=datetime.now(timezone.utc) - timedelta(hours=context.temporal_window_hours or 24)
                )
                enhancement["temporal_context"] = [event.to_dict() for event in user_timeline[-10:]]
            
            # Generate query expansions based on related concepts
            enhancement["expansion_queries"] = [
                f"{context.query} {concept}"
                for concept, _ in top_concepts[:3]
            ]
            
            # Apply boost factors
            for term, boost in context.boost_factors.items():
                if term.lower() in context.query.lower():
                    enhancement["boost_terms"].append({"term": term, "boost": boost})
            
            # Record metrics
            hit_count = len(related_nodes)
            rag_retrievals_total.labels(
                retrieval_type="knowledge_enhanced",
                hit_count=min(hit_count, 10)  # Cap for cardinality
            ).inc()
            
            return enhancement
            
        finally:
            duration = (datetime.now(timezone.utc) - start_time).total_seconds()
            kg_query_duration.labels(query_type="rag_enhancement").observe(duration)
            kg_queries_total.labels(query_type="rag_enhancement", status="completed").inc()
    
    def get_neighbors(
        self, 
        node_id: str, 
        edge_types: List[EdgeType] = None,
        max_distance: int = 1
    ) -> List[Tuple[KnowledgeNode, KnowledgeEdge, int]]:
        """Get neighboring nodes with their connecting edges and distances"""
        if node_id not in self.nodes:
            return []
        
        result = []
        visited = set()
        queue = deque([(node_id, 0)])
        
        while queue:
            current_id, distance = queue.popleft()
            
            if distance >= max_distance:
                continue
            
            if current_id in visited:
                continue
            visited.add(current_id)
            
            # Get direct neighbors
            for neighbor_id in self.adjacency[current_id]:
                if neighbor_id not in self.nodes:
                    continue
                
                # Find connecting edge
                connecting_edge = None
                for edge in self.edges.values():
                    if (edge.source_id == current_id and 
                        edge.target_id == neighbor_id):
                        if edge_types is None or edge.edge_type in edge_types:
                            connecting_edge = edge
                            break
                
                if connecting_edge:
                    neighbor_node = self.nodes[neighbor_id]
                    result.append((neighbor_node, connecting_edge, distance + 1))
                    
                    if distance + 1 < max_distance:
                        queue.append((neighbor_id, distance + 1))
        
        return result
    
    def add_temporal_event(self, event: TemporalEvent) -> None:
        """Add event to temporal memory"""
        self.temporal_events.append(event)
    
    def get_temporal_timeline(
        self, 
        entity_id: str, 
        start_time: datetime = None,
        end_time: datetime = None
    ) -> List[TemporalEvent]:
        """Get temporal timeline for an entity"""
        if not start_time:
            start_time = datetime.now(timezone.utc) - timedelta(hours=self.temporal_window_hours)
        if not end_time:
            end_time = datetime.now(timezone.utc)
        
        timeline = []
        for event in self.temporal_events:
            if (event.entity_id == entity_id and 
                start_time <= event.timestamp <= end_time):
                timeline.append(event)
        
        return sorted(timeline, key=lambda e: e.timestamp)


def create_knowledge_graph_service(temporal_window_hours: int = 168) -> KnowledgeGraphService:
    """Create a configured knowledge graph service"""
    return KnowledgeGraphService(temporal_window_hours=temporal_window_hours)
