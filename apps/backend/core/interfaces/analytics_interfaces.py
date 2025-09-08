"""Analytics interfaces.

This module defines abstract interfaces for analytics operations
including metrics collection, data analysis, and reporting.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any
import bool
import dict
import float
import int
import list
import str
import tuple


class MetricsCollectionInterface(ABC):
    """Interface for metrics collection operations."""

    @abstractmethod
    async def record_metric(
        self,
        name: str,
        value: float,
        tags: dict[str, str] | None = None,
        timestamp: float | None = None,
    ) -> bool:
        """Record a metric value.

        Args:
            name: Metric name.
            value: Metric value.
            tags: Optional metric tags.
            timestamp: Optional timestamp.

        Returns:
            True if metric recorded successfully.
        """

    @abstractmethod
    async def record_counter(
        self,
        name: str,
        increment: int = 1,
        tags: dict[str, str] | None = None,
    ) -> bool:
        """Record counter increment.

        Args:
            name: Counter name.
            increment: Increment value.
            tags: Optional counter tags.

        Returns:
            True if counter recorded successfully.
        """

    @abstractmethod
    async def record_histogram(
        self,
        name: str,
        value: float,
        tags: dict[str, str] | None = None,
    ) -> bool:
        """Record histogram value.

        Args:
            name: Histogram name.
            value: Value to record.
            tags: Optional histogram tags.

        Returns:
            True if histogram recorded successfully.
        """

    @abstractmethod
    async def record_gauge(
        self,
        name: str,
        value: float,
        tags: dict[str, str] | None = None,
    ) -> bool:
        """Record gauge value.

        Args:
            name: Gauge name.
            value: Current gauge value.
            tags: Optional gauge tags.

        Returns:
            True if gauge recorded successfully.
        """

    @abstractmethod
    async def get_metric_stats(
        self,
        name: str,
        start_time: float | None = None,
        end_time: float | None = None,
        tags: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Get metric statistics.

        Args:
            name: Metric name.
            start_time: Start time filter.
            end_time: End time filter.
            tags: Optional tag filters.

        Returns:
            Metric statistics.
        """


class DataAnalysisInterface(ABC):
    """Interface for data analysis operations."""

    @abstractmethod
    async def analyze_time_series(
        self,
        data: list[dict[str, Any]],
        time_column: str,
        value_column: str,
        analysis_type: str = "trend",
    ) -> dict[str, Any]:
        """Analyze time series data.

        Args:
            data: Time series data.
            time_column: Column containing time values.
            value_column: Column containing values to analyze.
            analysis_type: Type of analysis (trend, seasonality, etc.).

        Returns:
            Analysis results.
        """

    @abstractmethod
    async def compute_statistics(
        self,
        data: list[float],
        statistics: list[str] | None = None,
    ) -> dict[str, float]:
        """Compute statistical measures.

        Args:
            data: Numerical data.
            statistics: List of statistics to compute.

        Returns:
            Computed statistics.
        """

    @abstractmethod
    async def detect_anomalies(
        self,
        data: list[dict[str, Any]],
        method: str = "isolation_forest",
        threshold: float = 0.1,
    ) -> list[dict[str, Any]]:
        """Detect anomalies in data.

        Args:
            data: Input data for analysis.
            method: Anomaly detection method.
            threshold: Anomaly threshold.

        Returns:
            List of detected anomalies.
        """

    @abstractmethod
    async def correlate_data(
        self,
        dataset1: list[float],
        dataset2: list[float],
        method: str = "pearson",
    ) -> float:
        """Compute correlation between datasets.

        Args:
            dataset1: First dataset.
            dataset2: Second dataset.
            method: Correlation method.

        Returns:
            Correlation coefficient.
        """

    @abstractmethod
    async def segment_data(
        self,
        data: list[dict[str, Any]],
        features: list[str],
        num_segments: int = 3,
    ) -> dict[str, Any]:
        """Segment data into clusters.

        Args:
            data: Input data.
            features: Features to use for segmentation.
            num_segments: Number of segments to create.

        Returns:
            Segmentation results.
        """


