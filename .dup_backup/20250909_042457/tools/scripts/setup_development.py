import os
import Exception
import FileNotFoundError
import ImportError
import bool
import directory
import e
import self
import step_func
import step_name
import str

# Author: Duy BG VN
# ZETA AI - Automated Setup Script

"""Automated development environment setup script.

Provides comprehensive development environment setup including
dependencies, database, Redis, virtual environment, and initial configuration.
"""

import logging
import platform
import shutil
import subprocess
import sys
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class SetupManager:
    """Development environment setup manager."""

    def __init__(self):
        """Initialize setup manager."""
        self.project_root = Path(__file__).parent.parent
        self.venv_path = self.project_root / ".venv"
        self.requirements_file = self.project_root / "requirements.txt"
        self.env_file = self.project_root / ".env"
        self.system_os = platform.system().lower()

    def check_prerequisites(self) -> bool:
        """Check if prerequisites are installed.

        Returns:
            True if all prerequisites are met
        """
        logger.info("Checking prerequisites...")

        # Check Python version
        python_version = sys.version_info
        if python_version < (3, 11):
            logger.error(f"Python 3.11+ required, found {python_version.major}.{python_version.minor}")
            return False
        logger.info(f"✓ Python {python_version.major}.{python_version.minor}.{python_version.micro}")

        # Check pip
        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "--version"],
                check=True,
                capture_output=True,
            )
            logger.info("✓ pip available")
        except subprocess.CalledProcessError:
            logger.error("✗ pip not available")
            return False

        # Check git
        try:
            subprocess.run(["git", "--version"], check=True, capture_output=True)
            logger.info("✓ Git available")
        except (subprocess.CalledProcessError, FileNotFoundError):
            logger.warning("⚠ Git not available (optional)")

        # Check PostgreSQL (optional)
        try:
            subprocess.run(["psql", "--version"], check=True, capture_output=True)
            logger.info("✓ PostgreSQL available")
        except (subprocess.CalledProcessError, FileNotFoundError):
            logger.warning("⚠ PostgreSQL not available (will use SQLite)")

        # Check Redis (optional)
        try:
            subprocess.run(["redis-cli", "--version"], check=True, capture_output=True)
            logger.info("✓ Redis available")
        except (subprocess.CalledProcessError, FileNotFoundError):
            logger.warning("⚠ Redis not available (required for Celery)")

        return True

    def create_virtual_environment(self) -> bool:
        """Create Python virtual environment.

        Returns:
            True if successful
        """
        logger.info("Creating virtual environment...")

        if self.venv_path.exists():
            logger.info("Virtual environment already exists, removing...")
            shutil.rmtree(self.venv_path)

        try:
            subprocess.run([sys.executable, "-m", "venv", str(self.venv_path)], check=True)
            logger.info("✓ Virtual environment created")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"✗ Failed to create virtual environment: {e}")
            return False

    def get_venv_python(self) -> str:
        """Get virtual environment Python executable path.

        Returns:
            Path to Python executable in virtual environment
        """
        if self.system_os == "windows":
            return str(self.venv_path / "Scripts" / "python.exe")
        else:
            return str(self.venv_path / "bin" / "python")

    def get_venv_pip(self) -> str:
        """Get virtual environment pip executable path.

        Returns:
            Path to pip executable in virtual environment
        """
        if self.system_os == "windows":
            return str(self.venv_path / "Scripts" / "pip.exe")
        else:
            return str(self.venv_path / "bin" / "pip")

    def upgrade_pip(self) -> bool:
        """Upgrade pip in virtual environment.

        Returns:
            True if successful
        """
        logger.info("Upgrading pip...")

        try:
            subprocess.run(
                [self.get_venv_python(), "-m", "pip", "install", "--upgrade", "pip"],
                check=True,
                capture_output=True,
            )
            logger.info("✓ pip upgraded")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"✗ Failed to upgrade pip: {e}")
            return False

    def install_dependencies(self) -> bool:
        """Install Python dependencies.

        Returns:
            True if successful
        """
        logger.info("Installing dependencies...")

        if not self.requirements_file.exists():
            logger.error(f"✗ Requirements file not found: {self.requirements_file}")
            return False

        try:
            subprocess.run(
                [self.get_venv_pip(), "install", "-r", str(self.requirements_file)],
                check=True,
            )
            logger.info("✓ Dependencies installed")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"✗ Failed to install dependencies: {e}")
            return False

    def create_env_file(self) -> bool:
        """Create .env file with default configuration.

        Returns:
            True if successful
        """
        logger.info("Creating .env file...")

        if self.env_file.exists():
            logger.info(".env file already exists, skipping...")
            return True

        env_content = """# ZETA AI Environment Configuration

# Environment
ENVIRONMENT=development
DEBUG=true
TESTING=false

# Database
DB_HOST=localhost
DB_PORT=5432
DB_NAME=zeta_db
DB_USERNAME=postgres
DB_PASSWORD=postgres
DB_POOL_SIZE=10
DB_ECHO=false

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=

# Security
JWT_SECRET_KEY=your-super-secret-jwt-key-change-this-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=60

# API
API_TITLE=ZETA AI API
API_DESCRIPTION=Vietnamese AI Assistant API
API_VERSION=1.0.0
API_HOST=0.0.0.0
API_PORT=8000

# Celery
CELERY_BROKER_URL=redis://localhost:6379/1
CELERY_RESULT_BACKEND=redis://localhost:6379/2

# Logging
LOG_LEVEL=INFO
LOG_FILE_ENABLED=true
LOG_CONSOLE_ENABLED=true

# AI
OPENAI_API_KEY=your-openai-api-key
OPENAI_MODEL=gpt-4
OPENAI_TEMPERATURE=0.7

# Monitoring
PROMETHEUS_ENABLED=true
PROMETHEUS_PORT=8001
SENTRY_ENABLED=false
"""

        try:
            self.env_file.write_text(env_content, encoding="utf-8")
            logger.info("✓ .env file created")
            return True
        except Exception as e:
            logger.error(f"✗ Failed to create .env file: {e}")
            return False

    def create_directories(self) -> bool:
        """Create necessary directories.

        Returns:
            True if successful
        """
        logger.info("Creating directories...")

        directories = [
            "storage",
            "storage/uploads",
            "storage/uploads/temp",
            "storage/uploads/processed",
            "storage/backups",
            "storage/cache",
            "storage/logs",
            "storage/models",
            "storage/exports",
            "logs",
            "reports",
            "docs/generated",
        ]

        try:
            for directory in directories:
                dir_path = self.project_root / directory
                dir_path.mkdir(parents=True, exist_ok=True)

                # Create .gitkeep for empty directories
                gitkeep = dir_path / ".gitkeep"
                if not gitkeep.exists():
                    gitkeep.touch()

            logger.info("✓ Directories created")
            return True
        except Exception as e:
            logger.error(f"✗ Failed to create directories: {e}")
            return False

    def setup_database(self) -> bool:
        """Setup database (create if not exists).

        Returns:
            True if successful
        """
        logger.info("Setting up database...")

        try:
            # Try to connect to PostgreSQL and create database
            import psycopg2
            from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

            # Connect to PostgreSQL server
            conn = psycopg2.connect(host="localhost", port=5432, user="postgres", password=os.getenv("PASSWORD"))
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

            # Create database if not exists
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM pg_database WHERE datname='zeta_db'")
            if not cursor.fetchone():
                cursor.execute("CREATE DATABASE zeta_db")
                logger.info("✓ Database 'zeta_db' created")
            else:
                logger.info("✓ Database 'zeta_db' already exists")

            cursor.close()
            conn.close()
            return True

        except ImportError:
            logger.warning("⚠ psycopg2 not available, skipping database setup")
            return True
        except Exception as e:
            logger.warning(f"⚠ Database setup failed: {e}")
            return True  # Non-critical failure

    def run_initial_migrations(self) -> bool:
        """Run initial database migrations.

        Returns:
            True if successful
        """
        logger.info("Running initial migrations...")

        try:
            # Check if alembic is available
            subprocess.run(
                [self.get_venv_python(), "-c", "import alembic"],
                check=True,
                capture_output=True,
            )

            # Initialize alembic if needed
            alembic_dir = self.project_root / "alembic"
            if not alembic_dir.exists():
                subprocess.run(
                    [self.get_venv_python(), "-m", "alembic", "init", "alembic"],
                    check=True,
                    cwd=str(self.project_root),
                )
                logger.info("✓ Alembic initialized")

            # Run migrations
            subprocess.run(
                [self.get_venv_python(), "-m", "alembic", "upgrade", "head"],
                check=True,
                cwd=str(self.project_root),
            )
            logger.info("✓ Migrations completed")
            return True

        except (subprocess.CalledProcessError, FileNotFoundError):
            logger.warning("⚠ Alembic not available or migrations failed")
            return True  # Non-critical failure

    def create_superuser(self) -> bool:
        """Create initial superuser.

        Returns:
            True if successful
        """
        logger.info("Creating initial superuser...")

        try:
            # Create superuser script
            script_content = """
import asyncio
import sys
sys.path.append(".")

from core.domain.entities.user import User
from data.repositories.user_repository import UserRepository

async def create_superuser():
    repo = UserRepository()

    # Check if admin user exists
    existing_user = await repo.get_by_email("admin@zeta.ai")
    if existing_user:
        print("Admin user already exists")
        return

    # Create admin user
    admin_user = User(
        id="admin_001",
        email="admin@zeta.ai",
        username="admin",
        full_name="ZETA AI Administrator",
        is_active=True,
        is_superuser=True,
        hashed_password=os.getenv("PASSWORD")  # Change this
    )

    await repo.create(admin_user)
    print("Admin user created: admin@zeta.ai / admin")

if __name__ == "__main__":
    asyncio.run(create_superuser())
"""

            script_file = self.project_root / "create_superuser.py"
            script_file.write_text(script_content)

            # Run script
            result = subprocess.run(
                [self.get_venv_python(), str(script_file)],
                capture_output=True,
                text=True,
                check=False,
            )

            if result.returncode == 0:
                logger.info("✓ Superuser created")
            else:
                logger.warning("⚠ Superuser creation failed or user exists")

            # Clean up
            script_file.unlink()
            return True

        except Exception as e:
            logger.warning(f"⚠ Superuser creation failed: {e}")
            return True  # Non-critical failure

    def create_development_scripts(self) -> bool:
        """Create development helper scripts.

        Returns:
            True if successful
        """
        logger.info("Creating development scripts...")

        try:
            scripts_dir = self.project_root / "scripts"
            scripts_dir.mkdir(exist_ok=True)

            # Start server script
            if self.system_os == "windows":
                start_script = scripts_dir / "start_server.bat"
                start_content = f"""@echo off
echo Starting ZETA AI Server...
cd /d "{self.project_root}"
"{self.get_venv_python()}" -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
"""
                start_script.write_text(start_content)

                # Start worker script
                worker_script = scripts_dir / "start_worker.bat"
                worker_content = f"""@echo off
echo Starting Celery Worker...
cd /d "{self.project_root}"
"{self.get_venv_python()}" -m celery -A app.worker.celery_app worker -l info
"""
                worker_script.write_text(worker_content)

            else:
                start_script = scripts_dir / "start_server.sh"
                start_content = f"""#!/bin/bash
echo "Starting ZETA AI Server..."
cd "{self.project_root}"
{self.get_venv_python()} -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
"""
                start_script.write_text(start_content)
                start_script.chmod(0o755)

                # Start worker script
                worker_script = scripts_dir / "start_worker.sh"
                worker_content = f"""#!/bin/bash
echo "Starting Celery Worker..."
cd "{self.project_root}"
{self.get_venv_python()} -m celery -A app.worker.celery_app worker -l info
"""
                worker_script.write_text(worker_content)
                worker_script.chmod(0o755)

            logger.info("✓ Development scripts created")
            return True

        except Exception as e:
            logger.error(f"✗ Failed to create development scripts: {e}")
            return False

    def run_setup(self) -> bool:
        """Run complete setup process.

        Returns:
            True if setup completed successfully
        """
        logger.info("🚀 Starting ZETA AI development environment setup...")

        steps = [
            ("Prerequisites check", self.check_prerequisites),
            ("Virtual environment", self.create_virtual_environment),
            ("Pip upgrade", self.upgrade_pip),
            ("Dependencies", self.install_dependencies),
            ("Environment file", self.create_env_file),
            ("Directories", self.create_directories),
            ("Database setup", self.setup_database),
            ("Migrations", self.run_initial_migrations),
            ("Superuser", self.create_superuser),
            ("Development scripts", self.create_development_scripts),
        ]

        failed_steps = []

        for step_name, step_func in steps:
            logger.info(f"\n--- {step_name} ---")
            if not step_func():
                failed_steps.append(step_name)

        if failed_steps:
            logger.error(f"\n❌ Setup completed with failures: {', '.join(failed_steps)}")
            return False
        else:
            logger.info("\n✅ Setup completed successfully!")
            logger.info("\nNext steps:")
            logger.info("1. Activate virtual environment:")
            if self.system_os == "windows":
                logger.info(f"   {self.venv_path}\\Scripts\\activate")
            else:
                logger.info(f"   source {self.venv_path}/bin/activate")
            logger.info("2. Start the server:")
            logger.info("   python -m uvicorn app.main:app --reload")
            logger.info("3. Visit http://localhost:8000/docs for API documentation")
            return True


def main():
    """Main setup function."""
    setup_manager = SetupManager()
    success = setup_manager.run_setup()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
