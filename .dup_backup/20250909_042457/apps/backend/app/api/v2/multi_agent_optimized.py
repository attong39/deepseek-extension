import Exception
import TimeoutError
import agent
import agent_type
import agents
import all
import best_agent
import bool
import dep_id
import dict
import e
import float
import from_agent
import int
import len
import list
import max
import property
import registration
import self
import set
import staticmethod
import str
import sub_id
import subtask
import subtask_id
import sum
import task_request
import task_type
import tasks
import user
import websocket
import x
# zeta_vn/app/api/v2/multi_agent_optimized.py
"""
Multi-Agent System v2 - Optimized với Hierarchical Orchestration

Tối ưu hóa:
1. Hierarchical agent coordination với supervisor/worker pattern
2. Dynamic task decomposition và load balancing
3. Inter-agent communication với message queuing
4. Agent capability matching và resource optimization
"""

from __future__ import annotations

import asyncio
import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from enum import Enum
from typing import Any

import networkx as nx
from apps.backend.app.api.v1._common_audit import audit
from apps.backend.app.api.v1._common_cache import acached
from apps.backend.app.api.v1._common_idempotency import idempotency_guard
from apps.backend.app.api.v1._common_security import Role, User, require_roles
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    WebSocket,
    WebSocketDisconnect,
    status,
)
from pydantic import BaseModel, Field

router = APIRouter(prefix="/multi-agent", tags=["MultiAgent-V2-Optimized"])

# === Constants ===

ROUND_NOT_FOUND = "Round not found"
AGENT_NOT_FOUND = "Agent not found"
TASK_NOT_FOUND = "Task not found"

# === Agent Types & Models ===


class AgentType(str, Enum):
    SUPERVISOR = "supervisor"  # High-level orchestrator
    COORDINATOR = "coordinator"  # Mid-level task coordinator
    SPECIALIST = "specialist"  # Domain-specific agent
    WORKER = "worker"  # Basic execution agent
    MONITOR = "monitor"  # System monitoring agent


class AgentCapability(str, Enum):
    REASONING = "reasoning"
    PLANNING = "planning"
    EXECUTION = "execution"
    MONITORING = "monitoring"
    COMMUNICATION = "communication"
    DATA_PROCESSING = "data_processing"
    MODEL_INFERENCE = "model_inference"
    TOOL_USE = "tool_use"


class TaskType(str, Enum):
    ANALYSIS = "analysis"
    GENERATION = "generation"
    CLASSIFICATION = "classification"
    OPTIMIZATION = "optimization"
    COORDINATION = "coordination"
    MONITORING = "monitoring"


class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AgentStatus(str, Enum):
    IDLE = "idle"
    BUSY = "busy"
    OVERLOADED = "overloaded"
    OFFLINE = "offline"
    MAINTENANCE = "maintenance"


class TaskStatus(str, Enum):
    PENDING = "pending"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class AgentMetrics:
    """Real-time agent performance metrics"""

    cpu_usage: float = 0.0
    memory_usage: float = 0.0
    active_tasks: int = 0
    completed_tasks: int = 0
    failed_tasks: int = 0
    avg_task_duration: float = 0.0
    success_rate: float = 1.0
    last_heartbeat: datetime = field(default_factory=datetime.now)


@dataclass
class Agent:
    """Agent definition with capabilities and state"""

    agent_id: str
    agent_type: AgentType
    capabilities: set[AgentCapability]
    max_concurrent_tasks: int
    status: AgentStatus = AgentStatus.IDLE
    current_tasks: set[str] = field(default_factory=set)
    metrics: AgentMetrics = field(default_factory=AgentMetrics)
    supervisor_id: str | None = None
    subordinates: set[str] = field(default_factory=set)

    @property
    def is_available(self) -> bool:
        return (
            self.status == AgentStatus.IDLE
            and len(self.current_tasks) < self.max_concurrent_tasks
        )

    @property
    def load_factor(self) -> float:
        """Current load as ratio of active to max tasks"""
        return len(self.current_tasks) / max(1, self.max_concurrent_tasks)


