"""GPT-5 Distillation Service - Teacher labeling cho student models.

Module này triển khai knowledge distillation từ GPT-5 (teacher)
xuống Llama 4/Qwen (students) thông qua high-quality labeling.
"""

from __future__ import annotations

import asyncio
import logging
from collections.abc import Iterable
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from apps.backend.trainer.datasets.registry import DatasetStage, registry
from apps.backend.trainer.model_matrix import get_teacher_model
from openai import AsyncOpenAI
from pydantic import BaseModel, Field
import Exception
import ValueError
import bool
import config
import dataset_name
import description
import dict
import e
import enumerate
import ex
import example
import examples
import float
import i
import int
import isinstance
import len
import list
import marker
import max
import min
import openai_client
import prompt
import ref
import result
import self
import source_type
import str
import sum
import term
import tuple

logger = logging.getLogger(__name__)


class RawExample(BaseModel):
    """Mẫu dữ liệu thô cần được teacher label."""

    id: str = Field(default_factory=lambda: str(uuid4()))
    prompt: str = Field(..., description="Câu hỏi/nhiệm vụ cần giải")
    context: str = Field(default="", description="Context bổ sung")
    refs: list[str] = Field(default_factory=list, description="Reference materials")
    meta: dict[str, Any] = Field(default_factory=dict, description="Metadata khác")
    source_url: str | None = None

    def get_full_prompt(self) -> str:
        """Tạo prompt đầy đủ cho teacher model."""
        parts = [self.prompt]

        if self.context:
            parts.append(f"Context: {self.context}")

        if self.refs:
            refs_text = "\n".join(f"- {ref}" for ref in self.refs)
            parts.append(f"References:\n{refs_text}")

        return "\n\n".join(parts)


class LabeledExample(BaseModel):
    """Mẫu đã được teacher model label."""

    id: str = Field(default_factory=lambda: str(uuid4()))
    prompt: str = Field(..., description="Input prompt")
    answer: str = Field(..., description="Teacher answer")
    critique: str = Field(..., description="Teacher critique/explanation")
    rationale: str = Field(default="", description="Step-by-step reasoning (internal)")

    # Metadata
    teacher_model: str = Field(..., description="Model đã label")
    teacher_version: str = Field(..., description="Version model")
    temperature: float = Field(default=0.2)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    source_id: str = Field(..., description="ID của RawExample gốc")

    # Quality metrics
    confidence_score: float = Field(default=0.0, ge=0.0, le=1.0)
    complexity_score: float = Field(default=0.0, ge=0.0, le=1.0)

    def get_training_pair(self) -> dict[str, str]:
        """Convert thành format chuẩn cho training (prompt → answer)."""
        return {
            "prompt": self.prompt,
            "response": self.answer,
            "metadata": {
                "teacher": self.teacher_model,
                "created_at": self.created_at.isoformat(),
                "confidence": self.confidence_score,
                "complexity": self.complexity_score,
            },
        }


class DistillationConfig(BaseModel):
    """Cấu hình cho quá trình distillation."""

    # Teacher model settings
    teacher_model: str = "gpt-5"
    temperature: float = 0.2
    max_tokens: int | None = None

    # Batch processing
    batch_size: int = 10
    max_concurrent: int = 5
    retry_attempts: int = 3

    # Quality control
    min_answer_length: int = 10
    max_answer_length: int = 4000
    require_critique: bool = True

    # Safety
    content_filter: bool = True
    pii_detection: bool = True


