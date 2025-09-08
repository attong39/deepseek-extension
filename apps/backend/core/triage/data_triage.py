"""Data triage system for intelligent data routing and processing.

Hệ thống phân loại và định tuyến dữ liệu thông minh để tối ưu hóa
luồng xử lý và training trong hệ thống học liên tục.
"""

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any

from .safety_filters import SafetyLevel, SafetyResult, evaluate_data_safety
import Exception
import any
import bool
import c
import dict
import e
import enabled
import enumerate
import float
import i
import int
import k
import len
import list
import max
import min
import name
import rule
import rule_name
import safety_level
import safety_results
import self
import set
import str
import super
import threshold
import tuple

logger = logging.getLogger(__name__)


class DataPriority(str, Enum):
    """Mức độ ưu tiên xử lý dữ liệu."""

    CRITICAL = "critical"  # Xử lý ngay lập tức
    HIGH = "high"  # Xử lý trong 1h
    MEDIUM = "medium"  # Xử lý trong 6h
    LOW = "low"  # Xử lý trong 24h
    BACKGROUND = "background"  # Xử lý khi rảnh


class ProcessingRoute(str, Enum):
    """Tuyến đường xử lý dữ liệu."""

    IMMEDIATE_TRAINING = "immediate_training"  # Đưa vào training ngay
    BATCH_PROCESSING = "batch_processing"  # Xử lý theo batch
    QUALITY_REVIEW = "quality_review"  # Cần review chất lượng
    HUMAN_ANNOTATION = "human_annotation"  # Cần human labeling
    ARCHIVE = "archive"  # Lưu trữ để sau
    REJECT = "reject"  # Từ chối xử lý


class DataSource(str, Enum):
    """Nguồn dữ liệu."""

    USER_INTERACTION = "user_interaction"
    SYSTEM_GENERATED = "system_generated"
    EXTERNAL_API = "external_api"
    FILE_UPLOAD = "file_upload"
    WEB_SCRAPING = "web_scraping"
    DATABASE_SYNC = "database_sync"
    REAL_TIME_STREAM = "real_time_stream"


@dataclass
class DataItem:
    """Đại diện cho một item dữ liệu cần được triage."""

    id: str
    content: str
    source: DataSource
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: dict[str, Any] = field(default_factory=dict)
    size_bytes: int = 0
    format_type: str = "text"

    def __post_init__(self):
        if self.size_bytes == 0:
            self.size_bytes = len(self.content.encode("utf-8"))


@dataclass
class TriageDecision:
    """Quyết định triage cho một data item."""

    item_id: str
    priority: DataPriority
    route: ProcessingRoute
    safety_level: SafetyLevel
    confidence: float
    reasons: list[str]
    suggested_actions: list[str]
    estimated_processing_time: int  # seconds
    resource_requirements: dict[str, Any]
    safety_results: list[SafetyResult] = field(default_factory=list)


class BaseTriageRule(ABC):
    """Abstract base class cho triage rules."""

    def __init__(self, name: str, weight: float = 1.0, enabled: bool = True):
        self.name = name
        self.weight = weight
        self.enabled = enabled

    @abstractmethod
    def evaluate(self, item: DataItem) -> tuple[DataPriority, ProcessingRoute, float]:
        """Đánh giá item và trả về priority, route, confidence."""


class SizeBasedRule(BaseTriageRule):
    """Rule dựa trên kích thước dữ liệu."""

    def __init__(self):
        super().__init__("size_based_rule")

        # Thresholds cho size-based routing
        self.size_thresholds = {
            1024: (DataPriority.HIGH, ProcessingRoute.IMMEDIATE_TRAINING),  # < 1KB
            10240: (DataPriority.MEDIUM, ProcessingRoute.IMMEDIATE_TRAINING),  # < 10KB
            102400: (DataPriority.MEDIUM, ProcessingRoute.BATCH_PROCESSING),  # < 100KB
            1048576: (DataPriority.LOW, ProcessingRoute.BATCH_PROCESSING),  # < 1MB
        }

    def evaluate(self, item: DataItem) -> tuple[DataPriority, ProcessingRoute, float]:
        """Route dựa trên kích thước file."""
        size = item.size_bytes

        for threshold, (priority, route) in self.size_thresholds.items():
            if size <= threshold:
                confidence = 0.8  # High confidence for size-based decisions
                return priority, route, confidence

        # Very large files -> low priority batch processing
        return DataPriority.BACKGROUND, ProcessingRoute.BATCH_PROCESSING, 0.9


