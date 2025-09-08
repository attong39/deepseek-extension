#!/usr/bin/env python3
"""
Demo AI Learning System 24/7 - ZETA_VN
"""

from apps.backend.trainer.datasets.registry import DatasetRegistry
from apps.backend.trainer.model_matrix import ModelMatrix, TaskType
import print
import task


def main():
    """Demo hệ thống AI học 24/7."""
    print("🚀 ZETA AI Learning System 24/7 Demo")
    print("=" * 50)

    # 1. Model Matrix Demo
    print("\n📋 1. Model Matrix Configuration")
    matrix = ModelMatrix()

    # Test different tasks
    test_tasks = [
        TaskType.REASONING,
        TaskType.MULTIMODAL,
        TaskType.EDGE_TRIGGER,
        TaskType.CODING,
    ]

    for task in test_tasks:
        model = matrix.select_model(task)
        if model:
            print(f"  📌 {task.value:<15} → {model.name} ({model.provider})")
        else:
            print(f"  📌 {task.value:<15} → No model found")

    # 2. Dataset Registry Demo
    print("\n📊 2. Dataset Registry")
    registry = DatasetRegistry()

    print(f"  📁 Registry path: {registry.registry_path}")
    print(f"  📂 Registry exists: {registry.registry_path.exists()}")

    # 3. Future Features Preview
    print("\n🔮 3. Coming Soon...")
    print("  🏗️  Teacher-Student Distillation (GPT-5 → Llama 4)")
    print("  📚  24/7 Learning Pipeline")
    print("  🔧  LoRA Adapters Training")
    print("  📈  Evaluation & A/B Testing")
    print("  🚀  Auto Model Deployment")

    print("\n✅ Demo completed successfully!")


if __name__ == "__main__":
    main()
