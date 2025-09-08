"""
Performance Intelligence Integration Manager.

Features:
- Seamless integration với existing FastAPI routes
- Performance monitoring middleware integration
- ML-driven insights API endpoints
- Real-time performance dashboard data
- Enterprise-grade monitoring activation
"""

from __future__ import annotations

import logging
from datetime import UTC
from typing import Any

from apps.backend.perf.production_config import (
import Exception
import ImportError
import abs
import any
import app
import background_tasks
import bool
import dict
import exc
import float
import imp
import int
import len
import request
import str
import sum
    get_enhanced_runtime,
    get_enhanced_settings,
    is_feature_enabled,
    update_runtime_feature,
)
from apps.backend.perf.success_metrics import BaselineMetrics, SuccessMetricsTracker
from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel

logger = logging.getLogger("zeta.perf.integration")

# Initialize success metrics tracker
_success_tracker = SuccessMetricsTracker()

# Create enhanced performance router
enhanced_router = APIRouter(prefix="/admin/perf/enhanced", tags=["perf-enhanced"])


class PerformanceStatusResponse(BaseModel):
    """Performance system status response."""

    status: str
    enhanced_features_available: bool
    active_features: dict[str, bool]
    current_metrics: dict[str, Any]
    success_metrics: dict[str, Any]


class FeatureToggleRequest(BaseModel):
    """Feature toggle request."""

    feature_name: str
    enabled: bool
    reason: str = ""


class BaselineSetupRequest(BaseModel):
    """Baseline metrics setup request."""

    avg_response_time_ms: float
    p95_response_time_ms: float
    p99_response_time_ms: float
    requests_per_second: float
    error_rate_percent: float
    cpu_usage_percent: float
    memory_usage_percent: float
    alert_frequency_per_day: int = 0
    debugging_time_hours_per_incident: float = 0.0
    system_downtime_minutes_per_month: float = 0.0
    infrastructure_cost_per_month: float = 0.0
    engineering_hours_per_month: float = 0.0


def _require_enhanced_features():
    """Dependency to ensure enhanced features are available."""
    if not is_feature_enabled("enhanced_metrics"):
        raise HTTPException(
            status_code=503, detail="Enhanced performance features not available"
        )


async def _collect_ml_insights() -> dict[str, Any]:
    """Collect ML-driven performance insights."""
    insights = {
        "anomalies_detected": [],
        "predictions": [],
        "optimization_recommendations": [],
        "alert_summary": {},
    }

    try:
        # Try to collect ML insights if features are enabled
        if is_feature_enabled("anomaly_detection"):
            try:
                import importlib.util

                if importlib.util.find_spec("zeta_vn.perf.ml_optimization"):
                    insights["anomaly_detection_active"] = True
                    insights["anomaly_detector_available"] = True
            except ImportError:
                insights["anomaly_detection_error"] = "ML components not available"

        if is_feature_enabled("predictive_analysis"):
            try:
                import importlib.util

                if importlib.util.find_spec("zeta_vn.perf.ml_optimization"):
                    insights["predictive_analysis_active"] = True
                    insights["predictor_available"] = True
            except ImportError:
                insights["predictive_analysis_error"] = "ML components not available"

        if is_feature_enabled("intelligent_alerting"):
            from apps.backend.perf.ml_optimization import IntelligentAlertManager

            # In production, this would be a singleton instance
            alert_manager = IntelligentAlertManager()
            insights["alert_summary"] = alert_manager.get_alert_summary()

    except ImportError as exc:
        logger.warning("ML components not available: %s", exc)
        insights["ml_components_error"] = str(exc)

    return insights


