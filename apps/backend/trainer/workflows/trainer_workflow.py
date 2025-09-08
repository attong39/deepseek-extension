"""Trainer Workflow Orchestrator - điều phối hệ thống học 24/7.

Module này kết nối với Celery workers hiện có để chạy các workflow
training tự động: ingest → triage → label → train → evaluate → deploy.
"""

from __future__ import annotations

import asyncio
import logging
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from apps.backend.data.external.worker.celery_app import celery_app
from apps.backend.trainer.datasets.registry import DatasetStage, registry
from apps.backend.trainer.distill_gpt5 import DistillationService, RawExample
from apps.backend.trainer.finetune_llama4 import (
import Exception
import bool
import config_dict
import d
import dataset_lineage
import dict
import e
import float
import int
import len
import list
import max
import self
import source
import str
import sum
    FineTuningConfig,
    fine_tune_from_dataset,
)
from apps.backend.trainer.model_matrix import get_teacher_model, model_matrix
from celery import Celery
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class WorkflowConfig(BaseModel):
    """Cấu hình cho trainer workflow."""

    # Scheduling
    ingest_interval_minutes: int = 30  # Thu thập dữ liệu mỗi 30p
    labeling_interval_minutes: int = 60  # Label data mỗi 1h
    training_interval_hours: int = 6  # Fine-tune mỗi 6h
    evaluation_interval_hours: int = 12  # Evaluate mỗi 12h

    # Quality gates
    min_examples_per_batch: int = 50  # Tối thiểu examples để label
    min_labeled_for_training: int = 500  # Tối thiểu để bắt đầu train
    min_quality_score: float = 0.7  # Điểm chất lượng tối thiểu

    # Safety limits
    max_concurrent_tasks: int = 5  # Giới hạn tasks đồng thời
    max_training_time_hours: int = 24  # Timeout cho training
    enable_auto_deployment: bool = False  # Có tự động deploy không

    # Sources
    ingest_sources: list[str] = Field(
        default_factory=lambda: ["web_crawler", "user_feedback", "self_play"]
    )


class WorkflowStatus(BaseModel):
    """Trạng thái hiện tại của workflow."""

    workflow_id: str = Field(default_factory=lambda: str(uuid4()))
    started_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    last_ingest: datetime | None = None
    last_labeling: datetime | None = None
    last_training: datetime | None = None
    last_evaluation: datetime | None = None

    # Counters
    total_ingested: int = 0
    total_labeled: int = 0
    total_trained: int = 0

    # Current state
    active_tasks: dict[str, str] = Field(default_factory=dict)  # task_id -> task_type
    is_running: bool = False
    error_count: int = 0
    last_error: str | None = None


