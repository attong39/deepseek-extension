"""
Enhanced API Routers for Zero-Trust, Agent Orchestration, and Knowledge Graph
"""
from __future__ import annotations
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
import uuid

from fastapi import APIRouter, HTTPException, Depends, Request, WebSocket, WebSocketDisconnect
from pydantic import BaseModel, Field
from prometheus_client import Counter, Histogram
import asyncio
import json

from apps.backend.core.security.zero_trust.policy import Subject, get_resource_policy
from apps.backend.core.agents.orchestrator import (
import Exception
import ValueError
import bool
import current_user
import dict
import e
import enhancement_request
import float
import hasattr
import int
import kg_service
import len
import node_type
import orchestrator
import query_request
import r
import request
import request_data
import str
import task_request
import team_id
import user_id
import websocket
    AgentOrchestrator, AgentTask, TaskPriority, AgentTeam, 
    create_orchestrator, create_default_team
)
from apps.backend.core.knowledge.graph_service import (
    KnowledgeGraphService, RetrievalContext, KnowledgeNode, NodeType,
    create_knowledge_graph_service
)
from apps.backend.core.events.outbox import OutboxService


# Prometheus metrics
api_requests_total = Counter(
    "zeta_api_requests_total",
    "Total API requests",
    ["endpoint", "method", "status"]
)

api_request_duration = Histogram(
    "zeta_api_request_duration_seconds",
    "API request duration",
    ["endpoint"]
)

websocket_connections = Counter(
    "zeta_websocket_connections_total",
    "Total WebSocket connections",
    ["endpoint", "status"]
)


# Request/Response Models
class SecurityPolicyRequest(BaseModel):
    """Request for security policy evaluation"""
    resource_path: str
    action: str
    context: Dict[str, Any] = Field(default_factory=dict)


class SecurityPolicyResponse(BaseModel):
    """Response from security policy evaluation"""
    allowed: bool
    risk_level: str
    reasons: List[str]
    required_actions: List[str]
    decision_metadata: Dict[str, Any]


class AgentTaskRequest(BaseModel):
    """Request to create an agent task"""
    team_id: str
    task_type: str
    parameters: Dict[str, Any] = Field(default_factory=dict)
    priority: TaskPriority = TaskPriority.NORMAL
    timeout_seconds: int = 300
    metadata: Dict[str, Any] = Field(default_factory=dict)


class AgentTaskResponse(BaseModel):
    """Response from agent task creation"""
    task_id: str
    status: str
    message: str


class KnowledgeQueryRequest(BaseModel):
    """Request for knowledge graph query"""
    query: str
    query_type: str = "bfs_path"
    parameters: Dict[str, Any] = Field(default_factory=dict)


class KnowledgeQueryResponse(BaseModel):
    """Response from knowledge graph query"""
    results: Any
    metadata: Dict[str, Any]
    execution_time: float


class RAGEnhancementRequest(BaseModel):
    """Request for RAG enhancement"""
    query: str
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    max_results: int = 10
    temporal_window_hours: int = 24
    include_related: bool = True
    boost_factors: Dict[str, float] = Field(default_factory=dict)


# Dependency injection
def get_orchestrator() -> AgentOrchestrator:
    """Get agent orchestrator instance"""
    # In production, this would be from DI container
    return create_orchestrator()


def get_knowledge_graph() -> KnowledgeGraphService:
    """Get knowledge graph service instance"""
    # In production, this would be from DI container
    return create_knowledge_graph_service()


def get_current_user(request: Request) -> Subject:
    """Extract current user from Zero-Trust context"""
    if hasattr(request.state, 'zero_trust'):
        return request.state.zero_trust['subject']
    
    # Fallback for non-ZT protected endpoints
    return Subject(
        user_id="anonymous",
        roles=["anonymous"],
        attributes={}
    )


# Security API Router
security_router = APIRouter(prefix="/api/v1/security", tags=["security"])


