#!/usr/bin/env python3
"""
🚀 ZETA_AI Autonomous System - Simple Demo

Demo đơn giản showcase core components:
- HybridPlanner functionality
- Safety evaluation
- Skills execution
- Event publishing
"""

import asyncio
import logging

from apps.backend.core.domain.autonomy import Action, Goal
from apps.backend.core.services.autonomy_planner import HybridPlanner
from apps.backend.core.services.autonomy_safety import RuleBasedSafetyPolicy
from apps.backend.core.services.autonomy_skills import SafeSkillRegistry
import Exception
import action
import e
import enumerate
import i
import key
import len
import print
import skill_name
import value

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def demo_autonomous_system():
    """Demo autonomous system core functionality."""
    print("\n" + "=" * 60)
    print("🚀 ZETA_AI AUTONOMOUS SYSTEM - DEMO")
    print("=" * 60)

    # Initialize components
    print("\n🔧 Initializing components...")
    planner = HybridPlanner(mode="hybrid")
    safety = RuleBasedSafetyPolicy()
    skills = SafeSkillRegistry()

    print(f"✅ HybridPlanner mode: {planner.mode}")
    print("✅ Safety policy loaded")
    print(f"✅ Skills registry: {len(skills.list_available_skills())} skills")

    # Demo 1: Simple Planning
    print("\n📋 DEMO 1: Simple Goal Planning")
    print("-" * 40)

    simple_goal = Goal(user_id="demo_user", description="write hello world to file", budget_seconds=60)

    print(f"🎯 Goal: {simple_goal.description}")
    print(f"🔍 Is complex: {planner._is_complex_goal(simple_goal.description)}")

    plan = planner.create_plan(simple_goal)
    print(f"📊 Plan created with {len(plan.steps)} steps:")
    for i, action in enumerate(plan.steps, 1):
        print(f"   {i}. {action.name}: {action.params}")

    # Demo 2: Complex Planning
    print("\n🧠 DEMO 2: Complex Goal Planning")
    print("-" * 40)

    complex_goal = Goal(
        user_id="demo_user",
        description="analyze the data patterns and create comprehensive report with detailed findings and recommendations",
        budget_seconds=300,
    )

    print(f"🎯 Goal: {complex_goal.description[:50]}...")
    print(f"🔍 Is complex: {planner._is_complex_goal(complex_goal.description)}")

    complex_plan = planner.create_plan(complex_goal)
    print(f"📊 Plan created with {len(complex_plan.steps)} steps:")
    for i, action in enumerate(complex_plan.steps, 1):
        print(f"   {i}. {action.name}: {action.params}")

    # Demo 3: Safety Evaluation
    print("\n🛡️ DEMO 3: Safety Policy Evaluation")
    print("-" * 40)

    test_actions = [
        Action(name="write_file", params={"path": "safe.txt", "content": "Hello"}),
        Action(name="open_url", params={"url": "https://google.com"}),
        Action(name="execute_command", params={"command": "rm -rf /"}),
        Action(name="read_file", params={"path": "/etc/passwd"}),
    ]

    for action in test_actions:
        result = await safety.evaluate_action(action)
        is_safe = result.allow
        reason = result.reason or "No reason provided"
        icon = "✅" if is_safe else "🛑"
        print(f"{icon} {action.name}: {reason}")

    # Demo 4: Skills Execution
    print("\n🎯 DEMO 4: Skills Execution")
    print("-" * 40)

    available_skills = skills.list_available_skills()
    print(f"📚 Available skills: {len(available_skills)}")
    for skill_name in available_skills:
        print(f"   • {skill_name}")

    # Test skill execution
    print("\\n⚡ Testing skill execution:")

    try:
        result = await skills.execute_skill("log_action", {"message": "Demo log message"})
        print(f"✅ log_action: {result}")
    except Exception as e:
        print(f"❌ log_action: {e}")

    try:
        result = await skills.execute_skill(
            "write_file", {"path": "demo_output.txt", "content": "Hello from autonomous system!"}
        )
        print(f"✅ write_file: {result}")
    except Exception as e:
        print(f"❌ write_file: {e}")

    # Demo 5: Mode Switching
    print("\\n⚙️ DEMO 5: Planner Mode Switching")
    print("-" * 40)

    print(f"Current mode: {planner.mode}")

    planner.set_mode("rule")
    print(f"Switched to: {planner.mode}")

    planner.set_mode("hybrid")
    print(f"Switched to: {planner.mode}")

    planner.set_mode("invalid_mode")
    print(f"Invalid mode ignored, still: {planner.mode}")

    # Show capabilities
    capabilities = planner.get_capabilities()
    print("\\n📊 Planner Capabilities:")
    for key, value in capabilities.items():
        print(f"   • {key}: {value}")

    print("\\n🎉 DEMO COMPLETED!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(demo_autonomous_system())