class DistillationService:
    """Service thực hiện knowledge distillation từ teacher models."""

    def __init__(
        self,
        config: DistillationConfig | None = None,
        openai_client: AsyncOpenAI | None = None,
    ):
        """Khởi tạo distillation service.

        Args:
            config: Cấu hình distillation
            openai_client: OpenAI client (tự tạo nếu None)
        """
        self.config = config or DistillationConfig()
        self.client = openai_client or AsyncOpenAI()  # Cần OPENAI_API_KEY env var

        # Validate teacher model availability
        teacher_spec = get_teacher_model()
        if not teacher_spec:
            raise ValueError("No teacher model available in model matrix")

        if teacher_spec.name != self.config.teacher_model:
            logger.warning(
                f"Config teacher model '{self.config.teacher_model}' != matrix model '{teacher_spec.name}'"
            )

    async def label_single(self, example: RawExample) -> LabeledExample | None:
        """Label một example duy nhất bằng teacher model.

        Args:
            example: Raw example cần label

        Returns:
            LabeledExample hoặc None nếu lỗi
        """
        try:
            # Tạo system prompt cho teacher
            system_prompt = self._build_system_prompt()

            # Tạo user prompt
            user_prompt = self._build_user_prompt(example)

            # Call teacher model
            response = await self.client.chat.completions.create(
                model=self.config.teacher_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens,
            )

            content = response.choices[0].message.content
            if not content:
                logger.warning(f"Empty response for example {example.id}")
                return None

            # Parse response thành answer + critique
            parsed = self._parse_teacher_response(content)
            if not parsed:
                return None

            answer, critique, rationale = parsed

            # Validate quality
            if not self._validate_quality(answer, critique):
                logger.warning(f"Quality check failed for example {example.id}")
                return None

            # Calculate scores
            confidence = self._calculate_confidence(answer, critique)
            complexity = self._calculate_complexity(example.prompt, answer)

            return LabeledExample(
                prompt=example.get_full_prompt(),
                answer=answer,
                critique=critique,
                rationale=rationale,
                teacher_model=self.config.teacher_model,
                teacher_version="20250824",  # Version hiện tại
                temperature=self.config.temperature,
                source_id=example.id,
                confidence_score=confidence,
                complexity_score=complexity,
            )

        except Exception as e:
            logger.error(f"Failed to label example {example.id}: {e}")
            return None

    async def label_batch(
        self,
        examples: list[RawExample],
        batch_tag: str = "default",
    ) -> list[LabeledExample]:
        """Label một batch examples với concurrency control.

        Args:
            examples: Danh sách raw examples
            batch_tag: Tag để group trong dataset registry

        Returns:
            Danh sách labeled examples
        """
        logger.info(f"Starting distillation batch: {len(examples)} examples")

        # Create semaphore để limit concurrent requests
        semaphore = asyncio.Semaphore(self.config.max_concurrent)

        async def label_with_semaphore(example: RawExample) -> LabeledExample | None:
            async with semaphore:
                return await self.label_single(example)

        # Process all examples concurrently
        tasks = [label_with_semaphore(ex) for ex in examples]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Filter out failures and exceptions
        labeled_examples = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Example {examples[i].id} failed: {result}")
            elif result is not None:
                labeled_examples.append(result)

        success_rate = len(labeled_examples) / len(examples) if examples else 0.0
        logger.info(
            f"Distillation complete: {len(labeled_examples)}/{len(examples)} success ({success_rate:.1%})"
        )

        return labeled_examples

    async def distill_and_save(
        self,
        examples: Iterable[RawExample],
        dataset_name: str,
        description: str = "",
        source_type: str = "distillation",
    ) -> str:
        """Distill examples và lưu vào dataset registry.

        Args:
            examples: Raw examples để distill
            dataset_name: Tên dataset
            description: Mô tả dataset
            source_type: Loại nguồn dữ liệu

        Returns:
            dataset_id của dataset đã tạo
        """
        example_list = list(examples)

        # Register dataset
        dataset_id = registry.register_dataset(
            name=dataset_name,
            description=description,
            source_type=source_type,
        )

        # Label examples
        labeled = await self.label_batch(example_list, batch_tag=dataset_id)

        # Calculate quality metrics
        if labeled:
            avg_confidence = sum(ex.confidence_score for ex in labeled) / len(labeled)
            avg_complexity = sum(ex.complexity_score for ex in labeled) / len(labeled)

            from apps.backend.trainer.datasets.registry import DatasetQualityScore

            quality = DatasetQualityScore(
                safety_score=1.0,  # Teacher models được giả định safe
                quality_score=avg_confidence,
                uniqueness_score=0.9,  # Distilled data ít trùng lặp
                relevance_score=avg_complexity,
            )

            registry.update_quality(dataset_id, quality)

        # Update dataset stage
        registry.update_stage(dataset_id, DatasetStage.LABELED)

        # Save labeled examples (trong thực tế nên lưu vào file/DB)
        # TODO: Implement persistent storage

        logger.info(
            f"Dataset {dataset_id} created with {len(labeled)} labeled examples"
        )
        return dataset_id

    def _build_system_prompt(self) -> str:
        """Tạo system prompt cho teacher model."""
        return """You are a world-class AI teacher helping to create high-quality training data.

Your task is to:
1. Provide a comprehensive, accurate answer to the given prompt
2. Write a brief critique explaining your reasoning
3. Keep internal reasoning steps (but don't expose sensitive chain-of-thought)

Format your response as:
ANSWER:
[Your complete answer here]

CRITIQUE:
[Brief critique explaining your approach and why this answer is good]

RATIONALE:
[Step-by-step reasoning - keep this internal/educational]

Guidelines:
- Be thorough but concise
- Prioritize accuracy over speed
- Use clear, educational language
- Avoid harmful, biased, or inappropriate content
- If uncertain, state your confidence level"""

    def _build_user_prompt(self, example: RawExample) -> str:
        """Tạo user prompt từ RawExample."""
        return example.get_full_prompt()

    def _parse_teacher_response(self, content: str) -> tuple[str, str, str] | None:
        """Parse response từ teacher model thành (answer, critique, rationale).

        Args:
            content: Raw response từ teacher

        Returns:
            Tuple (answer, critique, rationale) hoặc None nếu parse lỗi
        """
        try:
            # Split theo markers
            sections = {}
            current_section = None
            current_content = []

            for line in content.split("\n"):
                line = line.strip()

                if line.startswith("ANSWER:"):
                    if current_section:
                        sections[current_section] = "\n".join(current_content).strip()
                    current_section = "answer"
                    current_content = []
                elif line.startswith("CRITIQUE:"):
                    if current_section:
                        sections[current_section] = "\n".join(current_content).strip()
                    current_section = "critique"
                    current_content = []
                elif line.startswith("RATIONALE:"):
                    if current_section:
                        sections[current_section] = "\n".join(current_content).strip()
                    current_section = "rationale"
                    current_content = []
                else:
                    current_content.append(line)

            # Add last section
            if current_section:
                sections[current_section] = "\n".join(current_content).strip()

            answer = sections.get("answer", "")
            critique = sections.get("critique", "")
            rationale = sections.get("rationale", "")

            # Fallback nếu không có markers
            if not answer and not critique:
                # Assume entire content is answer
                parts = content.split("\n\n", 1)
                answer = parts[0].strip()
                critique = parts[1].strip() if len(parts) > 1 else ""

            return (answer, critique, rationale)

        except Exception as e:
            logger.error(f"Failed to parse teacher response: {e}")
            return None

    def _validate_quality(self, answer: str, critique: str) -> bool:
        """Kiểm tra chất lượng của answer và critique."""
        # Check length
        if len(answer) < self.config.min_answer_length:
            return False
        if len(answer) > self.config.max_answer_length:
            return False

        # Check có critique không (nếu required)
        if self.config.require_critique and len(critique) < 10:
            return False

        # Check content (basic)
        if answer.lower().strip() in ["i don't know", "unclear", "no answer"]:
            return False

        return True

    def _calculate_confidence(self, answer: str, critique: str) -> float:
        """Tính confidence score dựa trên độ dài và chất lượng."""
        # Simple heuristic: longer, more detailed = higher confidence
        answer_score = min(len(answer) / 500, 1.0)  # Normalize to 0-1
        critique_score = min(len(critique) / 100, 1.0)

        # Penalize uncertainty markers
        uncertainty_markers = ["maybe", "possibly", "not sure", "unclear", "uncertain"]
        uncertainty_penalty = 0.0
        for marker in uncertainty_markers:
            if marker in answer.lower():
                uncertainty_penalty += 0.1

        confidence = (answer_score + critique_score) / 2 - uncertainty_penalty
        return max(0.0, min(1.0, confidence))

    def _calculate_complexity(self, prompt: str, answer: str) -> float:
        """Tính complexity score dựa trên độ phức tạp của prompt và answer."""
        # Simple heuristic: longer prompt + detailed answer = higher complexity
        prompt_complexity = min(len(prompt.split()) / 50, 1.0)
        answer_complexity = min(len(answer.split()) / 200, 1.0)

        # Bonus for technical terms
        tech_terms = [
            "algorithm",
            "function",
            "class",
            "method",
            "implementation",
            "architecture",
        ]
        tech_bonus = sum(1 for term in tech_terms if term in answer.lower()) * 0.1

        complexity = (prompt_complexity + answer_complexity) / 2 + tech_bonus
        return max(0.0, min(1.0, complexity))


# Convenience function để sử dụng nhanh
async def distill_examples(
    examples: list[RawExample],
    dataset_name: str,
    description: str = "",
) -> str:
    """Convenience function để distill examples thành dataset.

    Args:
        examples: Raw examples cần distill
        dataset_name: Tên dataset
        description: Mô tả dataset

    Returns:
        dataset_id của dataset đã tạo
    """
    service = DistillationService()
    return await service.distill_and_save(
        examples=examples,
        dataset_name=dataset_name,
        description=description,
    )
