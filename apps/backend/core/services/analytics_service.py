"""Analytics service for collecting and processing application metrics.





This service handles analytics data collection, metric aggregation,


and reporting functionality for the AI server.





It also provides a minimal API-facing surface used by the v1 analytics router


for simple health checks, event ingestion/query, timeseries queries, and


ad-hoc aggregates. The implementation is in-memory for now and can be replaced


by infrastructure-backed adapters later.


"""

from __future__ import annotations

import logging
from datetime import UTC, datetime, timedelta
from typing import TYPE_CHECKING, Any, Literal, TypedDict, cast

from apps.backend.core.common.base_classes import BaseService
from apps.backend.core.observability.metrics import Counter, Histogram
from apps.backend.core.observability.tracing import tracer
import Exception
import activities
import activity
import agent_counts
import agent_id
import count
import counts
import created_by
import daily_counts
import dashboard_id
import date
import dict
import dt
import durations
import e
import end_date
import end_time
import ev
import event_counts
import float
import groups
import ingested
import int
import isinstance
import item
import k
import kv
import last_jobs
import len
import limit
import list
import m
import max
import metadata
import offset
import order
import q
import result
import self
import sorted
import start_date
import start_time
import str
import sum
import tuple
import type_counts
import user_counts
import user_id
import v
import x
import zip

if TYPE_CHECKING:
    from collections.abc import Iterable, Sequence


logger = logging.getLogger(__name__)


# Typed dicts for API queries


class MetricQuery(TypedDict, total=False):
    name: str

    start: datetime

    end: datetime

    interval: str

    agg: str

    tags: list[str]


class EventQuery(TypedDict, total=False):
    type: str | None

    user_id: str | None

    session_id: str | None

    start: datetime | None

    end: datetime | None

    tags: list[str]


class AggregateQuery(TypedDict, total=False):
    dataset: str

    measures: list[str]

    group_by: list[str]

    filters: dict[str, Any]

    start: datetime | None

    end: datetime | None

    interval: str | None

    agg: str | None


