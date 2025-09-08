"""Tests for Self-Improvement Package v2."""

import tempfile
from pathlib import Path

import pytest
from apps.backend.core.self_improvement import (
    AutoUpdater,
    AutoUpdaterV2,
    FeatureContext,
    FeatureEngine,
    FeatureFlag,
    FeatureState,
    FileChange,
    ImprovementGoal,
    OperationType,
    Patch,
    PercentageRule,
    QualityGateSpec,
    TargetingRule,
    feature_guard,
)
from apps.backend.core.self_improvement.auto_updater import (
    AsyncShellRunner,
    LocalFSRepoAdapter,
)
from apps.backend.core.self_improvement.auto_updater_v2 import Policy


class TestAutoUpdaterV1:
    """Test AutoUpdater (v1) với patch system."""
import ValueError
import abs
import enabled
import f
import i
import len
import range
import result
import self
import sum

    def setup_method(self):
        self.temp_dir = tempfile.mkdtemp()
        self.repo = LocalFSRepoAdapter(self.temp_dir)
        self.runner = AsyncShellRunner()
        self.updater = AutoUpdater(self.repo, self.runner)

    def test_file_operations(self):
        """Test basic file operations."""
        # Test write and read
        self.repo.write_text("test.txt", "Hello World")
        content = self.repo.read_text("test.txt")
        assert content == "Hello World"

        # Test exists
        assert self.repo.exists("test.txt") is True
        assert self.repo.exists("nonexistent.txt") is False

        # Test delete
        self.repo.delete("test.txt")
        assert self.repo.exists("test.txt") is False

    def test_patch_creation(self):
        """Test patch model creation."""
        changes = [
            FileChange(op=OperationType.ADD, path="new_file.py", content="# New file"),
            FileChange(
                op=OperationType.UPDATE, path="existing.py", content="# Updated"
            ),
            FileChange(op=OperationType.DELETE, path="old_file.py"),
        ]

        patch = Patch(title="Test patch", summary="Test changes", changes=changes)

        assert patch.title == "Test patch"
        assert len(patch.changes) == 3
        assert patch.created_at is not None

    def test_preview_generation(self):
        """Test diff preview generation."""
        # Setup existing file
        self.repo.write_text("sample.py", "def old_function():\n    pass\n")

        changes = [
            FileChange(
                op=OperationType.UPDATE,
                path="sample.py",
                content="def new_function():\n    return True\n",
            )
        ]

        patch = Patch(title="Update function", changes=changes)
        diffs = self.updater.preview(patch)

        assert "sample.py" in diffs
        assert "old_function" in diffs["sample.py"]
        assert "new_function" in diffs["sample.py"]

    @pytest.mark.skip(reason="Subprocess execution varies by platform")
    @pytest.mark.asyncio
    async def test_apply_patch_success(self):
        """Test successful patch application."""
        changes = [
            FileChange(op=OperationType.ADD, path="new.py", content="print('hello')")
        ]

        patch = Patch(title="Add new file", changes=changes)

        # Use minimal quality gates for testing (Windows compatible)
        qg = QualityGateSpec(commands=["dir"], timeout_s=10.0)

        _ = await self.updater.apply_patch(patch, qg)

        assert result.applied is True
        assert result.passed_quality_gates is True
        assert result.rolled_back is False
        assert len(result.gates) == 1
        assert result.gates[0].exit_code == 0

    @pytest.mark.asyncio
    async def test_apply_patch_rollback(self):
        """Test patch rollback on quality gate failure."""
        changes = [
            FileChange(op=OperationType.ADD, path="bad.py", content="invalid syntax")
        ]

        patch = Patch(title="Bad patch", changes=changes)

        # Use failing quality gate (Windows compatible)
        qg = QualityGateSpec(commands=["dir nonexistent_folder"], timeout_s=10.0)

        _ = await self.updater.apply_patch(patch, qg)

        assert result.applied is True
        assert result.passed_quality_gates is False
        assert result.rolled_back is True
        assert len(result.gates) == 1
        assert result.gates[0].exit_code == 1


