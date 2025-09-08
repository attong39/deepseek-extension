#!/usr/bin/env python3
"""Demo đơn giản cho AI Trainer 24/7 system (không cần dependencies nặng).

Script này demo core concepts mà không cần PyTorch/Transformers:
1. Dataset registry
2. Model matrix
3. Workflow orchestration concepts
"""

from __future__ import annotations

import asyncio
import logging
import sys
from pathlib import Path
import Exception
import ImportError
import component
import dep
import description
import e
import len
import model
import print
import str
import success
import sum

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def demo_dataset_registry():
    """Demo dataset registry."""
    logger.info("=== DEMO 1: Dataset Registry ===")

    try:
        from apps.backend.trainer.datasets.registry import DatasetStage, registry

        # Create mock dataset
        dataset_id = registry.register_dataset(
            name="demo_educational_content",
            description="Demo dataset với educational content đa dạng",
            source_type="manual",
        )

        logger.info(f"✅ Created dataset: {dataset_id}")

        # Update quality score
        from apps.backend.trainer.datasets.registry import DatasetQualityScore

        quality = DatasetQualityScore(
            safety_score=0.95,
            quality_score=0.88,
            uniqueness_score=0.92,
            relevance_score=0.85,
        )
        registry.update_quality(dataset_id, quality)
        registry.update_stage(dataset_id, DatasetStage.LABELED)

        # Show stats
        stats = registry.get_stats()
        logger.info(f"   - Total datasets: {stats['total_datasets']}")
        logger.info(f"   - Average quality: {stats['average_quality']:.2f}")

        # List datasets
        datasets = registry.list_datasets(min_quality=0.8)
        logger.info(f"   - High quality datasets: {len(datasets)}")

        return dataset_id

    except Exception as e:
        logger.error(f"❌ Dataset registry demo failed: {e}")
        return None


def demo_model_matrix():
    """Demo model matrix."""
    logger.info("=== DEMO 2: Model Matrix ===")

    try:
        from apps.backend.trainer.model_matrix import ModelRole, TaskType, model_matrix

        # Show available models
        models = model_matrix.list_models()
        logger.info(f"✅ Found {len(models)} models:")

        for model in models[:5]:  # Show first 5
            logger.info(f"   - {model.name} ({model.role.value}, {model.provider})")

        # Demo model selection
        teacher = model_matrix.select_model(task=TaskType.LABELING, role=ModelRole.TEACHER)
        if teacher:
            logger.info(f"✅ Best teacher model: {teacher.name}")

        student = model_matrix.select_model(task=TaskType.REASONING, role=ModelRole.STUDENT, require_local=True)
        if student:
            logger.info(f"✅ Best local student model: {student.name}")

        # Cost estimation
        if teacher:
            cost = model_matrix.get_cost_estimate(teacher.name, input_tokens=1000, output_tokens=500)
            logger.info(f"   - Estimated cost for 1.5k tokens: ${cost:.4f}")

        return True

    except Exception as e:
        logger.error(f"❌ Model matrix demo failed: {e}")
        return False


async def demo_distillation_basic():
    """Demo basic distillation concepts."""
    logger.info("=== DEMO 3: Distillation Concepts ===")

    try:
        from apps.backend.trainer.distill_gpt5 import DistillationConfig, LabeledExample, RawExample

        # Create mock examples
        examples = [
            RawExample(
                prompt="What is machine learning?",
                context="Educational content about AI",
            ),
            RawExample(
                prompt="Explain neural networks",
                context="Deep learning fundamentals",
            ),
        ]

        logger.info(f"✅ Created {len(examples)} raw examples")

        # Show config
        config = DistillationConfig()
        logger.info("✅ Distillation config:")
        logger.info(f"   - Teacher model: {config.teacher_model}")
        logger.info(f"   - Batch size: {config.batch_size}")
        logger.info(f"   - Temperature: {config.temperature}")

        # Mock labeled example
        labeled = LabeledExample(
            prompt=examples[0].prompt,
            answer="Machine learning is a subset of AI that enables computers to learn and improve from experience without being explicitly programmed.",
            critique="This answer provides a clear, concise definition that captures the essence of ML.",
            teacher_model=config.teacher_model,
            teacher_version="20250824",
            source_id=examples[0].id,
            confidence_score=0.92,
            complexity_score=0.75,
        )

        logger.info("✅ Mock labeled example:")
        logger.info(f"   - Confidence: {labeled.confidence_score:.2f}")
        logger.info(f"   - Complexity: {labeled.complexity_score:.2f}")

        return True

    except Exception as e:
        logger.error(f"❌ Distillation demo failed: {e}")
        return False


