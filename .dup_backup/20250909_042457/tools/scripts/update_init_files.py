#!/usr/bin/env python3
"""Script cập nhật toàn bộ file __init__.py theo chuẩn ZETA_AI.

Thiết kế __init__.py chuẩn cho FastAPI + Clean Architecture/DDD:
- Public API rõ ràng với __all__
- Version management an toàn
- Typing-first approach
- Lazy import support
- Tối thiểu side-effects
- Deprecation gateway
"""

from __future__ import annotations

from pathlib import Path
import Exception
import PACKAGE_CONFIGS
import any
import comp
import components
import description
import dict
import e
import f
import feature
import features
import len
import list
import open
import package_path
import print
import str
import tuple

# Mapping thư mục -> (description, components, special_features)
PACKAGE_CONFIGS: dict[str, tuple[str, list[str], list[str]]] = {
    # Core Layer
    "zeta_vn": (
        "ZETA AI - Enterprise AI Platform với Clean Architecture/DDD",
        [
            "FastAPI application factory",
            "Core domain models và services",
            "Infrastructure adapters",
            "Configuration management",
            "Public API endpoints",
        ],
        ["main_entry", "version_management", "app_factory"],
    ),
    "zeta_vn/core": (
        "Core domain layer - Business logic và domain models",
        [
            "Domain entities và value objects",
            "Domain services và specifications",
            "Use cases và application services",
            "Domain events và aggregates",
            "Ports và interfaces",
        ],
        ["domain_core"],
    ),
    "zeta_vn/core/domain": (
        "Domain model layer - Pure business logic",
        [
            "Domain entities",
            "Value objects",
            "Domain events",
            "Aggregates",
            "Specifications và business rules",
        ],
        ["domain_purity"],
    ),
    "zeta_vn/core/application": (
        "Application layer - Use cases và orchestration",
        [
            "Application services",
            "Command và query handlers",
            "Use case implementations",
            "Business workflow orchestration",
            "Cross-cutting concerns",
        ],
        ["use_cases"],
    ),
    "zeta_vn/core/infrastructure": (
        "Infrastructure layer - External concerns",
        [
            "Database implementations",
            "External API clients",
            "File systems",
            "Message queues",
            "Caching implementations",
        ],
        ["infrastructure"],
    ),
    "zeta_vn/core/mlops": (
        "MLOps - Machine Learning Operations và Model Lifecycle",
        [
            "Model versioning và tracking",
            "Model deployment và serving",
            "Model monitoring và performance",
            "A/B testing frameworks",
            "Feature stores và ML pipelines",
        ],
        ["ml_operations"],
    ),
    "zeta_vn/core/multimodal": (
        "Multimodal AI - Cross-modal capabilities",
        [
            "Vision-language models",
            "Audio processing",
            "Video analysis",
            "Cross-modal embeddings",
            "Multimodal reasoning",
        ],
        ["multimodal_ai"],
    ),
    "zeta_vn/core/memory": (
        "Advanced Memory - Cognitive memory systems",
        [
            "Working memory management",
            "Long-term memory storage",
            "Memory consolidation",
            "Associative memory networks",
            "Context-aware retrieval",
        ],
        ["memory_systems"],
    ),
    "zeta_vn/core/reasoning": (
        "AI Reasoning - Advanced cognitive processing",
        [
            "Logical inference engines",
            "Causal reasoning",
            "Analogical reasoning",
            "Meta-reasoning và reflection",
            "Chain-of-thought processing",
        ],
        ["reasoning_engine"],
    ),
    "zeta_vn/core/performance": (
        "Performance optimization - System efficiency",
        [
            "Performance monitoring",
            "Resource optimization",
            "Profiling tools",
            "Load balancing",
            "Performance analytics",
        ],
        ["performance_monitoring"],
    ),
    "zeta_vn/core/caching": (
        "Advanced Caching - Multi-tier caching strategies",
        [
            "Multi-level cache hierarchy",
            "Cache invalidation strategies",
            "Distributed caching",
            "Smart cache warming",
            "Cache performance analytics",
        ],
        ["caching_system"],
    ),
    "zeta_vn/core/resilience": (
        "System Resilience - Fault tolerance patterns",
        [
            "Circuit breaker patterns",
            "Retry mechanisms với backoff",
            "Bulkhead isolation",
            "Graceful degradation",
            "Health checks và monitoring",
        ],
        ["resilience_patterns"],
    ),
    "zeta_vn/core/testing": (
        "Testing Infrastructure - Comprehensive testing support",
        [
            "Test fixtures và utilities",
            "Mock implementations",
            "Property-based testing",
            "Performance testing",
            "Integration test helpers",
        ],
        ["testing_framework"],
    ),
    # App Layer
    "zeta_vn/app": (
        "Application layer - FastAPI controllers và middleware",
        [
            "FastAPI application",
            "API controllers",
            "Middleware stack",
            "Authentication/Authorization",
            "Request/Response handling",
        ],
        ["fastapi_app"],
    ),
    "zeta_vn/app/ai": (
        "AI Application Services - AI capabilities exposure",
        [
            "AI agent orchestration",
            "Chat service endpoints",
            "Analytics processing",
            "Multimodal service APIs",
            "ML model serving",
        ],
        ["ai_services"],
    ),
    "zeta_vn/app/api": (
        "REST API layer - HTTP endpoint definitions",
        [
            "REST API endpoints",
            "Request/Response schemas",
            "API versioning",
            "OpenAPI documentation",
            "API middleware",
        ],
        ["rest_api"],
    ),
    # Data Layer
    "zeta_vn/data": (
        "Data layer - Persistence và external integrations",
        [
            "Database models",
            "Repository implementations",
            "External API clients",
            "Data mappers",
            "Migration scripts",
        ],
        ["data_access"],
    ),
    # Infrastructure
    "zeta_vn/infrastructure": (
        "Infrastructure implementations - Technical adapters",
        [
            "Database adapters",
            "Message queue clients",
            "File storage systems",
            "External service clients",
            "Monitoring integrations",
        ],
        ["infrastructure_adapters"],
    ),
    # Utilities
    "zeta_vn/tools": (
        "Development Tools - Code generation và utilities",
        [
            "Code scaffolding tools",
            "Refactoring utilities",
            "Template generators",
            "Development helpers",
            "Build automation",
        ],
        ["dev_tools"],
    ),
    "zeta_vn/scripts": (
        "Automation Scripts - Deployment và maintenance",
        [
            "Deployment automation",
            "Data seeding scripts",
            "Database migrations",
            "Testing utilities",
            "Maintenance tasks",
        ],
        ["automation_scripts"],
    ),
}


