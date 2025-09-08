"""
Agent Team API Router with Production Hardening
==============================================

FastAPI router for agent team management with REST endpoints and WebSocket streaming.
Enhanced with backpressure, heartbeat, rate-limiting for production readiness.
"""

import asyncio
import json
import logging
import time
from contextlib import asynccontextmanager
from typing import List

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException

from apps.backend.core.domain.agents.team import AgentTeam, TeamStatus
from apps.backend.core.use_cases.collaboration.orchestrate_team import AgentTeamOrchestrator, TaskRequest
from apps.backend.app.observability.ws_metrics import (
import Exception
import dict
import e
import event
import len
import list
import max
import pending
import queue
import str
import t
import task
import team_id
import websocket
    ws_connections, 
    ws_messages_total, 
    ws_send_latency_seconds,
    ws_backpressure_total,
    ws_errors_total,
    ws_heartbeat_total
)

logger = logging.getLogger(__name__)

# Production configuration
MAX_QUEUE = 512         # backpressure threshold
SEND_RATE_TPS = 200     # rate limit to prevent client flooding
PING_INTERVAL = 20.0    # heartbeat interval (seconds)
CLIENT_TIMEOUT = 60.0   # close idle connections after this

# Router configuration
router = APIRouter(prefix="/agents", tags=["agents"])

# In-memory storage (replace with Redis/DB in production)
_TEAM_STORE: dict[str, AgentTeam] = {}
_ORCHESTRATOR = AgentTeamOrchestrator(_TEAM_STORE)

@asynccontextmanager
async def track_ws_connection(route: str):
    """Context manager for tracking WebSocket connection metrics."""
    ws_connections.labels(route=route).inc()
    try:
        yield
    finally:
        ws_connections.labels(route=route).dec()

@router.post("/teams", response_model=AgentTeam)
async def create_team(team: AgentTeam):
    """
    Create a new agent team.
    
    Creates a team with specified agents and workflow configuration.
    Team will be in 'pending' status until execution begins.
    """
    logger.info(f"Creating team {team.id} with {len(team.agents)} agents")
    
    # Validate team doesn't already exist
    if team.id in _TEAM_STORE:
        raise HTTPException(status_code=409, detail=f"Team {team.id} already exists")
    
    # Validate agents list
    if not team.agents:
        raise HTTPException(status_code=400, detail="Team must have at least one agent")
    
    return await _ORCHESTRATOR.create_team(team)

@router.get("/teams", response_model=list[AgentTeam])
async def list_teams():
    """List all agent teams."""
    return await _ORCHESTRATOR.list_teams()

@router.get("/teams/{team_id}", response_model=AgentTeam)
async def get_team(team_id: str):
    """Get specific team by ID."""
    team = await _ORCHESTRATOR.get_team(team_id)
    if not team:
        raise HTTPException(status_code=404, detail=f"Team {team_id} not found")
    return team

@router.delete("/teams/{team_id}")
async def delete_team(team_id: str):
    """Delete a team."""
    if team_id not in _TEAM_STORE:
        raise HTTPException(status_code=404, detail=f"Team {team_id} not found")
    
    # Stop running team if needed
    if _TEAM_STORE[team_id].status == TeamStatus.running:
        await _ORCHESTRATOR.stop_team(team_id)
    
    del _TEAM_STORE[team_id]
    return {"message": f"Team {team_id} deleted"}

@router.post("/teams/{team_id}/stop")
async def stop_team(team_id: str):
    """Stop running team execution."""
    success = await _ORCHESTRATOR.stop_team(team_id)
    if not success:
        raise HTTPException(status_code=400, detail="Team not running or not found")
    return {"message": f"Team {team_id} stopped"}

