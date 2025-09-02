"""
Core domain entities cho hệ thống distillation.
Định nghĩa các entity chính: TeacherLabel, DistillationDatapoint
"""

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Optional


class LabelConfidence(Enum):
    """Mức độ tin cậy của teacher label"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"


class ModelType(Enum):
    """Loại model trong hệ thống"""
    TEACHER = "teacher"
    STUDENT = "student"


@dataclass
class TeacherLabel:
    """
    Label được generate bởi teacher model.
    Chứa thông tin về prediction và confidence score.
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    input_text: str = ""
    predicted_label: str = ""
    confidence_score: float = 0.0
    confidence_level: LabelConfidence = LabelConfidence.LOW
    model_name: str = ""
    model_version: str = ""
    processing_time_ms: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)

    def __post_init__(self):
        """Validate và set confidence level dựa trên score"""
        if not 0.0 <= self.confidence_score <= 1.0:
            raise ValueError("Confidence score phải trong khoảng [0.0, 1.0]")

        # Tự động set confidence level
        if self.confidence_score >= 0.9:
            self.confidence_level = LabelConfidence.VERY_HIGH
        elif self.confidence_score >= 0.7:
            self.confidence_level = LabelConfidence.HIGH
        elif self.confidence_score >= 0.5:
            self.confidence_level = LabelConfidence.MEDIUM
        else:
            self.confidence_level = LabelConfidence.LOW

    @property
    def is_cacheable(self) -> bool:
        """Kiểm tra xem label này có thể cache được không (confidence cao)"""
        return self.confidence_level in [LabelConfidence.HIGH, LabelConfidence.VERY_HIGH]

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "id": self.id,
            "input_text": self.input_text,
            "predicted_label": self.predicted_label,
            "confidence_score": self.confidence_score,
            "confidence_level": self.confidence_level.value,
            "model_name": self.model_name,
            "model_version": self.model_version,
            "processing_time_ms": self.processing_time_ms,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
        }


@dataclass
class DistillationDatapoint:
    """
    Một datapoint trong quá trình distillation.
    Bao gồm input, teacher label, và student prediction (nếu có).
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    input_data: str = ""
    teacher_label: Optional[TeacherLabel] = None
    student_prediction: Optional[str] = None
    student_confidence: Optional[float] = None
    loss_value: Optional[float] = None
    dataset_name: str = ""
    batch_id: str = ""
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def __post_init__(self):
        """Validate student confidence if provided"""
        if self.student_confidence is not None:
            if not 0.0 <= self.student_confidence <= 1.0:
                raise ValueError("Student confidence phải trong khoảng [0.0, 1.0]")

    @property
    def has_teacher_label(self) -> bool:
        """Kiểm tra xem có teacher label hay không"""
        return self.teacher_label is not None

    @property
    def has_student_prediction(self) -> bool:
        """Kiểm tra xem có student prediction hay không"""
        return self.student_prediction is not None

    @property
    def is_complete(self) -> bool:
        """Kiểm tra xem datapoint đã complete (có cả teacher và student)"""
        return self.has_teacher_label and self.has_student_prediction

    def calculate_agreement(self) -> Optional[bool]:
        """Tính toán xem teacher và student có đồng ý không"""
        if not self.is_complete:
            return None
        return self.teacher_label.predicted_label == self.student_prediction

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "id": self.id,
            "input_data": self.input_data,
            "teacher_label": self.teacher_label.to_dict() if self.teacher_label else None,
            "student_prediction": self.student_prediction,
            "student_confidence": self.student_confidence,
            "loss_value": self.loss_value,
            "dataset_name": self.dataset_name,
            "batch_id": self.batch_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


@dataclass
class BatchProcessingResult:
    """
    Kết quả của một batch processing operation.
    """
    batch_id: str
    total_items: int
    successful_items: int
    failed_items: int
    processing_time_ms: float
    average_confidence: float
    cached_items: int = 0
    errors: list[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)

    @property
    def success_rate(self) -> float:
        """Tính tỷ lệ thành công"""
        if self.total_items == 0:
            return 0.0
        return self.successful_items / self.total_items

    @property
    def cache_hit_rate(self) -> float:
        """Tính tỷ lệ cache hit"""
        if self.total_items == 0:
            return 0.0
        return self.cached_items / self.total_items

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "batch_id": self.batch_id,
            "total_items": self.total_items,
            "successful_items": self.successful_items,
            "failed_items": self.failed_items,
            "processing_time_ms": self.processing_time_ms,
            "average_confidence": self.average_confidence,
            "cached_items": self.cached_items,
            "success_rate": self.success_rate,
            "cache_hit_rate": self.cache_hit_rate,
            "errors": self.errors,
            "created_at": self.created_at.isoformat(),
        }


# Type aliases for better code readability
TeacherLabelList = list[TeacherLabel]
DistillationDatapointList = list[DistillationDatapoint]
BatchResults = list[BatchProcessingResult]
