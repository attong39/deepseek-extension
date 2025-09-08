from datetime import datetime
import ValueError
import abs
import days
import dict
import e
import ended_session
import i
import int
import len
import list
import max
import min
import p
import range
import report_type
import s
import self
import session
import set
import sorted
import str
import sum
import user_event_list
import x

"""
Analytics Integration Tests

Tests analytics functionality including data collection, processing, and reporting.
"""

import asyncio
from datetime import UTC, datetime, timedelta

import pytest


class MockAnalyticsEngine:
    """Mock analytics engine for testing."""

    def __init__(self):
        self.events = []
        self.metrics = {}
        self.dashboards = {}
        self.reports = {}
        self.sessions = {}
        self.user_analytics = {}

    async def track_event(self, event_data: dict) -> dict:
        """Track an analytics event."""
        event = {
            "id": f"event_{len(self.events) + 1}",
            "event_type": event_data["event_type"],
            "user_id": event_data.get("user_id"),
            "session_id": event_data.get("session_id"),
            "properties": event_data.get("properties", {}),
            "timestamp": datetime.now(UTC).isoformat(),
            "source": event_data.get("source", "web"),
        }

        self.events.append(event)

        # Update metrics
        event_type = event["event_type"]
        if event_type not in self.metrics:
            self.metrics[event_type] = {"count": 0, "last_seen": None}

        self.metrics[event_type]["count"] += 1
        self.metrics[event_type]["last_seen"] = event["timestamp"]

        return event

    async def create_session(self, user_id: str, session_data: dict = None) -> dict:
        """Create analytics session."""
        session_id = f"session_{len(self.sessions) + 1}"
        _ = {
            "id": session_id,
            "user_id": user_id,
            "start_time": datetime.now(UTC).isoformat(),
            "end_time": None,
            "page_views": 0,
            "events": [],
            "properties": session_data or {},
            "is_active": True,
        }

        self.sessions[session_id] = session
        return session

    async def end_session(self, session_id: str) -> dict:
        """End analytics session."""
        _ = self.sessions.get(session_id)
        if not session:
            raise ValueError("Session not found")

        session["end_time"] = datetime.now(UTC).isoformat()
        session["is_active"] = False

        # Calculate session duration
        start_time = datetime.fromisoformat(
            session["start_time"].replace("Z", "+00:00")
        )
        end_time = datetime.fromisoformat(session["end_time"].replace("Z", "+00:00"))
        duration = (end_time - start_time).total_seconds()
        session["duration_seconds"] = duration

        return session

    async def get_user_analytics(self, user_id: str, days: int = 30) -> dict:
        """Get analytics for a specific user."""
        cutoff_date = datetime.now(UTC) - timedelta(days=days)

        user_events = [
            event
            for event in self.events
            if event.get("user_id") == user_id
            and datetime.fromisoformat(event["timestamp"].replace("Z", "+00:00"))
            > cutoff_date
        ]

        user_sessions = [
            session
            for session in self.sessions.values()
            if session["user_id"] == user_id
            and datetime.fromisoformat(session["start_time"].replace("Z", "+00:00"))
            > cutoff_date
        ]

        # Calculate metrics
        total_events = len(user_events)
        total_sessions = len(user_sessions)
        total_page_views = sum(
            session.get("page_views", 0) for session in user_sessions
        )

        # Calculate average session duration
        completed_sessions = [s for s in user_sessions if s.get("duration_seconds")]
        avg_session_duration = (
            sum(s["duration_seconds"] for s in completed_sessions)
            / len(completed_sessions)
            if completed_sessions
            else 0
        )

        return {
            "user_id": user_id,
            "period_days": days,
            "total_events": total_events,
            "total_sessions": total_sessions,
            "total_page_views": total_page_views,
            "average_session_duration": avg_session_duration,
            "events": user_events,
            "sessions": user_sessions,
        }

    async def generate_report(self, report_type: str, filters: dict = None) -> dict:
        """Generate analytics report."""
        filters = filters or {}
        start_date = filters.get(
            "start_date", (datetime.now(UTC) - timedelta(days=30)).isoformat()
        )
        end_date = filters.get("end_date", datetime.now(UTC).isoformat())

        # Filter events by date range
        filtered_events = []
        for event in self.events:
            event_time = datetime.fromisoformat(
                event["timestamp"].replace("Z", "+00:00")
            )
            start_time = datetime.fromisoformat(start_date.replace("Z", "+00:00"))
            end_time = datetime.fromisoformat(end_date.replace("Z", "+00:00"))

            if start_time <= event_time <= end_time:
                filtered_events.append(event)

        report_id = f"report_{len(self.reports) + 1}"

        if report_type == "overview":
            report = await self._generate_overview_report(filtered_events)
        elif report_type == "user_behavior":
            report = await self._generate_user_behavior_report(filtered_events)
        elif report_type == "performance":
            report = await self._generate_performance_report(filtered_events)
        else:
            raise ValueError(f"Unknown report type: {report_type}")

        report.update(
            {
                "id": report_id,
                "type": report_type,
                "generated_at": datetime.now(UTC).isoformat(),
                "filters": filters,
                "period": {"start": start_date, "end": end_date},
            }
        )

        self.reports[report_id] = report
        return report

    async def _generate_overview_report(self, events: list[dict]) -> dict:
        """Generate overview report."""
        total_events = len(events)
        unique_users = len(
            set(event.get("user_id") for event in events if event.get("user_id"))
        )

        # Event breakdown
        event_breakdown = {}
        for event in events:
            event_type = event["event_type"]
            event_breakdown[event_type] = event_breakdown.get(event_type, 0) + 1

        return {
            "total_events": total_events,
            "unique_users": unique_users,
            "event_breakdown": event_breakdown,
            "top_events": sorted(
                event_breakdown.items(), key=lambda x: x[1], reverse=True
            )[:10],
        }

    async def _generate_user_behavior_report(self, events: list[dict]) -> dict:
        """Generate user behavior report."""
        user_events = {}
        for event in events:
            user_id = event.get("user_id")
            if user_id:
                if user_id not in user_events:
                    user_events[user_id] = []
                user_events[user_id].append(event)

        # Calculate user patterns
        user_patterns = {}
        for user_id, user_event_list in user_events.items():
            event_types = [e["event_type"] for e in user_event_list]
            most_common_event = (
                max(set(event_types), key=event_types.count) if event_types else None
            )

            user_patterns[user_id] = {
                "total_events": len(user_event_list),
                "unique_event_types": len(set(event_types)),
                "most_common_event": most_common_event,
                "first_event": min(user_event_list, key=lambda x: x["timestamp"])[
                    "timestamp"
                ]
                if user_event_list
                else None,
                "last_event": max(user_event_list, key=lambda x: x["timestamp"])[
                    "timestamp"
                ]
                if user_event_list
                else None,
            }

        return {
            "total_users": len(user_patterns),
            "user_patterns": user_patterns,
            "average_events_per_user": sum(
                p["total_events"] for p in user_patterns.values()
            )
            / len(user_patterns)
            if user_patterns
            else 0,
        }

    async def _generate_performance_report(self, events: list[dict]) -> dict:
        """Generate performance report."""
        # Simulate performance metrics
        performance_events = [
            e for e in events if "performance" in e.get("properties", {})
        ]

        if not performance_events:
            return {
                "total_performance_events": 0,
                "average_response_time": 0,
                "error_rate": 0,
            }

        response_times = []
        error_count = 0

        for event in performance_events:
            props = event.get("properties", {})
            if "response_time" in props:
                response_times.append(props["response_time"])
            if props.get("error"):
                error_count += 1

        avg_response_time = (
            sum(response_times) / len(response_times) if response_times else 0
        )
        error_rate = (
            (error_count / len(performance_events)) * 100 if performance_events else 0
        )

        return {
            "total_performance_events": len(performance_events),
            "average_response_time": avg_response_time,
            "error_rate": error_rate,
            "response_time_samples": response_times[:100],  # First 100 samples
        }


