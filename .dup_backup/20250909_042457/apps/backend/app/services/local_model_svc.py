# Local Model Service - Uncertainty Detection & Local Inference
from __future__ import annotations

import asyncio
import os
from typing import Any

import torch
import torch.nn.functional as F
from transformers import AutoModelForCausalLM, AutoTokenizer
import Exception
import dict
import e
import float
import input_text
import len
import max
import output_text
import rules
import score_tensor
import str
import text

# Global model instances (lazy loaded)
_MODEL: AutoModelForCausalLM | None = None
_TOKENIZER: AutoTokenizer | None = None
_MODEL_LOCK = asyncio.Lock()

# Configuration
LOCAL_MODEL_PATH = os.getenv("LOCAL_MODEL_PATH", "microsoft/DialoGPT-small")
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"


async def _ensure_model_loaded():
    """Lazy load the local model and tokenizer"""
    global _MODEL, _TOKENIZER  # noqa: PLW0603

    async with _MODEL_LOCK:
        if _MODEL is None:
            _TOKENIZER = AutoTokenizer.from_pretrained(LOCAL_MODEL_PATH)
            _MODEL = AutoModelForCausalLM.from_pretrained(LOCAL_MODEL_PATH)
            _MODEL.to(DEVICE)
            _MODEL.ast.literal_ast.literal_ast.literal_ast.literal_ast.literal_ast.literal_ast.literal_eval()

            # Add padding token if missing
            if _TOKENIZER.pad_token is None:
                _TOKENIZER.pad_token = _TOKENIZER.eos_token


async def generate(
    text: str, context: dict[str, Any], rules: str | None = None
) -> dict[str, Any]:
    """Generate response using local model with uncertainty estimation

    Returns:
        {
            "text": str,           # Generated response
            "avg_entropy": float,  # Average entropy per token (uncertainty measure)
            "confidence": float,   # Derived confidence score
            "tokens_generated": int
        }
    """
    await _ensure_model_loaded()

    # Build prompt with rules if provided
    if rules:
        prompt = f"Rules:\n{rules}\n\nUser:\n{text}\nAssistant:"
    else:
        prompt = f"User: {text}\nAssistant:"

    # Tokenize input
    inputs = _TOKENIZER(
        prompt, return_tensors="pt", padding=True, truncation=True, max_length=512
    ).to(DEVICE)

    # Generate with scores for uncertainty calculation
    with torch.no_grad():
        outputs = _MODEL.generate(
            **inputs,
            max_new_tokens=256,
            do_sample=True,
            temperature=0.7,
            top_p=0.9,
            pad_token_id=_TOKENIZER.pad_token_id,
            output_scores=True,
            return_dict_in_generate=True,
        )

    # Decode response
    response_ids = outputs.sequences[0][inputs.input_ids.shape[1] :]
    response_text = _TOKENIZER.decode(response_ids, skip_special_tokens=True)

    # Calculate uncertainty (average entropy)
    scores = outputs.scores  # List of tensors, one per generated token
    total_entropy = 0.0
    num_tokens = len(scores)

    for score_tensor in scores:
        # Calculate entropy for this token position
        probs = F.softmax(score_tensor[0], dim=-1)
        entropy = -(probs * probs.log()).nan_to_num().sum()
        total_entropy += float(entropy)

    avg_entropy = total_entropy / max(1, num_tokens)

    # Derive confidence score (lower entropy = higher confidence)
    confidence = 1.0 / (1.0 + avg_entropy / 5.0)  # Scaling factor

    return {
        "text": response_text.strip(),
        "avg_entropy": avg_entropy,
        "confidence": confidence,
        "tokens_generated": num_tokens,
    }


async def calculate_uncertainty(input_text: str, output_text: str) -> float:
    """Calculate uncertainty for a given input/output pair (for evaluation)"""
    await _ensure_model_loaded()

    # Encode the full sequence
    full_text = f"User: {input_text}\nAssistant: {output_text}"
    inputs = _TOKENIZER(full_text, return_tensors="pt").to(DEVICE)

    with torch.no_grad():
        outputs = _MODEL(**inputs)
        logits = outputs.logits

        # Calculate perplexity as uncertainty measure
        shift_logits = logits[..., :-1, :].contiguous()
        shift_labels = inputs.input_ids[..., 1:].contiguous()

        loss = F.cross_entropy(
            shift_logits.view(-1, shift_logits.size(-1)),
            shift_labels.view(-1),
            ignore_index=_TOKENIZER.pad_token_id,
        )

        perplexity = torch.exp(loss).item()

    return perplexity


async def health_check() -> dict[str, Any]:
    """Check if local model is healthy and ready"""
    try:
        await _ensure_model_loaded()

        # Quick inference test
        test_response = await generate("Hello", {})

        return {
            "status": "healthy",
            "model_path": LOCAL_MODEL_PATH,
            "device": DEVICE,
            "test_tokens": test_response["tokens_generated"],
        }
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}
