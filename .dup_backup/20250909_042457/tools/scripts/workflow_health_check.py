#!/usr/bin/env python3
"""
ZETA AI - Workflow Health Check Tool
Kiểm tra tính nhất quán và health của GitHub Actions workflows
"""

import json
import logging
import re
import sys
from pathlib import Path
from typing import Any

import yaml
import Exception
import any
import description
import dict
import e
import env_value
import f
import file
import filename
import files
import i
import isinstance
import issue
import issue_type
import job_config
import job_name
import key
import len
import list
import max
import open
import pattern
import print
import self
import sorted
import step
import str
import trigger
import workflow
import yaml_file

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class WorkflowHealthChecker:
    """GitHub Actions Workflow Health Checker"""

    def __init__(self, workflows_dir: Path):
        self.workflows_dir = workflows_dir
        self.workflows: dict[str, dict] = {}
        self.issues: list[dict] = []

    def load_workflows(self) -> None:
        """Load tất cả workflow files"""
        logger.info("🔍 Loading workflows...")

        for yaml_file in self.workflows_dir.glob("*.yml"):
            try:
                with open(yaml_file, encoding="utf-8") as f:
                    content = yaml.safe_load(f)
                    self.workflows[yaml_file.name] = content
                    logger.debug(f"✅ Loaded {yaml_file.name}")
            except Exception as e:
                self.add_issue("LOAD_ERROR", f"Failed to load {yaml_file.name}: {e}")

        logger.info(f"📊 Loaded {len(self.workflows)} workflows")

    def add_issue(self, issue_type: str, description: str, file: str = None) -> None:
        """Thêm issue vào danh sách"""
        self.issues.append(
            {
                "type": issue_type,
                "description": description,
                "file": file,
                "severity": self.get_severity(issue_type),
            }
        )

    def get_severity(self, issue_type: str) -> str:
        """Xác định mức độ nghiêm trọng"""
        critical = ["SYNTAX_ERROR", "MISSING_REQUIRED", "SECURITY_ISSUE"]
        warning = ["NAMING_INCONSISTENCY", "DUPLICATE_TRIGGER", "PERFORMANCE"]

        if issue_type in critical:
            return "CRITICAL"
        elif issue_type in warning:
            return "WARNING"
        else:
            return "INFO"

    def check_naming_convention(self) -> None:
        """Kiểm tra naming convention"""
        logger.info("🏷️  Checking naming conventions...")

        expected_patterns = {
            "ci-": r"^ci-[a-z]+\.yml$",
            "desktop-": r"^desktop-[a-z]+\.yml$",
            "auto-": r"^auto-[a-z-]+\.yml$",
            "contract": r"^contract.*\.yml$",
        }

        for filename, workflow in self.workflows.items():
            # Check filename convention
            name_compliant = any(re.match(pattern, filename) for pattern in expected_patterns.values()) or filename in [
                "ai-self-management.yml",
                "guards.yml",
                "compliance.yml",
                "production-cicd.yml",
                "build-docker.yml",
                "deploy-k8s.yml",
                "chaos-staging.yml",
                "importlinter.yml",
                "duplicate-check.yml",
                "focus-guard.yml",
                "map-enforcer.yml",
                "barrel-check.yml",
                "copilot_manifest_check.yml",
                "dependency-map-check.yml",
                "publish-desktop.yml",
                "publish-windows.yml",
                "release-electron.yml",
            ]

            if not name_compliant:
                self.add_issue(
                    "NAMING_INCONSISTENCY",
                    f"Filename '{filename}' doesn't follow naming convention",
                    filename,
                )

            # Check workflow name consistency
            if "name" in workflow:
                workflow_name = workflow["name"]
                if not workflow_name or len(workflow_name.strip()) == 0:
                    self.add_issue("NAMING_INCONSISTENCY", f"Empty workflow name in {filename}", filename)

    def check_trigger_consistency(self) -> None:
        """Kiểm tra trigger consistency"""
        logger.info("🔄 Checking trigger consistency...")

        trigger_conflicts = {}

        for filename, workflow in self.workflows.items():
            if "on" not in workflow:
                self.add_issue("MISSING_REQUIRED", f"Missing 'on' trigger in {filename}", filename)
                continue

            triggers = workflow["on"]
            if isinstance(triggers, str):
                triggers = [triggers]
            elif isinstance(triggers, dict):
                triggers = list(triggers.keys())

            for trigger in triggers:
                if trigger not in trigger_conflicts:
                    trigger_conflicts[trigger] = []
                trigger_conflicts[trigger].append(filename)

        # Kiểm tra potential conflicts
        for trigger, files in trigger_conflicts.items():
            if trigger == "push" and len(files) > 5:
                self.add_issue(
                    "PERFORMANCE",
                    f"Too many workflows ({len(files)}) triggered on 'push': {', '.join(files)}",
                )

    def check_required_components(self) -> None:
        """Kiểm tra các components bắt buộc"""
        logger.info("🔧 Checking required components...")

        for filename, workflow in self.workflows.items():
            # Check required top-level keys
            required_keys = ["name", "on", "jobs"]
            for key in required_keys:
                if key not in workflow:
                    self.add_issue("MISSING_REQUIRED", f"Missing required key '{key}' in {filename}", filename)

            # Check jobs structure
            if "jobs" in workflow:
                jobs = workflow["jobs"]
                if not jobs or len(jobs) == 0:
                    self.add_issue("MISSING_REQUIRED", f"No jobs defined in {filename}", filename)

                for job_name, job_config in jobs.items():
                    if "runs-on" not in job_config:
                        self.add_issue(
                            "MISSING_REQUIRED",
                            f"Job '{job_name}' missing 'runs-on' in {filename}",
                            filename,
                        )

    def check_security_practices(self) -> None:
        """Kiểm tra security best practices"""
        logger.info("🔒 Checking security practices...")

        for filename, workflow in self.workflows.items():
            # Check for hardcoded secrets
            workflow_str = str(workflow)
            if re.search(
                r'(password|token|key|secret).*[:=]\s*["\'][^"\']{10,}["\']',
                workflow_str,
                re.IGNORECASE,
            ):
                self.add_issue("SECURITY_ISSUE", f"Potential hardcoded secret in {filename}", filename)

            # Check for proper secret usage
            if "jobs" in workflow:
                for job_name, job_config in workflow["jobs"].items():
                    if "steps" in job_config:
                        for step in job_config["steps"]:
                            if "env" in step:
                                for env_key, env_value in step["env"].items():
                                    if isinstance(env_value, str) and "secret" in env_value.lower():
                                        if not env_value.startswith("${{ secrets."):
                                            self.add_issue(
                                                "SECURITY_ISSUE",
                                                f"Improper secret usage in {filename}, job {job_name}",
                                                filename,
                                            )

    def check_performance_patterns(self) -> None:
        """Kiểm tra performance patterns"""
        logger.info("⚡ Checking performance patterns...")

        for filename, workflow in self.workflows.items():
            if "jobs" in workflow:
                total_jobs = len(workflow["jobs"])
                if total_jobs > 10:
                    self.add_issue(
                        "PERFORMANCE",
                        f"High number of jobs ({total_jobs}) in {filename} may impact performance",
                        filename,
                    )

                # Check for missing dependency optimization
                for job_name, job_config in workflow["jobs"].items():
                    if "needs" not in job_config and total_jobs > 3:
                        self.add_issue(
                            "PERFORMANCE",
                            f"Job '{job_name}' in {filename} might benefit from 'needs' dependency",
                            filename,
                        )

    def generate_report(self) -> dict[str, Any]:
        """Tạo health report"""
        logger.info("📊 Generating health report...")

        issues_by_severity = {
            "CRITICAL": [i for i in self.issues if i["severity"] == "CRITICAL"],
            "WARNING": [i for i in self.issues if i["severity"] == "WARNING"],
            "INFO": [i for i in self.issues if i["severity"] == "INFO"],
        }

        issues_by_file = {}
        for issue in self.issues:
            if issue["file"]:
                if issue["file"] not in issues_by_file:
                    issues_by_file[issue["file"]] = []
                issues_by_file[issue["file"]].append(issue)

        health_score = max(
            0,
            100
            - (
                len(issues_by_severity["CRITICAL"]) * 20
                + len(issues_by_severity["WARNING"]) * 5
                + len(issues_by_severity["INFO"]) * 1
            ),
        )

        return {
            "summary": {
                "total_workflows": len(self.workflows),
                "total_issues": len(self.issues),
                "health_score": health_score,
                "status": "HEALTHY" if health_score >= 90 else "WARNING" if health_score >= 70 else "CRITICAL",
            },
            "issues_by_severity": issues_by_severity,
            "issues_by_file": issues_by_file,
            "workflows": list(self.workflows.keys()),
        }

    def run_full_check(self) -> dict[str, Any]:
        """Chạy đầy đủ health check"""
        logger.info("🚀 Starting workflow health check...")

        self.load_workflows()
        self.check_naming_convention()
        self.check_trigger_consistency()
        self.check_required_components()
        self.check_security_practices()
        self.check_performance_patterns()

        return self.generate_report()


