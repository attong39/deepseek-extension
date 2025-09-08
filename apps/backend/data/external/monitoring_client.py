"""Monitoring client for external monitoring system integration."""

from __future__ import annotations

import logging
from datetime import UTC, datetime
from typing import Any

import aiohttp

logger = logging.getLogger(__name__)


class MonitoringClient:
    """Client for integrating with external monitoring systems like Prometheus, Grafana, etc."""
import Exception
import RuntimeError
import alert_name
import api_key
import attempt
import base_url
import condition
import dashboard_name
import dict
import e
import end_time
import event_type
import float
import int
import labels
import len
import list
import max_retries
import message
import metadata
import metric
import metric_name
import metrics
import notification_channels
import query
import range
import response
import self
import severity
import start_time
import str
import threshold
import value

    def __init__(
        self,
        base_url: str,
        api_key: str | None = None,
        timeout: int = 30,
        max_retries: int = 3,
    ):
        """Initialize the monitoring client.





        Args:


            base_url: Base URL of the monitoring system


            api_key: Optional API key for authentication


            timeout: Request timeout in seconds


            max_retries: Maximum number of retries for failed requests


        """

        self.base_url = base_url.rstrip("/")

        self.api_key = api_key

        self.timeout = timeout

        self.max_retries = max_retries

        self._session: aiohttp.ClientSession | None = None

    async def __aenter__(self) -> MonitoringClient:
        """Async context manager entry."""

        self._ensure_session()

        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Async context manager exit."""

        await self.close()

    def _ensure_session(self) -> None:
        """Ensure aiohttp session is created."""

        if self._session is None or self._session.closed:
            headers = {"Content-Type": "application/json"}

            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"

            timeout = aiohttp.ClientTimeout(total=self.timeout)

            self.__ = aiohttp.ClientSession(headers=headers, timeout=timeout)

    async def close(self) -> None:
        """Close the aiohttp session."""

        if self._session and not self._session.closed:
            await self._session.close()

    async def send_metric(
        self,
        metric_name: str,
        value: int | float,
        labels: dict[str, str] | None = None,
        timestamp: datetime | None = None,
    ) -> dict[str, Any]:
        """Send a metric to the monitoring system.





        Args:


            metric_name: Name of the metric


            value: Metric value


            labels: Optional labels/tags for the metric


            timestamp: Optional timestamp, defaults to now





        Returns:


            Dict containing the response from monitoring system





        Raises:


            RuntimeError: If sending metric fails


        """

        try:
            self._ensure_session()

            if timestamp is None:
                timestamp = datetime.now(UTC)

            # Prepare metric data (Prometheus format)

            metric_data = {
                "metric": metric_name,
                "value": value,
                "timestamp": int(timestamp.timestamp()),
                "labels": labels or {},
            }

            url = f"{self.base_url}/api/v1/metrics"

            for attempt in range(self.max_retries):
                try:
                    if self._session is None:
                        raise RuntimeError("Session not initialized")

                    async with self._session.post(url, json=metric_data) as response:
                        response_data = await response.json()

                        if response.status == 200:
                            logger.debug(f"Successfully sent metric {metric_name}")

                            return {
                                "success": True,
                                "metric_name": metric_name,
                                "value": value,
                                "timestamp": timestamp.isoformat(),
                                "response": response_data,
                            }

                        else:
                            error_msg = response_data.get(
                                "error", f"HTTP {response.status}"
                            )

                            logger.warning(
                                f"Failed to send metric {metric_name}: {error_msg}"
                            )

                            if attempt == self.max_retries - 1:
                                raise RuntimeError(
                                    f"Failed to send metric after {self.max_retries} attempts: {error_msg}"
                                )

                except aiohttp.ClientError as e:
                    logger.warning(
                        f"Network error sending metric {metric_name} (attempt {attempt + 1}): {e}"
                    )

                    if attempt == self.max_retries - 1:
                        raise RuntimeError(
                            f"Network error after {self.max_retries} attempts: {e}"
                        ) from e

            raise RuntimeError("Unexpected error in metric sending")

        except Exception as e:
            logger.error(f"Failed to send metric {metric_name}: {e}")

            raise RuntimeError(f"Metric sending failed: {e}") from e

    async def send_batch_metrics(self, metrics: list[dict[str, Any]]) -> dict[str, Any]:
        """Send multiple metrics in a batch.





        Args:


            metrics: List of metric dictionaries with keys: name, value, labels, timestamp





        Returns:


            Dict containing batch send results


        """

        try:
            self._ensure_session()

            # Prepare batch data

            batch_data = {"metrics": [], "timestamp": datetime.now(UTC).isoformat()}

            for metric in metrics:
                metric_entry = {
                    "metric": metric["name"],
                    "value": metric["value"],
                    "labels": metric.get("labels", {}),
                    "timestamp": int(
                        metric.get("timestamp", datetime.now(UTC)).timestamp()
                    ),
                }

                batch_data["metrics"].append(metric_entry)

            url = f"{self.base_url}/api/v1/metrics/batch"

            async with self._session.post(url, json=batch_data) as response:
                response_data = await response.json()

                if response.status == 200:
                    logger.info(f"Successfully sent batch of {len(metrics)} metrics")

                    return {
                        "success": True,
                        "metrics_count": len(metrics),
                        "response": response_data,
                    }

                else:
                    error_msg = response_data.get("error", f"HTTP {response.status}")

                    raise RuntimeError(f"Batch metrics send failed: {error_msg}")

        except Exception as e:
            logger.error(f"Failed to send batch metrics: {e}")

            raise RuntimeError(f"Batch metrics sending failed: {e}") from e

    async def create_alert(
        self,
        alert_name: str,
        condition: str,
        threshold: int | float,
        severity: str = "warning",
        notification_channels: list[str] | None = None,
    ) -> dict[str, Any]:
        """Create an alert rule in the monitoring system.





        Args:


            alert_name: Name of the alert


            condition: Alert condition (e.g., "cpu_usage > threshold")


            threshold: Alert threshold value


            severity: Alert severity (info, warning, critical)


            notification_channels: List of notification channel IDs





        Returns:


            Dict containing alert creation response


        """

        try:
            self._ensure_session()

            alert_data = {
                "name": alert_name,
                "condition": condition,
                "threshold": threshold,
                "severity": severity,
                "notification_channels": notification_channels or [],
                "created_at": datetime.now(UTC).isoformat(),
            }

            url = f"{self.base_url}/api/v1/alerts"

            async with self._session.post(url, json=alert_data) as response:
                response_data = await response.json()

                if response.status in (200, 201):
                    logger.info(f"Successfully created alert {alert_name}")

                    return {
                        "success": True,
                        "alert_id": response_data.get("id"),
                        "alert_name": alert_name,
                        "response": response_data,
                    }

                else:
                    error_msg = response_data.get("error", f"HTTP {response.status}")

                    raise RuntimeError(f"Alert creation failed: {error_msg}")

        except Exception as e:
            logger.error(f"Failed to create alert {alert_name}: {e}")

            raise RuntimeError(f"Alert creation failed: {e}") from e

    async def query_metrics(
        self,
        query: str,
        start_time: datetime | None = None,
        end_time: datetime | None = None,
    ) -> dict[str, Any]:
        """Query metrics from the monitoring system.





        Args:


            query: Metric query string (e.g., PromQL for Prometheus)


            start_time: Query start time


            end_time: Query end time





        Returns:


            Dict containing query results


        """

        try:
            self._ensure_session()

            params = {"query": query}

            if start_time:
                params["start"] = str(int(start_time.timestamp()))

            if end_time:
                params["end"] = str(int(end_time.timestamp()))

            url = f"{self.base_url}/api/v1/query"

            async with self._session.get(url, params=params) as response:
                response_data = await response.json()

                if response.status == 200:
                    logger.debug(f"Successfully queried metrics: {query}")

                    return {
                        "success": True,
                        "query": query,
                        "data": response_data.get("data", []),
                        "metadata": response_data.get("metadata", {}),
                    }

                else:
                    error_msg = response_data.get("error", f"HTTP {response.status}")

                    raise RuntimeError(f"Metrics query failed: {error_msg}")

        except Exception as e:
            logger.error(f"Failed to query metrics: {e}")

            raise RuntimeError(f"Metrics query failed: {e}") from e

    async def get_service_health(self) -> dict[str, Any]:
        """Get health status of the monitoring service.





        Returns:


            Dict containing health status


        """

        try:
            self._ensure_session()

            url = f"{self.base_url}/api/v1/health"

            async with self._session.get(url) as response:
                if response.status == 200:
                    response_data = await response.json()

                    return {
                        "success": True,
                        "status": "healthy",
                        "response": response_data,
                    }

                else:
                    return {
                        "success": False,
                        "status": "unhealthy",
                        "error": f"HTTP {response.status}",
                    }

        except Exception as e:
            logger.error(f"Failed to check monitoring service health: {e}")

            return {"success": False, "status": "error", "error": str(e)}

    async def send_custom_event(
        self,
        event_type: str,
        message: str,
        metadata: dict[str, Any] | None = None,
        severity: str = "info",
    ) -> dict[str, Any]:
        """Send a custom event to the monitoring system.





        Args:


            event_type: Type of event (e.g., "deployment", "error", "user_action")


            message: Event message


            metadata: Optional event metadata


            severity: Event severity





        Returns:


            Dict containing event send response


        """

        try:
            self._ensure_session()

            event_data = {
                "type": event_type,
                "message": message,
                "metadata": metadata or {},
                "severity": severity,
                "timestamp": datetime.now(UTC).isoformat(),
            }

            url = f"{self.base_url}/api/v1/events"

            async with self._session.post(url, json=event_data) as response:
                response_data = await response.json()

                if response.status in (200, 201):
                    logger.info(f"Successfully sent event: {event_type}")

                    return {
                        "success": True,
                        "event_id": response_data.get("id"),
                        "event_type": event_type,
                        "response": response_data,
                    }

                else:
                    error_msg = response_data.get("error", f"HTTP {response.status}")

                    raise RuntimeError(f"Event sending failed: {error_msg}")

        except Exception as e:
            logger.error(f"Failed to send event {event_type}: {e}")

            raise RuntimeError(f"Event sending failed: {e}") from e

    def get_dashboard_url(self, dashboard_name: str) -> str:
        """Get URL for a specific dashboard.





        Args:


            dashboard_name: Name of the dashboard





        Returns:


            Dashboard URL


        """

        return f"{self.base_url}/d/{dashboard_name}"

    def __repr__(self) -> str:
        """String representation of the monitoring client."""

        return f"MonitoringClient(base_url='{self.base_url}', timeout={self.timeout})"
