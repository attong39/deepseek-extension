"""
AI Agent Orchestration with Event Sourcing and Domain Events
"""
from __future__ import annotations
from typing import Dict, List, Optional, Any, Protocol, runtime_checkable
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
import uuid
import asyncio
from concurrent.futures import ThreadPoolExecutor
import json

from pydantic import BaseModel, Field
from prometheus_client import Counter, Histogram, Gauge
from sqlmodel import SQLModel, Field as SQLField, select

from apps.backend.core.events.domain import DomainEvent
from apps.backend.core.events.outbox import OutboxService
import Exception
import ValueError
import agents
import all
import bool
import dict
import e
import enumerate
import float
import i
import int
import isinstance
import len
import list
import name
import orchestrator
import outbox_service
import print
import property
import r
import self
import str
import sum
import t
import task
import task_type
import team_id


# Prometheus metrics
agent_executions_total = Counter(
    "zeta_agent_executions_total",
    "Total agent executions",
    ["agent_type", "status", "team_id"]
)

agent_execution_duration = Histogram(
    "zeta_agent_execution_duration_seconds", 
    "Agent execution duration",
    ["agent_type"]
)

active_agent_teams = Gauge(
    "zeta_active_agent_teams",
    "Number of active agent teams"
)

agent_tasks_queued = Gauge(
    "zeta_agent_tasks_queued",
    "Number of queued agent tasks"
)


class AgentStatus(str, Enum):
    """Agent execution status"""
    IDLE = "idle"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TaskPriority(str, Enum):
    """Task priority levels"""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class AgentContext:
    """Context passed to agents during execution"""
    task_id: str
    team_id: str
    user_id: str
    parameters: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    trace_id: str = field(default_factory=lambda: str(uuid.uuid4()))


@dataclass 
class AgentResult:
    """Result from agent execution"""
    agent_id: str
    status: AgentStatus
    output: Any = None
    error: Optional[str] = None
    execution_time: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)


@runtime_checkable
class Agent(Protocol):
    """Protocol for AI agents"""
    
    @property
    def agent_id(self) -> str:
        """Unique agent identifier"""
        ...
    
    @property
    def agent_type(self) -> str:
        """Agent type/category"""
        ...
    
    @property
    def capabilities(self) -> List[str]:
        """List of agent capabilities"""
        ...
    
    async def execute(self, context: AgentContext) -> AgentResult:
        """Execute agent with given context"""
        ...
    
    async def can_handle(self, task_type: str, parameters: Dict[str, Any]) -> bool:
        """Check if agent can handle the task"""
        ...


class AgentTask(BaseModel):
    """Represents a task for agent execution"""
    task_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    team_id: str
    task_type: str
    parameters: Dict[str, Any] = Field(default_factory=dict)
    priority: TaskPriority = TaskPriority.NORMAL
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    scheduled_at: Optional[datetime] = None
    max_retries: int = 3
    retry_count: int = 0
    timeout_seconds: int = 300
    metadata: Dict[str, Any] = Field(default_factory=dict)


class AgentTeam:
    """Collection of agents working together"""
    
    def __init__(
        self, 
        team_id: str,
        name: str,
        agents: List[Agent] = None,
        orchestrator: 'AgentOrchestrator' = None
    ):
        self.team_id = team_id
        self.name = name
        self.agents = agents or []
        self.orchestrator = orchestrator
        self.status = AgentStatus.IDLE
        self.active_tasks: Dict[str, AgentTask] = {}
        self.task_history: List[AgentTask] = []
        
    def add_agent(self, agent: Agent) -> None:
        """Add agent to team"""
        if agent not in self.agents:
            self.agents.append(agent)
    
    def remove_agent(self, agent_id: str) -> bool:
        """Remove agent from team"""
        for i, agent in enumerate(self.agents):
            if agent.agent_id == agent_id:
                del self.agents[i]
                return True
        return False
    
    def get_capable_agents(self, task_type: str, parameters: Dict[str, Any]) -> List[Agent]:
        """Get agents capable of handling the task"""
        capable = []
        for agent in self.agents:
            # This would be async in real implementation
            if task_type in agent.capabilities:
                capable.append(agent)
        return capable
    
    async def execute_task(self, task: AgentTask) -> List[AgentResult]:
        """Execute task using team agents"""
        self.active_tasks[task.task_id] = task
        self.status = AgentStatus.RUNNING
        
        try:
            # Find capable agents
            capable_agents = self.get_capable_agents(task.task_type, task.parameters)
            
            if not capable_agents:
                raise ValueError(f"No agents capable of handling task type: {task.task_type}")
            
            # Create execution context
            context = AgentContext(
                task_id=task.task_id,
                team_id=self.team_id,
                user_id=task.metadata.get("user_id", "system"),
                parameters=task.parameters,
                metadata=task.metadata
            )
            
            # Execute with capable agents (parallel execution)
            results = []
            start_time = datetime.now(timezone.utc)
            
            try:
                # Use first capable agent for now (could be enhanced for parallel/consensus)
                agent = capable_agents[0]
                result = await asyncio.wait_for(
                    agent.execute(context),
                    timeout=task.timeout_seconds
                )
                results.append(result)
                
                # Record metrics
                execution_time = (datetime.now(timezone.utc) - start_time).total_seconds()
                agent_execution_duration.labels(agent_type=agent.agent_type).observe(execution_time)
                agent_executions_total.labels(
                    agent_type=agent.agent_type,
                    status=result.status.value,
                    team_id=self.team_id
                ).inc()
                
            except asyncio.TimeoutError:
                result = AgentResult(
                    agent_id=capable_agents[0].agent_id,
                    status=AgentStatus.FAILED,
                    error=f"Task timed out after {task.timeout_seconds} seconds"
                )
                results.append(result)
            
            # Emit domain event
            if self.orchestrator:
                await self.orchestrator.emit_task_completed_event(task, results)
            
            # Move to history
            self.task_history.append(task)
            del self.active_tasks[task.task_id]
            
            return results
            
        finally:
            self.status = AgentStatus.IDLE if not self.active_tasks else AgentStatus.RUNNING