@dataclass
class Task:
    """Task definition with requirements and state"""

    task_id: str
    task_type: TaskType
    priority: TaskPriority
    required_capabilities: set[AgentCapability]
    estimated_duration: timedelta
    input_data: dict[str, Any]
    status: TaskStatus = TaskStatus.PENDING
    assigned_agent_id: str | None = None
    created_at: datetime = field(default_factory=datetime.now)
    started_at: datetime | None = None
    completed_at: datetime | None = None
    result: dict[str, Any] | None = None
    error_message: str | None = None
    dependencies: set[str] = field(default_factory=set)  # Task IDs this depends on
    subtasks: set[str] = field(default_factory=set)  # Generated subtasks
    parent_task_id: str | None = None


class AgentRegistration(BaseModel):
    agent_type: AgentType
    capabilities: list[AgentCapability]
    max_concurrent_tasks: int = Field(default=5, ge=1, le=100)
    supervisor_id: str | None = None


class TaskRequest(BaseModel):
    task_type: TaskType
    priority: TaskPriority = TaskPriority.MEDIUM
    required_capabilities: list[AgentCapability]
    estimated_duration_minutes: int = Field(default=10, ge=1, le=1440)
    input_data: dict[str, Any]
    dependencies: list[str] = Field(default_factory=list)


class TaskAssignment(BaseModel):
    task_id: str
    agent_id: str
    estimated_completion: datetime


class AgentMessage(BaseModel):
    from_agent: str
    to_agent: str
    message_type: str
    content: dict[str, Any]
    timestamp: datetime = Field(default_factory=datetime.now)


# === Task Decomposition Engine ===


class TaskDecomposer:
    """Intelligent task decomposition for complex requests"""

    @staticmethod
    def decompose_complex_task(task: Task) -> list[Task]:
        """Break down complex tasks into manageable subtasks"""
        subtasks = []

        if task.task_type == TaskType.ANALYSIS:
            # Decompose analysis into data prep + processing + reporting
            subtasks.extend(
                [
                    Task(
                        task_id=f"{task.task_id}_prep",
                        task_type=TaskType.GENERATION,  # Data preparation
                        priority=task.priority,
                        required_capabilities={AgentCapability.DATA_PROCESSING},
                        estimated_duration=task.estimated_duration * 0.3,
                        input_data=task.input_data,
                        parent_task_id=task.task_id,
                    ),
                    Task(
                        task_id=f"{task.task_id}_process",
                        task_type=TaskType.ANALYSIS,
                        priority=task.priority,
                        required_capabilities={
                            AgentCapability.REASONING,
                            AgentCapability.MODEL_INFERENCE,
                        },
                        estimated_duration=task.estimated_duration * 0.5,
                        input_data=task.input_data,
                        dependencies={f"{task.task_id}_prep"},
                        parent_task_id=task.task_id,
                    ),
                    Task(
                        task_id=f"{task.task_id}_report",
                        task_type=TaskType.GENERATION,
                        priority=task.priority,
                        required_capabilities={AgentCapability.GENERATION},
                        estimated_duration=task.estimated_duration * 0.2,
                        input_data=task.input_data,
                        dependencies={f"{task.task_id}_process"},
                        parent_task_id=task.task_id,
                    ),
                ]
            )

        elif task.task_type == TaskType.OPTIMIZATION:
            # Decompose optimization into search + evaluate + refine
            subtasks.extend(
                [
                    Task(
                        task_id=f"{task.task_id}_search",
                        task_type=TaskType.GENERATION,
                        priority=task.priority,
                        required_capabilities={
                            AgentCapability.REASONING,
                            AgentCapability.PLANNING,
                        },
                        estimated_duration=task.estimated_duration * 0.6,
                        input_data=task.input_data,
                        parent_task_id=task.task_id,
                    ),
                    Task(
                        task_id=f"{task.task_id}_evaluate",
                        task_type=TaskType.ANALYSIS,
                        priority=task.priority,
                        required_capabilities={AgentCapability.REASONING},
                        estimated_duration=task.estimated_duration * 0.3,
                        input_data=task.input_data,
                        dependencies={f"{task.task_id}_search"},
                        parent_task_id=task.task_id,
                    ),
                    Task(
                        task_id=f"{task.task_id}_refine",
                        task_type=TaskType.OPTIMIZATION,
                        priority=task.priority,
                        required_capabilities={
                            AgentCapability.REASONING,
                            AgentCapability.EXECUTION,
                        },
                        estimated_duration=task.estimated_duration * 0.1,
                        input_data=task.input_data,
                        dependencies={f"{task.task_id}_evaluate"},
                        parent_task_id=task.task_id,
                    ),
                ]
            )

        # Update parent task with subtask references
        task.subtasks = {subtask.task_id for subtask in subtasks}

        return subtasks


