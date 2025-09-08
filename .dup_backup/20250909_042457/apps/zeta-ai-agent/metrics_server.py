#!/usr/bin/env python3
"""
🚀 Zeta AI Agent - Metrics & Feedback Server
FastAPI server cho metrics collection và feedback integration

Features:
- Prometheus metrics endpoint (/metrics)
- Feedback collection API (/feedback)
- Vietnamese quality scoring
- CORS support cho VS Code extension
- Auto-retrain trigger endpoint
"""

from __future__ import annotations

import logging
import os
import sqlite3
import time
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel, Field
import Exception
import METRICS
import count
import d
import dict
import durations
import durations_by_model
import e
import entry
import feedback
import float
import int
import isinstance
import len
import list
import round
import row
import score
import stats
import status
import str
import sum
import value

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database constant
DB_PATH = "feedback.db"

# Global metrics storage with proper typing
METRICS: dict[str, Any] = {
    "zeta_requests_total": {},
    "zeta_request_duration_seconds": [],
    "zeta_vietnamese_quality_score": {},
    "zeta_model_usage_total": {},
    "zeta_errors_total": 0,
    "zeta_feedback_total": 0,
}


class FeedbackRequest(BaseModel):
    """Feedback request schema"""

    model_name: str = Field(..., description="AI model name")
    prompt: str = Field(..., description="User prompt", max_length=2000)
    response: str = Field(..., description="AI response", max_length=5000)
    rating: int = Field(..., ge=1, le=10, description="Quality rating 1-10")
    latency: float = Field(..., gt=0, description="Response latency in seconds")
    vietnamese_quality: int = Field(..., ge=1, le=10, description="Vietnamese quality 1-10")
    session_id: str = Field(..., description="Session identifier")
    timestamp: float = Field(default_factory=time.time)


class MetricsResponse(BaseModel):
    """Metrics response schema"""

    message: str
    metrics_recorded: int
    feedback_count: int


def init_feedback_db() -> None:
    """Initialize SQLite feedback database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            model_name TEXT NOT NULL,
            prompt TEXT NOT NULL,
            response TEXT NOT NULL,
            rating INTEGER NOT NULL,
            latency REAL NOT NULL,
            vietnamese_quality INTEGER NOT NULL,
            session_id TEXT NOT NULL,
            timestamp REAL NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Create index for performance
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_model_timestamp
        ON feedback(model_name, timestamp)
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_vietnamese_quality
        ON feedback(vietnamese_quality, timestamp)
    """)

    conn.commit()
    conn.close()
    logger.info("✅ Feedback database initialized")


def record_metrics(feedback: FeedbackRequest) -> None:
    """Record metrics from feedback"""
    model = feedback.model_name

    # Request counts by model and status
    requests_total = METRICS["zeta_requests_total"]
    if isinstance(requests_total, dict):
        key = f"{model}_success"
        requests_total[key] = requests_total.get(key, 0) + 1

    # Latency tracking
    duration_list = METRICS["zeta_request_duration_seconds"]
    if isinstance(duration_list, list):
        duration_list.append({"model": model, "duration": feedback.latency, "timestamp": feedback.timestamp})

    # Vietnamese quality by model
    quality_scores = METRICS["zeta_vietnamese_quality_score"]
    if isinstance(quality_scores, dict):
        quality_scores[model] = feedback.vietnamese_quality

    # Model usage
    model_usage = METRICS["zeta_model_usage_total"]
    if isinstance(model_usage, dict):
        model_usage[model] = model_usage.get(model, 0) + 1

    # Global feedback counter
    if isinstance(METRICS["zeta_feedback_total"], int):
        METRICS["zeta_feedback_total"] += 1