class AgentOrchestrator:
    """Orchestrates multiple agent teams and manages task distribution"""
    
    def __init__(self, outbox_service: OutboxService = None):
        self.teams: Dict[str, AgentTeam] = {}
        self.task_queue: List[AgentTask] = []
        self.executor = ThreadPoolExecutor(max_workers=10)
        self.outbox_service = outbox_service
        self.running = False
        
    def register_team(self, team: AgentTeam) -> None:
        """Register an agent team"""
        team.orchestrator = self
        self.teams[team.team_id] = team
        active_agent_teams.set(len(self.teams))
    
    def unregister_team(self, team_id: str) -> bool:
        """Unregister an agent team"""
        if team_id in self.teams:
            del self.teams[team_id]
            active_agent_teams.set(len(self.teams))
            return True
        return False
    
    async def submit_task(self, task: AgentTask) -> str:
        """Submit task for execution"""
        # Validate team exists
        if task.team_id not in self.teams:
            raise ValueError(f"Team not found: {task.team_id}")
        
        # Add to queue
        self.task_queue.append(task)
        agent_tasks_queued.set(len(self.task_queue))
        
        # Emit domain event
        await self.emit_task_submitted_event(task)
        
        return task.task_id
    
    async def execute_task_immediately(self, task: AgentTask) -> List[AgentResult]:
        """Execute task immediately without queueing"""
        if task.team_id not in self.teams:
            raise ValueError(f"Team not found: {task.team_id}")
        
        team = self.teams[task.team_id]
        return await team.execute_task(task)
    
    async def start(self) -> None:
        """Start the orchestrator task processing loop"""
        self.running = True
        while self.running:
            try:
                await self._process_task_queue()
                await asyncio.sleep(1)  # Process every second
            except Exception as e:
                print(f"Error in orchestrator: {e}")
                await asyncio.sleep(5)  # Wait longer on error
    
    async def stop(self) -> None:
        """Stop the orchestrator"""
        self.running = False
        self.executor.shutdown(wait=True)
    
    async def _process_task_queue(self) -> None:
        """Process pending tasks in queue"""
        if not self.task_queue:
            return
        
        # Sort by priority and creation time
        self.task_queue.sort(key=lambda t: (
            ["critical", "high", "normal", "low"].index(t.priority.value),
            t.created_at
        ))
        
        # Process tasks that are ready
        ready_tasks = []
        now = datetime.now(timezone.utc)
        
        for task in self.task_queue[:]:
            if task.scheduled_at is None or task.scheduled_at <= now:
                ready_tasks.append(task)
                self.task_queue.remove(task)
        
        agent_tasks_queued.set(len(self.task_queue))
        
        # Execute ready tasks
        for task in ready_tasks:
            try:
                team = self.teams[task.team_id]
                asyncio.create_task(team.execute_task(task))
            except Exception as e:
                print(f"Error executing task {task.task_id}: {e}")
                # Could implement retry logic here
    
    async def emit_task_submitted_event(self, task: AgentTask) -> None:
        """Emit domain event when task is submitted"""
        event = DomainEvent(
            event_type="agent_task_submitted",
            aggregate_id=task.task_id,
            data={
                "task_id": task.task_id,
                "team_id": task.team_id,
                "task_type": task.task_type,
                "priority": task.priority.value,
                "parameters": task.parameters,
                "metadata": task.metadata
            },
            metadata={
                "source": "agent_orchestrator",
                "version": "1.0"
            }
        )
        
        if self.outbox_service:
            await self.outbox_service.add_event(event)
    
    async def emit_task_completed_event(self, task: AgentTask, results: List[AgentResult]) -> None:
        """Emit domain event when task is completed"""
        event = DomainEvent(
            event_type="agent_task_completed",
            aggregate_id=task.task_id,
            data={
                "task_id": task.task_id,
                "team_id": task.team_id,
                "task_type": task.task_type,
                "results": [
                    {
                        "agent_id": r.agent_id,
                        "status": r.status.value,
                        "execution_time": r.execution_time,
                        "error": r.error,
                        "metadata": r.metadata
                    }
                    for r in results
                ],
                "total_execution_time": sum(r.execution_time for r in results),
                "success": all(r.status == AgentStatus.COMPLETED for r in results)
            },
            metadata={
                "source": "agent_orchestrator", 
                "version": "1.0"
            }
        )
        
        if self.outbox_service:
            await self.outbox_service.add_event(event)
    
    def get_team_status(self, team_id: str) -> Optional[Dict[str, Any]]:
        """Get status of a specific team"""
        if team_id not in self.teams:
            return None
        
        team = self.teams[team_id]
        return {
            "team_id": team.team_id,
            "name": team.name,
            "status": team.status.value,
            "agent_count": len(team.agents),
            "active_tasks": len(team.active_tasks),
            "agents": [
                {
                    "agent_id": agent.agent_id,
                    "agent_type": agent.agent_type,
                    "capabilities": agent.capabilities
                }
                for agent in team.agents
            ]
        }
    
    def get_all_teams_status(self) -> List[Dict[str, Any]]:
        """Get status of all teams"""
        return [
            self.get_team_status(team_id) 
            for team_id in self.teams.keys()
        ]


