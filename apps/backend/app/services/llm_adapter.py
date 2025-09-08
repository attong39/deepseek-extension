"""
Local LLM Adapter - 100% offline inference
Không sử dụng OpenAI hoặc external APIs
Mock implementation for development - sẽ thay thế bằng transformers khi ready
"""

from __future__ import annotations

import logging
import os
import random
from typing import Any
import Exception
import bool
import dict
import e
import float
import isinstance
import result
import return_scores
import rules
import str
import temperature
import text

logger = logging.getLogger(__name__)

MODEL_PATH = os.getenv("LOCAL_MODEL_PATH", "mock-local-model")
TEACHER_MODE = os.getenv("TEACHER_MODE", "disabled")

# Mock responses for development
MOCK_RESPONSES = [
    "Tôi hiểu yêu cầu của bạn và sẽ cố gắng hỗ trợ tốt nhất có thể.",
    "Đây là một câu trả lời được tạo bởi mô hình AI cục bộ.",
    "Dựa trên quy tắc đã được thiết lập, tôi khuyên bạn nên...",
    "Vấn đề này có thể được giải quyết bằng cách...",
    "Theo kinh nghiệm của tôi, cách tốt nhất là...",
]


def generate_local(
    prompt: str, temperature: float = 0.7, return_scores: bool = False
) -> str | dict[str, Any]:
    """
    Generate text using local model (mock implementation)

    Args:
        prompt: Input text
        max_new_tokens: Maximum tokens to generate
        temperature: Sampling temperature
        do_sample: Whether to use sampling
        return_scores: Whether to return confidence scores

    Returns:
        Generated text or dict with text and scores
    """
    # Simulate processing time
    # TODO: Replace blocking sleep with async await asyncio.sleep(0.1 + random.uniform(0, 0.3))

    # Generate mock response
    if "rules" in prompt.lower() or "quy tắc" in prompt.lower():
        base_response = "Dựa trên quy tắc được cung cấp, " + random.choice(
            MOCK_RESPONSES
        )
    else:
        base_response = random.choice(MOCK_RESPONSES)

    # Add variety based on temperature
    if temperature > 0.8:
        base_response += " (phản hồi có tính sáng tạo cao)"
    elif temperature < 0.3:
        base_response += " (phản hồi có tính chính xác cao)"

    if return_scores:
        # Mock confidence scores
        avg_entropy = random.uniform(0.5, 2.0)
        confidence = 1.0 / (1.0 + avg_entropy)

        return {
            "text": base_response,
            "avg_entropy": avg_entropy,
            "confidence": confidence,
        }
    else:
        return base_response


def generate_with_entropy(text: str, rules: str | None = None) -> dict[str, Any]:
    """Generate response with uncertainty estimation"""
    if TEACHER_MODE == "enabled":
        # In real implementation, this would call teacher model
        logger.warning("Teacher mode is enabled but not implemented in mock")

    prompt = (
        f"Quy tắc:\n{rules}\n\nNgười dùng:\n{text}\nTrợ lý:"
        if rules
        else f"Người dùng: {text}\nTrợ lý:"
    )

    _ = generate_local(prompt, return_scores=True)

    if isinstance(result, dict):
        return result
    else:
        # Fallback if something goes wrong
        return {"text": result, "avg_entropy": 1.5, "confidence": 0.5}


def get_model_info() -> dict[str, Any]:
    """Get information about the loaded model"""
    return {
        "model_path": MODEL_PATH,
        "model_type": "MockLocalModel",
        "device": "cpu",
        "status": "mock_implementation",
        "teacher_mode": TEACHER_MODE,
        "features": ["text_generation", "confidence_scoring"],
        "limitations": ["mock_responses_only", "no_real_training"],
    }


def health_check() -> dict[str, Any]:
    """Check if LLM service is healthy"""
    try:
        test_output = generate_local("Test")
        return {
            "status": "healthy_mock",
            "model_loaded": True,
            "test_generation": bool(test_output),
            "implementation": "mock",
            **get_model_info(),
        }
    except Exception as e:
        return {"status": "error", "error": str(e), "model_loaded": False}