# === Agent Matching Engine ===


class AgentMatcher:
    """Intelligent agent selection for optimal task assignment"""

    @staticmethod
    def find_best_agent(task: Task, available_agents: list[Agent]) -> Agent | None:
        """Find the best agent for a task using multi-criteria optimization"""
        if not available_agents:
            return None

        candidates = []

        for agent in available_agents:
            if not agent.is_available:
                continue

            # Check capability match
            if not task.required_capabilities.issubset(agent.capabilities):
                continue

            # Calculate fitness score
            score = AgentMatcher._calculate_fitness_score(task, agent)
            candidates.append((agent, score))

        if not candidates:
            return None

        # Return agent with highest score
        return max(candidates, key=lambda x: x[1])[0]

    @staticmethod
    def _calculate_fitness_score(task: Task, agent: Agent) -> float:
        """Calculate fitness score for agent-task pairing"""
        score = 0.0

        # Capability match bonus (exact match vs superset)
        if task.required_capabilities == agent.capabilities:
            score += 10.0  # Perfect match
        else:
            score += 5.0  # Superset match

        # Load factor penalty (prefer less loaded agents)
        score -= agent.load_factor * 5.0

        # Success rate bonus
        score += agent.metrics.success_rate * 3.0

        # Agent type preference for task type
        type_bonus = {
            TaskType.ANALYSIS: {AgentType.SPECIALIST: 2.0, AgentType.WORKER: 1.0},
            TaskType.GENERATION: {AgentType.SPECIALIST: 2.0, AgentType.WORKER: 1.0},
            TaskType.COORDINATION: {
                AgentType.SUPERVISOR: 3.0,
                AgentType.COORDINATOR: 2.0,
            },
            TaskType.MONITORING: {AgentType.MONITOR: 3.0, AgentType.SUPERVISOR: 1.0},
        }
        score += type_bonus.get(task.task_type, {}).get(agent.agent_type, 0.0)

        # Priority urgency factor
        if task.priority == TaskPriority.CRITICAL:
            score += 5.0
        elif task.priority == TaskPriority.HIGH:
            score += 2.0

        return score


# === Message Queue System ===


class MessageQueue:
    """Inter-agent communication message queue"""

    def __init__(self):
        self.queues: dict[str, list[AgentMessage]] = {}
        self.connections: dict[str, WebSocket] = {}

    async def send_message(self, message: AgentMessage):
        """Send message to target agent"""
        if message.to_agent not in self.queues:
            self.queues[message.to_agent] = []

        self.queues[message.to_agent].append(message)

        # If agent is connected via WebSocket, send immediately
        if message.to_agent in self.connections:
            try:
                await self.connections[message.to_agent].send_text(message.json())
            except Exception:
                # Connection might be stale
                del self.connections[message.to_agent]

    async def get_messages(self, agent_id: str) -> list[AgentMessage]:
        """Get pending messages for agent"""
        messages = self.queues.get(agent_id, [])
        self.queues[agent_id] = []  # Clear after retrieval
        return messages

    def register_connection(self, agent_id: str, websocket: WebSocket):
        """Register WebSocket connection for agent"""
        self.connections[agent_id] = websocket

    def unregister_connection(self, agent_id: str):
        """Unregister WebSocket connection"""
        if agent_id in self.connections:
            del self.connections[agent_id]


