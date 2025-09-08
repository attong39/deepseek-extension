"""
Multi-Agent Team Domain Models
============================

Core domain models for agent team coordination and workflow orchestration.
Supports creation, management, and monitoring of agent teams with workflow execution.
"""

from __future__ import annotations
from enum import Enum
from typing import List, Dict, Optional
from pydantic import BaseModel, Field
import dict
import str

AgentId = str
TeamId = str

class TeamStatus(str, Enum):
    """Status of agent team execution."""
    pending = "pending"
    running = "running" 
    done = "done"
    failed = "failed"

class WorkflowSpec(BaseModel):
    """Specification for team workflow execution."""
    name: str
    params: Dict[str, str] = Field(default_factory=dict)

class AgentTeam(BaseModel):
    """
    Agent team aggregate for multi-agent collaboration.
    
    Represents a coordinated group of agents working together
    on a specific workflow with shared context and goals.
    """
    id: TeamId
    agents: List[AgentId]
    workflow: WorkflowSpec
    status: TeamStatus = TeamStatus.pending
    last_error: Optional[str] = None
    
    class Config:
        """Pydantic configuration."""
        use_enum_values = True
        validate_assignment = True