class TestAutoUpdaterV2:
    """Test AutoUpdater v2 với orchestration."""

    def setup_method(self):
        self.temp_dir = tempfile.mkdtemp()
        self.repo = LocalFSRepoAdapter(self.temp_dir)
        self.runner = AsyncShellRunner()
        self.v1_updater = AutoUpdater(self.repo, self.runner)

        policy = Policy(
            max_changed_files=5, allow_globs=("*.py", "*.md"), deny_globs=("*.env",)
        )

        self.v2_updater = AutoUpdaterV2(
            self.v1_updater,
            policy=policy,
            history_path=Path(self.temp_dir) / "history.jsonl",
        )

    def test_policy_enforcement(self):
        """Test policy enforcement."""
        # Test file limit
        changes = [
            FileChange(op=OperationType.ADD, path=f"file{i}.py", content="")
            for i in range(10)  # Exceeds limit of 5
        ]

        patch = Patch(title="Too many files", changes=changes)

        with pytest.raises(ValueError, match="too many files"):
            self.v2_updater._enforce_policy(patch)

    def test_policy_deny_patterns(self):
        """Test deny pattern enforcement."""
        changes = [
            FileChange(op=OperationType.ADD, path=".env", content="SECRET=value")
        ]

        patch = Patch(title="Denied file", changes=changes)

        with pytest.raises(ValueError, match="denied by policy"):
            self.v2_updater._enforce_policy(patch)

    def test_policy_allow_patterns(self):
        """Test allow pattern enforcement."""
        changes = [
            FileChange(op=OperationType.ADD, path="script.sh", content="#!/bin/bash")
        ]

        patch = Patch(title="Unallowed file", changes=changes)

        with pytest.raises(ValueError, match="not allowed by policy"):
            self.v2_updater._enforce_policy(patch)

    def test_improvement_goal_model(self):
        """Test ImprovementGoal model."""
        goal = ImprovementGoal(
            title="Optimize performance",
            description="Improve API response times",
            metadata={"area": "performance", "target": "p95<100ms"},
        )

        assert goal.title == "Optimize performance"
        assert goal.metadata["area"] == "performance"


class TestFeatureEngine:
    """Test Feature Flag system."""

    def setup_method(self):
        self.engine = FeatureEngine()

    def test_feature_crud(self):
        """Test basic CRUD operations."""
        flag = FeatureFlag(
            name="test_feature", state=FeatureState.ON, description="Test feature"
        )

        # Create
        self.engine.upsert(flag)

        # Read
        retrieved = self.engine.get("test_feature")
        assert retrieved is not None
        assert retrieved.name == "test_feature"

        # Update
        flag.description = "Updated description"
        self.engine.upsert(flag)
        updated = self.engine.get("test_feature")
        assert updated is not None
        assert updated.description == "Updated description"

        # Delete
        self.engine.remove("test_feature")
        assert self.engine.get("test_feature") is None

    def test_feature_state_decisions(self):
        """Test feature state decision logic."""
        ctx = FeatureContext(user_id="user123", env="prod")

        # OFF state
        flag_off = FeatureFlag(name="feature_off", state=FeatureState.OFF)
        self.engine.upsert(flag_off)
        assert self.engine.decide("feature_off", ctx) is False

        # ON state
        flag_on = FeatureFlag(name="feature_on", state=FeatureState.ON)
        self.engine.upsert(flag_on)
        assert self.engine.decide("feature_on", ctx) is True

    def test_percentage_rule(self):
        """Test percentage-based rollout."""
        rule = PercentageRule(percentage=50.0, salt="test")

        # Test deterministic behavior
        user_key = "consistent_user"
        result1 = rule.hit(user_key)
        result2 = rule.hit(user_key)
        assert result1 == result2  # Should be deterministic

        # Test percentage distribution (rough check)
        hits = sum(1 for i in range(1000) if rule.hit(f"user{i}"))
        # Should be roughly 50% (allow 20% variance)
        assert 400 <= hits <= 600

    def test_targeting_rule(self):
        """Test user/org targeting."""
        rule = TargetingRule(
            allow_users={"user1", "user2"},
            deny_users={"banned_user"},
            allow_orgs={"org1"},
        )

        # Allowed user
        assert rule.allowed("user1", None) is True

        # Denied user (takes precedence)
        assert rule.allowed("banned_user", "org1") is False

        # User not in allow list
        assert rule.allowed("random_user", None) is False

        # Allowed org
        assert rule.allowed("any_user", "org1") is True

    def test_conditional_feature(self):
        """Test conditional feature with multiple rules."""
        percentage_rule = PercentageRule(percentage=100.0)  # Always hit
        targeting_rule = TargetingRule(allow_users={"allowed_user"})

        flag = FeatureFlag(
            name="conditional_feature",
            state=FeatureState.CONDITIONAL,
            percentage=percentage_rule,
            targeting=targeting_rule,
        )

        self.engine.upsert(flag)

        # Allowed user should get feature
        ctx_allowed = FeatureContext(user_id="allowed_user")
        assert self.engine.decide("conditional_feature", ctx_allowed) is True

        # Non-allowed user should not get feature
        ctx_denied = FeatureContext(user_id="other_user")
        assert self.engine.decide("conditional_feature", ctx_denied) is False

    def test_feature_guard(self):
        """Test feature guard context manager."""
        flag = FeatureFlag(name="guarded_feature", state=FeatureState.ON)
        self.engine.upsert(flag)

        ctx = FeatureContext(user_id="test_user")

        with feature_guard(self.engine, "guarded_feature", ctx) as enabled:
            assert enabled is True

        # Test with disabled feature
        flag.state = FeatureState.OFF
        self.engine.upsert(flag)

        with feature_guard(self.engine, "guarded_feature", ctx) as enabled:
            assert enabled is False

    def test_json_export_import(self):
        """Test JSON serialization."""
        flag = FeatureFlag(
            name="export_test",
            state=FeatureState.CONDITIONAL,
            percentage=PercentageRule(percentage=25.0),
            targeting=TargetingRule(allow_users={"user1"}),
            description="Test export",
        )

        self.engine.upsert(flag)

        # Export
        json_data = self.engine.export_json()
        assert "export_test" in json_data

        # Import to new engine
        new_engine = FeatureEngine()
        new_engine.import_json(json_data)

        # Verify import
        imported_flag = new_engine.get("export_test")
        assert imported_flag is not None
        assert imported_flag.name == "export_test"
        assert imported_flag.percentage is not None
        assert abs(imported_flag.percentage.percentage - 25.0) < 0.1