# === Hierarchy Management ===


class AgentHierarchy:
    """Manages agent hierarchy and delegation"""

    def __init__(self):
        self.graph = nx.DiGraph()  # Directed graph for hierarchy

    def add_agent(self, agent: Agent):
        """Add agent to hierarchy"""
        self.graph.add_node(agent.agent_id, agent=agent)

        if agent.supervisor_id:
            self.graph.add_edge(agent.supervisor_id, agent.agent_id)

    def get_subordinates(self, agent_id: str) -> list[str]:
        """Get direct subordinates of an agent"""
        return list(self.graph.successors(agent_id))

    def get_supervisor_chain(self, agent_id: str) -> list[str]:
        """Get supervision chain up to root"""
        chain = []
        current = agent_id

        while True:
            predecessors = list(self.graph.predecessors(current))
            if not predecessors:
                break
            supervisor = predecessors[0]  # Assume single supervisor
            chain.append(supervisor)
            current = supervisor

        return chain

    def delegate_task(self, from_agent: str, task: Task) -> str | None:
        """Delegate task down the hierarchy"""
        subordinates = self.get_subordinates(from_agent)

        if not subordinates:
            return None

        # Find best subordinate for the task
        available_subordinates = []
        for sub_id in subordinates:
            if sub_id in agents and agents[sub_id].is_available:
                available_subordinates.append(agents[sub_id])

        AgentMatcher.find_best_agent(task, available_subordinates)
        return best_agent.agent_id if best_agent else None


# === Global State Management ===

agents: dict[str, Agent] = {}
tasks: dict[str, Task] = {}
message_queue = MessageQueue()
hierarchy = AgentHierarchy()
task_dependency_graph = nx.DiGraph()

# === API Endpoints ===


@router.post("/agents/register")
async def register_agent(
    registration: AgentRegistration, user: User = Depends(require_roles(Role.USER))
) -> dict[str, str]:
    """Register new agent in the multi-agent system"""
    agent_id = f"agent_{uuid.uuid4().hex[:8]}"

    await audit(
        "multiagent.agent.register",
        actor=user.sub,
        payload={
            "agent_id": agent_id,
            "agent_type": registration.agent_type,
            "capabilities": registration.capabilities,
        },
    )

    _ = Agent(
        agent_id=agent_id,
        agent_type=registration.agent_type,
        capabilities=set(registration.capabilities),
        max_concurrent_tasks=registration.max_concurrent_tasks,
        supervisor_id=registration.supervisor_id,
    )

    agents[agent_id] = agent
    hierarchy.add_agent(agent)

    return {"agent_id": agent_id, "status": "registered"}


@router.post("/tasks/submit")
async def submit_task(
    task_request: TaskRequest,
    user: User = Depends(require_roles(Role.USER)),
    _: str = Depends(idempotency_guard),
) -> dict[str, Any]:
    """Submit new task to the multi-agent system"""
    task_id = f"task_{uuid.uuid4().hex[:8]}"

    await audit(
        "multiagent.task.submit",
        actor=user.sub,
        payload={
            "task_id": task_id,
            "task_type": task_request.task_type,
            "priority": task_request.priority,
        },
    )

    task = Task(
        task_id=task_id,
        task_type=task_request.task_type,
        priority=task_request.priority,
        required_capabilities=set(task_request.required_capabilities),
        estimated_duration=timedelta(minutes=task_request.estimated_duration_minutes),
        input_data=task_request.input_data,
        dependencies=set(task_request.dependencies),
    )

    tasks[task_id] = task

    # Add to dependency graph
    task_dependency_graph.add_node(task_id)
    for dep_id in task.dependencies:
        if dep_id in tasks:
            task_dependency_graph.add_edge(dep_id, task_id)

    # Check if task needs decomposition
    if task.estimated_duration > timedelta(hours=1):  # Complex task threshold
        subtasks = TaskDecomposer.decompose_complex_task(task)
        for subtask in subtasks:
            tasks[subtask.task_id] = subtask
            task_dependency_graph.add_node(subtask.task_id)
            for dep_id in subtask.dependencies:
                if dep_id in tasks:
                    task_dependency_graph.add_edge(dep_id, subtask.task_id)

    # Try immediate assignment if no dependencies
    if not task.dependencies:
        assignment = await _assign_task(task_id)
        if assignment:
            return {
                "task_id": task_id,
                "status": "assigned",
                "assigned_agent": assignment.agent_id,
                "estimated_completion": assignment.estimated_completion,
            }

    return {
        "task_id": task_id,
        "status": "pending",
        "message": "Task queued for assignment",
    }


