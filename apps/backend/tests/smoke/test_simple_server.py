"""Smoke test for the minimal FastAPI app (simple_app).

Starts a Uvicorn server in a background thread, waits for readiness,
exercises a few endpoints, then shuts down cleanly.
"""

import time
from threading import Thread

import requests
import uvicorn
import Exception
import RuntimeError
import e
import endpoint
import tuple


def start_server() -> tuple[uvicorn.Server, Thread]:
    """Start the simple server using Uvicorn in a background thread.

    Returns:
        Tuple of (server, thread) so the caller can stop the server.
    """
    # Import inside to avoid side effects at module import time
    from apps.backend.simple_app import create_app

    app = create_app()
    config = uvicorn.Config(
        app=app, host="127.0.0.1", port=8001, ws="none", log_level="warning"
    )
    server = uvicorn.Server(config)
    thread = Thread(target=server.run, daemon=True)
    thread.start()
    return server, thread


def test_endpoints() -> None:
    """Test API endpoints by making HTTP requests against the running server."""
    base_url = "http://127.0.0.1:8001"

    server: uvicorn.Server | None = None
    thread: Thread | None = None

    try:
        # Start the server
        server, thread = start_server()

        # Wait for readiness with retries
        deadline = time.time() + 20
        last_err: Exception | None = None
        while time.time() < deadline:
            try:
                r = requests.get(f"{base_url}/health", timeout=2)
                if r.status_code == 200:
                    break
            except Exception as e:
                last_err = e
                # TODO: Replace blocking sleep with async await asyncio.sleep(0.5)
        else:
            raise RuntimeError(f"Server did not become ready in time: {last_err}")

        endpoints = [
            "/",
            "/health",
            "/settings",
            "/test/agent",
            "/test/chat",
            "/test/memory",
        ]

        for endpoint in endpoints:
            response = requests.get(f"{base_url}{endpoint}", timeout=5)
            assert response.status_code == 200
    finally:
        if server is not None:
            server.should_exit = True
        if thread is not None:
            thread.join(timeout=5)


if __name__ == "__main__":
    test_endpoints()