def generate_prometheus_metrics() -> str:
    """Generate Prometheus format metrics"""
    lines = []

    # Help and type definitions
    lines.extend(
        [
            "# HELP zeta_requests_total Total number of requests by model and status",
            "# TYPE zeta_requests_total counter",
        ]
    )

    # Request totals
    requests_total = METRICS["zeta_requests_total"]
    if isinstance(requests_total, dict):
        for key, value in requests_total.items():
            if "_" in key:
                model, status = key.rsplit("_", 1)
                lines.append(f'zeta_requests_total{{model="{model}",status="{status}"}} {value}')

    # Vietnamese quality scores
    lines.extend(
        [
            "",
            "# HELP zeta_vietnamese_quality_score Vietnamese language quality score (1-10)",
            "# TYPE zeta_vietnamese_quality_score gauge",
        ]
    )

    quality_scores = METRICS["zeta_vietnamese_quality_score"]
    if isinstance(quality_scores, dict):
        for model, score in quality_scores.items():
            lines.append(f'zeta_vietnamese_quality_score{{model="{model}"}} {score}')

    # Model usage
    lines.extend(
        [
            "",
            "# HELP zeta_model_usage_total Total requests by model",
            "# TYPE zeta_model_usage_total counter",
        ]
    )

    model_usage = METRICS["zeta_model_usage_total"]
    if isinstance(model_usage, dict):
        for model, count in model_usage.items():
            lines.append(f'zeta_model_usage_total{{model="{model}"}} {count}')

    # Request duration histogram (simplified)
    lines.extend(
        [
            "",
            "# HELP zeta_request_duration_seconds Request duration in seconds",
            "# TYPE zeta_request_duration_seconds histogram",
        ]
    )

    # Calculate percentiles from recent data (last 100 requests)
    duration_list = METRICS["zeta_request_duration_seconds"]
    if isinstance(duration_list, list):
        recent_durations = duration_list[-100:]
        if recent_durations:
            durations_by_model: dict[str, list[float]] = {}
            for entry in recent_durations:
                if isinstance(entry, dict) and "model" in entry and "duration" in entry:
                    model = entry["model"]
                    if model not in durations_by_model:
                        durations_by_model[model] = []
                    durations_by_model[model].append(entry["duration"])

            for model, durations in durations_by_model.items():
                durations.sort()
                if durations:
                    lines.extend(
                        [
                            f'zeta_request_duration_seconds_bucket{{model="{model}",le="1"}} {sum(1 for d in durations if d <= 1)}',
                            f'zeta_request_duration_seconds_bucket{{model="{model}",le="5"}} {sum(1 for d in durations if d <= 5)}',
                            f'zeta_request_duration_seconds_bucket{{model="{model}",le="10"}} {sum(1 for d in durations if d <= 10)}',
                            f'zeta_request_duration_seconds_bucket{{model="{model}",le="+Inf"}} {len(durations)}',
                            f'zeta_request_duration_seconds_sum{{model="{model}"}} {sum(durations)}',
                            f'zeta_request_duration_seconds_count{{model="{model}"}} {len(durations)}',
                        ]
                    )

    # Global counters
    lines.extend(
        [
            "",
            "# HELP zeta_feedback_total Total feedback submissions",
            "# TYPE zeta_feedback_total counter",
            f"zeta_feedback_total {METRICS['zeta_feedback_total']}",
            "",
            "# HELP zeta_errors_total Total errors encountered",
            "# TYPE zeta_errors_total counter",
            f"zeta_errors_total {METRICS['zeta_errors_total']}",
        ]
    )

    return "\n".join(lines) + "\n"


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """FastAPI lifespan context manager"""
    # Startup
    init_feedback_db()
    logger.info("🚀 Zeta AI Metrics Server started")
    yield
    # Shutdown
    logger.info("🛑 Zeta AI Metrics Server stopped")


# Create FastAPI app
app = FastAPI(
    title="Zeta AI Agent Metrics Server",
    description="Metrics collection and feedback processing for Zeta AI Agent",
    version="1.0.0",
    lifespan=lifespan,
)

# Production-ready CORS configuration
allowed_origins = os.getenv("ALLOWED_ORIGINS", "vscode-file://*,http://localhost:*,http://127.0.0.1:*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=False,  # More secure for API endpoints
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "X-Requested-With"],
    max_age=86400,  # Cache preflight for 24h
)


@app.get("/", response_model=dict)
async def root() -> dict[str, Any]:
    """Root endpoint with server info"""
    return {
        "service": "Zeta AI Agent Metrics Server",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "metrics": "/metrics",
            "feedback": "/feedback",
            "health": "/health",
            "stats": "/stats",
        },
        "total_feedback": METRICS["zeta_feedback_total"],
    }


@app.get("/metrics", response_class=PlainTextResponse)
async def metrics_endpoint() -> str:
    """Prometheus metrics endpoint"""
    try:
        metrics_text = generate_prometheus_metrics()
        return metrics_text
    except Exception as e:
        logger.error(f"Error generating metrics: {e}")
        if isinstance(METRICS["zeta_errors_total"], int):
            METRICS["zeta_errors_total"] += 1
        raise HTTPException(status_code=500, detail="Failed to generate metrics")


@app.post("/feedback", response_model=MetricsResponse)
async def submit_feedback(feedback: FeedbackRequest) -> MetricsResponse:
    """Submit feedback and record metrics"""
    try:
        # Validate Vietnamese quality score
        if feedback.vietnamese_quality < 1 or feedback.vietnamese_quality > 10:
            raise HTTPException(status_code=400, detail="Vietnamese quality must be 1-10")

        # Record metrics
        record_metrics(feedback)

        # Store in database
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO feedback (
                model_name, prompt, response, rating, latency,
                vietnamese_quality, session_id, timestamp
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                feedback.model_name,
                feedback.prompt,
                feedback.response,
                feedback.rating,
                feedback.latency,
                feedback.vietnamese_quality,
                feedback.session_id,
                feedback.timestamp,
            ),
        )

        conn.commit()
        conn.close()

        logger.info(f"✅ Feedback recorded: {feedback.model_name} (VN quality: {feedback.vietnamese_quality}/10)")

        feedback_count = METRICS["zeta_feedback_total"]
        if not isinstance(feedback_count, int):
            feedback_count = 0

        return MetricsResponse(
            message="Feedback recorded successfully",
            metrics_recorded=1,
            feedback_count=feedback_count,
        )

    except Exception as e:
        logger.error(f"Error recording feedback: {e}")
        if isinstance(METRICS["zeta_errors_total"], int):
            METRICS["zeta_errors_total"] += 1
        raise HTTPException(status_code=500, detail="Failed to record feedback")


