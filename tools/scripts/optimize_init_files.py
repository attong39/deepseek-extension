from __future__ import annotations

import os
from pathlib import Path
import any
import d
import dir_path
import dirs
import export
import f
import files
import item
import len
import list
import module
import print
import py_file
import root
import skip
import sorted
import str
import subdir

"""
Script để xóa và tạo lại tất cả __init__.py files trong zeta_vn một cách tối ưu.
Author: duy_bg_vn
Date: September 1, 2025
Purpose: Clean up và opt        for subdir in subdirs:
            content_lines.append("try:")
            content_lines.append(f"    from . import {subdir}")
            content_lines.append("except ImportError:")
            content_lines.append("    pass  # Subpackage {} not available".format(subdir))         content_lines.append("except ImportError:")
            content_lines.append("    pass  # Subpackage {} not available".format(subdir))e package structure
"""
LAYER_STRUCTURE = {
    "domain": {
        "entities": ["agent", "user", "conversation", "memory", "task"],
        "value_objects": ["agent_id", "user_id", "message", "capability"],
        "domain_events": ["agent_created", "conversation_started", "task_completed"],
        "repositories": ["agent_repository", "user_repository", "conversation_repository"],
        "services": ["domain_service"],
    },
    "use_cases": {
        "agent": ["create_agent", "get_agent", "update_agent", "delete_agent"],
        "conversation": ["start_conversation", "send_message", "get_history"],
        "memory": ["store_memory", "retrieve_memory", "search_memory"],
        "task": ["create_task", "execute_task", "monitor_task"],
    },
    "infrastructure": {
        "database": ["connection", "migrations", "models"],
        "cache": ["redis_cache", "memory_cache"],
        "storage": ["file_storage", "vector_storage"],
        "external": ["openai_client", "anthropic_client", "pinecone_client"],
        "config": ["settings", "logging", "security"],
    },
    "app": {
        "api": {
            "v1": ["agent", "conversation", "memory", "health"],
            "v2": ["enhanced_agent", "advanced_conversation"],
            "graphql": ["schema", "resolvers", "mutations", "queries"],
            "websockets": ["chat_ws", "notification_ws"],
        },
        "controllers": ["agent_controller", "conversation_controller"],
        "middleware": ["auth", "cors", "rate_limit", "logging"],
        "dependencies": ["container", "auth_dependencies"],
        "exceptions": ["api_exceptions", "handlers"],
    },
    "core": {
        "interfaces": ["cache", "repository", "service"],
        "exceptions": ["domain_exceptions", "application_exceptions"],
        "shared": ["constants", "utils", "types"],
        "security": ["auth", "permissions", "encryption"],
        "observability": ["logging", "metrics", "tracing"],
        "performance": ["caching", "monitoring", "optimization"],
    },
    "services": {
        "ai": ["llm_service", "embedding_service", "rag_service"],
        "ml": ["training_service", "inference_service"],
        "memory": ["memory_manager", "vector_store"],
        "notification": ["email_service", "websocket_service"],
    },
    "config": {
        "settings": ["base", "development", "production", "testing"],
        "cache": ["redis_config", "memory_config"],
        "database": ["postgres_config", "sqlite_config"],
    },
    "data": {
        "models": ["agent_model", "user_model", "conversation_model"],
        "repositories": ["sqlalchemy_repos", "redis_repos"],
        "external": ["api_clients", "file_clients"],
        "migrations": ["alembic_migrations"],
    },
}


def remove_all_init_files(base_path: Path) -> list[Path]:
    """Xóa tất cả __init__.py files trong zeta_vn."""
    removed_files = []
    for init_file in base_path.rglob("__init__.py"):
        if "zeta_vn" in str(init_file):
            print(f"🗑️ Removing: {init_file}")
            init_file.unlink()
            removed_files.append(init_file)
    return removed_files


def get_python_files_in_dir(dir_path: Path) -> list[str]:
    """Lấy tất cả Python files trong directory (không bao gồm __init__.py)."""
    if not dir_path.exists() or not dir_path.is_dir():
        return []
    python_files = []
    for py_file in dir_path.glob("*.py"):
        if py_file.name != "__init__.py":
            module_name = py_file.stem
            python_files.append(module_name)
    return sorted(python_files)


def get_subdirectories(dir_path: Path) -> list[str]:
    """Lấy tất cả subdirectories."""
    if not dir_path.exists() or not dir_path.is_dir():
        return []
    subdirs = []
    for item in dir_path.iterdir():
        if item.is_dir() and not item.name.startswith(".") and item.name != "__pycache__":
            subdirs.append(item.name)
    return sorted(subdirs)


