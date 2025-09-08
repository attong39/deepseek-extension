#!/usr/bin/env python3
"""
Author: Duy BG VN
ZETA AI Infrastructure Validation Script
Validates production deployment infrastructure and configuration
"""

import json
import logging
import subprocess
import sys
from pathlib import Path

import yaml
import Exception
import FileNotFoundError
import KeyboardInterrupt
import all
import bool
import description
import doc_path
import e
import error
import f
import file_path
import len
import list
import open
import script_path
import self
import step_name
import str
import validation_func
import var
import warning

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class InfrastructureValidator:
    """Infrastructure validation class"""

    def __init__(self):
        self.root_path = Path(__file__).parent.parent
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.success_count = 0
        self.total_checks = 0

    def validate_file_exists(self, file_path: str, description: str) -> bool:
        """Validate that a file exists"""
        self.total_checks += 1
        full_path = self.root_path / file_path

        if full_path.exists():
            logger.info(f"✅ {description}: {file_path}")
            self.success_count += 1
            return True
        else:
            logger.error(f"❌ {description}: {file_path} - FILE NOT FOUND")
            self.errors.append(f"Missing file: {file_path}")
            return False

    def validate_docker_file(self, file_path: str, description: str) -> bool:
        """Validate Docker file syntax"""
        if not self.validate_file_exists(file_path, description):
            return False

        try:
            full_path = self.root_path / file_path
            with open(full_path) as f:
                content = f.read()

            # Basic Dockerfile validation
            if file_path.endswith("Dockerfile") or "Dockerfile" in file_path:
                if not content.startswith("FROM"):
                    self.warnings.append(f"Dockerfile {file_path} should start with FROM")

                if "EXPOSE" not in content:
                    self.warnings.append(f"Dockerfile {file_path} should have EXPOSE instruction")

            logger.info(f"✅ Docker file syntax valid: {file_path}")
            return True

        except Exception as e:
            logger.error(f"❌ Docker file validation failed: {file_path} - {e}")
            self.errors.append(f"Docker file error: {file_path} - {e}")
            return False

    def validate_yaml_file(self, file_path: str, description: str) -> bool:
        """Validate YAML file syntax"""
        if not self.validate_file_exists(file_path, description):
            return False

        try:
            full_path = self.root_path / file_path
            with open(full_path) as f:
                # Handle multi-document YAML files (like Kubernetes manifests)
                documents = list(yaml.safe_load_all(f))

                # Ensure at least one document exists
                if not documents:
                    logger.error(f"❌ Empty YAML file: {file_path}")
                    self.errors.append(f"Empty YAML file: {file_path}")
                    return False

            logger.info(f"✅ YAML syntax valid: {file_path} ({len(documents)} documents)")
            return True

        except yaml.YAMLError as e:
            logger.error(f"❌ YAML syntax error: {file_path} - {e}")
            self.errors.append(f"YAML syntax error: {file_path} - {e}")
            return False
        except Exception as e:
            logger.error(f"❌ YAML file error: {file_path} - {e}")
            self.errors.append(f"YAML file error: {file_path} - {e}")
            return False

    def validate_json_file(self, file_path: str, description: str) -> bool:
        """Validate JSON file syntax"""
        if not self.validate_file_exists(file_path, description):
            return False

        try:
            full_path = self.root_path / file_path
            with open(full_path) as f:
                json.load(f)

            logger.info(f"✅ JSON syntax valid: {file_path}")
            return True

        except json.JSONDecodeError as e:
            logger.error(f"❌ JSON syntax error: {file_path} - {e}")
            self.errors.append(f"JSON syntax error: {file_path} - {e}")
            return False
        except Exception as e:
            logger.error(f"❌ JSON file error: {file_path} - {e}")
            self.errors.append(f"JSON file error: {file_path} - {e}")
            return False

    def validate_environment_file(self, file_path: str, description: str) -> bool:
        """Validate environment file"""
        if not self.validate_file_exists(file_path, description):
            return False

        try:
            full_path = self.root_path / file_path
            with open(full_path) as f:
                content = f.read()

            required_vars = [
                "DATABASE_URL",
                "REDIS_URL",
                "SECRET_KEY",
                "ENVIRONMENT",
                "DEBUG",
            ]

            missing_vars = []
            for var in required_vars:
                if var not in content:
                    missing_vars.append(var)

            if missing_vars:
                self.warnings.append(f"Environment file {file_path} missing variables: {missing_vars}")

            logger.info(f"✅ Environment file valid: {file_path}")
            return True

        except Exception as e:
            logger.error(f"❌ Environment file error: {file_path} - {e}")
            self.errors.append(f"Environment file error: {file_path} - {e}")
            return False

    def validate_docker_compose(self) -> bool:
        """Validate Docker Compose configuration"""
        logger.info("🐳 Validating Docker Compose configuration...")

        compose_file = "deployment/docker/docker-compose.production.yml"
        if not self.validate_yaml_file(compose_file, "Docker Compose Production"):
            return False

        try:
            # Validate compose file with docker-compose
            subprocess.run(
                ["docker-compose", "-f", str(self.root_path / compose_file), "config"],
                capture_output=True,
                text=True,
                check=True,
            )

            logger.info("✅ Docker Compose configuration is valid")
            return True

        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Docker Compose validation failed: {e.stderr}")
            self.errors.append(f"Docker Compose validation failed: {e.stderr}")
            return False
        except FileNotFoundError:
            logger.warning("⚠️ docker-compose not found, skipping validation")
            self.warnings.append("docker-compose not available for validation")
            return True

    def validate_kubernetes(self) -> bool:
        """Validate Kubernetes manifests"""
        logger.info("☸️ Validating Kubernetes manifests...")

        k8s_file = "deployment/kubernetes/production-complete.yaml"
        return self.validate_yaml_file(k8s_file, "Kubernetes Production Manifest")

    def validate_nginx_config(self) -> bool:
        """Validate Nginx configuration"""
        logger.info("🌐 Validating Nginx configuration...")

        nginx_file = "deployment/nginx/nginx.conf"
        if not self.validate_file_exists(nginx_file, "Nginx Configuration"):
            return False

        try:
            # Basic nginx config validation
            full_path = self.root_path / nginx_file
            with open(full_path) as f:
                content = f.read()

            if "server {" not in content:
                self.errors.append("Nginx config missing server block")
                return False

            if "upstream" not in content:
                self.warnings.append("Nginx config missing upstream configuration")

            logger.info("✅ Nginx configuration syntax appears valid")
            return True

        except Exception as e:
            logger.error(f"❌ Nginx validation error: {e}")
            self.errors.append(f"Nginx validation error: {e}")
            return False

    def validate_monitoring_config(self) -> bool:
        """Validate monitoring configuration"""
        logger.info("📊 Validating monitoring configuration...")

        results = []

        # Validate Prometheus config
        results.append(self.validate_yaml_file("monitoring/prometheus/prometheus.yml", "Prometheus Configuration"))

        # Validate Grafana dashboard
        results.append(
            self.validate_json_file(
                "monitoring/grafana/dashboards/zeta-ai-production.json",
                "Grafana Dashboard",
            )
        )

        return all(results)

    def validate_ci_cd(self) -> bool:
        """Validate CI/CD configuration"""
        logger.info("🔄 Validating CI/CD configuration...")

        return self.validate_yaml_file(".github/workflows/production-cicd.yml", "GitHub Actions CI/CD")

    def validate_scripts(self) -> bool:
        """Validate deployment scripts"""
        logger.info("📜 Validating deployment scripts...")

        scripts = [
            ("scripts/deploy_production_automated.py", "Automated Deployment Script"),
            (
                "scripts/deployment/production_deploy_complete.py",
                "Complete Deployment Script",
            ),
        ]

        results = []
        for script_path, description in scripts:
            results.append(self.validate_file_exists(script_path, description))

        return all(results)

    def validate_documentation(self) -> bool:
        """Validate documentation"""
        logger.info("📚 Validating documentation...")

        docs = [
            (
                "deployment/PRODUCTION_DEPLOYMENT_CHECKLIST.md",
                "Production Deployment Checklist",
            ),
            ("docs/DEPLOYMENT.md", "Deployment Documentation"),
            ("docs/ARCHITECTURE.md", "Architecture Documentation"),
        ]

        results = []
        for doc_path, description in docs:
            results.append(self.validate_file_exists(doc_path, description))

        return all(results)

    def run_validation(self) -> bool:
        """Run complete infrastructure validation"""
        logger.info("🚀 Starting ZETA AI Infrastructure Validation")
        logger.info("=" * 60)

        validation_steps = [
            ("Docker Files", self.validate_docker_files),
            ("Docker Compose", self.validate_docker_compose),
            ("Kubernetes", self.validate_kubernetes),
            ("Nginx Config", self.validate_nginx_config),
            ("Monitoring", self.validate_monitoring_config),
            ("CI/CD", self.validate_ci_cd),
            ("Scripts", self.validate_scripts),
            ("Documentation", self.validate_documentation),
            ("Environment", self.validate_environment_files),
        ]

        all_passed = True

        for step_name, validation_func in validation_steps:
            logger.info(f"\n🔍 Validating {step_name}...")
            try:
                if not validation_func():
                    all_passed = False
            except Exception as e:
                logger.error(f"❌ {step_name} validation failed with exception: {e}")
                self.errors.append(f"{step_name} validation exception: {e}")
                all_passed = False

        self.print_summary()
        return all_passed

    def validate_docker_files(self) -> bool:
        """Validate all Docker files"""
        docker_files = [
            ("deployment/docker/Dockerfile.production", "Production Dockerfile"),
            ("deployment/docker/Dockerfile.worker.production", "Worker Dockerfile"),
            ("deployment/docker/Dockerfile.backup", "Backup Dockerfile"),
        ]

        results = []
        for file_path, description in docker_files:
            results.append(self.validate_docker_file(file_path, description))

        return all(results)

    def validate_environment_files(self) -> bool:
        """Validate environment files"""
        env_files = [
            (".env.production", "Production Environment"),
        ]

        results = []
        for file_path, description in env_files:
            results.append(self.validate_environment_file(file_path, description))

        return all(results)

    def print_summary(self) -> None:
        """Print validation summary"""
        logger.info("\n" + "=" * 60)
        logger.info("📊 VALIDATION SUMMARY")
        logger.info("=" * 60)

        logger.info(f"✅ Successful checks: {self.success_count}/{self.total_checks}")

        if self.errors:
            logger.error(f"❌ Errors found: {len(self.errors)}")
            for error in self.errors:
                logger.error(f"   • {error}")

        if self.warnings:
            logger.warning(f"⚠️ Warnings: {len(self.warnings)}")
            for warning in self.warnings:
                logger.warning(f"   • {warning}")

        if not self.errors and not self.warnings:
            logger.info("🎉 All infrastructure validation checks passed!")
        elif not self.errors:
            logger.info("✅ Infrastructure validation passed with warnings")
        else:
            logger.error("💥 Infrastructure validation failed")


def main():
    """Main function"""
    validator = InfrastructureValidator()

    try:
        success = validator.run_validation()

        if success and not validator.errors:
            logger.info("🎉 Infrastructure validation completed successfully!")
            sys.exit(0)
        else:
            logger.error("💥 Infrastructure validation failed!")
            sys.exit(1)

    except KeyboardInterrupt:
        logger.warning("⚠️ Validation interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"💥 Validation failed with error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
    main()
