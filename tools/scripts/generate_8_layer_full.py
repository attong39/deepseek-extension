from __future__ import annotations

import sys
from pathlib import Path
import STRUCTURE_MAP
import base_path
import dict
import f
import file_name
import file_path
import files
import len
import list
import open
import print
import root_dir
import str

"""
Script tạo cấu trúc 8-layer architecture hoàn chỉnh cho zeta_vn
Tích hợp DDD + Clean Architecture + One-Click Learning + FastAPI
"""
STRUCTURE_MAP: dict[str, list[str]] = {
    "zeta_vn": [
        "__init__.py",
        "core/application/__init__.py",
        "core/application/ports/__init__.py",
        "core/application/ports/vector_store.py",
        "core/application/use_cases/__init__.py",
        "core/application/use_cases/train_pipeline.py",
        "core/application/use_cases/rag_search.py",
        "core/domain/__init__.py",
        "core/domain/entities.py",
        "core/domain/events.py",
        "core/domain/value_objects.py",
        "application/__init__.py",
        "application/api/__init__.py",
        "application/api/main.py",
        "application/api/v1/__init__.py",
        "application/api/v1/endpoints/__init__.py",
        "application/api/v1/endpoints/health.py",
        "application/api/v1/endpoints/documents.py",
        "application/api/v1/endpoints/training.py",
        "application/api/v1/endpoints/rag.py",
        "application/api/v1/schemas/__init__.py",
        "application/api/v1/schemas/documents.py",
        "application/api/v1/schemas/training.py",
        "application/api/v1/schemas/rag.py",
        "application/api/v1/dependencies/__init__.py",
        "application/api/v1/dependencies/auth.py",
        "application/api/v1/dependencies/rate_limit.py",
        "application/ws/__init__.py",
        "application/ws/manager.py",
        "application/ws/progress.py",
        "application/orchestrator/__init__.py",
        "application/orchestrator/workflow_orchestrator.py",
        "infrastructure/__init__.py",
        "infrastructure/config/__init__.py",
        "infrastructure/config/settings.py",
        "infrastructure/config/logging.py",
        "infrastructure/database/__init__.py",
        "infrastructure/database/connection.py",
        "infrastructure/database/models.py",
        "infrastructure/cache/__init__.py",
        "infrastructure/cache/redis.py",
        "infrastructure/cache/memory.py",
        "infrastructure/storage/__init__.py",
        "infrastructure/storage/local_storage.py",
        "infrastructure/storage/cloud_storage.py",
        "infrastructure/clients/__init__.py",
        "infrastructure/clients/openai_client.py",
        "infrastructure/clients/github_client.py",
        "protocols/__init__.py",
        "protocols/http/__init__.py",
        "protocols/http/client.py",
        "protocols/websocket/__init__.py",
        "protocols/websocket/handler.py",
        "protocols/serialization/__init__.py",
        "protocols/serialization/json_serializer.py",
        "cognition/__init__.py",
        "cognition/planning/__init__.py",
        "cognition/planning/task_planner.py",
        "cognition/algorithms/__init__.py",
        "cognition/algorithms/chunkers.py",
        "memory/__init__.py",
        "memory/vector_store/__init__.py",
        "memory/vector_store/faiss_store.py",
        "memory/vector_store/pgvector_store.py",
        "memory/session/__init__.py",
        "memory/session/session_store.py",
        "ops/__init__.py",
        "ops/monitoring/__init__.py",
        "ops/monitoring/metrics.py",
        "ops/logging/__init__.py",
        "ops/logging/audit.py",
        "ops/security/__init__.py",
        "ops/security/pii_mask.py",
        "ops/security/rate_limit.py",
    ],
    "scripts": [
        "generate_project_map.py",
        "migrate.py",
        "quality/quality_gates.sh",
        "quality/quality_gates.ps1",
    ],
    "tests": [
        "__init__.py",
        "unit/__init__.py",
        "unit/test_health.py",
        "unit/test_train_pipeline.py",
        "integration/__init__.py",
        "integration/test_rag_api.py",
        "e2e/__init__.py",
        "e2e/test_full_workflow.py",
    ],
    "docs": [
        "PROJECT_FILE_MAP_FUNCTIONS.md",
        "architecture/overview.md",
        "api/v1/endpoints.md",
        "examples/basic_usage.md",
    ],
    ".github/workflows": [
        "ci.yml",
        "cd.yml",
        "quality_gates.yml",
    ],
}
TEMPLATES = {
    "pyproject.toml": """[project]
name = "zeta_vn"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
  "fastapi>=0.115",
  "uvicorn[standard]>=0.30",
  "pydantic>=2.8",
  "pydantic-settings>=2.4",
  "sqlmodel>=0.0.21",
  "prometheus-fastapi-instrumentator>=7.0",
  "python-multipart>=0.0.9",
  "httpx>=0.27",
  "redis>=5.0",
  "psycopg[binary]>=3.2",
  "numpy>=1.26",
  "scikit-learn>=1.4",
  "faiss-cpu>=1.8; platform_machine != 'aarch64'",
  "pgvector>=0.3"
]
[tool.uv]
index-url = "https://pypi.org/simple"
[tool.pytest.ini_options]
addopts = "-q"
[build-system]
requires = ["setuptools", "wheel"]
build-backend = "setuptools.build_meta"
""",
    "ruff.toml": """line-length = 100
target-version = "py311"
select = ["E","F","I","B","C90"]
ignore = []
""",
    "mypy.ini": """[mypy]
python_version = 3.11
strict = True
exclude = (tests/|build/)
""",
    "pytest.ini": """[pytest]
testpaths = tests
""",
    ".env.example": """DATABASE_URL=sqlite:///./zeta.db
CORS_ALLOW_ORIGINS=*
REDIS_URL=redis://localhost:6379
""",
    "zeta_vn/application/api/main.py": """from __future__ import annotations
@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
app = FastAPI(title="ZETA_AI Server", version="0.1.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(health.router, prefix="/api/v1", tags=["health"])
app.include_router(documents.router, prefix="/api/v1", tags=["documents"])
app.include_router(training.router, prefix="/api/v1", tags=["training"])
app.include_router(rag.router, prefix="/api/v1", tags=["rag"])
app.include_router(ws_router, prefix="/ws")
Instrumentator().instrument(app).expose(app)
""",
    "zeta_vn/application/api/v1/endpoints/health.py": '''from fastapi import APIRouter
router = APIRouter()
@router.get("/health")
def health():
    """Health check endpoint"""
    return {"status": "ok", "service": "zeta_ai"}
''',
    "zeta_vn/infrastructure/config/settings.py": '''from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    """Application settings with environment variable support"""
    cors_allow_origins: list[str] = ["*"]
    database_url: str = "sqlite:///./zeta.db"
    redis_url: str | None = None
    model_config = {"env_file": ".env"}
settings = Settings()
''',
    "zeta_vn/core/application/ports/vector_store.py": '''from __future__ import annotations
class VectorStore(Protocol):
    """Vector store protocol for RAG system"""
    def index(self, doc_id: str, text: str) -> None:
        """Index document text"""
        ...
    def search(self, query: str, top_k: int = 5) -> list[tuple[str, float, str]]:
        """Search similar documents"""
        ...
''',
    "tests/unit/test_health.py": '''from fastapi.testclient import TestClient
def test_health():
    """Test health endpoint"""
    client = TestClient(app)
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
''',
    ".github/workflows/ci.yml": """name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v3
      - name: Install dependencies
        run: uv pip install -e . "pytest" "ruff" "mypy" "bandit" "pip-audit"
      - name: Lint with ruff
        run: ruff check .
      - name: Type check with mypy
        run: mypy zeta_vn || true
      - name: Security check with bandit
        run: bandit -r zeta_vn || true
      - name: Audit dependencies
        run: pip-audit || true
      - name: Run tests
        run: pytest -q
""",
}