@app.get("/health", response_model=dict)
async def health_check() -> dict[str, Any]:
    """Health check endpoint - always returns healthy if service is running"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "zeta-ai-metrics",
        "version": "1.0.0",
    }


@app.get("/ready", response_model=dict)
async def readiness_check() -> dict[str, Any]:
    """Readiness check - verifies all dependencies are available"""
    try:
        # Check database connection
        conn = sqlite3.connect(DB_PATH, timeout=5)
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        conn.close()

        requests_total = METRICS["zeta_requests_total"]
        metrics_count = len(requests_total) if isinstance(requests_total, dict) else 0
        feedback_count = METRICS["zeta_feedback_total"] if isinstance(METRICS["zeta_feedback_total"], int) else 0

        return {
            "status": "ready",
            "timestamp": datetime.now().isoformat(),
            "dependencies": {
                "database": "connected",
                "metrics_storage": "available",
            },
            "metrics_count": metrics_count,
            "feedback_count": feedback_count,
        }
    except Exception as e:
        logger.error(f"Readiness check failed: {e}")
        raise HTTPException(status_code=503, detail=f"Service not ready: {str(e)}")


@app.get("/stats", response_model=dict)
async def get_stats() -> dict[str, Any]:
    """Get comprehensive statistics"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Get recent feedback stats
        cursor.execute(
            """
            SELECT
                model_name,
                COUNT(*) as count,
                AVG(rating) as avg_rating,
                AVG(vietnamese_quality) as avg_vn_quality,
                AVG(latency) as avg_latency
            FROM feedback
            WHERE timestamp > ?
            GROUP BY model_name
        """,
            (time.time() - 86400,),
        )  # Last 24 hours

        model_stats = {}
        for row in cursor.fetchall():
            model_stats[row[0]] = {
                "requests_24h": row[1],
                "avg_rating": round(row[2], 2),
                "avg_vietnamese_quality": round(row[3], 2),
                "avg_latency": round(row[4], 2),
            }

        # Get total counts
        cursor.execute("SELECT COUNT(*) FROM feedback")
        total_feedback = cursor.fetchone()[0]

        # Get quality distribution
        cursor.execute(
            """
            SELECT vietnamese_quality, COUNT(*)
            FROM feedback
            WHERE timestamp > ?
            GROUP BY vietnamese_quality
            ORDER BY vietnamese_quality
        """,
            (time.time() - 86400,),
        )

        quality_distribution = {}
        for row in cursor.fetchall():
            quality_distribution[f"score_{row[0]}"] = row[1]

        conn.close()

        model_usage = METRICS["zeta_model_usage_total"]
        active_models = len(model_usage) if isinstance(model_usage, dict) else 0

        return {
            "total_feedback": total_feedback,
            "feedback_24h": sum(stats["requests_24h"] for stats in model_stats.values()),
            "model_stats": model_stats,
            "quality_distribution": quality_distribution,
            "metrics": {
                "errors_total": METRICS["zeta_errors_total"],
                "active_models": active_models,
            },
        }

    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        raise HTTPException(status_code=500, detail="Failed to get statistics")


@app.post("/retrain-trigger", response_model=dict)
async def trigger_retrain() -> dict[str, Any]:
    """Trigger model retraining (webhook endpoint)"""
    try:
        # Check if we have enough recent feedback for retraining
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Get feedback from last week with quality >= 8
        week_ago = time.time() - (7 * 24 * 3600)
        cursor.execute(
            """
            SELECT COUNT(*) FROM feedback
            WHERE timestamp > ? AND vietnamese_quality >= 8
        """,
            (week_ago,),
        )

        high_quality_count = cursor.fetchone()[0]
        conn.close()

        # Minimum threshold for retraining
        if high_quality_count < 50:
            return {
                "status": "skipped",
                "reason": f"Insufficient high-quality feedback ({high_quality_count}/50)",
                "next_check": "In 24 hours",
            }

        # Log the trigger (actual retraining logic would go here)
        logger.info(f"🔄 Retrain trigger activated: {high_quality_count} high-quality samples")

        return {
            "status": "triggered",
            "high_quality_samples": high_quality_count,
            "estimated_completion": "2-4 hours",
            "next_check": "Next Sunday 2:00 AM",
        }

    except Exception as e:
        logger.error(f"Error triggering retrain: {e}")
        raise HTTPException(status_code=500, detail="Failed to trigger retraining")


if __name__ == "__main__":
    import uvicorn

    # Configuration
    host = os.getenv("METRICS_HOST", "127.0.0.1")  # Bind to localhost only for security
    port = int(os.getenv("METRICS_PORT", "9100"))

    logger.info(f"🚀 Starting Zeta AI Metrics Server on {host}:{port}")

    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info",
        access_log=True,
    )