@security_router.post("/policy/evaluate", response_model=SecurityPolicyResponse)
async def evaluate_security_policy(
    request_data: SecurityPolicyRequest,
    current_user: Subject = Depends(get_current_user)
):
    """Evaluate security policy for a resource and action"""
    start_time = datetime.now(timezone.utc)
    
    try:
        from apps.backend.core.security.zero_trust.policy import abac_decide, Environment
        from apps.backend.core.security.zero_trust.risk import risk_engine
        
        # Get resource policy
        resource = get_resource_policy(request_data.resource_path)
        
        # Create environment context
        environment = Environment(
            hour=datetime.now(timezone.utc).hour,
            geo=request_data.context.get("geo"),
            token_age_seconds=int(request_data.context.get("token_age", "0")),
            request_rate=0.0,  # Would be calculated in real implementation
            anomaly_score=0.0,  # Would be from threat detection
            network_trust=True  # Would be calculated
        )
        
        # Make access decision
        decision = abac_decide(current_user, request_data.action, resource, environment)
        
        # Get risk score
        risk_score = risk_engine.compute_risk(current_user.user_id)
        
        return SecurityPolicyResponse(
            allowed=decision.allow,
            risk_level=decision.risk,
            reasons=decision.reasons,
            required_actions=decision.required_actions,
            decision_metadata={
                "resource_type": resource.resource_type,
                "classification": resource.classification,
                "risk_score": risk_score.score,
                "evaluation_time": (datetime.now(timezone.utc) - start_time).total_seconds()
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Policy evaluation failed: {str(e)}")
    finally:
        # Record metrics
        duration = (datetime.now(timezone.utc) - start_time).total_seconds()
        api_request_duration.labels(endpoint="security_policy_evaluate").observe(duration)
        api_requests_total.labels(
            endpoint="security_policy_evaluate",
            method="POST",
            status="200"
        ).inc()


@security_router.get("/risk/{user_id}")
async def get_user_risk_score(
    user_id: str,
    current_user: Subject = Depends(get_current_user)
):
    """Get current risk score for a user"""
    try:
        from apps.backend.core.security.zero_trust.risk import risk_engine
        
        # Check authorization (user can only access their own risk or admin)
        if current_user.user_id != user_id and "admin" not in current_user.roles:
            raise HTTPException(status_code=403, detail="Access denied")
        
        risk_score = risk_engine.compute_risk(user_id)
        
        return {
            "user_id": user_id,
            "risk_score": risk_score.score,
            "risk_label": risk_score.label,
            "factors": risk_score.factors,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Risk calculation failed: {str(e)}")


# Agent Orchestration API Router
agents_router = APIRouter(prefix="/api/v1/agents", tags=["agents"])


@agents_router.post("/tasks", response_model=AgentTaskResponse)
async def create_agent_task(
    task_request: AgentTaskRequest,
    orchestrator: AgentOrchestrator = Depends(get_orchestrator),
    current_user: Subject = Depends(get_current_user)
):
    """Create a new agent task"""
    try:
        # Create task
        task = AgentTask(
            team_id=task_request.team_id,
            task_type=task_request.task_type,
            parameters=task_request.parameters,
            priority=task_request.priority,
            timeout_seconds=task_request.timeout_seconds,
            metadata={
                **task_request.metadata,
                "user_id": current_user.user_id,
                "created_by": current_user.user_id
            }
        )
        
        # Submit task
        task_id = await orchestrator.submit_task(task)
        
        return AgentTaskResponse(
            task_id=task_id,
            status="submitted",
            message=f"Task {task_id} submitted to team {task_request.team_id}"
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Task creation failed: {str(e)}")


@agents_router.get("/teams")
async def list_agent_teams(
    orchestrator: AgentOrchestrator = Depends(get_orchestrator),
    current_user: Subject = Depends(get_current_user)
):
    """List all agent teams and their status"""
    try:
        teams_status = orchestrator.get_all_teams_status()
        return {
            "teams": teams_status,
            "total_teams": len(teams_status),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list teams: {str(e)}")


@agents_router.get("/teams/{team_id}")
async def get_team_status(
    team_id: str,
    orchestrator: AgentOrchestrator = Depends(get_orchestrator),
    current_user: Subject = Depends(get_current_user)
):
    """Get detailed status of a specific team"""
    try:
        team_status = orchestrator.get_team_status(team_id)
        if not team_status:
            raise HTTPException(status_code=404, detail=f"Team {team_id} not found")
        
        return team_status
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get team status: {str(e)}")


@agents_router.websocket("/teams/{team_id}/run")
async def run_team_websocket(
    websocket: WebSocket,
    team_id: str,
    orchestrator: AgentOrchestrator = Depends(get_orchestrator)
):
    """WebSocket endpoint for real-time team task execution"""
    await websocket.accept()
    websocket_connections.labels(endpoint="team_run", status="connected").inc()
    
    try:
        # Verify team exists
        team_status = orchestrator.get_team_status(team_id)
        if not team_status:
            await websocket.send_json({
                "error": f"Team {team_id} not found",
                "timestamp": datetime.now(timezone.utc).isoformat()
            })
            return
        
        await websocket.send_json({
            "status": "connected",
            "team_id": team_id,
            "message": f"Connected to team {team_id}",
            "timestamp": datetime.now(timezone.utc).isoformat()
        })
        
        while True:
            try:
                # Receive task from client
                data = await websocket.receive_json()
                
                if data.get("type") == "execute_task":
                    # Create and execute task immediately
                    task = AgentTask(
                        team_id=team_id,
                        task_type=data.get("task_type", "process_data"),
                        parameters=data.get("parameters", {}),
                        priority=TaskPriority.HIGH,  # WebSocket tasks are high priority
                        metadata={
                            "source": "websocket",
                            "connection_id": str(uuid.uuid4())
                        }
                    )
                    
                    # Send task started notification
                    await websocket.send_json({
                        "type": "task_started",
                        "task_id": task.task_id,
                        "timestamp": datetime.now(timezone.utc).isoformat()
                    })
                    
                    # Execute task
                    results = await orchestrator.execute_task_immediately(task)
                    
                    # Send results
                    await websocket.send_json({
                        "type": "task_completed",
                        "task_id": task.task_id,
                        "results": [
                            {
                                "agent_id": r.agent_id,
                                "status": r.status.value,
                                "output": r.output,
                                "error": r.error,
                                "execution_time": r.execution_time
                            }
                            for r in results
                        ],
                        "timestamp": datetime.now(timezone.utc).isoformat()
                    })
                
                elif data.get("type") == "get_status":
                    # Send current team status
                    current_status = orchestrator.get_team_status(team_id)
                    await websocket.send_json({
                        "type": "status_update",
                        "team_status": current_status,
                        "timestamp": datetime.now(timezone.utc).isoformat()
                    })
                
            except WebSocketDisconnect:
                break
            except Exception as e:
                await websocket.send_json({
                    "type": "error",
                    "error": str(e),
                    "timestamp": datetime.now(timezone.utc).isoformat()
                })
    
    except WebSocketDisconnect:
        pass
    finally:
        websocket_connections.labels(endpoint="team_run", status="disconnected").inc()


# Knowledge Graph API Router
knowledge_router = APIRouter(prefix="/api/v1/knowledge", tags=["knowledge"])


@knowledge_router.post("/query", response_model=KnowledgeQueryResponse)
async def query_knowledge_graph(
    query_request: KnowledgeQueryRequest,
    kg_service: KnowledgeGraphService = Depends(get_knowledge_graph),
    current_user: Subject = Depends(get_current_user)
):
    """Query the knowledge graph"""
    start_time = datetime.now(timezone.utc)
    
    try:
        if query_request.query_type == "bfs_path":
            # BFS path query
            start_id = query_request.parameters.get("start_id")
            end_id = query_request.parameters.get("end_id")
            max_depth = query_request.parameters.get("max_depth", 6)
            
            if not start_id or not end_id:
                raise HTTPException(status_code=400, detail="start_id and end_id required for BFS path query")
            
            result = kg_service.bfs_shortest_path(start_id, end_id, max_depth)
            
            return KnowledgeQueryResponse(
                results=result.dict() if result else None,
                metadata={
                    "query_type": "bfs_path",
                    "parameters": query_request.parameters
                },
                execution_time=(datetime.now(timezone.utc) - start_time).total_seconds()
            )
        
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported query type: {query_request.query_type}")
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Knowledge query failed: {str(e)}")


@knowledge_router.post("/rag/enhance")
async def enhance_rag_retrieval(
    enhancement_request: RAGEnhancementRequest,
    kg_service: KnowledgeGraphService = Depends(get_knowledge_graph),
    current_user: Subject = Depends(get_current_user)
):
    """Enhance RAG retrieval with knowledge graph context"""
    try:
        # Create retrieval context
        context = RetrievalContext(
            query=enhancement_request.query,
            user_id=enhancement_request.user_id or current_user.user_id,
            session_id=enhancement_request.session_id,
            max_results=enhancement_request.max_results,
            temporal_window_hours=enhancement_request.temporal_window_hours,
            include_related=enhancement_request.include_related,
            boost_factors=enhancement_request.boost_factors
        )
        
        # Get enhancement
        enhancement = kg_service.enhance_rag_retrieval(context)
        
        return {
            "enhancement": enhancement,
            "original_query": enhancement_request.query,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"RAG enhancement failed: {str(e)}")


@knowledge_router.get("/stats")
async def get_knowledge_graph_stats(
    kg_service: KnowledgeGraphService = Depends(get_knowledge_graph),
    current_user: Subject = Depends(get_current_user)
):
    """Get knowledge graph statistics"""
    try:
        # Check if user has admin access
        if "admin" not in current_user.roles:
            raise HTTPException(status_code=403, detail="Admin access required")
        
        stats = {
            "total_nodes": len(kg_service.nodes),
            "total_edges": len(kg_service.edges),
            "temporal_events": len(kg_service.temporal_events),
            "node_types": {
                node_type.value: len(kg_service.type_index[node_type])
                for node_type in NodeType
            }
        }
        
        return stats
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get stats: {str(e)}")


# Combined router
def create_enhanced_api_router() -> APIRouter:
    """Create the combined enhanced API router"""
    main_router = APIRouter()
    
    # Include all sub-routers
    main_router.include_router(security_router)
    main_router.include_router(agents_router)
    main_router.include_router(knowledge_router)
    
    return main_router