async def _assign_task(task_id: str) -> TaskAssignment | None:
    """Internal function to assign task to best available agent"""
    if task_id not in tasks:
        return None

    task = tasks[task_id]

    # Check if dependencies are completed
    for dep_id in task.dependencies:
        if dep_id not in tasks or tasks[dep_id].status != TaskStatus.COMPLETED:
            return None  # Dependencies not ready

    # Find available agents
    available_agents = [agent for agent in agents.values() if agent.is_available]

    # Find best agent
    AgentMatcher.find_best_agent(task, available_agents)

    if not best_agent:
        return None

    # Assign task
    task.status = TaskStatus.ASSIGNED
    task.assigned_agent_id = best_agent.agent_id
    task.started_at = datetime.now(UTC)

    best_agent.current_tasks.add(task_id)
    if len(best_agent.current_tasks) >= best_agent.max_concurrent_tasks:
        best_agent.status = AgentStatus.BUSY

    estimated_completion = datetime.now(UTC) + task.estimated_duration

    return TaskAssignment(
        task_id=task_id,
        agent_id=best_agent.agent_id,
        estimated_completion=estimated_completion,
    )


@router.get("/tasks/{task_id}/status")
@acached("multiagent:task:status", ttl=30)
async def get_task_status(task_id: str):
    """Get task status and progress"""
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail=TASK_NOT_FOUND)

    task = tasks[task_id]

    # Get subtask statuses if applicable
    subtask_statuses = {}
    if task.subtasks:
        for subtask_id in task.subtasks:
            if subtask_id in tasks:
                subtask_statuses[subtask_id] = tasks[subtask_id].status

    return {
        "task_id": task_id,
        "status": task.status,
        "assigned_agent": task.assigned_agent_id,
        "progress": _calculate_task_progress(task),
        "created_at": task.created_at,
        "started_at": task.started_at,
        "completed_at": task.completed_at,
        "estimated_duration_minutes": int(task.estimated_duration.total_seconds() / 60),
        "result": task.result,
        "error_message": task.error_message,
        "subtasks": subtask_statuses,
        "dependencies_completed": all(
            dep_id in tasks and tasks[dep_id].status == TaskStatus.COMPLETED
            for dep_id in task.dependencies
        ),
    }


def _calculate_task_progress(task: Task) -> float:
    """Calculate task progress percentage"""
    if task.status == TaskStatus.PENDING:
        return 0.0
    elif task.status == TaskStatus.ASSIGNED:
        return 10.0
    elif task.status == TaskStatus.IN_PROGRESS:
        # Estimate based on subtasks if available
        if task.subtasks:
            completed_subtasks = sum(
                1
                for subtask_id in task.subtasks
                if subtask_id in tasks
                and tasks[subtask_id].status == TaskStatus.COMPLETED
            )
            return 10.0 + (completed_subtasks / len(task.subtasks)) * 80.0
        else:
            return 50.0  # Rough estimate for simple tasks
    elif task.status == TaskStatus.COMPLETED:
        return 100.0
    elif task.status in [TaskStatus.FAILED, TaskStatus.CANCELLED]:
        return 0.0

    return 0.0


