#!/usr/bin/env python3
"""
tools/main_tsx_analyzer.py

Phân tích chi tiết file main.tsx - entry point của desktop_ai_zeta.
Kiểm tra architecture patterns, API integration, type safety, và consistency.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any
import any
import bool
import dict
import enumerate
import imp
import issue
import len
import line
import list
import max
import print
import r
import rec
import self
import str
import sum
import url

ROOT = Path(__file__).resolve().parents[1]
DESKTOP_ROOT = ROOT / "desktop_ai_zeta"
MAIN_FILE = DESKTOP_ROOT / "src" / "main.tsx"


class MainTsxAnalyzer:
    def __init__(self):
        self.issues: list[dict[str, Any]] = []
        self.recommendations: list[dict[str, Any]] = []
        self.analysis: dict[str, Any] = {}

    def analyze(self) -> None:
        """Phân tích toàn diện file main.tsx."""
        print("🔍 MAIN.TSX ANALYSIS - Desktop Entry Point")
        print("=" * 55)

        if not MAIN_FILE.exists():
            print("❌ main.tsx not found!")
            return

        content = MAIN_FILE.read_text(encoding="utf-8")

        # Core analysis
        self._analyze_imports(content)
        self._analyze_environment_config(content)
        self._analyze_api_integration(content)
        self._analyze_websocket_setup(content)
        self._analyze_routing_structure(content)
        self._analyze_context_providers(content)
        self._analyze_error_handling(content)
        self._analyze_type_safety(content)
        self._analyze_i18n_setup(content)
        self._analyze_performance_patterns(content)
        self._analyze_security_considerations(content)

        # Generate report
        self._generate_report()

    def _analyze_imports(self, content: str) -> None:
        """Phân tích import patterns và dependencies."""
        print("📦 Analyzing imports...")

        import_lines = [line.strip() for line in content.split("\n") if line.strip().startswith("import")]

        # Categorize imports
        react_imports = [imp for imp in import_lines if "react" in imp.lower()]
        mui_imports = [imp for imp in import_lines if "@mui" in imp]
        routing_imports = [imp for imp in import_lines if "react-router" in imp]
        internal_imports = [imp for imp in import_lines if imp.startswith("import") and ("@/" in imp or "./" in imp)]

        self.analysis["imports"] = {
            "total": len(import_lines),
            "react": len(react_imports),
            "mui": len(mui_imports),
            "routing": len(routing_imports),
            "internal": len(internal_imports),
            "lines": import_lines,
        }

        # Check for potential issues
        if len(import_lines) > 20:
            self.recommendations.append(
                {
                    "category": "IMPORTS",
                    "priority": "LOW",
                    "message": f"Many imports ({len(import_lines)}) - consider splitting into modules",
                }
            )

        # Check for alias consistency
        has_at_alias = any("@/" in imp for imp in internal_imports)
        has_relative = any(("./" in imp or "../" in imp) for imp in internal_imports)

        if has_at_alias and has_relative:
            self.issues.append(
                {
                    "category": "IMPORTS",
                    "severity": "MEDIUM",
                    "message": "Mixed import patterns: both @/ alias and relative imports",
                }
            )

    def _analyze_environment_config(self, content: str) -> None:
        """Phân tích environment configuration."""
        print("🌍 Analyzing environment config...")

        env_vars = re.findall(r"import\.meta.*?env.*?(\w+)", content)
        hardcoded_urls = re.findall(r'["\']https?://[^"\']+["\']', content)

        self.analysis["environment"] = {
            "env_vars": env_vars,
            "hardcoded_urls": hardcoded_urls,
            "uses_meta_env": "import.meta.env" in content,
            "has_fallbacks": "||" in content and "env" in content,
        }

        # Check for hardcoded values
        if hardcoded_urls:
            for url in hardcoded_urls:
                if "localhost" in url:
                    self.issues.append(
                        {
                            "category": "ENVIRONMENT",
                            "severity": "HIGH",
                            "message": f"Hardcoded localhost URL: {url}",
                            "recommendation": "Use environment variables",
                        }
                    )

    def _analyze_api_integration(self, content: str) -> None:
        """Phân tích API integration patterns."""
        print("🌐 Analyzing API integration...")

        api_patterns = {
            "base_url_config": "API_BASE_URL" in content,
            "dynamic_config": "DESKTOP_API_BASE_URL" in content,
            "context_provider": "ApiCfgCtx" in content,
            "query_client": "QueryClient" in content,
            "auth_integration": "AuthProvider" in content,
        }

        self.analysis["api_integration"] = api_patterns

        # Check API configuration quality
        if not api_patterns["base_url_config"]:
            self.issues.append(
                {
                    "category": "API_INTEGRATION",
                    "severity": "HIGH",
                    "message": "Missing API base URL configuration",
                }
            )

        if not api_patterns["query_client"]:
            self.recommendations.append(
                {
                    "category": "API_INTEGRATION",
                    "priority": "MEDIUM",
                    "message": "Consider adding React Query for API state management",
                }
            )

    def _analyze_websocket_setup(self, content: str) -> None:
        """Phân tích WebSocket implementation."""
        print("🔌 Analyzing WebSocket setup...")

        ws_features = {
            "auto_reconnect": "retry" in content.lower() and "websocket" in content.lower(),
            "backoff_strategy": "backoff" in content.lower(),
            "status_tracking": "status" in content and "connecting" in content,
            "token_auth": "token" in content and "websocket" in content.lower(),
            "error_handling": "onerror" in content.lower() or "onclose" in content.lower(),
        }

        self.analysis["websocket"] = ws_features

        # Check WebSocket quality
        if not ws_features["auto_reconnect"]:
            self.recommendations.append(
                {
                    "category": "WEBSOCKET",
                    "priority": "HIGH",
                    "message": "Add auto-reconnect functionality for WebSocket",
                }
            )

        if not ws_features["status_tracking"]:
            self.recommendations.append(
                {
                    "category": "WEBSOCKET",
                    "priority": "MEDIUM",
                    "message": "Add connection status tracking for better UX",
                }
            )

    def _analyze_routing_structure(self, content: str) -> None:
        """Phân tích routing configuration."""
        print("🛣️ Analyzing routing structure...")

        routing_features = {
            "has_router": "Router" in content,
            "electron_support": "HashRouter" in content,
            "web_support": "BrowserRouter" in content,
            "route_count": len(re.findall(r"<Route", content)),
            "has_fallback": "Navigate" in content and "*" in content,
            "suspense_wrapper": "Suspense" in content,
        }

        self.analysis["routing"] = routing_features

        # Check routing quality
        if not routing_features["has_fallback"]:
            self.recommendations.append(
                {
                    "category": "ROUTING",
                    "priority": "MEDIUM",
                    "message": "Add fallback route for unknown paths",
                }
            )

        if not routing_features["suspense_wrapper"]:
            self.recommendations.append(
                {
                    "category": "ROUTING",
                    "priority": "LOW",
                    "message": "Consider adding Suspense for lazy loading",
                }
            )

    def _analyze_context_providers(self, content: str) -> None:
        """Phân tích context providers hierarchy."""
        print("🏗️ Analyzing context providers...")

        providers = re.findall(r"(\w+Provider)", content)
        provider_hierarchy = []

        # Find nesting structure
        lines = content.split("\n")
        for i, line in enumerate(lines):
            if "Provider" in line and "<" in line:
                indent = len(line) - len(line.lstrip())
                provider_hierarchy.append((line.strip(), indent))

        self.analysis["context_providers"] = {
            "providers": providers,
            "hierarchy": provider_hierarchy,
            "count": len(providers),
        }

        # Check provider organization
        if len(providers) > 5:
            self.recommendations.append(
                {
                    "category": "CONTEXT",
                    "priority": "LOW",
                    "message": f"Many providers ({len(providers)}) - consider provider composition",
                }
            )

    def _analyze_error_handling(self, content: str) -> None:
        """Phân tích error handling patterns."""
        print("🛡️ Analyzing error handling...")

        error_features = {
            "error_boundary": "ErrorBoundary" in content,
            "try_catch_blocks": len(re.findall(r"try\s*{", content)),
            "error_state": "error" in content.lower() and "state" in content.lower(),
            "global_error_handler": "componentDidCatch" in content,
            "toast_errors": "snackbar" in content.lower() and "error" in content.lower(),
        }

        self.analysis["error_handling"] = error_features

        # Check error handling quality
        if not error_features["error_boundary"]:
            self.issues.append(
                {
                    "category": "ERROR_HANDLING",
                    "severity": "HIGH",
                    "message": "Missing global error boundary",
                }
            )

        if error_features["try_catch_blocks"] < 2:
            self.recommendations.append(
                {
                    "category": "ERROR_HANDLING",
                    "priority": "MEDIUM",
                    "message": "Add more try-catch blocks for async operations",
                }
            )

    def _analyze_type_safety(self, content: str) -> None:
        """Phân tích TypeScript type safety."""
        print("🛡️ Analyzing type safety...")

        type_features = {
            "any_usage": len(re.findall(r"\bany\b", content)),
            "interface_count": len(re.findall(r"interface\s+\w+", content)),
            "type_assertions": len(re.findall(r"as\s+\w+", content)),
            "strict_typing": "!" in content and "getElementById" in content,
            "generic_usage": len(re.findall(r"<[A-Z]\w*>", content)),
        }

        self.analysis["type_safety"] = type_features

        # Check type safety issues
        if type_features["any_usage"] > 5:
            self.issues.append(
                {
                    "category": "TYPE_SAFETY",
                    "severity": "MEDIUM",
                    "message": f"High 'any' usage: {type_features['any_usage']} occurrences",
                }
            )

        if type_features["type_assertions"] > 10:
            self.recommendations.append(
                {
                    "category": "TYPE_SAFETY",
                    "priority": "MEDIUM",
                    "message": f"Many type assertions ({type_features['type_assertions']}) - review type definitions",
                }
            )

    def _analyze_i18n_setup(self, content: str) -> None:
        """Phân tích internationalization setup."""
        print("🌍 Analyzing i18n setup...")

        # Determine default language
        default_lang = None
        if '"vi"' in content:
            default_lang = "vi"
        elif '"en"' in content:
            default_lang = "en"

        i18n_features = {
            "has_i18n": "i18next" in content,
            "inline_setup": "initReactI18next" in content,
            "default_language": default_lang,
            "language_resources": "resources" in content and "translation" in content,
            "translation_usage": "useTranslation" in content,
        }

        self.analysis["i18n"] = i18n_features

        # Check i18n quality
        if i18n_features["inline_setup"]:
            self.recommendations.append(
                {
                    "category": "I18N",
                    "priority": "MEDIUM",
                    "message": "Consider moving i18n setup to separate file for maintainability",
                }
            )

        if not i18n_features["translation_usage"]:
            self.recommendations.append(
                {
                    "category": "I18N",
                    "priority": "LOW",
                    "message": "Add translation usage in components",
                }
            )

    def _analyze_performance_patterns(self, content: str) -> None:
        """Phân tích performance optimization patterns."""
        print("⚡ Analyzing performance patterns...")

        perf_features = {
            "memo_usage": "useMemo" in content,
            "callback_usage": "useCallback" in content,
            "lazy_loading": "lazy" in content,
            "suspense_usage": "Suspense" in content,
            "strict_mode": "StrictMode" in content,
        }

        self.analysis["performance"] = perf_features

        # Performance recommendations
        if not perf_features["memo_usage"] and "useState" in content:
            self.recommendations.append(
                {
                    "category": "PERFORMANCE",
                    "priority": "LOW",
                    "message": "Consider using useMemo for expensive computations",
                }
            )

    def _analyze_security_considerations(self, content: str) -> None:
        """Phân tích security considerations."""
        print("🔒 Analyzing security...")

        security_features = {
            "token_handling": "token" in content.lower(),
            "url_validation": "URL" in content and "new URL" in content,
            "electron_security": "electron" in content.lower() and "ipcRenderer" in content,
            "xss_protection": "dangerouslySetInnerHTML" not in content,
            "csp_ready": not bool(re.search(r"eval\(", content)),
        }

        self.analysis["security"] = security_features

        # Security checks
        if "ast.literal_ast.literal_ast.literal_ast.literal_ast.literal_ast.literal_ast.literal_eval(" in content:
            self.issues.append(
                {
                    "category": "SECURITY",
                    "severity": "HIGH",
                    "message": "Found ast.literal_ast.literal_ast.literal_ast.literal_ast.literal_ast.literal_ast.literal_eval() usage - potential security risk",
                }
            )

    def _generate_report(self) -> None:
        """Generate comprehensive analysis report."""
        print("\n" + "=" * 60)
        print("📊 MAIN.TSX ANALYSIS REPORT")
        print("=" * 60)

        # File stats
        lines = len(MAIN_FILE.read_text(encoding="utf-8").splitlines())
        print("\n📈 FILE STATISTICS:")
        print(f"   Lines of Code: {lines}")
        print(f"   Total Imports: {self.analysis.get('imports', {}).get('total', 0)}")
        print(f"   Context Providers: {self.analysis.get('context_providers', {}).get('count', 0)}")

        # Issues summary
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

        # Recommendations
        if self.recommendations:
            print(f"\n💡 RECOMMENDATIONS: {len(self.recommendations)}")
            for rec in self.recommendations[:5]:  # Show first 5
                self._print_recommendation(rec)

            if len(self.recommendations) > 5:
                print(f"   ... and {len(self.recommendations) - 5} more recommendations")

        # Feature analysis
        self._print_feature_analysis()

        # Final assessment
        self._print_final_assessment()

    def _print_issue(self, issue: dict[str, Any]) -> None:
        """Print formatted issue."""
        severity_icons = {"CRITICAL": "🔴", "HIGH": "🟡", "MEDIUM": "🟠", "LOW": "🔵"}
        icon = severity_icons.get(issue["severity"], "❓")

        print(f"\n{icon} {issue['message']}")
        if "recommendation" in issue:
            print(f"   💡 {issue['recommendation']}")

    def _print_recommendation(self, rec: dict[str, Any]) -> None:
        """Print formatted recommendation."""
        priority_icons = {"HIGH": "🔥", "MEDIUM": "📈", "LOW": "💭"}
        icon = priority_icons.get(rec["priority"], "💡")

        print(f"\n{icon} {rec['message']}")

    def _print_feature_analysis(self) -> None:
        """Print feature-by-feature analysis."""
        print("\n🎯 FEATURE ANALYSIS:")

        # API Integration
        api_features = self.analysis.get("api_integration", {})
        api_score = sum(api_features.values()) / len(api_features) * 100 if api_features else 0
        print(f"   🌐 API Integration: {api_score:.0f}% complete")

        # WebSocket
        ws_features = self.analysis.get("websocket", {})
        ws_score = sum(ws_features.values()) / len(ws_features) * 100 if ws_features else 0
        print(f"   🔌 WebSocket Setup: {ws_score:.0f}% complete")

        # Error Handling
        error_features = self.analysis.get("error_handling", {})
        error_score = sum(error_features.values()) / len(error_features) * 100 if error_features else 0
        print(f"   🛡️ Error Handling: {error_score:.0f}% complete")

        # Type Safety
        type_features = self.analysis.get("type_safety", {})
        # Calculate score (lower any_usage is better)
        type_score = max(0, 100 - type_features.get("any_usage", 0) * 5)
        print(f"   🛡️ Type Safety: {type_score:.0f}% score")

    def _print_final_assessment(self) -> None:
        """Print final assessment và recommendations."""
        print("\n🎉 FINAL ASSESSMENT:")

        critical_issues = sum(1 for issue in self.issues if issue["severity"] in ["CRITICAL", "HIGH"])

        if critical_issues == 0:
            print("   ✅ PRODUCTION READY - No critical issues found")
        elif critical_issues <= 2:
            print("   🟡 GOOD - Few issues to address before production")
        else:
            print("   🔴 NEEDS WORK - Multiple critical issues to fix")

        # Priority actions
        high_priority_recs = [r for r in self.recommendations if r["priority"] == "HIGH"]
        if high_priority_recs:
            print("\n🔥 PRIORITY ACTIONS:")
            for rec in high_priority_recs[:3]:
                print(f"   • {rec['message']}")


def main():
    """Main entry point."""
    analyzer = MainTsxAnalyzer()
    analyzer.analyze()


if __name__ == "__main__":
    main()
