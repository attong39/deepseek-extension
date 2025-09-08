#!/usr/bin/env python
"""
Script kiểm tra đồng bộ API schema giữa server và desktop client.

Verify rằng desktop app có schema tương thích với server API.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any
import Exception
import any
import bool
import cmd
import data
import dict
import e
import enumerate
import f
import file_path
import i
import key
import keyword
import len
import line
import list
import mismatch
import open
import print
import py_file
import rec
import self
import str
import try_codegen
import ts_file


class ClientAPIVerifier:
    """Kiểm tra tính nhất quán API giữa server và client"""

    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.server_api_dir = repo_root / "zeta_vn" / "app" / "api"
        self.desktop_dir = repo_root / "desktop_ai_zeta"
        self.results: dict[str, Any] = {
            "server_endpoints": {},
            "client_schemas": {},
            "mismatches": [],
            "recommendations": [],
        }

    def scan_server_endpoints(self) -> None:
        """Scan các endpoint trong server API"""
        print("🔍 Scanning server API endpoints...")

        v1_dir = self.server_api_dir / "v1"
        if not v1_dir.exists():
            print("⚠️  Server API v1 directory not found")
            return

        endpoints = {}
        for py_file in v1_dir.rglob("*.py"):
            if py_file.name != "__init__.py":
                try:
                    content = py_file.read_text(encoding="utf-8")
                    # Extract routes (simplified - tìm @router. và @app.)
                    routes = self._extract_routes(content)
                    if routes:
                        rel_path = str(py_file.relative_to(self.server_api_dir))
                        endpoints[rel_path] = {
                            "file": rel_path,
                            "routes": routes,
                            "hash": self._calculate_content_hash(content),
                        }
                except Exception as e:
                    print(f"⚠️  Error reading {py_file}: {e}")

        self.results["server_endpoints"] = endpoints
        print(f"✅ Found {len(endpoints)} endpoint files")

    def _extract_routes(self, content: str) -> list[dict[str, str]]:
        """Extract route definitions từ Python code"""
        routes = []
        lines = content.split("\n")

        for i, line in enumerate(lines):
            stripped = line.strip()
            # Tìm decorator @router.get, @router.post, etc.
            if stripped.startswith("@") and ("router." in stripped or "app." in stripped):
                # Extract method và path
                if "(" in stripped and ")" in stripped:
                    method_part = stripped.split("(")[0].replace("@", "").replace("router.", "").replace("app.", "")
                    path_part = stripped.split("(")[1].split(")")[0].strip("'\"")

                    # Tìm function name ở dòng tiếp theo
                    func_name = ""
                    if i + 1 < len(lines):
                        next_line = lines[i + 1].strip()
                        if next_line.startswith("def "):
                            func_name = next_line.split("(")[0].replace("def ", "")

                    routes.append({"method": method_part.upper(), "path": path_part, "function": func_name})

        return routes

    def _calculate_content_hash(self, content: str) -> str:
        """Tính hash của nội dung file"""
        return hashlib.md5(content.encode("utf-8")).hexdigest()[:8]

    def scan_client_schemas(self) -> None:
        """Scan client API schemas trong desktop app"""
        print("🔍 Scanning client API schemas...")

        # Tìm generated API files
        api_dir = self.desktop_dir / "src" / "api"
        generated_dir = api_dir / "generated"

        schemas = {}

        if generated_dir.exists():
            for ts_file in generated_dir.rglob("*.ts"):
                try:
                    content = ts_file.read_text(encoding="utf-8")
                    rel_path = str(ts_file.relative_to(self.desktop_dir))

                    # Extract exported interfaces/types
                    exports = self._extract_ts_exports(content)

                    schemas[rel_path] = {
                        "file": rel_path,
                        "exports": exports,
                        "hash": self._calculate_content_hash(content),
                        "size": len(content),
                    }
                except Exception as e:
                    print(f"⚠️  Error reading {ts_file}: {e}")

        # Scan manual API service files
        if api_dir.exists():
            for ts_file in api_dir.rglob("*.ts"):
                if "generated" not in str(ts_file):
                    try:
                        content = ts_file.read_text(encoding="utf-8")
                        rel_path = str(ts_file.relative_to(self.desktop_dir))

                        # Check if có API calls
                        if self._has_api_calls(content):
                            schemas[rel_path] = {
                                "file": rel_path,
                                "api_calls": self._extract_api_calls(content),
                                "hash": self._calculate_content_hash(content),
                                "type": "service",
                            }
                    except Exception as e:
                        print(f"⚠️  Error reading {ts_file}: {e}")

        self.results["client_schemas"] = schemas
        print(f"✅ Found {len(schemas)} client schema files")

    def _extract_ts_exports(self, content: str) -> list[str]:
        """Extract exported interfaces và types từ TypeScript"""
        exports = []
        lines = content.split("\n")

        for line in lines:
            stripped = line.strip()
            if stripped.startswith("export"):
                if "interface " in stripped or "type " in stripped or "const " in stripped:
                    # Extract name
                    if "interface " in stripped:
                        name = stripped.split("interface ")[1].split(" ")[0].split("{")[0]
                        exports.append(f"interface {name}")
                    elif "type " in stripped:
                        name = stripped.split("type ")[1].split(" ")[0].split("=")[0]
                        exports.append(f"type {name}")
                    elif "const " in stripped:
                        name = stripped.split("const ")[1].split(" ")[0].split(":")[0]
                        exports.append(f"const {name}")

        return exports

    def _has_api_calls(self, content: str) -> bool:
        """Kiểm tra file có chứa API calls không"""
        api_keywords = ["fetch(", "axios.", "api.", "/api/", "endpoint"]
        return any(keyword in content for keyword in api_keywords)

    def _extract_api_calls(self, content: str) -> list[str]:
        """Extract API calls từ TypeScript service files"""
        calls = []
        lines = content.split("\n")

        for line in lines:
            stripped = line.strip()
            if "/api/" in stripped or "endpoint" in stripped:
                calls.append(stripped[:100])  # Limit length

        return calls

    def check_package_json_scripts(self) -> None:
        """Kiểm tra scripts trong package.json"""
        print("🔍 Checking package.json scripts...")

        package_json = self.desktop_dir / "package.json"
        if not package_json.exists():
            self.results["recommendations"].append("❌ package.json not found in desktop app")
            return

        try:
            with open(package_json, encoding="utf-8") as f:
                package_data = json.load(f)

            scripts = package_data.get("scripts", {})

            # Check for API generation scripts
            api_scripts = [key for key in scripts if "api" in key.lower() or "codegen" in key.lower()]

            if api_scripts:
                print(f"✅ Found API scripts: {', '.join(api_scripts)}")
                self.results["client_schemas"]["package_scripts"] = api_scripts
            else:
                self.results["recommendations"].append("⚠️  No API generation scripts found in package.json")

        except Exception as e:
            self.results["recommendations"].append(f"❌ Error reading package.json: {e}")

    def run_desktop_codegen(self) -> bool:
        """Thử chạy desktop API codegen"""
        print("🚀 Attempting to run desktop API codegen...")

        try:
            # Check if npm installed
            result = subprocess.run(
                ["npm", "--version"],
                check=False,
                cwd=self.desktop_dir,
                capture_output=True,
                text=True,
                timeout=10,
            )

            if result.returncode != 0:
                self.results["recommendations"].append("❌ npm not available")
                return False

            # Try to run codegen script
            codegen_commands = ["npm run codegen:api", "npm run api:gen", "npm run generate:api"]

            for cmd in codegen_commands:
                try:
                    result = subprocess.run(
                        cmd.split(),
                        check=False,
                        cwd=self.desktop_dir,
                        capture_output=True,
                        text=True,
                        timeout=30,
                    )

                    if result.returncode == 0:
                        print(f"✅ Successfully ran: {cmd}")
                        return True
                    else:
                        print(f"⚠️  Failed: {cmd} - {result.stderr[:100]}")

                except subprocess.TimeoutExpired:
                    print(f"⏰ Timeout: {cmd}")
                except Exception as e:
                    print(f"❌ Error: {cmd} - {e}")

            self.results["recommendations"].append("⚠️  No working codegen script found")
            return False

        except Exception as e:
            self.results["recommendations"].append(f"❌ Error running codegen: {e}")
            return False

    def analyze_compatibility(self) -> None:
        """Phân tích compatibility giữa server và client"""
        print("🔗 Analyzing server-client compatibility...")

        server_endpoints = self.results["server_endpoints"]
        client_schemas = self.results["client_schemas"]

        # Check if có generated files
        generated_files = [f for f in client_schemas if "generated" in f]

        if not generated_files:
            self.results["mismatches"].append(
                {
                    "type": "missing_generated",
                    "message": "No generated API files found in client",
                    "recommendation": "Run API codegen to generate TypeScript schemas",
                }
            )

        # Check for old/stale generated files
        if generated_files:
            for file_path in generated_files:
                file_data = client_schemas[file_path]
                # Simple check - nếu file nhỏ có thể là outdated
                if file_data.get("size", 0) < 100:
                    self.results["mismatches"].append(
                        {
                            "type": "suspicious_file",
                            "file": file_path,
                            "message": f"Generated file {file_path} seems too small",
                            "recommendation": "Re-run API codegen",
                        }
                    )

        # Summary
        print(f"📊 Server endpoints: {len(server_endpoints)}")
        print(f"📊 Client schema files: {len(client_schemas)}")
        print(f"📊 Potential issues: {len(self.results['mismatches'])}")

    def print_results(self) -> None:
        """In kết quả ra console"""
        print("\n" + "=" * 60)
        print("🔗 CLIENT-SERVER API COMPATIBILITY CHECK")
        print("=" * 60)

        # Server summary
        print(f"🖥️  Server API endpoints: {len(self.results['server_endpoints'])}")
        if self.results["server_endpoints"]:
            print("   Server endpoint files:")
            for file_path, data in self.results["server_endpoints"].items():
                print(f"     📄 {file_path} ({len(data['routes'])} routes)")

        print()

        # Client summary
        print(f"💻 Client schema files: {len(self.results['client_schemas'])}")
        if self.results["client_schemas"]:
            print("   Client schema files:")
            for file_path, data in self.results["client_schemas"].items():
                file_type = data.get("type", "schema")
                print(f"     📄 {file_path} ({file_type})")

        print()

        # Issues
        if self.results["mismatches"]:
            print("⚠️  COMPATIBILITY ISSUES:")
            for mismatch in self.results["mismatches"]:
                print(f"   🔸 {mismatch['message']}")
                print(f"      💡 {mismatch['recommendation']}")
        else:
            print("✅ No obvious compatibility issues detected")

        print()

        # Recommendations
        if self.results["recommendations"]:
            print("💡 RECOMMENDATIONS:")
            for rec in self.results["recommendations"]:
                print(f"   {rec}")

    def save_results(self, output_file: Path) -> None:
        """Lưu kết quả vào file JSON"""
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        print(f"💾 Results saved to: {output_file}")

    def run_verification(self, try_codegen: bool = True, output_file: Path | None = None) -> None:
        """Chạy toàn bộ quá trình verification"""
        self.scan_server_endpoints()
        self.scan_client_schemas()
        self.check_package_json_scripts()

        if try_codegen:
            self.run_desktop_codegen()
            # Re-scan sau khi codegen
            self.scan_client_schemas()

        self.analyze_compatibility()
        self.print_results()

        if output_file:
            self.save_results(output_file)


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify client-server API compatibility")
    parser.add_argument("--no-codegen", action="store_true", help="Skip running codegen")
    parser.add_argument("--output", type=str, help="Output JSON file path")
    args = parser.parse_args()

    repo_root = Path(__file__).parent.parent.parent
    verifier = ClientAPIVerifier(repo_root)

    output_file = None
    if args.output:
        output_file = Path(args.output)
    else:
        output_file = repo_root / "api_compatibility_check.json"

    verifier.run_verification(not args.no_codegen, output_file)


if __name__ == "__main__":
    main()
