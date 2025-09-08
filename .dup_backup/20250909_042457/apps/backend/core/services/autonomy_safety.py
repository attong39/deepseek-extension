#!/usr/bin/env python3
"""
🤖 Safety Policy Implementation

Concrete implementation của ISafetyPolicy cho Autonomous system:
- RuleBasedSafetyPolicy: Policy engine dựa trên rules
- ConfigurableSafetyPolicy: Policy từ YAML/JSON config
- Risk assessment và audit logging

Tuân thủ: security-first, fail-safe, comprehensive logging
"""

from __future__ import annotations

import logging
import re
from datetime import datetime
from typing import Any

from apps.backend.core.domain.autonomy import Action, Goal, SafetyDecision
import action
import blocked_cmd
import blocked_path
import blocked_pattern
import context
import dict
import goal
import int
import isinstance
import keyword
import len
import limit
import list
import p
import param_key
import param_value
import pii_pattern
import self
import str
import text
import user_context
import v

logger = logging.getLogger(__name__)


class RuleBasedSafetyPolicy:
    """
    Rule-based safety policy cho Autonomous system.

    Features:
    - Deny-list URLs/paths/commands
    - Resource limits (file size, execution time)
    - PII detection và blocking
    - Risk level assessment
    - Audit trail
    """

    def __init__(self) -> None:
        self.blocked_urls = self._load_blocked_urls()
        self.blocked_paths = self._load_blocked_paths()
        self.blocked_commands = self._load_blocked_commands()
        self.resource_limits = self._load_resource_limits()
        self.pii_patterns = self._load_pii_patterns()

        # Audit log
        self.audit_log: list[dict[str, Any]] = []

    def _load_blocked_urls(self) -> list[str]:
        """Load blocked URL patterns."""
        return [
            # Local file access
            "file://",
            "about:",
            "chrome://",
            "edge://",
            "firefox://",
            # Administrative interfaces
            "localhost:22",  # SSH
            "127.0.0.1:22",
            "admin",
            "/admin",
            # Suspicious patterns
            "javascript:",
            "data:",
            "vbscript:",
        ]

    def _load_blocked_paths(self) -> list[str]:
        """Load blocked file paths."""
        return [
            # System directories
            "/",
            "C:\\",
            "C:\\Windows",
            "C:\\Program Files",
            "/etc",
            "/var",
            "/usr",
            "/bin",
            "/sbin",
            # User sensitive areas
            "C:\\Users\\",
            "/home",
            # Config files
            ".ssh",
            ".aws",
            ".config",
            "id_rsa",
            "private",
        ]

    def _load_blocked_commands(self) -> list[str]:
        """Load blocked command patterns."""
        return [
            # System modification
            "rm ",
            "del ",
            "format",
            "fdisk",
            "mkfs",
            # Network
            "wget",
            "curl",
            "ssh",
            "scp",
            "ftp",
            # Process control
            "kill",
            "killall",
            "taskkill",
            # Privilege escalation
            "sudo",
            "su ",
            "runas",
            # Script execution
            "powershell",
            "cmd.exe",
            "bash",
            "sh ",
        ]

    def _load_resource_limits(self) -> dict[str, Any]:
        """Load resource limits."""
        return {
            "max_file_size_bytes": 10_000_000,  # 10MB
            "max_execution_time_seconds": 30,
            "max_url_length": 1000,
            "max_content_length": 100_000,
        }

    def _load_pii_patterns(self) -> list[dict[str, str]]:
        """Load PII detection patterns."""
        return [
            {
                "name": "email",
                "pattern": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
                "risk": "medium",
            },
            {
                "name": "phone",
                "pattern": r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b",
                "risk": "medium",
            },
            {
                "name": "ssn",
                "pattern": r"\b\d{3}-?\d{2}-?\d{4}\b",
                "risk": "high",
            },
            {
                "name": "credit_card",
                "pattern": r"\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b",
                "risk": "critical",
            },
        ]

    async def evaluate_action(
        self,
        action: Action,
        context: dict[str, Any] | None = None,
    ) -> SafetyDecision:
        """
        Đánh giá tính an toàn của action.

        Args:
            action: Action cần đánh giá
            context: Context thêm (user, session, etc.)

        Returns:
            SafetyDecision với allow/deny và lý do
        """
        decision = SafetyDecision(
            action_id=action.id,
            allow=True,
            reason="Initial approval",
            risk_level="low",
        )

        # Check action type
        self._check_url_safety(action, decision)
        if not decision.allow:
            return decision

        self._check_file_safety(action, decision)
        if not decision.allow:
            return decision

        self._check_command_safety(action, decision)
        if not decision.allow:
            return decision

        self._check_resource_limits(action, decision)
        if not decision.allow:
            return decision

        self._check_pii_exposure(action, decision)
        if not decision.allow:
            return decision

        # Log decision
        self._audit_decision(action, decision, context)

        return decision

    async def evaluate_goal(
        self,
        goal: Goal,
        user_context: dict[str, Any] | None = None,
    ) -> SafetyDecision:
        """Đánh giá tính an toàn của goal ban đầu."""
        decision = SafetyDecision(
            action_id=f"goal_{goal.id}",
            allow=True,
            reason="Goal approved",
            risk_level="low",
        )

        goal_text = goal.description.lower()

        # Check for dangerous keywords in goal
        dangerous_keywords = [
            "delete",
            "remove",
            "format",
            "hack",
            "crack",
            "exploit",
            "virus",
            "malware",
        ]

        for keyword in dangerous_keywords:
            if keyword in goal_text:
                decision.allow = False
                decision.reason = f"Goal contains dangerous keyword: {keyword}"
                decision.risk_level = "high"
                break

        # Check PII in goal description
        if decision.allow:
            pii_found = self._detect_pii(goal.description)
            if pii_found:
                decision.allow = False
                decision.reason = f"Goal contains PII: {', '.join(pii_found)}"
                decision.risk_level = "critical"

        # Log decision
        self._audit_decision(None, decision, user_context, goal=goal)

        return decision

    def get_policy_rules(self) -> list[dict[str, Any]]:
        """Lấy danh sách rules đang áp dụng."""
        return [
            {
                "category": "blocked_urls",
                "rules": self.blocked_urls,
                "count": len(self.blocked_urls),
            },
            {
                "category": "blocked_paths",
                "rules": self.blocked_paths,
                "count": len(self.blocked_paths),
            },
            {
                "category": "blocked_commands",
                "rules": self.blocked_commands,
                "count": len(self.blocked_commands),
            },
            {
                "category": "resource_limits",
                "rules": self.resource_limits,
                "count": len(self.resource_limits),
            },
            {
                "category": "pii_patterns",
                "rules": [p["name"] for p in self.pii_patterns],
                "count": len(self.pii_patterns),
            },
        ]

    # ---- Internal Check Methods ----

    def _check_url_safety(self, action: Action, decision: SafetyDecision) -> None:
        """Check URL safety for web-related actions."""
        if action.name != "open_url":
            return

        url = str(action.params.get("url", ""))

        # Check blocked patterns
        for blocked_pattern in self.blocked_urls:
            if blocked_pattern in url.lower():
                decision.allow = False
                decision.reason = f"Blocked URL pattern: {blocked_pattern}"
                decision.risk_level = "high"
                decision.policy_rules_applied.append("blocked_urls")
                return

        # Check URL length
        if len(url) > self.resource_limits["max_url_length"]:
            decision.allow = False
            decision.reason = "URL too long"
            decision.risk_level = "medium"
            decision.policy_rules_applied.append("url_length_limit")

    def _check_file_safety(self, action: Action, decision: SafetyDecision) -> None:
        """Check file operation safety."""
        if action.name not in ["write_file", "read_file"]:
            return

        path = str(action.params.get("path", ""))

        # Check blocked paths
        for blocked_path in self.blocked_paths:
            if path.startswith(blocked_path):
                decision.allow = False
                decision.reason = f"Blocked path: {blocked_path}"
                decision.risk_level = "critical"
                decision.policy_rules_applied.append("blocked_paths")
                return

        # Check file size for write operations
        if action.name == "write_file":
            content = str(action.params.get("content", ""))
            content_size = len(content.encode("utf-8"))

            if content_size > self.resource_limits["max_file_size_bytes"]:
                decision.allow = False
                decision.reason = f"Content too large: {content_size} bytes"
                decision.risk_level = "medium"
                decision.policy_rules_applied.append("file_size_limit")

    def _check_command_safety(self, action: Action, decision: SafetyDecision) -> None:
        """Check command execution safety."""
        # Look for command-like content in any parameter
        for param_value in action.params.values():
            param_str = str(param_value).lower()

            for blocked_cmd in self.blocked_commands:
                if blocked_cmd in param_str:
                    decision.allow = False
                    decision.reason = f"Blocked command pattern: {blocked_cmd}"
                    decision.risk_level = "critical"
                    decision.policy_rules_applied.append("blocked_commands")
                    return

    def _check_resource_limits(self, action: Action, decision: SafetyDecision) -> None:
        """Check resource limits."""
        # Check content length in any text parameter
        for param_key, param_value in action.params.items():
            if isinstance(param_value, str):
                if len(param_value) > self.resource_limits["max_content_length"]:
                    decision.allow = False
                    decision.reason = f"Parameter {param_key} too long"
                    decision.risk_level = "medium"
                    decision.policy_rules_applied.append("content_length_limit")
                    return

    def _check_pii_exposure(self, action: Action, decision: SafetyDecision) -> None:
        """Check for PII exposure in action parameters."""
        # Combine all text parameters
        text_content = " ".join(
            str(v) for v in action.params.values() if isinstance(v, str)
        )

        pii_found = self._detect_pii(text_content)
        if pii_found:
            decision.allow = False
            decision.reason = f"PII detected: {', '.join(pii_found)}"
            decision.risk_level = "critical"
            decision.policy_rules_applied.append("pii_protection")

    def _detect_pii(self, text: str) -> list[str]:
        """Detect PII patterns in text."""
        found_pii = []

        for pii_pattern in self.pii_patterns:
            pattern = pii_pattern["pattern"]
            name = pii_pattern["name"]

            if re.search(pattern, text):
                found_pii.append(name)

        return found_pii

    def _audit_decision(
        self,
        action: Action | None,
        decision: SafetyDecision,
        context: dict[str, Any] | None,
        goal: Goal | None = None,
    ) -> None:
        """Log audit trail cho safety decision."""
        audit_entry = {
            "timestamp": datetime.now().isoformat(),
            "decision": {
                "allow": decision.allow,
                "reason": decision.reason,
                "risk_level": decision.risk_level,
                "rules_applied": decision.policy_rules_applied,
            },
            "action": {
                "id": action.id if action else None,
                "name": action.name if action else None,
                "params_keys": list(action.params.keys()) if action else None,
            }
            if action
            else None,
            "goal": {
                "id": goal.id if goal else None,
                "description": goal.description[:100] if goal else None,  # truncated
            }
            if goal
            else None,
            "context": {
                "user_id": context.get("user_id") if context else None,
                "session_id": context.get("session_id") if context else None,
            }
            if context
            else None,
        }

        self.audit_log.append(audit_entry)

        # Log to standard logger
        log_msg = f"Safety decision: {decision.allow} - {decision.reason}"
        if decision.allow:
            logger.info(log_msg)
        else:
            logger.warning(log_msg)

    def get_audit_log(self, limit: int = 100) -> list[dict[str, Any]]:
        """Lấy audit log gần đây."""
        return self.audit_log[-limit:]
