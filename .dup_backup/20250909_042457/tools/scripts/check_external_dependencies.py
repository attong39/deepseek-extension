#!/usr/bin/env python3
"""
ZETA AI SERVER - SMART DEPENDENCY CHECKER
Intelligently identifies missing external dependencies vs internal modules.
"""

import ast
import sys
from pathlib import Path
import Exception
import ImportError
import alias
import dir_name
import e
import enumerate
import f
import file_path
import i
import import_name
import isinstance
import len
import list
import missing
import node
import open
import package
import pkg
import print
import py_file
import req
import self
import set
import sorted
import str


class SmartDependencyChecker:
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.external_imports = set()
        self.internal_modules = set()
        self.missing_external = set()

    def identify_internal_modules(self):
        """Identify internal project modules."""
        internal_dirs = ["app", "core", "data", "config", "storage", "tests"]

        for dir_name in internal_dirs:
            dir_path = self.project_path / dir_name
            if dir_path.exists():
                for py_file in dir_path.rglob("*.py"):
                    # Get module path relative to project
                    rel_path = py_file.relative_to(self.project_path)
                    module_parts = rel_path.with_suffix("").parts

                    # Add all possible import variations
                    for i, _ in enumerate(module_parts):
                        module_name = ".".join(module_parts[: i + 1])
                        self.internal_modules.add(module_name)
                        self.internal_modules.add(module_parts[i])  # Individual parts

        print(f"🏠 Internal modules identified: {len(self.internal_modules)}")

    def extract_external_imports(self):
        """Extract only external imports."""
        python_files = list(self.project_path.rglob("*.py"))

        # Known external packages in AI/ML projects

        for file_path in python_files:
            try:
                with open(file_path, encoding="utf-8") as f:
                    content = f.read()

                tree = ast.parse(content)
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            top_level = alias.name.split(".")[0]
                            if top_level not in self.internal_modules and top_level not in sys.builtin_module_names:
                                self.external_imports.add(top_level)
                    elif isinstance(node, ast.ImportFrom) and node.module:
                        top_level = node.module.split(".")[0]
                        if top_level not in self.internal_modules and top_level not in sys.builtin_module_names:
                            self.external_imports.add(top_level)

            except Exception as e:
                if "test_chat" not in str(file_path):  # Skip known problematic files
                    print(f"⚠️  Error parsing {file_path}: {e}")

        print(f"📦 External imports found: {len(self.external_imports)}")
        return self.external_imports

    def check_import_availability(self):
        """Check which external imports are actually missing."""
        # Standard library modules (Python 3.11+)
        stdlib_modules = {
            "abc",
            "argparse",
            "ast",
            "asyncio",
            "base64",
            "collections",
            "contextlib",
            "copy",
            "datetime",
            "decimal",
            "email",
            "enum",
            "functools",
            "hashlib",
            "hmac",
            "html",
            "http",
            "importlib",
            "inspect",
            "io",
            "itertools",
            "json",
            "logging",
            "math",
            "multiprocessing",
            "operator",
            "os",
            "pathlib",
            "pickle",
            "platform",
            "random",
            "re",
            "secrets",
            "shutil",
            "signal",
            "socket",
            "sqlite3",
            "ssl",
            "string",
            "subprocess",
            "sys",
            "tempfile",
            "threading",
            "time",
            "typing",
            "unittest",
            "urllib",
            "uuid",
            "warnings",
            "weakref",
            "xml",
            "zipfile",
        }

        for import_name in self.external_imports:
            # Skip standard library
            if import_name in stdlib_modules:
                continue

            # Try to import
            try:
                __import__(import_name)
            except ImportError:
                self.missing_external.add(import_name)

        print(f"❌ Missing external packages: {len(self.missing_external)}")
        return self.missing_external

    def suggest_package_names(self):
        """Suggest correct package names for installation."""
        # Common package name mappings
        package_mappings = {
            "PIL": "Pillow",
            "cv2": "opencv-python",
            "sklearn": "scikit-learn",
            "yaml": "PyYAML",
            "dotenv": "python-dotenv",
            "jwt": "PyJWT",
            "multipart": "python-multipart",
            "psycopg2": "psycopg2-binary",
            "pymongo": "pymongo",
            "redis": "redis",
            "celery": "celery",
            "anthropic": "anthropic",
            "openai": "openai",
            "langchain": "langchain",
            "chromadb": "chromadb",
            "pinecone": "pinecone-client",
            "qdrant_client": "qdrant-client",
            "transformers": "transformers",
            "websockets": "websockets",
            "fastapi": "fastapi",
            "uvicorn": "uvicorn[standard]",
            "pydantic": "pydantic[email]",
            "sqlalchemy": "sqlalchemy",
            "alembic": "alembic",
            "httpx": "httpx",
            "aiofiles": "aiofiles",
            "passlib": "passlib[bcrypt]",
            "python_dotenv": "python-dotenv",
            "fakeredis": "fakeredis",
            "pyotp": "pyotp",
            "qrcode": "qrcode[pil]",
        }

        suggestions = []
        for missing in sorted(self.missing_external):
            suggestion = package_mappings.get(missing, missing)
            suggestions.append(suggestion)

        return suggestions

    def generate_requirements(self):
        """Generate requirements with versions."""
        version_suggestions = {
            "fastapi": "fastapi>=0.104.1",
            "uvicorn[standard]": "uvicorn[standard]>=0.24.0",
            "pydantic[email]": "pydantic[email]>=2.5.0",
            "sqlalchemy": "sqlalchemy>=2.0.23",
            "alembic": "alembic>=1.12.1",
            "redis": "redis>=5.0.1",
            "celery": "celery>=5.3.4",
            "httpx": "httpx>=0.25.2",
            "aiofiles": "aiofiles>=23.2.1",
            "psycopg2-binary": "psycopg2-binary>=2.9.9",
            "python-dotenv": "python-dotenv>=1.0.0",
            "PyJWT": "PyJWT>=2.8.0",
            "passlib[bcrypt]": "passlib[bcrypt]>=1.7.4",
            "bcrypt": "bcrypt>=4.1.1",
            "cryptography": "cryptography>=41.0.7",
            "Pillow": "Pillow>=10.1.0",
            "python-multipart": "python-multipart>=0.0.6",
            "websockets": "websockets>=12.0",
            "openai": "openai>=1.3.7",
            "anthropic": "anthropic>=0.7.7",
            "langchain": "langchain>=0.0.340",
            "transformers": "transformers>=4.35.2",
            "chromadb": "chromadb>=0.4.17",
            "pinecone-client": "pinecone-client>=2.2.4",
            "qdrant-client": "qdrant-client>=1.6.9",
            "numpy": "numpy>=1.24.4",
            "pandas": "pandas>=2.1.3",
            "scikit-learn": "scikit-learn>=1.3.2",
            "fakeredis": "fakeredis>=2.20.1",
            "pyotp": "pyotp>=2.9.0",
            "qrcode[pil]": "qrcode[pil]>=7.4.2",
            "opencv-python": "opencv-python>=4.8.1.78",
        }

        suggestions = self.suggest_package_names()
        requirements = []

        for package in suggestions:
            versioned = version_suggestions.get(package, f"{package}>=1.0.0")
            requirements.append(versioned)

        return requirements

    def run_analysis(self):
        """Run complete smart dependency analysis."""
        print("🧠 ZETA AI SERVER - SMART DEPENDENCY ANALYSIS")
        print("=" * 60)

        # Step 1: Identify internal modules
        self.identify_internal_modules()

        # Step 2: Extract external imports
        self.extract_external_imports()

        # Step 3: Check availability
        self.check_import_availability()

        # Step 4: Generate suggestions
        requirements = self.generate_requirements()

        # Results
        if self.missing_external:
            print(f"\n❌ MISSING EXTERNAL PACKAGES ({len(self.missing_external)}):")
            print("-" * 50)
            for pkg in sorted(self.missing_external):
                print(f"   📦 {pkg}")

            print("\n📋 SUGGESTED REQUIREMENTS:")
            print("-" * 40)
            for req in requirements:
                print(f"   {req}")

            # Write to file
            output_file = self.project_path.parent / "requirements-external-missing.txt"
            with open(output_file, "w") as f:
                f.write("# Missing external dependencies for ZETA AI Server\n")
                f.write("# Install with: pip install -r requirements-external-missing.txt\n\n")
                for req in requirements:
                    f.write(f"{req}\n")

            print(f"\n📄 Requirements written to: {output_file}")
            print("\n🚀 INSTALL COMMAND:")
            print("   pip install -r requirements-external-missing.txt")

        else:
            print("\n✅ ALL EXTERNAL DEPENDENCIES ARE SATISFIED!")
            print("   No missing packages found.")

        print("\n📊 SUMMARY:")
        print(f"   🏠 Internal modules: {len(self.internal_modules)}")
        print(f"   📦 External imports: {len(self.external_imports)}")
        print(f"   ❌ Missing external: {len(self.missing_external)}")


if __name__ == "__main__":
    project_path = Path(__file__).parent.parent / "zeta_vn"
    checker = SmartDependencyChecker(str(project_path))
    checker.run_analysis()