def create_file_with_content(file_path: Path, content: str = "") -> None:
    """Tạo file với nội dung"""
    file_path.parent.mkdir(parents=True, exist_ok=True)
    if file_path.suffix == ".py" and not content:
        if file_path.name == "__init__.py":
            content = f'"""Package: {file_path.parent.name}"""\n'
        else:
            content = f'"""Module: {file_path.stem}"""\nfrom __future__ import annotations\n'
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ Created: {file_path}")


def generate_8_layer_structure(base_path: str = ".") -> None:
    """Tạo cấu trúc 8-layer architecture hoàn chỉnh"""
    base = Path(base_path)
    print("🏗️ Generating 8-Layer Architecture Structure...")
    print("=" * 60)
    for root_dir, files in STRUCTURE_MAP.items():
        for file_path in files:
            full_path = base / root_dir / file_path
            create_file_with_content(full_path)
    print("\n📄 Creating configuration files...")
    for file_name, content in TEMPLATES.items():
        config_path = base / file_name
        create_file_with_content(config_path, content)
    print("\n🎯 Architecture structure generated successfully!")
    print("\nNext steps:")
    print("1. cd to your project directory")
    print("2. Run: uv pip install -e .")
    print("3. Run: uv run uvicorn zeta_vn.application.api.main:app --reload")
    print("4. Test: curl http://localhost:8000/api/v1/health")
    print("\n8-Layer Architecture is ready! 🚀")


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "."
    generate_8_layer_structure(path)
