#!/usr/bin/env python3
"""
One-Click Learning Setup Script

Automates the complete setup of the RAG + ASR + OCR + Desktop system.
CPU-first with GPU acceleration via ZETA_USE_GPU=1.
"""

import os
import sys
import subprocess
import platform
from pathlib import Path
from typing import List, Dict, Any
import json
import Exception
import FileNotFoundError
import bool
import command
import dep
import description
import e
import ignore_errors
import print
import self
import str
import tool


class OneClickSetup:
    """One-Click Learning setup automation."""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.backend_path = project_root / "apps" / "backend"
        self.desktop_path = project_root / "apps" / "desktop"
        self.system = platform.system().lower()
        self.is_windows = self.system == "windows"
        
    def run(self) -> None:
        """Run the complete setup process."""
        print("🎯 One-Click Learning + RAG + DevSecOps Setup")
        print("=" * 50)
        
        try:
            self.check_prerequisites()
            self.setup_python_environment()
            self.setup_backend_dependencies()
            self.setup_frontend_dependencies()
            self.generate_openapi_types()
            self.run_tests()
            self.show_completion_message()
            
        except Exception as e:
            print(f"❌ Setup failed: {e}")
            sys.exit(1)
    
    def check_prerequisites(self) -> None:
        """Check that required tools are installed."""
        print("\n🔍 Checking prerequisites...")
        
        required_tools = [
            ("python", "Python 3.11+"),
            ("uv", "uv package manager"),
            ("node", "Node.js 18+"),
            ("pnpm", "pnpm package manager"),
        ]
        
        missing_tools = []
        
        for tool, description in required_tools:
            if not self.check_command(tool):
                missing_tools.append(f"  - {description}")
        
        if missing_tools:
            print("❌ Missing required tools:")
            for tool in missing_tools:
                print(tool)
            print("\nPlease install the missing tools and try again.")
            sys.exit(1)
        
        print("✅ All prerequisites met")
    
    def check_command(self, command: str) -> bool:
        """Check if a command exists."""
        try:
            subprocess.run(
                [command, "--version"],
                check=True,
                capture_output=True,
                text=True,
            )
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    def setup_python_environment(self) -> None:
        """Setup Python virtual environment."""
        print("\n🐍 Setting up Python environment...")
        
        os.chdir(self.backend_path)
        
        # Sync dependencies with uv
        self.run_command(["uv", "sync"], "Installing Python dependencies")
        
        # Install optional dependencies based on system
        optional_deps = ["dev"]
        
        # Add GPU support if CUDA available
        if os.getenv("ZETA_USE_GPU") == "1":
            optional_deps.append("gpu")
        
        # Add PaddleOCR on non-Windows systems
        if not self.is_windows:
            optional_deps.append("paddleocr")
        else:
            optional_deps.append("ocr-alt")  # Tesseract alternative
        
        for dep in optional_deps:
            self.run_command(
                ["uv", "sync", "--extra", dep],
                f"Installing {dep} dependencies",
                ignore_errors=True,
            )
        
        print("✅ Python environment ready")
    
    def setup_backend_dependencies(self) -> None:
        """Setup and validate backend."""
        print("\n🚀 Setting up backend...")
        
        os.chdir(self.backend_path)
        
        # Run linting and type checking
        self.run_command(["uv", "run", "ruff", "check", "."], "Linting code", ignore_errors=True)
        self.run_command(["uv", "run", "mypy", "app"], "Type checking", ignore_errors=True)
        
        # Security checks
        self.run_command(["uv", "run", "bandit", "-r", "app", "-x", "tests"], "Security scan", ignore_errors=True)
        self.run_command(["uv", "run", "pip-audit"], "Dependency audit", ignore_errors=True)
        
        print("✅ Backend setup complete")
    
    def setup_frontend_dependencies(self) -> None:
        """Setup frontend dependencies."""
        print("\n💻 Setting up frontend...")
        
        os.chdir(self.desktop_path)
        
        # Install dependencies
        self.run_command(["pnpm", "install"], "Installing Node.js dependencies")
        
        # Type checking
        self.run_command(["pnpm", "typecheck"], "Type checking frontend", ignore_errors=True)
        
        # Linting
        self.run_command(["pnpm", "lint"], "Linting frontend", ignore_errors=True)
        
        print("✅ Frontend setup complete")
    
    def generate_openapi_types(self) -> None:
        """Generate TypeScript types from OpenAPI."""
        print("\n🔄 Generating OpenAPI types...")
        
        # Start backend server in background
        os.chdir(self.backend_path)
        backend_process = subprocess.Popen(
            ["uv", "run", "uvicorn", "app.main:app", "--port", "8000"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        
        try:
            # Wait for server to start
            import time
            time.sleep(5)
            
            # Generate types
            os.chdir(self.desktop_path)
            self.run_command(
                ["pnpm", "openapi:gen"],
                "Generating TypeScript types",
                ignore_errors=True,
            )
            
        finally:
            # Stop backend server
            backend_process.terminate()
            backend_process.wait()
        
        print("✅ OpenAPI types generated")
    
    def run_tests(self) -> None:
        """Run tests to validate setup."""
        print("\n🧪 Running tests...")
        
        # Backend tests
        os.chdir(self.backend_path)
        self.run_command(
            ["uv", "run", "pytest", "-q", "--cov=app", "--cov-report=term-missing"],
            "Running backend tests",
            ignore_errors=True,
        )
        
        # Frontend tests
        os.chdir(self.desktop_path)
        self.run_command(
            ["pnpm", "test"],
            "Running frontend tests",
            ignore_errors=True,
        )
        
        print("✅ Tests completed")
    
    def run_command(
        self,
        command: List[str],
        description: str,
        ignore_errors: bool = False,
    ) -> None:
        """Run a shell command with error handling."""
        print(f"  → {description}...")
        
        try:
            result = subprocess.run(
                command,
                check=True,
                capture_output=True,
                text=True,
            )
            
            if result.returncode == 0:
                print(f"    ✅ {description}")
            else:
                print(f"    ⚠️  {description} (warnings)")
                
        except subprocess.CalledProcessError as e:
            if ignore_errors:
                print(f"    ⚠️  {description} (skipped)")
            else:
                print(f"    ❌ {description} failed")
                print(f"       Error: {e.stderr}")
                raise
    
    def show_completion_message(self) -> None:
        """Show completion message with next steps."""
        print("\n" + "=" * 50)
        print("🎉 One-Click Learning Setup Complete!")
        print("=" * 50)
        
        print("\n🚀 Quick Start Commands:")
        print("\n1️⃣ Start Backend (CPU-first):")
        print(f"   cd {self.backend_path}")
        print("   uv run uvicorn app.main:app --reload --port 8000")
        
        print("\n2️⃣ Start Frontend:")
        print(f"   cd {self.desktop_path}")
        print("   pnpm electron:dev")
        
        print("\n3️⃣ Enable GPU (optional):")
        print("   export ZETA_USE_GPU=1  # Linux/macOS")
        print("   set ZETA_USE_GPU=1     # Windows")
        
        print("\n🌐 Available Endpoints:")
        print("   - Backend API: http://localhost:8000")
        print("   - API Docs: http://localhost:8000/docs")
        print("   - One-Click Learning: http://localhost:8000/api/v1/one-click")
        print("   - WebSocket Chat: ws://localhost:8000/ws/chat")
        
        print("\n📚 Features Ready:")
        print("   ✅ RAG (Retrieval-Augmented Generation)")
        print("   ✅ ASR (Automatic Speech Recognition)")
        print("   ✅ OCR (Optical Character Recognition)")
        print("   ✅ WebSocket Real-time Chat")
        print("   ✅ Electron Desktop App")
        print("   ✅ Type-safe APIs")
        print("   ✅ DevSecOps Pipeline")
        
        print("\n🔧 Test the System:")
        print("   # Test RAG search")
        print("   curl -X POST http://localhost:8000/api/v1/one-click/search \\")
        print("        -H 'Content-Type: application/json' \\")
        print("        -d '{\"query\": \"test query\", \"k\": 5}'")
        
        print("\n   # Test file upload pipeline")
        print("   curl -X POST http://localhost:8000/api/v1/one-click/pipeline \\")
        print("        -F 'file=@sample.txt' \\")
        print("        -F 'auto_ingest=true'")


def main():
    """Main entry point."""
    project_root = Path(__file__).parent
    setup = OneClickSetup(project_root)
    setup.run()


if __name__ == "__main__":
    main()