class ReportingInterface(ABC):
    """Interface for reporting operations."""

    @abstractmethod
    async def generate_report(
        self,
        report_type: str,
        data_sources: list[str],
        filters: dict[str, Any] | None = None,
        format_: str = "json",
    ) -> dict[str, Any]:
        """Generate analytical report.

        Args:
            report_type: Type of report to generate.
            data_sources: List of data source identifiers.
            filters: Optional data filters.
            format_: Report format.

        Returns:
            Generated report.
        """

    @abstractmethod
    async def schedule_report(
        self,
        report_config: dict[str, Any],
        schedule: str,
        recipients: list[str],
    ) -> str:
        """Schedule recurring report.

        Args:
            report_config: Report configuration.
            schedule: Schedule expression (cron-like).
            recipients: List of report recipients.

        Returns:
            Scheduled report ID.
        """

    @abstractmethod
    async def export_data(
        self,
        query: dict[str, Any],
        format_: str = "csv",
        compression: str | None = None,
    ) -> str:
        """Export data based on query.

        Args:
            query: Data query specification.
            format_: Export format.
            compression: Optional compression method.

        Returns:
            Export file path or URL.
        """

    @abstractmethod
    async def create_dashboard(
        self,
        name: str,
        widgets: list[dict[str, Any]],
        layout: dict[str, Any],
    ) -> str:
        """Create analytics dashboard.

        Args:
            name: Dashboard name.
            widgets: List of dashboard widgets.
            layout: Dashboard layout configuration.

        Returns:
            Dashboard ID.
        """


class UserAnalyticsInterface(ABC):
    """Interface for user behavior analytics."""

    @abstractmethod
    async def track_user_event(
        self,
        user_id: str,
        event_name: str,
        properties: dict[str, Any] | None = None,
        timestamp: float | None = None,
    ) -> bool:
        """Track user behavior event.

        Args:
            user_id: User identifier.
            event_name: Name of the event.
            properties: Optional event properties.
            timestamp: Optional event timestamp.

        Returns:
            True if event tracked successfully.
        """

    @abstractmethod
    async def analyze_user_journey(
        self,
        user_id: str,
        start_time: float | None = None,
        end_time: float | None = None,
    ) -> dict[str, Any]:
        """Analyze user journey and behavior patterns.

        Args:
            user_id: User identifier.
            start_time: Journey start time.
            end_time: Journey end time.

        Returns:
            User journey analysis.
        """

    @abstractmethod
    async def compute_user_segments(
        self,
        criteria: dict[str, Any],
        time_range: tuple[float, float] | None = None,
    ) -> list[dict[str, Any]]:
        """Compute user segments based on criteria.

        Args:
            criteria: Segmentation criteria.
            time_range: Optional time range for analysis.

        Returns:
            List of user segments.
        """

    @abstractmethod
    async def get_user_metrics(
        self,
        user_id: str,
        metrics: list[str],
        time_range: tuple[float, float] | None = None,
    ) -> dict[str, Any]:
        """Get metrics for specific user.

        Args:
            user_id: User identifier.
            metrics: List of metrics to retrieve.
            time_range: Optional time range.

        Returns:
            User metrics.
        """


class PerformanceAnalyticsInterface(ABC):
    """Interface for performance analytics."""

    @abstractmethod
    async def measure_response_time(
        self,
        operation: str,
        start_time: float,
        end_time: float,
        metadata: dict[str, Any] | None = None,
    ) -> bool:
        """Measure operation response time.

        Args:
            operation: Operation identifier.
            start_time: Operation start time.
            end_time: Operation end time.
            metadata: Optional operation metadata.

        Returns:
            True if measurement recorded.
        """

    @abstractmethod
    async def track_resource_usage(
        self,
        resource_type: str,
        usage_data: dict[str, float],
        timestamp: float | None = None,
    ) -> bool:
        """Track resource usage metrics.

        Args:
            resource_type: Type of resource (CPU, memory, etc.).
            usage_data: Resource usage measurements.
            timestamp: Optional timestamp.

        Returns:
            True if usage tracked successfully.
        """

    @abstractmethod
    async def analyze_bottlenecks(
        self,
        system_component: str,
        time_range: tuple[float, float],
    ) -> list[dict[str, Any]]:
        """Analyze performance bottlenecks.

        Args:
            system_component: Component to analyze.
            time_range: Time range for analysis.

        Returns:
            List of identified bottlenecks.
        """

    @abstractmethod
    async def generate_performance_report(
        self,
        components: list[str],
        time_range: tuple[float, float],
        metrics: list[str] | None = None,
    ) -> dict[str, Any]:
        """Generate performance analysis report.

        Args:
            components: List of components to analyze.
            time_range: Time range for report.
            metrics: Optional specific metrics to include.

        Returns:
            Performance report.
        """


