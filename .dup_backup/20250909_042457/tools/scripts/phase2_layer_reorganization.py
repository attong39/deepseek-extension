#!/usr/bin/env python3
"""
Phase 2: Layer reorganization theo Clean Architecture
"""

from __future__ import annotations

import shutil
from pathlib import Path
import Exception
import base_dir
import content
import e
import file_path
import print
import source
import str
import subdir
import subdirs
import target


def create_clean_architecture_structure():
    """Tạo cấu trúc thư mục Clean Architecture chuẩn"""

    print("🏗️  Tạo cấu trúc Clean Architecture...")

    # Core directories theo Clean Architecture
    core_structure = {
        "zeta_vn/core/domain/": [
            "entities/",
            "value_objects/",
            "events/",
            "aggregates/",
            "specifications/",
        ],
        "zeta_vn/core/": [
            "use_cases/",
            "services/",
            "interfaces/",
        ],
        "zeta_vn/app/": [
            "api/v1/",
            "websockets/",
            "controllers/",
            "serializers/",
            "validators/",
            "middleware/",
        ],
        "zeta_vn/data/": [
            "models/",
            "repositories/",
            "database/",
            "external/",
            "adapters/",
            "migrations/",
        ],
        "zeta_vn/config/": [
            "environments/",
        ],
        "zeta_vn/tests/": [
            "unit/",
            "integration/",
            "e2e/",
            "fixtures/",
        ],
    }

    # Tạo directories
    for base_dir, subdirs in core_structure.items():
        base_path = Path(base_dir)
        base_path.mkdir(parents=True, exist_ok=True)

        # Tạo __init__.py cho base directory
        init_file = base_path / "__init__.py"
        if not init_file.exists():
            init_file.write_text("# Package init\n", encoding="utf-8")

        for subdir in subdirs:
            subdir_path = base_path / subdir
            subdir_path.mkdir(parents=True, exist_ok=True)

            # Tạo __init__.py cho subdirectory
            sub_init = subdir_path / "__init__.py"
            if not sub_init.exists():
                sub_init.write_text("# Package init\n", encoding="utf-8")

        print(f"✅ Created: {base_dir}")


def migrate_existing_files():
    """Di chuyển files hiện tại vào đúng layer"""

    print("\n📦 Migrating existing files to proper layers...")

    # Migration mapping
    migrations = {
        # Core/Domain layer
        "zeta_vn/core/ports/": "zeta_vn/core/interfaces/",
        "zeta_vn/core/adapters/": "zeta_vn/data/adapters/",
        # Infrastructure layer
        "zeta_vn/infrastructure/": "zeta_vn/data/external/",
        # Application layer - AI services
        "zeta_vn/app/ai/": "zeta_vn/core/services/ai/",
        # Move some specific files
        "zeta_vn/app/worker/": "zeta_vn/data/external/worker/",
        "zeta_vn/app/deployment/": "zeta_vn/data/external/deployment/",
    }

    for source, target in migrations.items():
        source_path = Path(source)
        target_path = Path(target)

        if source_path.exists() and source_path.is_dir():
            print(f"📁 Moving {source} -> {target}")

            # Create target directory
            target_path.parent.mkdir(parents=True, exist_ok=True)

            try:
                # Move directory
                if target_path.exists():
                    # Merge if target exists
                    shutil.copytree(source_path, target_path, dirs_exist_ok=True)
                    shutil.rmtree(source_path)
                else:
                    shutil.move(str(source_path), str(target_path))

                print("  ✅ Moved successfully")
            except Exception as e:
                print(f"  ⚠️  Failed to move: {e}")