async def demo_evaluation_concepts():
    """Demo evaluation concepts."""
    logger.info("=== DEMO 4: Evaluation Concepts ===")

    try:
        from apps.backend.trainer.evaluators.gpt5_verifier import (
            BenchmarkTask,
            EvaluationReport,
            EvaluationScore,
            TaskCategory,
        )

        # Create mock benchmark task
        task = BenchmarkTask(
            id="demo_task_1",
            category=TaskCategory.REASONING,
            prompt="If all cats are animals, and some animals are pets, can we conclude that some cats are pets?",
            expected_output="No, we cannot conclude that some cats are pets.",
            evaluation_criteria="Check logical reasoning accuracy",
            difficulty=3,
        )

        logger.info(f"✅ Created benchmark task: {task.category.value}")

        # Mock evaluation score
        score = EvaluationScore(
            task_id=task.id,
            category=task.category,
            accuracy=0.85,
            quality=0.88,
            safety=0.95,
            instruction_following=0.82,
            explanation="Good logical reasoning with minor presentation issues",
        )

        logger.info("✅ Mock evaluation score:")
        logger.info(f"   - Overall: {score.overall_score:.2f}")
        logger.info(f"   - Safety: {score.safety:.2f}")

        # Mock evaluation report
        report = EvaluationReport(
            model_name="demo-model",
            total_tasks=5,
            completed_tasks=5,
            scores=[score] * 5,  # Mock 5 identical scores
        )

        report.calculate_aggregates()

        logger.info("✅ Evaluation report:")
        logger.info(f"   - Passes quality gate: {report.passes_quality_gate}")
        logger.info(f"   - Average score: {report.avg_overall:.2f}")

        return report.passes_quality_gate

    except Exception as e:
        logger.error(f"❌ Evaluation demo failed: {e}")
        return False


def demo_workflow_concepts():
    """Demo workflow orchestration concepts."""
    logger.info("=== DEMO 5: Workflow Concepts ===")

    try:
        from apps.backend.trainer.workflows.trainer_workflow import TrainerOrchestrator, WorkflowConfig

        # Show config
        config = WorkflowConfig()
        logger.info("✅ Workflow config:")
        logger.info(f"   - Ingest interval: {config.ingest_interval_minutes} min")
        logger.info(f"   - Training interval: {config.training_interval_hours} hours")
        logger.info(f"   - Min quality score: {config.min_quality_score}")

        # Create orchestrator
        orchestrator = TrainerOrchestrator(config)

        # Show status
        status = orchestrator.status
        logger.info("✅ Workflow status:")
        logger.info(f"   - Running: {status.is_running}")
        logger.info(f"   - Started at: {status.started_at}")
        logger.info(f"   - Total ingested: {status.total_ingested}")

        # Mock status update
        status.total_ingested = 100
        status.total_labeled = 80
        status.total_trained = 5

        logger.info("✅ Mock workflow progress:")
        logger.info(f"   - Ingested: {status.total_ingested}")
        logger.info(f"   - Labeled: {status.total_labeled}")
        logger.info(f"   - Trained: {status.total_trained}")

        return True

    except Exception as e:
        logger.error(f"❌ Workflow demo failed: {e}")
        return False


async def main():
    """Main demo function."""
    logger.info("🚀 Starting AI Trainer 24/7 Basic Demo")
    logger.info("=" * 50)

    results = {}

    try:
        # Demo 1: Dataset registry
        dataset_id = demo_dataset_registry()
        results["dataset"] = dataset_id is not None
        print()

        # Demo 2: Model matrix
        model_success = demo_model_matrix()
        results["models"] = model_success
        print()

        # Demo 3: Distillation concepts
        distill_success = await demo_distillation_basic()
        results["distillation"] = distill_success
        print()

        # Demo 4: Evaluation concepts
        eval_success = await demo_evaluation_concepts()
        results["evaluation"] = eval_success
        print()

        # Demo 5: Workflow concepts
        workflow_success = demo_workflow_concepts()
        results["workflow"] = workflow_success
        print()

        # Summary
        logger.info("=" * 50)
        logger.info("🎉 Demo Summary:")

        for component, success in results.items():
            status = "✅ PASS" if success else "❌ FAIL"
            logger.info(f"   - {component.title()}: {status}")

        total_success = sum(results.values())
        total_tests = len(results)
        logger.info(f"\n📊 Results: {total_success}/{total_tests} components working")

        if total_success == total_tests:
            logger.info("🏆 All systems operational!")

        logger.info("\n💡 Next steps to enable full AI learning:")
        logger.info("   1. Install ML dependencies: pip install openai transformers datasets torch")
        logger.info("   2. Set OPENAI_API_KEY environment variable")
        logger.info("   3. Configure GPU for local model training")
        logger.info("   4. Implement web crawlers and data ingestion")
        logger.info("   5. Start 24/7 workflow with real data")

        logger.info("\n📖 API endpoints available at:")
        logger.info("   - /api/v1/ai-trainer/datasets")
        logger.info("   - /api/v1/ai-trainer/models/matrix")
        logger.info("   - /api/v1/ai-trainer/workflow/status")
        logger.info("   - /api/v1/ai-trainer/stats/overview")

    except Exception as e:
        logger.error(f"💥 Demo failed: {e}")
        raise


if __name__ == "__main__":
    # Check basic Python setup
    logger.info(f"✅ Python {sys.version}")
    logger.info(f"✅ Project root: {project_root}")

    # Check optional dependencies
    optional_deps = {
        "torch": "PyTorch for model training",
        "transformers": "Hugging Face transformers",
        "datasets": "Hugging Face datasets",
        "openai": "OpenAI API client",
        "peft": "Parameter-Efficient Fine-Tuning",
    }

    for dep, description in optional_deps.items():
        try:
            __import__(dep)
            logger.info(f"✅ {dep} available")
        except ImportError:
            logger.warning(f"⚠️ {dep} not available - {description} disabled")

    # Run demo
    asyncio.run(main())
