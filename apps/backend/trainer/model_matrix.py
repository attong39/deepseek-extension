"""Model Matrix - routing AI models theo tác vụ và chi phí.

Module này quản lý ma trận model selection để chọn model phù hợp
cho từng loại tác vụ (teacher/student, reasoning/realtime/edge).
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import bool
import dict
import float
import input_tokens
import int
import list
import local_only
import m
import max_cost_tier
import max_latency_ms
import model_name
import name
import output_tokens
import provider
import require_local
import role
import self
import sorted
import str
import task


class ModelRole(str, Enum):
    """Vai trò của model trong hệ thống."""

    TEACHER = "teacher"  # GPT-5 cho labeling/verification
    STUDENT = "student"  # Llama 4, Qwen cho inference
    VERIFIER = "verifier"  # GPT-5 cho evaluation gate
    REALTIME = "realtime"  # GPT-4o cho multimodal realtime
    EDGE = "edge"  # GPT-4.1-nano cho on-device
    SPECIALIST = "specialist"  # Qwen2.5-VL cho vision, etc.


class TaskType(str, Enum):
    """Loại tác vụ cần model xử lý."""

    REASONING = "reasoning"  # Suy luận phức tạp
    CODING = "coding"  # Viết/debug code
    PLANNING = "planning"  # Agent planning
    LABELING = "labeling"  # Teacher labeling data
    VERIFICATION = "verification"  # Verify outputs
    MULTIMODAL = "multimodal"  # Xử lý ảnh/video/giọng nói
    DOCUMENT_VISION = "document_vision"  # Parse PDF/bảng/layout
    CHAT = "chat"  # Chat thường
    FUNCTION_CALLING = "function_calling"  # Tool use
    EDGE_TRIGGER = "edge_trigger"  # On-device light tasks
    DISTILLATION = "distillation"  # Knowledge distillation


class CostTier(str, Enum):
    """Mức chi phí sử dụng model."""

    FREE = "free"  # Local/open-weight models
    LOW = "low"  # Cheap API calls
    MEDIUM = "medium"  # Standard API
    HIGH = "high"  # Premium API (GPT-5)
    PREMIUM = "premium"  # Advanced features


@dataclass
class ModelSpec:
    """Thông số kỹ thuật của một AI model."""

    # Basic info
    name: str
    provider: str  # openai, meta, alibaba, local
    model_id: str  # API model name
    role: ModelRole
    supported_tasks: list[TaskType]
    max_context_tokens: int
    cost_tier: CostTier

    # Capabilities with defaults
    supports_function_calling: bool = False
    supports_multimodal: bool = False
    supports_streaming: bool = True

    # Performance & Cost with defaults
    cost_per_1k_tokens: float = 0.0  # USD
    avg_latency_ms: int = 1000
    throughput_tps: float = 10.0  # tokens per second

    # Deployment with defaults
    requires_api_key: bool = True
    can_run_local: bool = False
    gpu_memory_gb: float | None = None  # Nếu chạy local

    # Quality metrics with defaults
    benchmark_score: float = 0.0  # Composite score
    reliability_score: float = 1.0  # 0-1, reliability

    def __str__(self) -> str:
        return f"{self.name} ({self.provider}, {self.role.value})"


class ModelMatrix:
    """Ma trận routing model theo tác vụ và ràng buộc."""

    def __init__(self):
        """Khởi tạo với model portfolio mặc định."""
        self._models: dict[str, ModelSpec] = {}
        self._init_default_models()

    def _init_default_models(self) -> None:
        """Thiết lập danh sách model mặc định theo khuyến nghị."""

        # Teacher models (high-end)
        self.register_model(
            ModelSpec(
                name="GPT-5",
                provider="openai",
                model_id="gpt-5",
                role=ModelRole.TEACHER,
                supported_tasks=[
                    TaskType.REASONING,
                    TaskType.CODING,
                    TaskType.PLANNING,
                    TaskType.LABELING,
                    TaskType.VERIFICATION,
                    TaskType.FUNCTION_CALLING,
                ],
                max_context_tokens=200_000,
                supports_function_calling=True,
                cost_tier=CostTier.HIGH,
                cost_per_1k_tokens=0.10,  # Ước tính
                avg_latency_ms=3000,
                throughput_tps=15.0,
                benchmark_score=95.0,
            )
        )

        # Realtime multimodal
        self.register_model(
            ModelSpec(
                name="GPT-4o",
                provider="openai",
                model_id="gpt-4o",
                role=ModelRole.REALTIME,
                supported_tasks=[
                    TaskType.MULTIMODAL,
                    TaskType.CHAT,
                    TaskType.FUNCTION_CALLING,
                ],
                max_context_tokens=128_000,
                supports_function_calling=True,
                supports_multimodal=True,
                cost_tier=CostTier.MEDIUM,
                cost_per_1k_tokens=0.03,
                avg_latency_ms=500,
                throughput_tps=25.0,
                benchmark_score=88.0,
            )
        )

        # Edge model
        self.register_model(
            ModelSpec(
                name="GPT-4.1-nano",
                provider="openai",
                model_id="gpt-4.1-nano",
                role=ModelRole.EDGE,
                supported_tasks=[TaskType.EDGE_TRIGGER, TaskType.CHAT],
                max_context_tokens=16_000,
                cost_tier=CostTier.LOW,
                cost_per_1k_tokens=0.001,
                avg_latency_ms=200,
                throughput_tps=50.0,
                benchmark_score=70.0,
            )
        )

        # Open-weight teacher/student
        self.register_model(
            ModelSpec(
                name="GPT-OSS-120B",
                provider="openai",
                model_id="gpt-oss-120b",
                role=ModelRole.TEACHER,
                supported_tasks=[
                    TaskType.REASONING,
                    TaskType.CODING,
                    TaskType.FUNCTION_CALLING,
                    TaskType.DISTILLATION,
                ],
                max_context_tokens=100_000,
                supports_function_calling=True,
                cost_tier=CostTier.FREE,  # Self-hosted
                can_run_local=True,
                gpu_memory_gb=240.0,
                avg_latency_ms=2000,
                throughput_tps=8.0,
                benchmark_score=90.0,
            )
        )

        # Primary student models
        self.register_model(
            ModelSpec(
                name="Llama-4-Scout",
                provider="meta",
                model_id="meta-llama/Llama-4-Scout",
                role=ModelRole.STUDENT,
                supported_tasks=[
                    TaskType.REASONING,
                    TaskType.CODING,
                    TaskType.CHAT,
                    TaskType.FUNCTION_CALLING,
                    TaskType.MULTIMODAL,
                ],
                max_context_tokens=500_000,
                supports_function_calling=True,
                supports_multimodal=True,
                cost_tier=CostTier.FREE,
                can_run_local=True,
                gpu_memory_gb=80.0,
                avg_latency_ms=1500,
                throughput_tps=12.0,
                benchmark_score=85.0,
            )
        )

        # Specialist models
        self.register_model(
            ModelSpec(
                name="Qwen2.5-VL",
                provider="alibaba",
                model_id="Qwen/Qwen2.5-VL-72B",
                role=ModelRole.SPECIALIST,
                supported_tasks=[TaskType.DOCUMENT_VISION, TaskType.MULTIMODAL],
                max_context_tokens=32_000,
                supports_multimodal=True,
                cost_tier=CostTier.FREE,
                can_run_local=True,
                gpu_memory_gb=144.0,
                avg_latency_ms=2500,
                throughput_tps=6.0,
                benchmark_score=92.0,  # Cao cho vision tasks
            )
        )

        self.register_model(
            ModelSpec(
                name="Qwen3-Coder",
                provider="alibaba",
                model_id="Qwen/Qwen3-Coder-32B",
                role=ModelRole.SPECIALIST,
                supported_tasks=[TaskType.CODING, TaskType.FUNCTION_CALLING],
                max_context_tokens=64_000,
                supports_function_calling=True,
                cost_tier=CostTier.FREE,
                can_run_local=True,
                gpu_memory_gb=64.0,
                avg_latency_ms=1200,
                throughput_tps=18.0,
                benchmark_score=88.0,
            )
        )

    def register_model(self, model: ModelSpec) -> None:
        """Đăng ký model mới vào ma trận."""
        self._models[model.name] = model

    def select_model(
        self,
        task: TaskType,
        role: ModelRole | None = None,
        max_cost_tier: CostTier = CostTier.PREMIUM,
        require_local: bool = False,
        max_latency_ms: int = 10_000,
    ) -> ModelSpec | None:
        """Chọn model phù hợp nhất theo yêu cầu.

        Args:
            task: Loại tác vụ cần xử lý
            role: Vai trò model (nếu có)
            max_cost_tier: Chi phí tối đa chấp nhận
            require_local: Bắt buộc chạy local
            max_latency_ms: Độ trễ tối đa (ms)

        Returns:
            Model phù hợp nhất hoặc None nếu không tìm thấy
        """
        candidates = []

        cost_order = {
            CostTier.FREE: 0,
            CostTier.LOW: 1,
            CostTier.MEDIUM: 2,
            CostTier.HIGH: 3,
            CostTier.PREMIUM: 4,
        }

        for model in self._models.values():
            # Check task support
            if task not in model.supported_tasks:
                continue

            # Check role (nếu chỉ định)
            if role and model.role != role:
                continue

            # Check cost constraint
            if cost_order[model.cost_tier] > cost_order[max_cost_tier]:
                continue

            # Check local requirement
            if require_local and not model.can_run_local:
                continue

            # Check latency
            if model.avg_latency_ms > max_latency_ms:
                continue

            candidates.append(model)

        if not candidates:
            return None

        # Sắp xếp theo: cost tier (thấp hơn tốt hơn) → benchmark score (cao hơn tốt hơn)
        candidates.sort(
            key=lambda m: (
                cost_order[m.cost_tier],
                -m.benchmark_score,  # Negative để sort desc
            )
        )

        return candidates[0]

    def get_model(self, name: str) -> ModelSpec | None:
        """Lấy model theo tên."""
        return self._models.get(name)

    def list_models(
        self,
        role: ModelRole | None = None,
        provider: str | None = None,
        local_only: bool = False,
    ) -> list[ModelSpec]:
        """Liệt kê models theo filter."""
        results = []

        for model in self._models.values():
            if role and model.role != role:
                continue
            if provider and model.provider != provider:
                continue
            if local_only and not model.can_run_local:
                continue

            results.append(model)

        return sorted(results, key=lambda m: (m.role.value, m.name))

    def get_cost_estimate(
        self, model_name: str, input_tokens: int, output_tokens: int = 0
    ) -> float:
        """Ước tính chi phí sử dụng model.

        Args:
            model_name: Tên model
            input_tokens: Số token input
            output_tokens: Số token output (mặc định 0)

        Returns:
            Chi phí ước tính (USD)
        """
        model = self.get_model(model_name)
        if not model:
            return 0.0

        total_tokens = input_tokens + output_tokens
        return (total_tokens / 1000) * model.cost_per_1k_tokens


# Global model matrix instance
model_matrix = ModelMatrix()


# Convenience functions cho các use case phổ biến
def get_teacher_model() -> ModelSpec | None:
    """Lấy model teacher chính (GPT-5)."""
    return model_matrix.select_model(task=TaskType.LABELING, role=ModelRole.TEACHER)


def get_student_model() -> ModelSpec | None:
    """Lấy model student chính (Llama 4)."""
    return model_matrix.select_model(
        task=TaskType.REASONING, role=ModelRole.STUDENT, require_local=True
    )


def get_realtime_model() -> ModelSpec | None:
    """Lấy model realtime (GPT-4o)."""
    return model_matrix.select_model(task=TaskType.MULTIMODAL, role=ModelRole.REALTIME)


def get_edge_model() -> ModelSpec | None:
    """Lấy model edge (GPT-4.1-nano)."""
    return model_matrix.select_model(task=TaskType.EDGE_TRIGGER, role=ModelRole.EDGE)


def get_vision_model() -> ModelSpec | None:
    """Lấy model vision specialist (Qwen2.5-VL)."""
    return model_matrix.select_model(
        task=TaskType.DOCUMENT_VISION, role=ModelRole.SPECIALIST
    )


def get_coding_model() -> ModelSpec | None:
    """Lấy model coding specialist (Qwen3-Coder)."""
    return model_matrix.select_model(task=TaskType.CODING, role=ModelRole.SPECIALIST)
