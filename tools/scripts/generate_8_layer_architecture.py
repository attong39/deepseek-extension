from __future__ import annotations
from __future__ import annotations
from __future__ import annotations
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict
from typing import Any, Dict, Optional
from typing import Dict, List, Tuple
import logging
import os
import sys

from unittest.mock import Mock, patch
from {import_path} import {class_name}, create_{instance_name}
import pytest

"""
🏗️ ZETA_VN 8-Layer Architecture Generator
Script tự động tạo cấu trúc thư mục hoàn chỉnh cho kiến trúc 8-layer.
Tạo tất cả thư mục và file cần thiết với template code chuẩn.
Created: 2025-09-01
Author: Zeta_VN Auto-Architecture Generator
"""
LAYER_STRUCTURE = {
    "infrastructure": {
        "config": ["settings.py", "database.py", "logging.py"],
        "database": ["connection.py", "models.py"],
        "storage": ["local_storage.py", "cloud_storage.py"],
        "cache": ["redis.py", "memory.py"],
        "utilities": ["environment.py", "resource_manager.py"],
    },
    "integration": {
        "api_clients": ["openai_client.py", "github_client.py", "weather_client.py"],
        "data_fetchers": ["web_fetcher.py", "rss_fetcher.py"],
        "third_party": ["saas_integration.py", "payment_gateway.py"],
        "security": ["api_key_manager.py", "encryption.py"],
    },
    "protocols": {
        "http": ["client.py", "server.py"],
        "websocket": ["handler.py", "manager.py"],
        "message_queue": ["rabbitmq.py", "kafka.py"],
        "serialization": ["json_serializer.py", "protobuf_serializer.py"],
        "auth": ["oauth.py", "jwt.py"],
    },
    "tools": {
        "email": ["sender.py", "templates.py"],
        "browser": ["automation.py", "scraper.py"],
        "nlp": ["summarizer.py", "translator.py"],
        "iot": ["device_controller.py", "sensor_reader.py"],
        "utilities": ["calculator.py", "calendar.py"],
    },
    "cognition": {
        "planning": ["task_planner.py", "workflow_orchestrator.py"],
        "decision_making": ["rule_engine.py", "policy_manager.py"],
        "error_handling": ["retry_strategies.py", "fallback_handler.py"],
        "algorithms": ["context_analyzer.py", "reasoning_engine.py"],
    },
    "memory": {
        "vector_store": ["faiss_store.py", "pgvector_store.py"],
        "user_profiles": ["profile_manager.py", "preference_store.py"],
        "session_management": ["session_store.py", "context_manager.py"],
        "cache": ["document_cache.py", "conversation_cache.py"],
    },
    "application": {
        "api": {
            "v1": {
                "endpoints": ["health.py", "documents.py", "training.py", "rag.py"],
                "schemas": ["health.py", "documents.py", "training.py"],
                "dependencies": ["auth.py", "rate_limiting.py"],
            },
            "ws": ["progress.py", "chat.py"],
        },
        "web_ui": {
            "static": {"css": [], "js": [], "images": []},
            "templates": ["base.html", "index.html"],
        },
        "cli": {"commands": ["db.py", "training.py"]},
        "orchestrator": ["job_scheduler.py", "task_manager.py"],
    },
    "ops": {
        "monitoring": ["performance.py", "health_checks.py", "alerting.py"],
        "logging": ["event_logger.py", "audit_trail.py"],
        "security": ["access_control.py", "content_filter.py", "compliance_checker.py"],
        "governance": ["rate_limiting.py", "bias_detection.py"],
        "deployment": ["health_check.py", "rollback.py"],
    },
}
TEMPLATES = {
    "layer_init": '''"""
{layer_name} Layer - {description}
{layer_description}
"""
__all__ = [
]
''',
    "module_template": '''"""
{module_name} - {description}
Implementation for {module_description}
"""
logger = logging.getLogger(__name__)
class {class_name}:
    """
    {class_description}
    Args:
        config: Configuration parameters
    Example:
        >>> {instance_name} = {class_name}()
        >>> result = await {instance_name}.{method_name}()
    """
    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """Initialize {class_name} with configuration."""
        self.config = config or {{}}
        self._setup()
    def _setup(self) -> None:
        """Setup internal components."""
        logger.info(f"Setting up {{self.__class__.__name__}}")
    async def {method_name}(self) -> Dict[str, Any]:
        """
        Main operation method.
        Returns:
            Operation result
        Raises:
            Exception: If operation fails
        """
        try:
            logger.info(f"Executing {{self.__class__.__name__}}.{method_name}")
            return {{"status": "success", "data": None}}
        except Exception as e:
            logger.error(f"Error in {{self.__class__.__name__}}: {{e}}")
            raise
def create_{instance_name}(config: Optional[Dict[str, Any]] = None) -> {class_name}:
    """
    Factory function to create {class_name} instance.
    Args:
        config: Optional configuration
    Returns:
        Configured {class_name} instance
    """
    return {class_name}(config)
''',
    "test_template": '''"""
Tests for {module_name}
Comprehensive test suite for {description}
"""
class Test{class_name}:
    """Test suite for {class_name}."""
    @pytest.fixture
    def {instance_name}(self) -> {class_name}:
        """Create {class_name} instance for testing."""
        return create_{instance_name}()
    @pytest.fixture
    def mock_config(self) -> Dict[str, Any]:
        """Mock configuration for testing."""
        return {{
            "test_mode": True,
            "timeout": 30
        }}
    async def test_{method_name}_success(self, {instance_name}: {class_name}) -> None:
        """Test successful {method_name} operation."""
        result = await {instance_name}.{method_name}()
        assert result["status"] == "success"
        assert "data" in result
    async def test_{method_name}_with_config(self, mock_config: Dict[str, Any]) -> None:
        """Test {method_name} with custom configuration."""
        {instance_name} = create_{instance_name}(mock_config)
        result = await {instance_name}.{method_name}()
        assert result["status"] == "success"
    async def test_setup(self, {instance_name}: {class_name}) -> None:
        """Test instance setup."""
        assert {instance_name}.config is not None
        assert isinstance({instance_name}.config, dict)
    @pytest.mark.asyncio
    async def test_error_handling(self, {instance_name}: {class_name}) -> None:
        """Test error handling in {method_name}."""
        with patch.object({instance_name}, '{method_name}', side_effect=Exception("Test error")):
            with pytest.raises(Exception, match="Test error"):
                await {instance_name}.{method_name}()
@pytest.mark.integration
class Test{class_name}Integration:
    """Integration tests for {class_name}."""
    async def test_end_to_end_workflow(self) -> None:
        """Test complete workflow."""
        {instance_name} = create_{instance_name}()
        result = await {instance_name}.{method_name}()
        assert result is not None
        assert result["status"] == "success"
''',
}
LAYER_DESCRIPTIONS = {
    "infrastructure": (
        "Infrastructure Layer",
        "Provides foundational services like configuration, database, storage, and caching",
    ),
    "integration": (
        "Integration Layer",
        "Handles external service integrations and third-party APIs",
    ),
    "protocols": ("Protocols Layer", "Manages communication protocols and data serialization"),
    "tools": ("Tools Layer", "Contains utility tools and external service wrappers"),
    "cognition": ("Cognition Layer", "Implements reasoning, planning, and decision-making logic"),
    "memory": ("Memory Layer", "Manages data persistence, user profiles, and session state"),
    "application": ("Application Layer", "Provides user interfaces including API, web UI, and CLI"),
    "ops": ("Operations Layer", "Handles monitoring, security, governance, and deployment"),
}
class ArchitectureGenerator:
    """Tạo cấu trúc 8-layer architecture tự động."""
    def __init__(self, base_path: str = "zeta_vn_restructured") -> None:
        """
        Initialize generator.
        Args:
            base_path: Đường dẫn thư mục gốc
        """
        self.base_path = Path(base_path)
        self.zeta_vn_path = self.base_path / "zeta_vn"
        self.tests_path = self.base_path / "tests"
        self.docs_path = self.base_path / "docs"
    def create_directory_structure(self) -> None:
        """Tạo cấu trúc thư mục đầy đủ."""
        print("🏗️ Creating 8-layer directory structure...")
        self.base_path.mkdir(exist_ok=True)
        self.zeta_vn_path.mkdir(exist_ok=True)
        self.tests_path.mkdir(exist_ok=True)
        self.docs_path.mkdir(exist_ok=True)
        (self.zeta_vn_path / "__init__.py").write_text(
            '"""Zeta_VN - 8-Layer AI Agent Architecture"""\n\n__version__ = "1.0.0"\n'
        )
        for layer_name, layer_structure in LAYER_STRUCTURE.items():
            self._create_layer_structure(layer_name, layer_structure)
        self._create_test_structure()
        self._create_docs_structure()
        self._create_config_files()
        print("✅ Directory structure created successfully!")
    def _create_layer_structure(self, layer_name: str, structure: Dict) -> None:
        """Tạo cấu trúc cho một layer."""
        layer_path = self.zeta_vn_path / layer_name
        layer_path.mkdir(exist_ok=True)
        layer_desc = LAYER_DESCRIPTIONS.get(layer_name, (layer_name.title(), f"{layer_name} layer"))
        init_content = TEMPLATES["layer_init"].format(
            layer_name=layer_desc[0], description=layer_desc[1], layer_description=layer_desc[1]
        )
        (layer_path / "__init__.py").write_text(init_content)
        self._create_nested_structure(layer_path, structure, layer_name)
    def _create_nested_structure(self, parent_path: Path, structure: Dict, layer_name: str) -> None:
        """Tạo cấu trúc lồng ghép."""
        for key, value in structure.items():
            current_path = parent_path / key
            current_path.mkdir(exist_ok=True)
            (current_path / "__init__.py").write_text(
                f'"""{key} module for {layer_name} layer"""\n'
            )
            if isinstance(value, list):
                for filename in value:
                    if filename.endswith(".py"):
                        self._create_module_file(current_path / filename, filename, layer_name, key)
                    else:
                        (current_path / filename).touch()
            elif isinstance(value, dict):
                self._create_nested_structure(current_path, value, layer_name)
    def _create_module_file(
        self, file_path: Path, filename: str, layer_name: str, module_group: str
    ) -> None:
        """Tạo file module với template code."""
        module_name = filename.replace(".py", "")
        class_name = self._to_pascal_case(module_name)
        instance_name = self._to_snake_case(class_name)
        method_name = "execute" if "executor" in module_name else "process"
        content = TEMPLATES["module_template"].format(
            module_name=module_name.replace("_", " ").title(),
            description=f"{module_name} implementation",
            module_description=f"{module_name} in {layer_name} layer",
            class_name=class_name,
            class_description=f"Implementation of {module_name} functionality",
            instance_name=instance_name,
            method_name=method_name,
        )
        file_path.write_text(content)
    def _create_test_structure(self) -> None:
        """Tạo cấu trúc test."""
        (self.tests_path / "__init__.py").write_text('"""Test suite for Zeta_VN"""\n')
        unit_path = self.tests_path / "unit"
        unit_path.mkdir(exist_ok=True)
        (unit_path / "__init__.py").write_text('"""Unit tests"""\n')
        for layer_name in LAYER_STRUCTURE.keys():
            layer_test_path = unit_path / layer_name
            layer_test_path.mkdir(exist_ok=True)
            (layer_test_path / "__init__.py").write_text(f'"""Tests for {layer_name} layer"""\n')
            test_file = layer_test_path / f"test_{layer_name}.py"
            test_content = TEMPLATES["test_template"].format(
                module_name=layer_name,
                description=f"{layer_name} layer",
                import_path=f"zeta_vn.{layer_name}",
                class_name=self._to_pascal_case(layer_name),
                instance_name=layer_name,
                method_name="process",
            )
            test_file.write_text(test_content)
        for test_type in ["integration", "e2e"]:
            test_path = self.tests_path / test_type
            test_path.mkdir(exist_ok=True)
            (test_path / "__init__.py").write_text(f'"""{test_type.upper()} tests"""\n')
    def _create_docs_structure(self) -> None:
        """Tạo cấu trúc documentation."""
        arch_path = self.docs_path / "architecture"
        arch_path.mkdir(exist_ok=True)
        overview_content = """# 8-Layer Architecture Overview
The Zeta_VN system follows an 8-layer architecture designed for scalability, maintainability, and separation of concerns.
1. **Infrastructure Layer**: Foundation services
2. **Integration Layer**: External service connections
3. **Protocols Layer**: Communication protocols
4. **Tools Layer**: Utility tools and services
5. **Cognition Layer**: AI reasoning and planning
6. **Memory Layer**: Data persistence and state
7. **Application Layer**: User interfaces
8. **Operations Layer**: Monitoring and governance
Each layer only depends on layers below it, ensuring clean separation and testability.
"""
        (arch_path / "overview.md").write_text(overview_content)
        for i, (layer_name, desc) in enumerate(LAYER_DESCRIPTIONS.items(), 1):
            layer_doc = f"""# Layer {i}: {desc[0]}
{desc[1]}
This layer contains the following modules:
```
{layer_name}/
├── __init__.py
"""
            if layer_name in LAYER_STRUCTURE:
                for module in LAYER_STRUCTURE[layer_name]:
                    layer_doc += f"├── {module}/\n"
            layer_doc += """```
- Follow async/await patterns
- Include comprehensive error handling
- Add type hints for all functions
- Document all public APIs
"""
            (arch_path / f"layer{i}_{layer_name}.md").write_text(layer_doc)
    def _create_config_files(self) -> None:
        """Tạo các file cấu hình."""
        pyproject_content = """[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
[project]
name = "zeta-vn"
dynamic = ["version"]
description = "8-Layer AI Agent Architecture"
readme = "README.md"
requires-python = ">=3.11"
license = "MIT"
keywords = ["ai", "agent", "architecture", "8-layer"]
authors = [
  { name = "Zeta_VN Team" },
]
classifiers = [
  "Development Status :: 4 - Beta",
  "Programming Language :: Python",
  "Programming Language :: Python :: 3.11",
  "Programming Language :: Python :: 3.12",
  "Programming Language :: Python :: Implementation :: CPython",
]
dependencies = [
  "fastapi>=0.104.0",
  "pydantic>=2.5.0",
  "uvicorn[standard]>=0.24.0",
  "sqlalchemy[asyncio]>=2.0.0",
  "alembic>=1.13.0",
  "redis>=5.0.0",
  "httpx>=0.25.0",
  "websockets>=12.0",
  "celery>=5.3.0",
  "rich>=13.0.0",
]
[project.optional-dependencies]
dev = [
  "pytest>=7.4.0",
  "pytest-asyncio>=0.21.0",
  "pytest-cov>=4.1.0",
  "ruff>=0.1.0",
  "mypy>=1.7.0",
  "pre-commit>=3.5.0",
]
[project.urls]
Documentation = "https://github.com/zeta-vn/docs"
Issues = "https://github.com/zeta-vn/issues"
Source = "https://github.com/zeta-vn/zeta-vn"
[tool.hatch.version]
path = "zeta_vn/__init__.py"
[tool.ruff]
target-version = "py311"
line-length = 88
select = ["E", "F", "UP", "B", "SIM", "I"]
ignore = ["E501", "B008"]
[tool.ruff.isort]
known-first-party = ["zeta_vn"]
[tool.mypy]
python_version = "3.11"
strict = true
warn_return_any = true
warn_unused_configs = true
"""
        (self.base_path / "pyproject.toml").write_text(pyproject_content)
        readme_content = """# Zeta_VN - 8-Layer AI Agent Architecture
A comprehensive AI agent system built with 8-layer architecture for maximum scalability and maintainability.
```
┌─────────────────────────────────────┐
│           Layer 8: Ops              │ ← Monitoring, Security, Governance
├─────────────────────────────────────┤
│        Layer 7: Application         │ ← API, Web UI, CLI
├─────────────────────────────────────┤
│          Layer 6: Memory            │ ← Vector Store, User Profiles
├─────────────────────────────────────┤
│         Layer 5: Cognition          │ ← Planning, Decision Making
├─────────────────────────────────────┤
│          Layer 4: Tools             │ ← Email, Browser, NLP, IoT
├─────────────────────────────────────┤
│         Layer 3: Protocols          │ ← HTTP, WebSocket, Message Queue
├─────────────────────────────────────┤
│        Layer 2: Integration         │ ← API Clients, Data Fetchers
├─────────────────────────────────────┤
│       Layer 1: Infrastructure       │ ← Config, Database, Storage
└─────────────────────────────────────┘
```
```bash
pip install -e .
uvicorn zeta_vn.application.api.main:app --reload
pytest
ruff check .
mypy .
```
See [docs/architecture/overview.md](docs/architecture/overview.md) for detailed architecture documentation.
MIT License - see LICENSE file for details.
"""
        (self.base_path / "README.md").write_text(readme_content)
        gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db
