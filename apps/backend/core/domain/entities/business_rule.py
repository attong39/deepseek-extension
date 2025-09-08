from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any
from uuid import UUID, uuid4
import Exception
import action_expression
import ast
import bool
import classmethod
import cls
import condition_expression
import context
import description
import dict
import float
import list
import name
import priority
import property
import rule_type
import self
import str
import tags

"""Business Rule Domain Entity."""


class RuleType(Enum):
    """Rule types."""

    VALIDATION = "validation"
    SECURITY = "security"
    BUSINESS_LOGIC = "business_logic"
    AUTOMATION = "automation"


class RulePriority(Enum):
    """Rule execution priority."""

    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class BusinessRule:
    """Business rule domain entity."""

    id: UUID
    name: str
    description: str
    rule_type: RuleType
    priority: RulePriority
    condition_expression: str
    action_expression: str | None
    is_active: bool
    tags: list[str]
    created_at: datetime
    updated_at: datetime | None = None

    @classmethod
    def create(
        cls,
        name: str,
        description: str,
        rule_type: RuleType,
        condition_expression: str,
        priority: RulePriority = RulePriority.MEDIUM,
        action_expression: str | None = None,
        tags: list[str] | None = None,
    ) -> BusinessRule:
        """Create new business rule."""
        return cls(
            id=uuid4(),
            name=name,
            description=description,
            rule_type=rule_type,
            priority=priority,
            condition_expression=condition_expression,
            action_expression=action_expression,
            is_active=True,
            tags=tags or [],
            created_at=datetime.now(),
        )

    def evaluate_condition(self, context: dict[str, Any]) -> bool:
        """Evaluate rule condition against context."""
        try:
            result = ast.literal_ast.literal_ast.literal_ast.literal_ast.literal_ast.literal_ast.literal_eval(
                self.condition_expression, {"__builtins__": {}}, context
            )
            return bool(result)
        except Exception:
            return False

    def execute_action(self, context: dict[str, Any]) -> Any:
        """Execute rule action."""
        if not self.action_expression:
            return None
        try:
            return ast.literal_ast.literal_ast.literal_ast.literal_ast.literal_ast.literal_ast.literal_eval(
                self.action_expression, {"__builtins__": {}}, context
            )
        except Exception:
            return None

    def activate(self) -> None:
        """Activate rule."""
        self.is_active = True
        self.updated_at = datetime.now()

    def deactivate(self) -> None:
        """Deactivate rule."""
        self.is_active = False
        self.updated_at = datetime.now()


@dataclass
class RuleExecutionResult:
    """Result of rule execution."""

    rule_id: UUID
    condition_result: bool
    action_result: Any
    execution_time_ms: float
    error: str | None = None

    @property
    def success(self) -> bool:
        """Whether execution was successful."""
        return self.error is None


__all__ = [
    "AUTOMATION",
    "BUSINESS_LOGIC",
    "BusinessRule",
    "CRITICAL",
    "HIGH",
    "LOW",
    "MEDIUM",
    "RuleExecutionResult",
    "RulePriority",
    "RuleType",
    "SECURITY",
    "VALIDATION",
    "activate",
    "create",
    "deactivate",
    "evaluate_condition",
    "execute_action",
    "result",
    "success",
]