def create_optimized_init(dir_path: Path, package_name: str = None) -> str:
    """Tạo __init__.py tối ưu cho directory."""
    modules = get_python_files_in_dir(dir_path)
    subdirs = get_subdirectories(dir_path)
    relative_path = str(dir_path).replace(str(Path.cwd()), "").replace("\\", "/").strip("/")
    package_desc = f"{relative_path} package"
    if "domain" in relative_path:
        package_desc = "Domain layer - Core business logic and entities"
    elif "use_cases" in relative_path:
        package_desc = "Application layer - Use cases and business workflows"
    elif "infrastructure" in relative_path:
        package_desc = "Infrastructure layer - External services and data persistence"
    elif "app" in relative_path:
        package_desc = "Application interface layer - API endpoints and controllers"
    elif "core" in relative_path:
        package_desc = "Core shared components - Interfaces, exceptions, and utilities"
    elif "services" in relative_path:
        package_desc = "Service layer - Business services and orchestration"
    elif "config" in relative_path:
        package_desc = "Configuration layer - Settings and environment configuration"
    elif "data" in relative_path:
        package_desc = "Data layer - Models, repositories, and data access"
    content_lines = [
        f'"""{package_desc}."""',
        "",
        "from __future__ import annotations",
        "",
    ]
    if modules:
        content_lines.append("# Modules")
        for module in modules:
            content_lines.append("try:")
            content_lines.append(f"    from .{module} import *  # noqa: F403, F401")
            content_lines.append("except ImportError:")
            content_lines.append(f"    pass  # Module {module} not available")
            content_lines.append("")
    if subdirs:
        content_lines.append("# Subpackages")
        for subdir in subdirs:
            content_lines.append("try:")
            content_lines.append(f"    from . import {subdir}")
            content_lines.append("except ImportError:")
            content_lines.append(f"    pass  # Subpackage {subdir} not available")
            content_lines.append("")
    all_exports = modules + subdirs
    if all_exports:
        content_lines.append("# Public API")
        content_lines.append("__all__ = [")
        for export in all_exports:
            content_lines.append(f'    "{export}",')
        content_lines.append("]")
        content_lines.append("")
    content_lines.extend(
        [
            "# Package metadata",
            f'__package__ = "{relative_path.replace("/", ".")}"',
            '__version__ = "1.0.0"',
            '__author__ = "ZETA AI Team"',
            "",
        ]
    )
    return "\n".join(content_lines)


def create_all_init_files(base_path: Path) -> list[Path]:
    """Tạo tất cả __init__.py files tối ưu."""
    created_files = []
    for root, dirs, files in os.walk(base_path):
        root_path = Path(root)
        if any(
            skip in str(root_path) for skip in [".git", "__pycache__", ".pytest_cache", ".mypy_cache", "node_modules"]
        ):
            continue
        has_python = any(f.endswith(".py") for f in files)
        has_subdirs = any(os.path.isdir(os.path.join(root, d)) for d in dirs)
        if has_python or has_subdirs:
            init_file = root_path / "__init__.py"
            if not init_file.exists():
                content = create_optimized_init(root_path)
                print(f"✅ Creating: {init_file}")
                init_file.write_text(content, encoding="utf-8")
                created_files.append(init_file)
    return created_files


def main():
    """Main execution function."""
    print("🚀 Starting __init__.py optimization for zeta_vn")
    print("=" * 60)
    base_path = Path("zeta_vn")
    if not base_path.exists():
        print(f"❌ Error: {base_path} directory not found!")
        return
    print("\n📁 Step 1: Removing existing __init__.py files...")
    removed_files = remove_all_init_files(Path("."))
    print(f"🗑️ Removed {len(removed_files)} __init__.py files")
    print("\n📁 Step 2: Creating optimized __init__.py files...")
    created_files = create_all_init_files(base_path)
    print(f"✅ Created {len(created_files)} __init__.py files")
    print("\n" + "=" * 60)
    print("🎉 __init__.py optimization completed!")
    print("📊 Summary:")
    print(f"   - Removed: {len(removed_files)} files")
    print(f"   - Created: {len(created_files)} files")
    print(f"   - Net change: {len(created_files) - len(removed_files)} files")
    print("\n🔍 Next steps:")
    print("1. Run 'uv run ruff check .' to validate imports")
    print("2. Run 'uv run mypy zeta_vn' to check types")
    print("3. Run 'uv run pytest tests/' to verify functionality")


if __name__ == "__main__":
    main()