@enhanced_router.get("/status", response_model=PerformanceStatusResponse)
async def get_enhanced_performance_status():
    """
    Get comprehensive performance system status với enhanced features.

    Returns detailed status including ML components, success metrics,
    và current performance state.
    """
    settings = get_enhanced_settings()
    runtime = get_enhanced_runtime()
    flags = settings.get_feature_flags()

    # Collect active features
    active_features = {
        "basic_monitoring": runtime.enabled,
        "enhanced_metrics": runtime.enhanced_metrics_active,
        "ml_optimization": runtime.ml_optimization_active,
        "anomaly_detection": runtime.anomaly_detection_active,
        "predictive_analysis": runtime.predictive_analysis_active,
        "intelligent_alerting": runtime.intelligent_alerting_active,
        "emergency_mode": runtime.emergency_mode,
    }

    # Collect ML insights
    ml_insights = await _collect_ml_insights()

    # Get success metrics
    success_report = _success_tracker.generate_success_report()

    # Current performance metrics (simplified for demo)
    current_metrics = {
        "load_level": runtime.current_load_level,
        "auto_optimization_enabled": runtime.auto_optimization_enabled,
        "monitoring_interval_seconds": settings.METRICS_COLLECTION_INTERVAL,
        "ml_insights": ml_insights,
    }

    # Determine overall status
    if runtime.emergency_mode:
        status = "emergency"
    elif runtime.enabled and any(active_features.values()):
        status = "enhanced_active"
    elif runtime.enabled:
        status = "basic_active"
    else:
        status = "disabled"

    return PerformanceStatusResponse(
        status=status,
        enhanced_features_available=any(
            [
                flags.enhanced_metrics,
                flags.ml_optimization,
                flags.anomaly_detection,
            ]
        ),
        active_features=active_features,
        current_metrics=current_metrics,
        success_metrics=success_report,
    )


@enhanced_router.post("/features/toggle")
async def toggle_enhanced_feature(
    request: FeatureToggleRequest,
    background_tasks: BackgroundTasks,
):
    """
    Toggle enhanced performance features at runtime.

    Allows safe enablement/disablement của advanced features
    without requiring application restart.
    """
    success = update_runtime_feature(request.feature_name, request.enabled)

    if not success:
        raise HTTPException(
            status_code=400, detail=f"Unknown feature: {request.feature_name}"
        )

    # Log the change
    action = "enabled" if request.enabled else "disabled"
    logger.info(
        "Feature %s %s by admin. Reason: %s",
        request.feature_name,
        action,
        request.reason or "No reason provided",
    )

    # Background task to update monitoring
    def _update_monitoring():
        runtime = get_enhanced_runtime()
        logger.info(
            "Updated runtime state: %s",
            {
                "enhanced_metrics": runtime.enhanced_metrics_active,
                "ml_optimization": runtime.ml_optimization_active,
                "anomaly_detection": runtime.anomaly_detection_active,
            },
        )

    background_tasks.add_task(_update_monitoring)

    return {
        "success": True,
        "feature": request.feature_name,
        "enabled": request.enabled,
        "message": f"Feature {request.feature_name} {action} successfully",
    }


@enhanced_router.post("/baseline/setup")
async def setup_performance_baseline(request: BaselineSetupRequest):
    """
    Setup performance baseline cho success metrics tracking.

    Establishes baseline measurements để compare against
    after performance optimization implementation.
    """
    from datetime import datetime

    baseline = BaselineMetrics(
        timestamp=datetime.now(UTC),
        avg_response_time_ms=request.avg_response_time_ms,
        p95_response_time_ms=request.p95_response_time_ms,
        p99_response_time_ms=request.p99_response_time_ms,
        requests_per_second=request.requests_per_second,
        error_rate_percent=request.error_rate_percent,
        cpu_usage_percent=request.cpu_usage_percent,
        memory_usage_percent=request.memory_usage_percent,
        disk_io_ops_per_sec=0.0,  # Default values
        network_throughput_mbps=0.0,
        alert_frequency_per_day=request.alert_frequency_per_day,
        debugging_time_hours_per_incident=request.debugging_time_hours_per_incident,
        system_downtime_minutes_per_month=request.system_downtime_minutes_per_month,
        infrastructure_cost_per_month=request.infrastructure_cost_per_month,
        engineering_hours_per_month=request.engineering_hours_per_month,
    )

    _success_tracker.set_baseline(baseline)

    logger.info(
        "Performance baseline established: P95=%.1fms, RPS=%.1f, Error=%.2f%%",
        baseline.p95_response_time_ms,
        baseline.requests_per_second,
        baseline.error_rate_percent,
    )

    return {
        "success": True,
        "message": "Performance baseline established successfully",
        "baseline_timestamp": baseline.timestamp.isoformat(),
        "baseline_summary": {
            "p95_response_time_ms": baseline.p95_response_time_ms,
            "requests_per_second": baseline.requests_per_second,
            "error_rate_percent": baseline.error_rate_percent,
            "cpu_usage_percent": baseline.cpu_usage_percent,
            "memory_usage_percent": baseline.memory_usage_percent,
        },
    }


