"""Shim: simple_app moved to `zeta_vn/examples/simple_app_impl.py` to keep dev artifacts separate."""

from apps.backend.examples.simple_app_impl import (
    app,
)  # re-export for backward compatibility

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8001, ws="none", log_level="info")
