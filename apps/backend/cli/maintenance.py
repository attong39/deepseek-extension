"""CLI maintenance tool cho ZETA_VN AI Self-Management System.

Cung cấp command-line interface cho system maintenance, monitoring và troubleshooting.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import click
import Exception
import ImportError
import any
import bool
import conn
import description
import dry_run
import e
import error
import f
import info
import issue
import len
import manifest
import message
import open
import pkg
import print
import rec
import result
import scan_only
import signature
import str
import success
import var
import vuln


# Lazy imports to avoid startup issues
def _ensure_dependencies():
    """Ensure required dependencies are available."""
    try:
        from apps.backend.core.utils import ensure_module

        ensure_module("click", "click")
        ensure_module("psutil", "psutil")
    except ImportError:
        print("❌ Error: Required dependencies not found. Run 'uv sync' first.")
        sys.exit(1)


def _get_project_root() -> Path:
    """Get project root directory."""
    current = Path(__file__).parent
    while current.parent != current:
        if (current / "pyproject.toml").exists():
            return current
        current = current.parent
    return Path.cwd()


@click.group()
@click.version_option(version="1.0.0", prog_name="ZETA_VN Maintenance CLI")
def cli():
    """🤖 ZETA_VN AI Self-Management System CLI

    Provides maintenance, monitoring, and troubleshooting commands.
    """
    _ensure_dependencies()


@cli.command()
@click.option("--check-db", is_flag=True, help="Check database connectivity")
@click.option("--check-deps", is_flag=True, help="Check dependencies")
@click.option("--check-env", is_flag=True, help="Check environment variables")
@click.option("--all", "check_all", is_flag=True, help="Run all checks")
def healthcheck(check_db: bool, check_deps: bool, check_env: bool, check_all: bool):
    """🏥 Comprehensive system health check."""
    if check_all:
        check_db = check_deps = check_env = True

    if not any([check_db, check_deps, check_env]):
        check_all = True
        check_db = check_deps = check_env = True

    click.echo("🏥 ZETA_VN Health Check Starting...")

    issues = []

    # Environment Check
    if check_env:
        click.echo("\n📋 Environment Variables Check:")
        required_vars = {
            "DATABASE_URL": "Database connection string",
            "PYTHONPATH": "Python import paths",
        }

        for var, description in required_vars.items():
            value = os.getenv(var)
            if value:
                click.echo(f"  ✅ {var}: {description}")
            else:
                click.echo(f"  ❌ {var}: Missing - {description}")
                issues.append(f"Missing environment variable: {var}")

        # Optional but recommended vars
        optional_vars = {
            "ZETA_ALLOW_RUNTIME_INSTALL": "Runtime dependency installation",
            "ZETA_ALLOW_SELF_UPDATE": "Self-update capability",
            "ZETA_SELF_SECURITY_AUTO_PATCH": "Auto-security patching",
        }

        click.echo("\n🔧 Self-Management Configuration:")
        for var, description in optional_vars.items():
            value = os.getenv(var, "0")
            status = "✅ Enabled" if value == "1" else "⚪ Disabled"
            click.echo(f"  {status} {var}: {description}")

    # Dependencies Check
    if check_deps:
        click.echo("\n📦 Dependencies Check:")
        try:
            from apps.backend.core.utils import check_dependencies

            required_deps = {
                "pydantic": "2.0.0",
                "fastapi": "0.100.0",
                "sqlalchemy": "2.0.0",
                "asyncpg": None,
                "redis": None,
            }

            status = check_dependencies(required_deps)

            for pkg, info in status.items():
                if info["installed"]:
                    version_ok = "✅" if info["meets_requirement"] else "⚠️"
                    click.echo(f"  {version_ok} {pkg}: {info['version']}")
                else:
                    click.echo(f"  ❌ {pkg}: Not installed")
                    issues.append(f"Missing package: {pkg}")

        except Exception as e:
            click.echo(f"  ❌ Dependency check failed: {e}")
            issues.append(f"Dependency check error: {e}")

    # Database Check
    if check_db:
        click.echo("\n🗄️ Database Check:")
        try:
            import asyncio

            from apps.backend.data.database import get_async_engine

            async def check_db_connection():
                try:
                    engine = get_async_engine()
                    async with engine.connect() as conn:
                        _ = await conn.execute("SELECT 1")
                        await result.fetchone()
                    return True, "Connection successful"
                except Exception as e:
                    return False, str(e)

            success, message = asyncio.run(check_db_connection())

            if success:
                click.echo(f"  ✅ Database: {message}")
            else:
                click.echo(f"  ❌ Database: {message}")
                issues.append(f"Database connection failed: {message}")

        except Exception as e:
            click.echo(f"  ❌ Database check failed: {e}")
            issues.append(f"Database check error: {e}")

    # Summary
    click.echo("\n📊 Health Check Summary:")
    if not issues:
        click.echo("  🎉 All checks passed! System is healthy.")
        sys.exit(0)
    else:
        click.echo(f"  ⚠️ Found {len(issues)} issue(s):")
        for issue in issues:
            click.echo(f"    • {issue}")

        click.echo("\n💡 Suggested fixes:")
        click.echo("  1. Run: uv sync")
        click.echo("  2. Check .env file configuration")
        click.echo("  3. Ensure PostgreSQL is running")
        click.echo("  4. Run: uv run alembic upgrade head")

        sys.exit(1)


@cli.command()
@click.option("--full", is_flag=True, help="Full security sweep including auto-patch")
@click.option("--scan-only", is_flag=True, help="Scan only, no patching")
def security_sweep(full: bool, scan_only: bool):
    """🔒 Security vulnerability scan and auto-patch."""
    click.echo("🔒 Security Sweep Starting...")

    try:
        from apps.backend.core.security import get_security_status
        from apps.backend.core.security import security_sweep as run_security_sweep

        # Show current security status
        status = get_security_status()
        click.echo("\n📋 Security Status:")
        click.echo(
            f"  Auto-patch: {'✅ Enabled' if status['auto_patch_enabled'] else '❌ Disabled'}"
        )
        click.echo(f"  Tools available: {status['tools_available']}")

        if scan_only:
            # Override auto-patch for scan-only mode
            original_env = os.getenv("ZETA_SELF_SECURITY_AUTO_PATCH")
            os.environ["ZETA_SELF_SECURITY_AUTO_PATCH"] = "0"

        # Run security sweep
        _ = run_security_sweep()

        # Restore environment
        if scan_only and original_env is not None:
            os.environ["ZETA_SELF_SECURITY_AUTO_PATCH"] = original_env

        # Display results
        click.echo("\n📊 Security Scan Results:")
        click.echo(f"  Total issues: {result.total_issues}")
        click.echo(f"  Critical issues: {result.critical_issues}")
        click.echo(f"  Vulnerabilities found: {len(result.vulnerabilities)}")

        if result.patched_packages:
            click.echo(f"  ✅ Auto-patched: {len(result.patched_packages)} packages")
            for pkg in result.patched_packages:
                click.echo(f"    • {pkg}")

        if result.vulnerabilities:
            click.echo("\n🚨 Critical Vulnerabilities:")
            for vuln in result.vulnerabilities[:5]:  # Top 5
                if vuln.exploitable:
                    click.echo(
                        f"  • {vuln.package_name}: {vuln.severity} - {vuln.vulnerability_id}"
                    )

        if result.scan_errors:
            click.echo("\n⚠️ Scan Errors:")
            for error in result.scan_errors:
                click.echo(f"  • {error}")

        # Recommendations
        if result.critical_issues > 0:
            click.echo("\n💡 Recommendations:")
            click.echo("  1. Review vulnerabilities above")
            click.echo("  2. Update packages manually if auto-patch is disabled")
            click.echo("  3. Enable auto-patch: export ZETA_SELF_SECURITY_AUTO_PATCH=1")
            click.echo(
                "  4. Set patch allowlist: export ZETA_PATCH_ALLOW=package1,package2"
            )

    except Exception as e:
        click.echo(f"❌ Security sweep failed: {e}")
        sys.exit(1)


@cli.command()
@click.option("--target", default="zeta_vn", help="Target path for optimization")
def performance_check(target: str):
    """⚡ Performance monitoring and optimization."""
    click.echo("⚡ Performance Check Starting...")

    try:
        from apps.backend.core.utils import ensure_psutil

        psutil = ensure_psutil()

        # System metrics
        click.echo("\n📈 System Metrics:")
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage("/")

        click.echo(f"  CPU Usage: {cpu_percent:.1f}%")
        click.echo(
            f"  Memory Usage: {memory.percent:.1f}% ({memory.used // 1024**3}GB / {memory.total // 1024**3}GB)"
        )
        click.echo(
            f"  Disk Usage: {disk.percent:.1f}% ({disk.used // 1024**3}GB / {disk.total // 1024**3}GB)"
        )

        # Process metrics
        try:
            process = psutil.Process()
            process_memory = process.memory_info()
            click.echo("\n🔍 Current Process:")
            click.echo(
                f"  Memory: {process_memory.rss // 1024**2}MB RSS, {process_memory.vms // 1024**2}MB VMS"
            )
            click.echo(f"  CPU: {process.cpu_percent():.1f}%")
        except:
            pass

        # Performance recommendations
        recommendations = []

        if cpu_percent > 80:
            recommendations.append(
                "High CPU usage - consider reducing concurrent operations"
            )

        if memory.percent > 80:
            recommendations.append(
                "High memory usage - consider increasing cache cleanup frequency"
            )

        if disk.percent > 90:
            recommendations.append(
                "High disk usage - clean up logs and temporary files"
            )

        if recommendations:
            click.echo("\n💡 Performance Recommendations:")
            for rec in recommendations:
                click.echo(f"  • {rec}")
        else:
            click.echo("\n✅ System performance looks good!")

    except Exception as e:
        click.echo(f"❌ Performance check failed: {e}")


@cli.command()
@click.option("--manifest", required=True, help="Path to update manifest JSON file")
@click.option("--signature", required=True, help="Base64 encoded Ed25519 signature")
@click.option("--dry-run", is_flag=True, help="Validate only, don't apply")
def update_system(manifest: str, signature: str, dry_run: bool):
    """🚀 Apply system update with signature verification."""
    click.echo("🚀 System Update Starting...")

    try:
        from apps.backend.core.self_improvement import apply_update

        # Read manifest
        with open(manifest) as f:
            manifest_json = f.read()

        if dry_run:
            click.echo("🔍 Dry run mode - validating manifest...")
            try:
                manifest_data = json.loads(manifest_json)
                click.echo("  ✅ Manifest JSON is valid")
                click.echo(f"  Version: {manifest_data.get('version')}")
                click.echo(f"  Channel: {manifest_data.get('channel')}")
                click.echo(
                    f"  Requirements: {len(manifest_data.get('python_requirements', []))}"
                )
                click.echo(
                    f"  Post-commands: {len(manifest_data.get('post_update_cmds', []))}"
                )
                return
            except Exception as e:
                click.echo(f"❌ Invalid manifest: {e}")
                sys.exit(1)

        # Apply update
        _ = apply_update(manifest_json, signature)

        if result.get("updated"):
            click.echo("✅ Update applied successfully!")
            click.echo(f"  Version: {result.get('version')}")
            click.echo(f"  Channel: {result.get('channel')}")

            if result.get("requirements_updated"):
                click.echo(f"  Dependencies updated: {result['requirements_updated']}")

            if result.get("post_commands_executed"):
                click.echo(
                    f"  Post-commands executed: {result['post_commands_executed']}"
                )
        else:
            click.echo(f"❌ Update failed: {result.get('reason')}")
            if result.get("error"):
                click.echo(f"  Error: {result['error']}")

    except Exception as e:
        click.echo(f"❌ Update failed: {e}")
        sys.exit(1)


@cli.command()
def setup_dev():
    """🛠️ Setup development environment (interactive)."""
    click.echo("🛠️ ZETA_VN Development Setup")

    project_root = _get_project_root()
    click.echo(f"📁 Project root: {project_root}")

    # Check if .env exists
    env_file = project_root / ".env"
    if not env_file.exists():
        click.echo("\n📝 Creating .env file...")

        env_content = """# ZETA_VN Development Environment