@enhanced_router.get("/success-metrics/report")
async def get_success_metrics_report():
    """
    Get comprehensive success metrics report.

    Returns detailed analysis của performance improvements,
    ROI calculations, và implementation progress.
    """
    report = _success_tracker.generate_success_report()

    # Add real-time enhancements
    if _success_tracker.baseline and _success_tracker.measurements:
        improvements = _success_tracker.calculate_improvements()

        # Calculate summary statistics
        significant_improvements = [
            imp
            for imp in improvements
            if abs(imp.improvement_percent) > 5 and imp.trend == "improving"
        ]

        report["summary"] = {
            "total_metrics_tracked": len(improvements),
            "significant_improvements": len(significant_improvements),
            "metrics_degraded": len(
                [imp for imp in improvements if imp.trend == "degrading"]
            ),
            "average_improvement": sum(
                imp.improvement_percent for imp in significant_improvements
            )
            / len(significant_improvements)
            if significant_improvements
            else 0,
        }

        # ROI calculation (simplified)
        if len(_success_tracker.measurements) > 0:
            try:
                roi_analysis = _success_tracker.calculate_roi(
                    {
                        "development_hours": 240,  # Estimated 6 weeks * 40 hours
                        "infrastructure_costs": 5000,  # Estimated additional costs
                        "training_costs": 2000,  # Training và onboarding
                    }
                )
                report["roi_analysis"] = {
                    "roi_percent": roi_analysis.roi_percent,
                    "payback_period_months": roi_analysis.payback_period_months,
                    "total_savings": roi_analysis.total_savings,
                    "total_investment": roi_analysis.total_investment,
                }
            except Exception as exc:
                logger.warning("ROI calculation failed: %s", exc)
                report["roi_analysis"] = {"error": "ROI calculation not available"}

    return report


@enhanced_router.post("/emergency/enable")
async def enable_emergency_mode():
    """
    Enable emergency mode - disable non-essential performance features.

    Used during critical incidents để ensure system stability
    by disabling ML processing và advanced analytics.
    """
    runtime = get_enhanced_runtime()
    runtime.enable_emergency_mode()

    logger.warning(
        "Emergency mode enabled - non-essential performance features disabled"
    )

    return {
        "success": True,
        "message": "Emergency mode enabled",
        "disabled_features": [
            "ml_optimization",
            "predictive_analysis",
            "auto_optimization",
        ],
        "active_features": [
            "basic_monitoring",
            "enhanced_metrics" if runtime.enhanced_metrics_active else None,
        ],
    }


@enhanced_router.post("/emergency/disable")
async def disable_emergency_mode():
    """
    Disable emergency mode và restore normal operation.

    Restores all configured performance features to their
    normal operational state.
    """
    settings = get_enhanced_settings()
    runtime = get_enhanced_runtime()
    runtime.disable_emergency_mode(settings)

    logger.info("Emergency mode disabled - normal performance monitoring restored")

    return {
        "success": True,
        "message": "Emergency mode disabled - normal operation restored",
        "restored_features": {
            "ml_optimization": runtime.ml_optimization_active,
            "anomaly_detection": runtime.anomaly_detection_active,
            "predictive_analysis": runtime.predictive_analysis_active,
        },
    }


def integrate_with_existing_api(app) -> None:
    """
    Integrate enhanced performance monitoring với existing FastAPI app.

    Args:
        app: FastAPI application instance
    """
    # Add enhanced performance router
    app.include_router(enhanced_router)

    # Initialize enhanced runtime
    from apps.backend.perf.production_config import initialize_enhanced_runtime

    initialize_enhanced_runtime()

    # Setup enhanced instrumentation if available
    try:
        if is_feature_enabled("enhanced_metrics"):
            from apps.backend.perf.enhanced_instrumentation import (
                instrument_fastapi_enhanced,
            )

            instrument_fastapi_enhanced(app)
            logger.info("Enhanced performance instrumentation activated")
        else:
            from apps.backend.perf.instrumentation import instrument_fastapi

            instrument_fastapi(app)
            logger.info("Basic performance instrumentation activated")
    except ImportError as exc:
        logger.warning("Performance instrumentation not available: %s", exc)

    # Setup tracing if enabled
    if is_feature_enabled("distributed_tracing_correlation"):
        try:
            from apps.backend.perf.tracing import setup_tracing

            setup_tracing("zeta_enhanced")
            logger.info("Enhanced distributed tracing activated")
        except ImportError as exc:
            logger.warning("Distributed tracing not available: %s", exc)

    logger.info("Enhanced performance monitoring integration complete")


# Utility function để add vào existing routers
def get_enhanced_performance_router() -> APIRouter:
    """Get the enhanced performance router for manual integration."""
    return enhanced_router
