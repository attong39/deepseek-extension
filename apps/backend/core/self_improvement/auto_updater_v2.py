from __future__ import annotations
import ValueError
import any
import bool
import ch
import dict
import g
import generator
import goal
import history_path
import i
import int
import iterations
import len
import list
import max_iters
import msgs
import p
import pat
import policy
import range
import self
import set
import str
import tuple
import updater
import w

"""Self‑improvement Orchestrator (v2)

V2 mở rộng AutoUpdater với vòng lặp *Plan → Apply → Evaluate → Reflect*:
- Cho phép cắm *PatchGenerator* bên ngoài (LLM hoặc rule‑based)
- Lưu lịch sử vào JSONL (idempotent, dễ audit/rollback)
- Cơ chế feedback: chuyển log quality gates/trace về generator để cải thiện ở vòng sau
- Chính sách an toàn: số file tối đa, thư mục cho phép, deny‑list pattern
"""

import json
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Protocol

from apps.backend.core.self_improvement.auto_updater import (
    AutoUpdater,
    Patch,
    PatchResult,
    QualityGateSpec,
)
from pydantic import BaseModel, Field


# ----------------------
# Interfaces & models
# ----------------------
class PatchGenerator(Protocol):
    async def generate(
        self, goal: ImprovementGoal, *, iteration: int, feedback: str | None
    ) -> Patch: ...

    async def acknowledge(self, iteration: int, result: PatchResult) -> None: ...


class ImprovementGoal(BaseModel):
    """Mục tiêu cải tiến (ngắn gọn, có thể trace)."""

    title: str
    description: str | None = None
    # Ví dụ: {"area": "performance", "target": "p95<100ms"}
    metadata: dict[str, str] = Field(default_factory=dict)


class IterationLog(BaseModel):
    iteration: int
    patch_id: str
    started_at: datetime
    finished_at: datetime
    passed: bool
    errors: list[str] = Field(default_factory=list)
    gates: list[dict] = Field(default_factory=list)


class SelfImproveResult(BaseModel):
    goal: ImprovementGoal
    success: bool
    iterations: list[IterationLog]
    last_result: PatchResult | None = None


@dataclass
class Policy:
    max_changed_files: int = 40
    allow_globs: tuple[str, ...] = (
        "zeta_vn/**",
        "tests/**",
        "pyproject.toml",
        ".github/**",
    )
    deny_globs: tuple[str, ...] = (
        "**/.env",
        "**/secrets.*",
        "**/.env.*",
        "**/*.bin",
        "**/tessdata/**",
    )


# ----------------------
# Orchestrator
# ----------------------
class AutoUpdaterV2:
    """Điều phối self‑improvement nhiều vòng lặp.

    Parameters:
        updater: AutoUpdater (v1) đã cấu hình repo + runner.
        policy: ràng buộc an toàn khi áp patch.
        history_path: file JSONL để lưu vết mỗi iteration.
    """

    def __init__(
        self,
        updater: AutoUpdater,
        *,
        policy: Policy | None = None,
        history_path: str | Path | None = None,
    ) -> None:
        self.updater = updater
        self.policy = policy or Policy()
        self.history_path = Path(history_path) if history_path else None

    async def run(
        self,
        goal: ImprovementGoal,
        generator: PatchGenerator,
        *,
        max_iters: int = 3,
        qg: QualityGateSpec | None = None,
    ) -> SelfImproveResult:
        qg = qg or QualityGateSpec()
        iterations: list[IterationLog] = []
        feedback: str | None = None
        last: PatchResult | None = None

        for i in range(1, max_iters + 1):
            t0 = datetime.now(UTC)
            patch = await generator.generate(goal, iteration=i, feedback=feedback)
            self._enforce_policy(patch)

            res = await self.updater.apply_patch(patch, qg)
            t1 = datetime.now(UTC)
            last = res

            log = IterationLog(
                iteration=i,
                patch_id=patch.id,
                started_at=t0,
                finished_at=t1,
                passed=res.passed_quality_gates,
                errors=res.errors[:],
                gates=[g.model_dump() for g in res.gates],
            )
            iterations.append(log)
            self._append_history(goal, log)

            await generator.acknowledge(i, res)

            if res.passed_quality_gates:
                return SelfImproveResult(
                    goal=goal, success=True, iterations=iterations, last_result=res
                )

            # Tạo feedback ngắn gọn từ lỗi/gates để vòng sau sửa
            feedback = self._format_feedback(res)

        return SelfImproveResult(
            goal=goal, success=False, iterations=iterations, last_result=last
        )

    # ----------------------
    # Helpers
    # ----------------------
    def _append_history(self, goal: ImprovementGoal, log: IterationLog) -> None:
        if not self.history_path:
            return
        rec = {
            "ts": datetime.now(UTC).isoformat(),
            "goal": goal.model_dump(),
            "iteration": log.model_dump(),
        }
        self.history_path.parent.mkdir(parents=True, exist_ok=True)
        with self.history_path.open("a", encoding="utf-8") as w:
            w.write(json.dumps(rec, ensure_ascii=False) + "\n")

    def _format_feedback(self, res: PatchResult) -> str:
        msgs: list[str] = []
        if res.errors:
            msgs.append("Errors: " + "; ".join(res.errors))
        for g in res.gates:
            if g.exit_code != 0:
                msgs.append(
                    f"Gate FAIL: {g.cmd} → rc={g.exit_code}; tail: {g.stderr.strip()[:400]}"
                )
        return "\n".join(msgs) if msgs else "quality gates failed"

    def _enforce_policy(self, patch: Patch) -> None:
        # Số file đổi
        seen_paths = set()
        for ch in patch.changes:
            seen_paths.add(ch.path)
            if ch.new_path:
                seen_paths.add(ch.new_path)
        if len(seen_paths) > self.policy.max_changed_files:
            raise ValueError(
                f"patch touches too many files: {len(seen_paths)} > {self.policy.max_changed_files}"
            )

        # Deny‑list patterns
        from fnmatch import fnmatch

        def _deny(p: str) -> bool:
            return any(fnmatch(p, pat) for pat in self.policy.deny_globs)

        def _allow(p: str) -> bool:
            return any(fnmatch(p, pat) for pat in self.policy.allow_globs)

        for p in seen_paths:
            if _deny(p):
                raise ValueError(f"path denied by policy: {p}")
            if not _allow(p):
                raise ValueError(f"path not allowed by policy: {p}")