*.log
logs/
*.db
*.sqlite3
.cache/
.pytest_cache/
.mypy_cache/
.ruff_cache/
.coverage
htmlcov/
"""
        (self.base_path / ".gitignore").write_text(gitignore_content)
    def _to_pascal_case(self, snake_str: str) -> str:
        """Convert snake_case to PascalCase."""
        return "".join(word.capitalize() for word in snake_str.split("_"))
    def _to_snake_case(self, pascal_str: str) -> str:
        """Convert PascalCase to snake_case."""
        result = []
        for i, char in enumerate(pascal_str):
            if char.isupper() and i > 0:
                result.append("_")
            result.append(char.lower())
        return "".join(result)
    def generate_summary_report(self) -> None:
        """Tạo báo cáo tổng kết."""
        print("\n" + "=" * 60)
        print("🎉 8-LAYER ARCHITECTURE GENERATION COMPLETE!")
        print("=" * 60)
        print(f"\n📁 Project Structure Created at: {self.base_path.absolute()}")
        print(f"📦 Main Package: {self.zeta_vn_path}")
        print(f"🧪 Tests: {self.tests_path}")
        print(f"📖 Documentation: {self.docs_path}")
        print("\n🏗️ Generated Layers:")
        for i, (layer_name, desc) in enumerate(LAYER_DESCRIPTIONS.items(), 1):
            print(f"  {i}. {desc[0]} ({layer_name}/)")
        print("\n📋 Next Steps:")
        print("  1. cd zeta_vn_restructured")
        print("  2. python -m venv .venv")
        print("  3. .venv/Scripts/activate  # Windows")
        print("  4. pip install -e .")
        print("  5. pytest  # Run tests")
        print("  6. Start implementing layer by layer!")
        print("\n✅ Ready for development with full 8-layer architecture!")
def main() -> None:
    """Main entry point."""
    if len(sys.argv) > 1:
        base_path = sys.argv[1]
    else:
        base_path = "zeta_vn_restructured"
    generator = ArchitectureGenerator(base_path)
    try:
        generator.create_directory_structure()
        generator.generate_summary_report()
    except Exception as e:
        print(f"❌ Error generating architecture: {e}")
        sys.exit(1)
if __name__ == "__main__":
    main()