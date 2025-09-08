#!/usr/bin/env python3
# 🚀 Zeta AI Agent Local Development Server

import asyncio
import os
import sqlite3
import time
from collections import deque
from contextlib import asynccontextmanager
from datetime import UTC, datetime
from threading import RLock
from typing import Any

import psutil
import requests
import structlog
import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, PlainTextResponse
from prometheus_client import Counter, Gauge, Histogram, generate_latest
from pydantic import BaseModel, Field
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
import Exception
import ImportError
import ai_request
import call_next
import conn
import count
import dict
import e
import exc
import feedback
import float
import int
import len
import list
import maxsize
import metric
import model
import print
import prompt
import request
import self
import str

# Import our optimized configuration
try:
    from config.settings import get_environment_settings

    settings = get_environment_settings()
except ImportError:
    # Fallback configuration for development
    class DevSettings:
        environment = "development"
        debug = True
        version = "1.0.0-dev"

        class Server:
            host = "127.0.0.1"
            port = 9100
            log_level = "DEBUG"

        class CORS:
            allowed_origins = [
                "http://localhost:3000",
                "http://127.0.0.1:3000",
                "vscode-webview:*",
                "https://vscode-webview.net",
            ]
            allow_credentials = False
            allowed_methods = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
            allowed_headers = ["*"]
            max_age = 86400

        class Security:
            rate_limit_requests = 1000
            max_prompt_length = 5000
            max_response_length = 10000

        class Database:
            url = "sqlite:///zeta_feedback_dev.db"
            timeout = 30

        def __init__(self) -> None:
            self.server = self.Server()
            self.cors = self.CORS()
            self.security = self.Security()
            self.database = self.Database()

    settings = DevSettings()

# Initialize logger
logger = structlog.get_logger()

# Create custom registry to avoid conflicts
from prometheus_client import CollectorRegistry

custom_registry = CollectorRegistry()

# Prometheus metrics
REQUEST_COUNT = Counter(
    "zeta_dev_requests_total", "Total requests", ["method", "endpoint", "status"], registry=custom_registry
)
REQUEST_DURATION = Histogram(
    "zeta_dev_request_duration_seconds", "Request duration", ["endpoint"], registry=custom_registry
)
MEMORY_USAGE = Gauge("zeta_dev_memory_usage_bytes", "Memory usage in bytes", registry=custom_registry)
CPU_USAGE = Gauge("zeta_dev_cpu_usage_percent", "CPU usage percentage", registry=custom_registry)
ACTIVE_CONNECTIONS = Gauge("zeta_dev_active_connections", "Active connections", registry=custom_registry)
ERROR_COUNT = Counter("zeta_dev_errors_total", "Total errors", ["error_type"], registry=custom_registry)

# Rate limiter with generous limits for development
limiter = Limiter(key_func=get_remote_address)

# Ollama Turbo API configuration
OLLAMA_API_KEY = os.getenv("OLLAMA_TURBO_API_KEY")
OLLAMA_BASE_URL = os.getenv("OLLAMA_TURBO_BASE_URL", "https://api.ollama.ai/v1")
OLLAMA_MODEL = os.getenv("OLLAMA_TURBO_MODEL", "turbo")
OLLAMA_MAX_TOKENS = int(os.getenv("OLLAMA_TURBO_MAX_TOKENS", "4096"))
OLLAMA_TEMPERATURE = float(os.getenv("OLLAMA_TURBO_TEMPERATURE", "0.7"))
OLLAMA_TIMEOUT = int(os.getenv("OLLAMA_TURBO_TIMEOUT", "30"))


def call_ollama_turbo_api(prompt: str, model: str | None = None) -> dict[str, Any] | None:
    """Call Ollama Turbo API for AI responses"""
    if not OLLAMA_API_KEY:
        logger.warning("Ollama Turbo API key not configured, using mock response")
        return None

    try:
        headers = {"Authorization": f"Bearer {OLLAMA_API_KEY}", "Content-Type": "application/json"}

        payload = {
            "model": model or OLLAMA_MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": OLLAMA_MAX_TOKENS,
            "temperature": OLLAMA_TEMPERATURE,
        }

        response = requests.post(
            f"{OLLAMA_BASE_URL}/chat/completions", headers=headers, json=payload, timeout=OLLAMA_TIMEOUT
        )

        if response.status_code == 200:
            data = response.json()
            return {
                "response": data["choices"][0]["message"]["content"],
                "model": data["model"],
                "tokens_used": data.get("usage", {}).get("total_tokens", 0),
                "finish_reason": data["choices"][0].get("finish_reason", "completed"),
            }
        else:
            logger.error(f"Ollama API error: {response.status_code} - {response.text}")
            return None

    except Exception as e:
        logger.error(f"Ollama API call failed: {e}")
        return None