def create_interface_definitions():
    """Tạo interface definitions cho Clean Architecture"""

    print("\n🔌 Creating interface definitions...")

    # Repository interfaces
    repo_interfaces = {
        "zeta_vn/core/interfaces/repositories/user_repository.py": '''"""User repository interface"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from apps.backend.core.domain.entities.user import User


class UserRepositoryInterface(ABC):
    """Interface for user repository"""
    
    @abstractmethod
    async def get_by_id(self, user_id: str) -> Optional[User]:
        """Get user by ID"""
        pass
    
    @abstractmethod
    async def save(self, user: User) -> User:
        """Save user"""
        pass
    
    @abstractmethod
    async def delete(self, user_id: str) -> bool:
        """Delete user"""
        pass
''',
        "zeta_vn/core/interfaces/repositories/agent_repository.py": '''"""Agent repository interface"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional

from apps.backend.core.domain.entities.agent import Agent


class AgentRepositoryInterface(ABC):
    """Interface for agent repository"""
    
    @abstractmethod
    async def get_by_id(self, agent_id: str) -> Optional[Agent]:
        """Get agent by ID"""
        pass
    
    @abstractmethod
    async def get_by_user_id(self, user_id: str) -> List[Agent]:
        """Get agents by user ID"""
        pass
    
    @abstractmethod
    async def save(self, agent: Agent) -> Agent:
        """Save agent"""
        pass
''',
    }

    # Service interfaces
    service_interfaces = {
        "zeta_vn/core/interfaces/services/ai_service.py": '''"""AI service interface"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict

from apps.backend.core.domain.value_objects.ai_request import AIRequest
from apps.backend.core.domain.value_objects.ai_response import AIResponse


class AIServiceInterface(ABC):
    """Interface for AI service"""
    
    @abstractmethod
    async def process_request(self, request: AIRequest) -> AIResponse:
        """Process AI request"""
        pass
    
    @abstractmethod
    async def get_capabilities(self) -> Dict[str, Any]:
        """Get service capabilities"""
        pass
''',
    }

    # Create interface files
    all_interfaces = {**repo_interfaces, **service_interfaces}

    for file_path, content in all_interfaces.items():
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        if not path.exists():
            path.write_text(content, encoding="utf-8")
            print(f"✅ Created interface: {file_path}")


def update_barrel_exports():
    """Update barrel exports cho các packages"""

    print("\n📤 Updating barrel exports...")

    # Core domain barrel
    domain_init = Path("zeta_vn/core/domain/__init__.py")
    domain_content = '''"""Core domain package"""

# Entities
from .entities.base import BaseEntity
from .entities.agent import Agent, AgentCapability

# Value Objects
from .value_objects.user import *
from .value_objects.agent import *
from .value_objects.memory import *

# Events
from .events.domain_events import DomainEvent
from .events.user_events import *
from .events.agent_events import *

__all__ = [
    # Entities
    "BaseEntity",
    "Agent",
    "AgentCapability",
    
    # Events
    "DomainEvent",
]
'''
    domain_init.write_text(domain_content, encoding="utf-8")
    print("✅ Updated domain barrel")

    # Core interfaces barrel
    interfaces_init = Path("zeta_vn/core/interfaces/__init__.py")
    interfaces_content = '''"""Core interfaces package"""

from .repositories.user_repository import UserRepositoryInterface
from .repositories.agent_repository import AgentRepositoryInterface
from .services.ai_service import AIServiceInterface

__all__ = [
    "UserRepositoryInterface",
    "AgentRepositoryInterface",
    "AIServiceInterface",
]
'''
    interfaces_init.write_text(interfaces_content, encoding="utf-8")
    print("✅ Updated interfaces barrel")


def main():
    """Main execution for Phase 2"""
    print("🚀 PHASE 2: LAYER REORGANIZATION")

    # 1. Create Clean Architecture structure
    create_clean_architecture_structure()

    # 2. Migrate existing files
    migrate_existing_files()

    # 3. Create interface definitions
    create_interface_definitions()

    # 4. Update barrel exports
    update_barrel_exports()

    print("""
✅ PHASE 2 HOÀN TẤT!

🏗️  Đã tạo cấu trúc Clean Architecture chuẩn
📦 Đã migrate existing files vào đúng layer
🔌 Đã tạo interface definitions
📤 Đã update barrel exports

🎯 Sẵn sàng cho Phase 3: Domain consolidation
""")


if __name__ == "__main__":
    main()
