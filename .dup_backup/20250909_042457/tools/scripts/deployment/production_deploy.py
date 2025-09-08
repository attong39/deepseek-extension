#!/usr/bin/env python3
"""
Production deployment script for Zeta AI.

Handles automated deployment to production environment with
rollback capabilities, health checks, and notification.
"""

import asyncio
import json
import logging
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

import aiohttp
from pydantic import BaseModel, Field


class DeploymentConfig(BaseModel):
    """Deployment configuration settings."""

    # Environment settings
    environment: str = "production"
    app_name: str = "zeta-ai"
    namespace: str = "zeta-ai-prod"

    # Docker settings
    docker_registry: str = "your-registry.com"
    image_tag: str | None = None

    # Kubernetes settings
    kubectl_context: str = "prod-cluster"
    deployment_name: str = "zeta-ai-api"
    service_name: str = "zeta-ai-service"

    # Health check settings
    health_url: str = "https://api.zeta-ai.com/health"
    health_timeout: int = 30
    max_health_retries: int = 10

    # Rollback settings
    enable_rollback: bool = True
    rollback_timeout: int = 300

    # Notification settings
    slack_webhook_url: str | None = None
    discord_webhook_url: str | None = None

    # Database migration
    run_migrations: bool = True
    migration_timeout: int = 600


class DeploymentStatus(BaseModel):
    """Deployment status tracking."""

    deployment_id: str
    environment: str
    status: str  # "pending", "in_progress", "success", "failed", "rolled_back"
    start_time: datetime
    end_time: datetime | None = None
    steps: list[dict] = Field(default_factory=list)
    error_message: str | None = None
    rollback_available: bool = False


