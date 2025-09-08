#!/usr/bin/env python3
from __future__ import annotations
import Exception
import SystemExit
import action
import bool
import content
import dict
import e
import f
import filepath
import int
import len
import list
import miss
import print
import root
import str
import sum
import tuple

"""
Tự sinh khung vá nhanh cho file thiếu/rỗng.

Đọc module_symbol_report.json → sinh skeleton tối thiểu để build không vỡ.
- Không ghi đè file đã có nội dung > 20 ký tự
- Chỉ sinh skeleton chuẩn (FastAPI router, Adapter class với TODO)

Output: .artifacts/scaffold_actions.md
"""

import json
from pathlib import Path

ART = Path(".artifacts")
REPORT_FILE = ART / "module_symbol_report.json"
OUTPUT_FILE = ART / "scaffold_actions.md"

# Templates
ROUTER_SKELETON = '''from __future__ import annotations
"""Auto-generated router skeleton."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok"}
'''

ADAPTER_SKELETON = '''from __future__ import annotations
"""Auto-generated {name} skeleton."""

from typing import Any


class {name}:
    """TODO: Implement {name}."""
    
    def __init__(self, **kwargs: Any) -> None:
        """Initialize adapter with config."""
        self._config = kwargs
    
    def __str__(self) -> str:
        """String representation."""
        return f"{self.__class__.__name__}()"
'''

ENTITY_SKELETON = '''from __future__ import annotations
"""Auto-generated {name} entity skeleton."""

from typing import Any
from dataclasses import dataclass


@dataclass
class {name}:
    """TODO: Implement {name} entity."""
    
    id: str
    
    def __post_init__(self) -> None:
        """Post-initialization validation."""
        if not self.id:
            raise ValueError("ID is required")
'''

SERVICE_SKELETON = '''from __future__ import annotations
"""Auto-generated {name} skeleton."""

from typing import Any


class {name}:
    """TODO: Implement {name}."""
    
    def __init__(self) -> None:
        """Initialize service."""
        pass
    
    def process(self, data: Any) -> Any:
        """TODO: Implement main processing logic."""
        raise NotImplementedError("Service not implemented yet")
'''


def _ensure_file_with_content(filepath: Path, content: str) -> bool:
    """
    Tạo file với nội dung nếu chưa tồn tại hoặc quá nhỏ.

    Returns:
        True nếu đã tạo/ghi đè, False nếu bỏ qua
    """
    # Tạo thư mục parent nếu cần
    filepath.parent.mkdir(parents=True, exist_ok=True)

    # Kiểm tra file đã tồn tại và có nội dung đủ lớn chưa
    if filepath.exists():
        try:
            existing_content = filepath.read_text(encoding="utf-8", errors="ignore")
            if len(existing_content.strip()) > 20:  # File đã có nội dung
                return False
        except Exception:
            pass  # Lỗi đọc file -> ghi đè

    # Ghi nội dung mới
    try:
        filepath.write_text(content, encoding="utf-8")
        return True
    except Exception as e:
        print(f"Error writing {filepath}: {e}")
        return False


def _guess_skeleton_type(module_name: str, symbol_name: str) -> tuple[str, str] | None:
    """
    Đoán loại skeleton cần tạo dựa trên tên module/symbol.

    Returns:
        (template, filename) hoặc None nếu không nhận ra
    """
    module_lower = module_name.lower()
    symbol_lower = symbol_name.lower()

    # Router patterns
    if "router" in module_lower or module_lower.endswith((".status", ".rag", ".memory", ".chat", ".agent", ".auth")):
        return (ROUTER_SKELETON, "router.py" if symbol_name == "router" else f"{symbol_name}.py")

    # Adapter patterns
    if "adapter" in symbol_lower or module_lower.endswith("_adapter"):
        template = ADAPTER_SKELETON.format(name=symbol_name)
        filename = f"{symbol_name.lower()}.py"
        return (template, filename)

    # Entity patterns
    if "entities" in module_lower and symbol_name in ["Agent", "Chat", "Memory", "User", "Plan"]:
        template = ENTITY_SKELETON.format(name=symbol_name)
        filename = f"{symbol_name.lower()}.py"
        return (template, filename)

    # Service patterns
    if "service" in symbol_lower or module_lower.endswith("_service"):
        template = SERVICE_SKELETON.format(name=symbol_name)
        filename = f"{symbol_name.lower()}.py"
        return (template, filename)

    return None


def _convert_module_to_path(module_name: str) -> Path:
    """Convert module name to file path."""
    # Tìm source root
    roots = [Path("zeta_vn"), Path("src")]
    source_root = None

    for root in roots:
        if root.exists():
            source_root = root
            break

    if not source_root:
        source_root = Path("zeta_vn")  # Default fallback

    # Convert module.submodule -> path/submodule
    parts = module_name.split(".")
    if parts[0] in ["zeta_vn", "src"]:
        # Bỏ prefix nếu trùng với source root
        parts = parts[1:]

    return source_root / Path(*parts)


def _process_missing_symbols(misses: list[dict]) -> list[str]:
    """Xử lý danh sách symbol thiếu và tạo skeleton."""
    actions = []
    created_count = 0

    for miss in misses:
        if miss.get("severity") != "HIGH":
            continue  # Chỉ xử lý HIGH severity

        module_name = miss["module"]
        symbol_name = miss["symbol"]

        if symbol_name == "*":
            # Module không import được - tạo __init__.py
            module_path = _convert_module_to_path(module_name)
            init_file = module_path / "__init__.py"

            if _ensure_file_with_content(init_file, '"""Package initialization."""\n'):
                actions.append(f"✓ Created package init: {init_file}")
                created_count += 1
            continue

        # Đoán loại skeleton
        skeleton_info = _guess_skeleton_type(module_name, symbol_name)
        if not skeleton_info:
            actions.append(f"⚠ Cannot generate skeleton for {module_name}.{symbol_name}")
            continue

        template, filename = skeleton_info
        module_path = _convert_module_to_path(module_name)
        target_file = module_path.parent / filename

        if _ensure_file_with_content(target_file, template):
            actions.append(f"✓ Created skeleton: {target_file}")
            created_count += 1
        else:
            actions.append(f"⚠ Skipped existing file: {target_file}")

    actions.append(f"\nTotal created: {created_count}")
    return actions


def main() -> int:
    """Entry point chính."""
    print("🔧 Scaffolding missing modules...")

    if not REPORT_FILE.exists():
        print(f"Error: {REPORT_FILE} not found. Run verify_module_symbols.py first.")
        return 2

    try:
        with REPORT_FILE.open(encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading report: {e}")
        return 2

    misses = data.get("misses", [])
    if not misses:
        print("No missing symbols found, nothing to scaffold")
        OUTPUT_FILE.write_text("# Scaffold Actions\n\nNo actions needed.\n", encoding="utf-8")
        return 0

    print(f"Processing {len(misses)} missing symbols...")

    actions = ["# Scaffold Actions", ""]
    actions.extend(_process_missing_symbols(misses))

    # Ghi output
    output_content = "\n".join(actions) + "\n"
    OUTPUT_FILE.write_text(output_content, encoding="utf-8")

    print(f"[scaffold-missing] wrote {OUTPUT_FILE}")
    created_files = sum(1 for action in actions if action.startswith("✓"))
    print(f"  created_files={created_files}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
