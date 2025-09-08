"""Model Management - Router thông minh cho chọn model tối ưu.

Module này cung cấp:
- Router thông minh dựa trên tác vụ, chi phí, độ nhạy cảm dữ liệu
- Model registry với cấu hình YAML
- Cost optimization và latency control
- Security và privacy compliance
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, Field
import Exception
import bool
import data_sensitivity
import dict
import e
import f
import float
import input_tokens
import int
import kwargs
import len
import list
import m
import max
import model_config
import model_id
import model_spec
import open
import output_tokens
import provider
import s
import self
import str
import task_type
import tuple
import x

logger = logging.getLogger(__name__)


class ModelRequest(BaseModel):
    """Yêu cầu model với các ràng buộc."""

    task_type: str = Field(..., description="Loại tác vụ cần xử lý")
    data_sensitivity: Literal["low", "medium", "high"] = Field(
        default="medium", description="Độ nhạy cảm dữ liệu"
    )
    budget_constraint: float | None = Field(
        default=None, description="Ngân sách tối đa ($/1K tokens)"
    )
    required_context_length: int | None = Field(
        default=None, description="Độ dài context tối thiểu"
    )
    max_latency_ms: int | None = Field(default=None, description="Độ trễ tối đa (ms)")
    requires_vision: bool = Field(
        default=False, description="Cần khả năng xử lý hình ảnh"
    )
    requires_function_calling: bool = Field(
        default=False, description="Cần function calling"
    )
    prefer_self_hosted: bool = Field(default=False, description="Ưu tiên model tự host")


class ModelSpec(BaseModel):
    """Thông số kỹ thuật của model."""

    name: str
    provider: str
    role: str
    use_cases: list[str]
    cost_per_1k: float
    context_length: int
    max_output_tokens: int
    supports_vision: bool
    supports_function_calling: bool
    latency_ms: int
    availability: str


class ModelRouter:
    """Router thông minh để chọn model phù hợp."""

    def __init__(self, config_path: str | None = None):
        """Khởi tạo router với cấu hình model.

        Args:
            config_path: Đường dẫn tới file cấu hình YAML
        """
        if config_path is None:
            config_path = (
                Path(__file__).parent.parent.parent / "config" / "model_matrix.yaml"
            )

        self.config_path = Path(config_path)
        self.models: dict[str, ModelSpec] = {}
        self.routing_rules: dict = {}
        self.aliases: dict[str, str] = {}
        self.default_model = "gpt-4o"  # Fallback an toàn

        self._load_config()

    def _load_config(self) -> None:
        """Load cấu hình từ file YAML."""
        try:
            if not self.config_path.exists():
                logger.warning(f"Config file not found: {self.config_path}")
                return

            with open(self.config_path, encoding="utf-8") as f:
                config = yaml.safe_load(f)

            # Load models
            for model_id, model_config in config.get("models", {}).items():
                self.models[model_id] = ModelSpec(name=model_id, **model_config)

            # Load routing rules
            self.routing_rules = config.get("routing_rules", {})

            # Load aliases
            self.aliases = config.get("aliases", {})

            logger.info(f"Loaded {len(self.models)} models from {self.config_path}")

        except Exception as e:
            logger.error(f"Error loading model config: {e}")
            # Fallback tối thiểu
            self._load_fallback_config()

    def _load_fallback_config(self) -> None:
        """Load cấu hình fallback nếu file YAML lỗi."""
        logger.warning("Using fallback model configuration")

        self.models = {
            "gpt-4o": ModelSpec(
                name="gpt-4o",
                provider="openai",
                role="multimodal_realtime",
                use_cases=["general", "multimodal", "chat"],
                cost_per_1k=5.0,
                context_length=128000,
                max_output_tokens=16384,
                supports_vision=True,
                supports_function_calling=True,
                latency_ms=800,
                availability="24/7",
            )
        }

    def select_model(self, request: ModelRequest) -> str | None:
        """Chọn model phù hợp nhất dựa trên yêu cầu.

        Args:
            request: Yêu cầu model với các ràng buộc

        Returns:
            Model ID phù hợp nhất hoặc None nếu không tìm thấy
        """
        try:
            # 1. Lọc candidates theo use_cases
            candidates = []
            for model_id, model_spec in self.models.items():
                if request.task_type in model_spec.use_cases:
                    candidates.append((model_id, model_spec))

            if not candidates:
                logger.warning(f"No models found for task_type: {request.task_type}")
                return self.default_model

            # 2. Áp dụng các ràng buộc bắt buộc
            candidates = self._apply_constraints(candidates, request)

            if not candidates:
                logger.warning("No models passed constraints")
                return self.default_model

            # 3. Score và rank candidates
            scored_candidates = self._score_candidates(candidates, request)

            # 4. Chọn model có điểm cao nhất
            best_candidate = max(scored_candidates, key=lambda x: x[2])
            selected_model = best_candidate[0]

            logger.info(
                f"Selected model: {selected_model} for task: {request.task_type}"
            )
            return selected_model

        except Exception as e:
            logger.error(f"Error selecting model: {e}")
            return self.default_model

    def _apply_constraints(
        self, candidates: list[tuple[str, ModelSpec]], request: ModelRequest
    ) -> list[tuple[str, ModelSpec]]:
        """Áp dụng các ràng buộc bắt buộc."""
        filtered = []

        for model_id, spec in candidates:
            # Budget constraint
            if (
                request.budget_constraint
                and spec.cost_per_1k > request.budget_constraint
            ):
                continue

            # Context length
            if (
                request.required_context_length
                and spec.context_length < request.required_context_length
            ):
                continue

            # Latency
            if request.max_latency_ms and spec.latency_ms > request.max_latency_ms:
                continue

            # Vision support
            if request.requires_vision and not spec.supports_vision:
                continue

            # Function calling
            if request.requires_function_calling and not spec.supports_function_calling:
                continue

            # Data sensitivity - high security prefers self-hosted
            if request.data_sensitivity == "high":
                if spec.availability != "self_hosted":
                    continue

            # Self-hosted preference
            if request.prefer_self_hosted and spec.availability != "self_hosted":
                continue

            filtered.append((model_id, spec))

        return filtered

    def _score_candidates(
        self, candidates: list[tuple[str, ModelSpec]], request: ModelRequest
    ) -> list[tuple[str, ModelSpec, float]]:
        """Tính điểm cho từng candidate."""
        scored = []

        for model_id, spec in candidates:
            score = 0.0

            # Cost scoring (lower cost = higher score)
            max_cost = max(s.cost_per_1k for _, s in candidates)
            if max_cost > 0:
                cost_score = (max_cost - spec.cost_per_1k) / max_cost * 30
                score += cost_score

            # Latency scoring (lower latency = higher score)
            max_latency = max(s.latency_ms for _, s in candidates)
            if max_latency > 0:
                latency_score = (max_latency - spec.latency_ms) / max_latency * 20
                score += latency_score

            # Context length scoring (more context = higher score)
            max_context = max(s.context_length for _, s in candidates)
            if max_context > 0:
                context_score = spec.context_length / max_context * 15
                score += context_score

            # Security preference
            if (
                request.data_sensitivity == "high"
                and spec.availability == "self_hosted"
            ):
                score += 20

            # Self-hosted preference
            if request.prefer_self_hosted and spec.availability == "self_hosted":
                score += 10

            # Feature completeness
            if request.requires_vision and spec.supports_vision:
                score += 10
            if request.requires_function_calling and spec.supports_function_calling:
                score += 5

            scored.append((model_id, spec, score))

        return scored

    def get_model_spec(self, model_id: str) -> ModelSpec | None:
        """Lấy thông số kỹ thuật của model.

        Args:
            model_id: ID của model hoặc alias

        Returns:
            ModelSpec hoặc None nếu không tìm thấy
        """
        # Check alias trước
        actual_id = self.aliases.get(model_id, model_id)
        return self.models.get(actual_id)

    def list_models(
        self, task_type: str | None = None, provider: str | None = None
    ) -> list[ModelSpec]:
        """Liệt kê models theo bộ lọc.

        Args:
            task_type: Lọc theo loại tác vụ
            provider: Lọc theo nhà cung cấp

        Returns:
            Danh sách ModelSpec phù hợp
        """
        models = list(self.models.values())

        if task_type:
            models = [m for m in models if task_type in m.use_cases]

        if provider:
            models = [m for m in models if m.provider == provider]

        return models

    def estimate_cost(
        self, model_id: str, input_tokens: int, output_tokens: int
    ) -> float:
        """Ước tính chi phí sử dụng model.

        Args:
            model_id: ID của model
            input_tokens: Số tokens đầu vào
            output_tokens: Số tokens đầu ra

        Returns:
            Chi phí ước tính ($)
        """
        spec = self.get_model_spec(model_id)
        if not spec:
            return 0.0

        total_tokens = input_tokens + output_tokens
        return (total_tokens / 1000) * spec.cost_per_1k


# Global router instance
_router: ModelRouter | None = None


def get_model_router() -> ModelRouter:
    """Lấy global router instance."""
    global _router
    if _router is None:
        _router = ModelRouter()
    return _router


def select_optimal_model(
    task_type: str,
    data_sensitivity: Literal["low", "medium", "high"] = "medium",
    **kwargs,
) -> str | None:
    """Convenience function để chọn model tối ưu.

    Args:
        task_type: Loại tác vụ
        data_sensitivity: Độ nhạy cảm dữ liệu
        **kwargs: Các tham số khác cho ModelRequest

    Returns:
        Model ID được chọn
    """
    router = get_model_router()
    request = ModelRequest(
        task_type=task_type, data_sensitivity=data_sensitivity, **kwargs
    )
    return router.select_model(request)


# Teacher/Student shortcuts cho compatibility
def get_teacher_model() -> str | None:
    """Lấy model teacher chính (GPT-5)."""
    return select_optimal_model("data_labeling", data_sensitivity="low")


def get_student_model() -> str | None:
    """Lấy model student chính (Llama 4)."""
    return select_optimal_model("general_reasoning", prefer_self_hosted=True)


def get_realtime_model() -> str | None:
    """Lấy model realtime (GPT-4o)."""
    return select_optimal_model("multimodal", max_latency_ms=1000)


def get_edge_model() -> str | None:
    """Lấy model edge (GPT-4.1-nano)."""
    return select_optimal_model("edge_trigger", max_latency_ms=500)


def get_vision_model() -> str | None:
    """Lấy model vision (Qwen2.5-VL)."""
    return select_optimal_model("document_vision", requires_vision=True)


def get_coding_model() -> str | None:
    """Lấy model coding (Qwen3)."""
    return select_optimal_model("coding", prefer_self_hosted=True)
