"""Enhanced distillation service với GPT-5 teacher và Llama 4 student.

Triển khai teacher-student architecture cho knowledge distillation,
với GPT-5 làm teacher model để generate high-quality labels cho Llama 4 student.
"""

import asyncio
import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any

from app.ingest.safety_filters import SafetyLevel, evaluate_data_safety
from app.model_management.router import ModelRequest, get_model_router
from app.triage.data_triage import DataItem, triage_data_item
from pydantic import BaseModel
import Exception
import auto_train
import bool
import confidence_marker
import config
import cycle_interval
import data_item
import data_items
import datapoints
import dict
import dp
import e
import enumerate
import float
import i
import input_text
import inputs
import int
import isinstance
import item
import len
import line
import list
import marker
import model_spec
import reasoning_marker
import response_marker
import result
import safety_level
import self
import str
import task_context
import teacher_response
import training_result
import tuple

logger = logging.getLogger(__name__)


class DistillationStrategy(str, Enum):
    """Chiến lược distillation."""

    RESPONSE_MATCHING = "response_matching"  # Match teacher responses
    ATTENTION_TRANSFER = "attention_transfer"  # Transfer attention patterns
    INTERMEDIATE_FEATURES = "intermediate_features"  # Match intermediate layers
    CURRICULUM_LEARNING = "curriculum_learning"  # Progressive difficulty
    CHAIN_OF_THOUGHT = "chain_of_thought"  # Reasoning process transfer


class LabelingQuality(str, Enum):
    """Chất lượng label từ teacher."""

    EXCELLENT = "excellent"  # > 0.9 confidence
    GOOD = "good"  # 0.7-0.9 confidence
    ACCEPTABLE = "acceptable"  # 0.5-0.7 confidence
    POOR = "poor"  # < 0.5 confidence


@dataclass
class TeacherLabel:
    """Label được generate bởi teacher model."""

    input_text: str
    teacher_response: str
    teacher_model: str
    confidence: float
    reasoning: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    quality: LabelingQuality | None = None

    def __post_init__(self):
        if self.quality is None:
            if self.confidence >= 0.9:
                self.quality = LabelingQuality.EXCELLENT
            elif self.confidence >= 0.7:
                self.quality = LabelingQuality.GOOD
            elif self.confidence >= 0.5:
                self.quality = LabelingQuality.ACCEPTABLE
            else:
                self.quality = LabelingQuality.POOR


@dataclass
class DistillationDatapoint:
    """Một datapoint cho distillation training."""

    input_text: str
    teacher_label: TeacherLabel
    student_prediction: str | None = None
    student_confidence: float | None = None
    loss_value: float | None = None
    improvement_score: float | None = None


class DistillationConfig(BaseModel):
    """Configuration cho distillation process."""

    teacher_model: str = "gpt-5"
    student_model: str = "llama-4"
    strategy: DistillationStrategy = DistillationStrategy.RESPONSE_MATCHING
    batch_size: int = 32
    max_input_length: int = 2048
    max_output_length: int = 512
    temperature: float = 0.1
    min_quality_threshold: LabelingQuality = LabelingQuality.ACCEPTABLE
    use_chain_of_thought: bool = True
    enable_curriculum: bool = True
    parallel_labeling: bool = True
    max_retries: int = 3


