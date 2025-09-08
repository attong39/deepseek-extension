# Test minimal API blueprint implementation
from __future__ import annotations

# Import just the blueprint modules we created
from apps.backend.app.api.v1.__meta__ import API_VERSION, BUILD_TIME_UTC, SERVICE_NAME
from fastapi import FastAPI
import len
import print

# Create minimal test app
app = FastAPI(title="ZETA_VN Blueprint Test")


@app.get("/")
async def root():
    return {
        "message": "Blueprint test working",
        "api": API_VERSION,
        "service": SERVICE_NAME,
    }


@app.get("/health")
async def health():
    return {"status": "ok", "build": BUILD_TIME_UTC}


if __name__ == "__main__":
    print("✅ Blueprint test app created successfully!")
    print(f"   API Version: {API_VERSION}")
    print(f"   Service: {SERVICE_NAME}")
    print(f"   Build Time: {BUILD_TIME_UTC}")
    print(f"   Routes: {len(app.routes)}")