class BusinessAnalyticsInterface(ABC):
    """Interface for business analytics operations."""

    @abstractmethod
    async def compute_kpi(
        self,
        kpi_name: str,
        parameters: dict[str, Any],
        time_range: tuple[float, float] | None = None,
    ) -> float:
        """Compute key performance indicator.

        Args:
            kpi_name: Name of the KPI.
            parameters: KPI calculation parameters.
            time_range: Optional time range for calculation.

        Returns:
            Computed KPI value.
        """

    @abstractmethod
    async def analyze_conversion_funnel(
        self,
        funnel_steps: list[str],
        time_range: tuple[float, float],
        filters: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Analyze conversion funnel performance.

        Args:
            funnel_steps: List of funnel step identifiers.
            time_range: Time range for analysis.
            filters: Optional data filters.

        Returns:
            Funnel analysis results.
        """

    @abstractmethod
    async def forecast_metrics(
        self,
        metric_name: str,
        historical_data: list[dict[str, Any]],
        forecast_periods: int,
        model_type: str = "arima",
    ) -> dict[str, Any]:
        """Forecast future metric values.

        Args:
            metric_name: Name of metric to forecast.
            historical_data: Historical metric data.
            forecast_periods: Number of periods to forecast.
            model_type: Forecasting model type.

        Returns:
            Forecast results with predictions and confidence intervals.
        """

    @abstractmethod
    async def calculate_roi(
        self,
        investment_data: dict[str, float],
        revenue_data: dict[str, float],
        time_period: str,
    ) -> dict[str, float]:
        """Calculate return on investment.

        Args:
            investment_data: Investment cost data.
            revenue_data: Revenue data.
            time_period: Time period for calculation.

        Returns:
            ROI calculation results.
        """


class DataVisualizationInterface(ABC):
    """Interface for data visualization operations."""

    @abstractmethod
    async def create_chart(
        self,
        chart_type: str,
        data: list[dict[str, Any]],
        config: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Create data visualization chart.

        Args:
            chart_type: Type of chart (bar, line, pie, etc.).
            data: Data to visualize.
            config: Optional chart configuration.

        Returns:
            Chart specification and data.
        """

    @abstractmethod
    async def generate_heatmap(
        self,
        data: list[list[float]],
        labels: dict[str, list[str]] | None = None,
    ) -> dict[str, Any]:
        """Generate heatmap visualization.

        Args:
            data: 2D data array for heatmap.
            labels: Optional axis labels.

        Returns:
            Heatmap specification.
        """

    @abstractmethod
    async def create_time_series_plot(
        self,
        time_series_data: list[dict[str, Any]],
        time_column: str,
        value_columns: list[str],
    ) -> dict[str, Any]:
        """Create time series plot.

        Args:
            time_series_data: Time series data.
            time_column: Column containing time values.
            value_columns: Columns containing values to plot.

        Returns:
            Time series plot specification.
        """

    @abstractmethod
    async def export_visualization(
        self,
        visualization: dict[str, Any],
        format_: str = "png",
        resolution: tuple[int, int] | None = None,
    ) -> str:
        """Export visualization to file.

        Args:
            visualization: Visualization specification.
            format_: Export format (png, svg, pdf, etc.).
            resolution: Optional resolution for raster formats.

        Returns:
            Export file path or URL.
        """
