"""
Enhanced Main Application with Zero-Trust, Orchestration, and Knowledge Graph
"""
from __future__ import annotations
import asyncio
import os
from contextlib import asynccontextmanager
from typing import Dict, Any

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app, Counter
import uvicorn

# Enhanced Core Components
from apps.backend.app.api.middleware.zero_trust import create_zero_trust_middleware
from apps.backend.app.api.routers.enhanced_core import create_enhanced_api_router
from apps.backend.core.agents.orchestrator import (
import call_next
import edge
import event
import len
import node
import print
import request
    create_orchestrator, create_default_team, AgentOrchestrator
)
from apps.backend.core.knowledge.graph_service import (
    create_knowledge_graph_service, KnowledgeGraphService,
    KnowledgeNode, NodeType, KnowledgeEdge, EdgeType, TemporalEvent
)
from apps.backend.core.events.outbox import OutboxService
from apps.backend.core.events.domain import DomainEvent


# Global instances (in production, use proper DI container)
orchestrator: AgentOrchestrator = None
knowledge_graph: KnowledgeGraphService = None
outbox_service: OutboxService = None


# Prometheus metrics
app_startup_total = Counter("zeta_app_startup_total", "Application startup count")
app_requests_total = Counter(
    "zeta_app_requests_total", 
    "Total application requests", 
    ["method", "endpoint"]
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    global orchestrator, knowledge_graph, outbox_service
    
    # Startup
    print("🚀 Starting Enhanced Zeta Core...")
    
    # Initialize services
    outbox_service = OutboxService()
    orchestrator = create_orchestrator(outbox_service)
    knowledge_graph = create_knowledge_graph_service()
    
    # Create and register default agent teams
    default_team = create_default_team("default", "Default Agent Team")
    orchestrator.register_team(default_team)
    
    # Create sample knowledge graph data
    await setup_sample_knowledge_graph()
    
    # Start orchestrator background processing
    orchestrator_task = asyncio.create_task(orchestrator.start())
    
    # Record startup
    app_startup_total.inc()
    print("✅ Enhanced Zeta Core started successfully")
    
    yield  # Application runs here
    
    # Shutdown
    print("🛑 Shutting down Enhanced Zeta Core...")
    
    # Stop orchestrator
    await orchestrator.stop()
    orchestrator_task.cancel()
    
    # Cleanup
    print("✅ Enhanced Zeta Core shutdown complete")


async def setup_sample_knowledge_graph():
    """Setup sample knowledge graph data for testing"""
    global knowledge_graph
    
    if not knowledge_graph:
        return
    
    # Create sample nodes
    nodes = [
        KnowledgeNode("ai_ml", NodeType.CONCEPT, "Artificial Intelligence", {
            "description": "The simulation of human intelligence in machines",
            "domain": "technology"
        }),
        KnowledgeNode("neural_nets", NodeType.CONCEPT, "Neural Networks", {
            "description": "Computing systems inspired by biological neural networks",
            "domain": "technology"
        }),
        KnowledgeNode("python_guide", NodeType.DOCUMENT, "Python Programming Guide", {
            "type": "tutorial",
            "language": "python",
            "difficulty": "beginner"
        }),
        KnowledgeNode("user_admin", NodeType.USER, "System Administrator", {
            "role": "admin",
            "experience": "expert"
        })
    ]
    
    for node in nodes:
        knowledge_graph.add_node(node)
    
    # Create sample edges
    edges = [
        KnowledgeEdge("rel_1", "neural_nets", "ai_ml", EdgeType.PART_OF, weight=0.9),
        KnowledgeEdge("rel_2", "python_guide", "ai_ml", EdgeType.RELATED_TO, weight=0.7),
        KnowledgeEdge("rel_3", "user_admin", "ai_ml", EdgeType.REFERENCES, weight=0.6)
    ]
    
    for edge in edges:
        knowledge_graph.add_edge(edge)
    
    # Add sample temporal events
    events = [
        TemporalEvent(
            "evt_1", 
            datetime.utcnow(), 
            "query", 
            "user_admin",
            {"query": "What is machine learning?", "context": "learning"}
        ),
        TemporalEvent(
            "evt_2",
            datetime.utcnow(),
            "document_access",
            "user_admin", 
            {"document": "python_guide", "action": "read", "duration": 120}
        )
    ]
    
    for event in events:
        knowledge_graph.add_temporal_event(event)
    
    print(f"📊 Knowledge graph initialized with {len(knowledge_graph.nodes)} nodes and {len(knowledge_graph.edges)} edges")


def create_enhanced_app() -> FastAPI:
    """Create the enhanced FastAPI application"""
    
    # Create FastAPI app with lifespan
    app = FastAPI(
        title="Enhanced Zeta Core API",
        description="Zero-Trust Security, AI Agent Orchestration, and Knowledge Graph",
        version="2.0.0",
        lifespan=lifespan
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure appropriately for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Add Zero-Trust middleware (with feature flag)
    ENABLE_ZERO_TRUST = os.getenv("ENABLE_ZERO_TRUST", "true").lower() == "true"
    if ENABLE_ZERO_TRUST:
        JWT_SECRET = os.getenv("JWT_SECRET", "your-secret-key-change-in-production")
        zero_trust_middleware = create_zero_trust_middleware(JWT_SECRET)
        app.add_middleware(zero_trust_middleware)
        print("🔒 Zero-Trust middleware enabled")
    else:
        print("⚠️  Zero-Trust middleware disabled")
    
    # Add request tracking middleware
    @app.middleware("http")
    async def track_requests(request: Request, call_next):
        """Track requests for metrics"""
        response = await call_next(request)
        
        # Record metrics
        app_requests_total.labels(
            method=request.method,
            endpoint=request.url.path
        ).inc()
        
        return response
    
    # Include enhanced API router
    enhanced_router = create_enhanced_api_router()
    app.include_router(enhanced_router)
    
    # Add Prometheus metrics endpoint
    metrics_app = make_asgi_app()
    app.mount("/metrics", metrics_app)
    
    # Health check endpoint
    @app.get("/health")
    async def health_check():
        """Health check endpoint"""
        return {
            "status": "healthy",
            "services": {
                "orchestrator": "running" if orchestrator and orchestrator.running else "stopped",
                "knowledge_graph": "active" if knowledge_graph else "inactive",
                "outbox_service": "active" if outbox_service else "inactive"
            },
            "timestamp": datetime.utcnow().isoformat()
        }
    
    # Enhanced status endpoint
    @app.get("/api/v1/status")
    async def enhanced_status():
        """Enhanced system status"""
        global orchestrator, knowledge_graph
        
        status = {
            "system": "Enhanced Zeta Core",
            "version": "2.0.0",
            "timestamp": datetime.utcnow().isoformat(),
            "components": {
                "zero_trust": {
                    "enabled": ENABLE_ZERO_TRUST,
                    "status": "active" if ENABLE_ZERO_TRUST else "disabled"
                },
                "agent_orchestrator": {
                    "status": "running" if orchestrator and orchestrator.running else "stopped",
                    "teams": len(orchestrator.teams) if orchestrator else 0,
                    "queued_tasks": len(orchestrator.task_queue) if orchestrator else 0
                },
                "knowledge_graph": {
                    "status": "active" if knowledge_graph else "inactive",
                    "nodes": len(knowledge_graph.nodes) if knowledge_graph else 0,
                    "edges": len(knowledge_graph.edges) if knowledge_graph else 0,
                    "temporal_events": len(knowledge_graph.temporal_events) if knowledge_graph else 0
                },
                "event_outbox": {
                    "status": "active" if outbox_service else "inactive"
                }
            },
            "features": {
                "zero_trust_security": ENABLE_ZERO_TRUST,
                "ai_agent_orchestration": True,
                "knowledge_graph": True,
                "temporal_memory": True,
                "event_sourcing": True,
                "prometheus_metrics": True,
                "websocket_support": True
            }
        }
        
        return status
    
    return app


# Create the app instance
app = create_enhanced_app()


# Development server
if __name__ == "__main__":
    import datetime
    
    print("🔥 Starting Enhanced Zeta Core Development Server...")
    uvicorn.run(
        "enhanced_main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
