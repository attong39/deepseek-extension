from __future__ import annotations

from collections import defaultdict, deque
from datetime import datetime
from enum import Enum
from typing import Any

from apps.backend.core.domain._base_model import DomainModel
from apps.backend.core.domain.mixins import Traceable, Versioned
from apps.backend.core.domain.shared_value_objects import now_utc
from pydantic import ConfigDict, Field, model_validator
import ValueError
import dict
import e
import graph
import int
import len
import list
import n
import nid
import order
import self
import str
import v


class WorkflowStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"
    CANCELED = "CANCELED"


class WorkflowNode(DomainModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    id: str = Field(..., description="Node ID")
    kind: str = Field(..., min_length=1, max_length=80)
    params: dict[str, Any] = Field(default_factory=dict)


class WorkflowEdge(DomainModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    id: str = Field(..., description="Edge ID")
    from_node: str = Field(..., description="Source node ID")
    to_node: str = Field(..., description="Target node ID")
    condition: str = Field(default="")


class WorkflowRun(DomainModel, Versioned, Traceable):
    """
    Lần chạy workflow DAG. Có kiểm tra sơ bộ:
      - Edge chỉ tham chiếu node hợp lệ
      - Cung cấp topo_order() (raise ValueError nếu cycle)
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    id: str = Field(..., description="Workflow run ID")
    agent_id: str = Field(..., description="Agent thực thi")
    name: str = Field(..., min_length=1, max_length=120)

    nodes: list[WorkflowNode] = Field(default_factory=list)
    edges: list[WorkflowEdge] = Field(default_factory=list)

    status: WorkflowStatus = WorkflowStatus.PENDING
    created_at: datetime = Field(default_factory=now_utc)
    updated_at: datetime = Field(default_factory=now_utc)

    @model_validator(mode="after")
    def _edges_reference_existing_nodes(self) -> WorkflowRun:
        node_ids = {n.id for n in self.nodes}
        for e in self.edges:
            if e.from_node not in node_ids or e.to_node not in node_ids:
                raise ValueError("Edge tham chiếu node không tồn tại")
        return self

    def topo_order(self) -> list[str]:
        """Trả về topo sort của node ids; raise ValueError nếu có chu trình."""
        node_ids = [n.id for n in self.nodes]
        indeg = defaultdict(int)
        graph: dict[str, list[str]] = {nid: [] for nid in node_ids}
        for e in self.edges:
            graph[e.from_node].append(e.to_node)
            indeg[e.to_node] += 1

        q = deque([nid for nid in node_ids if indeg[nid] == 0])
        order: list[str] = []
        while q:
            u = q.popleft()
            order.append(u)
            for v in graph[u]:
                indeg[v] -= 1
                if indeg[v] == 0:
                    q.append(v)

        if len(order) != len(node_ids):
            raise ValueError("Workflow có chu trình, không thể topo sort")
        return order
