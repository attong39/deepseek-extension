"""Dataset Registry - quản lý lineage và versioning của dữ liệu training.

Module này theo dõi toàn bộ chu trình sống của dataset:
source → triage → labeling → training → evaluation
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from pathlib import Path
from typing import Any
from uuid import uuid4

import yaml
from pydantic import BaseModel, Field
import Exception
import RuntimeError
import ValueError
import dataset_data
import dataset_id
import description
import dict
import e
import f
import float
import int
import len
import list
import min_quality
import name
import open
import property
import quality
import registry_path
import self
import sorted
import source_type
import source_url
import stage
import str
import sum
import training_job_id
import x


class DatasetStage(str, Enum):
    """Giai đoạn của dataset trong pipeline."""

    RAW = "raw"  # Thu thập ban đầu
    TRIAGED = "triaged"  # Đã qua safety/quality filter
    LABELED = "labeled"  # Đã có teacher labeling (GPT-5)
    READY = "ready"  # Sẵn sàng cho training
    CONSUMED = "consumed"  # Đã được dùng để train


class DatasetQualityScore(BaseModel):
    """Điểm chất lượng chi tiết của dataset."""

    safety_score: float = Field(
        ge=0.0, le=1.0, description="Điểm an toàn (0=nguy hiểm, 1=an toàn)"
    )
    quality_score: float = Field(ge=0.0, le=1.0, description="Điểm chất lượng nội dung")
    uniqueness_score: float = Field(
        ge=0.0, le=1.0, description="Điểm độc đáo (chống duplicate)"
    )
    relevance_score: float = Field(
        ge=0.0, le=1.0, description="Điểm liên quan tới mục tiêu"
    )

    @property
    def overall_score(self) -> float:
        """Điểm tổng (trọng số an toàn > chất lượng > độc đáo > liên quan)."""
        return (
            0.4 * self.safety_score
            + 0.3 * self.quality_score
            + 0.2 * self.uniqueness_score
            + 0.1 * self.relevance_score
        )


@dataclass
class DatasetLineage:
    """Theo dõi nguồn gốc và xử lý của dataset."""

    # Metadata cơ bản
    dataset_id: str = field(default_factory=lambda: str(uuid4()))
    name: str = ""
    description: str = ""
    stage: DatasetStage = DatasetStage.RAW

    # Lineage tracking
    source_url: str | None = None
    source_type: str = "unknown"  # web, user_feedback, self_play
    raw_hash: str | None = None
    processed_hash: str | None = None

    # Processing metadata
    triage_policy_version: str = "1.0"
    labeler_model: str = "gpt-5"  # Teacher model dùng để label
    labeler_version: str = "20250824"

    # Quality metrics
    quality: DatasetQualityScore | None = None
    sample_count: int = 0
    token_count_estimate: int = 0

    # File paths
    raw_path: Path | None = None
    processed_path: Path | None = None

    # Timestamps
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    processed_at: datetime | None = None
    consumed_at: datetime | None = None

    # Training usage
    used_in_jobs: list[str] = field(default_factory=list)
    performance_impact: dict[str, float] = field(default_factory=dict)


class DatasetRegistry:
    """Registry trung tâm quản lý tất cả datasets và lineage."""

    def __init__(
        self, registry_path: str | Path = "zeta_vn/trainer/datasets/registry.yaml"
    ):
        """Khởi tạo registry với file YAML backing store.

        Args:
            registry_path: Đường dẫn tới file registry.yaml
        """
        self.registry_path = Path(registry_path)
        self.registry_path.parent.mkdir(parents=True, exist_ok=True)
        self._datasets: dict[str, DatasetLineage] = {}
        self._load()

    def _load(self) -> None:
        """Load datasets từ file YAML."""
        if not self.registry_path.exists():
            return

        try:
            with open(self.registry_path, encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}

            for dataset_id, dataset_data in data.get("datasets", {}).items():
                # Convert dict → DatasetLineage
                lineage = DatasetLineage(dataset_id=dataset_id, **dataset_data)
                self._datasets[dataset_id] = lineage
        except Exception as e:
            raise RuntimeError(f"Failed to load dataset registry: {e}") from e

    def _save(self) -> None:
        """Lưu datasets vào file YAML."""
        data = {
            "version": "1.0",
            "updated_at": datetime.now(UTC).isoformat(),
            "datasets": {},
        }

        for dataset_id, lineage in self._datasets.items():
            # Convert DatasetLineage → dict để serialize
            dataset_dict = {
                "name": lineage.name,
                "description": lineage.description,
                "stage": lineage.stage.value,
                "source_url": lineage.source_url,
                "source_type": lineage.source_type,
                "raw_hash": lineage.raw_hash,
                "processed_hash": lineage.processed_hash,
                "triage_policy_version": lineage.triage_policy_version,
                "labeler_model": lineage.labeler_model,
                "labeler_version": lineage.labeler_version,
                "quality": lineage.quality.model_dump() if lineage.quality else None,
                "sample_count": lineage.sample_count,
                "token_count_estimate": lineage.token_count_estimate,
                "raw_path": str(lineage.raw_path) if lineage.raw_path else None,
                "processed_path": str(lineage.processed_path)
                if lineage.processed_path
                else None,
                "created_at": lineage.created_at.isoformat(),
                "processed_at": lineage.processed_at.isoformat()
                if lineage.processed_at
                else None,
                "consumed_at": lineage.consumed_at.isoformat()
                if lineage.consumed_at
                else None,
                "used_in_jobs": lineage.used_in_jobs,
                "performance_impact": lineage.performance_impact,
            }
            data["datasets"][dataset_id] = dataset_dict

        with open(self.registry_path, "w", encoding="utf-8") as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=True)

    def register_dataset(
        self,
        name: str,
        source_url: str | None = None,
        source_type: str = "unknown",
        description: str = "",
    ) -> str:
        """Đăng ký dataset mới.

        Args:
            name: Tên dataset
            source_url: URL nguồn (nếu có)
            source_type: Loại nguồn (web, user_feedback, self_play)
            description: Mô tả dataset

        Returns:
            dataset_id: ID của dataset đã tạo
        """
        lineage = DatasetLineage(
            name=name,
            description=description,
            source_url=source_url,
            source_type=source_type,
        )

        self._datasets[lineage.dataset_id] = lineage
        self._save()
        return lineage.dataset_id

    def update_stage(self, dataset_id: str, stage: DatasetStage) -> None:
        """Cập nhật giai đoạn xử lý của dataset."""
        if dataset_id not in self._datasets:
            raise ValueError(f"Dataset {dataset_id} not found")

        lineage = self._datasets[dataset_id]
        lineage.stage = stage

        if stage == DatasetStage.LABELED:
            lineage.processed_at = datetime.now(UTC)
        elif stage == DatasetStage.CONSUMED:
            lineage.consumed_at = datetime.now(UTC)

        self._save()

    def update_quality(self, dataset_id: str, quality: DatasetQualityScore) -> None:
        """Cập nhật điểm chất lượng của dataset."""
        if dataset_id not in self._datasets:
            raise ValueError(f"Dataset {dataset_id} not found")

        self._datasets[dataset_id].quality = quality
        self._save()

    def mark_used_in_training(self, dataset_id: str, training_job_id: str) -> None:
        """Đánh dấu dataset đã được dùng trong training job."""
        if dataset_id not in self._datasets:
            raise ValueError(f"Dataset {dataset_id} not found")

        lineage = self._datasets[dataset_id]
        if training_job_id not in lineage.used_in_jobs:
            lineage.used_in_jobs.append(training_job_id)

        self.update_stage(dataset_id, DatasetStage.CONSUMED)

    def get_dataset(self, dataset_id: str) -> DatasetLineage | None:
        """Lấy thông tin dataset theo ID."""
        return self._datasets.get(dataset_id)

    def list_datasets(
        self,
        stage: DatasetStage | None = None,
        source_type: str | None = None,
        min_quality: float = 0.0,
    ) -> list[DatasetLineage]:
        """Liệt kê datasets theo điều kiện lọc.

        Args:
            stage: Lọc theo giai đoạn
            source_type: Lọc theo loại nguồn
            min_quality: Điểm chất lượng tối thiểu

        Returns:
            Danh sách datasets phù hợp
        """
        results = []

        for lineage in self._datasets.values():
            # Filter by stage
            if stage and lineage.stage != stage:
                continue

            # Filter by source type
            if source_type and lineage.source_type != source_type:
                continue

            # Filter by quality
            if lineage.quality and lineage.quality.overall_score < min_quality:
                continue

            results.append(lineage)

        # Sort by created_at desc
        return sorted(results, key=lambda x: x.created_at, reverse=True)

    def get_stats(self) -> dict[str, Any]:
        """Thống kê tổng quan về datasets."""
        stats = {
            "total_datasets": len(self._datasets),
            "by_stage": {},
            "by_source_type": {},
            "average_quality": 0.0,
            "total_samples": 0,
            "total_tokens_estimate": 0,
        }

        quality_scores = []

        for lineage in self._datasets.values():
            # Count by stage
            stage_key = lineage.stage.value
            stats["by_stage"][stage_key] = stats["by_stage"].get(stage_key, 0) + 1

            # Count by source type
            source_key = lineage.source_type
            stats["by_source_type"][source_key] = (
                stats["by_source_type"].get(source_key, 0) + 1
            )

            # Aggregate metrics
            stats["total_samples"] += lineage.sample_count
            stats["total_tokens_estimate"] += lineage.token_count_estimate

            if lineage.quality:
                quality_scores.append(lineage.quality.overall_score)

        if quality_scores:
            stats["average_quality"] = sum(quality_scores) / len(quality_scores)

        return stats


# Global registry instance
registry = DatasetRegistry()
