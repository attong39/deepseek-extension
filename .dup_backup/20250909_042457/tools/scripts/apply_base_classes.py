#!/usr/bin/env python3
"""
ZETA AI SERVER - BASE CLASS APPLIER
Automatically applies base classes to reduce __init__ duplication.
"""

import re
from pathlib import Path
import Exception
import e
import f
import file_rel_path
import open
import print
import self
import str


class BaseClassApplier:
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.applied_count = 0

    def apply_base_service(self, file_path: Path):
        """Apply BaseService to a service file."""
        print(f"🔧 Applying BaseService to {file_path.name}...")

        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()

            # Check if already using base class
            if "BaseService" in content or "base_classes" in content:
                print(f"   ⚠️  {file_path.name} already uses base classes")
                return False

            # Find service class with zero-arg __init__

            # Add import
            import_pattern = r"(from __future__ import annotations\n)"
            if "from __future__ import annotations" in content:
                new_content = re.sub(
                    import_pattern,
                    r"\1\nfrom core.common.base_classes import BaseService",
                    content,
                    count=1,
                )
            else:
                # Add at top after docstring
                new_content = (
                    content.replace(
                        '"""',
                        '"""\n\nfrom core.common.base_classes import BaseService',
                        1,
                    ).replace(
                        '"""\n\nfrom core.common.base_classes import BaseService',
                        '"""',
                        1,
                    )
                    + "\n\nfrom core.common.base_classes import BaseService"
                )
                new_content = re.sub(
                    r"(\n\nfrom core\.common\.base_classes import BaseService)+",
                    r"\1",
                    new_content,
                )

            # Replace class definition
            new_content = re.sub(r"class (\w+Service):", r"class \1(BaseService):", new_content)

            # Replace __init__ with _setup
            new_content = re.sub(
                r'def __init__\(self\) -> None:\s*""".*?"""\s*(.*?)(?=\n    def)',
                r'def _setup(self) -> None:\n        """Setup service specific state."""\n\1\n\n    def',
                new_content,
                flags=re.DOTALL,
            )

            # Write if changed
            if new_content != content:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"   ✅ Applied BaseService to {file_path.name}")
                self.applied_count += 1
                return True
            else:
                print(f"   ⚠️  No changes needed for {file_path.name}")
                return False

        except Exception as e:
            print(f"   ❌ Error applying to {file_path.name}: {e}")
            return False

    def apply_to_services(self):
        """Apply BaseService to service files."""
        print("🚀 APPLYING BASE CLASSES TO SERVICES")
        print("=" * 50)

        service_files = [
            "core/services/ai_assistant.py",
            "core/services/analytics_service.py",
            "core/services/chat_service.py",
            "core/services/conversation_manager.py",
            "core/services/event_dispatcher.py",
            "core/services/memory_service.py",
            "app/services/collab_service.py",
            "app/services/federated_service.py",
        ]

        for file_rel_path in service_files:
            file_path = self.project_path / file_rel_path
            if file_path.exists():
                self.apply_base_service(file_path)
            else:
                print(f"⚠️  File not found: {file_rel_path}")

        print(f"\n📊 SUMMARY: Applied base classes to {self.applied_count} files")
        return self.applied_count


if __name__ == "__main__":
    project_path = Path(__file__).parent.parent / "zeta_vn"
    applier = BaseClassApplier(str(project_path))
    applier.apply_to_services()
