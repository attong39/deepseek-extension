#!/usr/bin/env python3
"""
ZETA AI SERVER - V2 API DEPENDENCY FIXER
Automatically removes mock dependencies from V2 API files.
"""

import re
from pathlib import Path
import Exception
import e
import enumerate
import f
import file_rel_path
import i
import len
import line
import open
import print
import self
import str


class V2DependencyFixer:
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)

    def fix_v2_file(self, file_path: Path):
        """Fix a single V2 API file."""
        print(f"🔧 Fixing {file_path.name}...")

        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()

            # Pattern to match the entire mock dependencies section
            mock_pattern = r"""# Dependencies
try:
    from app\.dependencies import \(
.*?
    \)
except ImportError:
.*?
        return _Mock.*?\(\)"""

            # Replace with clean import
            clean_import = (
                """# Dependencies
from app.dependencies import (
    get_current_user,
    get_federated_service,
    require_permissions,
)"""
                if "federated" in file_path.name
                else """# Dependencies
from app.dependencies import (
    get_current_user,
    get_collab_service,
    require_permissions,
)"""
                if "collab" in file_path.name
                else """# Dependencies
from app.dependencies import (
    get_current_user,
    get_advanced_memory_service,
    require_permissions,
)"""
            )

            # Apply the replacement
            new_content = re.sub(mock_pattern, clean_import, content, flags=re.DOTALL)

            # If pattern didn't match, try a more specific approach
            if new_content == content:
                # Look for the exact mock structure
                lines = content.split("\n")
                start_idx = None
                end_idx = None

                for i, line in enumerate(lines):
                    if "# Dependencies" in line and "try:" in lines[i + 1] if i + 1 < len(lines) else False:
                        start_idx = i
                    elif start_idx is not None and "return _Mock" in line and "()" in line:
                        end_idx = i + 1
                        break

                if start_idx is not None and end_idx is not None:
                    # Replace the mock section
                    service_name = (
                        "get_federated_service"
                        if "federated" in file_path.name
                        else "get_collab_service"
                        if "collab" in file_path.name
                        else "get_advanced_memory_service"
                    )

                    replacement_lines = [
                        "# Dependencies",
                        "from app.dependencies import (",
                        "    get_current_user,",
                        f"    {service_name},",
                        "    require_permissions,",
                        ")",
                        "",
                        "",
                        "# Router",
                        "router = APIRouter()",
                    ]

                    new_lines = lines[:start_idx] + replacement_lines + lines[end_idx:]
                    new_content = "\n".join(new_lines)

            # Write back if changed
            if new_content != content:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"   ✅ Fixed {file_path.name}")
                return True
            else:
                print(f"   ⚠️  No changes needed for {file_path.name}")
                return False

        except Exception as e:
            print(f"   ❌ Error fixing {file_path.name}: {e}")
            return False

    def fix_all_v2_files(self):
        """Fix all V2 API files."""
        print("🚀 FIXING V2 API DEPENDENCY MOCKS")
        print("=" * 50)

        v2_files = ["app/api/v2/advanced_memory.py", "app/api/v2/real_time_collab.py"]

        fixed_count = 0
        for file_rel_path in v2_files:
            file_path = self.project_path / file_rel_path
            if file_path.exists():
                if self.fix_v2_file(file_path):
                    fixed_count += 1
            else:
                print(f"⚠️  File not found: {file_rel_path}")

        print(f"\n📊 SUMMARY: Fixed {fixed_count} files")
        return fixed_count


if __name__ == "__main__":
    project_path = Path(__file__).parent.parent / "zeta_vn"
    fixer = V2DependencyFixer(str(project_path))
    fixer.fix_all_v2_files()