@pytest.fixture
def analytics_engine():
    """Analytics engine fixture."""
    return MockAnalyticsEngine()


class TestEventTracking:
    """Test event tracking functionality."""

    @pytest.mark.asyncio
    async def test_track_basic_event(self, analytics_engine):
        """Test tracking a basic event."""
        event_data = {
            "event_type": "page_view",
            "user_id": "user_123",
            "properties": {"page": "/dashboard", "referrer": "/login"},
        }

        event = await analytics_engine.track_event(event_data)

        assert event["event_type"] == "page_view"
        assert event["user_id"] == "user_123"
        assert event["properties"]["page"] == "/dashboard"
        assert "id" in event
        assert "timestamp" in event

        # Verify event is stored
        assert len(analytics_engine.events) == 1
        assert analytics_engine.events[0]["id"] == event["id"]

    @pytest.mark.asyncio
    async def test_track_multiple_events(self, analytics_engine):
        """Test tracking multiple events."""
        events_data = [
            {"event_type": "login", "user_id": "user_1"},
            {
                "event_type": "page_view",
                "user_id": "user_1",
                "properties": {"page": "/home"},
            },
            {
                "event_type": "click",
                "user_id": "user_1",
                "properties": {"button": "search"},
            },
            {"event_type": "logout", "user_id": "user_1"},
        ]

        tracked_events = []
        for event_data in events_data:
            event = await analytics_engine.track_event(event_data)
            tracked_events.append(event)

        assert len(tracked_events) == 4
        assert len(analytics_engine.events) == 4

        # Verify event types
        event_types = [e["event_type"] for e in tracked_events]
        assert "login" in event_types
        assert "page_view" in event_types
        assert "click" in event_types
        assert "logout" in event_types

    @pytest.mark.asyncio
    async def test_metrics_update(self, analytics_engine):
        """Test that metrics are updated when events are tracked."""
        # Track several events of different types
        await analytics_engine.track_event({"event_type": "login", "user_id": "user_1"})
        await analytics_engine.track_event({"event_type": "login", "user_id": "user_2"})
        await analytics_engine.track_event(
            {"event_type": "page_view", "user_id": "user_1"}
        )

        # Check metrics
        assert "login" in analytics_engine.metrics
        assert "page_view" in analytics_engine.metrics

        assert analytics_engine.metrics["login"]["count"] == 2
        assert analytics_engine.metrics["page_view"]["count"] == 1

        # Check last_seen timestamps
        assert analytics_engine.metrics["login"]["last_seen"] is not None
        assert analytics_engine.metrics["page_view"]["last_seen"] is not None