class SourceBasedRule(BaseTriageRule):
    """Rule dựa trên nguồn dữ liệu."""

    def __init__(self):
        super().__init__("source_based_rule")

        # Mapping source -> priority/route
        self.source_routing = {
            DataSource.USER_INTERACTION: (
                DataPriority.HIGH,
                ProcessingRoute.IMMEDIATE_TRAINING,
            ),
            DataSource.REAL_TIME_STREAM: (
                DataPriority.CRITICAL,
                ProcessingRoute.IMMEDIATE_TRAINING,
            ),
            DataSource.SYSTEM_GENERATED: (
                DataPriority.MEDIUM,
                ProcessingRoute.BATCH_PROCESSING,
            ),
            DataSource.FILE_UPLOAD: (
                DataPriority.MEDIUM,
                ProcessingRoute.QUALITY_REVIEW,
            ),
            DataSource.WEB_SCRAPING: (DataPriority.LOW, ProcessingRoute.QUALITY_REVIEW),
            DataSource.EXTERNAL_API: (
                DataPriority.MEDIUM,
                ProcessingRoute.BATCH_PROCESSING,
            ),
            DataSource.DATABASE_SYNC: (
                DataPriority.LOW,
                ProcessingRoute.BATCH_PROCESSING,
            ),
        }

    def evaluate(self, item: DataItem) -> tuple[DataPriority, ProcessingRoute, float]:
        """Route dựa trên data source."""
        source = item.source

        if source in self.source_routing:
            priority, route = self.source_routing[source]
            return priority, route, 0.7

        # Default cho unknown sources
        return DataPriority.MEDIUM, ProcessingRoute.QUALITY_REVIEW, 0.5


class ContentQualityRule(BaseTriageRule):
    """Rule dựa trên chất lượng nội dung."""

    def __init__(self):
        super().__init__("content_quality_rule")

    def evaluate(self, item: DataItem) -> tuple[DataPriority, ProcessingRoute, float]:
        """Route dựa trên quality assessment."""
        content = item.content

        # Basic quality heuristics
        quality_score = self._assess_quality(content)

        if quality_score >= 0.8:
            return DataPriority.HIGH, ProcessingRoute.IMMEDIATE_TRAINING, 0.9
        elif quality_score >= 0.6:
            return DataPriority.MEDIUM, ProcessingRoute.BATCH_PROCESSING, 0.7
        elif quality_score >= 0.4:
            return DataPriority.LOW, ProcessingRoute.QUALITY_REVIEW, 0.6
        else:
            return DataPriority.BACKGROUND, ProcessingRoute.REJECT, 0.8

    def _assess_quality(self, content: str) -> float:
        """Đánh giá nhanh chất lượng content."""
        if not content or len(content.strip()) < 10:
            return 0.0

        # Length score
        length_score = min(len(content) / 500, 1.0)  # Optimal around 500 chars

        # Word diversity score
        words = content.split()
        if len(words) < 2:
            diversity_score = 0.0
        else:
            unique_words = len(set(words))
            diversity_score = unique_words / len(words)

        # Structure score (có punctuation, capitalization)
        has_punctuation = any(c in content for c in ".!?;,")
        has_capitalization = content != content.lower()
        structure_score = (has_punctuation + has_capitalization) / 2

        # Combined score
        return length_score * 0.4 + diversity_score * 0.4 + structure_score * 0.2


class TimeBasedRule(BaseTriageRule):
    """Rule dựa trên timing và freshness."""

    def __init__(self):
        super().__init__("time_based_rule")

    def evaluate(self, item: DataItem) -> tuple[DataPriority, ProcessingRoute, float]:
        """Route dựa trên timestamp và freshness."""
        now = datetime.now()
        age_seconds = (now - item.timestamp).total_seconds()

        # Fresh data gets higher priority
        if age_seconds < 300:  # < 5 minutes
            return DataPriority.HIGH, ProcessingRoute.IMMEDIATE_TRAINING, 0.8
        elif age_seconds < 3600:  # < 1 hour
            return DataPriority.MEDIUM, ProcessingRoute.IMMEDIATE_TRAINING, 0.6
        elif age_seconds < 86400:  # < 1 day
            return DataPriority.MEDIUM, ProcessingRoute.BATCH_PROCESSING, 0.5
        else:
            return DataPriority.LOW, ProcessingRoute.BATCH_PROCESSING, 0.4


