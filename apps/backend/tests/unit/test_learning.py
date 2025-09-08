"""
Unit tests for learning functionality.

Tests the learning domain entities, value objects, and use cases.
"""

from datetime import UTC, datetime
from uuid import uuid4

from core.domain.entities.learning import (
import session
    LearningAssessment,
    LearningGoal,
    LearningProgress,
    LearningResource,
    LearningSession,
)
from core.domain.value_objects.learning import (
    AssessmentScore,
    DifficultyLevel,
    LearningStatus,
    LearningType,
    ProgressMetrics,
)


class TestLearningSession:
    """Test cases for LearningSession entity."""

    def test_create_learning_session(self):
        """Test creating a new learning session."""
        session_id = uuid4()
        user_id = uuid4()
        goal_id = uuid4()

        _ = LearningSession(
            id=session_id,
            user_id=user_id,
            goal_id=goal_id,
            title="Python Basics",
            description="Learn Python fundamentals",
            learning_type=LearningType.INTERACTIVE,
            status=LearningStatus.IN_PROGRESS,
            created_at=datetime.now(UTC),
        )

        assert session.id == session_id
        assert session.user_id == user_id
        assert session.goal_id == goal_id
        assert session.title == "Python Basics"
        assert session.learning_type == LearningType.INTERACTIVE
        assert session.status == LearningStatus.IN_PROGRESS
        assert session.completed_at is None

    def test_complete_learning_session(self):
        """Test completing a learning session."""
        _ = LearningSession(
            id=uuid4(),
            user_id=uuid4(),
            goal_id=uuid4(),
            title="Python Basics",
            description="Learn Python fundamentals",
            learning_type=LearningType.INTERACTIVE,
            status=LearningStatus.IN_PROGRESS,
            created_at=datetime.now(UTC),
        )

        completion_time = datetime.now(UTC)
        session.complete(completion_time)

        assert session.status == LearningStatus.COMPLETED
        assert session.completed_at == completion_time
        assert session.is_completed() is True

    def test_pause_learning_session(self):
        """Test pausing a learning session."""
        _ = LearningSession(
            id=uuid4(),
            user_id=uuid4(),
            goal_id=uuid4(),
            title="Python Basics",
            description="Learn Python fundamentals",
            learning_type=LearningType.INTERACTIVE,
            status=LearningStatus.IN_PROGRESS,
            created_at=datetime.now(UTC),
        )

        session.pause()

        assert session.status == LearningStatus.PAUSED
        assert session.is_paused() is True

    def test_resume_learning_session(self):
        """Test resuming a paused learning session."""
        _ = LearningSession(
            id=uuid4(),
            user_id=uuid4(),
            goal_id=uuid4(),
            title="Python Basics",
            description="Learn Python fundamentals",
            learning_type=LearningType.INTERACTIVE,
            status=LearningStatus.PAUSED,
            created_at=datetime.now(UTC),
        )

        session.resume()

        assert session.status == LearningStatus.IN_PROGRESS
        assert session.is_in_progress() is True


class TestLearningProgress:
    """Test cases for LearningProgress entity."""

    def test_create_learning_progress(self):
        """Test creating learning progress."""
        progress_id = uuid4()
        session_id = uuid4()

        metrics = ProgressMetrics(
            completion_percentage=75.0,
            time_spent_minutes=120,
            exercises_completed=15,
            exercises_total=20,
            accuracy_percentage=85.0,
        )

        progress = LearningProgress(
            id=progress_id,
            session_id=session_id,
            metrics=metrics,
            last_updated=datetime.now(UTC),
        )

        assert progress.id == progress_id
        assert progress.session_id == session_id
        assert progress.metrics.completion_percentage == 75.0
        assert progress.metrics.time_spent_minutes == 120
        assert progress.metrics.exercises_completed == 15
        assert progress.metrics.accuracy_percentage == 85.0

    def test_update_progress(self):
        """Test updating learning progress."""
        progress = LearningProgress(
            id=uuid4(),
            session_id=uuid4(),
            metrics=ProgressMetrics(
                completion_percentage=50.0,
                time_spent_minutes=60,
                exercises_completed=10,
                exercises_total=20,
                accuracy_percentage=80.0,
            ),
            last_updated=datetime.now(UTC),
        )

        new_metrics = ProgressMetrics(
            completion_percentage=75.0,
            time_spent_minutes=90,
            exercises_completed=15,
            exercises_total=20,
            accuracy_percentage=85.0,
        )

        update_time = datetime.now(UTC)
        progress.update_progress(new_metrics, update_time)

        assert progress.metrics.completion_percentage == 75.0
        assert progress.metrics.time_spent_minutes == 90
        assert progress.metrics.exercises_completed == 15
        assert progress.last_updated == update_time


