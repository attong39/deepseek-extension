#!/usr/bin/env python3
# 🚀 Zeta Development Setup Script

import os
import subprocess
import sys
from pathlib import Path
import Exception
import bool
import command
import config
import cwd
import description
import e
import name
import print
import req_file
import step_func
import step_name
import str
import title
import tuple

# Constants
NPM_INSTALL = "npm install"


def print_header(title: str) -> None:
    """Print a formatted header"""
    print("\n" + "=" * 60)
    print(f"🎯 {title}")
    print("=" * 60)


def run_command(command: str, description: str, cwd: str | None = None) -> bool:
    """Run a command and return success status"""
    print(f"\n🔄 {description}")
    print(f"Running: {command}")

    try:
        result = subprocess.run(command, shell=False, capture_output=True, text=True, cwd=cwd)
        if result.returncode == 0:
            print(f"✅ {description} completed successfully")
            if result.stdout.strip():
                print(f"Output: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ {description} failed")
            print(f"Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Failed to run command: {e}")
        return False


def check_prerequisites() -> bool:
    """Check if all prerequisites are installed"""
    print_header("Checking Prerequisites")

    prerequisites = [
        ("python", "python --version", "Python 3.11+"),
        ("pip", "pip --version", "Python package manager"),
        ("node", "node --version", "Node.js 18+"),
        ("npm", "npm --version", "Node package manager"),
        ("git", "git --version", "Git version control"),
    ]

    all_ok = True
    for name, command, description in prerequisites:
        print(f"\n🔍 Checking {name} ({description})")
        if not run_command(command, f"Check {name}"):
            all_ok = False
            print(f"💡 Please install {description}")

    return all_ok


def get_python_paths() -> tuple[str, str]:
    """Get Python and pip paths for current environment"""
    if os.name == "nt":  # Windows
        pip_path = ".venv\\Scripts\\pip"
        python_path = ".venv\\Scripts\\python"
    else:  # Unix/Linux/macOS
        pip_path = ".venv/bin/pip"
        python_path = ".venv/bin/python"
    return python_path, pip_path


def install_requirements(pip_path: str) -> bool:
    """Install Python requirements from zeta-ai-agent directory"""
    zeta_agent_path = Path("zeta-ai-agent")
    if not zeta_agent_path.exists():
        return True

    requirements_files = ["requirements-dev.txt", "requirements-optimization.txt"]

    for req_file in requirements_files:
        req_path = zeta_agent_path / req_file
        if req_path.exists() and not run_command(
            f"{pip_path} install -r {req_path}", f"Install {req_file}", cwd=str(zeta_agent_path)
        ):
            print(f"⚠️ Failed to install {req_file}, continuing...")

    return True


def setup_python_environment() -> bool:
    """Setup Python virtual environment"""
    print_header("Setting up Python Environment")

    venv_path = Path(".venv")

    # Create virtual environment if it doesn't exist
    if not venv_path.exists():
        if not run_command("python -m venv .venv", "Create Python virtual environment"):
            return False
    else:
        print("✅ Virtual environment already exists")

    # Get paths for current environment
    python_path, pip_path = get_python_paths()

    # Install/upgrade pip
    if not run_command(f"{python_path} -m pip install --upgrade pip", "Upgrade pip"):
        return False

    # Install requirements
    return install_requirements(pip_path)


def setup_node_dependencies() -> bool:
    """Setup Node.js dependencies"""
    print_header("Setting up Node.js Dependencies")

    # Install root dependencies
    if not run_command(NPM_INSTALL, "Install root Node dependencies"):
        return False

    # Install extension dependencies
    extension_path = Path("extension")
    if extension_path.exists():
        if not run_command(NPM_INSTALL, "Install extension dependencies", cwd="extension"):
            return False

    # Install desktop dependencies
    desktop_path = Path("desktop")
    if desktop_path.exists():
        if not run_command(NPM_INSTALL, "Install desktop dependencies", cwd="desktop"):
            return False

    return True


