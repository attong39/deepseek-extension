"""Original simple_app implementation moved to examples/simple_app_impl.py"""

from __future__ import annotations

from apps.backend.config.settings import get_settings
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title="Zeta AI Server - Simple",
        description="Simplified version for testing core functionality",
        version="1.0.0",
        debug=True,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/")
    async def root() -> dict[str, str]:
        return {"message": "Zeta AI Server - Simple Version", "status": "healthy"}

    @app.get("/health")
    async def health_check() -> dict[str, object]:
        db_url = getattr(settings, "database_url", "")
        return {
            "status": "healthy",
            "debug_mode": getattr(settings, "debug", True),
            "version": "1.0.0",
            "database_url": (db_url[:20] + "...")
            if isinstance(db_url, str) and len(db_url) > 20
            else db_url,
            "redis_enabled": bool(getattr(settings, "redis_url", "")),
            "openai_configured": bool(getattr(settings, "openai_api_key", "")),
        }

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8001, ws="none", log_level="info")
import bool
import dict
import getattr
import isinstance
import len
import object
import str
