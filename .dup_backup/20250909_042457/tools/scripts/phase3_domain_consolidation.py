#!/usr/bin/env python3
"""
Phase 3: Domain consolidation - Fix imports and clean domain layer
"""

from __future__ import annotations

import re
from pathlib import Path
import Exception
import domain
import e
import f
import int
import new_import
import old_import
import open
import print
import py_file


def fix_broken_imports() -> int:
    """Fix broken imports sau khi reorganize"""

    print("🔧 Fixing broken imports...")

    # Common import mappings
    import_fixes = {
        "from apps.backend.core.ports": "from apps.backend.core.interfaces",
        "from apps.backend.core.adapters": "from apps.backend.data.adapters",
        "from apps.backend.infrastructure": "from apps.backend.data.external",
        "from apps.backend.app.ai": "from apps.backend.core.services.ai",
        "from apps.backend.app.worker": "from apps.backend.data.external.worker",
    }

    fixed_files = 0

    for py_file in Path("zeta_vn").rglob("*.py"):
        try:
            with open(py_file, encoding="utf-8") as f:
                content = f.read()

            original_content = content

            # Apply import fixes
            for old_import, new_import in import_fixes.items():
                content = content.replace(old_import, new_import)

            # Fix specific patterns
            # Fix relative imports that might be broken
            content = re.sub(r"from \.ports(\.|import)", r"from .interfaces\1", content)
            content = re.sub(r"from \.adapters(\.|import)", r"from apps.backend.app.data.adapters\1", content)

            if content != original_content:
                with open(py_file, "w", encoding="utf-8") as f:
                    f.write(content)
                fixed_files += 1
                print(f"  ✅ Fixed imports: {py_file}")

        except Exception as e:
            print(f"  ⚠️  Failed to process {py_file}: {e}")

    return fixed_files


def consolidate_domain_entities() -> None:
    """Consolidate và organize domain entities"""

    print("\n🏗️  Consolidating domain entities...")

    # Ensure core domain entities are properly organized
    entities_dir = Path("zeta_vn/core/domain/entities")

    # Update entities __init__.py với proper exports
    entities_init = entities_dir / "__init__.py"
    entities_content = '''"""Core domain entities package"""

from .base import BaseEntity

# Import entities if they exist
try:
    from .agent import Agent, AgentCapability
except ImportError:
    pass

try:
    from .user import User
except ImportError:
    pass

try:
    from .chat import Chat, Message
except ImportError:
    pass

__all__ = [
    "BaseEntity",
]

# Add available entities to __all__
import sys
current_module = sys.modules[__name__]
for name in ["Agent", "AgentCapability", "User", "Chat", "Message"]:
    if hasattr(current_module, name):
        __all__.append(name)
'''

    entities_init.write_text(entities_content, encoding="utf-8")
    print("✅ Updated entities __init__.py")


def fix_value_objects_imports() -> None:
    """Fix value objects imports"""

    print("\n💎 Fixing value objects imports...")

    vo_init = Path("zeta_vn/core/domain/value_objects/__init__.py")
    vo_content = '''"""Core domain value objects package"""

# Import value objects by category
try:
    from .user import *
except ImportError:
    pass

try:
    from .agent import *
except ImportError:
    pass

try:
    from .memory import *
except ImportError:
    pass

try:
    from .permissions import *
except ImportError:
    pass

# Note: __all__ is defined in individual modules
'''

    vo_init.write_text(vo_content, encoding="utf-8")
    print("✅ Updated value objects __init__.py")


def organize_use_cases() -> None:
    """Organize use cases theo domain"""

    print("\n🎯 Organizing use cases...")

    use_cases_dir = Path("zeta_vn/core/use_cases")

    # Create domain-specific use case directories
    domains = ["agent", "user", "chat", "memory", "training"]

    for domain in domains:
        domain_dir = use_cases_dir / domain
        domain_dir.mkdir(exist_ok=True)

        domain_init = domain_dir / "__init__.py"
        if not domain_init.exists():
            domain_init.write_text(f'"""Use cases for {domain} domain"""\n', encoding="utf-8")

    # Update main use_cases __init__.py
    use_cases_init = use_cases_dir / "__init__.py"
    use_cases_content = '''"""Core use cases package"""

# Domain-specific use cases
try:
    from .agent import *
except ImportError:
    pass

try:
    from .user import *
except ImportError:
    pass

try:
    from .chat import *
except ImportError:
    pass

try:
    from .memory import *
except ImportError:
    pass

try:
    from .training import *
except ImportError:
    pass
'''

    use_cases_init.write_text(use_cases_content, encoding="utf-8")
    print("✅ Updated use cases structure")


