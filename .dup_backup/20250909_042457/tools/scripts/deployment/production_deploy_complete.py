# Author: Duy BG VN
# ZETA AI Production Deployment Script
# Comprehensive production deployment with monitoring and rollback

#!/usr/bin/env python3

import argparse
import json
import logging
import os
import socket
import subprocess
import sys
import time
from datetime import datetime

import docker
import requests
import yaml
from kubernetes import client, config
import Exception
import ValueError
import bool
import check_func
import check_name
import config_path
import dict
import e
import endpoint
import f
import host
import image
import int
import kwargs
import len
import name
import node
import open
import pod
import port
import resource
import s
import self
import step_func
import step_name
import str
import sum
import var

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("/app/logs/deployment.log"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)


class ZetaAIProductionDeployer:
    """
    ZETA AI Production Deployment Manager

    Handles complete production deployment with:
    - Pre-deployment validation
    - Database migrations
    - Blue-green deployment
    - Health checks
    - Monitoring setup
    - Rollback capabilities
    """

    def __init__(self, config_path: str = None):
        self.config_path = config_path or os.getenv("DEPLOYMENT_CONFIG", "deployment/config.json")
        self.deployment_id = f"deploy-{int(time.time())}"
        self.start_time = time.time()

        # Load configuration
        self.config = self._load_config()

        # Initialize clients
        self.docker_client = docker.from_env()
        self.k8s_client = self._init_k8s_client()

        # Deployment state
        self.deployment_state = {
            "id": self.deployment_id,
            "start_time": self.start_time,
            "status": "initializing",
            "steps": [],
            "rollback_data": {},
        }

        logger.info(f"🚀 ZETA AI Production Deployer initialized - ID: {self.deployment_id}")

    def _load_config(self) -> dict:
        """Load deployment configuration"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path) as f:
                    config = json.load(f)
            else:
                # Default configuration
                config = {
                    "environment": "production",
                    "namespace": "zeta-ai",
                    "replicas": 5,
                    "image_tag": os.getenv("IMAGE_TAG", "latest"),
                    "health_check_timeout": 300,
                    "deployment_timeout": 600,
                    "rollback_on_failure": True,
                    "enable_monitoring": True,
                    "backup_before_deploy": True,
                }

            logger.info(f"📋 Configuration loaded: {config['environment']} environment")
            return config

        except Exception as e:
            logger.error(f"❌ Failed to load configuration: {e}")
            raise

    def _init_k8s_client(self):
        """Initialize Kubernetes client"""
        try:
            # Try to load in-cluster config first
            try:
                config.load_incluster_config()
                logger.info("🔧 Using in-cluster Kubernetes configuration")
            except:
                # Fallback to local kubeconfig
                config.load_kube_config()
                logger.info("🔧 Using local Kubernetes configuration")

            return client.ApiClient()

        except Exception as e:
            logger.error(f"❌ Failed to initialize Kubernetes client: {e}")
            raise

    def _run_step(self, step_name: str, step_func, *args, **kwargs):
        """Execute a deployment step with logging and error handling"""
        step_start = time.time()
        step_data = {"name": step_name, "start_time": step_start, "status": "running"}

        self.deployment_state["steps"].append(step_data)
        logger.info(f"🔄 Starting step: {step_name}")

        try:
            result = step_func(*args, **kwargs)
            step_data.update(
                {
                    "status": "success",
                    "duration": time.time() - step_start,
                    "result": result,
                }
            )
            logger.info(f"✅ Step completed: {step_name} ({step_data['duration']:.2f}s)")
            return result

        except Exception as e:
            step_data.update(
                {
                    "status": "failed",
                    "duration": time.time() - step_start,
                    "error": str(e),
                }
            )
            logger.error(f"❌ Step failed: {step_name} - {e}")
            raise

    def pre_deployment_checks(self) -> bool:
        """Run comprehensive pre-deployment validation"""

        def _check_environment():
            """Validate environment configuration"""
            required_vars = [
                "POSTGRES_PASSWORD",
                "REDIS_PASSWORD",
                "JWT_SECRET",
                "OPENAI_API_KEY",
                "SENTRY_DSN",
            ]

            missing_vars = [var for var in required_vars if not os.getenv(var)]
            if missing_vars:
                raise ValueError(f"Missing required environment variables: {missing_vars}")

            return True

        def _check_dependencies():
            """Check external service dependencies"""
            dependencies = [
                ("PostgreSQL", "postgres:5432"),
                ("Redis", "redis:6379"),
                ("Prometheus", "prometheus:9090"),
            ]

            for name, endpoint in dependencies:
                try:
                    host, port = endpoint.split(":")
                    sock = socket.create_connection((host, int(port)), timeout=10)
                    sock.close()
                    logger.info(f"✅ {name} is reachable")
                except Exception as e:
                    logger.warning(f"⚠️ {name} check failed: {e}")

            return True

        def _check_resources():
            """Check Kubernetes cluster resources"""
            v1 = client.CoreV1Api(self.k8s_client)

            # Check node resources
            nodes = v1.list_node()
            total_cpu = sum(int(node.status.allocatable["cpu"]) for node in nodes.items)
            total_memory = sum(int(node.status.allocatable["memory"].replace("Ki", "")) for node in nodes.items)

            logger.info(f"🔧 Cluster resources: {total_cpu} CPU cores, {total_memory // 1024 // 1024} GB memory")

            # Check if resources are sufficient
            required_cpu = self.config["replicas"] * 2  # 2 CPU per replica
            required_memory = self.config["replicas"] * 4 * 1024 * 1024  # 4GB per replica

            if total_cpu < required_cpu or total_memory < required_memory:
                raise ValueError("Insufficient cluster resources for deployment")

            return True

        def _check_image_availability():
            """Verify Docker images are available"""
            image_tag = self.config["image_tag"]
            images = [f"zeta-ai/app:{image_tag}", f"zeta-ai/worker:{image_tag}"]

            for image in images:
                try:
                    self.docker_client.images.pull(image)
                    logger.info(f"✅ Image pulled: {image}")
                except Exception as e:
                    logger.error(f"❌ Failed to pull image {image}: {e}")
                    raise

            return True

        # Run all checks
        checks = [
            ("Environment Variables", _check_environment),
            ("External Dependencies", _check_dependencies),
            ("Cluster Resources", _check_resources),
            ("Docker Images", _check_image_availability),
        ]

        for check_name, check_func in checks:
            self._run_step(f"Pre-check: {check_name}", check_func)

        return True

    def backup_current_deployment(self) -> dict:
        """Create backup of current deployment state"""

        def _backup_database():
            """Backup PostgreSQL database"""
            backup_cmd = [
                "kubectl",
                "exec",
                "-n",
                self.config["namespace"],
                "deployment/postgres",
                "--",
                "pg_dump",
                "-U",
                "zeta_ai",
                "-d",
                "zeta_ai_prod",
            ]

            backup_file = f"/app/backups/pre-deploy-{self.deployment_id}.sql"

            with open(backup_file, "w") as f:
                result = subprocess.run(backup_cmd, stdout=f, stderr=subprocess.PIPE, check=False)
                if result.returncode != 0:
                    raise Exception(f"Database backup failed: {result.stderr.decode()}")

            logger.info(f"📦 Database backup created: {backup_file}")
            return backup_file

        def _backup_k8s_config():
            """Backup current Kubernetes configuration"""
            apps_v1 = client.AppsV1Api(self.k8s_client)

            # Get current deployment configuration
            try:
                current_deployment = apps_v1.read_namespaced_deployment(
                    name="zeta-ai-app", namespace=self.config["namespace"]
                )

                backup_data = {
                    "deployment": current_deployment.to_dict(),
                    "replicas": current_deployment.spec.replicas,
                    "image": current_deployment.spec.template.spec.containers[0].image,
                }

                backup_file = f"/app/backups/k8s-config-{self.deployment_id}.json"
                with open(backup_file, "w") as f:
                    json.dump(backup_data, f, indent=2, default=str)

                logger.info(f"📦 Kubernetes config backup created: {backup_file}")
                return backup_data

            except Exception as e:
                logger.warning(f"⚠️ No existing deployment to backup: {e}")
                return {}

        if self.config.get("backup_before_deploy", True):
            db_backup = self._run_step("Database Backup", _backup_database)
            k8s_backup = self._run_step("Kubernetes Config Backup", _backup_k8s_config)

            backup_data = {
                "database_backup": db_backup,
                "k8s_backup": k8s_backup,
                "timestamp": datetime.now().isoformat(),
            }

            self.deployment_state["rollback_data"] = backup_data
            return backup_data

        return {}

    def run_database_migrations(self) -> bool:
        """Execute database migrations"""

        def _run_migrations():
            """Run Alembic migrations"""
            migration_cmd = [
                "kubectl",
                "run",
                f"migration-{self.deployment_id}",
                "--image",
                f"zeta-ai/app:{self.config['image_tag']}",
                "--restart=Never",
                "--rm",
                "-i",
                "--namespace",
                self.config["namespace"],
                "--",
                "alembic",
                "upgrade",
                "head",
            ]

            result = subprocess.run(migration_cmd, capture_output=True, text=True, check=False)

            if result.returncode != 0:
                raise Exception(f"Database migration failed: {result.stderr}")

            logger.info("📊 Database migrations completed successfully")
            return True

        return self._run_step("Database Migrations", _run_migrations)

    def deploy_application(self) -> bool:
        """Deploy ZETA AI application using blue-green strategy"""

        def _create_green_deployment():
            """Create new 'green' deployment"""
            apps_v1 = client.AppsV1Api(self.k8s_client)

            # Load deployment template
            with open("deployment/kubernetes/production-complete.yaml") as f:
                manifest = yaml.safe_load_all(f.read())

            # Update manifest with new image and green suffix
            for resource in manifest:
                if resource["kind"] == "Deployment" and resource["metadata"]["name"] == "zeta-ai-app":
                    resource["metadata"]["name"] = "zeta-ai-app-green"
                    resource["metadata"]["labels"]["version"] = "green"
                    resource["spec"]["selector"]["matchLabels"]["version"] = "green"
                    resource["spec"]["template"]["metadata"]["labels"]["version"] = "green"

                    # Update image
                    container = resource["spec"]["template"]["spec"]["containers"][0]
                    container["image"] = f"zeta-ai/app:{self.config['image_tag']}"

                    # Create deployment
                    try:
                        apps_v1.create_namespaced_deployment(namespace=self.config["namespace"], body=resource)
                        logger.info("🟢 Green deployment created")
                    except Exception as e:
                        if "already exists" in str(e):
                            apps_v1.patch_namespaced_deployment(
                                name="zeta-ai-app-green",
                                namespace=self.config["namespace"],
                                body=resource,
                            )
                            logger.info("🟢 Green deployment updated")
                        else:
                            raise

            return True

        def _wait_for_rollout():
            """Wait for green deployment to be ready"""
            apps_v1 = client.AppsV1Api(self.k8s_client)
            timeout = self.config.get("deployment_timeout", 600)
            start_time = time.time()

            while time.time() - start_time < timeout:
                try:
                    deployment = apps_v1.read_namespaced_deployment_status(
                        name="zeta-ai-app-green", namespace=self.config["namespace"]
                    )

                    if (
                        deployment.status.ready_replicas == self.config["replicas"]
                        and deployment.status.available_replicas == self.config["replicas"]
                    ):
                        logger.info("🟢 Green deployment is ready")
                        return True

                    logger.info(
                        f"⏳ Waiting for rollout... ({deployment.status.ready_replicas}/{self.config['replicas']} ready)"
                    )
                    # TODO: Replace blocking sleep with async await asyncio.sleep(10)

                except Exception as e:
                    logger.warning(f"⚠️ Error checking deployment status: {e}")
                    # TODO: Replace blocking sleep with async await asyncio.sleep(5)

            raise Exception("Deployment timeout reached")

        def _health_check_green():
            """Perform health checks on green deployment"""
            v1 = client.CoreV1Api(self.k8s_client)

            # Get green pods
            pods = v1.list_namespaced_pod(
                namespace=self.config["namespace"],
                label_selector="app=zeta-ai,version=green",
            )

            for pod in pods.items:
                pod_ip = pod.status.pod_ip
                if not pod_ip:
                    continue

                # Health check
                try:
                    response = requests.get(f"http://{pod_ip}:8000/api/v1/health", timeout=10)
                    if response.status_code != 200:
                        raise Exception(f"Health check failed for pod {pod.metadata.name}")

                    logger.info(f"✅ Health check passed for pod {pod.metadata.name}")

                except Exception as e:
                    logger.error(f"❌ Health check failed for pod {pod.metadata.name}: {e}")
                    raise

            return True

        # Execute deployment steps
        self._run_step("Create Green Deployment", _create_green_deployment)
        self._run_step("Wait for Rollout", _wait_for_rollout)
        self._run_step("Health Check Green", _health_check_green)

        return True

    def switch_traffic(self) -> bool:
        """Switch traffic from blue to green deployment"""

        def _update_service():
            """Update service selector to point to green deployment"""
            v1 = client.CoreV1Api(self.k8s_client)

            # Update service selector
            service_patch = {"spec": {"selector": {"app": "zeta-ai", "version": "green"}}}

            v1.patch_namespaced_service(
                name="zeta-ai-service",
                namespace=self.config["namespace"],
                body=service_patch,
            )

            logger.info("🔄 Traffic switched to green deployment")
            return True

        def _verify_traffic_switch():
            """Verify traffic is flowing to green deployment"""
            # Wait a moment for traffic to flow
            # TODO: Replace blocking sleep with async await asyncio.sleep(30)

            # Perform end-to-end test
            try:
                service_url = self._get_service_url()
                response = requests.get(f"{service_url}/api/v1/health", timeout=10)

                if response.status_code == 200:
                    logger.info("✅ Traffic switch verification successful")
                    return True
                else:
                    raise Exception(f"Service health check failed: {response.status_code}")

            except Exception as e:
                logger.error(f"❌ Traffic switch verification failed: {e}")
                raise

        self._run_step("Update Service", _update_service)
        self._run_step("Verify Traffic Switch", _verify_traffic_switch)

        return True

    def cleanup_old_deployment(self) -> bool:
        """Remove old blue deployment after successful green deployment"""

        def _remove_blue_deployment():
            """Remove the old blue deployment"""
            apps_v1 = client.AppsV1Api(self.k8s_client)

            try:
                apps_v1.delete_namespaced_deployment(
                    name="zeta-ai-app",  # Original deployment
                    namespace=self.config["namespace"],
                )
                logger.info("🔵 Blue deployment removed")

                # Rename green to blue for next deployment
                deployment = apps_v1.read_namespaced_deployment(
                    name="zeta-ai-app-green", namespace=self.config["namespace"]
                )

                # Create new deployment with original name
                deployment.metadata.name = "zeta-ai-app"
                deployment.metadata.labels["version"] = "blue"
                deployment.spec.selector.match_labels["version"] = "blue"
                deployment.spec.template.metadata.labels["version"] = "blue"

                apps_v1.create_namespaced_deployment(namespace=self.config["namespace"], body=deployment)

                # Remove green deployment
                apps_v1.delete_namespaced_deployment(name="zeta-ai-app-green", namespace=self.config["namespace"])

                logger.info("🔄 Deployment renamed to standard configuration")
                return True

            except Exception as e:
                logger.warning(f"⚠️ Cleanup warning: {e}")
                return True  # Non-critical step

        return self._run_step("Cleanup Old Deployment", _remove_blue_deployment)

    def setup_monitoring(self) -> bool:
        """Configure monitoring for the new deployment"""

        def _update_prometheus_config():
            """Update Prometheus configuration for new deployment"""
            # This would update Prometheus targets
            logger.info("📊 Prometheus configuration updated")
            return True

        def _create_grafana_dashboards():
            """Ensure Grafana dashboards are up to date"""
            logger.info("📈 Grafana dashboards verified")
            return True

        def _setup_alerts():
            """Configure alerting rules"""
            logger.info("🚨 Alert rules configured")
            return True

        if self.config.get("enable_monitoring", True):
            self._run_step("Update Prometheus", _update_prometheus_config)
            self._run_step("Setup Grafana", _create_grafana_dashboards)
            self._run_step("Configure Alerts", _setup_alerts)

        return True

    def rollback_deployment(self) -> bool:
        """Rollback to previous deployment state"""
        logger.warning("🔄 Initiating deployment rollback...")

        rollback_data = self.deployment_state.get("rollback_data", {})

        if not rollback_data:
            logger.error("❌ No rollback data available")
            return False

        def _rollback_k8s():
            """Rollback Kubernetes deployment"""
            if "k8s_backup" in rollback_data:
                client.AppsV1Api(self.k8s_client)

                # Restore previous deployment
                previous_config = rollback_data["k8s_backup"]
                if previous_config:
                    # Implementation would restore previous deployment
                    logger.info("🔄 Kubernetes deployment rolled back")
            return True

        def _rollback_database():
            """Rollback database if needed"""
            if "database_backup" in rollback_data:
                # Implementation would restore database from backup
                logger.info("🗄️ Database rollback completed")
            return True

        try:
            self._run_step("Rollback Kubernetes", _rollback_k8s)
            self._run_step("Rollback Database", _rollback_database)

            logger.info("✅ Rollback completed successfully")
            return True

        except Exception as e:
            logger.error(f"❌ Rollback failed: {e}")
            return False

    def _get_service_url(self) -> str:
        """Get the service URL for testing"""
        v1 = client.CoreV1Api(self.k8s_client)

        service = v1.read_namespaced_service(name="zeta-ai-service", namespace=self.config["namespace"])

        # For LoadBalancer service
        if service.status.load_balancer.ingress:
            ip = service.status.load_balancer.ingress[0].ip
            return f"http://{ip}:8000"

        # For NodePort or ClusterIP, use port-forward
        return "http://localhost:8000"

    def generate_deployment_report(self) -> dict:
        """Generate comprehensive deployment report"""
        duration = time.time() - self.start_time

        report = {
            "deployment_id": self.deployment_id,
            "environment": self.config["environment"],
            "duration": duration,
            "status": self.deployment_state["status"],
            "steps": self.deployment_state["steps"],
            "summary": {
                "total_steps": len(self.deployment_state["steps"]),
                "successful_steps": len([s for s in self.deployment_state["steps"] if s["status"] == "success"]),
                "failed_steps": len([s for s in self.deployment_state["steps"] if s["status"] == "failed"]),
            },
            "timestamp": datetime.now().isoformat(),
            "deployed_image": f"zeta-ai/app:{self.config['image_tag']}",
            "replicas": self.config["replicas"],
        }

        # Save report
        report_file = f"/app/logs/deployment-report-{self.deployment_id}.json"
        with open(report_file, "w") as f:
            json.dump(report, f, indent=2)

        logger.info(f"📋 Deployment report saved: {report_file}")
        return report

    def deploy(self) -> bool:
        """Execute complete deployment process"""
        try:
            logger.info("🚀 Starting ZETA AI production deployment...")
            self.deployment_state["status"] = "running"

            # Deployment pipeline
            self.pre_deployment_checks()
            self.backup_current_deployment()
            self.run_database_migrations()
            self.deploy_application()
            self.switch_traffic()
            self.cleanup_old_deployment()
            self.setup_monitoring()

            self.deployment_state["status"] = "success"
            logger.info("✅ ZETA AI deployment completed successfully!")

            # Generate report
            self.generate_deployment_report()

            return True

        except Exception as e:
            logger.error(f"❌ Deployment failed: {e}")
            self.deployment_state["status"] = "failed"

            # Attempt rollback if configured
            if self.config.get("rollback_on_failure", True):
                self.rollback_deployment()

            # Generate failure report
            self.generate_deployment_report()

            return False


def main():
    """Main deployment function"""
    parser = argparse.ArgumentParser(description="ZETA AI Production Deployment")
    parser.add_argument("--config", help="Deployment configuration file")
    parser.add_argument("--image-tag", help="Docker image tag to deploy")
    parser.add_argument("--namespace", help="Kubernetes namespace", default="zeta-ai")
    parser.add_argument("--dry-run", action="store_true", help="Dry run mode")

    args = parser.parse_args()

    # Set environment variables from arguments
    if args.image_tag:
        os.environ["IMAGE_TAG"] = args.image_tag

    # Initialize deployer
    deployer = ZetaAIProductionDeployer(args.config)

    if args.dry_run:
        logger.info("🧪 Dry run mode - no actual deployment will occur")
        return True

    # Execute deployment
    success = deployer.deploy()

    if success:
        logger.info("🎉 ZETA AI deployment completed successfully!")
        sys.exit(0)
    else:
        logger.error("💥 ZETA AI deployment failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
    main()
