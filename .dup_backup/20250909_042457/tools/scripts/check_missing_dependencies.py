#!/usr/bin/env python3
"""
ZETA AI SERVER - MISSING DEPENDENCIES CHECKER
Scans the project for missing Python packages and libraries.
"""

import ast
import importlib.util
import subprocess
import sys
from pathlib import Path
import Exception
import ImportError
import alias
import e
import enumerate
import f
import i
import import_name
import isinstance
import len
import list
import node
import open
import print
import req
import req_file
import self
import set
import sorted
import str


class MissingDependenciesChecker:
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.imports = set()
        self.missing_imports = set()
        self.installed_packages = set()
        self.builtin_modules = set(sys.builtin_module_names)

    def get_installed_packages(self):
        """Get list of installed packages."""
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pip", "list"],
                capture_output=True,
                text=True,
                check=False,
            )
            if result.returncode == 0:
                lines = result.stdout.strip().split("\n")[2:]  # Skip header
                for line in lines:
                    if line.strip():
                        package_name = line.split()[0].lower()
                        self.installed_packages.add(package_name)
                        # Add common aliases
                        if package_name == "pillow":
                            self.installed_packages.add("pil")
                        elif package_name == "python-multipart":
                            self.installed_packages.add("multipart")
                        elif package_name == "pyjwt":
                            self.installed_packages.add("jwt")
        except Exception as e:
            print(f"⚠️  Error getting installed packages: {e}")

    def extract_imports_from_file(self, file_path: Path):
        """Extract imports from a Python file."""
        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()

            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        self.imports.add(alias.name.split(".")[0])
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        self.imports.add(node.module.split(".")[0])

        except Exception as e:
            print(f"⚠️  Error parsing {file_path}: {e}")

    def scan_project(self):
        """Scan entire project for imports."""
        print("🔍 SCANNING PROJECT FOR IMPORTS")
        print("=" * 50)

        python_files = list(self.project_path.rglob("*.py"))
        print(f"📁 Found {len(python_files)} Python files")

        for i, file_path in enumerate(python_files):
            if i % 50 == 0:
                print(f"   Processing {i}/{len(python_files)}...")
            self.extract_imports_from_file(file_path)

        print(f"📦 Total unique imports found: {len(self.imports)}")
        return self.imports

    def check_missing_dependencies(self):
        """Check which imports are missing."""
        print("\n🔍 CHECKING MISSING DEPENDENCIES")
        print("-" * 50)

        self.get_installed_packages()
        print(f"📦 Installed packages: {len(self.installed_packages)}")

        # Common standard library modules
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
            "enum",
            "functools",
            "hashlib",
            "hmac",
            "importlib",
            "inspect",
            "io",
            "itertools",
            "json",
            "logging",
            "math",
            "operator",
            "os",
            "pathlib",
            "re",
            "secrets",
            "shutil",
            "sqlite3",
            "sys",
            "tempfile",
            "time",
            "typing",
            "urllib",
            "uuid",
            "warnings",
            "weakref",
            "xml",
        }

        # Common aliases and mappings
        package_mappings = {
            "PIL": "pillow",
            "cv2": "opencv-python",
            "sklearn": "scikit-learn",
            "yaml": "pyyaml",
            "jwt": "pyjwt",
            "dotenv": "python-dotenv",
            "multipart": "python-multipart",
            "psycopg2": "psycopg2-binary",
            "mysqldb": "mysqlclient",
            "cx_oracle": "cx-oracle",
        }

        for import_name in self.imports:
            # Skip internal project modules
            if import_name in ["app", "core", "data", "config", "storage", "tests"]:
                continue

            # Skip builtin modules
            if import_name in self.builtin_modules:
                continue

            # Skip standard library
            if import_name in stdlib_modules:
                continue

            # Check if package is installed
            package_name = package_mappings.get(import_name, import_name).lower()

            if package_name not in self.installed_packages:
                # Try to import to double-check
                try:
                    importlib.import_module(import_name)
                except ImportError:
                    self.missing_imports.add(import_name)

        return self.missing_imports

    def analyze_requirements_files(self):
        """Analyze existing requirements files."""
        print("\n📋 ANALYZING REQUIREMENTS FILES")
        print("-" * 50)

        req_files = [
            "requirements.txt",
            "requirements-dev.txt",
            "pyproject.toml",
        ]

        declared_deps = set()

        for req_file in req_files:
            file_path = self.project_path.parent / req_file
            if file_path.exists():
                print(f"📄 Found {req_file}")
                try:
                    with open(file_path, encoding="utf-8") as f:
                        content = f.read()

                    if req_file.endswith(".txt"):
                        for line in content.split("\n"):
                            line = line.strip()
                            if line and not line.startswith("#"):
                                package = line.split("==")[0].split(">=")[0].split("~=")[0].strip()
                                declared_deps.add(package.lower())
                    elif req_file == "pyproject.toml":
                        # Basic TOML parsing for dependencies
                        lines = content.split("\n")
                        in_deps = False
                        for line in lines:
                            if "dependencies" in line and "[" in line:
                                in_deps = True
                            elif in_deps and line.strip().startswith('"'):
                                package = line.strip().strip('"').strip("'").split("==")[0].split(">=")[0]
                                declared_deps.add(package.lower())
                            elif in_deps and "]" in line:
                                in_deps = False

                except Exception as e:
                    print(f"⚠️  Error reading {req_file}: {e}")
            else:
                print(f"❌ {req_file} not found")

        print(f"📦 Declared dependencies: {len(declared_deps)}")
        return declared_deps

    def generate_missing_requirements(self):
        """Generate list of missing requirements."""
        print("\n📊 MISSING DEPENDENCIES ANALYSIS")
        print("=" * 50)

        if not self.missing_imports:
            print("✅ No missing dependencies found!")
            return []

        # Common package suggestions
        suggestions = {
            "fastapi": "fastapi>=0.104.1",
            "uvicorn": "uvicorn[standard]>=0.24.0",
            "sqlalchemy": "sqlalchemy>=2.0.23",
            "alembic": "alembic>=1.12.1",
            "pydantic": "pydantic>=2.5.0",
            "redis": "redis>=5.0.1",
            "celery": "celery>=5.3.4",
            "psycopg2": "psycopg2-binary>=2.9.9",
            "httpx": "httpx>=0.25.2",
            "pytest": "pytest>=7.4.3",
            "ruff": "ruff>=0.1.6",
            "mypy": "mypy>=1.7.1",
            "pre_commit": "pre-commit>=3.5.0",
            "python_dotenv": "python-dotenv>=1.0.0",
            "python_multipart": "python-multipart>=0.0.6",
            "pyjwt": "PyJWT>=2.8.0",
            "passlib": "passlib[bcrypt]>=1.7.4",
            "bcrypt": "bcrypt>=4.1.1",
            "cryptography": "cryptography>=41.0.7",
            "aiofiles": "aiofiles>=23.2.1",
            "pillow": "Pillow>=10.1.0",
            "numpy": "numpy>=1.24.4",
            "pandas": "pandas>=2.1.3",
            "matplotlib": "matplotlib>=3.8.2",
            "seaborn": "seaborn>=0.13.0",
            "scikit_learn": "scikit-learn>=1.3.2",
            "tensorflow": "tensorflow>=2.15.0",
            "torch": "torch>=2.1.1",
            "transformers": "transformers>=4.35.2",
            "openai": "openai>=1.3.7",
            "langchain": "langchain>=0.0.340",
            "chromadb": "chromadb>=0.4.17",
            "pinecone": "pinecone-client>=2.2.4",
            "websockets": "websockets>=12.0",
        }

        missing_requirements = []

        print(f"❌ MISSING PACKAGES ({len(self.missing_imports)}):")
        for import_name in sorted(self.missing_imports):
            suggestion = suggestions.get(import_name, f"{import_name}>=1.0.0")
            missing_requirements.append(suggestion)
            print(f"   📦 {import_name} → {suggestion}")

        return missing_requirements

    def write_missing_requirements_file(self, requirements: list[str]):
        """Write missing requirements to a file."""
        if not requirements:
            return

        output_file = self.project_path.parent / "requirements-missing.txt"
        with open(output_file, "w") as f:
            f.write("# Missing dependencies detected by dependency checker\n")
            f.write("# Review and add these to your main requirements.txt\n\n")
            for req in sorted(requirements):
                f.write(f"{req}\n")

        print(f"\n📄 Written missing requirements to: {output_file}")

    def run_full_analysis(self):
        """Run complete dependency analysis."""
        print("🚀 ZETA AI SERVER - DEPENDENCY ANALYSIS")
        print("=" * 60)

        # Scan project
        imports = self.scan_project()

        # Check missing
        missing = self.check_missing_dependencies()

        # Analyze existing requirements
        declared = self.analyze_requirements_files()

        # Generate suggestions
        requirements = self.generate_missing_requirements()

        # Write output file
        self.write_missing_requirements_file(requirements)

        # Summary
        print("\n📈 DEPENDENCY ANALYSIS SUMMARY")
        print("-" * 40)
        print(f"📦 Total imports found: {len(imports)}")
        print(f"📦 Installed packages: {len(self.installed_packages)}")
        print(f"📦 Declared dependencies: {len(declared)}")
        print(f"❌ Missing packages: {len(missing)}")

        if missing:
            print("\n💡 RECOMMENDED ACTIONS:")
            print("1. Review requirements-missing.txt")
            print("2. Install missing packages: pip install -r requirements-missing.txt")
            print("3. Add to main requirements.txt")
            print("4. Update pyproject.toml if using poetry/setuptools")


if __name__ == "__main__":
    project_path = Path(__file__).parent.parent / "zeta_vn"
    checker = MissingDependenciesChecker(str(project_path))
    checker.run_full_analysis()
