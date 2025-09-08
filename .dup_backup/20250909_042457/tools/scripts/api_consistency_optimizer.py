#!/usr/bin/env python3
"""
tools/api_consistency_optimizer.py

Kiểm tra và tối ưu tính nhất quán API giữa desktop_ai_zeta và zeta_vn server.
Phân tích từng component API và đưa ra đề xuất cụ thể.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any
import Exception
import dict
import exc_dir
import file_name
import i
import issue
import len
import list
import print
import py_file
import r
import rec
import self
import set
import str
import sum

ROOT = Path(__file__).resolve().parents[1]
SERVER_ROOT = ROOT / "zeta_vn"
DESKTOP_ROOT = ROOT / "desktop_ai_zeta"


class APIConsistencyOptimizer:
    def __init__(self):
        self.issues: list[dict[str, Any]] = []
        self.recommendations: list[dict[str, Any]] = []

    def analyze_all(self) -> None:
        """Phân tích tất cả các component API."""
        print("🔍 API Consistency Analysis - Desktop ↔ Server")
        print("=" * 60)

        # 1. Error Codes Analysis
        self._analyze_error_codes()

        # 2. Auth Mechanism Analysis
        self._analyze_auth_mechanisms()

        # 3. Generated Types Analysis
        self._analyze_generated_types()

        # 4. API Client Configuration
        self._analyze_api_client_config()

        # 5. Type Safety Analysis
        self._analyze_type_safety()

        # 6. WebSocket Schema Integration
        self._analyze_ws_integration()

        # Report results
        self._generate_optimization_report()

    def _analyze_error_codes(self) -> None:
        """Phân tích error codes consistency."""
        print("\n🚨 Analyzing Error Codes...")

        # Extract server error codes
        server_errors = self._extract_server_error_definitions()

        # Extract desktop error codes
        desktop_errors = self._extract_desktop_error_definitions()

        # Compare and analyze
        missing_in_desktop = server_errors - desktop_errors
        obsolete_in_desktop = desktop_errors - server_errors

        if missing_in_desktop:
            self.issues.append(
                {
                    "category": "ERROR_CODES",
                    "severity": "HIGH",
                    "title": "Missing Error Codes in Desktop",
                    "description": f"Server có {len(missing_in_desktop)} error codes chưa có trong desktop",
                    "codes": list(missing_in_desktop),
                    "file": "desktop_ai_zeta/src/api/errorCodes.ts",
                }
            )

        if obsolete_in_desktop:
            self.issues.append(
                {
                    "category": "ERROR_CODES",
                    "severity": "MEDIUM",
                    "title": "Obsolete Error Codes in Desktop",
                    "description": f"Desktop có {len(obsolete_in_desktop)} error codes không còn trong server",
                    "codes": list(obsolete_in_desktop),
                    "file": "desktop_ai_zeta/src/api/errorCodes.ts",
                }
            )

    def _analyze_auth_mechanisms(self) -> None:
        """Phân tích auth mechanisms consistency."""
        print("\n🔐 Analyzing Auth Mechanisms...")

        # Check server auth config
        server_auth_config = self._extract_server_auth_config()

        # Check desktop auth implementation
        desktop_auth_config = self._extract_desktop_auth_config()

        # JWT vs other mechanisms
        if server_auth_config.get("uses_jwt", False) != desktop_auth_config.get("uses_jwt", False):
            self.issues.append(
                {
                    "category": "AUTH",
                    "severity": "CRITICAL",
                    "title": "Auth Mechanism Mismatch",
                    "description": "Server và desktop sử dụng khác mechanism xác thực",
                    "server_method": server_auth_config.get("method", "unknown"),
                    "desktop_method": desktop_auth_config.get("method", "unknown"),
                    "file": "desktop_ai_zeta/src/api/auth.ts",
                }
            )

        # Token refresh handling
        if not desktop_auth_config.get("has_refresh_handler", False):
            self.recommendations.append(
                {
                    "category": "AUTH",
                    "priority": "HIGH",
                    "title": "Add Automatic Token Refresh",
                    "description": "Desktop nên có automatic token refresh để tránh auth interruptions",
                    "file": "desktop_ai_zeta/src/api/auth.ts",
                }
            )

    def _analyze_generated_types(self) -> None:
        """Phân tích generated types status."""
        print("\n📦 Analyzing Generated Types...")

        generated_dir = DESKTOP_ROOT / "src" / "api" / "generated"

        if not generated_dir.exists():
            self.issues.append(
                {
                    "category": "GENERATED_TYPES",
                    "severity": "CRITICAL",
                    "title": "Missing Generated API Types",
                    "description": "Thư mục generated/ không tồn tại",
                    "action": "Chạy npm run api:gen",
                }
            )
            return

        # Check file completeness
        required_files = ["client.ts", "types.ts", "schema.d.ts", "index.d.ts"]
        missing_files = []

        for file_name in required_files:
            file_path = generated_dir / file_name
            if not file_path.exists():
                missing_files.append(file_name)
            else:
                # Check if file has real content vs placeholder
                content = file_path.read_text(encoding="utf-8")
                if len(content.strip()) < 100 or "placeholder" in content.lower():
                    missing_files.append(f"{file_name} (placeholder)")

        if missing_files:
            self.issues.append(
                {
                    "category": "GENERATED_TYPES",
                    "severity": "HIGH",
                    "title": "Incomplete Generated Types",
                    "description": f"Thiếu hoặc có placeholder content: {missing_files}",
                    "action": "Regenerate API types từ server OpenAPI spec",
                }
            )

    def _analyze_api_client_config(self) -> None:
        """Phân tích API client configuration."""
        print("\n⚙️ Analyzing API Client Config...")

        api_client_file = DESKTOP_ROOT / "src" / "api" / "apiClient.ts"
        if not api_client_file.exists():
            self.issues.append(
                {
                    "category": "API_CLIENT",
                    "severity": "CRITICAL",
                    "title": "Missing API Client",
                    "description": "apiClient.ts không tồn tại",
                }
            )
            return

        content = api_client_file.read_text(encoding="utf-8")

        # Check timeout configuration
        if "timeout:" not in content:
            self.recommendations.append(
                {
                    "category": "API_CLIENT",
                    "priority": "MEDIUM",
                    "title": "Add Request Timeout",
                    "description": "Nên có timeout configuration để tránh hanging requests",
                    "file": "desktop_ai_zeta/src/api/apiClient.ts",
                }
            )

        # Check error handling
        if "interceptors.response.use" not in content:
            self.recommendations.append(
                {
                    "category": "API_CLIENT",
                    "priority": "HIGH",
                    "title": "Add Response Interceptor",
                    "description": "Nên có response interceptor để handle errors consistently",
                    "file": "desktop_ai_zeta/src/api/apiClient.ts",
                }
            )

        # Check tracing/monitoring integration
        if "trace" not in content.lower() and "telemetry" not in content:
            self.recommendations.append(
                {
                    "category": "API_CLIENT",
                    "priority": "LOW",
                    "title": "Add Request Tracing",
                    "description": "Consider adding request tracing cho debugging",
                    "file": "desktop_ai_zeta/src/api/apiClient.ts",
                }
            )

    def _analyze_type_safety(self) -> None:
        """Phân tích type safety của API calls."""
        print("\n🛡️ Analyzing Type Safety...")

        typed_client_file = DESKTOP_ROOT / "src" / "api" / "typedClient.ts"

        if not typed_client_file.exists():
            self.recommendations.append(
                {
                    "category": "TYPE_SAFETY",
                    "priority": "HIGH",
                    "title": "Create Typed API Client",
                    "description": "Tạo typed client wrapper để type safety 100%",
                    "file": "desktop_ai_zeta/src/api/typedClient.ts",
                }
            )
        else:
            content = typed_client_file.read_text(encoding="utf-8")

            # Check generic type support
            if "<Res" not in content:
                self.recommendations.append(
                    {
                        "category": "TYPE_SAFETY",
                        "priority": "MEDIUM",
                        "title": "Enhance Generic Type Support",
                        "description": "Cải thiện generic types cho request/response",
                        "file": "desktop_ai_zeta/src/api/typedClient.ts",
                    }
                )

    def _analyze_ws_integration(self) -> None:
        """Phân tích WebSocket schema integration."""
        print("\n🔌 Analyzing WebSocket Integration...")

        ws_schema_file = DESKTOP_ROOT / "src" / "api" / "wsSchema.ts"

        if not ws_schema_file.exists():
            self.issues.append(
                {
                    "category": "WEBSOCKET",
                    "severity": "HIGH",
                    "title": "Missing WebSocket Schema",
                    "description": "wsSchema.ts không tồn tại",
                    "action": "Tạo WebSocket schema definitions",
                }
            )
        else:
            content = ws_schema_file.read_text(encoding="utf-8")

            # Check if it's just a re-export
            if "export * from" in content and len(content.strip()) < 200:
                self.recommendations.append(
                    {
                        "category": "WEBSOCKET",
                        "priority": "MEDIUM",
                        "title": "Consider Direct Schema Definitions",
                        "description": "Có thể define schemas trực tiếp thay vì re-export",
                        "file": "desktop_ai_zeta/src/api/wsSchema.ts",
                    }
                )

    def _extract_server_error_definitions(self) -> set[str]:
        """Extract error codes từ server exception definitions."""
        error_codes = set()

        # Scan exception files
        exception_dirs = [
            SERVER_ROOT / "core" / "exceptions",
            SERVER_ROOT / "app" / "exceptions",
            SERVER_ROOT / "app" / "errors",
        ]

        for exc_dir in exception_dirs:
            if not exc_dir.exists():
                continue

            for py_file in exc_dir.glob("*.py"):
                try:
                    content = py_file.read_text(encoding="utf-8")
                    # Find error code constants
                    codes = re.findall(r'["\']([A-Z_]+_\d{3})["\']', content)
                    error_codes.update(codes)

                    # Find class-based error codes
                    class_codes = re.findall(r'code\s*=\s*["\']([A-Z_]+_\d{3})["\']', content)
                    error_codes.update(class_codes)
                except Exception:
                    continue

        return error_codes

    def _extract_desktop_error_definitions(self) -> set[str]:
        """Extract error codes từ desktop error definitions."""
        error_codes = set()

        error_file = DESKTOP_ROOT / "src" / "api" / "errorCodes.ts"
        if error_file.exists():
            try:
                content = error_file.read_text(encoding="utf-8")
                # Find error codes in ERROR_MESSAGES object
                codes = re.findall(r'["\']([A-Z_]+_\d{3})["\']:', content)
                error_codes.update(codes)

                # Find backward-compat aliases
                aliases = re.findall(r'([A-Z_]+):\s*["\']', content)
                error_codes.update(aliases)
            except Exception:
                pass

        return error_codes

    def _extract_server_auth_config(self) -> dict[str, Any]:
        """Extract auth configuration từ server."""
        config = {"uses_jwt": False, "method": "unknown"}

        # Check auth dependencies
        deps_file = SERVER_ROOT / "app" / "dependencies.py"
        if deps_file.exists():
            try:
                content = deps_file.read_text(encoding="utf-8")
                if "jwt" in content.lower() or "token" in content.lower():
                    config["uses_jwt"] = True
                    config["method"] = "JWT"
            except Exception:
                pass

        return config

    def _extract_desktop_auth_config(self) -> dict[str, Any]:
        """Extract auth configuration từ desktop."""
        config = {"uses_jwt": False, "method": "unknown", "has_refresh_handler": False}

        auth_file = DESKTOP_ROOT / "src" / "api" / "auth.ts"
        if auth_file.exists():
            try:
                content = auth_file.read_text(encoding="utf-8")
                if "token" in content.lower():
                    config["uses_jwt"] = True
                    config["method"] = "JWT"

                if "refresh" in content.lower():
                    config["has_refresh_handler"] = True
            except Exception:
                pass

        return config

    def _generate_optimization_report(self) -> None:
        """Generate comprehensive optimization report."""
        print("\n" + "=" * 60)
        print("📊 API CONSISTENCY OPTIMIZATION REPORT")
        print("=" * 60)

        # Issues Summary
        if self.issues:
            critical_count = sum(1 for issue in self.issues if issue["severity"] == "CRITICAL")
            high_count = sum(1 for issue in self.issues if issue["severity"] == "HIGH")
            medium_count = sum(1 for issue in self.issues if issue["severity"] == "MEDIUM")

            print(f"\n❌ ISSUES FOUND: {len(self.issues)} total")
            print(f"   🔴 Critical: {critical_count}")
            print(f"   🟡 High: {high_count}")
            print(f"   🟠 Medium: {medium_count}")

            for issue in self.issues:
                self._print_issue(issue)
        else:
            print("\n✅ NO CRITICAL ISSUES FOUND!")

        # Recommendations Summary
        if self.recommendations:
            print(f"\n💡 OPTIMIZATION RECOMMENDATIONS: {len(self.recommendations)}")

            for rec in self.recommendations:
                self._print_recommendation(rec)

        # Action Plan
        self._generate_action_plan()

    def _print_issue(self, issue: dict[str, Any]) -> None:
        """Print formatted issue."""
        severity_icons = {"CRITICAL": "🔴", "HIGH": "🟡", "MEDIUM": "🟠", "LOW": "🔵"}

        icon = severity_icons.get(issue["severity"], "❓")
        print(f"\n{icon} {issue['title']} ({issue['severity']})")
        print(f"   📁 {issue.get('file', 'N/A')}")
        print(f"   📝 {issue['description']}")

        if "action" in issue:
            print(f"   🔧 Action: {issue['action']}")

        if "codes" in issue:
            codes_preview = issue["codes"][:5]
            more = f" (+{len(issue['codes']) - 5} more)" if len(issue["codes"]) > 5 else ""
            print(f"   📋 Codes: {codes_preview}{more}")

    def _print_recommendation(self, rec: dict[str, Any]) -> None:
        """Print formatted recommendation."""
        priority_icons = {"HIGH": "🔥", "MEDIUM": "📈", "LOW": "💭"}

        icon = priority_icons.get(rec["priority"], "💡")
        print(f"\n{icon} {rec['title']} (Priority: {rec['priority']})")
        print(f"   📁 {rec.get('file', 'N/A')}")
        print(f"   📝 {rec['description']}")

    def _generate_action_plan(self) -> None:
        """Generate prioritized action plan."""
        print("\n" + "=" * 60)
        print("🎯 PRIORITIZED ACTION PLAN")
        print("=" * 60)

        # Critical issues first
        critical_issues = [i for i in self.issues if i["severity"] == "CRITICAL"]
        high_priority_recs = [r for r in self.recommendations if r["priority"] == "HIGH"]

        step = 1

        if critical_issues:
            print(f"\n🔴 STEP {step}: Fix Critical Issues")
            for issue in critical_issues:
                print(f"   • {issue['title']}")
                if "action" in issue:
                    print(f"     → {issue['action']}")
            step += 1

        if high_priority_recs:
            print(f"\n🟡 STEP {step}: High Priority Optimizations")
            for rec in high_priority_recs:
                print(f"   • {rec['title']}")
            step += 1

        # Generate specific commands
        print(f"\n🔧 STEP {step}: Run Consistency Tools")
        print("   • uv run python tools/cross_project_guard.py")
        print("   • cd desktop_ai_zeta && npm run api:gen")
        print("   • cd desktop_ai_zeta && npm run typecheck")

        print("\n✅ SUCCESS CRITERIA:")
        print("   • Cross-project guard passes với 0 issues")
        print("   • Desktop TypeScript compiles without errors")
        print("   • All API endpoints có proper typing")
        print("   • Error codes fully synced giữa server và desktop")


def main():
    """Main entry point."""
    optimizer = APIConsistencyOptimizer()
    optimizer.analyze_all()


if __name__ == "__main__":
    main()