class TeacherLabelingService:
    """Service để generate labels từ teacher model."""

    def __init__(self, config: DistillationConfig):
        self.config = config
        self.router = get_model_router()
        self.labeled_count = 0
        self.total_cost = 0.0

    async def generate_label(
        self, input_text: str, task_context: str = "general"
    ) -> TeacherLabel:
        """Generate label cho một input từ teacher model."""

        # Prepare prompt for teacher
        if self.config.use_chain_of_thought:
            prompt = self._create_cot_prompt(input_text, task_context)
        else:
            prompt = self._create_direct_prompt(input_text, task_context)

        # Request teacher model
        request = ModelRequest(
            task_type="text_generation",
            input_text=prompt,
            max_tokens=self.config.max_output_length,
            temperature=self.config.temperature,
            model_preferences=[self.config.teacher_model],
            require_reasoning=self.config.use_chain_of_thought,
        )

        try:
            # Get teacher response
            teacher_model = self.router.select_model(request)
            response = await self._call_teacher_model(teacher_model, prompt)

            # Parse response
            teacher_response, reasoning, confidence = self._parse_teacher_response(
                response
            )

            # Create label
            label = TeacherLabel(
                input_text=input_text,
                teacher_response=teacher_response,
                teacher_model=teacher_model.name,
                confidence=confidence,
                reasoning=reasoning,
                metadata={
                    "task_context": task_context,
                    "prompt_strategy": "chain_of_thought"
                    if self.config.use_chain_of_thought
                    else "direct",
                    "teacher_cost": teacher_model.cost_per_token
                    * len(response.split()),
                },
            )

            self.labeled_count += 1
            self.total_cost += label.metadata.get("teacher_cost", 0)

            return label

        except Exception as e:
            logger.error(f"Error generating teacher label: {e}")
            # Return fallback label
            return TeacherLabel(
                input_text=input_text,
                teacher_response="",
                teacher_model=self.config.teacher_model,
                confidence=0.0,
                reasoning=f"Error: {str(e)}",
                metadata={"error": str(e)},
            )

    async def batch_generate_labels(
        self, inputs: list[str], task_context: str = "general"
    ) -> list[TeacherLabel]:
        """Generate labels cho multiple inputs."""

        if self.config.parallel_labeling:
            # Parallel processing
            tasks = [
                self.generate_label(input_text, task_context) for input_text in inputs
            ]
            labels = await asyncio.gather(*tasks, return_exceptions=True)

            # Handle exceptions
            valid_labels = []
            for i, result in enumerate(labels):
                if isinstance(result, Exception):
                    logger.error(f"Error labeling input {i}: {result}")
                    # Create error label
                    error_label = TeacherLabel(
                        input_text=inputs[i],
                        teacher_response="",
                        teacher_model=self.config.teacher_model,
                        confidence=0.0,
                        reasoning=f"Batch error: {str(result)}",
                    )
                    valid_labels.append(error_label)
                else:
                    valid_labels.append(result)

            return valid_labels

        else:
            # Sequential processing
            labels = []
            for input_text in inputs:
                label = await self.generate_label(input_text, task_context)
                labels.append(label)

            return labels

    def _create_cot_prompt(self, input_text: str, task_context: str) -> str:
        """Tạo chain-of-thought prompt cho teacher."""
        return f"""Task: {task_context}

Input: {input_text}

Please provide a high-quality response with your reasoning process:

1. Analysis: First, analyze the input and identify key elements
2. Reasoning: Explain your thought process step by step
3. Response: Provide the final response
4. Confidence: Rate your confidence (0.0-1.0)

Format your response as:
ANALYSIS: [your analysis]
REASONING: [your step-by-step reasoning]
RESPONSE: [your final response]
CONFIDENCE: [0.0-1.0]"""

    def _create_direct_prompt(self, input_text: str, task_context: str) -> str:
        """Tạo direct prompt cho teacher."""
        return f"""Task: {task_context}

Input: {input_text}

Please provide a high-quality response and confidence score:

RESPONSE: [your response]
CONFIDENCE: [0.0-1.0]"""

    def _call_teacher_model(self, model_spec, prompt: str) -> str:
        """Call teacher model API (mock implementation)."""
        # Simulate response based on prompt length and complexity
        import random

        if "ANALYSIS:" in prompt:
            # Chain of thought response
            return f"""ANALYSIS: The input appears to be a {random.choice(["question", "request", "statement"])} requiring careful consideration.

REASONING: Based on the context and content, I need to: 1) Understand the core intent, 2) Consider relevant factors, 3) Provide appropriate response.

RESPONSE: [Generated response based on {model_spec.name}]

CONFIDENCE: {random.uniform(0.7, 0.95):.2f}"""
        else:
            # Direct response
            return f"""RESPONSE: [Generated response from {model_spec.name}]

CONFIDENCE: {random.uniform(0.6, 0.9):.2f}"""

    def _parse_teacher_response(self, response: str) -> tuple[str, str | None, float]:
        """Parse teacher response để extract content, reasoning, confidence."""
        CONFIDENCE_MARKER = "CONFIDENCE:"
        RESPONSE_MARKER = "RESPONSE:"
        REASONING_MARKER = "REASONING:"

        try:
            # Extract confidence
            confidence = self._extract_confidence(response, CONFIDENCE_MARKER)

            # Extract response
            main_response = self._extract_main_response(response, RESPONSE_MARKER)

            # Extract reasoning (if available)
            reasoning = self._extract_reasoning(
                response, REASONING_MARKER, RESPONSE_MARKER, CONFIDENCE_MARKER
            )

            return main_response, reasoning, confidence

        except Exception as e:
            logger.error(f"Error parsing teacher response: {e}")
            return response.strip(), None, 0.5

    def _extract_confidence(self, response: str, marker: str) -> float:
        """Extract confidence score from response."""
        if marker in response:
            confidence_lines = [line for line in response.split("\n") if marker in line]
            if confidence_lines:
                confidence_str = confidence_lines[0].split(marker)[1].strip()
                return float(confidence_str)
        return 0.5

    def _extract_main_response(self, response: str, marker: str) -> str:
        """Extract main response from teacher output."""
        if marker in response:
            response_lines = [line for line in response.split("\n") if marker in line]
            if response_lines:
                return response_lines[0].split(marker)[1].strip()
        return response.strip()

    def _extract_reasoning(
        self,
        response: str,
        reasoning_marker: str,
        response_marker: str,
        confidence_marker: str,
    ) -> str | None:
        """Extract reasoning section from teacher output."""
        if reasoning_marker not in response:
            return None

        reasoning_lines = []
        capture = False

        for line in response.split("\n"):
            if reasoning_marker in line:
                capture = True
                reasoning_content = line.split(reasoning_marker)[1].strip()
                if reasoning_content:
                    reasoning_lines.append(reasoning_content)
            elif capture and line.strip():
                if line.startswith(response_marker) or line.startswith(
                    confidence_marker
                ):
                    break
                reasoning_lines.append(line.strip())

        return " ".join(reasoning_lines) if reasoning_lines else None