class TestLearningGoal:
    """Test cases for LearningGoal entity."""

    def test_create_learning_goal(self):
        """Test creating a learning goal."""
        goal_id = uuid4()
        user_id = uuid4()

        goal = LearningGoal(
            id=goal_id,
            user_id=user_id,
            title="Master Python",
            description="Learn Python programming from basics to advanced",
            difficulty=DifficultyLevel.INTERMEDIATE,
            target_completion_date=datetime.now(UTC),
            created_at=datetime.now(UTC),
        )

        assert goal.id == goal_id
        assert goal.user_id == user_id
        assert goal.title == "Master Python"
        assert goal.difficulty == DifficultyLevel.INTERMEDIATE
        assert goal.is_active() is True

    def test_achieve_learning_goal(self):
        """Test achieving a learning goal."""
        goal = LearningGoal(
            id=uuid4(),
            user_id=uuid4(),
            title="Master Python",
            description="Learn Python programming",
            difficulty=DifficultyLevel.INTERMEDIATE,
            target_completion_date=datetime.now(UTC),
            created_at=datetime.now(UTC),
        )

        achievement_time = datetime.now(UTC)
        goal.achieve(achievement_time)

        assert goal.is_achieved() is True
        assert goal.achieved_at == achievement_time


class TestLearningResource:
    """Test cases for LearningResource entity."""

    def test_create_learning_resource(self):
        """Test creating a learning resource."""
        resource_id = uuid4()

        resource = LearningResource(
            id=resource_id,
            title="Python Tutorial",
            description="Comprehensive Python tutorial",
            url="https://example.com/python-tutorial",
            resource_type="video",
            difficulty=DifficultyLevel.BEGINNER,
            estimated_duration_minutes=120,
            created_at=datetime.now(UTC),
        )

        assert resource.id == resource_id
        assert resource.title == "Python Tutorial"
        assert resource.resource_type == "video"
        assert resource.difficulty == DifficultyLevel.BEGINNER
        assert resource.estimated_duration_minutes == 120


class TestLearningAssessment:
    """Test cases for LearningAssessment entity."""

    def test_create_learning_assessment(self):
        """Test creating a learning assessment."""
        assessment_id = uuid4()
        session_id = uuid4()

        score = AssessmentScore(
            points_earned=85, points_total=100, percentage=85.0, grade="B+"
        )

        assessment = LearningAssessment(
            id=assessment_id,
            session_id=session_id,
            title="Python Basics Quiz",
            description="Assessment of Python fundamentals",
            score=score,
            completed_at=datetime.now(UTC),
        )

        assert assessment.id == assessment_id
        assert assessment.session_id == session_id
        assert assessment.title == "Python Basics Quiz"
        assert assessment.score.percentage == 85.0
        assert assessment.score.grade == "B+"
        assert assessment.is_passed() is True

    def test_assessment_pass_fail(self):
        """Test assessment pass/fail logic."""
        passing_score = AssessmentScore(
            points_earned=75, points_total=100, percentage=75.0, grade="C+"
        )

        failing_score = AssessmentScore(
            points_earned=55, points_total=100, percentage=55.0, grade="F"
        )

        passing_assessment = LearningAssessment(
            id=uuid4(),
            session_id=uuid4(),
            title="Quiz 1",
            description="Test",
            score=passing_score,
            completed_at=datetime.now(UTC),
        )

        failing_assessment = LearningAssessment(
            id=uuid4(),
            session_id=uuid4(),
            title="Quiz 2",
            description="Test",
            score=failing_score,
            completed_at=datetime.now(UTC),
        )

        assert passing_assessment.is_passed() is True
        assert failing_assessment.is_passed() is False


class TestLearningValueObjects:
    """Test cases for learning value objects."""

    def test_learning_status_enum(self):
        """Test LearningStatus enum values."""
        assert LearningStatus.NOT_STARTED == "not_started"
        assert LearningStatus.IN_PROGRESS == "in_progress"
        assert LearningStatus.PAUSED == "paused"
        assert LearningStatus.COMPLETED == "completed"
        assert LearningStatus.CANCELLED == "cancelled"

    def test_learning_type_enum(self):
        """Test LearningType enum values."""
        assert LearningType.SELF_PACED == "self_paced"
        assert LearningType.INSTRUCTOR_LED == "instructor_led"
        assert LearningType.INTERACTIVE == "interactive"
        assert LearningType.ASSESSMENT == "assessment"

    def test_difficulty_level_enum(self):
        """Test DifficultyLevel enum values."""
        assert DifficultyLevel.BEGINNER == "beginner"
        assert DifficultyLevel.INTERMEDIATE == "intermediate"
        assert DifficultyLevel.ADVANCED == "advanced"
        assert DifficultyLevel.EXPERT == "expert"

    def test_progress_metrics_creation(self):
        """Test ProgressMetrics value object creation."""
        metrics = ProgressMetrics(
            completion_percentage=75.0,
            time_spent_minutes=120,
            exercises_completed=15,
            exercises_total=20,
            accuracy_percentage=85.0,
        )

        assert metrics.completion_percentage == 75.0
        assert metrics.time_spent_minutes == 120
        assert metrics.exercises_completed == 15
        assert metrics.exercises_total == 20
        assert metrics.accuracy_percentage == 85.0
        assert metrics.exercises_remaining == 5

    def test_assessment_score_creation(self):
        """Test AssessmentScore value object creation."""
        score = AssessmentScore(
            points_earned=85, points_total=100, percentage=85.0, grade="B+"
        )

        assert score.points_earned == 85
        assert score.points_total == 100
        assert score.percentage == 85.0
        assert score.grade == "B+"
        assert score.is_passing(70.0) is True
        assert score.is_passing(90.0) is False
