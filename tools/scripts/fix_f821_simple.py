from __future__ import annotations

import re
from pathlib import Path
import Exception
import bool
import e
import file_path
import new
import old
import pattern
import print
import replacement
import str
import test_file

"""
Simplified fix cho các lỗi F821 undefined names trong test files.
Chỉ sửa những pattern phổ biến và an toàn.
"""


def fix_common_f821_patterns(content: str) -> str:
    """Sửa các pattern F821 phổ biến."""
    fixes = [
        (
            r"(\s+)(await\s+system_orchestrator\.create_user_session\([^)]+\))\s*\n(\s+)users\.append\(user_session\)",
            r"\1user_session = \2\n\3users.append(user_session)",
        ),
        (
            r"(\s+)(await\s+system_orchestrator\.create_agent_and_conversation\([^)]+\))\s*\n(\s+)[^=]*agent_result",
            r'\1agent_result = \2\n\3conversation_id = agent_result["conversation"]["id"]',
        ),
        (
            r"(\s+)(await\s+ws_manager\.create_connection\([^)]+\))\s*\n(\s+)users\.append\(user\)",
            r"\1user = \2\n\3users.append(user)",
        ),
        (
            r"(\s+)(await\s+connection\.ping\(\))\s*\n(\s+)assert\s+ping_result",
            r"\1ping_result = \2\n\3assert ping_result",
        ),
        (
            r"(\s+)(await\s+connection\.pong\(\))\s*\n(\s+)assert\s+pong_result",
            r"\1pong_result = \2\n\3assert pong_result",
        ),
    ]
    for pattern, replacement in fixes:
        content = re.sub(pattern, replacement, content, flags=re.MULTILINE | re.DOTALL)
    simple_fixes = {
        "if agent.name in self.agents_by_name:": "if deleted_agent and deleted_agent.name in self.agents_by_name:",
        "del self.agents_by_name[agent.name]": "del self.agents_by_name[deleted_agent.name]",
        "assert result.error_rate_percent": "assert load_result.error_rate_percent",
        "assert result.average_response_time_ms": "assert load_result.average_response_time_ms",
        "assert result.p95_response_time_ms": "assert load_result.p95_response_time_ms",
        "assert result.requests_per_second": "assert load_result.requests_per_second",
        'f"Error rate too high: {result.error_rate_percent': 'f"Error rate too high: {load_result.error_rate_percent',
        'f"Average response time too slow: {result.average_response_time_ms': 'f"Average response time too slow: {load_result.average_response_time_ms',
        'f"P95 response time too slow: {result.p95_response_time_ms': 'f"P95 response time too slow: {load_result.p95_response_time_ms',
        'f"Throughput regression: {result.requests_per_second': 'f"Throughput regression: {load_result.requests_per_second',
        'f"Error rate regression: {result.error_rate_percent': 'f"Error rate regression: {load_result.error_rate_percent',
        'f"Average response time regression: {result.average_response_time_ms': 'f"Average response time regression: {load_result.average_response_time_ms',
        'f"P95 response time regression: {result.p95_response_time_ms': 'f"P95 response time regression: {load_result.p95_response_time_ms',
        "data.append(result)": "data.append(memory_result)",
        "assert agent.name": "assert created_agent.name",
        "assert agent.description": "assert created_agent.description",
        "assert AgentCapability.CHAT in agent.config.capabilities": "assert AgentCapability.CHAT in created_agent.config.capabilities",
        "assert agent.status": "assert created_agent.status",
        "automation:plan:create = {": "user_with_perms = {",
        "mock_agent_repo.create = AsyncMock(return_value=expected_agent)": "mock_agent_repo.create = AsyncMock(return_value=created_agent)",
        "mock_agent_repo.get_by_id = AsyncMock(return_value=original_agent)": "mock_agent_repo.get_by_id = AsyncMock(return_value=original_agent)",
    }
    for old, new in simple_fixes.items():
        content = content.replace(old, new)
    return content


def fix_test_file(file_path: Path) -> bool:
    """Fix F821 errors in a single test file."""
    try:
        content = file_path.read_text(encoding="utf-8")
        original_content = content
        fixed_content = fix_common_f821_patterns(content)
        if fixed_content != original_content:
            file_path.write_text(fixed_content, encoding="utf-8")
            return True
        return False
    except Exception as e:
        print(f"Error fixing {file_path}: {e}")
        return False


def main():
    """Main entry point."""
    project_root = Path(__file__).parent.parent
    test_files = [
        project_root / "zeta_vn/tests/integration/test_system_integration.py",
        project_root / "zeta_vn/tests/integration/test_websockets.py",
        project_root / "zeta_vn/tests/mocks/mock_agent_repository.py",
        project_root / "zeta_vn/tests/performance/test_performance.py",
        project_root / "zeta_vn/tests/performance/test_stress.py",
        project_root / "zeta_vn/tests/unit/agents/test_agent_management.py",
        project_root / "zeta_vn/tests/unit/auth/test_auth_use_cases.py",
        project_root / "zeta_vn/tests/unit/test_use_cases.py",
        project_root / "zeta_vn/tests/unit/test_specifications.py",
        project_root / "zeta_vn/tests/unit/test_session_entity.py",
        project_root / "zeta_vn/tests/unit/test_orchestrator_rule_permission.py",
        project_root / "zeta_vn/tests/test_agent_orchestrator_parallel.py",
    ]
    fixed_count = 0
    for test_file in test_files:
        if test_file.exists():
            if fix_test_file(test_file):
                print(f"✓ Fixed {test_file.relative_to(project_root)}")
                fixed_count += 1
        else:
            print(f"⚠ File not found: {test_file}")
    print(f"\n🎯 Fixed {fixed_count} test files")
    print("Now run: uv run ruff check . --statistics")


if __name__ == "__main__":
    main()
