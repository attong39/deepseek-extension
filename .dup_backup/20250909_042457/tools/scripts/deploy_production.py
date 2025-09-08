#!/usr/bin/env python3
"""
Production deployment script for ZETA AI Server.

This script automates the deployment process including:
- Environment validation
- Database migrations
- Service deployment
- Health checks
- Rollback capability
"""

import argparse
import logging
import subprocess
import sys
import time
from pathlib import Path

import requests
import yaml
import Exception
import FileNotFoundError
import all
import bool
import config_path
import dict
import e
import endpoint
import f
import int
import open
import secret_name
import self
import skip_validations
import str
import tag
import timeout

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class DeploymentManager:
    """Manages production deployment process."""

    def __init__(self, config_path: str = "deployment/production.yaml"):
        """Initialize deployment manager.

        Args:
            config_path: Path to deployment configuration file
        """
        self.config_path = Path(config_path)
        self.config = self._load_config()
        self.rollback_info: dict[str, str] = {}

    def _load_config(self) -> dict:
        """Load deployment configuration."""
        try:
            with open(self.config_path) as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            logger.error(f"Configuration file not found: {self.config_path}")
            raise
        except yaml.YAMLError as e:
            logger.error(f"Invalid YAML configuration: {e}")
            raise

    def validate_environment(self) -> bool:
        """Validate deployment environment.

        Returns:
            True if environment is valid for deployment
        """
        logger.info("Validating deployment environment...")

        checks = [
            self._check_kubernetes_cluster(),
            self._check_docker_registry(),
            self._check_database_connectivity(),
            self._check_required_secrets(),
        ]

        if all(checks):
            logger.info("Environment validation passed")
            return True
        else:
            logger.error("Environment validation failed")
            return False

    def _check_kubernetes_cluster(self) -> bool:
        """Check Kubernetes cluster connectivity."""
        try:
            subprocess.run(["kubectl", "cluster-info"], check=True, capture_output=True, text=True)
            logger.info("Kubernetes cluster is accessible")
            return True
        except subprocess.CalledProcessError:
            logger.error("Kubernetes cluster is not accessible")
            return False
        except FileNotFoundError:
            logger.error("kubectl command not found")
            return False

    def _check_docker_registry(self) -> bool:
        """Check Docker registry connectivity."""
        registry_url = self.config.get("docker", {}).get("registry", "")

        if not registry_url:
            logger.error("Docker registry URL not configured")
            return False

        try:
            # Simple ping to registry
            response = requests.get(f"https://{registry_url}/v2/", timeout=10)
            if response.status_code in [200, 401]:  # 401 is expected for auth
                logger.info(f"Docker registry {registry_url} is accessible")
                return True
            else:
                logger.error(f"Docker registry returned status {response.status_code}")
                return False
        except requests.RequestException as e:
            logger.error(f"Failed to connect to Docker registry: {e}")
            return False

    def _check_database_connectivity(self) -> bool:
        """Check database connectivity."""
        try:
            # Use pg_isready to check PostgreSQL
            db_host = self.config.get("database", {}).get("host", "localhost")
            db_port = self.config.get("database", {}).get("port", 5432)

            subprocess.run(
                ["pg_isready", "-h", db_host, "-p", str(db_port)],
                check=True,
                capture_output=True,
            )
            logger.info("Database is accessible")
            return True
        except subprocess.CalledProcessError:
            logger.error("Database is not accessible")
            return False
        except FileNotFoundError:
            logger.error("pg_isready command not found")
            return False

    def _check_required_secrets(self) -> bool:
        """Check that required Kubernetes secrets exist."""
        required_secrets = self.config.get("secrets", [])

        for secret_name in required_secrets:
            try:
                subprocess.run(
                    ["kubectl", "get", "secret", secret_name],
                    check=True,
                    capture_output=True,
                )
                logger.info(f"Secret {secret_name} exists")
            except subprocess.CalledProcessError:
                logger.error(f"Required secret {secret_name} not found")
                return False

        return True

    def build_and_push_image(self, tag: str) -> bool:
        """Build and push Docker image.

        Args:
            tag: Docker image tag

        Returns:
            True if build and push successful
        """
        logger.info(f"Building Docker image with tag: {tag}")

        try:
            # Build image
            build_cmd = ["docker", "build", "-t", tag, "-f", "Dockerfile.prod", "."]

            subprocess.run(build_cmd, check=True)
            logger.info("Docker image built successfully")

            # Push image
            push_cmd = ["docker", "push", tag]
            subprocess.run(push_cmd, check=True)
            logger.info("Docker image pushed successfully")

            return True

        except subprocess.CalledProcessError as e:
            logger.error(f"Docker build/push failed: {e}")
            return False

    def run_database_migrations(self) -> bool:
        """Run database migrations.

        Returns:
            True if migrations successful
        """
        logger.info("Running database migrations...")

        try:
            # Run Alembic migrations
            migration_cmd = [
                "kubectl",
                "run",
                "migration-job",
                "--image",
                self.config["docker"]["image"],
                "--restart=Never",
                "--rm",
                "--command",
                "--",
                "alembic",
                "upgrade",
                "head",
            ]

            subprocess.run(migration_cmd, check=True)
            logger.info("Database migrations completed successfully")
            return True

        except subprocess.CalledProcessError as e:
            logger.error(f"Database migration failed: {e}")
            return False

    def deploy_services(self, tag: str) -> bool:
        """Deploy services to Kubernetes.

        Args:
            tag: Docker image tag to deploy

        Returns:
            True if deployment successful
        """
        logger.info(f"Deploying services with image tag: {tag}")

        try:
            # Store current deployment for rollback
            self._store_rollback_info()

            # Update deployment with new image
            update_cmd = [
                "kubectl",
                "set",
                "image",
                "deployment/zeta-ai-server",
                f"app={tag}",
            ]

            subprocess.run(update_cmd, check=True)

            # Wait for rollout to complete
            rollout_cmd = [
                "kubectl",
                "rollout",
                "status",
                "deployment/zeta-ai-server",
                "--timeout=300s",
            ]

            subprocess.run(rollout_cmd, check=True)
            logger.info("Service deployment completed successfully")
            return True

        except subprocess.CalledProcessError as e:
            logger.error(f"Service deployment failed: {e}")
            return False

    def _store_rollback_info(self) -> None:
        """Store current deployment info for potential rollback."""
        try:
            result = subprocess.run(
                ["kubectl", "get", "deployment", "zeta-ai-server", "-o", "yaml"],
                check=True,
                capture_output=True,
                text=True,
            )

            # Extract current image
            import yaml

            deployment = yaml.safe_load(result.stdout)
            current_image = deployment["spec"]["template"]["spec"]["containers"][0]["image"]

            self.rollback_info["image"] = current_image
            logger.info(f"Stored rollback info: {current_image}")

        except Exception as e:
            logger.warning(f"Failed to store rollback info: {e}")

    def run_health_checks(self, timeout: int = 300) -> bool:
        """Run health checks after deployment.

        Args:
            timeout: Maximum time to wait for health checks

        Returns:
            True if all health checks pass
        """
        logger.info("Running post-deployment health checks...")

        health_endpoints = self.config.get("health_checks", [])
        start_time = time.time()

        while time.time() - start_time < timeout:
            all_healthy = True

            for endpoint in health_endpoints:
                try:
                    response = requests.get(endpoint, timeout=10)
                    if response.status_code == 200:
                        logger.info(f"Health check passed: {endpoint}")
                    else:
                        logger.warning(f"Health check failed: {endpoint} (status: {response.status_code})")
                        all_healthy = False
                except requests.RequestException as e:
                    logger.warning(f"Health check failed: {endpoint} (error: {e})")
                    all_healthy = False

            if all_healthy:
                logger.info("All health checks passed")
                return True

            logger.info("Waiting for services to become healthy...")
            # TODO: Replace blocking sleep with async await asyncio.sleep(10)

        logger.error("Health checks failed after timeout")
        return False

    def rollback_deployment(self) -> bool:
        """Rollback to previous deployment.

        Returns:
            True if rollback successful
        """
        if not self.rollback_info.get("image"):
            logger.error("No rollback information available")
            return False

        logger.info(f"Rolling back to previous deployment: {self.rollback_info['image']}")

        try:
            rollback_cmd = [
                "kubectl",
                "set",
                "image",
                "deployment/zeta-ai-server",
                f"app={self.rollback_info['image']}",
            ]

            subprocess.run(rollback_cmd, check=True)

            # Wait for rollback to complete
            rollout_cmd = [
                "kubectl",
                "rollout",
                "status",
                "deployment/zeta-ai-server",
                "--timeout=300s",
            ]

            subprocess.run(rollout_cmd, check=True)
            logger.info("Rollback completed successfully")
            return True

        except subprocess.CalledProcessError as e:
            logger.error(f"Rollback failed: {e}")
            return False

    def full_deployment(self, tag: str, skip_validations: bool = False) -> bool:
        """Execute full deployment process.

        Args:
            tag: Docker image tag to deploy
            skip_validations: Skip environment validations

        Returns:
            True if deployment successful
        """
        logger.info(f"Starting full deployment process for tag: {tag}")

        try:
            # Validate environment
            if not skip_validations and not self.validate_environment():
                return False

            # Build and push image
            if not self.build_and_push_image(tag):
                return False

            # Run database migrations
            if not self.run_database_migrations():
                logger.error("Migration failed, aborting deployment")
                return False

            # Deploy services
            if not self.deploy_services(tag):
                logger.error("Service deployment failed, attempting rollback")
                self.rollback_deployment()
                return False

            # Run health checks
            if not self.run_health_checks():
                logger.error("Health checks failed, attempting rollback")
                self.rollback_deployment()
                return False

            logger.info("Deployment completed successfully!")
            return True

        except Exception as e:
            logger.error(f"Deployment failed with unexpected error: {e}")
            logger.info("Attempting rollback...")
            self.rollback_deployment()
            return False


def main() -> None:
    """Main function for command line interface."""
    parser = argparse.ArgumentParser(description="Production deployment utility for ZETA AI Server")

    parser.add_argument("tag", help="Docker image tag to deploy")
    parser.add_argument(
        "--config",
        default="deployment/production.yaml",
        help="Deployment configuration file",
    )
    parser.add_argument("--skip-validations", action="store_true", help="Skip environment validations")
    parser.add_argument("--rollback", action="store_true", help="Rollback to previous deployment")

    args = parser.parse_args()

    try:
        deployment_manager = DeploymentManager(args.config)

        if args.rollback:
            success = deployment_manager.rollback_deployment()
        else:
            success = deployment_manager.full_deployment(args.tag, args.skip_validations)

        if success:
            logger.info("Operation completed successfully")
            sys.exit(0)
        else:
            logger.error("Operation failed")
            sys.exit(1)

    except Exception as e:
        logger.error(f"Deployment script failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