# Example agent implementations
class CodeAnalysisAgent:
    """Agent for code analysis tasks"""
    
    def __init__(self):
        self.agent_id = f"code_analysis_{uuid.uuid4().hex[:8]}"
        self.agent_type = "code_analysis"
        self.capabilities = ["analyze_code", "find_bugs", "suggest_improvements"]
    
    async def execute(self, context: AgentContext) -> AgentResult:
        """Execute code analysis"""
        start_time = datetime.now(timezone.utc)
        
        try:
            # Simulate code analysis
            code = context.parameters.get("code", "")
            if not code:
                return AgentResult(
                    agent_id=self.agent_id,
                    status=AgentStatus.FAILED,
                    error="No code provided for analysis"
                )
            
            # Mock analysis result
            await asyncio.sleep(0.1)  # Simulate processing
            
            analysis_result = {
                "lines_of_code": len(code.split('\n')),
                "complexity_score": 0.7,
                "suggestions": [
                    "Consider adding type hints",
                    "Add docstrings to functions"
                ],
                "issues": []
            }
            
            execution_time = (datetime.now(timezone.utc) - start_time).total_seconds()
            
            return AgentResult(
                agent_id=self.agent_id,
                status=AgentStatus.COMPLETED,
                output=analysis_result,
                execution_time=execution_time,
                metadata={"analysis_type": "static"}
            )
            
        except Exception as e:
            execution_time = (datetime.now(timezone.utc) - start_time).total_seconds()
            return AgentResult(
                agent_id=self.agent_id,
                status=AgentStatus.FAILED,
                error=str(e),
                execution_time=execution_time
            )
    
    async def can_handle(self, task_type: str, parameters: Dict[str, Any]) -> bool:
        """Check if this agent can handle the task"""
        return task_type in self.capabilities


class DataProcessingAgent:
    """Agent for data processing tasks"""
    
    def __init__(self):
        self.agent_id = f"data_processing_{uuid.uuid4().hex[:8]}"
        self.agent_type = "data_processing"
        self.capabilities = ["process_data", "transform_data", "validate_data"]
    
    async def execute(self, context: AgentContext) -> AgentResult:
        """Execute data processing"""
        start_time = datetime.now(timezone.utc)
        
        try:
            # Simulate data processing
            data = context.parameters.get("data", [])
            operation = context.parameters.get("operation", "transform")
            
            # Mock processing
            await asyncio.sleep(0.2)  # Simulate processing
            
            result = {
                "input_count": len(data) if isinstance(data, list) else 1,
                "output_count": len(data) if isinstance(data, list) else 1,
                "operation": operation,
                "processed_data": data  # In real implementation, this would be processed
            }
            
            execution_time = (datetime.now(timezone.utc) - start_time).total_seconds()
            
            return AgentResult(
                agent_id=self.agent_id,
                status=AgentStatus.COMPLETED,
                output=result,
                execution_time=execution_time,
                metadata={"operation_type": operation}
            )
            
        except Exception as e:
            execution_time = (datetime.now(timezone.utc) - start_time).total_seconds()
            return AgentResult(
                agent_id=self.agent_id,
                status=AgentStatus.FAILED,
                error=str(e),
                execution_time=execution_time
            )
    
    async def can_handle(self, task_type: str, parameters: Dict[str, Any]) -> bool:
        """Check if this agent can handle the task"""
        return task_type in self.capabilities


# Factory functions
def create_orchestrator(outbox_service: OutboxService = None) -> AgentOrchestrator:
    """Create configured agent orchestrator"""
    return AgentOrchestrator(outbox_service=outbox_service)


def create_default_team(team_id: str, name: str) -> AgentTeam:
    """Create a team with default agents"""
    team = AgentTeam(team_id=team_id, name=name)
    
    # Add default agents
    team.add_agent(CodeAnalysisAgent())
    team.add_agent(DataProcessingAgent())
    
    return team
