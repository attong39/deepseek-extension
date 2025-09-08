import Exception
import ImportError
import attempt
import bool
import dict
import e
import environment
import f
import image
import k8s_file
import key
import list
import manifest_file
import open
import placeholder
import range
import revision
import self
import step_func
import step_name
import str
import value
# Author: Duy BG VN
# ZETA AI - Deployment Script

"""Production deployment automation script.

Provides comprehensive deployment automation including Docker builds,
health checks, rollback capabilities, and environment-specific configurations.
"""

import logging
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class DeploymentManager:
    """Production deployment manager."""

    def __init__(self, environment: str = "production"):
        """Initialize deployment manager.

        Args:
            environment: Target deployment environment
        """
        self.environment = environment
        self.project_root = Path(__file__).parent.parent
        self.deployment_dir = self.project_root / "deployment"
        self.docker_dir = self.deployment_dir / "docker"
        self.k8s_dir = self.deployment_dir / "kubernetes"
        self.backup_dir = self.project_root / "storage" / "backups"

        # Deployment configuration
        self.config = self._load_deployment_config()

    def _load_deployment_config(self) -> dict[str, Any]:
        """Load deployment configuration.

        Returns:
            Deployment configuration dictionary
        """
        config_file = self.deployment_dir / f"{self.environment}.yml"

        if config_file.exists():
            with open(config_file) as f:
                return yaml.safe_load(f)

        # Default configuration
        return {
            "docker": {
                "registry": "localhost:5000",
                "image_tag": "latest",
                "build_args": {},
            },
            "kubernetes": {
                "namespace": f"zeta-{self.environment}",
                "replicas": 3,
                "resources": {
                    "requests": {"cpu": "100m", "memory": "128Mi"},
                    "limits": {"cpu": "500m", "memory": "512Mi"},
                },
            },
            "database": {"backup_before_deploy": True, "run_migrations": True},
            "health_check": {"timeout": 300, "interval": 10, "retries": 30},
        }

    def create_backup(self) -> str | None:
        """Create pre-deployment backup.

        Returns:
            Backup file path or None if failed
        """
        logger.info("Creating pre-deployment backup...")

        try:
            backup_name = f"pre_deploy_{self.environment}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            backup_file = self.backup_dir / f"{backup_name}.sql"

            # Ensure backup directory exists
            self.backup_dir.mkdir(parents=True, exist_ok=True)

            # PostgreSQL backup command (adjust based on your database)
            cmd = [
                "pg_dump",
                "-h",
                os.getenv("DB_HOST", "localhost"),
                "-p",
                os.getenv("DB_PORT", "5432"),
                "-U",
                os.getenv("DB_USERNAME", "postgres"),
                "-d",
                os.getenv("DB_NAME", "zeta_db"),
                "-f",
                str(backup_file),
                "--verbose",
                "--no-password",
            ]

            env = os.environ.copy()
            env["PGPASSWORD"] = os.getenv("DB_PASSWORD", "")

            result = subprocess.run(cmd, env=env, capture_output=True, text=True, check=False)

            if result.returncode == 0:
                logger.info(f"✓ Backup created: {backup_file}")
                return str(backup_file)
            else:
                logger.error(f"✗ Backup failed: {result.stderr}")
                return None

        except Exception as e:
            logger.error(f"✗ Backup creation failed: {e}")
            return None

    def build_docker_images(self) -> bool:
        """Build Docker images for deployment.

        Returns:
            True if successful
        """
        logger.info("Building Docker images...")

        try:
            docker_config = self.config.get("docker", {})
            registry = docker_config.get("registry", "localhost:5000")
            tag = docker_config.get("image_tag", "latest")
            build_args = docker_config.get("build_args", {})

            # Build main application image
            app_image = f"{registry}/zeta-ai:{tag}"
            cmd = [
                "docker",
                "build",
                "-t",
                app_image,
                "-f",
                str(self.docker_dir / "Dockerfile"),
                str(self.project_root),
            ]

            # Add build arguments
            for key, value in build_args.items():
                cmd.extend(["--build-arg", f"{key}={value}"])

            subprocess.run(cmd, check=True)
            logger.info(f"✓ Application image built: {app_image}")

            # Build worker image
            worker_image = f"{registry}/zeta-ai-worker:{tag}"
            cmd = [
                "docker",
                "build",
                "-t",
                worker_image,
                "-f",
                str(self.docker_dir / "Dockerfile.worker"),
                str(self.project_root),
            ]

            subprocess.run(cmd, check=True)
            logger.info(f"✓ Worker image built: {worker_image}")

            return True

        except subprocess.CalledProcessError as e:
            logger.error(f"✗ Docker build failed: {e}")
            return False
        except Exception as e:
            logger.error(f"✗ Unexpected error during build: {e}")
            return False

    def push_docker_images(self) -> bool:
        """Push Docker images to registry.

        Returns:
            True if successful
        """
        logger.info("Pushing Docker images to registry...")

        try:
            docker_config = self.config.get("docker", {})
            registry = docker_config.get("registry", "localhost:5000")
            tag = docker_config.get("image_tag", "latest")

            images = [f"{registry}/zeta-ai:{tag}", f"{registry}/zeta-ai-worker:{tag}"]

            for image in images:
                subprocess.run(["docker", "push", image], check=True)
                logger.info(f"✓ Pushed: {image}")

            return True

        except subprocess.CalledProcessError as e:
            logger.error(f"✗ Docker push failed: {e}")
            return False

    def run_database_migrations(self) -> bool:
        """Run database migrations.

        Returns:
            True if successful
        """
        logger.info("Running database migrations...")

        try:
            # Use virtual environment if available
            venv_python = self._get_python_executable()

            # Run Alembic migrations
            cmd = [venv_python, "-m", "alembic", "upgrade", "head"]

            subprocess.run(
                cmd,
                cwd=str(self.project_root),
                check=True,
                capture_output=True,
                text=True,
            )

            logger.info("✓ Database migrations completed")
            return True

        except subprocess.CalledProcessError as e:
            logger.error(f"✗ Migration failed: {e.stderr}")
            return False
        except Exception as e:
            logger.error(f"✗ Migration error: {e}")
            return False

    def deploy_to_kubernetes(self) -> bool:
        """Deploy to Kubernetes cluster.

        Returns:
            True if successful
        """
        logger.info("Deploying to Kubernetes...")

        try:
            k8s_config = self.config.get("kubernetes", {})
            namespace = k8s_config.get("namespace", f"zeta-{self.environment}")

            # Create namespace if it doesn't exist
            subprocess.run(
                [
                    "kubectl",
                    "create",
                    "namespace",
                    namespace,
                    "--dry-run=client",
                    "-o",
                    "yaml",
                ],
                capture_output=True,
                check=False,
            )
            subprocess.run(["kubectl", "apply", "-f", "-"], capture_output=True, check=False)

            # Apply Kubernetes manifests
            k8s_files = list(self.k8s_dir.glob("*.yaml"))

            for k8s_file in k8s_files:
                # Update image tags and other environment-specific values
                self._update_k8s_manifest(k8s_file, namespace)

                cmd = ["kubectl", "apply", "-f", str(k8s_file), "-n", namespace]
                subprocess.run(cmd, check=True)
                logger.info(f"✓ Applied: {k8s_file.name}")

            logger.info("✓ Kubernetes deployment completed")
            return True

        except subprocess.CalledProcessError as e:
            logger.error(f"✗ Kubernetes deployment failed: {e}")
            return False
        except Exception as e:
            logger.error(f"✗ Deployment error: {e}")
            return False

    def _update_k8s_manifest(self, manifest_file: Path, namespace: str) -> None:
        """Update Kubernetes manifest with environment-specific values.

        Args:
            manifest_file: Path to manifest file
            namespace: Target namespace
        """
        with open(manifest_file) as f:
            content = f.read()

        # Replace placeholders
        docker_config = self.config.get("docker", {})
        registry = docker_config.get("registry", "localhost:5000")
        tag = docker_config.get("image_tag", "latest")

        replacements = {
            "{{NAMESPACE}}": namespace,
            "{{IMAGE_REGISTRY}}": registry,
            "{{IMAGE_TAG}}": tag,
            "{{ENVIRONMENT}}": self.environment,
            "{{REPLICAS}}": str(self.config.get("kubernetes", {}).get("replicas", 3)),
        }

        for placeholder, value in replacements.items():
            content = content.replace(placeholder, value)

        with open(manifest_file, "w") as f:
            f.write(content)

    def wait_for_deployment(self) -> bool:
        """Wait for deployment to be ready.

        Returns:
            True if deployment is healthy
        """
        logger.info("Waiting for deployment to be ready...")

        health_config = self.config.get("health_check", {})
        health_config.get("timeout", 300)
        interval = health_config.get("interval", 10)
        retries = health_config.get("retries", 30)

        k8s_config = self.config.get("kubernetes", {})
        namespace = k8s_config.get("namespace", f"zeta-{self.environment}")

        for attempt in range(retries):
            try:
                # Check deployment status
                result = subprocess.run(
                    [
                        "kubectl",
                        "rollout",
                        "status",
                        "deployment/zeta-ai",
                        "-n",
                        namespace,
                        "--timeout=60s",
                    ],
                    capture_output=True,
                    text=True,
                    check=False,
                )

                if result.returncode == 0:
                    logger.info("✓ Deployment is ready")
                    return True

                logger.info(f"Waiting for deployment... ({attempt + 1}/{retries})")
                # TODO: Replace blocking sleep with async await asyncio.sleep(interval)

            except Exception as e:
                logger.warning(f"Health check failed: {e}")
                # TODO: Replace blocking sleep with async await asyncio.sleep(interval)

        logger.error("✗ Deployment health check timeout")
        return False

    def run_smoke_tests(self) -> bool:
        """Run smoke tests against deployed application.

        Returns:
            True if tests pass
        """
        logger.info("Running smoke tests...")

        try:
            # Get service URL
            k8s_config = self.config.get("kubernetes", {})
            namespace = k8s_config.get("namespace", f"zeta-{self.environment}")

            # Port forward for testing (in real deployment, use ingress)
            port_forward_process = subprocess.Popen(
                [
                    "kubectl",
                    "port-forward",
                    "service/zeta-ai",
                    "8080:8000",
                    "-n",
                    namespace,
                ]
            )

            # TODO: Replace blocking sleep with async await asyncio.sleep(5)  # Wait for port forward to establish

            try:
                # Test health endpoint
                import requests

                response = requests.get("http://localhost:8080/health", timeout=30)

                if response.status_code == 200:
                    logger.info("✓ Smoke tests passed")
                    return True
                else:
                    logger.error(f"✗ Health check failed: {response.status_code}")
                    return False

            finally:
                port_forward_process.terminate()
                port_forward_process.wait()

        except ImportError:
            logger.warning("⚠ requests library not available, skipping smoke tests")
            return True
        except Exception as e:
            logger.error(f"✗ Smoke tests failed: {e}")
            return False

    def rollback_deployment(self, revision: str | None = None) -> bool:
        """Rollback deployment to previous version.

        Args:
            revision: Specific revision to rollback to

        Returns:
            True if successful
        """
        logger.info("Rolling back deployment...")

        try:
            k8s_config = self.config.get("kubernetes", {})
            namespace = k8s_config.get("namespace", f"zeta-{self.environment}")

            cmd = ["kubectl", "rollout", "undo", "deployment/zeta-ai", "-n", namespace]
            if revision:
                cmd.extend([f"--to-revision={revision}"])

            subprocess.run(cmd, check=True)
            logger.info("✓ Rollback initiated")

            # Wait for rollback to complete
            subprocess.run(
                ["kubectl", "rollout", "status", "deployment/zeta-ai", "-n", namespace],
                check=True,
            )

            logger.info("✓ Rollback completed")
            return True

        except subprocess.CalledProcessError as e:
            logger.error(f"✗ Rollback failed: {e}")
            return False

    def _get_python_executable(self) -> str:
        """Get Python executable path.

        Returns:
            Path to Python executable
        """
        venv_path = self.project_root / ".venv"

        if venv_path.exists():
            if os.name == "nt":  # Windows
                return str(venv_path / "Scripts" / "python.exe")
            else:  # Unix-like
                return str(venv_path / "bin" / "python")

        return sys.executable

    def deploy(self) -> bool:
        """Run complete deployment process.

        Returns:
            True if deployment successful
        """
        logger.info(f"🚀 Starting deployment to {self.environment}...")

        steps = [
            ("Backup creation", lambda: self.create_backup() is not None),
            ("Docker build", self.build_docker_images),
            ("Docker push", self.push_docker_images),
            ("Database migrations", self.run_database_migrations),
            ("Kubernetes deployment", self.deploy_to_kubernetes),
            ("Health check", self.wait_for_deployment),
            ("Smoke tests", self.run_smoke_tests),
        ]

        failed_step = None

        for step_name, step_func in steps:
            logger.info(f"\n--- {step_name} ---")
            if not step_func():
                failed_step = step_name
                break

        if failed_step:
            logger.error(f"\n❌ Deployment failed at: {failed_step}")
            logger.info("Initiating rollback...")
            if self.rollback_deployment():
                logger.info("✓ Rollback completed")
            else:
                logger.error("✗ Rollback failed")
            return False
        else:
            logger.info("\n✅ Deployment completed successfully!")
            return True


def main():
    """Main deployment function."""
    import argparse

    parser = argparse.ArgumentParser(description="ZETA AI Deployment Manager")
    parser.add_argument(
        "--environment",
        "-e",
        default="production",
        help="Target environment (default: production)",
    )
    parser.add_argument("--rollback", "-r", action="store_true", help="Rollback to previous deployment")
    parser.add_argument("--revision", help="Specific revision to rollback to")

    args = parser.parse_args()

    manager = DeploymentManager(args.environment)

    if args.rollback:
        success = manager.rollback_deployment(args.revision)
    else:
        success = manager.deploy()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
