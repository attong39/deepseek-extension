#!/usr/bin/env python3
"""
DeepSeek Agent - Tự Động Quét & Nâng Cấp Dự Án

Orchestrator AI-powered để quét toàn bộ dự án, tối ưu code, thêm tính năng,
và phát triển liên tục với self-learning.

Attributes:
    PROJECT_DIRS: Danh sách thư mục dự án cần quét.
    LLM_MODEL: Model LLM sử dụng cho decision-making.
    SCAN_PATTERNS: Patterns để scan files.
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

from apps.backend.core.services.llm_service import LLMService
from apps.backend.data.models.deepseek_model import DeepSeekLocalModel

# Constants - không side-effect, immutable
PROJECT_DIRS: list[Path] = [
    Path("zeta_vn"),
    Path("desktop_ai_zeta"),
    Path("deepseek"),
    Path("deepseek-extension"),
]

SCAN_PATTERNS: set[str] = {
    "*.py",
    "*.ts",
    "*.tsx",
    "*.js",
    "*.jsx",
    "*.md",
    "*.yml",
    "*.yaml",
    "*.json",
}

LLM_MODEL: str = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
ROOT: Path = Path(__file__).parent.parent

# Logging setup với cấu hình nâng cao
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(ROOT / ".artifacts" / "deepseek_agent.log", encoding="utf-8"),
    ],
)
logger = logging.getLogger(__name__)


@dataclass
class FileMetadata:
    """Metadata cho file được scan."""

    path: Path
    type: str
    size: int
    mtime: float
    lines: int = 0

    @classmethod
    def from_path(cls, path: Path) -> FileMetadata:
        """Tạo FileMetadata từ Path."""
        stat = path.stat()
        file_type = cls._detect_type(path)
        lines = cls._count_lines(path) if file_type in {"python", "typescript", "javascript"} else 0

        return cls(path=path, type=file_type, size=stat.st_size, mtime=stat.st_mtime, lines=lines)

    @staticmethod
    def _detect_type(path: Path) -> str:
        """Detect file type từ extension."""
        ext = path.suffix.lower()
        type_map = {
            ".py": "python",
            ".ts": "typescript",
            ".tsx": "typescript",
            ".js": "javascript",
            ".jsx": "javascript",
            ".md": "markdown",
            ".yml": "yaml",
            ".yaml": "yaml",
            ".json": "json",
        }
        return type_map.get(ext, "unknown")

    @staticmethod
    def _count_lines(path: Path) -> int:
        """Count lines trong file."""
        try:
            with open(path, encoding="utf-8") as f:
                return sum(1 for _ in f)
        except Exception:
            return 0


@dataclass
class OptimizationSuggestion:
    """Suggestion cho optimization."""

    file: Path
    action: str
    description: str
    priority: str = "medium"
    estimated_effort: str = "low"

    def to_dict(self) -> dict[str, str]:
        """Convert to dict cho serialization."""
        return {
            "file": str(self.file),
            "action": self.action,
            "description": self.description,
            "priority": self.priority,
            "estimated_effort": self.estimated_effort,
        }


class DeepSeekAgent:
    """Main agent class cho project scanning và optimization."""

    def __init__(self, llm_service: LLMService | None = None) -> None:
        """Khởi tạo agent với LLM service.

        Args:
            llm_service: Service cho LLM operations. Nếu None, sẽ tạo default local model.
        """
        self.scanned_files: list[FileMetadata] = []
        self.suggestions: list[OptimizationSuggestion] = []
        self.stats = {
            "files_scanned": 0,
            "suggestions_generated": 0,
            "changes_applied": 0,
            "errors": 0,
        }

        # Initialize LLM service
        if llm_service is None:
            deepseek_model = DeepSeekLocalModel()
            self.llm_service = LLMService(deepseek_model)
        else:
            self.llm_service = llm_service

    async def scan_project(self, dir_path: Path) -> list[FileMetadata]:
        """Async scan thư mục dự án.

        Args:
            dir_path: Thư mục cần scan.

        Returns:
            Danh sách FileMetadata.
        """
        if not dir_path.exists():
            logger.warning(f"Directory {dir_path} does not exist")
            return []

        files = []
        tasks = []

        for pattern in SCAN_PATTERNS:
            for file_path in dir_path.rglob(pattern):
                if file_path.is_file() and not self._should_ignore(file_path):
                    tasks.append(self._process_file_async(file_path))

        # Execute concurrently
        if tasks:
            results = await asyncio.gather(*tasks, return_exceptions=True)
            for result in results:
                if isinstance(result, FileMetadata):
                    files.append(result)
                elif isinstance(result, Exception):
                    logger.error(f"Error processing file: {result}")
                    self.stats["errors"] += 1

        self.scanned_files.extend(files)
        self.stats["files_scanned"] += len(files)
        logger.info(f"Scanned {len(files)} files in {dir_path}")
        return files

    async def _process_file_async(self, file_path: Path) -> FileMetadata:
        """Process single file async."""
        return FileMetadata.from_path(file_path)

    def _should_ignore(self, path: Path) -> bool:
        """Check if file should be ignored."""
        ignore_patterns = {
            "__pycache__",
            ".git",
            "node_modules",
            ".venv",
            ".artifacts",
            "dist",
            "build",
            "*.pyc",
            "*.log",
        }

        path_str = str(path)
        return any(pattern in path_str for pattern in ignore_patterns)

    async def analyze_with_llm(self, files: list[FileMetadata]) -> list[OptimizationSuggestion]:
        """Sử dụng LLM để analyze và suggest optimizations.

        Args:
            files: Danh sách files từ scan.

        Returns:
            Danh sách suggestions.
        """
        suggestions = []

        # Process files in batches để optimize
        batch_size = 10
        for i in range(0, len(files), batch_size):
            batch = files[i : i + batch_size]
            batch_suggestions = await self._analyze_batch(batch)
            suggestions.extend(batch_suggestions)

        self.suggestions.extend(suggestions)
        self.stats["suggestions_generated"] += len(suggestions)
        logger.info(f"Generated {len(suggestions)} optimization suggestions")
        return suggestions

    async def _analyze_batch(self, files: list[FileMetadata]) -> list[OptimizationSuggestion]:
        """Analyze batch của files."""
        suggestions = []

        for file in files:
            try:
                suggestion = await self._analyze_single_file(file)
                if suggestion:
                    suggestions.append(suggestion)
            except Exception as e:
                logger.error(f"Error analyzing {file.path}: {e}")
                self.stats["errors"] += 1

        return suggestions

    async def _analyze_single_file(self, file: FileMetadata) -> OptimizationSuggestion | None:
        """Analyze single file và tạo suggestion sử dụng LLM."""
        try:
            # Đọc nội dung file
            content = file.path.read_text(encoding="utf-8")

            # Tạo prompt cho LLM
            prompt = f"""