class TestSessionManagement:
    """Test analytics session management."""

    @pytest.mark.asyncio
    async def test_create_session(self, analytics_engine):
        """Test creating an analytics session."""
        session_data = {"source": "web", "browser": "Chrome", "os": "Windows"}

        _ = await analytics_engine.create_session("user_123", session_data)

        assert session["user_id"] == "user_123"
        assert session["properties"]["browser"] == "Chrome"
        assert session["is_active"] is True
        assert "id" in session
        assert "start_time" in session
        assert session["end_time"] is None

        # Verify session is stored
        assert session["id"] in analytics_engine.sessions

    @pytest.mark.asyncio
    async def test_end_session(self, analytics_engine):
        """Test ending an analytics session."""
        # Create session
        _ = await analytics_engine.create_session("user_123")
        session_id = session["id"]

        # Simulate some time passing
        await asyncio.sleep(0.01)

        # End session
        await analytics_engine.end_session(session_id)

        assert ended_session["is_active"] is False
        assert ended_session["end_time"] is not None
        assert "duration_seconds" in ended_session
        assert ended_session["duration_seconds"] > 0

    @pytest.mark.asyncio
    async def test_session_with_events(self, analytics_engine):
        """Test session tracking with events."""
        # Create session
        _ = await analytics_engine.create_session("user_123")
        session_id = session["id"]

        # Track events in session
        await analytics_engine.track_event(
            {
                "event_type": "page_view",
                "user_id": "user_123",
                "session_id": session_id,
                "properties": {"page": "/dashboard"},
            }
        )

        await analytics_engine.track_event(
            {
                "event_type": "click",
                "user_id": "user_123",
                "session_id": session_id,
                "properties": {"button": "menu"},
            }
        )

        # Verify events are tracked
        assert len(analytics_engine.events) == 2

        # All events should have the session_id
        for event in analytics_engine.events:
            assert event["session_id"] == session_id


class TestUserAnalytics:
    """Test user-specific analytics."""

    @pytest.mark.asyncio
    async def test_get_user_analytics(self, analytics_engine):
        """Test getting analytics for a specific user."""
        user_id = "user_123"

        # Create session and track events
        _ = await analytics_engine.create_session(user_id)
        session_id = session["id"]

        # Track various events
        events_data = [
            {"event_type": "login", "user_id": user_id, "session_id": session_id},
            {
                "event_type": "page_view",
                "user_id": user_id,
                "session_id": session_id,
                "properties": {"page": "/home"},
            },
            {
                "event_type": "page_view",
                "user_id": user_id,
                "session_id": session_id,
                "properties": {"page": "/profile"},
            },
            {
                "event_type": "click",
                "user_id": user_id,
                "session_id": session_id,
                "properties": {"button": "save"},
            },
            {"event_type": "logout", "user_id": user_id, "session_id": session_id},
        ]

        for event_data in events_data:
            await analytics_engine.track_event(event_data)

        # End session
        await analytics_engine.end_session(session_id)

        # Get user analytics
        analytics = await analytics_engine.get_user_analytics(user_id)

        assert analytics["user_id"] == user_id
        assert analytics["total_events"] == 5
        assert analytics["total_sessions"] == 1
        assert analytics["average_session_duration"] > 0
        assert len(analytics["events"]) == 5
        assert len(analytics["sessions"]) == 1

    @pytest.mark.asyncio
    async def test_user_analytics_multiple_sessions(self, analytics_engine):
        """Test user analytics with multiple sessions."""
        user_id = "user_456"

        # Create multiple sessions
        sessions = []
        for i in range(3):
            _ = await analytics_engine.create_session(user_id)
            sessions.append(session)

            # Track events in each session
            await analytics_engine.track_event(
                {
                    "event_type": "page_view",
                    "user_id": user_id,
                    "session_id": session["id"],
                    "properties": {"page": f"/page_{i}"},
                }
            )

            # End session
            await analytics_engine.end_session(session["id"])

        # Get user analytics
        analytics = await analytics_engine.get_user_analytics(user_id)

        assert analytics["total_events"] == 3
        assert analytics["total_sessions"] == 3
        assert len(analytics["sessions"]) == 3

        # All sessions should be ended
        for session in analytics["sessions"]:
            assert session["is_active"] is False
            assert session["end_time"] is not None


