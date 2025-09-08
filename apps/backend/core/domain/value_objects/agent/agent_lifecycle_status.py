"""
Agent Status Enum - Simple domain status states.

Enum đơn giản cho trạng thái domain của Agent.
Tách biệt với runtime status complex ở agent_status.py.
"""

from __future__ import annotations

from enum import Enum
import bool
import self
import str


class AgentLifecycleStatus(str, Enum):
    """
    Enum đơn giản cho lifecycle status của Agent.

    Đây là domain status, khác với runtime status phức tạp.
    Sử dụng str enum để dễ serialize và debug.
    """

    INACTIVE = "INACTIVE"
    ACTIVE = "ACTIVE"
    BUSY = "BUSY"
    TRAINING = "TRAINING"
    ERROR = "ERROR"
    SUSPENDED = "SUSPENDED"
    ARCHIVED = "ARCHIVED"

    def is_operational(self) -> bool:
        """Kiểm tra agent có thể nhận task không."""
        return self in {self.ACTIVE, self.BUSY}

    def can_activate(self) -> bool:
        """Kiểm tra có thể chuyển sang ACTIVE không."""
        return self in {self.INACTIVE, self.ERROR, self.SUSPENDED}

    def can_assign_task(self) -> bool:
        """Kiểm tra có thể gán task mới không."""
        return self == self.ACTIVE


__all__ = ["AgentLifecycleStatus"]