Analyze this {file.type} file and suggest optimizations:

File: {file.path.name}
Type: {file.type}
Lines: {file.lines}
Size: {file.size} bytes

Content:
{content[:2000]}...  # Truncate for token limits

Please provide optimization suggestions in the following format:
- Action: [refactor|optimize|add_feature|fix]
- Description: [brief description]
- Priority: [high|medium|low]
- Effort: [high|medium|low]

Focus on:
1. Code quality improvements
2. Performance optimizations
3. Security enhancements
4. Best practices compliance
5. Maintainability improvements

Response format: JSON with keys: action, description, priority, effort
"""

            # Call LLM
            response = await self.llm_service.analyze_code(prompt)

            # Parse response và tạo suggestion
            try:
                import json

                suggestion_data = json.loads(response.strip())

                return OptimizationSuggestion(
                    file=file.path,
                    action=suggestion_data.get("action", "optimize"),
                    description=suggestion_data.get("description", "LLM suggested optimization"),
                    priority=suggestion_data.get("priority", "medium"),
                    estimated_effort=suggestion_data.get("effort", "medium"),
                )
            except json.JSONDecodeError:
                # Fallback to basic heuristics nếu LLM không trả JSON
                return await self._fallback_analysis(file)

        except Exception as e:
            logger.error(f"LLM analysis failed for {file.path}: {e}")
            # Fallback to heuristics
            return await self._fallback_analysis(file)

    async def _fallback_analysis(self, file: FileMetadata) -> OptimizationSuggestion | None:
        """Fallback analysis sử dụng heuristics khi LLM fail."""
        if file.type == "python":
            return await self._analyze_python_file(file)
        elif file.type in {"typescript", "javascript"}:
            return await self._analyze_typescript_file(file)
        else:
            return await self._analyze_generic_file(file)

    async def _analyze_python_file(self, file: FileMetadata) -> OptimizationSuggestion | None:
        """Analyze Python file."""
        if file.lines > 500:
            return OptimizationSuggestion(
                file=file.path,
                action="refactor",
                description="Large file detected - consider splitting into modules",
                priority="high",
                estimated_effort="medium",
            )
        elif file.size > 10000:  # 10KB
            return OptimizationSuggestion(
                file=file.path,
                action="optimize",
                description="Add type hints and improve performance",
                priority="medium",
                estimated_effort="low",
            )
        else:
            return OptimizationSuggestion(
                file=file.path,
                action="enhance",
                description="Add comprehensive docstrings and error handling",
                priority="low",
                estimated_effort="low",
            )

    async def _analyze_typescript_file(self, file: FileMetadata) -> OptimizationSuggestion | None:
        """Analyze TypeScript/JavaScript file."""
        return OptimizationSuggestion(
            file=file.path,
            action="modernize",
            description="Update to latest TypeScript features and patterns",
            priority="medium",
            estimated_effort="low",
        )

    async def _analyze_generic_file(self, file: FileMetadata) -> OptimizationSuggestion | None:
        """Analyze generic file."""
        if file.type == "markdown" and file.size > 5000:
            return OptimizationSuggestion(
                file=file.path,
                action="optimize",
                description="Large documentation file - consider splitting",
                priority="low",
                estimated_effort="low",
            )
        return None

    async def apply_changes(self, suggestions: list[OptimizationSuggestion]) -> None:
        """Apply changes qua existing tools.

        Args:
            suggestions: Danh sách suggestions cần apply.
        """
        logger.info(f"Applying {len(suggestions)} changes...")

        # Group suggestions by action
        actions = {}
        for suggestion in suggestions:
            if suggestion.action not in actions:
                actions[suggestion.action] = []
            actions[suggestion.action].append(suggestion)

        # Apply changes using existing tools
        for action, action_suggestions in actions.items():
            try:
                await self._apply_action(action, action_suggestions)
                self.stats["changes_applied"] += len(action_suggestions)
            except Exception as e:
                logger.error(f"Failed to apply {action}: {e}")
                self.stats["errors"] += 1

    async def _apply_action(self, action: str, suggestions: list[OptimizationSuggestion]) -> None:
        """Apply specific action."""
        if action == "refactor":
            # Use ai_runner for refactoring
            await self._run_command_async(["python", "ai_runner.py", "--once", "cleanup", "--apply"])
        elif action == "optimize":
            # Use auto_apply for optimizations
            await self._run_command_async(["python", "auto_apply.py", "--commit", "--push"])
        elif action == "enhance":
            # Use ai_runner for enhancements
            await self._run_command_async(["python", "ai_runner.py", "--once", "quality", "--apply"])
        elif action == "modernize":
            # Use ai_runner for modernization
            await self._run_command_async(["python", "ai_runner.py", "--once", "ts_imports", "--apply"])

    async def _run_command_async(self, cmd: list[str]) -> None:
        """Run command async với timeout."""
        try:
            process = await asyncio.create_subprocess_# SECURITY: # SECURITY: # SECURITY: # SECURITY: # SECURITY: # SECURITY: # SECURITY: exec() removed) removed) removed) removed) removed) removed) removed
                *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE, cwd=str(ROOT)
            )

            await asyncio.wait_for(process.communicate(), timeout=300)

            if process.returncode != 0:
                raise subprocess.CalledProcessError(process.returncode, cmd)

        except TimeoutError:
            logger.error(f"Command timeout: {' '.join(cmd)}")
            raise
        except subprocess.CalledProcessError as e:
            logger.error(f"Command failed: {e}")
            raise

    async def run_quality_gates(self) -> None:
        """Chạy quality gates sau apply."""
        logger.info("Running quality gates...")

        commands = [
            ["uv", "run", "ruff", "check", "."],
            ["uv", "run", "mypy", "."],
            ["uv", "run", "pytest", "-q", "--tb=short"],
        ]

        for cmd in commands:
            try:
                await self._run_command_async(cmd)
            except subprocess.CalledProcessError:
                logger.warning(f"Quality gate failed: {' '.join(cmd)}")
                raise

        logger.info("✅ Quality gates passed")

    def save_report(self) -> None:
        """Save execution report."""
        report = {
            "timestamp": asyncio.get_event_loop().time(),
            "stats": self.stats,
            "suggestions": [s.to_dict() for s in self.suggestions],
            "files_scanned": len(self.scanned_files),
        }

        report_file = ROOT / ".artifacts" / "deepseek_agent_report.json"
        report_file.parent.mkdir(parents=True, exist_ok=True)
        report_file.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

        logger.info(f"Report saved to {report_file}")

    async def self_learn(self, suggestions: list[OptimizationSuggestion]) -> None:
        """Self-learning từ feedback để cải thiện agent.

        Args:
            suggestions: Suggestions đã apply.
        """
        # Analyze success patterns
        successful_actions = {}
        for suggestion in suggestions:
            action = suggestion.action
            if action not in successful_actions:
                successful_actions[action] = 0
            successful_actions[action] += 1

        # Update learning data
        learning_file = ROOT / ".artifacts" / "deepseek_agent_learning.json"
        learning_data = {"action_success_rates": successful_actions}

        # Ensure artifacts directory exists
        learning_file.parent.mkdir(parents=True, exist_ok=True)

        learning_file.write_text(json.dumps(learning_data, indent=2), encoding="utf-8")

        logger.info("Self-learning: updated decision model")


async def run_agent_cycle(dry_run: bool = False) -> None:
    """Chạy một cycle quét & nâng cấp.

    Args:
        dry_run: Nếu True, chỉ scan và analyze, không apply changes.
    """
    logger.info("🎯 Starting DeepSeek Agent Cycle")
    logger.info(f"Mode: {'DRY RUN' if dry_run else 'LIVE'}")

    agent = DeepSeekAgent()

    try:
        # Scan all project directories
        all_files = []
        for dir_path in PROJECT_DIRS:
            files = await agent.scan_project(dir_path)
            all_files.extend(files)

        # Analyze with LLM-like logic
        suggestions = await agent.analyze_with_llm(all_files)

        if not dry_run:
            # Apply changes
            await agent.apply_changes(suggestions)

            # Run quality gates
            await agent.run_quality_gates()

            # Self-learning
            await agent.self_learn(suggestions)

        # Save report
        agent.save_report()

        logger.info("🎉 Agent cycle completed successfully")
        logger.info(f"📊 Stats: {agent.stats}")

    except Exception as e:
        logger.error(f"Agent cycle failed: {e}")
        agent.stats["errors"] += 1
        agent.save_report()
        raise


async def main() -> None:
    """Main function để run agent."""
    import argparse

    parser = argparse.ArgumentParser(description="DeepSeek Agent - Automated Project Scanner & Upgrader")
    parser.add_argument("--dry-run", action="store_true", help="Scan and analyze only, don't apply changes")
    parser.add_argument("--once", action="store_true", help="Run once and exit")
    parser.add_argument("--continuous", action="store_true", help="Run continuously")

    args = parser.parse_args()

    if args.once:
        await run_agent_cycle(dry_run=args.dry_run)
    elif args.continuous:
        logger.info("Starting continuous mode...")
        while True:
            try:
                await run_agent_cycle(dry_run=args.dry_run)
                await asyncio.sleep(86400)  # Run daily
            except KeyboardInterrupt:
                logger.info("Stopping continuous mode...")
                break
            except Exception as e:
                logger.error(f"Continuous cycle failed: {e}")
                await asyncio.sleep(3600)  # Retry after 1 hour
    else:
        # Default: run once
        await run_agent_cycle(dry_run=args.dry_run)


if __name__ == "__main__":
    asyncio.run(main())
