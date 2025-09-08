#!/usr/bin/env python3
"""
tools/cross_project_guard.py

Kiểm tra tính nhất quán giữa server (zeta_vn) và desktop (desktop_ai_zeta).
Đảm bảo API contracts, schemas, error codes, i18n keys đồng bộ.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any
import Exception
import ValueError
import bool
import category
import dict
import dir_name
import endpoints
import enumerate
import env_file
import error
import errors
import event_name
import f
import grouped_errors
import i
import i18n_keys
import isinstance
import json_file
import key
import len
import list
import max
import message
import method
import model
import name
import obj
import path
import prefix
import print
import py_file
import schema_file
import self
import set
import str
import suggestion
import suggestions
import ts_file
import types
import value
import var

ROOT = Path(__file__).resolve().parents[1]
SERVER_ROOT = ROOT / "zeta_vn"
DESKTOP_ROOT = ROOT / "desktop_ai_zeta"


class ConsistencyError:
    def __init__(self, category: str, message: str, suggestions: list[str] | None = None):
        self.category = category
        self.message = message
        self.suggestions = suggestions or []


class CrossProjectGuard:
    def __init__(self) -> None:
        self.errors: list[ConsistencyError] = []

    def check_all(self) -> bool:
        """Chạy tất cả kiểm tra consistency."""
        print("🔍 Cross-project consistency check...")

        # 1. API Contracts
        self._check_api_contracts()

        # 2. WebSocket Schemas
        self._check_websocket_schemas()

        # 3. Error Codes
        self._check_error_codes()

        # 4. Environment Variables
        self._check_environment_consistency()

        # 5. i18n Keys
        self._check_i18n_consistency()

        # 6. OpenAPI Generated Types
        self._check_generated_types()

        # Report results
        return self._report_results()

    def _check_api_contracts(self) -> None:
        """Kiểm tra API endpoints server có khớp với client types không."""
        print("📡 Checking API contracts...")

        # Tìm API endpoints trong server
        server_endpoints = self._extract_server_endpoints()

        # Tìm generated API types trong desktop
        desktop_types = self._extract_desktop_api_types()

        # So sánh
        missing_in_desktop = server_endpoints - desktop_types
        if missing_in_desktop:
            self.errors.append(
                ConsistencyError(
                    "API_CONTRACTS",
                    f"Server endpoints missing in desktop types: {missing_in_desktop}",
                    [
                        "Chạy: cd desktop_ai_zeta && node scripts/generate_openapi_types.mjs",
                        "Hoặc: npm run api:gen",
                    ],
                )
            )

    def _check_websocket_schemas(self) -> None:
        """Kiểm tra WebSocket schemas đồng bộ."""
        print("🔌 Checking WebSocket schemas...")

        # Tìm WS message types trong server
        server_ws_schemas = self._extract_server_ws_schemas()

        # Tìm WS schemas trong desktop
        desktop_ws_schemas = self._extract_desktop_ws_schemas()

        # So sánh keys
        server_keys = set(server_ws_schemas.keys()) if server_ws_schemas else set()
        desktop_keys = set(desktop_ws_schemas.keys()) if desktop_ws_schemas else set()

        missing_in_desktop = server_keys - desktop_keys
        missing_in_server = desktop_keys - server_keys

        if missing_in_desktop:
            self.errors.append(
                ConsistencyError(
                    "WS_SCHEMAS",
                    f"Server WS schemas missing in desktop: {missing_in_desktop}",
                    ["Cập nhật desktop_ai_zeta/src/api/wsSchema.ts"],
                )
            )

        if missing_in_server:
            self.errors.append(
                ConsistencyError(
                    "WS_SCHEMAS",
                    f"Desktop WS schemas missing in server: {missing_in_server}",
                    ["Cập nhật server WebSocket message definitions"],
                )
            )

    def _check_error_codes(self) -> None:
        """Kiểm tra error codes đồng bộ."""
        print("❌ Checking error codes...")

        # Server error codes
        server_errors = self._extract_server_error_codes()

        # Desktop error codes
        desktop_errors = self._extract_desktop_error_codes()

        missing_in_desktop = server_errors - desktop_errors
        if missing_in_desktop:
            self.errors.append(
                ConsistencyError(
                    "ERROR_CODES",
                    f"Server error codes missing in desktop: {missing_in_desktop}",
                    ["Cập nhật desktop_ai_zeta/src/api/errorCodes.ts"],
                )
            )

    def _check_environment_consistency(self) -> None:
        """Kiểm tra environment variables consistency."""
        print("🌍 Checking environment variables...")

        # Tìm env vars trong server
        server_env_vars = self._extract_server_env_vars()

        # Tìm env vars trong desktop
        desktop_env_vars = self._extract_desktop_env_vars()

        # Kiểm tra API_BASE_URL, WS_URL consistency
        api_vars = {var for var in server_env_vars if "API" in var or "URL" in var}
        desktop_api_vars = {var for var in desktop_env_vars if "API" in var or "URL" in var}

        if api_vars and not desktop_api_vars:
            self.errors.append(
                ConsistencyError(
                    "ENVIRONMENT",
                    "Server có API URL configs nhưng desktop thiếu VITE_ prefixed vars",
                    ["Đảm bảo desktop có VITE_API_BASE_URL, VITE_WS_URL"],
                )
            )

    def _check_i18n_consistency(self) -> None:
        """Kiểm tra i18n keys consistency."""
        print("🌐 Checking i18n keys...")

        # Server i18n (nếu có)
        server_i18n = self._extract_server_i18n_keys()

        # Desktop i18n
        desktop_i18n = self._extract_desktop_i18n_keys()

        # Tìm error message keys chung
        common_error_keys = {key for key in server_i18n if "error" in key.lower()}
        desktop_error_keys = {key for key in desktop_i18n if "error" in key.lower()}

        missing_error_translations = common_error_keys - desktop_error_keys
        if missing_error_translations:
            self.errors.append(
                ConsistencyError(
                    "I18N_KEYS",
                    f"Server error keys missing desktop translations: {missing_error_translations}",
                    ["Cập nhật desktop i18n/vi.json, i18n/en.json"],
                )
            )

    def _check_generated_types(self) -> None:
        """Kiểm tra generated types có up-to-date không."""
        print("🔧 Checking generated types...")

        openapi_file = SERVER_ROOT / "app" / "main.py"  # FastAPI app
        generated_file = DESKTOP_ROOT / "src" / "api" / "generated"

        if openapi_file.exists() and generated_file.exists():
            # Kiểm tra timestamp
            server_mtime = openapi_file.stat().st_mtime
            try:
                desktop_mtime = max(f.stat().st_mtime for f in generated_file.rglob("*.ts") if f.is_file())

                if server_mtime > desktop_mtime:
                    self.errors.append(
                        ConsistencyError(
                            "GENERATED_TYPES",
                            "Server API đã thay đổi sau lần generate types cuối",
                            [
                                "cd desktop_ai_zeta",
                                "node scripts/generate_openapi_types.mjs",
                            ],
                        )
                    )
            except ValueError:
                # Không có generated files
                self.errors.append(
                    ConsistencyError(
                        "GENERATED_TYPES",
                        "Chưa có generated API types trong desktop",
                        ["cd desktop_ai_zeta && node scripts/generate_openapi_types.mjs"],
                    )
                )

    def _extract_server_endpoints(self) -> set[str]:
        """Extract API endpoints từ server FastAPI routers."""
        endpoints: set[str] = set()

        api_dir = SERVER_ROOT / "app" / "api" / "v1" / "endpoints"
        if not api_dir.exists():
            return endpoints

        for py_file in api_dir.glob("*.py"):
            try:
                content = py_file.read_text(encoding="utf-8")
                # Tìm @router.post, @router.get, etc.
                router_methods = re.findall(
                    r'@router\.(get|post|put|delete|patch)\(["\']([^"\']+)["\']',
                    content,
                )
                for method, path in router_methods:
                    endpoints.add(f"{method.upper()} {path}")
            except Exception:
                continue

        return endpoints

    def _extract_desktop_api_types(self) -> set[str]:
        """Extract API types từ desktop generated files."""
        types: set[str] = set()

        generated_dir = DESKTOP_ROOT / "src" / "api" / "generated"
        if not generated_dir.exists():
            return types

        for ts_file in generated_dir.rglob("*.ts"):
            try:
                content = ts_file.read_text(encoding="utf-8")
                # Tìm exported functions/types
                exports = re.findall(r"export.*?(get|post|put|delete|patch)\w*", content, re.IGNORECASE)
                types.update(exports)
            except Exception:
                continue

        return types

    def _extract_server_ws_schemas(self) -> dict[str, Any]:
        """Extract WebSocket message schemas từ server."""
        schemas = {}

        # Tìm trong app/websockets/
        ws_dir = SERVER_ROOT / "app" / "websockets"
        if ws_dir.exists():
            for py_file in ws_dir.glob("*.py"):
                try:
                    content = py_file.read_text(encoding="utf-8")
                    # Tìm Pydantic models
                    models = re.findall(r"class (\w+)\(.*BaseModel\)", content)
                    for model in models:
                        # Skip WSBase vì đây là envelope wrapper, không phải event schema
                        if model != "WSBase":
                            schemas[model] = {"source": str(py_file)}
                except Exception:
                    continue

        return schemas

    def _extract_desktop_ws_schemas(self) -> dict[str, Any]:
        """Extract WebSocket schemas từ desktop."""
        schemas = {}

        ws_schema_file = DESKTOP_ROOT / "src" / "api" / "wsSchema.ts"
        ws_services_file = DESKTOP_ROOT / "src" / "services" / "wsSchema.ts"

        # Kiểm tra cả hai locations
        for schema_file in [ws_schema_file, ws_services_file]:
            if not schema_file.exists():
                continue

            try:
                content = schema_file.read_text(encoding="utf-8")

                # Tìm zod schemas pattern: export const XxxSchema
                schema_names = re.findall(r"export const (\w+Schema)", content)
                for name in schema_names:
                    schemas[name.replace("Schema", "")] = {"source": str(schema_file)}

                # Tìm WS_SCHEMAS object - extract tất cả schema names
                # Pattern: tìm các properties trong object với format: EventName: { ... }
                event_patterns = re.findall(r"(\w+(?:Event|Message|Base)):\s*{", content)
                for event_name in event_patterns:
                    schemas[event_name] = {"source": str(schema_file)}

            except Exception:
                pass

        return schemas

    def _extract_server_error_codes(self) -> set[str]:
        """Extract error codes từ server."""
        error_codes = set()

        # Tìm trong app/exceptions hoặc core/exceptions
        for dir_name in ["app/exceptions", "core/exceptions", "app/errors"]:
            error_dir = SERVER_ROOT / dir_name
            if error_dir.exists():
                for py_file in error_dir.glob("*.py"):
                    try:
                        content = py_file.read_text(encoding="utf-8")
                        # Tìm error codes/constants
                        codes = re.findall(r'["\']([A-Z_]+_ERROR)["\']', content)
                        error_codes.update(codes)
                    except Exception:
                        continue

        return error_codes

    def _extract_desktop_error_codes(self) -> set[str]:
        """Extract error codes từ desktop."""
        error_codes = set()

        error_file = DESKTOP_ROOT / "src" / "api" / "errorCodes.ts"
        if error_file.exists():
            try:
                content = error_file.read_text(encoding="utf-8")
                # Tìm exported error codes
                codes = re.findall(r'["\']([A-Z_]+_ERROR)["\']', content)
                error_codes.update(codes)
            except Exception:
                pass

        return error_codes

    def _extract_server_env_vars(self) -> set[str]:
        """Extract environment variables từ server."""
        env_vars = set()

        # Tìm trong config/settings.py
        settings_file = SERVER_ROOT / "config" / "settings.py"
        if settings_file.exists():
            try:
                content = settings_file.read_text(encoding="utf-8")
                # Tìm env variables
                vars_found = re.findall(r'os\.environ\.get\(["\']([^"\']+)["\']', content)
                env_vars.update(vars_found)

                # Tìm Field với env parameter
                field_envs = re.findall(r'Field\([^)]*env=["\']([^"\']+)["\']', content)
                env_vars.update(field_envs)
            except Exception:
                pass

        return env_vars

    def _extract_desktop_env_vars(self) -> set[str]:
        """Extract environment variables từ desktop."""
        env_vars = set()

        # Tìm trong .env files
        for env_file in [".env.example", ".env.development", ".env.production"]:
            file_path = DESKTOP_ROOT / env_file
            if file_path.exists():
                try:
                    content = file_path.read_text(encoding="utf-8")
                    vars_found = re.findall(r"^([A-Z_][A-Z0-9_]*)=", content, re.MULTILINE)
                    env_vars.update(vars_found)
                except Exception:
                    continue

        return env_vars

    def _extract_server_i18n_keys(self) -> set[str]:
        """Extract i18n keys từ server (nếu có)."""
        # Server có thể không có i18n, return empty set
        return set()

    def _extract_desktop_i18n_keys(self) -> set[str]:
        """Extract i18n keys từ desktop."""
        i18n_keys: set[str] = set()

        i18n_dir = DESKTOP_ROOT / "src" / "i18n"
        if not i18n_dir.exists():
            return i18n_keys

        for json_file in i18n_dir.glob("*.json"):
            keys = self._extract_keys_from_i18n_file(json_file)
            i18n_keys.update(keys)

        return i18n_keys

    def _extract_keys_from_i18n_file(self, json_file: Path) -> set[str]:
        """Helper để extract keys từ một file i18n."""
        keys: set[str] = set()
        try:
            content = json_file.read_text(encoding="utf-8")
            data = json.loads(content)
            self._extract_nested_keys(data, "", keys)
        except Exception:
            pass
        return keys

    def _extract_nested_keys(self, obj: Any, prefix: str, keys: set[str]) -> None:
        """Helper để extract nested keys recursively."""
        if isinstance(obj, dict):
            for key, value in obj.items():
                full_key = f"{prefix}.{key}" if prefix else key
                if isinstance(value, dict):
                    self._extract_nested_keys(value, full_key, keys)
                else:
                    keys.add(full_key)

    def _report_results(self) -> bool:
        """Report kết quả kiểm tra."""
        if not self.errors:
            print("✅ Cross-project consistency: TẤT CẢ ĐỀU NHẤT QUÁN!")
            return True

        print(f"\n❌ Phát hiện {len(self.errors)} vấn đề consistency:")

        grouped_errors: dict[str, list[ConsistencyError]] = {}
        for error in self.errors:
            if error.category not in grouped_errors:
                grouped_errors[error.category] = []
            grouped_errors[error.category].append(error)

        for category, errors in grouped_errors.items():
            print(f"\n📋 {category}:")
            for i, error in enumerate(errors, 1):
                print(f"  {i}. {error.message}")
                if error.suggestions:
                    print("     💡 Khắc phục:")
                    for suggestion in error.suggestions:
                        print(f"        - {suggestion}")

        print("\n🔧 Để khắc phục nhanh:")
        print("   cd desktop_ai_zeta")
        print("   npm run api:gen")
        print("   node scripts/contract_guard.mjs")

        return False


def main() -> None:
    """Main entry point."""
    guard = CrossProjectGuard()
    success = guard.check_all()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