@router.get("/agents/{agent_id}/status")
@acached("multiagent:agent:status", ttl=30)
async def get_agent_status(agent_id: str):
    """Get agent status and metrics"""
    if agent_id not in agents:
        raise HTTPException(status_code=404, detail=AGENT_NOT_FOUND)

    _ = agents[agent_id]

    return {
        "agent_id": agent_id,
        "agent_type": agent.agent_type,
        "status": agent.status,
        "capabilities": list(agent.capabilities),
        "load_factor": agent.load_factor,
        "current_tasks": list(agent.current_tasks),
        "supervisor": agent.supervisor_id,
        "subordinates": list(agent.subordinates),
        "metrics": {
            "cpu_usage": agent.metrics.cpu_usage,
            "memory_usage": agent.metrics.memory_usage,
            "active_tasks": agent.metrics.active_tasks,
            "completed_tasks": agent.metrics.completed_tasks,
            "failed_tasks": agent.metrics.failed_tasks,
            "success_rate": agent.metrics.success_rate,
            "avg_task_duration_minutes": agent.metrics.avg_task_duration,
            "last_heartbeat": agent.metrics.last_heartbeat,
        },
    }


@router.get("/system/analytics")
async def get_system_analytics(user: User = Depends(require_roles(Role.ADMIN))):
    """Get multi-agent system analytics"""
    await audit("multiagent.analytics", actor=user.sub)

    # Calculate system-wide metrics
    total_agents = len(agents)
    active_agents = sum(
        1 for agent in agents.values() if agent.status != AgentStatus.OFFLINE
    )
    total_tasks = len(tasks)
    completed_tasks = sum(
        1 for task in tasks.values() if task.status == TaskStatus.COMPLETED
    )
    failed_tasks = sum(1 for task in tasks.values() if task.status == TaskStatus.FAILED)

    # Calculate average load
    avg_load = sum(agent.load_factor for agent in agents.values()) / max(
        1, total_agents
    )

    # Task distribution by type
    task_distribution = {}
    for task_type in TaskType:
        task_distribution[task_type.value] = sum(
            1 for task in tasks.values() if task.task_type == task_type
        )

    # Agent distribution by type
    agent_distribution = {}
    for agent_type in AgentType:
        agent_distribution[agent_type.value] = sum(
            1 for agent in agents.values() if agent.agent_type == agent_type
        )

    return {
        "system_health": {
            "total_agents": total_agents,
            "active_agents": active_agents,
            "average_load": avg_load,
            "system_availability": active_agents / max(1, total_agents),
        },
        "task_metrics": {
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "failed_tasks": failed_tasks,
            "success_rate": completed_tasks / max(1, total_tasks),
            "task_distribution": task_distribution,
        },
        "agent_metrics": {
            "agent_distribution": agent_distribution,
            "hierarchy_depth": hierarchy.graph.number_of_nodes(),
            "coordination_efficiency": 0.85,  # Placeholder metric
        },
    }


@router.websocket("/agents/{agent_id}/connect")
async def agent_websocket(websocket: WebSocket, agent_id: str):
    """WebSocket connection for agent communication"""
    await websocket.accept()

    if agent_id not in agents:
        await websocket.close(code=status.WS_1003_UNSUPPORTED_DATA)
        return

    message_queue.register_connection(agent_id, websocket)

    try:
        while True:
            # Send pending messages
            pending_messages = await message_queue.get_messages(agent_id)
            for message in pending_messages:
                await websocket.send_text(message.json())

            # Listen for incoming messages
            try:
                data = await asyncio.wait_for(websocket.receive_text(), timeout=1.0)
                message = AgentMessage.parse_raw(data)
                await message_queue.send_message(message)
            except TimeoutError:
                continue  # Normal timeout, continue loop

    except WebSocketDisconnect:
        message_queue.unregister_connection(agent_id)
    except Exception as e:
        await audit(
            "multiagent.websocket.error", actor=agent_id, payload={"error": str(e)}
        )
        message_queue.unregister_connection(agent_id)
