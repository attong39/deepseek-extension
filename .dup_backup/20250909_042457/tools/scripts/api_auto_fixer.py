#!/usr/bin/env python3
"""
tools/api_auto_fixer.py

Tự động khắc phục các vấn đề API consistency giữa desktop và server.
"""

from __future__ import annotations

import re
from pathlib import Path
import Exception
import any
import code
import dict
import exc_dir
import k
import len
import message
import original_content
import p
import print
import py_file
import self
import set
import sorted
import str
import v

ROOT = Path(__file__).resolve().parents[1]
SERVER_ROOT = ROOT / "zeta_vn"
DESKTOP_ROOT = ROOT / "desktop_ai_zeta"


class APIAutoFixer:
    def __init__(self):
        self.fixes_applied = 0

    def fix_all(self) -> None:
        """Apply all available fixes."""
        print("🔧 Auto-fixing API consistency issues...")

        # 1. Sync error codes
        self._sync_error_codes()

        # 2. Fix generated types placeholders
        self._fix_generated_types()

        # 3. Optimize API client
        self._optimize_api_client()

        print(f"\n✅ Applied {self.fixes_applied} fixes!")
        print("🔄 Run cross-project guard để verify...")

    def _sync_error_codes(self) -> None:
        """Sync error codes từ server sang desktop."""
        print("\n🚨 Syncing error codes...")

        # Extract server error codes với messages
        server_errors = self._extract_server_error_codes_with_messages()

        # Read current desktop error codes
        desktop_error_file = DESKTOP_ROOT / "src" / "api" / "errorCodes.ts"

        if not desktop_error_file.exists():
            print("❌ Desktop errorCodes.ts not found")
            return

        current_content = desktop_error_file.read_text(encoding="utf-8")

        # Parse existing ERROR_MESSAGES object
        existing_codes = self._parse_existing_error_messages(current_content)

        # Merge server codes với existing desktop codes
        merged_codes = {**existing_codes, **server_errors}

        # Generate new ERROR_MESSAGES content
        new_content = self._generate_error_codes_file(merged_codes, current_content)

        # Write back
        desktop_error_file.write_text(new_content, encoding="utf-8")
        self.fixes_applied += 1
        print(f"✅ Synced {len(server_errors)} error codes to desktop")

    def _fix_generated_types(self) -> None:
        """Fix generated types placeholders."""
        print("\n📦 Fixing generated types...")

        generated_dir = DESKTOP_ROOT / "src" / "api" / "generated"

        # Fix index.d.ts placeholder
        index_file = generated_dir / "index.d.ts"
        if index_file.exists():
            content = index_file.read_text(encoding="utf-8")
            if "placeholder" in content.lower() or len(content.strip()) < 50:
                # Create proper index.d.ts
                new_content = """// AUTO-GENERATED. Run: npm run api:gen
export * from "./types";
export * from "./client";
export * from "./schema";
"""
                index_file.write_text(new_content, encoding="utf-8")
                self.fixes_applied += 1
                print("✅ Fixed index.d.ts placeholder")

    def _optimize_api_client(self) -> None:
        """Optimize API client configuration."""
        print("\n⚙️ Optimizing API client...")

        api_client_file = DESKTOP_ROOT / "src" / "api" / "apiClient.ts"
        if not api_client_file.exists():
            return

        content = api_client_file.read_text(encoding="utf-8")

        # Add retries configuration if missing
        if "retries" not in content and "retry" not in content:
            # Insert retry configuration
            config_pattern = r"(axios\.create\(\{[^}]+)"

            def add_retry_config(match):
                existing_config = match.group(1)
                if existing_config.endswith("{"):
                    return f"{existing_config}\n  retries: 3,"
                else:
                    return f"{existing_config},\n  retries: 3,"

            if re.search(config_pattern, content):
                new_content = re.sub(config_pattern, add_retry_config, content)
                api_client_file.write_text(new_content, encoding="utf-8")
                self.fixes_applied += 1
                print("✅ Added retry configuration to API client")

    def _extract_server_error_codes_with_messages(self) -> dict[str, str]:
        """Extract error codes và messages từ server."""
        error_codes = {}

        # Map error code patterns to Vietnamese messages
        default_messages = {
            # Auth errors
            "AUTH_001": "Thông tin đăng nhập không hợp lệ.",
            "AUTH_002": "Bạn không có đủ quyền để thực hiện thao tác này.",
            "AUTH_003": "Token không hợp lệ hoặc đã hết hạn.",
            "AUTH_004": "Yêu cầu xác thực đa yếu tố (MFA).",
            "AUTH_005": "Phiên làm việc đã hết hạn.",
            "AUTH_006": "Truy cập bị từ chối cho tài nguyên yêu cầu.",
            "AUTH_007": "Bạn thao tác quá nhanh, vui lòng thử lại sau.",
            # Business errors
            "BIZ_001": "Không tìm thấy agent.",
            "BIZ_002": "Tạo agent thất bại.",
            "BIZ_003": "Triển khai agent thất bại.",
            "BIZ_004": "Lỗi phiên chat.",
            "BIZ_005": "Xử lý tin nhắn thất bại.",
            "BIZ_006": "Lỗi thao tác bộ nhớ.",
            "BIZ_007": "Lỗi vector embedding.",
            "BIZ_008": "Lỗi lập kế hoạch.",
            "BIZ_009": "Lỗi thực thi quy trình.",
            "BIZ_010": "Lỗi huấn luyện mô hình.",
            "BIZ_011": "Lỗi tải mô hình.",
            "BIZ_012": "Dữ liệu không hợp lệ.",
            "BIZ_013": "Vi phạm luật nghiệp vụ.",
            "BIZ_014": "Vượt giới hạn tài nguyên.",
            "BIZ_015": "Dịch vụ bên ngoài gặp lỗi.",
            "BIZ_016": "Không tìm thấy thực thể.",
            # Repository errors
            "REPO_001": "Kết nối cơ sở dữ liệu thất bại.",
            "REPO_002": "Pool kết nối cơ sở dữ liệu bị cạn kiệt.",
            "REPO_003": "Vi phạm toàn vẹn dữ liệu.",
            "REPO_004": "Vi phạm khóa ngoại.",
            "REPO_005": "Không tìm thấy bản ghi.",
            "REPO_006": "Bản ghi trùng lặp.",
            "REPO_007": "Thực thi truy vấn thất bại.",
            "REPO_008": "Truy vấn quá thời gian.",
            "REPO_009": "Giao dịch cơ sở dữ liệu lỗi.",
            "REPO_010": "Deadlock cơ sở dữ liệu.",
            "REPO_011": "Lỗi cơ sở dữ liệu vector.",
            "REPO_012": "Sai kích thước embedding.",
            "REPO_013": "Lỗi bộ nhớ đệm (cache).",
            "REPO_014": "Kết nối cache thất bại.",
            "REPO_015": "Lỗi migration cơ sở dữ liệu.",
            "REPO_016": "Lỗi sao lưu dữ liệu.",
            "REPO_017": "Dữ liệu không hợp lệ.",
        }

        # Extract actual codes từ server files
        server_codes = self._scan_server_error_codes()

        # Combine với default messages
        for code in server_codes:
            if code in default_messages:
                error_codes[code] = default_messages[code]
            else:
                # Generate generic message
                category = code.split("_")[0].lower()
                error_codes[code] = f"Lỗi {category} không xác định."

        return error_codes

    def _scan_server_error_codes(self) -> set[str]:
        """Scan server files để tìm error codes."""
        codes = set()

        # Scan exception directories
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
                    # Find standard error code patterns
                    found_codes = re.findall(r'["\']([A-Z_]+_\d{3})["\']', content)
                    codes.update(found_codes)
                except Exception:
                    continue

        return codes

    def _parse_existing_error_messages(self, content: str) -> dict[str, str]:
        """Parse existing ERROR_MESSAGES object từ TypeScript file."""
        error_messages = {}

        # Find ERROR_MESSAGES object
        pattern = r"ERROR_MESSAGES:\s*Record<string,\s*string>\s*=\s*\{([^}]+)\}"
        match = re.search(pattern, content, re.DOTALL)

        if match:
            messages_content = match.group(1)
            # Parse individual error entries
            entry_pattern = r'([A-Z_]+):\s*["\']([^"\']+)["\']'
            entries = re.findall(entry_pattern, messages_content)

            for code, message in entries:
                error_messages[code] = message

        return error_messages

    def _generate_error_codes_file(self, error_codes: dict[str, str], original_content: str) -> str:
        """Generate new error codes file content."""

        # Build ERROR_MESSAGES object
        sorted_codes = sorted(error_codes.items())

        # Group by category
        auth_codes = [(k, v) for k, v in sorted_codes if k.startswith("AUTH_")]
        biz_codes = [(k, v) for k, v in sorted_codes if k.startswith("BIZ_")]
        repo_codes = [(k, v) for k, v in sorted_codes if k.startswith("REPO_")]
        other_codes = [(k, v) for k, v in sorted_codes if not any(k.startswith(p) for p in ["AUTH_", "BIZ_", "REPO_"])]

        error_messages_content = """export const ERROR_MESSAGES: Record<string, string> = {
  // ---- Backward-compat aliases ----
  AUTH_INVALID: "Thông tin đăng nhập không hợp lệ.", // → AUTH_001
  AUTH_EXPIRED: "Phiên đăng nhập đã hết hạn.", // → AUTH_005
  RATE_LIMITED: "Bạn thao tác quá nhanh, vui lòng thử lại sau.", // → AUTH_007
  VALIDATION_FAILED: "Dữ liệu không hợp lệ.", // → BIZ_012 / REPO_017

  // ---- Auth errors (AUTH_XXX) ----"""

        for code, message in auth_codes:
            error_messages_content += f'\n  {code}: "{message}",  // {self._get_error_comment(code)}'

        error_messages_content += "\n\n  // ---- Business errors (BIZ_XXX) ----"
        for code, message in biz_codes:
            error_messages_content += f'\n  {code}: "{message}",  // {self._get_error_comment(code)}'

        error_messages_content += "\n\n  // ---- Repository/Data errors (REPO_XXX) ----"
        for code, message in repo_codes:
            error_messages_content += f'\n  {code}: "{message}",  // {self._get_error_comment(code)}'

        if other_codes:
            error_messages_content += "\n\n  // ---- Other errors ----"
            for code, message in other_codes:
                error_messages_content += f'\n  {code}: "{message}",'

        error_messages_content += "\n\n  // ---- Fallback ----\n"
        error_messages_content += '  UNKNOWN: "Đã xảy ra lỗi không xác định.",\n};'

        # Find and replace ERROR_MESSAGES in original content
        pattern = r"export const ERROR_MESSAGES:[^{]+\{[^}]+\}"
        if re.search(pattern, original_content, re.DOTALL):
            return re.sub(pattern, error_messages_content, original_content, flags=re.DOTALL)
        else:
            # Insert at beginning if not found
            header = "// AUTO-UPDATED by api_auto_fixer.py\n"
            return header + error_messages_content + "\n\n" + original_content

    def _get_error_comment(self, code: str) -> str:
        """Get comment cho error code."""
        comments = {
            "AUTH_001": "AuthenticationError / InvalidCredentialsError",
            "AUTH_002": "AuthorizationError",
            "AUTH_003": "JWTTokenError / InvalidTokenError",
            "AUTH_004": "MFARequiredError",
            "AUTH_005": "SessionExpiredError",
            "AUTH_006": "PermissionDeniedError",
            "AUTH_007": "RateLimitExceededError",
            "BIZ_001": "AgentNotFoundError",
            "BIZ_002": "AgentCreationError",
            "BIZ_003": "AgentDeploymentError",
            "BIZ_004": "ChatSessionError",
            "BIZ_005": "MessageProcessingError",
            "BIZ_006": "MemoryOperationError",
            "BIZ_007": "VectorEmbeddingError",
            "BIZ_008": "PlanningError",
            "BIZ_009": "WorkflowExecutionError",
            "BIZ_010": "TrainingError",
            "BIZ_011": "ModelLoadError",
            "BIZ_012": "ValidationError (business)",
            "BIZ_013": "BusinessRuleViolationError",
            "BIZ_014": "ResourceLimitExceededError",
            "BIZ_015": "ExternalServiceError",
            "BIZ_016": "EntityNotFoundError",
            "REPO_001": "DatabaseConnectionError",
            "REPO_002": "ConnectionPoolExhaustedError",
            "REPO_003": "DataIntegrityError",
            "REPO_004": "ForeignKeyViolationError",
            "REPO_005": "RecordNotFoundError",
            "REPO_006": "DuplicateRecordError",
            "REPO_007": "QueryExecutionError",
            "REPO_008": "QueryTimeoutError",
            "REPO_009": "TransactionError",
            "REPO_010": "DeadlockError",
            "REPO_011": "VectorDatabaseError",
            "REPO_012": "EmbeddingDimensionError",
            "REPO_013": "CacheError",
            "REPO_014": "CacheConnectionError",
            "REPO_015": "MigrationError",
            "REPO_016": "BackupError",
            "REPO_017": "ValidationError (repository)",
        }
        return comments.get(code, "")


def main():
    """Main entry point."""
    fixer = APIAutoFixer()
    fixer.fix_all()


if __name__ == "__main__":
    main()