# Simple in-memory storage for development
dev_feedback_storage = deque(maxlen=1000)
dev_metrics_buffer = deque(maxlen=5000)


class CircularMetricsBuffer:
    """Lightweight metrics buffer for development"""

    def __init__(self, maxsize: int = 5000):
        self.buffer = deque(maxlen=maxsize)
        self.lock = RLock()

    def add_metric(self, metric: dict) -> None:
        with self.lock:
            metric["timestamp"] = time.time()
            self.buffer.append(metric)

    def get_recent_metrics(self, count: int = 100) -> list[dict]:
        with self.lock:
            return list(self.buffer)[-count:]

    def get_stats(self) -> dict:
        with self.lock:
            return {"count": len(self.buffer), "memory_usage_mb": len(str(self.buffer)) / (1024 * 1024)}


# Global instances
metrics_buffer = CircularMetricsBuffer()


# Pydantic models
class FeedbackRequest(BaseModel):
    model_name: str = Field(..., max_length=50, description="AI model name")
    prompt: str = Field(..., max_length=settings.security.max_prompt_length, description="User prompt")
    response: str = Field(..., max_length=settings.security.max_response_length, description="AI response")
    rating: int = Field(..., ge=1, le=10, description="Rating from 1-10")
    latency: float = Field(..., gt=0, le=300, description="Response latency in seconds")
    vietnamese_quality: int = Field(..., ge=1, le=10, description="Vietnamese quality rating")
    session_id: str = Field(..., max_length=50, description="Session identifier")


class AIRequest(BaseModel):
    prompt: str = Field(..., max_length=5000, description="User prompt")
    model: str = Field(default="default", max_length=50, description="Model to use")
    session_id: str = Field(..., max_length=50, description="Session identifier")


class AIResponse(BaseModel):
    response: str
    model_used: str
    latency: float
    session_id: str