def generate_standard_init_content(
    _package_path: str, description: str, components: list[str], features: list[str]
) -> str:
    """Generate standardized __init__.py content."""

    # Components formatted as bullet points
    components_text = "\\n".join(f"- {comp}" for comp in components)

    # Base template
    content = f'''"""
{description}.

Thành phần chính:
{components_text}

Thiết kế theo nguyên tắc:
- Clean Architecture/DDD patterns
- Typing-first approach
- Tối thiểu side-effects
- Public API rõ ràng qua __all__
- Lazy loading support
"""

from __future__ import annotations

'''

    # Add typing imports for complex packages
    if any(feature in features for feature in ["main_entry", "app_factory", "use_cases"]):
        content += """from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any, Dict, List, Optional  # noqa: PLC0415
    
"""

    # Version management for root package
    if "version_management" in features:
        content += """import sys
from importlib.metadata import PackageNotFoundError, version

# Version management với fallback an toàn
try:
    __version__ = version("zeta-vn")
except PackageNotFoundError:
    __version__ = "0.0.0+dev"

"""

    # Main entry point features
    if "main_entry" in features:
        content += '''# Public API - Chỉ export những gì cần thiết
__all__ = [
    "__version__",
    "get_version",
]

def get_version() -> str:
    """Trả về phiên bản hiện tại của package."""
    return __version__

# Lazy import support với __getattr__
def __getattr__(name: str) -> Any:
    """Lazy loading cho các module nặng."""
    if name == "create_app":
        from apps.backend.app.factory import create_app  # noqa: PLC0415
        return create_app
    elif name == "settings":
        from apps.backend.config.settings import settings  # noqa: PLC0415
        return settings
    elif name == "logger":
        from apps.backend.core.observability.logging import get_logger  # noqa: PLC0415
        return get_logger(__name__)
    
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")

# Runtime alias mapping for legacy imports
def _setup_aliases() -> None:
    """Setup module aliases for backward compatibility."""
    aliases = {
        "core": "zeta_vn.core",
        "app": "zeta_vn.app",
        "data": "zeta_vn.data",
        "config": "zeta_vn.config",
    }
    
    for alias, target in aliases.items():
        try:
            import importlib  # noqa: PLC0415
            module = importlib.import_module(target)
            sys.modules.setdefault(alias, module)
        except ImportError:
            pass  # Silent fallback

_setup_aliases()

'''

    elif "app_factory" in features:
        content += '''# FastAPI application factory
__all__ = [
    "create_app",
    "get_app_instance",
]

def __getattr__(name: str) -> Any:
    """Lazy loading cho FastAPI app và dependencies."""
    if name == "create_app":
        from apps.backend.app.factory import create_app  # noqa: PLC0415
        return create_app
    elif name == "app":
        from apps.backend.app.main import app  # noqa: PLC0415
        return app
    elif name == "router":
        from apps.backend.app.api.router import api_router  # noqa: PLC0415
        return api_router
        
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")

'''

    elif "domain_core" in features:
        content += """# Domain layer - Pure business logic exports
__all__ = [
    "entities",
    "value_objects",
    "events",
    "services",
    "specifications",
]

# Explicit re-exports để control public API
from . import entities, value_objects, events, services, specifications

"""

    elif "use_cases" in features:
        content += '''# Application services và use cases
__all__ = [
    "commands",
    "queries",
    "handlers",
    "services",
]

def __getattr__(name: str) -> Any:
    """Lazy loading cho application services."""
    # Command handlers
    if name.endswith("CommandHandler"):
        module_name = f".commands.{name.lower().replace('commandhandler', '')}"
        module = __import__(module_name, fromlist=[name], level=1)
        return getattr(module, name)
    
    # Query handlers
    elif name.endswith("QueryHandler"):
        module_name = f".queries.{name.lower().replace('queryhandler', '')}"
        module = __import__(module_name, fromlist=[name], level=1)
        return getattr(module, name)
        
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")

'''

    else:
        # Standard package init
        content += f'''# {description}
__all__: list[str] = []

# Lazy loading support
def __getattr__(name: str) -> Any:
    """Lazy import support để tránh circular imports."""
    # Import modules on-demand để tránh circular dependencies
    # và giảm thời gian khởi động
    raise AttributeError(f"module '{{__name__}}' has no attribute '{{name}}'")

'''

    # Add special features
    if "domain_purity" in features:
        content += '''
# Domain purity enforcement
def _validate_imports() -> None:
    """Validate rằng domain layer không import infrastructure."""
    import sys  # noqa: PLC0415
    forbidden_modules = [
        "sqlalchemy", "fastapi", "requests", "redis",
        "celery", "boto3", "psycopg2"
    ]
    
    loaded_modules = [name for name in sys.modules.keys()
                     if any(forbidden in name for forbidden in forbidden_modules)]
    
    if loaded_modules and __name__.startswith("zeta_vn.core.domain"):
        import warnings  # noqa: PLC0415
        warnings.warn(
            f"Domain layer importing infrastructure modules: {loaded_modules}",
            stacklevel=2
        )

# Chỉ validate trong development
if __debug__:
    _validate_imports()
'''

    if "testing_framework" in features:
        content += '''
# Testing utilities export
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from unittest.mock import Mock, MagicMock  # noqa: PLC0415
    import pytest  # noqa: PLC0415

__all__.extend([
    "create_test_client",
    "mock_factory",
    "test_fixtures",
])

def __getattr__(name: str) -> Any:
    """Lazy loading cho testing utilities."""
    if name == "create_test_client":
        from .client import create_test_client  # noqa: PLC0415
        return create_test_client
    elif name == "mock_factory":
        from .mocks import MockFactory  # noqa: PLC0415
        return MockFactory
    elif name == "fixtures":
        from . import fixtures  # noqa: PLC0415
        return fixtures
        
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
'''

    return content.strip()


