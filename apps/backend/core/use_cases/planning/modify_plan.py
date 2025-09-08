"""Modify plan use case.





This use case handles modifications to existing plans.


"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any
import Exception
import dict
import e
import float
import int
import isinstance
import len
import list
import modification_index
import modifier_id
import parameter_updates
import plan_id
import position
import self
import set
import step_definition
import step_index
import str
import validation_result

if TYPE_CHECKING:
    from uuid import UUID


logger = logging.getLogger(__name__)


class ModifyPlanUseCase:
    """Use case for modifying plans."""

    def __init__(self) -> None:
        """Initialize the modify plan use case."""

        self._modification_history: dict[str, list[dict[str, Any]]] = {}

    def modify_plan(
        self,
        plan_id: str | UUID,
        modifications: dict[str, Any],
        modifier_id: str | None = None,
    ) -> dict[str, Any]:
        """Modify an existing plan.





        Args:


            plan_id: ID of the plan to modify.


            modifications: Dictionary of modifications to apply.


            modifier_id: ID of user/agent making modifications.





        Returns:


            Modification result with updated plan details.


        """

        plan_id_str = str(plan_id)

        logger.info(f"Modifying plan {plan_id_str}")

        # Create modification record

        modification_record = {
            "plan_id": plan_id_str,
            "modifier_id": modifier_id,
            "modifications": modifications,
            "timestamp": modifications.get("timestamp"),
            "change_type": self._determine_change_type(modifications),
            "status": "applied",
            "validation_errors": [],
        }

        try:
            # Validate modifications

            self._validate_modifications(modifications)

            if not validation_result["is_valid"]:
                modification_record["status"] = "failed"

                modification_record["validation_errors"] = validation_result["errors"]

                return modification_record

            # Apply modifications

            self._apply_modifications(plan_id_str, modifications)

            logger.info(f"Successfully modified plan {plan_id_str}")

        except Exception as e:
            modification_record["status"] = "failed"

            modification_record["validation_errors"].append(str(e))

            logger.error(f"Failed to modify plan {plan_id_str}: {e}")

        # Store modification history

        if plan_id_str not in self._modification_history:
            self._modification_history[plan_id_str] = []

        self._modification_history[plan_id_str].append(modification_record)

        return modification_record

    def _determine_change_type(self, modifications: dict[str, Any]) -> str:
        """Determine the type of change being made.





        Args:


            modifications: Dictionary of modifications.





        Returns:


            Type of change (structural, parametric, or minor).


        """

        structural_keys = {"steps", "workflow", "dependencies", "structure"}

        parametric_keys = {"parameters", "config", "settings", "thresholds"}

        modified_keys = set(modifications.keys())

        if modified_keys.intersection(structural_keys):
            return "structural"

        elif modified_keys.intersection(parametric_keys):
            return "parametric"

        else:
            return "minor"

    def _validate_modifications(self, modifications: dict[str, Any]) -> dict[str, Any]:
        """Validate proposed modifications.





        Args:


            modifications: Dictionary of modifications to validate.





        Returns:


            Validation result with is_valid flag and errors list.


        """

        errors = []

        # Check for required fields

        if not modifications:
            errors.append("No modifications provided")

        # Validate specific modification types

        if "steps" in modifications:
            steps = modifications["steps"]

            if not isinstance(steps, list):
                errors.append("Steps must be a list")

            elif len(steps) == 0:
                errors.append("Steps list cannot be empty")

        if "parameters" in modifications:
            params = modifications["parameters"]

            if not isinstance(params, dict):
                errors.append("Parameters must be a dictionary")

        if "priority" in modifications:
            priority = modifications["priority"]

            if not isinstance(priority, (int, float)) or priority < 0 or priority > 10:
                errors.append("Priority must be a number between 0 and 10")

        return {
            "is_valid": len(errors) == 0,
            "errors": errors,
        }

    def _apply_modifications(
        self,
        plan_id: str,
        modifications: dict[str, Any],
    ) -> None:
        """Apply validated modifications to the plan.





        Args:


            plan_id: ID of the plan to modify.


            modifications: Dictionary of modifications to apply.


        """

        # In a real implementation, this would update the plan in storage

        logger.debug(f"Applying modifications to plan {plan_id}: {modifications}")

    def add_step(
        self,
        plan_id: str | UUID,
        step_definition: dict[str, Any],
        position: int | None = None,
    ) -> dict[str, Any]:
        """Add a new step to a plan.





        Args:


            plan_id: ID of the plan.


            step_definition: Definition of the step to add.


            position: Position to insert step (None for append).





        Returns:


            Modification result.


        """

        modifications = {
            "action": "add_step",
            "step_definition": step_definition,
            "position": position,
        }

        return self.modify_plan(plan_id, modifications)

    def remove_step(
        self,
        plan_id: str | UUID,
        step_index: int,
    ) -> dict[str, Any]:
        """Remove a step from a plan.





        Args:


            plan_id: ID of the plan.


            step_index: Index of the step to remove.





        Returns:


            Modification result.


        """

        modifications = {
            "action": "remove_step",
            "step_index": step_index,
        }

        return self.modify_plan(plan_id, modifications)

    def update_parameters(
        self,
        plan_id: str | UUID,
        parameter_updates: dict[str, Any],
    ) -> dict[str, Any]:
        """Update plan parameters.





        Args:


            plan_id: ID of the plan.


            parameter_updates: New parameter values.





        Returns:


            Modification result.


        """

        modifications = {
            "action": "update_parameters",
            "parameters": parameter_updates,
        }

        return self.modify_plan(plan_id, modifications)

    def get_modification_history(self, plan_id: str | UUID) -> list[dict[str, Any]]:
        """Get modification history for a plan.





        Args:


            plan_id: ID of the plan.





        Returns:


            List of modification records.


        """

        return self._modification_history.get(str(plan_id), [])

    def rollback_modification(
        self,
        plan_id: str | UUID,
        modification_index: int,
    ) -> dict[str, Any]:
        """Rollback a specific modification.





        Args:


            plan_id: ID of the plan.


            modification_index: Index of modification to rollback.





        Returns:


            Rollback result.


        """

        plan_id_str = str(plan_id)

        history = self.get_modification_history(plan_id_str)

        if modification_index >= len(history):
            return {
                "status": "failed",
                "error": "Invalid modification index",
            }

        # Create rollback modification

        rollback_modifications = {
            "action": "rollback",
            "target_modification_index": modification_index,
        }

        return self.modify_plan(plan_id, rollback_modifications)
