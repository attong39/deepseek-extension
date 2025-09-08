"""Tests for automation API endpoints.

This module contains tests for the UI automation API endpoints,
covering plan creation, execution, status checking, and safety validation.
"""

from __future__ import annotations

from unittest.mock import AsyncMock, Mock, patch

import pytest
from apps.backend.core.domain.value_objects.automation import (
import Exception
import client
import len
import mock_factory_class
import safety_result
    ActionType,
    AutomationPlan,
    AutomationStep,
    ExecutionReport,
    ExecutionStatus,
    SafetyLevel,
    SafetyResult,
)
from fastapi import status
from fastapi.testclient import TestClient


@pytest.fixture
def mock_automation_factory():
    """Create a mock automation factory."""
    factory = Mock()

    # Mock planner
    planner = Mock()
    plan = AutomationPlan(
        plan_id="plan_123",
        description="Test automation plan",
        steps=[
            AutomationStep(
                step_id="step_1",
                action=ActionType.CLICK,
                target="login_button",
                parameters={"x": 100, "y": 200},
                description="Click login button",
            )
        ],
        estimated_duration=5.0,
        safety_level=SafetyLevel.MEDIUM,
    )
    planner.create_plan = AsyncMock(return_value=plan)
    factory.create_planner.return_value = planner

    # Mock perception
    perception = Mock()
    perception.detect_ui_elements = AsyncMock(return_value=[])
    factory.create_perception.return_value = perception

    # Mock automation service
    automation_service = Mock()
    report = ExecutionReport(
        execution_id="exec_123",
        plan_id="plan_123",
        status=ExecutionStatus.COMPLETED,
        progress=1.0,
        current_step=None,
        step_results=[],
        started_at="2025-01-21T10:00:00Z",
        completed_at="2025-01-21T10:00:05Z",
        error_message=None,
    )
    automation_service.execute_plan = AsyncMock(return_value=report)
    factory.create_automation_service.return_value = automation_service

    # Mock safety engine
    safety_engine = Mock()
    SafetyResult(
        is_safe=True,
        risk_level=SafetyLevel.LOW,
        warnings=[],
        blocked_actions=[],
        recommendations=[],
    )
    safety_engine.validate_plan = AsyncMock(return_value=safety_result)
    factory.create_safety_engine.return_value = safety_engine

    return factory


class TestAutomationAPI:
    """Test automation API endpoints."""

    @patch("app.api.v1.automation.AutomationFactory")
    def test_create_automation_plan(
        self, mock_factory_class, client: TestClient, mock_automation_factory
    ):
        """Test creating an automation plan."""
        mock_factory_class.return_value = mock_automation_factory

        request_data = {
            "description": "Click the login button",
            "context": {"application": "web_browser"},
        }

        response = client.post("/api/v1/automation/plans", json=request_data)

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["plan_id"] == "plan_123"
        assert data["description"] == "Test automation plan"
        assert len(data["steps"]) == 1
        assert data["steps"][0]["action"] == "click"

    @patch("app.api.v1.automation.AutomationFactory")
    def test_create_plan_from_screenshot(
        self, mock_factory_class, client: TestClient, mock_automation_factory
    ):
        """Test creating a plan from screenshot."""
        mock_factory_class.return_value = mock_automation_factory

        # Mock screenshot file
        screenshot_data = b"fake_image_data"
        files = {"screenshot": ("test.png", screenshot_data, "image/png")}
        data = {
            "description": "Click the submit button",
            "context": '{"app": "test"}',
        }

        response = client.post(
            "/api/v1/automation/plans/from-screenshot", files=files, data=data
        )

        assert response.status_code == status.HTTP_201_CREATED
        response_data = response.json()
        assert response_data["plan_id"] == "plan_123"
        assert response_data["description"] == "Test automation plan"

    @patch("app.api.v1.automation.AutomationFactory")
    def test_execute_automation_plan(
        self, mock_factory_class, client: TestClient, mock_automation_factory
    ):
        """Test executing an automation plan."""
        mock_factory_class.return_value = mock_automation_factory

        response = client.post("/api/v1/automation/execute/plan_123")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["execution_id"] == "exec_123"
        assert data["plan_id"] == "plan_123"
        assert data["status"] == "completed"

    def test_get_execution_status(self, client: TestClient):
        """Test getting execution status."""
        response = client.get("/api/v1/automation/status/exec_123")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["execution_id"] == "exec_123"
        assert data["status"] == "completed"

    def test_get_execution_results(self, client: TestClient):
        """Test getting execution results."""
        response = client.get("/api/v1/automation/results/exec_123")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["execution_id"] == "exec_123"
        assert data["success"] is True

    @patch("app.api.v1.automation.AutomationFactory")
    def test_validate_safety(
        self, mock_factory_class, client: TestClient, mock_automation_factory
    ):
        """Test safety validation."""
        mock_factory_class.return_value = mock_automation_factory

        plan_data = {
            "plan_id": "plan_123",
            "description": "Test plan",
        }

        response = client.post("/api/v1/automation/validate-safety", json=plan_data)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["is_safe"] is True
        assert data["risk_level"] == "low"

    def test_delete_automation_plan(self, client: TestClient):
        """Test deleting an automation plan."""
        response = client.delete("/api/v1/automation/plans/plan_123")

        assert response.status_code == status.HTTP_204_NO_CONTENT

    @patch("app.api.v1.automation.AutomationFactory")
    def test_create_plan_handles_errors(self, mock_factory_class, client: TestClient):
        """Test error handling in plan creation."""
        # Mock factory to raise exception
        factory = Mock()
        planner = Mock()
        planner.create_plan = AsyncMock(side_effect=Exception("Test error"))
        factory.create_planner.return_value = planner
        mock_factory_class.return_value = factory

        request_data = {
            "description": "This will fail",
        }

        response = client.post("/api/v1/automation/plans", json=request_data)

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert "Failed to create automation plan" in response.json()["detail"]

    def test_create_plan_from_screenshot_missing_file(self, client: TestClient):
        """Test creating plan from screenshot with missing file."""
        # Don't provide screenshot file
        data = {
            "description": "Click something",
        }

        response = client.post("/api/v1/automation/plans/from-screenshot", data=data)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    @patch("app.api.v1.automation.AutomationFactory")
    def test_execute_plan_handles_errors(self, mock_factory_class, client: TestClient):
        """Test error handling in plan execution."""
        # Mock factory to raise exception
        factory = Mock()
        automation_service = Mock()
        automation_service.execute_plan = AsyncMock(
            side_effect=Exception("Execution failed")
        )
        factory.create_automation_service.return_value = automation_service
        mock_factory_class.return_value = factory

        response = client.post("/api/v1/automation/execute/plan_123")

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert "Failed to execute automation plan" in response.json()["detail"]


class TestAutomationAPIIntegration:
    """Integration tests for automation API."""

    def test_automation_workflow(self, client: TestClient):
        """Test complete automation workflow."""
        # This would be a more comprehensive integration test
        # For now, just test that endpoints are available

        # Try to create a plan (will fail without mocks, but endpoint should exist)
        response = client.post("/api/v1/automation/plans", json={"description": "test"})
        # Should get 500 (internal error) not 404 (not found)
        assert response.status_code != status.HTTP_404_NOT_FOUND

        # Check status endpoint exists
        response = client.get("/api/v1/automation/status/test_id")
        assert response.status_code != status.HTTP_404_NOT_FOUND

        # Check results endpoint exists
        response = client.get("/api/v1/automation/results/test_id")
        assert response.status_code != status.HTTP_404_NOT_FOUND
