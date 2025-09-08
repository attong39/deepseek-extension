#!/usr/bin/env python3
"""
ZETA AI SERVER - INIT PATTERN ANALYZER
Analyzes __init__ patterns to create appropriate base classes.
"""

import ast
from collections import defaultdict
from pathlib import Path
import Exception
import any
import class_name
import e
import f
import file_rel_path
import init_node
import isinstance
import item
import len
import list
import node
import open
import print
import rel_path
import self
import stmt
import str


class InitPatternAnalyzer:
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.patterns = defaultdict(list)

    def analyze_init_patterns(self):
        """Analyze __init__ method patterns."""
        print("🔍 ANALYZING __INIT__ PATTERNS")
        print("=" * 50)

        # Key files from duplicate analysis
        init_files = [
            "app/lifespan.py",
            "app/lifespan_enhanced.py",
            "app/services/collab_service.py",
            "app/services/federated_service.py",
            "core/services/agent_service.py",
            "core/services/ai_assistant.py",
            "core/services/analytics_service.py",
            "core/services/chat_service.py",
            "core/services/conversation_manager.py",
            "core/services/event_dispatcher.py",
            "core/services/learning_coordinator.py",
            "core/services/memory_service.py",
            "data/repositories/agent_repository.py",
            "data/repositories/memory_repository.py",
            "data/repositories/session_repository.py",
            "data/repositories/user_repository.py",
        ]

        for file_rel_path in init_files:
            file_path = self.project_path / file_rel_path
            if file_path.exists():
                self.analyze_file(file_path, file_rel_path)

        self.print_patterns()
        return self.patterns

    def analyze_file(self, file_path: Path, rel_path: str):
        """Analyze a single file for __init__ patterns."""
        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()

            tree = ast.parse(content)

            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    for item in node.body:
                        if isinstance(item, ast.FunctionDef) and item.name == "__init__":
                            self.classify_init_pattern(item, rel_path, node.name)

        except Exception as e:
            print(f"⚠️  Error analyzing {rel_path}: {e}")

    def classify_init_pattern(self, init_node: ast.FunctionDef, file_path: str, class_name: str):
        """Classify the __init__ pattern."""
        # Count arguments
        arg_count = len(init_node.args.args) - 1  # Exclude self

        # Check for body content
        body_lines = len(init_node.body)
        has_super = any(
            isinstance(stmt, ast.Expr)
            and isinstance(stmt.value, ast.Call)
            and isinstance(stmt.value.func, ast.Name)
            and stmt.value.func.id == "super"
            for stmt in init_node.body
        )

        # Classify pattern
        if arg_count == 0 and body_lines <= 2:
            pattern = "Empty/Minimal Init"
        elif arg_count == 0 and body_lines > 2:
            pattern = "Zero-Arg Service Init"
        elif arg_count > 0 and "repository" in file_path.lower():
            pattern = "Repository Init"
        elif arg_count > 0 and "service" in file_path.lower():
            pattern = "Service Init with Dependencies"
        elif has_super:
            pattern = "Inheriting Init"
        else:
            pattern = "Custom Init"

        self.patterns[pattern].append(
            {
                "file": file_path,
                "class": class_name,
                "args": arg_count,
                "body_lines": body_lines,
                "has_super": has_super,
            }
        )

    def print_patterns(self):
        """Print analysis results."""
        print("\n📊 INIT PATTERN ANALYSIS")
        print("-" * 50)

        for pattern, items in self.patterns.items():
            print(f"\n🔧 {pattern} ({len(items)} classes):")
            for item in items[:5]:  # Show first 5
                print(f"   📁 {item['file']} → {item['class']} " f"(args:{item['args']}, lines:{item['body_lines']})")
            if len(items) > 5:
                print(f"   ... and {len(items) - 5} more")

        print("\n💡 RECOMMENDED BASE CLASSES:")
        print("-" * 40)

        if "Empty/Minimal Init" in self.patterns:
            print("1. 🏗️  BaseEntity - for simple classes with empty __init__")

        if "Zero-Arg Service Init" in self.patterns:
            print("2. 🔧 BaseService - for services with zero-arg initialization")

        if "Repository Init" in self.patterns:
            print("3. 🗃️  BaseRepository - for repositories with dependency injection")

        if "Service Init with Dependencies" in self.patterns:
            print("4. ⚙️  BaseDependentService - for services with dependencies")


if __name__ == "__main__":
    project_path = Path(__file__).parent.parent / "zeta_vn"
    analyzer = InitPatternAnalyzer(str(project_path))
    analyzer.analyze_init_patterns()
