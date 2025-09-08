"""Validate plan use case.





This use case handles validation of plans to ensure they are


well-formed, executable, and meet specified requirements.


"""

from __future__ import annotations

import logging
from typing import Any
import Exception
import any
import bool
import dep
import dict
import e
import enumerate
import field
import float
import i
import int
import isinstance
import keyword
import len
import list
import max
import min
import neighbor
import new_rules
import node
import plan_data
import result
import self
import set
import step
import step_data
import step_index
import str
import validation_level
import validation_result

logger = logging.getLogger(__name__)


class ValidatePlanUseCase:
    """Use case for validating plans."""

    def __init__(self) -> None:
        """Initialize the validate plan use case."""

        self._validation_rules: dict[str, Any] = self._initialize_validation_rules()

    def _initialize_validation_rules(self) -> dict[str, Any]:
        """Initialize validation rules.





        Returns:


            Dictionary of validation rules.


        """

        return {
            "required_fields": ["id", "name", "steps"],
            "min_steps": 1,
            "max_steps": 100,
            "max_depth": 10,
            "required_step_fields": ["type", "action"],
            "valid_step_types": [
                "action",
                "condition",
                "loop",
                "parallel",
                "sequential",
            ],
            "max_execution_time_hours": 24,
            "max_resource_usage_percent": 100,
        }

    def validate_plan(
        self,
        plan_data: dict[str, Any],
        validation_level: str = "standard",
    ) -> dict[str, Any]:
        """Validate a plan according to specified validation level.





        Args:


            plan_data: Plan data to validate.


            validation_level: Level of validation (basic, standard, strict).





        Returns:


            Validation result with errors and warnings.


        """

        logger.info(f"Validating plan with {validation_level} validation level")

        try:
            # Perform validation based on level

            if validation_level in ["basic", "standard", "strict"]:
                self._validate_structure(plan_data, validation_result)

            if validation_level in ["standard", "strict"]:
                self._validate_semantics(plan_data, validation_result)

                self._validate_dependencies(plan_data, validation_result)

            if validation_level == "strict":
                self._validate_performance(plan_data, validation_result)

                self._validate_security(plan_data, validation_result)

            # Calculate overall validity

            validation_result["is_valid"] = len(validation_result["errors"]) == 0

            logger.info(
                f"Plan validation completed: {'valid' if validation_result['is_valid'] else 'invalid'}"
            )

        except Exception as e:
            validation_result["is_valid"] = False

            validation_result["errors"].append(f"Validation error: {e!s}")

            logger.error(f"Plan validation failed: {e}")

        return validation_result

    def _validate_structure(
        self,
        plan_data: dict[str, Any],
        validation_result: dict[str, Any],
    ) -> None:
        """Validate plan structure.





        Args:


            plan_data: Plan data to validate.


            validation_result: Result object to update.


        """

        # Check required fields

        for field in self._validation_rules["required_fields"]:
            if field not in plan_data:
                validation_result["errors"].append(f"Missing required field: {field}")

        # Validate steps

        steps = plan_data.get("steps", [])

        if not isinstance(steps, list):
            validation_result["errors"].append("Steps must be a list")

            return

        if len(steps) < self._validation_rules["min_steps"]:
            validation_result["errors"].append(
                f"Plan must have at least {self._validation_rules['min_steps']} step(s)"
            )

        if len(steps) > self._validation_rules["max_steps"]:
            validation_result["errors"].append(
                f"Plan cannot have more than {self._validation_rules['max_steps']} steps"
            )

        # Validate individual steps

        for i, step in enumerate(steps):
            self._validate_step_structure(step, i, validation_result)

    def _validate_step_structure(
        self,
        step: dict[str, Any],
        step_index: int,
        validation_result: dict[str, Any],
    ) -> None:
        """Validate individual step structure.





        Args:


            step: Step data to validate.


            step_index: Index of the step.


            validation_result: Result object to update.


        """

        if not isinstance(step, dict):
            validation_result["errors"].append(
                f"Step {step_index} must be a dictionary"
            )

            return

        # Check required step fields

        for field in self._validation_rules["required_step_fields"]:
            if field not in step:
                validation_result["errors"].append(
                    f"Step {step_index} missing required field: {field}"
                )

        # Validate step type

        step_type = step.get("type")

        if step_type not in self._validation_rules["valid_step_types"]:
            validation_result["errors"].append(
                f"Step {step_index} has invalid type '{step_type}'. "
                f"Valid types: {self._validation_rules['valid_step_types']}"
            )

    def _validate_semantics(
        self,
        plan_data: dict[str, Any],
        validation_result: dict[str, Any],
    ) -> None:
        """Validate plan semantics and logic.





        Args:


            plan_data: Plan data to validate.


            validation_result: Result object to update.


        """

        steps = plan_data.get("steps", [])

        # Check for logical consistency

        for i, step in enumerate(steps):
            step_type = step.get("type")

            self._validate_step_semantics(step, step_type, i, validation_result)

    def _validate_step_semantics(
        self,
        step: dict[str, Any],
        step_type: str,
        step_index: int,
        validation_result: dict[str, Any],
    ) -> None:
        """Validate semantics for a single step.





        Args:


            step: Step data to validate.


            step_type: Type of the step.


            step_index: Index of the step.


            validation_result: Result object to update.


        """

        if step_type == "condition":
            self._validate_conditional_step(step, step_index, validation_result)

        elif step_type == "loop":
            self._validate_loop_step(step, step_index, validation_result)

        elif step_type == "parallel":
            self._validate_parallel_step(step, step_index, validation_result)

    def _validate_conditional_step(
        self,
        step: dict[str, Any],
        step_index: int,
        validation_result: dict[str, Any],
    ) -> None:
        """Validate conditional step semantics."""

        if "condition" not in step:
            validation_result["errors"].append(
                f"Conditional step {step_index} missing condition"
            )

        if "then_steps" not in step and "else_steps" not in step:
            validation_result["warnings"].append(
                f"Conditional step {step_index} has no then/else branches"
            )

    def _validate_loop_step(
        self,
        step: dict[str, Any],
        step_index: int,
        validation_result: dict[str, Any],
    ) -> None:
        """Validate loop step semantics."""

        if "loop_condition" not in step and "iterations" not in step:
            validation_result["errors"].append(
                f"Loop step {step_index} missing loop condition or iterations"
            )

    def _validate_parallel_step(
        self,
        step: dict[str, Any],
        step_index: int,
        validation_result: dict[str, Any],
    ) -> None:
        """Validate parallel step semantics."""

        if "parallel_steps" not in step:
            validation_result["errors"].append(
                f"Parallel step {step_index} missing parallel_steps"
            )

        else:
            parallel_steps = step["parallel_steps"]

            if not isinstance(parallel_steps, list) or len(parallel_steps) < 2:
                validation_result["warnings"].append(
                    f"Parallel step {step_index} should have at least 2 parallel branches"
                )

    def _validate_dependencies(
        self,
        plan_data: dict[str, Any],
        validation_result: dict[str, Any],
    ) -> None:
        """Validate step dependencies.





        Args:


            plan_data: Plan data to validate.


            validation_result: Result object to update.


        """

        steps = plan_data.get("steps", [])

        step_ids = {step.get("id") for step in steps if step.get("id")}

        # Check dependency references

        for i, step in enumerate(steps):
            dependencies = step.get("depends_on", [])

            if dependencies:
                for dep in dependencies:
                    if dep not in step_ids:
                        validation_result["errors"].append(
                            f"Step {i} depends on non-existent step: {dep}"
                        )

        # Check for circular dependencies

        if self._has_circular_dependencies(steps):
            validation_result["errors"].append("Plan contains circular dependencies")

    def _has_circular_dependencies(self, steps: list[dict[str, Any]]) -> bool:
        """Check if plan has circular dependencies.





        Args:


            steps: List of plan steps.





        Returns:


            True if circular dependencies exist.


        """

        # Build dependency graph

        dependencies = {}

        for step in steps:
            step_id = step.get("id")

            if step_id:
                dependencies[step_id] = step.get("depends_on", [])

        # Check for cycles using DFS

        visited = set()

        rec_stack = set()

        def has_cycle(node: str) -> bool:
            if node in rec_stack:
                return True

            if node in visited:
                return False

            visited.add(node)

            rec_stack.add(node)

            for neighbor in dependencies.get(node, []):
                if has_cycle(neighbor):
                    return True

            rec_stack.remove(node)

            return False

        for node in dependencies:
            if has_cycle(node):
                return True

        return False

    def _validate_performance(
        self,
        plan_data: dict[str, Any],
        validation_result: dict[str, Any],
    ) -> None:
        """Validate performance characteristics.





        Args:


            plan_data: Plan data to validate.


            validation_result: Result object to update.


        """

        # Estimate execution time

        estimated_time = self._estimate_execution_time(plan_data)

        max_time = (
            self._validation_rules["max_execution_time_hours"] * 3600
        )  # Convert to seconds

        if estimated_time > max_time:
            validation_result["warnings"].append(
                f"Estimated execution time ({estimated_time / 3600:.1f}h) exceeds maximum ({max_time / 3600}h)"
            )

        # Estimate resource usage

        estimated_resources = self._estimate_resource_usage(plan_data)

        max_resources = self._validation_rules["max_resource_usage_percent"]

        if estimated_resources > max_resources:
            validation_result["warnings"].append(
                f"Estimated resource usage ({estimated_resources}%) exceeds maximum ({max_resources}%)"
            )

        validation_result["metrics"]["estimated_execution_time_seconds"] = (
            estimated_time
        )

        validation_result["metrics"]["estimated_resource_usage_percent"] = (
            estimated_resources
        )

    def _estimate_execution_time(self, plan_data: dict[str, Any]) -> float:
        """Estimate plan execution time in seconds.





        Args:


            plan_data: Plan data.





        Returns:


            Estimated execution time in seconds.


        """

        steps = plan_data.get("steps", [])

        total_time = 0.0

        for step in steps:
            step_type = step.get("type", "action")

            # Base time estimates by step type

            if step_type == "action":
                total_time += 10.0  # 10 seconds per action

            elif step_type == "condition":
                total_time += 1.0  # 1 second for condition evaluation

            elif step_type == "loop":
                iterations = step.get("iterations", 5)

                loop_steps = step.get("loop_steps", [])

                total_time += iterations * len(loop_steps) * 5.0

            elif step_type == "parallel":
                parallel_steps = step.get("parallel_steps", [])

                # Parallel steps run concurrently, so take max time

                parallel_time = max([5.0 for _ in parallel_steps], default=0.0)

                total_time += parallel_time

        return total_time

    def _estimate_resource_usage(self, plan_data: dict[str, Any]) -> float:
        """Estimate resource usage percentage.





        Args:


            plan_data: Plan data.





        Returns:


            Estimated resource usage as percentage.


        """

        steps = plan_data.get("steps", [])

        max_parallel = 1

        total_complexity = 0

        for step in steps:
            step_type = step.get("type", "action")

            if step_type == "parallel":
                parallel_steps = step.get("parallel_steps", [])

                max_parallel = max(max_parallel, len(parallel_steps))

            # Add complexity score

            complexity = step.get("complexity", 1)

            total_complexity += complexity

        # Estimate based on parallelism and complexity

        base_usage = min(total_complexity * 2, 80)  # Base usage

        parallel_multiplier = min(max_parallel * 10, 50)  # Parallel overhead

        return min(base_usage + parallel_multiplier, 100)

    def _validate_security(
        self,
        plan_data: dict[str, Any],
        validation_result: dict[str, Any],
    ) -> None:
        """Validate security aspects.





        Args:


            plan_data: Plan data to validate.


            validation_result: Result object to update.


        """

        steps = plan_data.get("steps", [])

        # Check for potential security issues

        for i, step in enumerate(steps):
            action = step.get("action", "")

            # Check for dangerous operations

            if any(
                keyword in action.lower() for keyword in ["delete", "remove", "destroy"]
            ):
                validation_result["warnings"].append(
                    f"Step {i} contains potentially dangerous operation: {action}"
                )

            # Check for external network access

            if any(
                keyword in action.lower() for keyword in ["http", "https", "ftp", "ssh"]
            ):
                validation_result["suggestions"].append(
                    f"Step {i} involves network access - ensure proper security measures"
                )

            # Check for file system operations

            if any(
                keyword in action.lower() for keyword in ["file", "directory", "path"]
            ):
                validation_result["suggestions"].append(
                    f"Step {i} involves file system operations - validate permissions"
                )

    def validate_step(self, step_data: dict[str, Any]) -> dict[str, Any]:
        """Validate a single step.





        Args:


            step_data: Step data to validate.





        Returns:


            Validation result for the step.


        """

        _ = {
            "is_valid": True,
            "errors": [],
            "warnings": [],
        }

        self._validate_step_structure(step_data, 0, result)

        result["is_valid"] = len(result["errors"]) == 0

        return result

    def get_validation_rules(self) -> dict[str, Any]:
        """Get current validation rules.





        Returns:


            Dictionary of validation rules.


        """

        return self._validation_rules.copy()

    def update_validation_rules(self, new_rules: dict[str, Any]) -> None:
        """Update validation rules.





        Args:


            new_rules: New validation rules to apply.


        """

        self._validation_rules.update(new_rules)

        logger.info("Updated validation rules")
