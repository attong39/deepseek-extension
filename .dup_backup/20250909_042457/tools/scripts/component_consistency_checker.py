#!/usr/bin/env python3
"""
tools/component_consistency_checker.py

Kiểm tra tính nhất quán của React components trong desktop_ai_zeta.
Phân tích patterns, imports, API usage, type safety, và architecture consistency.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any
import Exception
import any
import c
import call
import comp
import comp_file
import count
import dict
import e
import exp
import file_path
import hook
import imp
import int
import issue
import len
import lines
import list
import method
import name
import print
import rec
import s
import self
import set
import sorted
import str
import sum
import url
import x

ROOT = Path(__file__).resolve().parents[1]
DESKTOP_ROOT = ROOT / "desktop_ai_zeta"
COMPONENTS_DIR = DESKTOP_ROOT / "src" / "components"


class ComponentConsistencyChecker:
    def __init__(self):
        self.issues: list[dict[str, Any]] = []
        self.recommendations: list[dict[str, Any]] = []
        self.component_analysis: dict[str, dict[str, Any]] = {}

    def analyze_all(self) -> None:
        """Phân tích tất cả components."""
        print("🔍 DESKTOP COMPONENTS CONSISTENCY CHECK")
        print("=" * 50)

        if not COMPONENTS_DIR.exists():
            print("❌ Components directory not found!")
            return

        # Get all component files
        component_files = list(COMPONENTS_DIR.glob("*.tsx")) + list(COMPONENTS_DIR.glob("*.ts"))

        print(f"📂 Found {len(component_files)} component files")

        # Analyze each component
        for comp_file in component_files:
            self._analyze_component(comp_file)

        # Cross-component analysis
        self._analyze_patterns()
        self._analyze_api_usage()
        self._analyze_type_safety()
        self._analyze_imports()
        self._analyze_architecture_consistency()

        # Generate report
        self._generate_report()

    def _analyze_component(self, file_path: Path) -> None:
        """Phân tích một component file."""
        file_name = file_path.name
        print(f"🔎 Analyzing {file_name}...")

        try:
            content = file_path.read_text(encoding="utf-8")
        except Exception as e:
            self.issues.append(
                {
                    "category": "FILE_READ",
                    "severity": "HIGH",
                    "file": file_name,
                    "message": f"Cannot read file: {e}",
                }
            )
            return

        analysis = {
            "file_path": str(file_path),
            "content": content,
            "lines": len(content.splitlines()),
            "imports": self._extract_imports(content),
            "exports": self._extract_exports(content),
            "hooks_used": self._extract_hooks(content),
            "api_calls": self._extract_api_calls(content),
            "hardcoded_urls": self._find_hardcoded_urls(content),
            "type_annotations": self._check_type_annotations(content),
            "error_handling": self._check_error_handling(content),
            "i18n_usage": self._check_i18n_usage(content),
            "mui_components": self._extract_mui_components(content),
            "state_management": self._analyze_state_management(content),
            "event_handlers": self._extract_event_handlers(content),
        }

        self.component_analysis[file_name] = analysis

        # Individual component checks
        self._check_component_issues(file_name, analysis)

    def _extract_imports(self, content: str) -> list[str]:
        """Extract import statements."""
        imports = []
        import_pattern = r'import\s+.*?from\s+["\']([^"\']+)["\']'
        imports.extend(re.findall(import_pattern, content))

        # Also check dynamic imports
        dynamic_pattern = r'import\(["\']([^"\']+)["\']\)'
        imports.extend(re.findall(dynamic_pattern, content))

        return imports

    def _extract_exports(self, content: str) -> list[str]:
        """Extract export statements."""
        exports = []

        # Default exports
        default_exports = re.findall(r"export\s+default\s+(\w+)", content)
        exports.extend(default_exports)

        # Named exports
        named_exports = re.findall(r"export\s+(?:function|const|class)\s+(\w+)", content)
        exports.extend(named_exports)

        # Export destructuring
        export_destructure = re.findall(r"export\s+\{([^}]+)\}", content)
        for exp in export_destructure:
            names = [name.strip() for name in exp.split(",")]
            exports.extend(names)

        return exports

    def _extract_hooks(self, content: str) -> list[str]:
        """Extract React hooks usage."""
        hooks = []

        # React built-in hooks
        react_hooks = [
            "useState",
            "useEffect",
            "useContext",
            "useReducer",
            "useCallback",
            "useMemo",
            "useRef",
            "useImperativeHandle",
            "useLayoutEffect",
            "useDebugValue",
        ]

        for hook in react_hooks:
            if f"{hook}(" in content:
                hooks.append(hook)

        # Custom hooks (use*)
        custom_hooks = re.findall(r"\b(use[A-Z]\w*)\(", content)
        hooks.extend(custom_hooks)

        return list(set(hooks))

    def _extract_api_calls(self, content: str) -> list[dict[str, str]]:
        """Extract API calls and check if they use proper clients."""
        api_calls = []

        # Direct fetch calls
        fetch_calls = re.findall(r'fetch\(["\']([^"\']+)["\']', content)
        for url in fetch_calls:
            api_calls.append({"type": "fetch", "url": url, "method": "direct"})

        # Axios calls
        axios_calls = re.findall(r'axios\.(\w+)\(["\']([^"\']+)["\']', content)
        for method, url in axios_calls:
            api_calls.append({"type": "axios", "url": url, "method": method})

        # API client calls
        api_client_calls = re.findall(r"apiClient\.(\w+)\(", content)
        for method in api_client_calls:
            api_calls.append({"type": "apiClient", "method": method})

        return api_calls

    def _find_hardcoded_urls(self, content: str) -> list[str]:
        """Find hardcoded URLs."""
        urls = []

        # HTTP URLs
        http_urls = re.findall(r'["\']https?://[^"\']+["\']', content)
        urls.extend(http_urls)

        # Localhost URLs
        localhost_urls = re.findall(r'["\']http://localhost:\d+[^"\']*["\']', content)
        urls.extend(localhost_urls)

        return urls

    def _check_type_annotations(self, content: str) -> dict[str, Any]:
        """Check TypeScript type usage."""
        type_info = {
            "has_types": False,
            "any_usage": 0,
            "interface_count": 0,
            "type_alias_count": 0,
            "prop_types": False,
        }

        # Check for type annotations
        if ": " in content and ("string" in content or "number" in content or "boolean" in content):
            type_info["has_types"] = True

        # Count 'any' usage
        type_info["any_usage"] = len(re.findall(r"\bany\b", content))

        # Count interfaces
        type_info["interface_count"] = len(re.findall(r"interface\s+\w+", content))

        # Count type aliases
        type_info["type_alias_count"] = len(re.findall(r"type\s+\w+\s*=", content))

        # Check for Props type
        if re.search(r"type\s+Props\s*=|interface\s+Props", content):
            type_info["prop_types"] = True

        return type_info

    def _check_error_handling(self, content: str) -> dict[str, Any]:
        """Check error handling patterns."""
        error_handling = {
            "has_try_catch": "try {" in content and "catch" in content,
            "has_error_state": "error" in content.lower() and "useState" in content,
            "has_error_boundaries": "ErrorBoundary" in content,
            "has_loading_state": "loading" in content.lower() and "useState" in content,
        }

        return error_handling

    def _check_i18n_usage(self, content: str) -> dict[str, Any]:
        """Check internationalization usage."""
        i18n_info = {
            "uses_translation": "useTranslation" in content,
            "has_t_function": "t(" in content,
            "hardcoded_strings": self._count_hardcoded_strings(content),
        }

        return i18n_info

    def _count_hardcoded_strings(self, content: str) -> int:
        """Count potential hardcoded user-facing strings."""
        # Simple heuristic: strings in JSX that look like UI text
        jsx_strings = re.findall(r">[^<{]*[a-zA-Z][^<{]*<", content)
        ui_strings = [s for s in jsx_strings if len(s.strip()) > 3 and any(c.isalpha() for c in s)]
        return len(ui_strings)

    def _extract_mui_components(self, content: str) -> list[str]:
        """Extract Material-UI components used."""
        mui_components = []

        # Check imports from @mui/material
        mui_import_match = re.search(r'import\s*\{([^}]+)\}\s*from\s*["\']@mui/material["\']', content)
        if mui_import_match:
            components = [comp.strip() for comp in mui_import_match.group(1).split(",")]
            mui_components.extend(components)

        return mui_components

    def _analyze_state_management(self, content: str) -> dict[str, Any]:
        """Analyze state management patterns."""
        state_info = {
            "useState_count": len(re.findall(r"useState\(", content)),
            "useEffect_count": len(re.findall(r"useEffect\(", content)),
            "useContext_used": "useContext" in content,
            "local_storage_used": "localStorage" in content,
            "session_storage_used": "sessionStorage" in content,
        }

        return state_info

    def _extract_event_handlers(self, content: str) -> list[str]:
        """Extract event handler patterns."""
        handlers = []

        # onClick, onChange, etc.
        event_handlers = re.findall(r"on[A-Z]\w*=", content)
        handlers.extend(event_handlers)

        # Event handler functions
        handler_functions = re.findall(r"const\s+(handle\w*|on\w*)\s*=", content)
        handlers.extend(handler_functions)

        return handlers

    def _check_component_issues(self, file_name: str, analysis: dict[str, Any]) -> None:
        """Check individual component for issues."""

        # Check hardcoded URLs
        if analysis["hardcoded_urls"]:
            self.issues.append(
                {
                    "category": "HARDCODED_URLS",
                    "severity": "HIGH",
                    "file": file_name,
                    "message": f"Found {len(analysis['hardcoded_urls'])} hardcoded URLs",
                    "urls": analysis["hardcoded_urls"],
                }
            )

        # Check direct API calls without proper client
        direct_api_calls = [call for call in analysis["api_calls"] if call["type"] == "fetch"]
        if direct_api_calls:
            self.issues.append(
                {
                    "category": "API_USAGE",
                    "severity": "MEDIUM",
                    "file": file_name,
                    "message": "Using direct fetch() instead of apiClient",
                    "calls": direct_api_calls,
                }
            )

        # Check type safety
        if analysis["type_annotations"]["any_usage"] > 2:
            self.issues.append(
                {
                    "category": "TYPE_SAFETY",
                    "severity": "MEDIUM",
                    "file": file_name,
                    "message": f"Excessive 'any' usage: {analysis['type_annotations']['any_usage']}",
                }
            )

        # Check error handling
        if not analysis["error_handling"]["has_try_catch"] and analysis["api_calls"]:
            self.recommendations.append(
                {
                    "category": "ERROR_HANDLING",
                    "priority": "MEDIUM",
                    "file": file_name,
                    "message": "Consider adding try-catch for API calls",
                }
            )

        # Check i18n usage
        if analysis["i18n_usage"]["hardcoded_strings"] > 5 and not analysis["i18n_usage"]["uses_translation"]:
            self.recommendations.append(
                {
                    "category": "I18N",
                    "priority": "LOW",
                    "file": file_name,
                    "message": f"Consider using i18n for {analysis['i18n_usage']['hardcoded_strings']} hardcoded strings",
                }
            )

    def _analyze_patterns(self) -> None:
        """Analyze patterns across components."""
        print("\n🔍 Analyzing patterns across components...")

        # Check import consistency
        all_imports = {}
        for comp, analysis in self.component_analysis.items():
            for imp in analysis["imports"]:
                if imp not in all_imports:
                    all_imports[imp] = []
                all_imports[imp].append(comp)

        # Find inconsistent import patterns
        mui_imports = [imp for imp in all_imports if "@mui" in imp]
        if len(set(mui_imports)) > 1:
            self.recommendations.append(
                {
                    "category": "IMPORT_CONSISTENCY",
                    "priority": "LOW",
                    "message": f"Multiple MUI import patterns found: {set(mui_imports)}",
                }
            )

    def _analyze_api_usage(self) -> None:
        """Analyze API usage patterns."""
        print("🌐 Analyzing API usage patterns...")

        components_with_hardcoded_urls = []
        components_with_direct_fetch = []

        for comp, analysis in self.component_analysis.items():
            if analysis["hardcoded_urls"]:
                components_with_hardcoded_urls.append(comp)

            direct_calls = [call for call in analysis["api_calls"] if call["type"] == "fetch"]
            if direct_calls:
                components_with_direct_fetch.append(comp)

        if components_with_hardcoded_urls:
            self.issues.append(
                {
                    "category": "API_ARCHITECTURE",
                    "severity": "HIGH",
                    "message": f"Components with hardcoded URLs: {components_with_hardcoded_urls}",
                    "recommendation": "Use environment variables and API client",
                }
            )

        if components_with_direct_fetch:
            self.issues.append(
                {
                    "category": "API_ARCHITECTURE",
                    "severity": "MEDIUM",
                    "message": f"Components using direct fetch: {components_with_direct_fetch}",
                    "recommendation": "Use centralized API client",
                }
            )

    def _analyze_type_safety(self) -> None:
        """Analyze TypeScript type safety."""
        print("🛡️ Analyzing type safety...")

        total_any_usage = sum(
            analysis["type_annotations"]["any_usage"] for analysis in self.component_analysis.values()
        )

        components_without_props_types = []
        for comp, analysis in self.component_analysis.items():
            if comp.endswith(".tsx") and not analysis["type_annotations"]["prop_types"]:
                # Check if it's a component (has JSX)
                if "return (" in analysis["content"] or "return <" in analysis["content"]:
                    components_without_props_types.append(comp)

        if total_any_usage > 10:
            self.issues.append(
                {
                    "category": "TYPE_SAFETY",
                    "severity": "MEDIUM",
                    "message": f"High 'any' usage across components: {total_any_usage} occurrences",
                }
            )

        if components_without_props_types:
            self.recommendations.append(
                {
                    "category": "TYPE_SAFETY",
                    "priority": "MEDIUM",
                    "message": f"Components without Props types: {components_without_props_types}",
                }
            )

    def _analyze_imports(self) -> None:
        """Analyze import patterns."""
        print("📦 Analyzing import patterns...")

        # Check for relative vs absolute imports
        relative_imports = []
        absolute_imports = []

        for comp, analysis in self.component_analysis.items():
            for imp in analysis["imports"]:
                if imp.startswith("./") or imp.startswith("../"):
                    relative_imports.append((comp, imp))
                elif imp.startswith("@/") or imp.startswith("~/"):
                    absolute_imports.append((comp, imp))

        # Check consistency
        if relative_imports and absolute_imports:
            self.recommendations.append(
                {
                    "category": "IMPORT_CONSISTENCY",
                    "priority": "LOW",
                    "message": "Mixed relative and absolute imports found",
                    "details": {
                        "relative_count": len(relative_imports),
                        "absolute_count": len(absolute_imports),
                    },
                }
            )

    def _analyze_architecture_consistency(self) -> None:
        """Analyze architecture consistency."""
        print("🏗️ Analyzing architecture consistency...")

        # Check service usage patterns
        service_imports = {}
        for comp, analysis in self.component_analysis.items():
            services = [imp for imp in analysis["imports"] if "services" in imp]
            service_imports[comp] = services

        # Check if components directly import from services (good)
        # vs importing from other components (potentially bad)
        component_to_component_imports = []
        for comp, analysis in self.component_analysis.items():
            comp_imports = [imp for imp in analysis["imports"] if "components" in imp and imp != "./index"]
            if comp_imports:
                component_to_component_imports.append((comp, comp_imports))

        if component_to_component_imports:
            self.recommendations.append(
                {
                    "category": "ARCHITECTURE",
                    "priority": "MEDIUM",
                    "message": "Consider avoiding direct component-to-component imports",
                    "details": component_to_component_imports[:3],  # Show first 3
                }
            )

    def _generate_report(self) -> None:
        """Generate comprehensive report."""
        print("\n" + "=" * 60)
        print("📊 COMPONENT CONSISTENCY REPORT")
        print("=" * 60)

        # Summary stats
        total_components = len(self.component_analysis)
        total_lines = sum(analysis["lines"] for analysis in self.component_analysis.values())

        print("\n📈 SUMMARY:")
        print(f"   Total Components: {total_components}")
        print(f"   Total Lines: {total_lines:,}")
        print(f"   Average Lines per Component: {total_lines // total_components if total_components > 0 else 0}")

        # Issues
        if self.issues:
            critical_count = sum(1 for issue in self.issues if issue["severity"] == "CRITICAL")
            high_count = sum(1 for issue in self.issues if issue["severity"] == "HIGH")
            medium_count = sum(1 for issue in self.issues if issue["severity"] == "MEDIUM")

            print(f"\n❌ ISSUES FOUND: {len(self.issues)} total")
            print(f"   🔴 Critical: {critical_count}")
            print(f"   🟡 High: {high_count}")
            print(f"   🟠 Medium: {medium_count}")

            for issue in self.issues[:5]:  # Show first 5
                self._print_issue(issue)

            if len(self.issues) > 5:
                print(f"   ... and {len(self.issues) - 5} more issues")
        else:
            print("\n✅ NO CRITICAL ISSUES FOUND!")

        # Recommendations
        if self.recommendations:
            print(f"\n💡 RECOMMENDATIONS: {len(self.recommendations)}")
            for rec in self.recommendations[:5]:  # Show first 5
                self._print_recommendation(rec)

            if len(self.recommendations) > 5:
                print(f"   ... and {len(self.recommendations) - 5} more recommendations")

        # Top insights
        self._print_top_insights()

    def _print_issue(self, issue: dict[str, Any]) -> None:
        """Print formatted issue."""
        severity_icons = {"CRITICAL": "🔴", "HIGH": "🟡", "MEDIUM": "🟠", "LOW": "🔵"}
        icon = severity_icons.get(issue["severity"], "❓")

        print(f"\n{icon} {issue.get('file', 'N/A')} - {issue['message']}")
        if "recommendation" in issue:
            print(f"   💡 {issue['recommendation']}")

    def _print_recommendation(self, rec: dict[str, Any]) -> None:
        """Print formatted recommendation."""
        priority_icons = {"HIGH": "🔥", "MEDIUM": "📈", "LOW": "💭"}
        icon = priority_icons.get(rec["priority"], "💡")

        print(f"\n{icon} {rec.get('file', 'General')} - {rec['message']}")

    def _print_top_insights(self) -> None:
        """Print top insights from analysis."""
        print("\n🎯 TOP INSIGHTS:")

        # Most complex components
        complex_components = sorted(
            [(comp, analysis["lines"]) for comp, analysis in self.component_analysis.items()],
            key=lambda x: x[1],
            reverse=True,
        )[:3]

        print("   📏 Largest Components:")
        for comp, lines in complex_components:
            print(f"      • {comp}: {lines} lines")

        # Hook usage patterns
        hook_usage = {}
        for analysis in self.component_analysis.values():
            for hook in analysis["hooks_used"]:
                hook_usage[hook] = hook_usage.get(hook, 0) + 1

        popular_hooks = sorted(hook_usage.items(), key=lambda x: x[1], reverse=True)[:5]
        print("   🪝 Most Used Hooks:")
        for hook, count in popular_hooks:
            print(f"      • {hook}: {count} components")


def main():
    """Main entry point."""
    checker = ComponentConsistencyChecker()
    checker.analyze_all()


if __name__ == "__main__":
    main()