class TestSelfImprovementIntegration:
    """Integration tests across all components."""

    def setup_method(self):
        self.temp_dir = tempfile.mkdtemp()
        self.repo = LocalFSRepoAdapter(self.temp_dir)
        self.runner = AsyncShellRunner()
        self.v1_updater = AutoUpdater(self.repo, self.runner)
        self.v2_updater = AutoUpdaterV2(self.v1_updater)
        self.feature_engine = FeatureEngine()

    def test_feature_flag_controlled_updates(self):
        """Test updates controlled by feature flags."""
        # Setup feature flag for auto-updates
        flag = FeatureFlag(
            name="auto_updates_enabled",
            state=FeatureState.CONDITIONAL,
            percentage=PercentageRule(percentage=100.0),  # Always enabled for test
        )
        self.feature_engine.upsert(flag)

        ctx = FeatureContext(user_id="admin", env="staging")

        # Check if auto-updates are enabled
        auto_updates_enabled = self.feature_engine.decide("auto_updates_enabled", ctx)
        assert auto_updates_enabled is True

        # If enabled, proceed with update simulation
        if auto_updates_enabled:
            changes = [
                FileChange(
                    op=OperationType.ADD,
                    path="auto_generated.py",
                    content="# Auto-generated improvement",
                )
            ]

            patch = Patch(title="Auto improvement", changes=changes)
            diffs = self.v1_updater.preview(patch)

            assert "auto_generated.py" in diffs

    def test_comprehensive_system_status(self):
        """Test comprehensive system status."""
        # Add some feature flags
        self.feature_engine.upsert(FeatureFlag(name="feature1", state=FeatureState.ON))
        self.feature_engine.upsert(FeatureFlag(name="feature2", state=FeatureState.OFF))

        # Get status
        flags = self.feature_engine.list()

        system_status = {
            "auto_updater": "available",
            "feature_engine": "available",
            "active_features": len([f for f in flags if f.state != FeatureState.OFF]),
            "total_features": len(flags),
        }

        assert system_status["active_features"] == 1
        assert system_status["total_features"] == 2
