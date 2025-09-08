"""
Agent Orchestration Metrics
===========================

Prometheus metrics for agent team orchestration and workflow monitoring.
Provides counters, histograms, and gauges for observability and performance tracking.
"""

import logging
import time
from contextlib import contextmanager
from typing import Any

from prometheus_client import Counter, Histogram, Gauge
import Exception
import agent_id
import count
import dict
import e
import endpoint
import entities_count
import error_type
import float
import int
import len
import list
import max
import max_hops
import min
import relations_count
import self
import status
import str
import sum
import team_id
import teams_by_status
import workflow
import workflow_type

logger = logging.getLogger(__name__)

# Agent step execution metrics
agent_steps_total = Counter(
    "zeta_agent_steps_total", 
    "Total number of agent steps executed", 
    ["team_id", "agent_id", "status"]
)

# Team workflow execution latency
team_latency_seconds = Histogram(
    "zeta_team_latency_seconds", 
    "Team workflow execution time in seconds", 
    ["workflow", "status"],
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0, 60.0]
)

# Active teams gauge
active_teams_gauge = Gauge(
    "zeta_active_teams_total",
    "Current number of active teams",
    ["status"]
)

# Agent execution errors
agent_errors_total = Counter(
    "zeta_agent_errors_total",
    "Total number of agent execution errors",
    ["team_id", "agent_id", "error_type"]
)

# Knowledge graph metrics
knowledge_graph_entities = Gauge(
    "zeta_knowledge_graph_entities_total",
    "Total entities in knowledge graph"
)

knowledge_graph_relations = Gauge(
    "zeta_knowledge_graph_relations_total", 
    "Total relations in knowledge graph"
)

# Path discovery metrics
path_discovery_duration = Histogram(
    "zeta_path_discovery_duration_seconds",
    "Time spent discovering knowledge paths",
    ["max_hops"],
    buckets=[0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1.0]
)

# WebSocket connection metrics
websocket_connections_total = Counter(
    "zeta_websocket_connections_total",
    "Total WebSocket connections",
    ["endpoint", "status"]
)

websocket_active_connections = Gauge(
    "zeta_websocket_active_connections",
    "Currently active WebSocket connections",
    ["endpoint"]
)

# Team creation metrics
team_creation_total = Counter(
    "zeta_team_creation_total",
    "Total teams created",
    ["workflow_type"]
)

# Performance metrics
class AgentMetricsCollector:
    """Collector for agent orchestration metrics."""
    
    def __init__(self):
        self._active_teams: dict[str, float] = {}
        self._active_websockets: dict[str, int] = {}
    
    def record_agent_step(self, team_id: str, agent_id: str, status: str = "success"):
        """Record agent step execution."""
        agent_steps_total.labels(team_id=team_id, agent_id=agent_id, status=status).inc()
        logger.debug(f"Recorded agent step: team={team_id}, agent={agent_id}, status={status}")
    
    def record_agent_error(self, team_id: str, agent_id: str, error_type: str):
        """Record agent execution error."""
        agent_errors_total.labels(team_id=team_id, agent_id=agent_id, error_type=error_type).inc()
        logger.warning(f"Recorded agent error: team={team_id}, agent={agent_id}, error={error_type}")
    
    @contextmanager
    def measure_team_latency(self, workflow: str, status: str = "success"):
        """Context manager to measure team execution latency."""
        start_time = time.time()
        try:
            yield
            # Success case
            duration = time.time() - start_time
            team_latency_seconds.labels(workflow=workflow, status=status).observe(duration)
            logger.debug(f"Team latency recorded: workflow={workflow}, duration={duration:.3f}s")
        except Exception as e:
            # Error case
            duration = time.time() - start_time
            team_latency_seconds.labels(workflow=workflow, status="error").observe(duration)
            logger.error(f"Team execution failed: workflow={workflow}, duration={duration:.3f}s, error={e}")
            raise
    
    def update_active_teams(self, teams_by_status: dict[str, int]):
        """Update active teams gauge by status."""
        for status, count in teams_by_status.items():
            active_teams_gauge.labels(status=status).set(count)
    
    def record_team_creation(self, workflow_type: str):
        """Record team creation."""
        team_creation_total.labels(workflow_type=workflow_type).inc()
    
    def track_team_start(self, team_id: str):
        """Track team execution start."""
        self._active_teams[team_id] = time.time()
    
    def track_team_end(self, team_id: str):
        """Track team execution end."""
        if team_id in self._active_teams:
            del self._active_teams[team_id]
    
    @contextmanager
    def measure_path_discovery(self, max_hops: int):
        """Context manager to measure path discovery performance."""
        start_time = time.time()
        try:
            yield
        finally:
            duration = time.time() - start_time
            path_discovery_duration.labels(max_hops=str(max_hops)).observe(duration)
    
    def record_websocket_connection(self, endpoint: str, status: str = "connected"):
        """Record WebSocket connection event."""
        websocket_connections_total.labels(endpoint=endpoint, status=status).inc()
        
        # Update active connections count
        if status == "connected":
            current = self._active_websockets.get(endpoint, 0)
            self._active_websockets[endpoint] = current + 1
        elif status == "disconnected":
            current = self._active_websockets.get(endpoint, 0)
            self._active_websockets[endpoint] = max(0, current - 1)
        
        # Update gauge
        websocket_active_connections.labels(endpoint=endpoint).set(
            self._active_websockets.get(endpoint, 0)
        )
    
    def update_knowledge_graph_stats(self, entities_count: int, relations_count: int):
        """Update knowledge graph statistics."""
        knowledge_graph_entities.set(entities_count)
        knowledge_graph_relations.set(relations_count)
    
    def get_metrics_summary(self) -> dict[str, Any]:
        """Get current metrics summary."""
        return {
            "active_teams": len(self._active_teams),
            "active_websockets": sum(self._active_websockets.values()),
            "websocket_endpoints": list(self._active_websockets.keys()),
            "longest_running_team_seconds": (
                time.time() - min(self._active_teams.values()) 
                if self._active_teams else 0
            )
        }

# Global metrics collector instance
metrics_collector = AgentMetricsCollector()

# Convenience functions for easy metrics recording
def record_agent_step(team_id: str, agent_id: str, status: str = "success"):
    """Record agent step execution (convenience function)."""
    metrics_collector.record_agent_step(team_id, agent_id, status)

def record_agent_error(team_id: str, agent_id: str, error_type: str):
    """Record agent execution error (convenience function)."""
    metrics_collector.record_agent_error(team_id, agent_id, error_type)

def measure_team_latency(workflow: str, status: str = "success"):
    """Measure team execution latency (convenience function)."""
    return metrics_collector.measure_team_latency(workflow, status)

def record_websocket_event(endpoint: str, status: str):
    """Record WebSocket event (convenience function)."""
    metrics_collector.record_websocket_connection(endpoint, status)
