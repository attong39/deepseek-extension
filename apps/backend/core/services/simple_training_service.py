"""
Simple Training Service cho Desktop Integration Demo
Lightweight implementation cho WebSocket progress tracking
"""

from __future__ import annotations

import asyncio
import uuid
from collections.abc import Callable
from datetime import UTC, datetime
from typing import Any

from app.api.v1._schemas import TrainingJob, TrainingJobCreate
import Exception
import ValueError
import action
import bool
import callback
import channel
import dict
import e
import epoch
import int
import j
import limit
import list
import min
import payload
import range
import req
import self
import step
import str


class EventBus:
    """Simple EventBus cho demo"""

    def __init__(self) -> None:
        self.subscribers: dict[str, list[Callable[[dict[str, Any]], None]]] = {}

    def subscribe(
        self, channel: str, callback: Callable[[dict[str, Any]], None]
    ) -> None:
        """Subscribe to channel với callback"""
        if channel not in self.subscribers:
            self.subscribers[channel] = []
        self.subscribers[channel].append(callback)

    async def publish(self, channel: str, payload: dict[str, Any]) -> None:
        """Async publish message to channel"""
        callbacks = self.subscribers.get(channel, [])
        for callback in callbacks:
            try:
                callback(payload)
            except Exception:
                # Ignore callback errors
                pass


class SimpleTrainingService:
    """Simple training service for demo/integration"""

    def __init__(self) -> None:
        self.jobs: dict[str, TrainingJob] = {}
        self._paused: dict[str, bool] = {}
        self._cancelled: dict[str, bool] = {}
        self.bus = EventBus()
        self._tasks: list[asyncio.Task[None]] = []

    async def start_job(self, req: TrainingJobCreate) -> TrainingJob:
        """Bắt đầu training job mới"""
        job_id = f"j_{uuid.uuid4().hex[:12]}"
        now = datetime.now(UTC)

        job = TrainingJob(
            id=job_id,
            name=req.name,
            status="PENDING",
            progress=0.0,
            created_at=now,
            updated_at=now,
            model=req.model,
            lr=req.lr,
            epochs=req.epochs,
            current_epoch=0,
            dataset_file_ids=req.dataset_file_ids,
        )

        self.jobs[job_id] = job
        self._paused[job_id] = False
        self._cancelled[job_id] = False

        # Bắt đầu background task
        task = asyncio.create_task(self._run_training(job_id))
        self._tasks.append(task)

        return job

    def get_job(self, job_id: str) -> TrainingJob | None:
        """Lấy thông tin job"""
        return self.jobs.get(job_id)

    def list_jobs(self, limit: int = 50) -> list[TrainingJob]:
        """Lấy danh sách jobs"""
        jobs = list(self.jobs.values())
        jobs.sort(key=lambda j: j.created_at, reverse=True)
        return jobs[:limit]

    async def control_job(self, job_id: str, action: str) -> TrainingJob:
        """Control job: pause/resume/cancel"""
        job = self.jobs.get(job_id)
        if not job:
            raise ValueError(f"Job {job_id} không tồn tại")

        if action == "pause" and job.status == "RUNNING":
            job.status = "PAUSED"
            self._paused[job_id] = True
        elif action == "resume" and job.status == "PAUSED":
            job.status = "RUNNING"
            self._paused[job_id] = False
        elif action == "cancel":
            job.status = "CANCELLED"
            self._cancelled[job_id] = True
        else:
            raise ValueError(f"Action không hợp lệ: {action}")

        job.updated_at = datetime.now(UTC)

        # Emit status change
        await self.bus.publish(
            f"training:{job_id}",
            {
                "type": "status",
                "job_id": job_id,
                "status": job.status,
                "progress": job.progress,
                "timestamp": job.updated_at.isoformat(),
            },
        )

        return job

    async def _run_training(self, job_id: str) -> None:
        """Background training simulation"""
        job = self.jobs[job_id]

        try:
            job.status = "RUNNING"
            job.updated_at = datetime.now(UTC)

            await self.bus.publish(
                f"training:{job_id}",
                {
                    "type": "status",
                    "job_id": job_id,
                    "status": "RUNNING",
                    "progress": 0.0,
                    "timestamp": job.updated_at.isoformat(),
                },
            )

            total_steps = job.epochs * 100

            for epoch in range(1, job.epochs + 1):
                job.current_epoch = epoch

                for step in range(100):
                    if self._cancelled.get(job_id, False):
                        return

                    while self._paused.get(job_id, False):
                        await asyncio.sleep(0.3)
                        if self._cancelled.get(job_id, False):
                            return

                    current_step = (epoch - 1) * 100 + step + 1
                    job.progress = min(1.0, current_step / total_steps)
                    job.loss = 2.0 * (1.0 - job.progress) + 0.1
                    job.updated_at = datetime.now(UTC)

                    if step % 10 == 0:
                        await self.bus.publish(
                            f"training:{job_id}",
                            {
                                "type": "progress",
                                "job_id": job_id,
                                "progress": job.progress,
                                "current_epoch": job.current_epoch,
                                "loss": job.loss,
                                "timestamp": job.updated_at.isoformat(),
                            },
                        )

                    await asyncio.sleep(0.1)

            job.status = "SUCCEEDED"
            job.progress = 1.0
            job.updated_at = datetime.now(UTC)

            await self.bus.publish(
                f"training:{job_id}",
                {
                    "type": "done",
                    "job_id": job_id,
                    "status": "SUCCEEDED",
                    "progress": 1.0,
                    "timestamp": job.updated_at.isoformat(),
                },
            )

        except Exception as e:
            job.status = "FAILED"
            job.updated_at = datetime.now(UTC)

            await self.bus.publish(
                f"training:{job_id}",
                {
                    "type": "error",
                    "job_id": job_id,
                    "status": "FAILED",
                    "message": str(e),
                    "timestamp": job.updated_at.isoformat(),
                },
            )


# Singleton instance for demo
simple_training_service = SimpleTrainingService()
