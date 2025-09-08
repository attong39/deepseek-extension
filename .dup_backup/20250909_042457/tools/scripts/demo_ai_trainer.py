#!/usr/bin/env python3
"""Demo script cho AI Trainer 24/7 system.

Script này demo toàn bộ flow:
1. Tạo mock datasets
2. Distill với GPT-5 teacher
3. Fine-tune Llama 4 student
4. Evaluate với GPT-5 verifier
5. Khởi động workflow 24/7

Chạy: python scripts/demo_ai_trainer.py
"""

from __future__ import annotations

import asyncio
import logging
import sys
from pathlib import Path
import Exception
import ImportError
import e
import len
import model
import print
import report
import str

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from apps.backend.trainer import (
    distill_examples,
    evaluate_model_quick,
    model_matrix,
    orchestrator,
    registry,
)
from apps.backend.trainer.distill_gpt5 import RawExample
from apps.backend.trainer.model_matrix import get_student_model, get_teacher_model

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


async def demo_dataset_creation():
    """Demo 1: Tạo và distill dataset."""
    logger.info("=== DEMO 1: Dataset Creation & Distillation ===")

    # Tạo mock examples
    mock_examples = [
        RawExample(
            prompt="What is machine learning?",
            context="Educational content about AI",
            refs=["https://en.wikipedia.org/wiki/Machine_learning"],
        ),
        RawExample(
            prompt="Explain how neural networks work",
            context="Deep learning fundamentals",
            refs=["https://example.com/neural-nets"],
        ),
        RawExample(
            prompt="What are the benefits of renewable energy?",
            context="Environmental science topic",
            refs=["https://example.com/renewable-energy"],
        ),
        RawExample(
            prompt="How to implement quicksort algorithm?",
            context="Computer science algorithms",
            refs=["https://example.com/quicksort"],
        ),
    ]

    # Distill với GPT-5 (mock)
    try:
        dataset_id = await distill_examples(
            examples=mock_examples,
            dataset_name="demo_educational_content",
            description="Demo dataset với educational content đa dạng",
        )

        logger.info(f"✅ Created and distilled dataset: {dataset_id}")

        # Show dataset info
        dataset_info = registry.get_dataset(dataset_id)
        if dataset_info:
            logger.info(f"   - Stage: {dataset_info.stage}")
            logger.info(f"   - Sample count: {dataset_info.sample_count}")
            logger.info(f"   - Quality score: {dataset_info.quality.overall_score if dataset_info.quality else 'N/A'}")

        return dataset_id

    except Exception as e:
        logger.error(f"❌ Dataset creation failed: {e}")
        return None


def demo_model_matrix():
    """Demo 2: Model matrix và routing."""
    logger.info("=== DEMO 2: Model Matrix ===")

    # Show available models
    logger.info("Available models:")
    models = model_matrix.list_models()
    for model in models:
        logger.info(f"   - {model.name} ({model.role.value}, {model.provider})")

    # Demo model selection
    teacher = get_teacher_model()
    if teacher:
        logger.info(f"✅ Teacher model: {teacher.name}")

    student = get_student_model()
    if student:
        logger.info(f"✅ Student model: {student.name}")

    # Demo task routing
    from apps.backend.trainer.model_matrix import TaskType

    coding_model = model_matrix.select_model(TaskType.CODING, require_local=True)
    if coding_model:
        logger.info(f"✅ Best coding model (local): {coding_model.name}")

    vision_model = model_matrix.select_model(TaskType.DOCUMENT_VISION)
    if vision_model:
        logger.info(f"✅ Best vision model: {vision_model.name}")


def demo_training(dataset_id: str):
    """Demo 3: Fine-tuning (mock)."""
    logger.info("=== DEMO 3: Model Training ===")

    if not dataset_id:
        logger.warning("⚠️ No dataset ID provided, skipping training")
        return None

    try:
        # Check dataset ready
        dataset_info = registry.get_dataset(dataset_id)
        if not dataset_info:
            logger.error("❌ Dataset not found")
            return None

        logger.info(f"Training with dataset: {dataset_info.name}")

        # Mock training (thực tế sẽ train Llama 4)
        # model_path = fine_tune_from_dataset(dataset_id)

        # For demo, just simulate
        model_path = f"models/llama4-demo-{dataset_id[:8]}"
        logger.info(f"✅ Training completed (mock): {model_path}")

        return model_path

    except Exception as e:
        logger.error(f"❌ Training failed: {e}")
        return None