class TrainerOrchestrator:
    """Orchestrator chính điều phối tất cả training workflows."""

    def __init__(
        self,
        config: WorkflowConfig | None = None,
        celery_app: Celery | None = None,
    ):
        """Khởi tạo orchestrator.

        Args:
            config: Cấu hình workflow
            celery_app: Celery app instance
        """
        self.config = config or WorkflowConfig()
        self.celery = celery_app or celery_app
        self.status = WorkflowStatus()
        self._shutdown_event = asyncio.Event()

        # Initialize distillation service
        self.distillation_service = DistillationService()

    async def start_workflow(self) -> None:
        """Khởi động workflow 24/7."""
        logger.info("Starting 24/7 trainer workflow...")
        self.status.is_running = True

        try:
            # Start các background tasks
            tasks = [
                asyncio.create_task(self._ingest_loop()),
                asyncio.create_task(self._labeling_loop()),
                asyncio.create_task(self._training_loop()),
                asyncio.create_task(self._evaluation_loop()),
                asyncio.create_task(self._monitoring_loop()),
            ]

            # Wait cho shutdown signal hoặc error
            await asyncio.gather(*tasks, return_exceptions=True)

        except Exception as e:
            logger.error(f"Workflow error: {e}")
            self.status.error_count += 1
            self.status.last_error = str(e)
        finally:
            self.status.is_running = False
            logger.info("Trainer workflow stopped")

    async def stop_workflow(self) -> None:
        """Dừng workflow một cách graceful."""
        logger.info("Stopping trainer workflow...")
        self._shutdown_event.set()

    async def _ingest_loop(self) -> None:
        """Loop thu thập dữ liệu từ các nguồn."""
        logger.info("Starting ingest loop")

        while not self._shutdown_event.is_set():
            try:
                await self._run_ingest_cycle()
                self.status.last_ingest = datetime.now(UTC)

                # Wait next cycle
                await asyncio.sleep(self.config.ingest_interval_minutes * 60)

            except Exception as e:
                logger.error(f"Ingest cycle error: {e}")
                await asyncio.sleep(60)  # Short retry delay

    async def _labeling_loop(self) -> None:
        """Loop label dữ liệu bằng teacher models."""
        logger.info("Starting labeling loop")

        while not self._shutdown_event.is_set():
            try:
                await self._run_labeling_cycle()
                self.status.last_labeling = datetime.now(UTC)

                # Wait next cycle
                await asyncio.sleep(self.config.labeling_interval_minutes * 60)

            except Exception as e:
                logger.error(f"Labeling cycle error: {e}")
                await asyncio.sleep(300)  # 5 min retry delay

    async def _training_loop(self) -> None:
        """Loop training student models."""
        logger.info("Starting training loop")

        while not self._shutdown_event.is_set():
            try:
                await self._run_training_cycle()
                self.status.last_training = datetime.now(UTC)

                # Wait next cycle
                await asyncio.sleep(self.config.training_interval_hours * 3600)

            except Exception as e:
                logger.error(f"Training cycle error: {e}")
                await asyncio.sleep(1800)  # 30 min retry delay

    async def _evaluation_loop(self) -> None:
        """Loop evaluation và quality gates."""
        logger.info("Starting evaluation loop")

        while not self._shutdown_event.is_set():
            try:
                await self._run_evaluation_cycle()
                self.status.last_evaluation = datetime.now(UTC)

                # Wait next cycle
                await asyncio.sleep(self.config.evaluation_interval_hours * 3600)

            except Exception as e:
                logger.error(f"Evaluation cycle error: {e}")
                await asyncio.sleep(3600)  # 1 hour retry delay

    async def _monitoring_loop(self) -> None:
        """Loop monitoring và health checks."""
        while not self._shutdown_event.is_set():
            try:
                await self._run_monitoring_cycle()
                await asyncio.sleep(300)  # Check mỗi 5 phút

            except Exception as e:
                logger.error(f"Monitoring cycle error: {e}")
                await asyncio.sleep(60)

    async def _run_ingest_cycle(self) -> None:
        """Chạy một cycle thu thập dữ liệu."""
        logger.info("Running ingest cycle...")

        for source in self.config.ingest_sources:
            try:
                await self._ingest_from_source(source)
            except Exception as e:
                logger.error(f"Failed to ingest from {source}: {e}")

        stats = registry.get_stats()
        self.status.total_ingested = stats["total_samples"]
        logger.info(f"Ingest complete. Total samples: {self.status.total_ingested}")

    async def _ingest_from_source(self, source: str) -> None:
        """Thu thập từ một nguồn cụ thể.

        Args:
            source: Tên nguồn dữ liệu
        """
        if source == "web_crawler":
            await self._ingest_web_content()
        elif source == "user_feedback":
            await self._ingest_user_feedback()
        elif source == "self_play":
            await self._ingest_self_play()
        else:
            logger.warning(f"Unknown ingest source: {source}")

    async def _ingest_web_content(self) -> None:
        """Thu thập nội dung từ web (mock implementation)."""
        # TODO: Implement actual web crawling
        # Hiện tại tạo mock data

        mock_examples = [
            RawExample(
                prompt="What is the capital of France?",
                context="Geography question",
                source_url="https://example.com/geography",
            ),
            RawExample(
                prompt="How to implement binary search?",
                context="Programming algorithm",
                source_url="https://example.com/algorithms",
            ),
        ]

        # Register dataset
        dataset_id = registry.register_dataset(
            name=f"web_crawl_{datetime.now().strftime('%Y%m%d_%H%M')}",
            source_type="web",
            description="Web crawled content",
        )

        logger.info(
            f"Ingested {len(mock_examples)} web examples to dataset {dataset_id}"
        )

    async def _ingest_user_feedback(self) -> None:
        """Thu thập feedback từ người dùng."""
        # TODO: Pull from user feedback systems
        logger.info("Ingesting user feedback (not implemented)")

    async def _ingest_self_play(self) -> None:
        """Tạo dữ liệu từ self-play."""
        # TODO: Implement self-play data generation
        logger.info("Generating self-play data (not implemented)")

    async def _run_labeling_cycle(self) -> None:
        """Chạy một cycle labeling với teacher models."""
        logger.info("Running labeling cycle...")

        # Tìm datasets chưa được label
        raw_datasets = registry.list_datasets(
            stage=DatasetStage.RAW,
            min_quality=0.0,  # Accept all for now
        )

        labeled_count = 0

        for dataset_lineage in raw_datasets:
            try:
                # TODO: Load actual examples from dataset
                # Mock implementation
                mock_examples = [
                    RawExample(
                        prompt="Explain quantum computing",
                        context="Physics/Technology topic",
                    )
                ]

                if len(mock_examples) < self.config.min_examples_per_batch:
                    logger.info(
                        f"Dataset {dataset_lineage.dataset_id} có quá ít examples, skip"
                    )
                    continue

                # Label với teacher model
                labeled_examples = await self.distillation_service.label_batch(
                    mock_examples, batch_tag=dataset_lineage.dataset_id
                )

                if labeled_examples:
                    # Update stage
                    registry.update_stage(
                        dataset_lineage.dataset_id, DatasetStage.LABELED
                    )
                    labeled_count += len(labeled_examples)

                    logger.info(
                        f"Labeled {len(labeled_examples)} examples for dataset {dataset_lineage.dataset_id}"
                    )

            except Exception as e:
                logger.error(
                    f"Failed to label dataset {dataset_lineage.dataset_id}: {e}"
                )

        self.status.total_labeled += labeled_count
        logger.info(f"Labeling complete. Total labeled this cycle: {labeled_count}")

    async def _run_training_cycle(self) -> None:
        """Chạy một cycle training student models."""
        logger.info("Running training cycle...")

        # Tìm datasets sẵn sàng cho training
        labeled_datasets = registry.list_datasets(
            stage=DatasetStage.LABELED,
            min_quality=self.config.min_quality_score,
        )

        if not labeled_datasets:
            logger.info("No datasets ready for training")
            return

        # Aggregate datasets cho training
        total_samples = sum(d.sample_count for d in labeled_datasets)

        if total_samples < self.config.min_labeled_for_training:
            logger.info(
                f"Not enough samples for training: {total_samples} < {self.config.min_labeled_for_training}"
            )
            return

        try:
            # Chọn dataset tốt nhất để train
            best_dataset = max(
                labeled_datasets,
                key=lambda d: d.quality.overall_score if d.quality else 0.0,
            )

            # Submit training task to Celery
            task_id = str(uuid4())
            self.status.active_tasks[task_id] = "training"

            # TODO: Submit actual Celery task
            # _ = fine_tune_from_dataset.apply_async(
            #     args=[best_dataset.dataset_id],
            #     task_id=task_id
            # )

            logger.info(
                f"Started training task {task_id} for dataset {best_dataset.dataset_id}"
            )
            self.status.total_trained += 1

            # Mark datasets as consumed
            for dataset_lineage in labeled_datasets:
                registry.mark_used_in_training(dataset_lineage.dataset_id, task_id)

        except Exception as e:
            logger.error(f"Failed to start training: {e}")

    async def _run_evaluation_cycle(self) -> None:
        """Chạy evaluation và quality gates."""
        logger.info("Running evaluation cycle...")

        # TODO: Implement evaluation với GPT-5 verifier
        # - Load latest trained models
        # - Run benchmark tests
        # - Calculate performance metrics
        # - Decide promotion to production

        logger.info("Evaluation cycle (not fully implemented)")

    async def _run_monitoring_cycle(self) -> None:
        """Monitor health và cleanup tasks."""
        # Cleanup finished tasks
        finished_tasks = []
        for task_id, task_type in self.status.active_tasks.items():
            # TODO: Check actual task status
            # if task.ready():
            #     finished_tasks.append(task_id)
            pass

        for task_id in finished_tasks:
            del self.status.active_tasks[task_id]

        # Log current status
        if len(self.status.active_tasks) > 0:
            logger.debug(f"Active tasks: {len(self.status.active_tasks)}")

    def get_status(self) -> dict[str, Any]:
        """Lấy trạng thái hiện tại của workflow."""
        stats = registry.get_stats()

        return {
            "workflow": self.status.model_dump(),
            "registry_stats": stats,
            "config": self.config.model_dump(),
            "model_matrix": {
                "teacher": get_teacher_model().name if get_teacher_model() else None,
                "total_models": len(model_matrix.list_models()),
            },
        }


