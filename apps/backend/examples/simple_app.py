"""Simple FastAPI app for smoke tests (moved to examples/).

This file was moved from project root to examples to separate dev artifacts from main code.
"""

from apps.backend.examples.simple_app_impl import app

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8001, ws="none", log_level="info")