def main():
    """Main function"""
    root_dir = Path(__file__).parent.parent
    workflows_dir = root_dir / ".github" / "workflows"

    if not workflows_dir.exists():
        logger.error(f"❌ Workflows directory not found: {workflows_dir}")
        sys.exit(1)

    checker = WorkflowHealthChecker(workflows_dir)
    report = checker.run_full_check()

    # Print report
    print("\n" + "=" * 60)
    print("🎯 WORKFLOW HEALTH REPORT")
    print("=" * 60)

    summary = report["summary"]
    print(f"📊 Total Workflows: {summary['total_workflows']}")
    print(f"🔍 Total Issues: {summary['total_issues']}")
    print(f"💯 Health Score: {summary['health_score']}/100")
    print(f"🎯 Status: {summary['status']}")

    if report["issues_by_severity"]["CRITICAL"]:
        print(f"\n🚨 CRITICAL ISSUES ({len(report['issues_by_severity']['CRITICAL'])}):")
        for issue in report["issues_by_severity"]["CRITICAL"]:
            print(f"  ❌ {issue['description']}")

    if report["issues_by_severity"]["WARNING"]:
        print(f"\n⚠️  WARNING ISSUES ({len(report['issues_by_severity']['WARNING'])}):")
        for issue in report["issues_by_severity"]["WARNING"]:
            print(f"  ⚠️  {issue['description']}")

    if report["issues_by_severity"]["INFO"]:
        print(f"\n💡 INFO ISSUES ({len(report['issues_by_severity']['INFO'])}):")
        for issue in report["issues_by_severity"]["INFO"]:
            print(f"  💡 {issue['description']}")

    print("\n✅ HEALTHY WORKFLOWS:")
    healthy_workflows = []
    for workflow in report["workflows"]:
        if workflow not in report["issues_by_file"]:
            healthy_workflows.append(workflow)

    for workflow in sorted(healthy_workflows):
        print(f"  ✅ {workflow}")

    print("\n" + "=" * 60)

    # Save detailed report
    report_file = root_dir / "reports" / "workflow_health_report.json"
    report_file.parent.mkdir(exist_ok=True)

    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    logger.info(f"📄 Detailed report saved to: {report_file}")

    # Exit with appropriate code
    if summary["status"] == "CRITICAL":
        sys.exit(1)
    elif summary["status"] == "WARNING":
        sys.exit(0)  # Warning không fail build
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