class TestReportGeneration:
    """Test analytics report generation."""

    @pytest.mark.asyncio
    async def test_generate_overview_report(self, analytics_engine):
        """Test generating overview report."""
        # Setup test data
        events_data = [
            {"event_type": "login", "user_id": "user_1"},
            {"event_type": "login", "user_id": "user_2"},
            {
                "event_type": "page_view",
                "user_id": "user_1",
                "properties": {"page": "/home"},
            },
            {
                "event_type": "page_view",
                "user_id": "user_2",
                "properties": {"page": "/profile"},
            },
            {
                "event_type": "page_view",
                "user_id": "user_3",
                "properties": {"page": "/settings"},
            },
            {
                "event_type": "click",
                "user_id": "user_1",
                "properties": {"button": "menu"},
            },
            {"event_type": "logout", "user_id": "user_1"},
        ]

        for event_data in events_data:
            await analytics_engine.track_event(event_data)

        # Generate overview report
        report = await analytics_engine.generate_report("overview")

        assert report["type"] == "overview"
        assert report["total_events"] == 7
        assert report["unique_users"] == 3
        assert "event_breakdown" in report
        assert "top_events" in report

        # Check event breakdown
        assert report["event_breakdown"]["login"] == 2
        assert report["event_breakdown"]["page_view"] == 3
        assert report["event_breakdown"]["click"] == 1
        assert report["event_breakdown"]["logout"] == 1

    @pytest.mark.asyncio
    async def test_generate_user_behavior_report(self, analytics_engine):
        """Test generating user behavior report."""
        # Setup test data with user patterns
        events_data = [
            {"event_type": "login", "user_id": "user_1"},
            {"event_type": "page_view", "user_id": "user_1"},
            {"event_type": "page_view", "user_id": "user_1"},
            {"event_type": "click", "user_id": "user_1"},
            {"event_type": "logout", "user_id": "user_1"},
            {"event_type": "login", "user_id": "user_2"},
            {"event_type": "search", "user_id": "user_2"},
            {"event_type": "search", "user_id": "user_2"},
            {"event_type": "search", "user_id": "user_2"},
            {"event_type": "logout", "user_id": "user_2"},
        ]

        for event_data in events_data:
            await analytics_engine.track_event(event_data)

        # Generate user behavior report
        report = await analytics_engine.generate_report("user_behavior")

        assert report["type"] == "user_behavior"
        assert report["total_users"] == 2
        assert "user_patterns" in report
        assert "average_events_per_user" in report

        # Check user patterns
        user_1_pattern = report["user_patterns"]["user_1"]
        assert user_1_pattern["total_events"] == 5
        assert (
            user_1_pattern["most_common_event"] == "page_view"
        )  # Most frequent for user_1

        user_2_pattern = report["user_patterns"]["user_2"]
        assert user_2_pattern["total_events"] == 5
        assert (
            user_2_pattern["most_common_event"] == "search"
        )  # Most frequent for user_2

    @pytest.mark.asyncio
    async def test_generate_performance_report(self, analytics_engine):
        """Test generating performance report."""
        # Setup test data with performance metrics
        events_data = [
            {
                "event_type": "api_call",
                "user_id": "user_1",
                "properties": {
                    "performance": True,
                    "response_time": 0.15,
                    "endpoint": "/api/users",
                },
            },
            {
                "event_type": "api_call",
                "user_id": "user_2",
                "properties": {
                    "performance": True,
                    "response_time": 0.23,
                    "endpoint": "/api/agents",
                },
            },
            {
                "event_type": "api_call",
                "user_id": "user_3",
                "properties": {
                    "performance": True,
                    "response_time": 0.08,
                    "endpoint": "/api/chats",
                    "error": True,
                },
            },
        ]

        for event_data in events_data:
            await analytics_engine.track_event(event_data)

        # Generate performance report
        report = await analytics_engine.generate_report("performance")

        assert report["type"] == "performance"
        assert report["total_performance_events"] == 3
        assert "average_response_time" in report
        assert "error_rate" in report
        assert "response_time_samples" in report

        # Check calculated metrics
        expected_avg_response_time = (0.15 + 0.23 + 0.08) / 3
        assert abs(report["average_response_time"] - expected_avg_response_time) < 0.01

        expected_error_rate = (1 / 3) * 100  # 33.33%
        assert abs(report["error_rate"] - expected_error_rate) < 0.01


