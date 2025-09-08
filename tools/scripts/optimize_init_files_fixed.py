from __future__ import annotations

import os
import sys
from pathlib import Path
import LAYER_STRUCTURE
import chr
import content_lines
import d
import dict
import dir_path
import dirs
import export
import f
import file
import item
import layer
import len
import list
import module
import open
import print
import python_files
import root
import sorted
import str
import subdir

"""
Script tối ưu hóa __init__.py files cho zeta_vn project.
Xóa tất cả __init__.py hiện tại và tạo lại với cấu trúc tối ưu theo Clean Architecture.
"""
LAYER_STRUCTURE: dict[str, dict[str, list[str]]] = {
    "infrastructure": {
        "external": ["api_clients", "file_clients", "storage", "vector_stores"],
        "data": ["repositories", "models", "migrations", "cache"],
        "messaging": ["pubsub", "events", "queues"],
        "monitoring": ["logging", "metrics", "tracing"],
    },
    "integration": {
        "apis": ["rest", "graphql", "webhooks"],
        "adapters": ["database", "external_services", "file_system"],
        "gateways": ["payment", "notification", "auth"],
        "clients": ["http", "grpc", "websocket"],
    },
    "protocols": {
        "interfaces": ["repositories", "services", "ports"],
        "contracts": ["api_contracts", "domain_contracts"],
        "schemas": ["request", "response", "domain"],
        "types": ["value_objects", "entities", "aggregates"],
    },
    "tools": {
        "scaffold": ["generators", "templates", "builders"],
        "validation": ["validators", "rules", "constraints"],
        "serialization": ["serializers", "mappers", "converters"],
        "utilities": ["helpers", "formatters", "parsers"],
    },
    "cognition": {
        "ai": ["models", "processors", "engines"],
        "knowledge": ["graphs", "embeddings", "indexing"],
        "reasoning": ["inference", "decision", "planning"],
        "learning": ["training", "adaptation", "feedback"],
    },
    "memory": {
        "storage": ["persistent", "cache", "session"],
        "retrieval": ["search", "query", "filtering"],
        "management": ["lifecycle", "cleanup", "optimization"],
        "context": ["state", "history", "preferences"],
    },
    "application": {
        "services": ["business", "domain", "application"],
        "use_cases": ["commands", "queries", "workflows"],
        "controllers": ["api", "cli", "background"],
        "middleware": ["auth", "logging", "validation"],
    },
    "ops": {
        "deployment": ["docker", "kubernetes", "scripts"],
        "monitoring": ["health", "metrics", "alerts"],
        "configuration": ["settings", "secrets", "environment"],
        "maintenance": ["backup", "cleanup", "migration"],
    },
}
INIT_FILE_NAME = "__init__.py"


def remove_all_init_files(base_path: Path) -> list[Path]:
    """Xóa tất cả __init__.py files trong zeta_vn."""
    removed_files: list[Path] = []
    for init_file in base_path.rglob(INIT_FILE_NAME):
        if "zeta_vn" in str(init_file):
            print(f"🗑️  Removing: {init_file}")
            init_file.unlink()
            removed_files.append(init_file)
    return removed_files


def get_python_modules(dir_path: Path) -> list[str]:
    """Lấy danh sách Python modules trong thư mục."""
    python_files: list[str] = []
    for file in dir_path.iterdir():
        if file.is_file() and file.suffix == ".py" and file.name != INIT_FILE_NAME:
            module_name = file.stem
            python_files.append(module_name)
    return sorted(python_files)


def get_subdirectories(dir_path: Path) -> list[str]:
    """Lấy danh sách subdirectories."""
    subdirs: list[str] = []
    for item in dir_path.iterdir():
        if item.is_dir() and not item.name.startswith("__pycache__"):
            subdirs.append(item.name)
    return sorted(subdirs)


def create_optimized_init(dir_path: Path) -> str:
    """Tạo nội dung __init__.py tối ưu cho thư mục."""
    modules = get_python_modules(dir_path)
    subdirs = get_subdirectories(dir_path)
    content_lines: list[str] = [
        '"""',
        f"Package: {dir_path.name}",
        f"Path: {str(dir_path).replace(chr(92), '/')}",
        "",
        "Auto-generated optimized __init__.py file.",
        "Follows Clean Architecture and 8-Layer Structure principles.",
        '"""',
        "",
        "from __future__ import annotations",
        "",
    ]
    layer_type = "unknown"
    for layer, _ in LAYER_STRUCTURE.items():
        if layer in str(dir_path):
            layer_type = layer
            break
    if layer_type != "unknown":
        content_lines.extend(
            [
                f"# Layer: {layer_type.upper()}",
                "# Clean Architecture compliance",
                "",
            ]
        )
    if modules:
        content_lines.append("# Module imports")
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
            f'__package__ = "{dir_path.name}"',
            '__version__ = "1.0.0"',
            f'__layer__ = "{layer_type}"',
            "",
            "# Clean Architecture compliance marker",
            "__clean_architecture__ = True",
            "",
        ]
    )
    return "\n".join(content_lines)


def create_all_init_files(base_path: Path) -> list[Path]:
    """Tạo tất cả __init__.py files với cấu trúc tối ưu."""
    created_files: list[Path] = []
    for root, dirs, _ in os.walk(base_path):
        root_path = Path(root)
        dirs[:] = [d for d in dirs if not d.startswith("__pycache__") and not d.startswith(".")]
        init_file = root_path / INIT_FILE_NAME
        if not init_file.exists():
            content = create_optimized_init(root_path)
            with open(init_file, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"✅ Created: {init_file}")
            created_files.append(init_file)
    return created_files


def main() -> None:
    """Main execution function."""
    print("🚀 Starting __init__.py optimization for zeta_vn")
    print("=" * 60)
    base_path = Path("zeta_vn")
    if not base_path.exists():
        print("❌ zeta_vn directory not found!")
        sys.exit(1)
    print("\n📍 Phase 1: Removing existing __init__.py files...")
    removed_files = remove_all_init_files(base_path)
    print(f"🗑️  Removed {len(removed_files)} __init__.py files")
    print("\n📍 Phase 2: Creating optimized __init__.py files...")
    created_files = create_all_init_files(base_path)
    print(f"✅ Created {len(created_files)} optimized __init__.py files")
    print("\n" + "=" * 60)
    print("📊 Summary:")
    print(f"  • Removed: {len(removed_files)} files")
    print(f"  • Created: {len(created_files)} files")
    print("  • Architecture: 8-Layer Clean Architecture")
    print("  • Features: Safe imports, __all__ exports, metadata")
    print("✨ __init__.py optimization completed successfully!")


if __name__ == "__main__":
    main()
