"""
Unit tests for KnowledgeGraphService
====================================

Tests for BFS path discovery, entity management, and relationship operations.
Focuses on algorithmic correctness and performance characteristics.
"""

import pytest
from apps.backend.core.knowledge.graph_service import KnowledgeGraphService
import entity
import i
import len
import path
import range
import self
import set


class TestKnowledgeGraphService:
    """Test suite for KnowledgeGraphService."""
    
    def setup_method(self):
        """Setup fresh KnowledgeGraphService for each test."""
        self.graph = KnowledgeGraphService()
    
    def test_add_entity_basic(self):
        """Test basic entity addition."""
        entity_id = self.graph.add_entity("user_123", {"name": "Alice"})
        assert entity_id == "user_123"
        assert self.graph.get_entity("user_123") == {"name": "Alice"}
    
    def test_add_entity_with_metadata(self):
        """Test entity addition with rich metadata."""
        metadata = {
            "name": "Project Alpha", 
            "type": "project",
            "created": "2024-01-15",
            "team_size": 5
        }
        entity_id = self.graph.add_entity("project_alpha", metadata)
        
        retrieved = self.graph.get_entity("project_alpha")
        assert retrieved == metadata
        assert retrieved["team_size"] == 5
    
    def test_add_relation_bidirectional(self):
        """Test bidirectional relationship creation."""
        # Setup entities
        self.graph.add_entity("alice", {"role": "developer"})
        self.graph.add_entity("bob", {"role": "designer"}) 
        
        # Add relation
        self.graph.add_relation("alice", "bob", "collaborates_with")
        
        # Verify bidirectional connectivity
        alice_neighbors = self.graph.get_neighbors("alice")
        bob_neighbors = self.graph.get_neighbors("bob")
        
        assert "bob" in alice_neighbors
        assert "alice" in bob_neighbors
    
    def test_bfs_path_discovery_direct(self):
        """Test BFS path discovery for directly connected entities."""
        # Create simple chain: A -> B -> C
        self.graph.add_entity("A", {"type": "start"})
        self.graph.add_entity("B", {"type": "middle"})
        self.graph.add_entity("C", {"type": "end"})
        
        self.graph.add_relation("A", "B", "leads_to")
        self.graph.add_relation("B", "C", "leads_to")
        
        # Test direct connection
        paths = self.graph.find_paths("A", "B", max_hops=1)
        assert len(paths) == 1
        assert paths[0] == ["A", "B"]
        
        # Test 2-hop connection  
        paths = self.graph.find_paths("A", "C", max_hops=2)
        assert len(paths) == 1
        assert paths[0] == ["A", "B", "C"]
    
    def test_bfs_path_discovery_multiple_paths(self):
        """Test BFS discovery of multiple paths."""
        # Create diamond pattern: A -> B -> D, A -> C -> D
        entities = ["A", "B", "C", "D"]
        for entity in entities:
            self.graph.add_entity(entity, {"id": entity})
        
        # Create diamond connections
        self.graph.add_relation("A", "B", "path1")
        self.graph.add_relation("A", "C", "path2") 
        self.graph.add_relation("B", "D", "converge1")
        self.graph.add_relation("C", "D", "converge2")
        
        # Find all paths from A to D
        paths = self.graph.find_paths("A", "D", max_hops=3)
        
        # Should find both paths
        assert len(paths) == 2
        path_sets = [set(path) for path in paths]
        
        # Verify both routes exist
        assert {"A", "B", "D"} in path_sets
        assert {"A", "C", "D"} in path_sets
    
    def test_bfs_max_hops_limitation(self):
        """Test that BFS respects max_hops parameter."""
        # Create longer chain: A -> B -> C -> D -> E
        entities = ["A", "B", "C", "D", "E"]
        for entity in entities:
            self.graph.add_entity(entity, {"position": entity})
        
        for i in range(len(entities) - 1):
            self.graph.add_relation(entities[i], entities[i+1], "sequence")
        
        # Should find path with max_hops=4
        paths_4 = self.graph.find_paths("A", "E", max_hops=4)
        assert len(paths_4) == 1
        
        # Should NOT find path with max_hops=3
        paths_3 = self.graph.find_paths("A", "E", max_hops=3)
        assert len(paths_3) == 0
    
    def test_get_neighbors_empty(self):
        """Test neighbor retrieval for non-existent entities."""
        neighbors = self.graph.get_neighbors("nonexistent")
        assert neighbors == []
    
    def test_get_neighbors_with_relations(self):
        """Test neighbor retrieval with multiple relations."""
        # Setup network
        self.graph.add_entity("hub", {"type": "central"})
        self.graph.add_entity("node1", {"type": "peripheral"})
        self.graph.add_entity("node2", {"type": "peripheral"})
        self.graph.add_entity("node3", {"type": "peripheral"})
        
        # Connect hub to all nodes
        self.graph.add_relation("hub", "node1", "manages")
        self.graph.add_relation("hub", "node2", "coordinates")
        self.graph.add_relation("hub", "node3", "supervises")
        
        neighbors = self.graph.get_neighbors("hub")
        assert set(neighbors) == {"node1", "node2", "node3"}
    
    def test_empty_graph_queries(self):
        """Test queries on empty graph."""
        assert self.graph.get_entity("anything") is None
        assert self.graph.get_neighbors("anything") == []
        assert self.graph.find_paths("start", "end") == []
    
    def test_self_referential_relation(self):
        """Test entity relating to itself."""
        self.graph.add_entity("recursive", {"type": "self-loop"})
        self.graph.add_relation("recursive", "recursive", "self_reference")
        
        neighbors = self.graph.get_neighbors("recursive")
        assert "recursive" in neighbors
        
        # Should find self-path
        paths = self.graph.find_paths("recursive", "recursive", max_hops=1)
        assert len(paths) >= 1
    
    def test_large_graph_performance(self):
        """Test BFS performance on larger graph structure."""
        # Create star topology: central node connected to 20 nodes
        self.graph.add_entity("center", {"type": "hub"})
        
        for i in range(20):
            node_id = f"spoke_{i}"
            self.graph.add_entity(node_id, {"index": i})
            self.graph.add_relation("center", node_id, "connects")
        
        # All spokes should be reachable in 1 hop
        for i in range(20):
            spoke_id = f"spoke_{i}"
            paths = self.graph.find_paths("center", spoke_id, max_hops=1)
            assert len(paths) == 1
            assert paths[0] == ["center", spoke_id]
        
        # Verify total neighbors
        neighbors = self.graph.get_neighbors("center")
        assert len(neighbors) == 20
    
    def test_disconnected_components(self):
        """Test path finding across disconnected graph components."""
        # Create two separate components
        # Component 1: A -> B
        self.graph.add_entity("A", {"component": 1})
        self.graph.add_entity("B", {"component": 1})
        self.graph.add_relation("A", "B", "connected")
        
        # Component 2: X -> Y  
        self.graph.add_entity("X", {"component": 2})
        self.graph.add_entity("Y", {"component": 2})
        self.graph.add_relation("X", "Y", "connected")
        
        # Should find paths within components
        paths_ab = self.graph.find_paths("A", "B", max_hops=1)
        assert len(paths_ab) == 1
        
        paths_xy = self.graph.find_paths("X", "Y", max_hops=1)
        assert len(paths_xy) == 1
        
        # Should NOT find paths across components
        paths_ax = self.graph.find_paths("A", "X", max_hops=5)
        assert len(paths_ax) == 0
        
        paths_ay = self.graph.find_paths("A", "Y", max_hops=5)
        assert len(paths_ay) == 0