class ProductionDeployer:
    """Production deployment manager."""

    def __init__(self, config: DeploymentConfig):
        self.config = config
        self.logger = self._setup_logging()
        self.session: aiohttp.ClientSession | None = None
        self.deployment_status: DeploymentStatus | None = None

    def _setup_logging(self) -> logging.Logger:
        """Setup logging for deployment."""
        logger = logging.getLogger("production_deployer")
        logger.setLevel(logging.INFO)

        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
            handler.setFormatter(formatter)
            logger.addHandler(handler)

            # File handler for deployment logs
            log_dir = Path("./logs/deployment")
            log_dir.mkdir(parents=True, exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_handler = logging.FileHandler(log_dir / f"deployment_{timestamp}.log")
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

        return logger

    async def __aenter__(self):
        """Async context manager entry."""
        self.session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.config.health_timeout))
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.session:
            await self.session.close()

    def _add_step(self, step_name: str, status: str, details: dict | None = None) -> None:
        """Add a deployment step to status tracking."""
        if not self.deployment_status:
            return

        step = {
            "name": step_name,
            "status": status,
            "timestamp": datetime.now().isoformat(),
            "details": details or {},
        }

        self.deployment_status.steps.append(step)
        self.logger.info(f"Step {step_name}: {status}")

        if details:
            for key, value in details.items():
                self.logger.info(f"  {key}: {value}")

    async def pre_deployment_checks(self) -> bool:
        """Run pre-deployment validation checks."""
        self.logger.info("Running pre-deployment checks...")
        self._add_step("pre_deployment_checks", "started")

        try:
            # Check if kubectl is available and configured
            result = await self._run_command(["kubectl", "config", "current-context"], "Check kubectl context")

            if result.returncode != 0:
                self._add_step(
                    "pre_deployment_checks",
                    "failed",
                    {"error": "kubectl not configured or not available"},
                )
                return False

            # Check if Docker is available
            result = await self._run_command(["docker", "--version"], "Check Docker availability")

            if result.returncode != 0:
                self._add_step("pre_deployment_checks", "failed", {"error": "Docker not available"})
                return False

            # Check if namespace exists
            result = await self._run_command(
                ["kubectl", "get", "namespace", self.config.namespace],
                "Check namespace exists",
            )

            if result.returncode != 0:
                self.logger.info(f"Creating namespace {self.config.namespace}")
                await self._run_command(
                    ["kubectl", "create", "namespace", self.config.namespace],
                    "Create namespace",
                )

            self._add_step("pre_deployment_checks", "completed")
            return True

        except Exception as e:
            self._add_step("pre_deployment_checks", "failed", {"error": str(e)})
            return False

    async def build_and_push_image(self) -> bool:
        """Build and push Docker image."""
        self.logger.info("Building and pushing Docker image...")
        self._add_step("build_image", "started")

        try:
            # Generate image tag if not provided
            if not self.config.image_tag:
                self.config.image_tag = f"v{datetime.now().strftime('%Y%m%d-%H%M%S')}"

            image_name = f"{self.config.docker_registry}/{self.config.app_name}:{self.config.image_tag}"

            # Build Docker image
            build_result = await self._run_command(["docker", "build", "-t", image_name, "."], "Build Docker image")

            if build_result.returncode != 0:
                self._add_step("build_image", "failed", {"error": "Docker build failed"})
                return False

            # Push to registry
            push_result = await self._run_command(["docker", "push", image_name], "Push image to registry")

            if push_result.returncode != 0:
                self._add_step("build_image", "failed", {"error": "Docker push failed"})
                return False

            self._add_step(
                "build_image",
                "completed",
                {"image": image_name, "tag": self.config.image_tag},
            )
            return True

        except Exception as e:
            self._add_step("build_image", "failed", {"error": str(e)})
            return False

    async def run_database_migrations(self) -> bool:
        """Run database migrations if enabled."""
        if not self.config.run_migrations:
            self.logger.info("Database migrations disabled, skipping...")
            return True

        self.logger.info("Running database migrations...")
        self._add_step("database_migrations", "started")

        try:
            # Create migration job
            migration_job = f"""
apiVersion: batch/v1
kind: Job
metadata:
  name: zeta-ai-migration-{int(time.time())}
  namespace: {self.config.namespace}
spec:
  template:
    spec:
      containers:
      - name: migration
        image: {self.config.docker_registry}/{self.config.app_name}:{self.config.image_tag}
        command: ["python", "-m", "alembic", "upgrade", "head"]
        envFrom:
        - secretRef:
            name: zeta-ai-secrets
      restartPolicy: Never
  backoffLimit: 3
"""

            # Apply migration job
            result = await self._run_command_with_input(
                ["kubectl", "apply", "-f", "-"], migration_job, "Apply migration job"
            )

            if result.returncode != 0:
                self._add_step(
                    "database_migrations",
                    "failed",
                    {"error": "Failed to create migration job"},
                )
                return False

            # Wait for migration to complete
            job_name = f"zeta-ai-migration-{int(time.time())}"
            success = await self._wait_for_job_completion(job_name)

            if success:
                self._add_step("database_migrations", "completed")
            else:
                self._add_step(
                    "database_migrations",
                    "failed",
                    {"error": "Migration job failed or timed out"},
                )

            return success

        except Exception as e:
            self._add_step("database_migrations", "failed", {"error": str(e)})
            return False

    async def deploy_application(self) -> bool:
        """Deploy application to Kubernetes."""
        self.logger.info("Deploying application...")
        self._add_step("deploy_application", "started")

        try:
            # Update deployment image
            result = await self._run_command(
                [
                    "kubectl",
                    "set",
                    "image",
                    f"deployment/{self.config.deployment_name}",
                    f"{self.config.app_name}={self.config.docker_registry}/{self.config.app_name}:{self.config.image_tag}",
                    f"--namespace={self.config.namespace}",
                ],
                "Update deployment image",
            )

            if result.returncode != 0:
                self._add_step(
                    "deploy_application",
                    "failed",
                    {"error": "Failed to update deployment image"},
                )
                return False

            # Wait for rollout to complete
            rollout_result = await self._run_command(
                [
                    "kubectl",
                    "rollout",
                    "status",
                    f"deployment/{self.config.deployment_name}",
                    f"--namespace={self.config.namespace}",
                    "--timeout=600s",
                ],
                "Wait for rollout completion",
            )

            if rollout_result.returncode != 0:
                self._add_step(
                    "deploy_application",
                    "failed",
                    {"error": "Deployment rollout failed or timed out"},
                )
                return False

            self._add_step(
                "deploy_application",
                "completed",
                {
                    "deployment": self.config.deployment_name,
                    "image_tag": self.config.image_tag,
                },
            )
            return True

        except Exception as e:
            self._add_step("deploy_application", "failed", {"error": str(e)})
            return False

    async def verify_deployment(self) -> bool:
        """Verify deployment health and functionality."""
        self.logger.info("Verifying deployment...")
        self._add_step("verify_deployment", "started")

        try:
            # Check pod status
            result = await self._run_command(
                [
                    "kubectl",
                    "get",
                    "pods",
                    f"--namespace={self.config.namespace}",
                    f"--selector=app={self.config.app_name}",
                    "--output=json",
                ],
                "Check pod status",
            )

            if result.returncode != 0:
                self._add_step("verify_deployment", "failed", {"error": "Failed to get pod status"})
                return False

            # Parse pod status
            pods_data = json.loads(result.stdout)
            running_pods = 0
            total_pods = len(pods_data.get("items", []))

            for pod in pods_data.get("items", []):
                if pod.get("status", {}).get("phase") == "Running":
                    running_pods += 1

            if running_pods == 0:
                self._add_step("verify_deployment", "failed", {"error": "No pods are running"})
                return False

            # Health check
            health_success = await self._verify_health_endpoint()

            if health_success:
                self._add_step(
                    "verify_deployment",
                    "completed",
                    {
                        "running_pods": running_pods,
                        "total_pods": total_pods,
                        "health_check": "passed",
                    },
                )
            else:
                self._add_step("verify_deployment", "failed", {"error": "Health check failed"})

            return health_success

        except Exception as e:
            self._add_step("verify_deployment", "failed", {"error": str(e)})
            return False

    async def _verify_health_endpoint(self) -> bool:
        """Verify application health endpoint."""
        for attempt in range(self.config.max_health_retries):
            try:
                self.logger.info(f"Health check attempt {attempt + 1}/{self.config.max_health_retries}")

                async with self.session.get(self.config.health_url) as response:
                    if response.status == 200:
                        await response.json()
                        self.logger.info("Health check passed")
                        return True
                    else:
                        self.logger.warning(f"Health check failed: {response.status}")

            except Exception as e:
                self.logger.warning(f"Health check error: {e!s}")

            if attempt < self.config.max_health_retries - 1:
                await asyncio.sleep(10)  # Wait 10 seconds between attempts

        return False

    async def rollback_deployment(self) -> bool:
        """Rollback to previous deployment."""
        if not self.config.enable_rollback:
            self.logger.warning("Rollback is disabled")
            return False

        self.logger.info("Rolling back deployment...")
        self._add_step("rollback_deployment", "started")

        try:
            # Rollback deployment
            result = await self._run_command(
                [
                    "kubectl",
                    "rollout",
                    "undo",
                    f"deployment/{self.config.deployment_name}",
                    f"--namespace={self.config.namespace}",
                ],
                "Rollback deployment",
            )

            if result.returncode != 0:
                self._add_step(
                    "rollback_deployment",
                    "failed",
                    {"error": "Failed to initiate rollback"},
                )
                return False

            # Wait for rollback to complete
            rollback_result = await self._run_command(
                [
                    "kubectl",
                    "rollout",
                    "status",
                    f"deployment/{self.config.deployment_name}",
                    f"--namespace={self.config.namespace}",
                    f"--timeout={self.config.rollback_timeout}s",
                ],
                "Wait for rollback completion",
            )

            if rollback_result.returncode != 0:
                self._add_step(
                    "rollback_deployment",
                    "failed",
                    {"error": "Rollback failed or timed out"},
                )
                return False

            # Verify rollback
            rollback_health = await self._verify_health_endpoint()

            if rollback_health:
                self._add_step("rollback_deployment", "completed")
                if self.deployment_status:
                    self.deployment_status.status = "rolled_back"
            else:
                self._add_step(
                    "rollback_deployment",
                    "failed",
                    {"error": "Rollback health check failed"},
                )

            return rollback_health

        except Exception as e:
            self._add_step("rollback_deployment", "failed", {"error": str(e)})
            return False

    async def send_notification(self, message: str, success: bool = True) -> None:
        """Send deployment notification."""
        try:
            color = "good" if success else "danger"

            notification_data = {"text": message, "color": color, "fields": []}

            if self.deployment_status:
                notification_data["fields"].extend(
                    [
                        {
                            "title": "Environment",
                            "value": self.deployment_status.environment,
                            "short": True,
                        },
                        {
                            "title": "Status",
                            "value": self.deployment_status.status,
                            "short": True,
                        },
                        {
                            "title": "Duration",
                            "value": self._get_deployment_duration(),
                            "short": True,
                        },
                    ]
                )

            # Send to Slack
            if self.config.slack_webhook_url:
                await self._send_webhook_notification(
                    self.config.slack_webhook_url, {"attachments": [notification_data]}
                )

            # Send to Discord
            if self.config.discord_webhook_url:
                discord_data = {
                    "content": message,
                    "embeds": [
                        {
                            "color": 65280 if success else 16711680,  # Green or red
                            "fields": notification_data["fields"],
                        }
                    ],
                }
                await self._send_webhook_notification(self.config.discord_webhook_url, discord_data)

        except Exception as e:
            self.logger.error(f"Failed to send notification: {e!s}")

    async def _send_webhook_notification(self, webhook_url: str, data: dict) -> None:
        """Send webhook notification."""
        try:
            async with self.session.post(webhook_url, json=data) as response:
                if response.status < 300:
                    self.logger.info("Notification sent successfully")
                else:
                    self.logger.error(f"Notification failed: {response.status}")
        except Exception as e:
            self.logger.error(f"Webhook notification error: {e!s}")

    def _get_deployment_duration(self) -> str:
        """Get deployment duration string."""
        if not self.deployment_status or not self.deployment_status.start_time:
            return "Unknown"

        end_time = self.deployment_status.end_time or datetime.now()
        duration = end_time - self.deployment_status.start_time

        minutes = int(duration.total_seconds() // 60)
        seconds = int(duration.total_seconds() % 60)

        return f"{minutes}m {seconds}s"

    async def _run_command(self, cmd: list[str], description: str) -> subprocess.CompletedProcess:
        """Run shell command asynchronously."""
        self.logger.info(f"{description}: {' '.join(cmd)}")

        process = await asyncio.create_subprocess_# SECURITY: # SECURITY: # SECURITY: # SECURITY: # SECURITY: # SECURITY: # SECURITY: exec() removed) removed) removed) removed) removed) removed) removed
            *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await process.communicate()

        result = subprocess.CompletedProcess(cmd, process.returncode, stdout.decode(), stderr.decode())

        if result.returncode != 0:
            self.logger.error(f"Command failed: {result.stderr}")

        return result

    async def _run_command_with_input(
        self, cmd: list[str], input_data: str, description: str
    ) -> subprocess.CompletedProcess:
        """Run shell command with input data."""
        self.logger.info(f"{description}: {' '.join(cmd)}")

        process = await asyncio.create_subprocess_# SECURITY: # SECURITY: # SECURITY: # SECURITY: # SECURITY: # SECURITY: # SECURITY: exec() removed) removed) removed) removed) removed) removed) removed
            *cmd,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        stdout, stderr = await process.communicate(input_data.encode())

        result = subprocess.CompletedProcess(cmd, process.returncode, stdout.decode(), stderr.decode())

        if result.returncode != 0:
            self.logger.error(f"Command failed: {result.stderr}")

        return result

    async def _wait_for_job_completion(self, job_name: str) -> bool:
        """Wait for Kubernetes job to complete."""
        timeout = self.config.migration_timeout
        start_time = time.time()

        while time.time() - start_time < timeout:
            result = await self._run_command(
                [
                    "kubectl",
                    "get",
                    "job",
                    job_name,
                    f"--namespace={self.config.namespace}",
                    "--output=json",
                ],
                "Check job status",
            )

            if result.returncode == 0:
                job_data = json.loads(result.stdout)
                status = job_data.get("status", {})

                if status.get("succeeded", 0) > 0:
                    return True
                elif status.get("failed", 0) > 0:
                    return False

            await asyncio.sleep(10)  # Check every 10 seconds

        return False  # Timeout

    async def deploy(self) -> bool:
        """Execute full deployment process."""
        deployment_id = f"deploy_{int(time.time())}"

        self.deployment_status = DeploymentStatus(
            deployment_id=deployment_id,
            environment=self.config.environment,
            status="in_progress",
            start_time=datetime.now(),
        )

        self.logger.info(f"Starting deployment {deployment_id}")

        try:
            await self.send_notification(f"🚀 Starting deployment to {self.config.environment}", success=True)

            # Run deployment steps
            steps = [
                ("Pre-deployment checks", self.pre_deployment_checks),
                ("Build and push image", self.build_and_push_image),
                ("Database migrations", self.run_database_migrations),
                ("Deploy application", self.deploy_application),
                ("Verify deployment", self.verify_deployment),
            ]

            for step_name, step_func in steps:
                self.logger.info(f"Executing: {step_name}")
                success = await step_func()

                if not success:
                    self.deployment_status.status = "failed"
                    self.deployment_status.end_time = datetime.now()

                    await self.send_notification(f"❌ Deployment failed at step: {step_name}", success=False)

                    # Attempt rollback
                    if self.config.enable_rollback:
                        self.logger.info("Attempting rollback...")
                        rollback_success = await self.rollback_deployment()

                        if rollback_success:
                            await self.send_notification(
                                "🔄 Deployment failed but rollback successful",
                                success=False,
                            )
                        else:
                            await self.send_notification(
                                "💥 Deployment failed and rollback also failed!",
                                success=False,
                            )

                    return False

            # Success
            self.deployment_status.status = "success"
            self.deployment_status.end_time = datetime.now()

            await self.send_notification(
                f"✅ Deployment to {self.config.environment} completed successfully!",
                success=True,
            )

            return True

        except Exception as e:
            self.deployment_status.status = "failed"
            self.deployment_status.error_message = str(e)
            self.deployment_status.end_time = datetime.now()

            self.logger.error(f"Deployment failed with exception: {e!s}")

            await self.send_notification(f"💥 Deployment failed with error: {e!s}", success=False)

            return False


async def main():
    """Main deployment function."""
    try:
        # Parse command line arguments
        import argparse

        parser = argparse.ArgumentParser(description="Zeta AI Production Deployment")
        parser.add_argument("--config", help="Configuration file path")
        parser.add_argument("--image-tag", help="Docker image tag to deploy")
        parser.add_argument("--no-migrations", action="store_true", help="Skip database migrations")
        parser.add_argument("--no-rollback", action="store_true", help="Disable automatic rollback")

        args = parser.parse_args()

        # Load configuration
        config = DeploymentConfig()

        if args.config and Path(args.config).exists():
            with open(args.config) as f:
                config_data = json.load(f)
                config = DeploymentConfig(**config_data)

        # Override with command line arguments
        if args.image_tag:
            config.image_tag = args.image_tag
        if args.no_migrations:
            config.run_migrations = False
        if args.no_rollback:
            config.enable_rollback = False

        # Execute deployment
        async with ProductionDeployer(config) as deployer:
            success = await deployer.deploy()
            return 0 if success else 1

    except Exception as e:
        logging.error(f"Deployment script error: {e!s}")
        return 1


if __name__ == "__main__":
    import sys

    sys.exit(asyncio.run(main()))