class DataTriageSystem:
    """Hệ thống triage chính để phân loại và định tuyến dữ liệu."""

    def __init__(self):
        self.rules: list[BaseTriageRule] = [
            SizeBasedRule(),
            SourceBasedRule(),
            ContentQualityRule(),
            TimeBasedRule(),
        ]

        # Processing time estimates (seconds)
        self.processing_estimates = {
            ProcessingRoute.IMMEDIATE_TRAINING: 60,
            ProcessingRoute.BATCH_PROCESSING: 300,
            ProcessingRoute.QUALITY_REVIEW: 1800,
            ProcessingRoute.HUMAN_ANNOTATION: 3600,
            ProcessingRoute.ARCHIVE: 10,
            ProcessingRoute.REJECT: 1,
        }

        # Resource requirements
        self.resource_requirements = {
            ProcessingRoute.IMMEDIATE_TRAINING: {
                "cpu": 2,
                "memory": "1GB",
                "gpu": False,
            },
            ProcessingRoute.BATCH_PROCESSING: {
                "cpu": 1,
                "memory": "512MB",
                "gpu": False,
            },
            ProcessingRoute.QUALITY_REVIEW: {"cpu": 1, "memory": "256MB", "gpu": False},
            ProcessingRoute.HUMAN_ANNOTATION: {"cpu": 0, "memory": "0MB", "gpu": False},
            ProcessingRoute.ARCHIVE: {"cpu": 0, "memory": "64MB", "gpu": False},
            ProcessingRoute.REJECT: {"cpu": 0, "memory": "0MB", "gpu": False},
        }

    def add_rule(self, rule: BaseTriageRule) -> None:
        """Thêm triage rule mới."""
        self.rules.append(rule)

    def remove_rule(self, rule_name: str) -> bool:
        """Remove triage rule theo tên."""
        for i, rule in enumerate(self.rules):
            if rule.name == rule_name:
                del self.rules[i]
                return True
        return False

    def triage_item(self, item: DataItem) -> TriageDecision:
        """Thực hiện triage cho một data item."""
        # Đầu tiên check safety
        safety_level, safety_results = evaluate_data_safety(item.content, item.metadata)

        # Nếu không safe, route trực tiếp
        if safety_level == SafetyLevel.BLOCKED:
            return TriageDecision(
                item_id=item.id,
                priority=DataPriority.BACKGROUND,
                route=ProcessingRoute.REJECT,
                safety_level=safety_level,
                confidence=1.0,
                reasons=["Blocked by safety filters"],
                suggested_actions=["Manual review required"],
                estimated_processing_time=1,
                resource_requirements=self.resource_requirements[
                    ProcessingRoute.REJECT
                ],
                safety_results=safety_results,
            )

        # Collect decisions từ tất cả rules
        rule_decisions = []
        total_weight = 0.0

        for rule in self.rules:
            if not rule.enabled:
                continue

            try:
                priority, route, confidence = rule.evaluate(item)
                rule_decisions.append(
                    {
                        "rule": rule.name,
                        "priority": priority,
                        "route": route,
                        "confidence": confidence,
                        "weight": rule.weight,
                    }
                )
                total_weight += rule.weight

            except Exception as e:
                logger.error(f"Error in rule {rule.name}: {e}")
                continue

        if not rule_decisions:
            # Fallback decision
            return self._create_fallback_decision(item, safety_level, safety_results)

        # Aggregate decisions
        final_decision = self._aggregate_decisions(
            item, rule_decisions, total_weight, safety_level, safety_results
        )

        return final_decision

    def _create_fallback_decision(
        self,
        item: DataItem,
        safety_level: SafetyLevel,
        safety_results: list[SafetyResult],
    ) -> TriageDecision:
        """Tạo fallback decision khi không có rules."""
        return TriageDecision(
            item_id=item.id,
            priority=DataPriority.MEDIUM,
            route=ProcessingRoute.QUALITY_REVIEW,
            safety_level=safety_level,
            confidence=0.1,
            reasons=["No triage rules available - using fallback"],
            suggested_actions=["Configure triage rules"],
            estimated_processing_time=self.processing_estimates[
                ProcessingRoute.QUALITY_REVIEW
            ],
            resource_requirements=self.resource_requirements[
                ProcessingRoute.QUALITY_REVIEW
            ],
            safety_results=safety_results,
        )

    def _aggregate_decisions(
        self,
        item: DataItem,
        rule_decisions: list[dict[str, Any]],
        total_weight: float,
        safety_level: SafetyLevel,
        safety_results: list[SafetyResult],
    ) -> TriageDecision:
        """Aggregate multiple rule decisions thành final decision."""

        # Score các options
        priority_scores = {}
        route_scores = {}

        for decision in rule_decisions:
            weight = decision["weight"]
            confidence = decision["confidence"]
            weighted_score = weight * confidence

            # Accumulate priority scores
            priority = decision["priority"]
            if priority not in priority_scores:
                priority_scores[priority] = 0
            priority_scores[priority] += weighted_score

            # Accumulate route scores
            route = decision["route"]
            if route not in route_scores:
                route_scores[route] = 0
            route_scores[route] += weighted_score

        # Chọn priority và route với score cao nhất
        final_priority = max(priority_scores.keys(), key=lambda k: priority_scores[k])
        final_route = max(route_scores.keys(), key=lambda k: route_scores[k])

        # Calculate confidence
        final_confidence = (
            max(priority_scores[final_priority], route_scores[final_route])
            / total_weight
        )

        # Adjust route based on safety level
        if safety_level == SafetyLevel.QUARANTINE:
            final_route = ProcessingRoute.HUMAN_ANNOTATION
            final_priority = DataPriority.LOW

        # Collect reasons
        reasons = [f"Rule aggregation: {len(rule_decisions)} rules evaluated"]
        for decision in rule_decisions:
            reasons.append(
                f"{decision['rule']}: {decision['priority']}/{decision['route']} (conf: {decision['confidence']:.2f})"
            )

        # Suggested actions
        suggested_actions = []
        if final_route == ProcessingRoute.IMMEDIATE_TRAINING:
            suggested_actions.append("Process for immediate training")
        elif final_route == ProcessingRoute.BATCH_PROCESSING:
            suggested_actions.append("Add to batch processing queue")
        elif final_route == ProcessingRoute.QUALITY_REVIEW:
            suggested_actions.append("Schedule for quality review")
        elif final_route == ProcessingRoute.HUMAN_ANNOTATION:
            suggested_actions.append("Require human annotation")
        elif final_route == ProcessingRoute.ARCHIVE:
            suggested_actions.append("Archive for future use")
        else:
            suggested_actions.append("Reject processing")

        return TriageDecision(
            item_id=item.id,
            priority=final_priority,
            route=final_route,
            safety_level=safety_level,
            confidence=final_confidence,
            reasons=reasons,
            suggested_actions=suggested_actions,
            estimated_processing_time=self.processing_estimates[final_route],
            resource_requirements=self.resource_requirements[final_route],
            safety_results=safety_results,
        )

    def batch_triage(self, items: list[DataItem]) -> list[TriageDecision]:
        """Thực hiện triage cho nhiều items cùng lúc."""
        decisions = []

        for item in items:
            try:
                decision = self.triage_item(item)
                decisions.append(decision)
            except Exception as e:
                logger.error(f"Error triaging item {item.id}: {e}")
                # Create error decision
                error_decision = TriageDecision(
                    item_id=item.id,
                    priority=DataPriority.BACKGROUND,
                    route=ProcessingRoute.QUALITY_REVIEW,
                    safety_level=SafetyLevel.QUARANTINE,
                    confidence=0.0,
                    reasons=[f"Triage error: {str(e)}"],
                    suggested_actions=["Manual investigation required"],
                    estimated_processing_time=3600,
                    resource_requirements={"cpu": 0, "memory": "0MB", "gpu": False},
                    safety_results=[],
                )
                decisions.append(error_decision)

        return decisions

    def get_queue_stats(self, decisions: list[TriageDecision]) -> dict[str, Any]:
        """Thống kê về queue từ triage decisions."""
        route_counts = {}
        priority_counts = {}
        total_processing_time = 0

        for decision in decisions:
            # Count routes
            route = decision.route
            if route not in route_counts:
                route_counts[route] = 0
            route_counts[route] += 1

            # Count priorities
            priority = decision.priority
            if priority not in priority_counts:
                priority_counts[priority] = 0
            priority_counts[priority] += 1

            # Sum processing time
            total_processing_time += decision.estimated_processing_time

        return {
            "total_items": len(decisions),
            "routes": route_counts,
            "priorities": priority_counts,
            "estimated_total_time_seconds": total_processing_time,
            "estimated_total_time_hours": total_processing_time / 3600,
        }


# Singleton instance
_triage_system = None


def get_data_triage_system() -> DataTriageSystem:
    """Get singleton instance của data triage system."""
    global _triage_system
    if _triage_system is None:
        _triage_system = DataTriageSystem()
    return _triage_system


def triage_data_item(
    content: str,
    source: DataSource,
    metadata: dict[str, Any] = None,
    item_id: str | None = None,
) -> TriageDecision:
    """Convenience function để triage một data item."""
    if item_id is None:
        import uuid

        item_id = str(uuid.uuid4())

    if metadata is None:
        metadata = {}

    item = DataItem(id=item_id, content=content, source=source, metadata=metadata)

    triage = get_data_triage_system()
    return triage.triage_item(item)