def create_development_configs() -> bool:
    """Create development configuration files"""
    print_header("Creating Development Configurations")

    # Check if .env already exists in zeta-ai-agent
    zeta_env_path = Path("zeta-ai-agent/.env")
    if zeta_env_path.exists():
        print("✅ Development .env file already exists")
    else:
        env_example_path = Path("zeta-ai-agent/.env.example")
        if env_example_path.exists():
            try:
                import shutil

                shutil.copy(env_example_path, zeta_env_path)
                print("✅ Created .env from .env.example")
            except Exception as e:
                print(f"⚠️ Failed to copy .env.example: {e}")

    # Check VS Code configurations
    vscode_path = Path(".vscode")
    if vscode_path.exists():
        print("✅ VS Code configuration directory exists")

        required_configs = ["launch.json", "tasks.json", "settings.json"]
        for config in required_configs:
            config_path = vscode_path / config
            if config_path.exists():
                print(f"✅ {config} exists")
            else:
                print(f"⚠️ {config} missing")

    return True


def build_projects() -> bool:
    """Build all projects"""
    print_header("Building Projects")

    # Build extension
    extension_path = Path("extension")
    if extension_path.exists():
        if not run_command("npm run compile", "Build extension", cwd="extension"):
            print("⚠️ Extension build failed, continuing...")

    # Build desktop app
    desktop_path = Path("desktop")
    if desktop_path.exists():
        if not run_command("npm run build", "Build desktop app", cwd="desktop"):
            print("⚠️ Desktop app build failed, continuing...")

    return True


def test_setup() -> bool:
    """Test the development setup"""
    print_header("Testing Development Setup")

    # Test Python environment
    python_path, _ = get_python_paths()

    test_commands = [
        (f"{python_path} -c \"import fastapi; print('✅ FastAPI available')\"", "Test FastAPI import"),
        (f"{python_path} -c \"import uvicorn; print('✅ Uvicorn available')\"", "Test Uvicorn import"),
        ("node --version", "Test Node.js"),
        ("npm --version", "Test npm"),
    ]

    all_tests_passed = True
    for command, description in test_commands:
        if not run_command(command, description):
            all_tests_passed = False

    return all_tests_passed


def show_next_steps() -> None:
    """Show next steps for development"""
    print_header("🎉 Development Setup Complete!")

    python_path, _ = get_python_paths()

    print("\n🚀 Next Steps:")
    print("\n1️⃣ Start the development server:")
    print(f"   {python_path} zeta-ai-agent\\dev_server.py")

    print("\n2️⃣ Or use VS Code tasks:")
    print("   • Press Ctrl+Shift+P")
    print("   • Type 'Tasks: Run Task'")
    print("   • Select '🚀 Full Stack Development'")

    print("\n3️⃣ Debug in VS Code:")
    print("   • Press F5")
    print("   • Select '🚀 Full Stack Development'")
    print("   • Set breakpoints and debug!")

    print("\n4️⃣ Test the setup:")
    print("   • Server: http://127.0.0.1:9100")
    print("   • Health: http://127.0.0.1:9100/health")
    print("   • Dev Info: http://127.0.0.1:9100/dev")

    print("\n💡 Useful Commands:")
    print("   npm run dev                    # Start all services")
    print("   npm run build                  # Build all projects")
    print("   npm run test                   # Run all tests")

    print("\n🔧 VS Code Features:")
    print("   • IntelliSense for Python & TypeScript")
    print("   • Integrated debugging")
    print("   • Auto-reload on file changes")
    print("   • Extension development mode")

    print("\n📁 Project Structure:")
    print("   • backend/           - FastAPI backend services")
    print("   • extension/         - VS Code extension")
    print("   • desktop/           - Electron desktop app")
    print("   • zeta-ai-agent/     - Optimized AI agent server")
    print("   • .vscode/           - VS Code configurations")


def main() -> None:
    """Main setup function"""
    print("🚀 Zeta AI Agent - Development Environment Setup")
    print("This script will prepare your local development environment")

    # Change to script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)

    print(f"\n📍 Working directory: {os.getcwd()}")

    setup_steps = [
        (check_prerequisites, "Check Prerequisites"),
        (setup_python_environment, "Setup Python Environment"),
        (setup_node_dependencies, "Setup Node Dependencies"),
        (create_development_configs, "Create Development Configs"),
        (build_projects, "Build Projects"),
        (test_setup, "Test Setup"),
    ]

    for step_func, step_name in setup_steps:
        if not step_func():
            print(f"\n❌ Setup failed at step: {step_name}")
            print("\n💡 Try running the script again or check the error messages above")
            sys.exit(1)

    show_next_steps()


if __name__ == "__main__":
    main()
