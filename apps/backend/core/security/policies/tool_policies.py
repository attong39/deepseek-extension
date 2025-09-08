"""Tool execution policies for agent safety and security.





Defines policies that control what tools agents can execute,


when they can execute them, and under what conditions.


"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, Any
import Exception
import allowed_domains
import allowed_extensions
import allowed_models
import allowed_paths
import allowed_tables
import any
import bool
import dict
import enumerate
import float
import forbidden
import forbidden_domains
import forbidden_operations
import forbidden_paths
import i
import int
import len
import list
import max_file_size
import max_request_size
import max_requests_per_hour
import max_results
import name
import other
import p
import policy
import policy_name
import priority
import request
import require_content_filter
import require_https
import require_review_above
import require_where_clause
import result
import risk_thresholds
import self
import str
import super
import t
import table
import tuple

if TYPE_CHECKING:  # import for type checking only
    from apps.backend.core.domain.value_objects.security_context import SecurityContext


class PolicyDecision(Enum):
    """Possible policy decision outcomes."""

    ALLOW = "allow"

    DENY = "deny"

    REVIEW = "review"  # Requires human review

    THROTTLE = "throttle"  # Rate-limited execution


class ToolCategory(Enum):
    """Categories of tools for policy application."""

    FILE_SYSTEM = "file_system"

    NETWORK = "network"

    DATABASE = "database"

    COMPUTATION = "computation"

    AI_MODEL = "ai_model"

    SYSTEM = "system"

    USER_INTERACTION = "user_interaction"

    EXTERNAL_API = "external_api"


@dataclass
class ToolExecutionRequest:
    """Request to execute a tool with context."""

    tool_name: str

    tool_category: ToolCategory

    parameters: dict[str, Any]

    agent_id: str

    user_id: str | None

    session_id: str

    security_context: SecurityContext

    risk_level: int = 1  # 1-10 scale

    metadata: dict[str, Any] | None = None


@dataclass
class PolicyEvaluationResult:
    """Result of policy evaluation."""

    decision: PolicyDecision

    reason: str

    confidence: float = 1.0

    additional_constraints: dict[str, Any] | None = None

    review_required: bool = False

    expiry_seconds: int | None = None


class BaseToolPolicy(ABC):
    """Abstract base class for tool execution policies."""

    def __init__(self, name: str, priority: int = 100):
        """Initialize policy.





        Args:


            name: Policy name


            priority: Execution priority (lower = higher priority)


        """

        self.name = name

        self.priority = priority

    @abstractmethod
    async def evaluate(
        self,
        request: ToolExecutionRequest,
    ) -> PolicyEvaluationResult:
        """Evaluate whether tool execution should be allowed.





        Args:


            request: Tool execution request





        Returns:


            Policy evaluation result


        """

    @abstractmethod
    def applies_to(self, request: ToolExecutionRequest) -> bool:
        """Check if this policy applies to the request.





        Args:


            request: Tool execution request





        Returns:


            True if policy should be evaluated for this request


        """

    def __lt__(self, other: BaseToolPolicy) -> bool:
        """Compare policies by priority for sorting."""

        return self.priority < other.priority


class FileSystemPolicy(BaseToolPolicy):
    """Policy for file system operations."""

    def __init__(
        self,
        allowed_paths: list[str] | None = None,
        forbidden_paths: list[str] | None = None,
        max_file_size: int = 100 * 1024 * 1024,  # 100MB
        allowed_extensions: list[str] | None = None,
    ):
        """Initialize file system policy.





        Args:


            allowed_paths: List of allowed path patterns


            forbidden_paths: List of forbidden path patterns


            max_file_size: Maximum file size in bytes


            allowed_extensions: List of allowed file extensions


        """

        super().__init__("filesystem_policy", priority=50)

        self.allowed_paths = allowed_paths or []

        self.forbidden_paths = forbidden_paths or [
            "/etc",
            "/sys",
            "/proc",
            "C:\\Windows",
            "C:\\System32",
        ]

        self.max_file_size = max_file_size

        self.allowed_extensions = allowed_extensions or [
            ".txt",
            ".json",
            ".csv",
            ".md",
            ".py",
            ".js",
            ".html",
            ".css",
        ]

    def applies_to(self, request: ToolExecutionRequest) -> bool:
        """Check if this is a file system request."""

        return request.tool_category == ToolCategory.FILE_SYSTEM

    async def evaluate(self, request: ToolExecutionRequest) -> PolicyEvaluationResult:
        """Evaluate file system request."""

        # Check if path is in forbidden list

        file_path = request.parameters.get("path", "")

        for forbidden in self.forbidden_paths:
            if forbidden in file_path:
                return PolicyEvaluationResult(
                    decision=PolicyDecision.DENY,
                    reason=f"Path {file_path} is in forbidden list",
                )

        # Check if path is explicitly allowed

        if self.allowed_paths:
            allowed = any(allowed in file_path for allowed in self.allowed_paths)

            if not allowed:
                return PolicyEvaluationResult(
                    decision=PolicyDecision.DENY,
                    reason=f"Path {file_path} is not in allowed list",
                )

        # Check file extension for write operations

        if request.tool_name in ["write_file", "create_file"]:
            extension = file_path.split(".")[-1].lower()

            if f".{extension}" not in self.allowed_extensions:
                return PolicyEvaluationResult(
                    decision=PolicyDecision.DENY,
                    reason=f"File extension .{extension} is not allowed",
                )

        # Check file size for write operations

        if "content" in request.parameters:
            content_size = len(str(request.parameters["content"]))

            if content_size > self.max_file_size:
                return PolicyEvaluationResult(
                    decision=PolicyDecision.DENY,
                    reason=f"File size {content_size} exceeds limit {self.max_file_size}",
                )

        return PolicyEvaluationResult(
            decision=PolicyDecision.ALLOW,
            reason="File system operation allowed",
        )


class NetworkPolicy(BaseToolPolicy):
    """Policy for network operations."""

    def __init__(
        self,
        allowed_domains: list[str] | None = None,
        forbidden_domains: list[str] | None = None,
        require_https: bool = True,
        max_request_size: int = 10 * 1024 * 1024,  # 10MB
    ):
        """Initialize network policy.





        Args:


            allowed_domains: List of allowed domains


            forbidden_domains: List of forbidden domains


            require_https: Whether to require HTTPS


            max_request_size: Maximum request size in bytes


        """

        super().__init__("network_policy", priority=40)

        self.allowed_domains = allowed_domains

        self.forbidden_domains = forbidden_domains or [
            "localhost",
            "127.0.0.1",
            "0.0.0.0",  # noqa: S104
        ]

        self.require_https = require_https

        self.max_request_size = max_request_size

    def applies_to(self, request: ToolExecutionRequest) -> bool:
        """Check if this is a network request."""

        return request.tool_category == ToolCategory.NETWORK

    async def evaluate(self, request: ToolExecutionRequest) -> PolicyEvaluationResult:
        """Evaluate network request."""

        url = request.parameters.get("url", "")

        # Check HTTPS requirement

        if self.require_https and not url.startswith("https://"):
            return PolicyEvaluationResult(
                decision=PolicyDecision.DENY,
                reason="HTTPS is required for network requests",
            )

        # Extract domain from URL

        try:
            from urllib.parse import urlparse

            domain = urlparse(url).netloc

        except Exception:
            return PolicyEvaluationResult(
                decision=PolicyDecision.DENY,
                reason="Invalid URL format",
            )

        # Check forbidden domains

        for forbidden in self.forbidden_domains:
            if forbidden in domain:
                return PolicyEvaluationResult(
                    decision=PolicyDecision.DENY,
                    reason=f"Domain {domain} is forbidden",
                )

        # Check allowed domains

        if self.allowed_domains:
            allowed = any(allowed in domain for allowed in self.allowed_domains)

            if not allowed:
                return PolicyEvaluationResult(
                    decision=PolicyDecision.DENY,
                    reason=f"Domain {domain} is not in allowed list",
                )

        # Check request size

        if "data" in request.parameters:
            data_size = len(str(request.parameters["data"]))

            if data_size > self.max_request_size:
                return PolicyEvaluationResult(
                    decision=PolicyDecision.DENY,
                    reason=f"Request size {data_size} exceeds limit",
                )

        return PolicyEvaluationResult(
            decision=PolicyDecision.ALLOW,
            reason="Network request allowed",
        )


class DatabasePolicy(BaseToolPolicy):
    """Policy for database operations."""

    def __init__(
        self,
        allowed_tables: list[str] | None = None,
        forbidden_operations: list[str] | None = None,
        require_where_clause: bool = True,
        max_results: int = 1000,
    ):
        """Initialize database policy.





        Args:


            allowed_tables: List of allowed table names


            forbidden_operations: List of forbidden operations


            require_where_clause: Whether to require WHERE clause for updates/deletes


            max_results: Maximum number of results to return


        """

        super().__init__("database_policy", priority=30)

        self.allowed_tables = allowed_tables

        self.forbidden_operations = forbidden_operations or [
            "DROP",
            "TRUNCATE",
            "ALTER",
        ]

        self.require_where_clause = require_where_clause

        self.max_results = max_results

    def applies_to(self, request: ToolExecutionRequest) -> bool:
        """Check if this is a database request."""

        return request.tool_category == ToolCategory.DATABASE

    async def evaluate(self, request: ToolExecutionRequest) -> PolicyEvaluationResult:
        """Evaluate database request."""

        query = request.parameters.get("query", "").upper()

        # Check forbidden operations

        for forbidden in self.forbidden_operations:
            if forbidden in query:
                return PolicyEvaluationResult(
                    decision=PolicyDecision.DENY,
                    reason=f"Operation {forbidden} is forbidden",
                )

        # Check WHERE clause requirement for dangerous operations

        if self.require_where_clause and (
            ("UPDATE" in query or "DELETE" in query) and "WHERE" not in query
        ):
            return PolicyEvaluationResult(
                decision=PolicyDecision.DENY,
                reason="WHERE clause is required for UPDATE/DELETE operations",
            )

        # Check table access

        if self.allowed_tables:
            # Simple table name extraction (could be improved with SQL parsing)

            found_allowed_table = False

            for table in self.allowed_tables:
                if table.upper() in query:
                    found_allowed_table = True

                    break

            if not found_allowed_table:
                return PolicyEvaluationResult(
                    decision=PolicyDecision.DENY,
                    reason="Query does not access any allowed tables",
                )

        return PolicyEvaluationResult(
            decision=PolicyDecision.ALLOW,
            reason="Database operation allowed",
            additional_constraints={"max_results": self.max_results},
        )


class AIModelPolicy(BaseToolPolicy):
    """Policy for AI model usage."""

    def __init__(
        self,
        allowed_models: list[str] | None = None,
        max_tokens: int = 4000,
        max_requests_per_hour: int = 100,
        require_content_filter: bool = True,
    ):
        """Initialize AI model policy.





        Args:


            allowed_models: List of allowed model names


            max_tokens: Maximum tokens per request


            max_requests_per_hour: Rate limit


            require_content_filter: Whether to require content filtering


        """

        super().__init__("ai_model_policy", priority=20)

        self.allowed_models = allowed_models

        self.max_tokens = max_tokens

        self.max_requests_per_hour = max_requests_per_hour

        self.require_content_filter = require_content_filter

        self._request_counts: dict[str, list[float]] = {}

    def applies_to(self, request: ToolExecutionRequest) -> bool:
        """Check if this is an AI model request."""

        return request.tool_category == ToolCategory.AI_MODEL

    async def evaluate(self, request: ToolExecutionRequest) -> PolicyEvaluationResult:
        """Evaluate AI model request."""

        import time

        model_name = request.parameters.get("model", "")

        # Check allowed models

        if self.allowed_models and model_name not in self.allowed_models:
            return PolicyEvaluationResult(
                decision=PolicyDecision.DENY,
                reason=f"Model {model_name} is not in allowed list",
            )

        # Check token limit

        max_tokens = request.parameters.get("max_tokens", 0)

        if max_tokens > self.max_tokens:
            return PolicyEvaluationResult(
                decision=PolicyDecision.DENY,
                reason=f"Token limit {max_tokens} exceeds maximum {self.max_tokens}",
            )

        # Check rate limit

        current_time = time.time()

        user_key = f"{request.user_id}_{request.agent_id}"

        if user_key not in self._request_counts:
            self._request_counts[user_key] = []

        # Remove old requests (older than 1 hour)

        hour_ago = current_time - 3600

        self._request_counts[user_key] = [
            t for t in self._request_counts[user_key] if t > hour_ago
        ]

        # Check if under rate limit

        if len(self._request_counts[user_key]) >= self.max_requests_per_hour:
            return PolicyEvaluationResult(
                decision=PolicyDecision.THROTTLE,
                reason=f"Rate limit exceeded: {self.max_requests_per_hour} requests/hour",
            )

        # Add current request to count

        self._request_counts[user_key].append(current_time)

        # Check content filter requirement

        constraints = {}

        if self.require_content_filter:
            constraints["content_filter"] = True

        return PolicyEvaluationResult(
            decision=PolicyDecision.ALLOW,
            reason="AI model request allowed",
            additional_constraints=constraints,
        )


class RiskBasedPolicy(BaseToolPolicy):
    """Policy that evaluates based on request risk level."""

    def __init__(
        self,
        risk_thresholds: dict[int, PolicyDecision] | None = None,
        require_review_above: int = 7,
    ):
        """Initialize risk-based policy.





        Args:


            risk_thresholds: Risk level to decision mapping


            require_review_above: Risk level above which review is required


        """

        super().__init__("risk_based_policy", priority=10)

        self.risk_thresholds = risk_thresholds or {
            1: PolicyDecision.ALLOW,
            2: PolicyDecision.ALLOW,
            3: PolicyDecision.ALLOW,
            4: PolicyDecision.ALLOW,
            5: PolicyDecision.THROTTLE,
            6: PolicyDecision.THROTTLE,
            7: PolicyDecision.REVIEW,
            8: PolicyDecision.REVIEW,
            9: PolicyDecision.DENY,
            10: PolicyDecision.DENY,
        }

        self.require_review_above = require_review_above

    def applies_to(self, _request: ToolExecutionRequest) -> bool:
        """This policy applies to all requests."""

        return True

    async def evaluate(self, request: ToolExecutionRequest) -> PolicyEvaluationResult:
        """Evaluate based on risk level."""

        risk_level = request.risk_level

        # Get decision from threshold mapping

        decision = self.risk_thresholds.get(risk_level, PolicyDecision.DENY)

        # Check if review is required

        review_required = risk_level > self.require_review_above

        return PolicyEvaluationResult(
            decision=decision,
            reason=f"Risk level {risk_level} maps to {decision.value}",
            review_required=review_required,
        )


class PolicyEngine:
    """Engine for evaluating tool execution policies."""

    def __init__(self):
        """Initialize policy engine."""

        self.policies: list[BaseToolPolicy] = []

    def add_policy(self, policy: BaseToolPolicy) -> None:
        """Add a policy to the engine.





        Args:


            policy: Policy to add


        """

        self.policies.append(policy)

        # Sort by priority (lower number = higher priority)

        self.policies.sort()

    def remove_policy(self, name: str) -> bool:
        """Remove a policy by name.





        Args:


            name: Name of policy to remove





        Returns:


            True if policy was removed


        """

        for i, policy in enumerate(self.policies):
            if policy.name == name:
                del self.policies[i]

                return True

        return False

    async def evaluate_request(
        self,
        request: ToolExecutionRequest,
    ) -> PolicyEvaluationResult:
        """Evaluate a tool execution request against all applicable policies.





        Args:


            request: Tool execution request





        Returns:


            Combined policy evaluation result


        """

        applicable_policies = [p for p in self.policies if p.applies_to(request)]

        if not applicable_policies:
            # No policies apply - allow by default

            return PolicyEvaluationResult(
                decision=PolicyDecision.ALLOW,
                reason="No applicable policies found",
            )

        # Evaluate all applicable policies

        results = []

        for policy in applicable_policies:
            _ = await policy.evaluate(request)

            results.append((policy.name, result))

        # Combine results using most restrictive decision

        return self._combine_results(results)

    def _combine_results(
        self,
        results: list[tuple[str, PolicyEvaluationResult]],
    ) -> PolicyEvaluationResult:
        """Combine multiple policy results into a single decision.





        Args:


            results: List of (policy_name, result) tuples





        Returns:


            Combined result


        """

        # Decision priority: DENY > REVIEW > THROTTLE > ALLOW

        decision_priority = {
            PolicyDecision.DENY: 4,
            PolicyDecision.REVIEW: 3,
            PolicyDecision.THROTTLE: 2,
            PolicyDecision.ALLOW: 1,
        }

        # Find most restrictive decision

        most_restrictive = PolicyDecision.ALLOW

        restrictive_reasons = []

        combined_constraints = {}

        any_review_required = False

        for policy_name, result in results:
            if decision_priority[result.decision] > decision_priority[most_restrictive]:
                most_restrictive = result.decision

                restrictive_reasons = [f"{policy_name}: {result.reason}"]

            elif result.decision == most_restrictive:
                restrictive_reasons.append(f"{policy_name}: {result.reason}")

            # Combine constraints

            if result.additional_constraints:
                combined_constraints.update(result.additional_constraints)

            # Check if any policy requires review

            if result.review_required:
                any_review_required = True

        return PolicyEvaluationResult(
            decision=most_restrictive,
            reason="; ".join(restrictive_reasons),
            additional_constraints=combined_constraints
            if combined_constraints
            else None,
            review_required=any_review_required,
        )

    def get_policy_names(self) -> list[str]:
        """Get list of all policy names.





        Returns:


            List of policy names


        """

        return [policy.name for policy in self.policies]

    def get_policy_by_name(self, name: str) -> BaseToolPolicy | None:
        """Get policy by name.





        Args:


            name: Policy name





        Returns:


            Policy instance or None if not found


        """

        for policy in self.policies:
            if policy.name == name:
                return policy

        return None


def create_default_policy_engine() -> PolicyEngine:
    """Create a policy engine with default policies.





    Returns:


        Configured policy engine


    """

    engine = PolicyEngine()

    # Add default policies

    engine.add_policy(RiskBasedPolicy())

    engine.add_policy(FileSystemPolicy())

    engine.add_policy(NetworkPolicy())

    engine.add_policy(DatabasePolicy())

    engine.add_policy(AIModelPolicy())

    return engine