DATABASE_URL=postgresql+asyncpg://postgres:pass@localhost:5432/zeta
OUTBOX_WORKERS=2
OUTBOX_BATCH_SIZE=200

# AI Self-Management (Development)
ZETA_ALLOW_RUNTIME_INSTALL=1
ZETA_ALLOW_SELF_UPDATE=0
ZETA_SELF_SECURITY_AUTO_PATCH=0

# Security (optional - for auto-patching allowlist)
ZETA_PATCH_ALLOW=requests,aiohttp,psutil

# Monitoring
ENABLE_METRICS=true
HEALTH_CHECK_INTERVAL=30

# Development
ZETA_DEV_MODE=1
LOG_LEVEL=DEBUG
"""

        env_file.write_text(env_content)
        click.echo("  ✅ .env file created")
    else:
        click.echo("  ℹ️ .env file already exists")

    # Check PostgreSQL
    click.echo("\n🗄️ Database Setup:")
    if click.confirm("Start PostgreSQL with Docker?"):
        click.echo("Starting PostgreSQL container...")
        import subprocess

        cmd = [
            "docker",
            "run",
            "--rm",
            "-d",
            "--name",
            "zeta-pg",
            "-e",
            "POSTGRES_PASSWORD=pass",
            "-e",
            "POSTGRES_DB=zeta",
            "-p",
            "5432:5432",
            "pgvector/pgvector:pg16",
        ]

        try:
            subprocess.run(cmd, check=True)
            click.echo("  ✅ PostgreSQL started")

            # Wait a bit for startup
            click.echo("  ⏳ Waiting for database startup...")
            # TODO: Replace blocking sleep with async await asyncio.sleep(5)

        except subprocess.CalledProcessError as e:
            click.echo(f"  ❌ Failed to start PostgreSQL: {e}")

    # Run migrations
    click.echo("\n🔄 Running migrations...")
    try:
        import subprocess

        subprocess.run(
            ["uv", "run", "alembic", "upgrade", "head"], cwd=project_root, check=True
        )
        click.echo("  ✅ Migrations completed")
    except subprocess.CalledProcessError as e:
        click.echo(f"  ❌ Migration failed: {e}")

    # Desktop setup
    desktop_path = project_root / "desktop_ai_zeta"
    if desktop_path.exists():
        click.echo("\n🖥️ Desktop App Setup:")
        if click.confirm("Setup desktop app dependencies?"):
            try:
                subprocess.run(["npm", "ci"], cwd=desktop_path, check=True)
                click.echo("  ✅ Desktop dependencies installed")

                # Try to generate API types
                try:
                    subprocess.run(
                        ["npm", "run", "codegen:api"], cwd=desktop_path, check=True
                    )
                    click.echo("  ✅ API types generated")
                except subprocess.CalledProcessError:
                    try:
                        subprocess.run(
                            ["npm", "run", "api:gen"], cwd=desktop_path, check=True
                        )
                        click.echo("  ✅ API types generated")
                    except subprocess.CalledProcessError:
                        click.echo("  ⚠️ Could not generate API types")

            except subprocess.CalledProcessError as e:
                click.echo(f"  ❌ Desktop setup failed: {e}")

    click.echo("\n🎉 Development setup complete!")
    click.echo("\n🚀 Next steps:")
    click.echo(
        "  1. Terminal 1: uv run uvicorn zeta_vn.app.main_production:app --host 0.0.0.0 --port 8000"
    )
    click.echo("  2. Terminal 2: cd desktop_ai_zeta && npm run dev")
    click.echo("  3. Visit: http://localhost:8000/docs")


if __name__ == "__main__":
    cli()
