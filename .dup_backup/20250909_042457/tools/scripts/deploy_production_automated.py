#!/usr/bin/env python3
"""
Author: Duy BG VN
ZETA AI Production Deployment Automation
Complete automated production deployment script
"""

import logging
import os
import subprocess
import sys
import Exception
import KeyboardInterrupt
import check
import e
import isinstance
import service_name
import shell
import str
import url

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def run_command(command, check=True, shell=False):
    """Execute shell command with logging"""
    logger.info(f"🔧 Executing: {command}")

    if isinstance(command, str) and not shell:
        command = command.split()

    try:
        result = subprocess.run(command, check=check, capture_output=True, text=True, shell=shell)

        if result.stdout:
            logger.info(f"✅ Output: {result.stdout.strip()}")

        return result

    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Command failed: {e}")
        logger.error(f"❌ Error output: {e.stderr}")
        if check:
            raise
        return e


def deploy_production():
    """Main production deployment function"""

    logger.info("🚀 Starting ZETA AI Production Deployment")

    # Step 1: Build Docker images
    logger.info("📦 Building Docker images...")

    # Build main application image
    run_command(
        [
            "docker",
            "build",
            "-f",
            "deployment/docker/Dockerfile.production",
            "-t",
            "zeta-ai/app:production",
            "zeta_vn/",
        ]
    )

    # Build worker image
    run_command(
        [
            "docker",
            "build",
            "-f",
            "deployment/docker/Dockerfile.worker.production",
            "-t",
            "zeta-ai/worker:production",
            "zeta_vn/",
        ]
    )

    # Build backup image
    run_command(
        [
            "docker",
            "build",
            "-f",
            "deployment/docker/Dockerfile.backup",
            "-t",
            "zeta-ai/backup:production",
            "zeta_vn/",
        ]
    )

    # Step 2: Deploy with Docker Compose
    logger.info("🚀 Deploying with Docker Compose...")

    # Copy environment file
    if not os.path.exists(".env.production"):
        logger.warning("⚠️ .env.production not found, using template")
        run_command(["cp", ".env.production.template", ".env.production"])

    # Deploy services
    run_command(
        [
            "docker-compose",
            "-f",
            "deployment/docker/docker-compose.production.yml",
            "--env-file",
            ".env.production",
            "up",
            "-d",
        ]
    )

    # Step 3: Wait for services to be ready
    logger.info("⏳ Waiting for services to be ready...")
    # TODO: Replace blocking sleep with async await asyncio.sleep(60)

    # Step 4: Health checks
    logger.info("🏥 Performing health checks...")

    health_checks = [
        ("ZETA AI API", "http://localhost:8000/api/v1/health"),
        ("Prometheus", "http://localhost:9090/-/healthy"),
        ("Grafana", "http://localhost:3000/api/health"),
        ("Flower", "http://localhost:5555/api/workers"),
    ]

    for service_name, url in health_checks:
        try:
            result = run_command(["curl", "-f", "-s", url], check=False)

            if result.returncode == 0:
                logger.info(f"✅ {service_name} is healthy")
            else:
                logger.warning(f"⚠️ {service_name} health check failed")

        except Exception as e:
            logger.warning(f"⚠️ {service_name} health check error: {e}")

    # Step 5: Run post-deployment tests
    logger.info("🧪 Running post-deployment tests...")

    try:
        # Change to zeta_vn directory for tests
        os.chdir("zeta_vn")

        # Run smoke tests
        run_command(["python", "-m", "pytest", "tests/smoke/", "-v", "--tb=short"])

        logger.info("✅ Smoke tests passed")

    except Exception as e:
        logger.warning(f"⚠️ Some tests failed: {e}")
    finally:
        # Return to original directory
        os.chdir("..")

    # Step 6: Display deployment summary
    logger.info("📊 Deployment Summary")
    logger.info("=" * 50)

    # Show running containers
    result = run_command(
        [
            "docker-compose",
            "-f",
            "deployment/docker/docker-compose.production.yml",
            "ps",
        ],
        check=False,
    )

    # Show service URLs
    logger.info("🌐 Service URLs:")
    logger.info("  • ZETA AI API: http://localhost:8000")
    logger.info("  • API Docs: http://localhost:8000/docs")
    logger.info("  • Prometheus: http://localhost:9090")
    logger.info("  • Grafana: http://localhost:3000")
    logger.info("  • Flower (Celery): http://localhost:5555")
    logger.info("  • Jaeger: http://localhost:16686")
    logger.info("  • Kibana: http://localhost:5601")

    logger.info("✅ ZETA AI Production Deployment Completed!")

    return True


def main():
    """Main function"""
    try:
        success = deploy_production()

        if success:
            logger.info("🎉 Deployment successful!")
            sys.exit(0)
        else:
            logger.error("💥 Deployment failed!")
            sys.exit(1)

    except KeyboardInterrupt:
        logger.warning("⚠️ Deployment interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"💥 Deployment failed with error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