@router.websocket("/teams/{team_id}/run")
async def ws_run_team(websocket: WebSocket, team_id: str):
    """
    Execute team workflow with production-grade WebSocket streaming.
    
    Features:
    - Backpressure management with queue buffering
    - Rate limiting (200 TPS) to prevent client flooding  
    - Heartbeat ping/pong for connection health
    - Comprehensive metrics and error handling
    """
    route = "/agents/teams/run"
    await websocket.accept()
    
    async with track_ws_connection(route):
        # Initialize backpressure queue and control variables
        queue: asyncio.Queue[str] = asyncio.Queue(MAX_QUEUE)
        stop_event = asyncio.Event()
        last_activity = time.time()
        
        logger.info(f"WebSocket connected for team {team_id}")
        ws_messages_total.labels(route=route, direction="in", event="connect").inc()
        
        async def event_producer():
            """Producer: receives initial request and generates orchestration events."""
            try:
                # Receive single task request from client
                raw_data = await websocket.receive_text()
                ws_messages_total.labels(route=route, direction="in", event="init").inc()
                
                data = json.loads(raw_data)
                logger.info(f"Received task request for team {team_id}: {data}")
                
                # Validate team exists
                team = await _ORCHESTRATOR.get_team(team_id)
                if not team:
                    error_msg = json.dumps({
                        "event": "error",
                        "error": f"Team {team_id} not found",
                        "timestamp": time.time()
                    })
                    await queue.put(error_msg)
                    stop_event.set()
                    return
                
                # Parse and execute workflow
                task_request = TaskRequest(**data)
                
                # Stream orchestration events with backpressure handling
                async for event in _ORCHESTRATOR.run_task(team_id, task_request):
                    event_json = json.dumps(event, separators=(",", ":"))
                    
                    try:
                        # Try immediate queue insertion
                        queue.put_nowait(event_json)
                    except asyncio.QueueFull:
                        # Backpressure strategy: drop non-critical events, keep important ones
                        event_type = event.get("event", "unknown")
                        if event_type not in ["agent.step", "progress.update"]:
                            # Keep critical events (started, completed, error)
                            await queue.put(event_json)
                            ws_backpressure_total.labels(route=route, action="throttled").inc()
                        else:
                            # Drop non-critical events during overload
                            ws_backpressure_total.labels(route=route, action="dropped").inc()
                            logger.warning(f"Dropped event {event_type} due to backpressure")
                
                # Signal completion
                completion_msg = json.dumps({
                    "event": "team.done", 
                    "team_id": team_id,
                    "timestamp": time.time()
                })
                await queue.put(completion_msg)
                stop_event.set()
                
            except WebSocketDisconnect:
                logger.info(f"Client disconnected during execution: {team_id}")
                stop_event.set()
            except Exception as e:
                logger.error(f"Producer error for team {team_id}: {str(e)}")
                ws_errors_total.labels(route=route, error_type="producer").inc()
                error_msg = json.dumps({
                    "event": "error",
                    "error": str(e),
                    "timestamp": time.time()
                })
                try:
                    await queue.put(error_msg)
                except asyncio.QueueFull:
                    pass  # If we can't even queue an error, connection is doomed
                stop_event.set()
        
        async def message_consumer():
            """Consumer: sends queued messages with rate limiting."""
            last_send = 0.0
            min_interval = 1.0 / max(1, SEND_RATE_TPS)  # Rate limit interval
            
            while not (stop_event.is_set() and queue.empty()):
                try:
                    # Get next message with timeout
                    message = await asyncio.wait_for(queue.get(), timeout=1.0)
                except asyncio.TimeoutError:
                    continue
                
                # Rate limiting: ensure minimum interval between sends
                now = time.perf_counter()
                elapsed = now - last_send
                if elapsed < min_interval:
                    await asyncio.sleep(min_interval - elapsed)
                
                # Send message with latency tracking
                send_start = time.perf_counter()
                try:
                    await websocket.send_text(message)
                    
                    # Record metrics
                    send_duration = time.perf_counter() - send_start
                    ws_send_latency_seconds.labels(route=route).observe(send_duration)
                    ws_messages_total.labels(route=route, direction="out", event="data").inc()
                    
                    last_send = time.perf_counter()
                    
                except Exception as e:
                    logger.error(f"Send error for team {team_id}: {str(e)}")
                    ws_errors_total.labels(route=route, error_type="send").inc()
                    break
        
        async def heartbeat_manager():
            """Heartbeat: sends periodic pings and monitors client activity."""
            nonlocal last_activity
            
            while not stop_event.is_set():
                try:
                    # Send ping
                    ping_msg = json.dumps({"type": "ping", "timestamp": time.time()})
                    await websocket.send_text(ping_msg)
                    ws_heartbeat_total.labels(route=route, type="ping_sent").inc()
                    
                    # Check for client timeout
                    if time.time() - last_activity > CLIENT_TIMEOUT:
                        logger.warning(f"Client timeout for team {team_id}")
                        ws_heartbeat_total.labels(route=route, type="timeout").inc()
                        stop_event.set()
                        break
                    
                    await asyncio.sleep(PING_INTERVAL)
                    
                except Exception as e:
                    logger.error(f"Heartbeat error for team {team_id}: {str(e)}")
                    ws_errors_total.labels(route=route, error_type="heartbeat").inc()
                    stop_event.set()
                    break
        
        # Launch concurrent tasks
        tasks = [
            asyncio.create_task(event_producer()),
            asyncio.create_task(message_consumer()),
            asyncio.create_task(heartbeat_manager())
        ]
        
        try:
            # Wait for any task to complete or fail
            done, pending = await asyncio.wait(
                tasks, 
                return_when=asyncio.FIRST_COMPLETED
            )
            
            # Cancel remaining tasks
            for task in pending:
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass
            
            logger.info(f"WebSocket session completed for team {team_id}")
            
        except WebSocketDisconnect:
            logger.info(f"WebSocket disconnected for team {team_id}")
        except Exception as e:
            logger.error(f"WebSocket session error for team {team_id}: {str(e)}")
            ws_errors_total.labels(route=route, error_type="session").inc()
        finally:
            # Cleanup: ensure WebSocket is closed properly
            try:
                if not websocket.client_state.DISCONNECTED:
                    await websocket.close(code=1000)
            except Exception:
                pass  # Connection might already be closed

@router.get("/teams/{team_id}/status")
async def get_team_status(team_id: str):
    """Get team execution status."""
    team = await _ORCHESTRATOR.get_team(team_id)
    if not team:
        raise HTTPException(status_code=404, detail=f"Team {team_id} not found")
    
    return {
        "team_id": team_id,
        "status": team.status,
        "agents": team.agents,
        "workflow": team.workflow.name,
        "last_error": team.last_error
    }

# Health check endpoint
@router.get("/health")
async def health_check():
    """Agent orchestration service health check."""
    return {
        "status": "healthy",
        "active_teams": len(_TEAM_STORE),
        "running_teams": len([t for t in _TEAM_STORE.values() if t.status == TeamStatus.running])
    }