# Initialize database for development
def init_dev_database():
    """Initialize SQLite database for development"""
    try:
        db_path = settings.database.url.replace("sqlite:///", "")
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        with sqlite3.connect(db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS feedback (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    model_name TEXT NOT NULL,
                    prompt TEXT,
                    response TEXT,
                    rating INTEGER,
                    latency REAL,
                    vietnamese_quality INTEGER,
                    session_id TEXT,
                    timestamp REAL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_feedback_timestamp 
                ON feedback(timestamp)
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_feedback_model 
                ON feedback(model_name)
            """)
            conn.commit()
            logger.info("Development database initialized", db_path=db_path)
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management"""
    # Startup
    logger.info(
        "🚀 Starting Zeta AI Agent Development Server", version=settings.version, environment=settings.environment
    )

    # Initialize database
    init_dev_database()

    # Start metrics collection
    async def collect_dev_metrics():
        while True:
            try:
                process = psutil.Process()
                memory_info = process.memory_info()
                MEMORY_USAGE.set(memory_info.rss)
                CPU_USAGE.set(process.cpu_percent())
                await asyncio.sleep(30)
            except Exception as e:
                logger.error(f"Metrics collection error: {e}")
                await asyncio.sleep(60)

    metrics_task = asyncio.create_task(collect_dev_metrics())

    yield

    # Shutdown
    logger.info("🛑 Shutting down development server")
    metrics_task.cancel()
    try:
        await metrics_task
    except asyncio.CancelledError:
        pass


# Initialize FastAPI app
app = FastAPI(
    title="Zeta AI Agent - Development Server",
    description="Local development server with hot reload and debugging",
    version=settings.version,
    debug=settings.debug,
    lifespan=lifespan,
)

# Add CORS middleware with permissive settings for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors.allowed_origins,
    allow_credentials=settings.cors.allow_credentials,
    allow_methods=settings.cors.allowed_methods,
    allow_headers=settings.cors.allowed_headers,
    max_age=settings.cors.max_age,
)


# Rate limiting error handler
@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    logger.warning(f"Rate limit exceeded for {request.client.host}")
    return JSONResponse(status_code=429, content={"detail": f"Rate limit exceeded: {exc.detail}"})


# Middleware for request metrics and logging
@app.middleware("http")
async def dev_middleware(request: Request, call_next):
    start_time = time.time()

    # Log incoming requests in development
    logger.info(
        f"📨 {request.method} {request.url.path}", client=str(request.client.host) if request.client else "unknown"
    )

    response = await call_next(request)

    # Record metrics
    duration = time.time() - start_time
    REQUEST_DURATION.labels(endpoint=request.url.path).observe(duration)
    REQUEST_COUNT.labels(method=request.method, endpoint=request.url.path, status=response.status_code).inc()

    # Log response in development
    logger.info(f"📤 {response.status_code} ({duration:.3f}s)")

    return response


@app.get("/")
async def root():
    """Root endpoint with development info"""
    return {
        "name": "Zeta AI Agent Development Server",
        "version": settings.version,
        "environment": settings.environment,
        "debug": settings.debug,
        "endpoints": {
            "health": "/health",
            "metrics": "/metrics",
            "feedback": "/feedback",
            "ai_chat": "/api/ask",
            "stats": "/stats",
            "dev_info": "/dev",
        },
        "timestamp": datetime.now(UTC).isoformat(),
    }


@app.get("/health")
async def health_check():
    """Basic health check"""
    return {
        "status": "healthy",
        "environment": settings.environment,
        "debug": settings.debug,
        "timestamp": datetime.now(UTC).isoformat(),
    }


@app.get("/health/detailed")
async def detailed_health_check():
    """Detailed health check for development"""
    try:
        # Check database
        db_path = settings.database.url.replace("sqlite:///", "")
        db_ok = os.path.exists(db_path)

        # System metrics
        memory_percent = psutil.virtual_memory().percent
        cpu_percent = psutil.cpu_percent()
        disk_percent = psutil.disk_usage(".").percent

        buffer_stats = metrics_buffer.get_stats()

        return {
            "status": "healthy",
            "environment": settings.environment,
            "checks": {
                "database": db_ok,
                "memory_ok": memory_percent < 90,
                "cpu_ok": cpu_percent < 90,
                "disk_ok": disk_percent < 90,
            },
            "metrics": {
                "memory_percent": memory_percent,
                "cpu_percent": cpu_percent,
                "disk_percent": disk_percent,
                "buffer_count": buffer_stats["count"],
                "buffer_memory_mb": buffer_stats["memory_usage_mb"],
            },
            "timestamp": datetime.now(UTC).isoformat(),
        }
    except Exception as e:
        logger.error(f"Health check error: {e}")
        raise HTTPException(status_code=503, detail="Health check failed")


@app.post("/feedback")
@limiter.limit(f"{settings.security.rate_limit_requests}/minute")
async def submit_feedback(request: Request, feedback: FeedbackRequest):
    """Submit feedback with development logging"""
    try:
        logger.info(
            "📝 Feedback received", model=feedback.model_name, rating=feedback.rating, session=feedback.session_id
        )

        # Store in memory for development
        feedback_data = feedback.model_dump()
        feedback_data["timestamp"] = time.time()
        dev_feedback_storage.append(feedback_data)
        metrics_buffer.add_metric(feedback_data)

        # Also store in database
        db_path = settings.database.url.replace("sqlite:///", "")
        with sqlite3.connect(db_path, timeout=settings.database.timeout) as conn:
            conn.execute(
                """
                INSERT INTO feedback 
                (model_name, prompt, response, rating, latency, vietnamese_quality, session_id, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    feedback.model_name,
                    feedback.prompt[:1000],
                    feedback.response[:2000],
                    feedback.rating,
                    feedback.latency,
                    feedback.vietnamese_quality,
                    feedback.session_id,
                    time.time(),
                ),
            )
            conn.commit()

        return {
            "status": "success",
            "message": "Feedback recorded in development mode",
            "debug_info": {"stored_in_memory": True, "stored_in_db": True, "total_feedback": len(dev_feedback_storage)},
        }

    except Exception as e:
        logger.error(f"Feedback submission error: {e}")
        ERROR_COUNT.labels(error_type="feedback_submission").inc()
        raise HTTPException(status_code=500, detail=f"Failed to record feedback: {str(e)}")


@app.post("/api/ask")
@limiter.limit("500/minute")  # Generous for development
async def ai_chat(request: Request, ai_request: AIRequest):
    """AI chat endpoint for extension integration"""
    try:
        logger.info(
            "🤖 AI request received",
            model=ai_request.model,
            prompt_length=len(ai_request.prompt),
            session=ai_request.session_id,
        )

        start_time = time.time()

        # Try to get real AI response from Ollama Turbo
        ollama_result = call_ollama_turbo_api(ai_request.prompt, ai_request.model)

        if ollama_result:
            # Use real AI response
            ai_response = ollama_result["response"]
            model_used = ollama_result["model"]
            tokens_used = ollama_result.get("tokens_used", 0)
            logger.info("🤖 Real AI response from Ollama Turbo", model=model_used, tokens_used=tokens_used)
        else:
            # Fallback to mock response
            ai_response = f"""# AI Response (Development Mode - API Unavailable)

**Model**: {ai_request.model}
**Session**: {ai_request.session_id}
**Timestamp**: {datetime.now(UTC).isoformat()}

## Your Question:
{ai_request.prompt[:500]}{'...' if len(ai_request.prompt) > 500 else ''}

## Mock Response:
Ollama Turbo API is not available. This is a development mock response from Zeta AI Agent.

### Possible Issues:
- API key not configured correctly
- Network connectivity issues
- Ollama Turbo service unavailable
- Invalid model configuration

### Check Configuration:
- OLLAMA_TURBO_API_KEY: {'✅ Set' if OLLAMA_API_KEY else '❌ Missing'}
- OLLAMA_TURBO_BASE_URL: {OLLAMA_BASE_URL}
- OLLAMA_TURBO_MODEL: {OLLAMA_MODEL}

**Development Server Status**: ✅ Active (Mock Mode)
"""
            model_used = ai_request.model
            logger.warning("🤖 Using mock response - Ollama Turbo API unavailable")

        latency = time.time() - start_time

        # Store interaction for development
        interaction = {
            "prompt": ai_request.prompt,
            "response": ai_response,
            "model": model_used,
            "session_id": ai_request.session_id,
            "latency": latency,
            "timestamp": time.time(),
        }
        dev_metrics_buffer.append(interaction)

        response = AIResponse(
            response=ai_response, model_used=model_used, latency=latency, session_id=ai_request.session_id
        )

        logger.info("🤖 AI response sent", latency=f"{latency:.3f}s", response_length=len(ai_response))

        return response

    except Exception as e:
        logger.error(f"AI chat error: {e}")
        ERROR_COUNT.labels(error_type="ai_chat").inc()
        raise HTTPException(status_code=500, detail=f"AI processing failed: {str(e)}")


@app.get("/metrics")
async def get_prometheus_metrics():
    """Prometheus metrics endpoint"""
    return PlainTextResponse(generate_latest(custom_registry))


@app.get("/stats")
async def get_dev_stats():
    """Development statistics"""
    try:
        recent_feedback = list(dev_feedback_storage)[-10:]
        recent_interactions = list(dev_metrics_buffer)[-10:]

        return {
            "development_mode": True,
            "total_feedback": len(dev_feedback_storage),
            "total_interactions": len(dev_metrics_buffer),
            "recent_feedback": recent_feedback,
            "recent_interactions": recent_interactions,
            "system_stats": {
                "memory_percent": psutil.virtual_memory().percent,
                "cpu_percent": psutil.cpu_percent(),
                "disk_percent": psutil.disk_usage(".").percent,
            },
            "buffer_stats": metrics_buffer.get_stats(),
            "timestamp": datetime.now(UTC).isoformat(),
        }
    except Exception as e:
        logger.error(f"Stats error: {e}")
        raise HTTPException(status_code=500, detail="Failed to get stats")


@app.get("/dev")
async def dev_info():
    """Development server information"""
    return {
        "server_info": {
            "name": "Zeta AI Agent Development Server",
            "version": settings.version,
            "environment": settings.environment,
            "debug": settings.debug,
            "pid": os.getpid(),
        },
        "configuration": {
            "host": settings.server.host,
            "port": settings.server.port,
            "cors_origins": settings.cors.allowed_origins,
            "rate_limit": settings.security.rate_limit_requests,
            "database": settings.database.url,
        },
        "endpoints": {
            "Root": "/",
            "Health": "/health",
            "Detailed Health": "/health/detailed",
            "Submit Feedback": "POST /feedback",
            "AI Chat": "POST /api/ask",
            "Metrics": "/metrics",
            "Stats": "/stats",
            "Dev Info": "/dev",
        },
        "development_features": {
            "hot_reload": True,
            "detailed_logging": True,
            "in_memory_storage": True,
            "mock_ai_responses": True,
            "generous_rate_limits": True,
            "permissive_cors": True,
        },
    }


if __name__ == "__main__":
    # Development server startup
    print("🚀 Starting Zeta AI Agent Development Server")
    print(f"📍 Environment: {settings.environment}")
    print(f"🌐 URL: http://{settings.server.host}:{settings.server.port}")
    print(f"🔧 Debug: {settings.debug}")
    print("📋 Available endpoints:")
    print("   • GET  /          - Server info")
    print("   • GET  /health    - Health check")
    print("   • POST /feedback  - Submit feedback")
    print("   • POST /api/ask   - AI chat")
    print("   • GET  /metrics   - Prometheus metrics")
    print("   • GET  /stats     - Development stats")
    print("   • GET  /dev       - Development info")
    print("\n💡 Tips:")
    print("   • Use Ctrl+C to stop the server")
    print("   • Server will auto-reload on code changes")
    print("   • Check /dev endpoint for configuration details")
    print("   • VS Code extension should connect automatically")

    uvicorn.run(
        "dev_server:app",
        host=settings.server.host,
        port=settings.server.port,
        reload=True,
        log_level=settings.server.log_level.lower(),
        access_log=True,
    )
