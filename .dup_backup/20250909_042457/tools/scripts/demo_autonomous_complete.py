#!/usr/bin/env python3
"""
🚀 ZETA_AI Autonomous System Demo

Demo showcase cho complete autonomous loop implementation:
- HybridPlanner với rule-based và LLM modes
- JWT middleware security
- WebSocket real-time updates
- Outbox worker event processing
- Safety policy enforcement
- Skill execution system

Chạy: python scripts/demo_autonomous_complete.py
"""

import asyncio
import logging

from apps.backend.core.domain.autonomy import AutonomySession, Goal
from apps.backend.core.services.autonomy_planner import HybridPlanner
from apps.backend.core.services.autonomy_safety import RuleBasedSafetyPolicy
from apps.backend.core.services.autonomy_skills import SafeSkillRegistry
from apps.backend.core.services.outbox_worker import AutonomyEvent, OutboxWorker
import Exception
import action_data
import count
import e
import enumerate
import event
import i
import is_safe
import key
import len
import print
import reason
import request
import self
import skill
import status
import str
import value

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class AutonomousSystemDemo:
    """
    Complete autonomous system demo showcasing all components.
    """

    def __init__(self):
        self.planner = HybridPlanner(mode="hybrid")
        self.safety_engine = RuleBasedSafetyPolicy()
        self.skill_registry = SafeSkillRegistry()
        self.outbox_worker = OutboxWorker()

        self.session: AutonomySession = None
        self.demo_stats = {
            "goals_processed": 0,
            "plans_created": 0,
            "actions_executed": 0,
            "safety_blocks": 0,
            "events_published": 0,
        }

    async def run_complete_demo(self) -> None:
        """Run complete autonomous system demo."""
        try:
            print("\n" + "=" * 80)
            print("🚀 ZETA_AI AUTONOMOUS SYSTEM - COMPLETE DEMO")
            print("=" * 80)

            # Start outbox worker
            await self.outbox_worker.start()
            print("✅ Outbox worker started")

            # Demo 1: Simple goal with rule-based planning
            await self._demo_simple_autonomous_loop()

            # Demo 2: Complex goal with hybrid planning
            await self._demo_complex_autonomous_loop()

            # Demo 3: Safety policy enforcement
            await self._demo_safety_enforcement()

            # Demo 4: Skills execution
            await self._demo_skills_execution()

            # Demo 5: Event processing
            await self._demo_event_processing()

            # Show final statistics
            await self._show_final_stats()

        except Exception as e:
            logger.error(f"Demo error: {e}")
            raise
        finally:
            # Cleanup
            await self.outbox_worker.stop()
            print("🛑 Demo completed, outbox worker stopped")

    async def _demo_simple_autonomous_loop(self) -> None:
        """Demo simple autonomous loop with rule-based planning."""
        print("\n📋 DEMO 1: Simple Autonomous Loop (Rule-based)")
        print("-" * 50)

        # Create session
        goal = self.session.goal

        self.session = AutonomySession(goal=goal)
        print(f"✅ Created session: {self.session.id}")
        print(f"🎯 Goal: {goal.description}")
        self.demo_stats["goals_processed"] += 1

        # Force rule-based mode for this demo
        original_mode = self.planner.mode
        self.planner.set_mode("rule")

        # Create plan
        plan = self.planner.create_plan(goal)
        print(f"📊 Plan created with {len(plan.steps)} steps:")
        for i, action in enumerate(plan.steps, 1):
            print(f"   {i}. {action.name}: {action.params}")

        self.demo_stats["plans_created"] += 1
        goal.current_plan_id = plan.id

        # Simulate action execution
        for action in plan.steps:
            print(f"⚡ Executing: {action.name}")

            # Safety check
            is_safe, reason = self.safety_engine.evaluate_action_safety(action)
            if not is_safe:
                print(f"🛑 Action blocked: {reason}")
                self.demo_stats["safety_blocks"] += 1
                continue

            # Execute action (simulated)
            await asyncio.sleep(0.1)  # Simulate execution time
            action.status = "completed"
            action.result = {"status": "success", "message": f"Executed {action.name}"}
            self.demo_stats["actions_executed"] += 1
            print(f"✅ Completed: {action.name}")

        # Restore original mode
        self.planner.set_mode(original_mode)

        print("✨ Simple autonomous loop completed!")

    async def _demo_complex_autonomous_loop(self) -> None:
        """Demo complex autonomous loop with hybrid planning."""
        print("\n🧠 DEMO 2: Complex Autonomous Loop (Hybrid)")
        print("-" * 50)

        # Create complex goal
        complex_goal = Goal(
            user_id="demo_user_001",
            description="analyze website traffic patterns and create detailed performance report with recommendations for optimization",
            budget_seconds=300,
        )
        print(f"🎯 Complex Goal: {complex_goal.description}")

        # Check complexity
        is_complex = self.planner._is_complex_goal(complex_goal.description)
        print(f"🔍 Goal complexity detected: {is_complex}")

        # Create hybrid plan
        self.planner.set_mode("hybrid")
        plan = self.planner.create_plan(complex_goal)
        print(f"📊 Hybrid plan created with {len(plan.steps)} steps:")
        for i, action in enumerate(plan.steps, 1):
            print(f"   {i}. {action.name}: {action.params}")

        self.demo_stats["plans_created"] += 1
        self.demo_stats["goals_processed"] += 1

        # Simulate execution of first few actions
        for action in plan.steps[:3]:  # Execute first 3 actions
            print(f"⚡ Executing: {action.name}")

            # Safety evaluation
            is_safe, reason = self.safety_engine.evaluate_action_safety(action)
            if is_safe:
                await asyncio.sleep(0.1)
                action.status = "completed"
                self.demo_stats["actions_executed"] += 1
                print(f"✅ Completed: {action.name}")
            else:
                print(f"🛑 Blocked: {reason}")
                self.demo_stats["safety_blocks"] += 1

        print("✨ Complex autonomous loop demonstrated!")

    async def _demo_safety_enforcement(self) -> None:
        """Demo safety policy enforcement."""
        print("\n🛡️ DEMO 3: Safety Policy Enforcement")
        print("-" * 50)

        # Test various safety scenarios
        test_actions = [
            {"name": "write_file", "params": {"path": "safe_file.txt", "content": "Hello"}},
            {"name": "execute_command", "params": {"command": "ls -la"}},
            {"name": "open_url", "params": {"url": "https://malicious-site.com"}},
            {"name": "read_file", "params": {"path": "/etc/passwd"}},
            {"name": "send_request", "params": {"url": "http://safe-api.com/data"}},
        ]

        from apps.backend.core.domain.autonomy import Action

        for action_data in test_actions:
            action = Action(name=action_data["name"], params=action_data["params"])

            is_safe, reason = self.safety_engine.evaluate_action_safety(action)
            status_icon = "✅" if is_safe else "🛑"
            print(f"{status_icon} {action.name}: {reason}")

            if not is_safe:
                self.demo_stats["safety_blocks"] += 1

        print("✨ Safety enforcement demonstrated!")

    async def _demo_skills_execution(self) -> None:
        """Demo skill registry and execution."""
        print("\n🎯 DEMO 4: Skills System")
        print("-" * 50)

        # Get available skills
        skills = self.skill_registry.list_skills()
        print(f"📚 Available skills: {len(skills)}")
        for skill in skills[:5]:  # Show first 5
            print(f"   • {skill.name}: {skill.description}")

        # Demo skill execution
        test_skill_requests = [
            {"skill": "log_message", "params": {"message": "Demo log entry"}},
            {"skill": "write_file", "params": {"path": "demo.txt", "content": "Test content"}},
            {"skill": "unknown_skill", "params": {}},
        ]

        for request in test_skill_requests:
            skill_name = request["skill"]
            params = request["params"]

            try:
                result = await self.skill_registry.execute_skill(skill_name, params)
                print(f"✅ {skill_name}: {result}")
                self.demo_stats["actions_executed"] += 1
            except Exception as e:
                print(f"❌ {skill_name}: {str(e)}")

        print("✨ Skills system demonstrated!")

    async def _demo_event_processing(self) -> None:
        """Demo event publishing and processing."""
        print("\n📡 DEMO 5: Event Processing")
        print("-" * 50)

        # Create sample events
        events = [
            AutonomyEvent(
                event_type="goal_created",
                aggregate_id="demo_goal_001",
                event_data={
                    "goal_id": "demo_goal_001",
                    "user_id": "demo_user_001",
                    "description": "Demo goal for event processing",
                },
            ),
            AutonomyEvent(
                event_type="plan_completed",
                aggregate_id="demo_plan_001",
                event_data={
                    "plan_id": "demo_plan_001",
                    "goal_id": "demo_goal_001",
                    "steps_count": 3,
                    "success_rate": 100.0,
                },
            ),
            AutonomyEvent(
                event_type="safety_violation",
                aggregate_id="demo_action_001",
                event_data={
                    "action_name": "dangerous_operation",
                    "violation_type": "file_access",
                    "severity": "high",
                    "user_id": "demo_user_001",
                },
            ),
        ]

        # Publish events
        for event in events:
            event_id = await self.outbox_worker.add_event(event)
            print(f"📤 Published event: {event.event_type} (ID: {event_id[:8]}...)")
            self.demo_stats["events_published"] += 1

        # Let worker process events
        print("⏳ Processing events...")
        await asyncio.sleep(2.0)

        # Check worker stats
        worker_stats = self.outbox_worker.get_stats()
        print("📊 Worker stats:")
        for status, count in worker_stats["status_counts"].items():
            if count > 0:
                print(f"   • {status}: {count}")

        print("✨ Event processing demonstrated!")

    async def _show_final_stats(self) -> None:
        """Show final demo statistics."""
        print("\n📈 FINAL DEMO STATISTICS")
        print("-" * 50)

        for key, value in self.demo_stats.items():
            formatted_key = key.replace("_", " ").title()
            print(f"📊 {formatted_key}: {value}")

        # Planner capabilities
        capabilities = self.planner.get_capabilities()
        print("\n🤖 Planner Capabilities:")
        for key, value in capabilities.items():
            print(f"   • {key}: {value}")

        print("\n🎉 AUTONOMOUS SYSTEM DEMO COMPLETED!")
        print("=" * 80)


async def main():
    """Main demo function."""
    demo = AutonomousSystemDemo()
    await demo.run_complete_demo()


if __name__ == "__main__":
    asyncio.run(main())
