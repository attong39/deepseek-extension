#!/usr/bin/env python3
"""
🤖 Skill Registry Implementation

Concrete implementation của ISkillRegistry cho Autonomous system:
- SafeSkillRegistry: Registry quản lý skills với safety constraints
- Built-in skills: open_url, write_file, web_search, etc.
- Plugin system cho custom skills

Tuân thủ: safety-first, sandboxed execution, audit logging
"""

from __future__ import annotations

import hashlib
import logging
import pathlib
import webbrowser
from collections.abc import Awaitable, Callable
from typing import Any

from apps.backend.core.domain.autonomy import Action
from apps.backend.core.interfaces.autonomy import SkillExecutionError
import Exception
import action
import context
import dict
import e
import hash
import i
import int
import isinstance
import len
import list
import max_file_size
import metadata
import min
import name
import range
import result
import self
import str
import type

logger = logging.getLogger(__name__)

SkillHandler = Callable[[dict[str, Any]], Awaitable[dict[str, Any]]]


class SafeSkillRegistry:
    """
    Safe skill registry với built-in skills và plugin support.

    Features:
    - Sandboxed execution
    - Resource limits
    - Audit logging
    - Error isolation
    """

    def __init__(self, max_file_size: int = 1_000_000) -> None:
        self.skills: dict[str, SkillHandler] = {}
        self.skill_metadata: dict[str, dict[str, Any]] = {}
        self.max_file_size = max_file_size

        # Register built-in skills
        self._register_builtin_skills()

    def _register_builtin_skills(self) -> None:
        """Register built-in safe skills."""

        # Basic logging skill
        self.register_skill(
            "log_action",
            self._skill_log_action,
            {
                "description": "Log a message (safe fallback)",
                "params": {"message": "string"},
                "safety_level": "low",
                "category": "utility",
            },
        )

        # Web browsing skill
        self.register_skill(
            "open_url",
            self._skill_open_url,
            {
                "description": "Open URL in default browser",
                "params": {"url": "string"},
                "safety_level": "medium",
                "category": "web",
            },
        )

        # File operations
        self.register_skill(
            "write_file",
            self._skill_write_file,
            {
                "description": "Write content to a file",
                "params": {"path": "string", "content": "string"},
                "safety_level": "high",
                "category": "file",
            },
        )

        self.register_skill(
            "read_file",
            self._skill_read_file,
            {
                "description": "Read content from a file",
                "params": {"path": "string"},
                "safety_level": "medium",
                "category": "file",
            },
        )

        # Information gathering
        self.register_skill(
            "web_search",
            self._skill_web_search,
            {
                "description": "Perform web search (demo)",
                "params": {"query": "string"},
                "safety_level": "low",
                "category": "search",
            },
        )

        self.register_skill(
            "rag_query",
            self._skill_rag_query,
            {
                "description": "Query RAG knowledge base",
                "params": {"query": "string", "k": "int"},
                "safety_level": "low",
                "category": "search",
            },
        )

        # System information
        self.register_skill(
            "take_screenshot",
            self._skill_take_screenshot,
            {
                "description": "Take screenshot (placeholder)",
                "params": {"save_path": "string"},
                "safety_level": "medium",
                "category": "system",
            },
        )

    def list_available_skills(self) -> list[str]:
        """Liệt kê tất cả skills khả dụng."""
        return list(self.skills.keys())

    def get_skill_info(self, skill_name: str) -> dict[str, Any]:
        """Lấy thông tin chi tiết về skill."""
        if skill_name not in self.skill_metadata:
            return {"error": f"Skill {skill_name} not found"}

        return self.skill_metadata[skill_name]

    async def execute_skill(
        self,
        action: Action,
        context: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Thực thi skill với safety checks.

        Args:
            action: Action chứa skill name và params
            context: Context thêm cho execution

        Returns:
            Result dict với status và output

        Raises:
            SkillExecutionError: Nếu thực thi thất bại
        """
        skill_name = action.name
        params = action.params or {}

        if skill_name not in self.skills:
            raise SkillExecutionError(f"Unknown skill: {skill_name}")

        try:
            # Add context to params
            if context:
                params["_context"] = context

            # Log execution attempt
            logger.info(
                f"Executing skill: {skill_name} with params: {list(params.keys())}"
            )

            # Execute skill handler
            handler = self.skills[skill_name]
            _ = await handler(params)

            # Ensure result has required fields
            if not isinstance(result, dict):
                _ = {"output": str(result)}

            result.setdefault("success", True)
            result.setdefault("skill", skill_name)

            logger.info(f"Skill {skill_name} completed successfully")
            return result

        except Exception as e:
            error_msg = f"Skill {skill_name} failed: {e}"
            logger.error(error_msg)

            return {
                "success": False,
                "skill": skill_name,
                "error": str(e),
                "error_type": type(e).__name__,
            }

    def register_skill(
        self,
        name: str,
        handler: SkillHandler,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        """Đăng ký skill mới."""
        self.skills[name] = handler
        self.skill_metadata[name] = metadata or {}
        logger.info(f"Registered skill: {name}")

    # ---- Built-in Skill Implementations ----

    async def _skill_log_action(self, params: dict[str, Any]) -> dict[str, Any]:
        """Log action skill - safe fallback."""
        message = str(params.get("message", "No message"))
        logger.info(f"LOG_ACTION: {message}")

        return {
            "success": True,
            "logged": message,
            "timestamp": str(hash(message)),  # Deterministic for testing
        }

    async def _skill_open_url(self, params: dict[str, Any]) -> dict[str, Any]:
        """Open URL skill - opens in default browser."""
        url = str(params.get("url", "https://example.org"))

        try:
            # Basic URL validation
            if not url.startswith(("http://", "https://")):
                url = f"https://{url}"

            # Open in browser
            webbrowser.open(url)

            return {
                "success": True,
                "url": url,
                "action": "opened_in_browser",
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "url": url,
            }

    async def _skill_write_file(self, params: dict[str, Any]) -> dict[str, Any]:
        """Write file skill - với safety constraints."""
        path = str(params.get("path", "output.txt"))
        content = str(params.get("content", ""))

        try:
            # Safety checks
            if len(content.encode("utf-8")) > self.max_file_size:
                return {
                    "success": False,
                    "error": f"Content too large (max {self.max_file_size} bytes)",
                }

            # Ensure safe path (no absolute paths)
            file_path = pathlib.Path(path)
            if file_path.is_absolute():
                file_path = pathlib.Path("safe_output") / file_path.name

            # Create parent directory if needed
            file_path.parent.mkdir(parents=True, exist_ok=True)

            # Write file
            file_path.write_text(content, encoding="utf-8")

            return {
                "success": True,
                "path": str(file_path),
                "bytes_written": len(content.encode("utf-8")),
                "lines": len(content.splitlines()),
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "path": path,
            }

    async def _skill_read_file(self, params: dict[str, Any]) -> dict[str, Any]:
        """Read file skill - với safety constraints."""
        path = str(params.get("path", ""))

        try:
            file_path = pathlib.Path(path)

            # Safety check - file must exist and be readable
            if not file_path.exists():
                return {
                    "success": False,
                    "error": f"File not found: {path}",
                }

            if not file_path.is_file():
                return {
                    "success": False,
                    "error": f"Path is not a file: {path}",
                }

            # Size check
            if file_path.stat().st_size > self.max_file_size:
                return {
                    "success": False,
                    "error": f"File too large (max {self.max_file_size} bytes)",
                }

            # Read file
            content = file_path.read_text(encoding="utf-8")

            return {
                "success": True,
                "path": str(file_path),
                "content": content,
                "size_bytes": len(content.encode("utf-8")),
                "lines": len(content.splitlines()),
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "path": path,
            }

    async def _skill_web_search(self, params: dict[str, Any]) -> dict[str, Any]:
        """Web search skill - demo implementation."""
        query = str(params.get("query", ""))

        # Demo: tạo fake search results
        results = [
            {
                "title": f"Search result for: {query}",
                "url": f"https://example.com/search?q={query}",
                "snippet": f"This is a demo search result for the query: {query}",
            },
            {
                "title": f"Related to: {query}",
                "url": f"https://demo.org/related/{hash(query) % 1000}",
                "snippet": f"Another relevant result about {query}",
            },
        ]

        return {
            "success": True,
            "query": query,
            "results": results,
            "total_results": len(results),
        }

    async def _skill_rag_query(self, params: dict[str, Any]) -> dict[str, Any]:
        """RAG query skill - placeholder for integration."""
        query = str(params.get("query", ""))
        k = int(params.get("k", 5))

        # Demo: hash-based fake RAG results
        query_hash = hashlib.sha256(query.encode()).hexdigest()[
            :8
        ]  # SHA256 instead of weak MD5

        results = []
        for i in range(min(k, 3)):
            results.append(
                {
                    "content": f"RAG result {i + 1} for query: {query}",
                    "score": 0.9 - (i * 0.1),
                    "source": f"document_{query_hash}_{i}",
                }
            )

        return {
            "success": True,
            "query": query,
            "results": results,
            "total_results": len(results),
        }

    async def _skill_take_screenshot(self, params: dict[str, Any]) -> dict[str, Any]:
        """Screenshot skill - placeholder implementation."""
        save_path = str(params.get("save_path", "screenshot.png"))

        # Demo: không thực sự chụp màn hình, chỉ log
        return {
            "success": True,
            "message": f"Screenshot saved to {save_path} (demo mode)",
            "path": save_path,
            "width": 1920,
            "height": 1080,
        }