class AnalyticsService(BaseService):
    """Service for handling analytics and metrics collection."""

    def _setup(self) -> None:
        """Setup service specific state."""

        self.metrics_cache: dict[str, Any] = {}

        self.event_log: list[dict[str, Any]] = []

        # Metrics (use dummy fallbacks when prometheus_client is unavailable)

        self._events_ingested = Counter(
            "zeta_analytics_events_ingested_total",
            "Total analytics events ingested",
            ["type"],
        )

        self._query_latency = Histogram(
            "zeta_analytics_query_latency_seconds",
            "Analytics query latency",
            ["operation"],
        )

    # -------- v1 router API-compatible methods --------

    async def health(self) -> dict[str, Any]:
        """Simple health probe for analytics stack.





        Returns:


            Health dict with status and current timestamp.


        """

        return {"status": "ok", "detail": "analytics-ready", "ts": datetime.now(UTC)}

    async def list_metrics(
        self,
        name: str | None,
        namespace: str | None,  # noqa: ARG002 - placeholder for future filter
        tag: str | None,  # noqa: ARG002 - placeholder for future filter
        limit: int,
        offset: int,
    ) -> list[dict[str, Any]]:
        """List available metrics metadata (static for now).





        Args:


            name: Optional name filter.


            namespace: Optional namespace filter.


            tag: Optional tag filter.


            limit: Page size.


            offset: Page offset.





        Returns:


            A list of metric metadata dicts.


        """

        # Static catalog for demo; can be sourced from registry later

        catalog = [
            {
                "name": "zeta_request_total",
                "namespace": "http",
                "unit": "count",
                "description": "Total HTTP requests",
                "tags": ["path", "method", "status"],
            },
            {
                "name": "zeta_request_latency_seconds",
                "namespace": "http",
                "unit": "seconds",
                "description": "HTTP request latency",
                "tags": ["path", "method"],
            },
            {
                "name": "zeta_analytics_events_ingested_total",
                "namespace": "analytics",
                "unit": "count",
                "description": "Total analytics events ingested",
                "tags": ["type"],
            },
        ]

        items = [m for m in catalog if not name or m["name"].startswith(name)]

        return items[offset : offset + limit]

    async def query_timeseries(self, q: Any) -> dict[str, Any]:
        """Compute a simple timeseries over ingested events.





        Currently supports name 'zeta_analytics_events_ingested_total'.


        """

        query = cast("MetricQuery", q)

        name = query.get("name")

        start = query.get("start")

        end = query.get("end")

        interval = query.get("interval", "1m")

        agg = query.get("agg", "sum")

        if (
            name != "zeta_analytics_events_ingested_total"
            or start is None
            or end is None
        ):
            return {
                "metric": name or "unknown",
                "agg": agg,
                "interval": interval,
                "points": [],
                "tags": query.get("tags", []),
            }

        # Naive bucketing by minute/hour/day based on suffix

        bucket: Literal["minute", "hour", "day"]

        if interval.endswith("m"):
            bucket = "minute"

        elif interval.endswith("h"):
            bucket = "hour"

        else:
            bucket = "day"

        def _bucket_key(dt: datetime) -> datetime:
            if bucket == "minute":
                return dt.replace(second=0, microsecond=0)

            if bucket == "hour":
                return dt.replace(minute=0, second=0, microsecond=0)

            return dt.replace(hour=0, minute=0, second=0, microsecond=0)

        from collections import defaultdict

        counts: dict[datetime, int] = defaultdict(int)

        for e in self.event_log:
            ts = cast("datetime", e.get("timestamp"))

            if ts is None or ts < start or ts > end:
                continue

            counts[_bucket_key(ts)] += 1

        points = [
            {"ts": k, "value": float(v)}
            for k, v in sorted(counts.items(), key=lambda x: x[0])
        ]

        return {
            "metric": name,
            "agg": agg,
            "interval": interval,
            "points": points,
            "tags": query.get("tags", []),
        }

    async def track_event(
        self,
        event_type: str,
        user_id: str | None = None,
        agent_id: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        """Track an analytics event.





        Args:


            event_type: Type of event to track.


            user_id: Optional user ID associated with event.


            agent_id: Optional agent ID associated with event.


            metadata: Additional event metadata.


        """

        event = {
            "type": event_type,
            "timestamp": datetime.now(UTC),
            "user_id": str(user_id) if user_id else None,
            "agent_id": str(agent_id) if agent_id else None,
            "metadata": metadata or {},
        }

        self.event_log.append(event)

        with tracer.start_as_current_span("analytics.track_event"):
            from contextlib import suppress

            with suppress(Exception):  # pragma: no cover
                self._events_ingested.labels(event_type).inc()  # type: ignore[attr-defined]

        logger.info("Tracked event: %s", event_type)

    # API batch ingestion used by router

    async def ingest_events(
        self, events: list[dict[str, Any]], created_by: str | None
    ) -> list[dict[str, Any]]:
        """Ingest a batch of events.





        Args:


            events: List of event dicts.


            created_by: Optional creator identifier (user id).





        Returns:


            The ingested events with IDs (string) assigned.


        """

        from uuid import uuid4

        ingested: list[dict[str, Any]] = []

        with tracer.start_as_current_span("analytics.ingest_events"):
            for e in events:
                item: dict[str, Any] = {
                    "id": str(uuid4()),
                    "type": e.get("type") or "unknown",
                    "timestamp": e.get("ts") or datetime.now(UTC),
                    "user_id": e.get("user_id") or created_by,
                    "session_id": e.get("session_id"),
                    "properties": e.get("properties") or {},
                    "tags": e.get("tags") or [],
                }

                self.event_log.append(item)

                from contextlib import suppress

                with suppress(Exception):  # pragma: no cover
                    self._events_ingested.labels(item["type"]).inc()  # type: ignore[attr-defined]

                ingested.append(item)

        return ingested

    async def get_user_metrics(self, user_id: str) -> dict[str, Any]:
        """Get analytics metrics for a specific user.





        Args:


            user_id: User ID to get metrics for.





        Returns:


            Dictionary containing user metrics.


        """

        user_events = [
            event for event in self.event_log if event.get("user_id") == str(user_id)
        ]

        return {
            "total_events": len(user_events),
            "last_activity": max(
                (event["timestamp"] for event in user_events),
                default=None,
            ),
            "event_types": list({event["type"] for event in user_events}),
            "events_today": len(
                [
                    event
                    for event in user_events
                    if cast("datetime", event["timestamp"]).date()
                    == datetime.now(UTC).date()
                ]
            ),
        }

    async def get_agent_metrics(self, agent_id: str) -> dict[str, Any]:
        """Get analytics metrics for a specific agent.





        Args:


            agent_id: Agent ID to get metrics for.





        Returns:


            Dictionary containing agent metrics.


        """

        agent_events = [
            event for event in self.event_log if event.get("agent_id") == str(agent_id)
        ]

        return {
            "total_interactions": len(agent_events),
            "last_interaction": max(
                (event["timestamp"] for event in agent_events),
                default=None,
            ),
            "interaction_types": list({event["type"] for event in agent_events}),
            "interactions_today": len(
                [
                    event
                    for event in agent_events
                    if cast("datetime", event["timestamp"]).date()
                    == datetime.now(UTC).date()
                ]
            ),
        }

    async def get_system_metrics(self) -> dict[str, Any]:
        """Get overall system analytics metrics.





        Returns:


            Dictionary containing system-wide metrics.


        """

        total_events = len(self.event_log)

        unique_users = len(
            {event["user_id"] for event in self.event_log if event.get("user_id")}
        )

        unique_agents = len(
            {event["agent_id"] for event in self.event_log if event.get("agent_id")}
        )

        return {
            "total_events": total_events,
            "unique_users": unique_users,
            "unique_agents": unique_agents,
            "events_today": len(
                [
                    event
                    for event in self.event_log
                    if cast("datetime", event["timestamp"]).date()
                    == datetime.now(UTC).date()
                ]
            ),
            "most_common_events": self._get_most_common_events(),
        }

    async def get_events_by_timeframe(
        self,
        start_time: datetime,
        end_time: datetime,
        event_type: str | None = None,
    ) -> Sequence[dict[str, Any]]:
        """Get events within a specific timeframe.





        Args:


            start_time: Start of timeframe.


            end_time: End of timeframe.


            event_type: Optional filter by event type.





        Returns:


            List of events matching criteria.


        """

        filtered_events: list[dict[str, Any]] = [
            event
            for event in self.event_log
            if start_time <= cast("datetime", event["timestamp"]) <= end_time
        ]

        if event_type:
            filtered_events = [
                event for event in filtered_events if event["type"] == event_type
            ]

        return filtered_events

    # -------- Event listing for API with basic filters and pagination --------

    async def list_events(
        self,
        q: Any,
        limit: int,
        offset: int,
        order: Literal["asc", "desc"],
    ) -> list[dict[str, Any]]:
        query = cast("EventQuery", q)

        items: Iterable[dict[str, Any]] = self.event_log

        t = query.get("type")

        if t:
            items = (e for e in items if e.get("type") == t)

        uid = query.get("user_id")

        if uid:
            items = (e for e in items if e.get("user_id") == uid)

        sid = query.get("session_id")

        if sid:
            items = (e for e in items if e.get("session_id") == sid)

        s = query.get("start")

        if s is not None:
            s_ts = s.timestamp()

            items = (
                e
                for e in items
                if cast("datetime", e.get("timestamp")).timestamp() >= s_ts
            )

        en = query.get("end")

        if en is not None:
            en_ts = en.timestamp()

            items = (
                e
                for e in items
                if cast("datetime", e.get("timestamp")).timestamp() <= en_ts
            )

        _ = list(items)

        desc = order == "desc"

        result.sort(key=lambda e: cast("datetime", e.get("timestamp")), reverse=desc)

        return result[offset : offset + limit]

    async def generate_report(
        self,
        start_date: datetime,
        end_date: datetime,
    ) -> dict[str, Any]:
        """Generate an analytics report for a date range.





        Args:


            start_date: Start date for report.


            end_date: End date for report.





        Returns:


            Comprehensive analytics report.


        """

        events = await self.get_events_by_timeframe(start_date, end_date)

        return {
            "period": {
                "start": start_date,
                "end": end_date,
                "duration_days": (end_date - start_date).days,
            },
            "overview": {
                "total_events": len(events),
                "unique_users": len(
                    {event["user_id"] for event in events if event.get("user_id")}
                ),
                "unique_agents": len(
                    {event["agent_id"] for event in events if event.get("agent_id")}
                ),
            },
            "event_breakdown": self._analyze_events(events),
            "daily_activity": self._get_daily_activity(events, start_date, end_date),
        }

    def _get_most_common_events(self, limit: int = 10) -> list[dict[str, Any]]:
        """Get most common event types.





        Args:


            limit: Maximum number of events to return.





        Returns:


            List of event types with counts.


        """

        event_counts: dict[str, int] = {}

        for event in self.event_log:
            event_type = event["type"]

            event_counts[event_type] = event_counts.get(event_type, 0) + 1

        return [
            {"type": event_type, "count": count}
            for event_type, count in sorted(
                event_counts.items(), key=lambda x: x[1], reverse=True
            )[:limit]
        ]

    def _analyze_events(self, events: Sequence[dict[str, Any]]) -> dict[str, Any]:
        """Analyze event patterns and distributions.





        Args:


            events: List of events to analyze.





        Returns:


            Event analysis results.


        """

        event_types = [event["type"] for event in events]

        type_counts: dict[str, int] = {}

        for event_type in event_types:
            type_counts[event_type] = type_counts.get(event_type, 0) + 1

        return {
            "event_types": type_counts,
            "most_active_users": self._get_most_active_users(events),
            "most_active_agents": self._get_most_active_agents(events),
        }

    def _get_most_active_users(
        self,
        events: Sequence[dict[str, Any]],
        limit: int = 5,
    ) -> list[dict[str, Any]]:
        """Get most active users from events.





        Args:


            events: List of events to analyze.


            limit: Maximum number of users to return.





        Returns:


            List of most active users.


        """

        user_counts: dict[str, int] = {}

        for event in events:
            if user_id := event.get("user_id"):
                user_counts[user_id] = user_counts.get(user_id, 0) + 1

        return [
            {"user_id": user_id, "event_count": count}
            for user_id, count in sorted(
                user_counts.items(), key=lambda x: x[1], reverse=True
            )[:limit]
        ]

    def _get_most_active_agents(
        self,
        events: Sequence[dict[str, Any]],
        limit: int = 5,
    ) -> list[dict[str, Any]]:
        """Get most active agents from events.





        Args:


            events: List of events to analyze.


            limit: Maximum number of agents to return.





        Returns:


            List of most active agents.


        """

        agent_counts: dict[str, int] = {}

        for event in events:
            if agent_id := event.get("agent_id"):
                agent_counts[agent_id] = agent_counts.get(agent_id, 0) + 1

        return [
            {"agent_id": agent_id, "event_count": count}
            for agent_id, count in sorted(
                agent_counts.items(), key=lambda x: x[1], reverse=True
            )[:limit]
        ]

    def _get_daily_activity(
        self,
        events: Sequence[dict[str, Any]],
        start_date: datetime,
        end_date: datetime,
    ) -> list[dict[str, Any]]:
        """Get daily activity breakdown.





        Args:


            events: List of events to analyze.


            start_date: Start date for analysis.


            end_date: End date for analysis.





        Returns:


            Daily activity data.


        """

        daily_counts: dict[str, int] = {}

        # Initialize all days in range

        current_date = start_date.date()

        while current_date <= end_date.date():
            daily_counts[current_date.isoformat()] = 0

            current_date += timedelta(days=1)

        # Count events by day

        for event in events:
            event_date = cast("datetime", event["timestamp"]).date().isoformat()

            if event_date in daily_counts:
                daily_counts[event_date] += 1

        return [
            {"date": date, "event_count": count}
            for date, count in sorted(daily_counts.items())
        ]

    # -------- Dashboards and compute (minimal stubs) --------

    async def get_dashboard(self, dashboard_id: str) -> dict[str, Any] | None:
        """Return a minimal dashboard definition or None if not found."""

        if dashboard_id != "default":
            return None

        return {
            "id": "default",
            "name": "Default Dashboard",
            "description": "Built-in analytics overview",
            "widgets": [
                {
                    "type": "timeseries",
                    "title": "Events Ingested",
                    "metric": "zeta_analytics_events_ingested_total",
                }
            ],
        }

    async def compute(self, q: Any) -> dict[str, Any]:
        """Compute a simple aggregate over the in-memory events.





        Supports count() grouped by type/user_id/session_id.


        """

        query = cast("AggregateQuery", q)

        dataset = query.get("dataset", "events")

        if dataset != "events":
            return {"rows": [], "meta": {"dataset": dataset}}

        items: Iterable[dict[str, Any]] = self.event_log

        f = query.get("filters", {})

        t = f.get("type")

        if t:
            items = (e for e in items if e.get("type") == t)

        uid = f.get("user_id")

        if uid:
            items = (e for e in items if e.get("user_id") == uid)

        sid = f.get("session_id")

        if sid:
            items = (e for e in items if e.get("session_id") == sid)

        group_by = query.get("group_by", [])

        from collections import defaultdict

        groups: dict[tuple[Any, ...], int] = defaultdict(int)

        for e in items:
            key = tuple(e.get(k) for k in group_by) if group_by else ()

            groups[key] += 1

        rows = [
            {
                "group": dict(zip(group_by, key, strict=False)),
                "values": {"count": float(count)},
            }
            for key, count in sorted(groups.items(), key=lambda kv: kv[1], reverse=True)
        ]

        return {"rows": rows, "meta": {"dataset": dataset, "group_by": group_by}}

    # -------- Dashboard compatibility (merged from deprecated DashboardService) --------

    async def get_dashboard_stats(self, user_id: Any) -> dict[str, Any]:
        """Return dashboard statistics for a user.





        This implementation derives stats from in-memory analytics events. It matches


        the API schema expected by app/serializers/dashboard_serializers.py (StatsOut).


        """

        uid = str(user_id)

        user_events = [e for e in self.event_log if e.get("user_id") == uid]

        total_items = len(user_events)

        total_tokens = sum(
            int(e.get("properties", {}).get("tokens", 0)) for e in user_events
        )

        successes = sum(
            1
            for e in user_events
            if (e.get("properties", {}) or {}).get("status") == "completed"
        )

        success_rate = (successes / total_items) if total_items else 0.0

        durations: list[float] = []

        for e in user_events:
            props = e.get("properties") or {}

            d = props.get("duration_sec")

            if isinstance(d, int | float):
                durations.append(float(d))

        avg_job_time = (sum(durations) / len(durations)) if durations else 0.0

        recent = sorted(
            user_events,
            key=lambda x: cast("datetime", x.get("timestamp")),
            reverse=True,
        )[:5]

        last_jobs: list[dict[str, Any]] = []

        for ev in recent:
            props = cast("dict[str, Any]", ev.get("properties") or {})

            last_jobs.append(
                {
                    "job_id": props.get("job_id", ""),
                    "source": props.get("source", ""),
                    "status": props.get("status", "unknown"),
                    "duration_sec": float(props.get("duration_sec", 0.0)),
                }
            )

        return {
            "total_items": total_items,
            "total_tokens": total_tokens,
            "success_rate": success_rate,
            "avg_job_time": avg_job_time,
            "last_jobs": last_jobs,
        }

    async def get_recent_activities(
        self, user_id: Any, limit: int = 10
    ) -> list[dict[str, str]]:
        """Return recent activities for a user based on analytics events."""

        uid = str(user_id)

        items = [e for e in self.event_log if e.get("user_id") == uid]

        items.sort(key=lambda x: cast("datetime", x.get("timestamp")), reverse=True)

        activities: list[dict[str, str]] = []

        for e in items[:limit]:
            props = cast("dict[str, Any]", e.get("properties") or {})

            title = props.get("title") or f"Event: {e.get('type', 'unknown')}"

            status = (props.get("status") or "").lower()

            activity: dict[str, str] = {
                "id": str(props.get("job_id") or props.get("id") or ""),
                "type": str(e.get("type") or "event"),
                "title": str(title),
                "description": f"Status: {status or 'n/a'}",
                "timestamp": cast("datetime", e.get("timestamp")).isoformat()
                if e.get("timestamp")
                else "",
                "status": status,
            }

            prog = props.get("progress")

            if isinstance(prog, int | float):
                activity["progress"] = f"{float(prog):.1%}"

            activities.append(activity)

        return activities