class TestAnalyticsIntegration:
    """Test complete analytics integration scenarios."""

    @pytest.mark.asyncio
    async def test_complete_user_journey_analytics(self, analytics_engine):
        """Test tracking complete user journey."""
        user_id = "journey_user"

        # 1. User starts session
        _ = await analytics_engine.create_session(
            user_id, {"source": "organic", "browser": "Chrome"}
        )
        session_id = session["id"]

        # 2. User journey events
        journey_events = [
            {"event_type": "landing", "properties": {"page": "/"}},
            {"event_type": "signup_start", "properties": {"form": "header"}},
            {"event_type": "signup_complete", "properties": {"method": "email"}},
            {"event_type": "first_login", "properties": {}},
            {"event_type": "onboarding_start", "properties": {}},
            {"event_type": "profile_setup", "properties": {"completed": True}},
            {
                "event_type": "first_agent_create",
                "properties": {"agent_type": "assistant"},
            },
            {"event_type": "first_conversation", "properties": {"message_count": 5}},
            {
                "event_type": "feature_discovery",
                "properties": {"feature": "file_upload"},
            },
            {"event_type": "session_end", "properties": {"duration": "long"}},
        ]

        # Track all journey events
        for event_data in journey_events:
            event_data.update({"user_id": user_id, "session_id": session_id})
            await analytics_engine.track_event(event_data)

        # 3. End session
        await analytics_engine.end_session(session_id)

        # 4. Analyze the journey
        user_analytics = await analytics_engine.get_user_analytics(user_id)

        assert user_analytics["total_events"] == len(journey_events)
        assert user_analytics["total_sessions"] == 1

        # Verify journey progression
        events = user_analytics["events"]
        event_types = [e["event_type"] for e in events]

        # Check that events follow expected journey order
        assert event_types[0] == "landing"
        assert "signup_start" in event_types
        assert "signup_complete" in event_types
        assert event_types.index("signup_complete") > event_types.index("signup_start")
        assert event_types[-1] == "session_end"

    @pytest.mark.asyncio
    async def test_multi_user_analytics_aggregation(self, analytics_engine):
        """Test analytics aggregation across multiple users."""
        users = [f"user_{i}" for i in range(5)]

        # Simulate activity for multiple users
        for user_id in users:
            _ = await analytics_engine.create_session(user_id)

            # Each user performs similar but slightly different actions
            user_events = [
                {"event_type": "login"},
                {"event_type": "page_view", "properties": {"page": "/dashboard"}},
                {"event_type": "agent_create", "properties": {"count": 1}},
                {"event_type": "conversation_start"},
                {"event_type": "message_send", "properties": {"length": "medium"}},
                {"event_type": "logout"},
            ]

            for event_data in user_events:
                event_data.update({"user_id": user_id, "session_id": session["id"]})
                await analytics_engine.track_event(event_data)

            await analytics_engine.end_session(session["id"])

        # Generate aggregated reports
        overview_report = await analytics_engine.generate_report("overview")
        behavior_report = await analytics_engine.generate_report("user_behavior")

        # Verify aggregated metrics
        assert (
            overview_report["total_events"] == len(users) * 6
        )  # 5 users × 6 events each
        assert overview_report["unique_users"] == len(users)

        # All users should show similar patterns
        assert behavior_report["total_users"] == len(users)
        assert behavior_report["average_events_per_user"] == 6.0

        # Each user should have consistent behavior patterns
        for user_id in users:
            user_pattern = behavior_report["user_patterns"][user_id]
            assert user_pattern["total_events"] == 6
            assert user_pattern["unique_event_types"] == 6


if __name__ == "__main__":
    pytest.main([__file__])