class StudentTrainingService:
    """Service để train student model với teacher labels."""

    def __init__(self, config: DistillationConfig):
        self.config = config
        self.router = get_model_router()
        self.training_data: list[DistillationDatapoint] = []

    def add_training_data(self, datapoints: list[DistillationDatapoint]) -> None:
        """Thêm training data."""
        # Filter by quality threshold
        quality_threshold = self.config.min_quality_threshold
        quality_levels = [
            LabelingQuality.POOR,
            LabelingQuality.ACCEPTABLE,
            LabelingQuality.GOOD,
            LabelingQuality.EXCELLENT,
        ]
        min_level_index = quality_levels.index(quality_threshold)

        filtered_data = [
            dp
            for dp in datapoints
            if quality_levels.index(dp.teacher_label.quality) >= min_level_index
        ]

        self.training_data.extend(filtered_data)
        logger.info(
            f"Added {len(filtered_data)} training datapoints (filtered from {len(datapoints)})"
        )

    def train_student_batch(self, batch_size: int | None = None) -> dict[str, Any]:
        """Train student model với current training data."""
        if batch_size is None:
            batch_size = self.config.batch_size

        if len(self.training_data) < batch_size:
            logger.warning(
                f"Insufficient training data: {len(self.training_data)} < {batch_size}"
            )
            return {
                "status": "insufficient_data",
                "data_count": len(self.training_data),
            }

        # Sample batch
        import random

        batch_data = random.sample(self.training_data, batch_size)

        # Simulate training process (placeholder for actual implementation)
        # In production, this would:
        # 1. Prepare training inputs/targets from teacher labels
        # 2. Run training step on student model
        # 3. Calculate distillation loss
        # 4. Update model parameters

        # Mock training results
        avg_loss = random.uniform(0.1, 0.5)
        improvement = random.uniform(0.01, 0.1)

        # Update datapoint metrics
        for dp in batch_data:
            dp.loss_value = random.uniform(0.05, 1.0)
            dp.improvement_score = random.uniform(0.0, 0.2)

        return {
            "status": "completed",
            "batch_size": batch_size,
            "avg_loss": avg_loss,
            "improvement": improvement,
            "student_model": self.config.student_model,
            "strategy": self.config.strategy,
        }

    def get_training_stats(self) -> dict[str, Any]:
        """Thống kê về training progress."""
        if not self.training_data:
            return {"total_datapoints": 0}

        quality_counts = {}
        avg_confidence = 0.0

        for dp in self.training_data:
            quality = dp.teacher_label.quality
            if quality not in quality_counts:
                quality_counts[quality] = 0
            quality_counts[quality] += 1
            avg_confidence += dp.teacher_label.confidence

        avg_confidence /= len(self.training_data)

        return {
            "total_datapoints": len(self.training_data),
            "quality_distribution": quality_counts,
            "avg_teacher_confidence": avg_confidence,
            "student_model": self.config.student_model,
            "teacher_model": self.config.teacher_model,
        }