def update_init_files() -> None:
    """Update all __init__.py files với chuẩn ZETA_AI."""

    root_dir = Path("zeta_vn")
    if not root_dir.exists():
        print(f"❌ Root directory {root_dir} not found!")
        return

    updated_count = 0
    created_count = 0

    print("🔄 Updating __init__.py files với ZETA_AI standard...")

    for package_path, (description, components, features) in PACKAGE_CONFIGS.items():
        init_file = Path(package_path) / "__init__.py"

        # Generate content
        content = generate_standard_init_content(package_path, description, components, features)

        # Create directory if needed
        init_file.parent.mkdir(parents=True, exist_ok=True)

        # Check if file exists
        file_existed = init_file.exists()

        # Write content
        try:
            with open(init_file, "w", encoding="utf-8") as f:
                f.write(content)

            if file_existed:
                updated_count += 1
                print(f"✅ Updated: {init_file}")
            else:
                created_count += 1
                print(f"➕ Created: {init_file}")

        except Exception as e:
            print(f"❌ Error processing {init_file}: {e}")

    print("\\n📊 Summary:")
    print(f"  ✅ Updated: {updated_count} files")
    print(f"  ➕ Created: {created_count} files")
    print(f"  📦 Total packages: {len(PACKAGE_CONFIGS)}")

    # Run autobarrel để cập nhật exports
    print("\\n🔄 Running autobarrel để cập nhật exports...")
    try:
        import subprocess  # noqa: PLC0415

        result = subprocess.run(
            ["uv", "run", "python", "tools/autobarrel_python.py"],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode == 0:
            print("✅ Autobarrel completed successfully")
        else:
            print(f"⚠️  Autobarrel warning: {result.stderr}")
    except Exception as e:
        print(f"❌ Could not run autobarrel: {e}")

    # Run quality checks
    print("\\n🔍 Running quality checks...")
    try:
        import subprocess  # noqa: PLC0415

        # Ruff format
        result = subprocess.run(
            ["uv", "run", "ruff", "format", "."],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode == 0:
            print("✅ Ruff format completed")

        # Ruff check imports
        result = subprocess.run(
            ["uv", "run", "ruff", "check", ".", "--select", "F401,F403,F405"],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode == 0:
            print("✅ Import checks passed")
        else:
            print(f"⚠️  Import issues found: {result.stdout}")

    except Exception as e:
        print(f"❌ Quality check error: {e}")


if __name__ == "__main__":
    update_init_files()