async def demo_evaluation(model_path: str):
    """Demo 4: Evaluation với GPT-5 verifier."""
    logger.info("=== DEMO 4: Model Evaluation ===")

    if not model_path:
        logger.warning("⚠️ No model path provided, skipping evaluation")
        return False

    try:
        # Evaluate model
        passes_gate, report = await evaluate_model_quick(
            model_name="llama4-demo",
            model_path=model_path,
            threshold=0.75,
        )

        logger.info("✅ Evaluation completed:")
        logger.info(f"   - Overall score: {report.avg_overall:.2f}")
        logger.info(f"   - Safety score: {report.avg_safety:.2f}")
        logger.info(f"   - Passes quality gate: {passes_gate}")
        logger.info(f"   - Recommendation: {report.recommendation}")

        return passes_gate

    except Exception as e:
        logger.error(f"❌ Evaluation failed: {e}")
        return False


def demo_workflow_status():
    """Demo 5: Workflow status."""
    logger.info("=== DEMO 5: Workflow Status ===")

    try:
        from apps.backend.trainer import get_learning_status

        status = get_learning_status()

        logger.info("Workflow status:")
        logger.info(f"   - Running: {status['workflow']['is_running']}")
        logger.info(f"   - Total ingested: {status['workflow']['total_ingested']}")
        logger.info(f"   - Total labeled: {status['workflow']['total_labeled']}")
        logger.info(f"   - Total trained: {status['workflow']['total_trained']}")
        logger.info(f"   - Active tasks: {len(status['workflow']['active_tasks'])}")

        # Registry stats
        logger.info("Registry stats:")
        registry_stats = status["registry_stats"]
        logger.info(f"   - Total datasets: {registry_stats['total_datasets']}")
        logger.info(f"   - Total samples: {registry_stats['total_samples']}")
        logger.info(f"   - Average quality: {registry_stats['average_quality']:.2f}")

    except Exception as e:
        logger.error(f"❌ Failed to get workflow status: {e}")


def demo_workflow_start():
    """Demo 6: Start workflow (mock)."""
    logger.info("=== DEMO 6: Workflow Control ===")

    try:
        logger.info("Current workflow status:")
        logger.info(f"   - Running: {orchestrator.status.is_running}")
        logger.info(f"   - Started at: {orchestrator.status.started_at}")

        if not orchestrator.status.is_running:
            logger.info("Starting 24/7 learning workflow (mock)...")
            # await start_24_7_learning()  # Mock for demo
            logger.info("✅ Workflow started (mock)")
        else:
            logger.info("✅ Workflow already running")

    except Exception as e:
        logger.error(f"❌ Failed to control workflow: {e}")


async def main():
    """Main demo function."""
    logger.info("🚀 Starting AI Trainer 24/7 Demo")
    logger.info("=" * 50)

    try:
        # Demo 1: Dataset creation
        dataset_id = await demo_dataset_creation()
        print()

        # Demo 2: Model matrix
        demo_model_matrix()
        print()

        # Demo 3: Training (mock)
        model_path = demo_training(dataset_id) if dataset_id else None
        print()

        # Demo 4: Evaluation
        passes_gate = await demo_evaluation(model_path) if model_path else False
        print()

        # Demo 5: Workflow status
        demo_workflow_status()
        print()

        # Demo 6: Workflow control
        demo_workflow_start()
        print()

        logger.info("=" * 50)
        logger.info("🎉 Demo completed successfully!")

        if dataset_id:
            logger.info(f"📊 Created dataset: {dataset_id}")
        if model_path:
            logger.info(f"🤖 Trained model: {model_path}")
        if passes_gate:
            logger.info("✅ Model passed quality gate!")

        logger.info("\n💡 Next steps:")
        logger.info("   1. Set up real OpenAI API keys")
        logger.info("   2. Configure GPU for Llama 4 training")
        logger.info("   3. Implement actual web crawlers")
        logger.info("   4. Start 24/7 workflow: await start_24_7_learning()")

    except Exception as e:
        logger.error(f"💥 Demo failed: {e}")
        raise


if __name__ == "__main__":
    # Check dependencies
    try:
        import torch

        logger.info(f"✅ PyTorch available: {torch.__version__}")
    except ImportError:
        logger.warning("⚠️ PyTorch not available - training will not work")

    try:
        import transformers

        logger.info(f"✅ Transformers available: {transformers.__version__}")
    except ImportError:
        logger.warning("⚠️ Transformers not available - training will not work")

    # Run demo
    asyncio.run(main())