class EnhancedDistillationService:
    """Main service orchestrating teacher labeling và student training."""

    def __init__(self, config: DistillationConfig | None = None):
        self.config = config or DistillationConfig()
        self.teacher_service = TeacherLabelingService(self.config)
        self.student_service = StudentTrainingService(self.config)
        self.processed_items = 0

    async def process_data_item(
        self, data_item: DataItem, task_context: str = "general"
    ) -> DistillationDatapoint | None:
        """Process một data item thành distillation datapoint."""

        # Safety check
        safety_level, _ = evaluate_data_safety(data_item.content)
        if safety_level == SafetyLevel.BLOCKED:
            logger.warning(f"Data item {data_item.id} blocked by safety filters")
            return None

        # Triage check
        triage_decision = triage_data_item(
            data_item.content, data_item.source, data_item.metadata, data_item.id
        )

        # Skip if not suitable for training
        if triage_decision.route in ["reject", "archive"]:
            logger.info(
                f"Data item {data_item.id} not suitable for training: {triage_decision.route}"
            )
            return None

        # Generate teacher label
        teacher_label = await self.teacher_service.generate_label(
            data_item.content, task_context
        )

        # Create distillation datapoint
        datapoint = DistillationDatapoint(
            input_text=data_item.content, teacher_label=teacher_label
        )

        self.processed_items += 1
        return datapoint

    async def process_batch(
        self,
        data_items: list[DataItem],
        task_context: str = "general",
        auto_train: bool = True,
    ) -> dict[str, Any]:
        """Process batch của data items."""

        # Process items into datapoints
        tasks = [self.process_data_item(item, task_context) for item in data_items]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Collect valid datapoints
        valid_datapoints = []
        errors = 0

        for result in results:
            if isinstance(result, Exception):
                errors += 1
                logger.error(f"Error processing data item: {result}")
            elif result is not None:
                valid_datapoints.append(result)

        # Add to training data
        if valid_datapoints:
            self.student_service.add_training_data(valid_datapoints)

        # Auto-train if enabled and enough data
        if auto_train and len(valid_datapoints) >= self.config.batch_size:
            self.student_service.train_student_batch()

        return {
            "processed_items": len(data_items),
            "valid_datapoints": len(valid_datapoints),
            "errors": errors,
            "training_result": training_result,
            "teacher_stats": {
                "labeled_count": self.teacher_service.labeled_count,
                "total_cost": self.teacher_service.total_cost,
            },
            "student_stats": self.student_service.get_training_stats(),
        }

    async def continuous_learning_cycle(
        self,
        data_stream: list[DataItem],
        cycle_interval: int = 300,  # 5 minutes
    ) -> None:
        """Chạy continuous learning cycle."""
        logger.info("Starting continuous learning cycle")

        while True:
            try:
                if data_stream:
                    # Process batch
                    batch = data_stream[: self.config.batch_size]
                    data_stream = data_stream[self.config.batch_size :]

                    _ = await self.process_batch(batch, auto_train=True)
                    logger.info(f"Processed batch: {result}")

                else:
                    logger.info("No data available, waiting...")

                # Wait for next cycle
                await asyncio.sleep(cycle_interval)

            except Exception as e:
                logger.error(f"Error in continuous learning cycle: {e}")
                await asyncio.sleep(cycle_interval)

    def get_service_stats(self) -> dict[str, Any]:
        """Comprehensive stats về distillation service."""
        return {
            "config": self.config.dict(),
            "processed_items": self.processed_items,
            "teacher_service": {
                "labeled_count": self.teacher_service.labeled_count,
                "total_cost": self.teacher_service.total_cost,
                "avg_cost_per_label": (
                    self.teacher_service.total_cost / self.teacher_service.labeled_count
                    if self.teacher_service.labeled_count > 0
                    else 0
                ),
            },
            "student_service": self.student_service.get_training_stats(),
        }


# Singleton instance
_distillation_service = None


def get_distillation_service(
    config: DistillationConfig | None = None,
) -> EnhancedDistillationService:
    """Get singleton instance của distillation service."""
    global _distillation_service
    if _distillation_service is None:
        _distillation_service = EnhancedDistillationService(config)
    return _distillation_service
