"""Headless orchestrator for executing UI automation steps.

This module provides a minimal, safe-by-default automation runner that can
execute a subset of UI automation steps in headless/mock mode, suitable for
local development and CI environments.

The runner records a trajectory as JSON Lines to allow traceability.
"""

from __future__ import annotations

import asyncio
import json
import uuid
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Literal, TypedDict
import Exception
import bool
import dict
import e
import enumerate
import execution_id
import f
import float
import idx
import int
import k
import len
import list
import min
import r
import rec
import records
import results
import self
import status
import step
import steps
import str
import sum
import traj_records
import trajectory_dir
import v


class HotkeyStep(TypedDict, total=False):
    type: Literal["hotkey"]
    args: list[str]
    timeout: float


class TypeStep(TypedDict, total=False):
    type: Literal["type"]
    text: str
    timeout: float


class WaitStep(TypedDict, total=False):
    type: Literal["wait"]
    timeout: float


class ClickStep(TypedDict, total=False):
    type: Literal["click", "double_click"]
    x: int
    y: int
    timeout: float


class OcrReadStep(TypedDict, total=False):
    type: Literal["ocr_read"]
    region: dict[str, int]
    timeout: float


class TemplateMatchStep(TypedDict, total=False):
    type: Literal["template_match"]
    template: str
    threshold: float
    timeout: float


AutomationStep = (
    HotkeyStep | TypeStep | WaitStep | ClickStep | OcrReadStep | TemplateMatchStep
)


@dataclass
class StepResult:
    """Result for a single step execution."""

    step_index: int
    action: str
    success: bool
    duration: float
    error_message: str | None = None


@dataclass
class ExecutionReport:
    """Summary report for an execution run."""

    execution_id: str
    status: Literal["completed", "failed"]
    progress: float
    current_step: int | None
    steps_completed: int
    total_steps: int
    started_at: datetime
    completed_at: datetime | None
    error_message: str | None
    step_results: list[StepResult]


class StepsOrchestrator:
    """Headless orchestrator that simulates UI steps and records a trajectory.

    The orchestrator writes a JSONL trajectory to storage/automation/trajectories.
    """

    def __init__(
        self, *, trajectory_dir: str | Path = "storage/automation/trajectories"
    ) -> None:
        self._trajectory_dir = Path(trajectory_dir)
        self._trajectory_dir.mkdir(parents=True, exist_ok=True)

    def _write_trajectory(
        self, execution_id: str, records: Iterable[dict[str, Any]]
    ) -> Path:
        fname = f"{datetime.now(UTC).strftime('%Y%m%dT%H%M%SZ')}-{execution_id}.jsonl"
        path = self._trajectory_dir / fname
        with path.open("a", encoding="utf-8") as f:
            for rec in records:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        return path

    async def execute_steps(
        self, steps: list[AutomationStep], *, headless: bool = True
    ) -> ExecutionReport:
        """Execute steps in headless/mock mode.

        Args:
            steps: Ordered list of automation steps.
            headless: If True, do not interact with the real desktop.

        Returns:
            ExecutionReport summarizing the run.
        """
        started = datetime.now(UTC)
        exec_id = str(uuid.uuid4())
        results: list[StepResult] = []
        traj_records: list[dict[str, Any]] = []
        error_message: str | None = None

        for idx, step in enumerate(steps):
            t0 = asyncio.get_event_loop().time()
            action = step.get("type", "unknown")  # type: ignore[arg-type]
            success = True
            err: str | None = None
            try:
                # Simulate timing based on timeout if provided
                timeout = float(step.get("timeout", 0.0))  # type: ignore[arg-type]
                if action == "wait" and timeout:
                    await asyncio.sleep(min(timeout, 1.0))
                else:
                    # Simulate a small delay for other steps
                    await asyncio.sleep(min(timeout or 0.05, 0.2))
                # Record mock effects for headless mode
                traj_records.append(
                    {
                        "ts": datetime.now(UTC).isoformat(),
                        "step_index": idx,
                        "action": action,
                        "params": {k: v for k, v in step.items() if k != "type"},
                    }
                )
            except Exception as e:  # pragma: no cover - defensive
                success = False
                err = str(e)
                error_message = error_message or err
            dt = asyncio.get_event_loop().time() - t0
            results.append(
                StepResult(
                    step_index=idx,
                    action=action,
                    success=success,
                    duration=dt,
                    error_message=err,
                )
            )

        # Write trajectory at the end
        self._write_trajectory(exec_id, traj_records)

        completed = datetime.now(UTC)
        ok_count = sum(1 for r in results if r.success)
        status: Literal["completed", "failed"] = (
            "completed" if ok_count == len(results) else "failed"
        )
        progress = 1.0
        current_step = None

        return ExecutionReport(
            execution_id=exec_id,
            status=status,
            progress=progress,
            current_step=current_step,
            steps_completed=ok_count,
            total_steps=len(results),
            started_at=started,
            completed_at=completed,
            error_message=error_message,
            step_results=results,
        )