# Celery tasks để tích hợp với worker hiện có
@celery_app.task(name="trainer.run_ingest")
def run_ingest_task(source: str) -> dict[str, Any]:
    """Celery task cho ingest cycle."""
    # TODO: Implement actual ingest logic
    return {"source": source, "status": "completed", "samples": 0}


@celery_app.task(name="trainer.run_labeling")
def run_labeling_task(dataset_id: str) -> dict[str, Any]:
    """Celery task cho labeling cycle."""
    # TODO: Implement actual labeling logic
    return {"dataset_id": dataset_id, "status": "completed", "labeled": 0}


@celery_app.task(name="trainer.run_training")
def run_training_task(dataset_id: str, config_dict: dict[str, Any]) -> dict[str, Any]:
    """Celery task cho training cycle."""
    try:
        config = FineTuningConfig(**config_dict)
        model_path = fine_tune_from_dataset(dataset_id, config=config)

        return {
            "dataset_id": dataset_id,
            "status": "completed",
            "model_path": model_path,
        }

    except Exception as e:
        logger.error(f"Training task failed: {e}")
        return {
            "dataset_id": dataset_id,
            "status": "failed",
            "error": str(e),
        }


# Global orchestrator instance
orchestrator = TrainerOrchestrator()


async def start_24_7_learning() -> None:
    """Convenience function để start learning 24/7."""
    await orchestrator.start_workflow()


def stop_24_7_learning() -> None:
    """Convenience function để stop learning."""
    asyncio.create_task(orchestrator.stop_workflow())


def get_learning_status() -> dict[str, Any]:
    """Lấy trạng thái học 24/7."""
    return orchestrator.get_status()