def fix_core_services() -> None:
    """Fix core services organization"""

    print("\n⚙️  Fixing core services...")

    services_dir = Path("zeta_vn/core/services")

    # Update services __init__.py
    services_init = services_dir / "__init__.py"
    services_content = '''"""Core services package"""

# AI services
try:
    from .ai import *
except ImportError:
    pass

# Domain services
try:
    from .agent_service import AgentService
except ImportError:
    pass

try:
    from .user_service import UserService
except ImportError:
    pass

try:
    from .chat_service import ChatService
except ImportError:
    pass
'''

    services_init.write_text(services_content, encoding="utf-8")
    print("✅ Updated services __init__.py")


def create_dependency_injection_setup() -> None:
    """Create basic dependency injection setup"""

    print("\n💉 Creating dependency injection setup...")

    # Create DI container
    di_file = Path("zeta_vn/app/dependencies.py")
    di_content = '''"""Dependency injection container"""

from __future__ import annotations

from typing import Any, Dict

from apps.backend.core.interfaces.repositories.user_repository import UserRepositoryInterface
from apps.backend.core.interfaces.repositories.agent_repository import AgentRepositoryInterface
from apps.backend.core.interfaces.services.ai_service import AIServiceInterface

# Import implementations
try:
    from apps.backend.data.repositories.user_repository import UserRepository
    from apps.backend.data.repositories.agent_repository import AgentRepository
    from apps.backend.core.services.ai.orchestrator import AIOrchestrator
except ImportError:
    # Fallback if implementations don't exist
    UserRepository = None
    AgentRepository = None
    AIOrchestrator = None


class DIContainer:
    """Simple dependency injection container"""
    
    def __init__(self) -> None:
        self._services: Dict[str, Any] = {}
        self._setup_services()
    
    def _setup_services(self) -> None:
        """Setup service bindings"""
        
        # Repositories
        if UserRepository:
            self._services["user_repository"] = UserRepository()
        
        if AgentRepository:
            self._services["agent_repository"] = AgentRepository()
        
        # Services
        if AIOrchestrator:
            self._services["ai_service"] = AIOrchestrator()
    
    def get(self, service_name: str) -> Any:
        """Get service instance"""
        return self._services.get(service_name)
    
    def register(self, service_name: str, instance: Any) -> None:
        """Register service instance"""
        self._services[service_name] = instance


# Global container instance
container = DIContainer()


def get_user_repository() -> UserRepositoryInterface:
    """Get user repository"""
    return container.get("user_repository")


def get_agent_repository() -> AgentRepositoryInterface:
    """Get agent repository"""
    return container.get("agent_repository")


def get_ai_service() -> AIServiceInterface:
    """Get AI service"""
    return container.get("ai_service")
'''

    di_file.write_text(di_content, encoding="utf-8")
    print("✅ Created dependency injection setup")


def main() -> None:
    """Main execution for Phase 3"""
    print("🚀 PHASE 3: DOMAIN CONSOLIDATION")

    # 1. Fix broken imports
    fixed_imports = fix_broken_imports()

    # 2. Consolidate domain entities
    consolidate_domain_entities()

    # 3. Fix value objects
    fix_value_objects_imports()

    # 4. Organize use cases
    organize_use_cases()

    # 5. Fix core services
    fix_core_services()

    # 6. Create DI setup
    create_dependency_injection_setup()

    print(f"""
✅ PHASE 3 HOÀN TẤT!

🔧 Đã fix {fixed_imports} files với broken imports
🏗️  Đã consolidate domain entities
💎 Đã organize value objects
🎯 Đã organize use cases theo domain
⚙️  Đã fix core services
💉 Đã tạo dependency injection setup

🎯 Sẵn sàng cho Phase 4: Testing & validation
""")


if __name__ == "__main__":
    main()
