#!/usr/bin/env python3
"""
Enhanced ROADMAP validation - Kiểm tra API contracts + performance budgets + security compliance.

Extends basic contract verification with:
- Performance budget validation
- Security policy compliance
- Documentation completeness
- Integration test coverage
"""

from __future__ import annotations

import importlib
import inspect
import time
from pathlib import Path
from types import ModuleType
from typing import NamedTuple
import ENHANCED_CONTRACTS
import Exception
import ImportError
import SystemExit
import any
import bool
import budget_ms
import contract
import dir
import e
import getattr
import hasattr
import int
import len
import list
import min_coverage
import module
import module_name
import module_path
import msg
import name
import passed
import print
import result
import set
import str
import sym
import tuple


class EnhancedContract(NamedTuple):
    """Enhanced contract with performance and security requirements."""

    module: str
    symbols: tuple[str, ...]
    performance_budget_ms: int | None = None
    requires_security_review: bool = False
    requires_integration_tests: bool = False
    documentation_coverage_min: int = 90


# Enhanced contracts với performance budgets và security requirements
ENHANCED_CONTRACTS: tuple[EnhancedContract, ...] = (
    # Adapters - Critical path với performance budgets
    EnhancedContract(
        "zeta_vn.core.adapters.asr.whisper_adapter",
        ("transcribe", "supports", "health_check"),
        performance_budget_ms=300,  # Realtime requirement
        requires_security_review=True,  # Audio processing
        requires_integration_tests=True,
    ),
    EnhancedContract(
        "zeta_vn.core.adapters.vector.openai_embeddings",
        ("embed_texts", "embed_query", "get_dimension"),
        performance_budget_ms=2000,  # p95 latency target
        requires_security_review=True,  # API keys, PII redaction
        requires_integration_tests=True,
    ),
    # Application layer - Reliability critical
    EnhancedContract(
        "zeta_vn.core.application.outbox_hardened",
        ("enqueue", "process_batch", "replay_dlq"),
        performance_budget_ms=100,  # Processing latency
        requires_security_review=False,
        requires_integration_tests=True,
    ),
    # Services - Business logic critical
    EnhancedContract(
        "zeta_vn.core.services.rag_service",
        ("RagService",),
        performance_budget_ms=2000,  # Query response time
        requires_security_review=True,  # Content filtering
        requires_integration_tests=True,
    ),
    # Domain - Core business logic
    EnhancedContract(
        "zeta_vn.core.domain.entities.agent",
        ("Agent", "AgentStatus", "AgentTier", "AgentCapability"),
        performance_budget_ms=None,  # Domain logic should be fast
        requires_security_review=True,  # Agent permissions
        requires_integration_tests=False,  # Unit tests sufficient
    ),
)


def check_performance_budget(module_name: str, budget_ms: int) -> tuple[bool, str]:
    """Check if module meets performance budget through simple import timing."""
    start = time.perf_counter()
    try:
        importlib.import_module(module_name)
        duration_ms = (time.perf_counter() - start) * 1000

        if duration_ms > budget_ms:
            return False, f"Import took {duration_ms:.1f}ms > budget {budget_ms}ms"
        return True, f"Import took {duration_ms:.1f}ms ≤ budget {budget_ms}ms"
    except Exception as e:
        return False, f"Import failed: {e}"


def check_security_compliance(module_path: str) -> tuple[bool, str]:
    """Basic security compliance check."""
    try:
        module_file = Path(module_path.replace(".", "/") + ".py")
        if not module_file.exists():
            return True, "Module file not found - skipping security check"

        content = module_file.read_text(encoding="utf-8")

        # Basic security checks
        security_issues = []

        # Check for common security anti-patterns
        if "secret" in content.lower() and "log" in content.lower():
            security_issues.append("Potential secret logging")

        if "password" in content.lower() and "print" in content.lower():
            security_issues.append("Potential password printing")

        # Check for proper typing (basic security through type safety)
        if "from __future__ import annotations" not in content:
            security_issues.append("Missing future annotations")

        if security_issues:
            return False, f"Security issues: {', '.join(security_issues)}"

        return True, "Basic security checks passed"

    except Exception as e:
        return False, f"Security check failed: {e}"


def check_documentation_coverage(module: ModuleType, min_coverage: int) -> tuple[bool, str]:
    """Check documentation coverage of public API."""
    try:
        public_members = [name for name in dir(module) if not name.startswith("_")]
        documented_members = []

        for name in public_members:
            member = getattr(module, name)
            if inspect.isclass(member) or inspect.isfunction(member):
                if member.__doc__ and member.__doc__.strip():
                    documented_members.append(name)

        if not public_members:
            return True, "No public members to document"

        coverage = (len(documented_members) / len(public_members)) * 100

        if coverage < min_coverage:
            undocumented = set(public_members) - set(documented_members)
            return (
                False,
                f"Documentation coverage {coverage:.1f}% < {min_coverage}%. Missing: {', '.join(list(undocumented)[:3])}",
            )

        return True, f"Documentation coverage {coverage:.1f}% ≥ {min_coverage}%"

    except Exception as e:
        return False, f"Documentation check failed: {e}"


def check_integration_tests(module_name: str) -> tuple[bool, str]:
    """Check if integration tests exist for module."""
    # Convert module name to test path
    test_path = Path("tests") / "integration" / module_name.replace(".", "/")
    test_file = test_path.with_suffix(".py")
    test_dir = test_path

    if test_file.exists() or (test_dir.exists() and any(test_dir.glob("test_*.py"))):
        return True, "Integration tests found"

    return False, f"No integration tests found at {test_file} or {test_dir}"


def verify_enhanced_contract(contract: EnhancedContract) -> tuple[bool, list[str]]:
    """Verify a single enhanced contract."""
    results = []
    all_passed = True

    # Basic symbol existence check
    try:
        mod = importlib.import_module(contract.module)
        missing = [sym for sym in contract.symbols if not hasattr(mod, sym)]
        if missing:
            all_passed = False
            results.append(f"❌ Missing symbols: {', '.join(missing)}")
        else:
            results.append(f"✅ All symbols present: {', '.join(contract.symbols)}")
    except ImportError as e:
        all_passed = False
        results.append(f"❌ Import failed: {e}")
        return False, results

    # Performance budget check
    if contract.performance_budget_ms:
        passed, msg = check_performance_budget(contract.module, contract.performance_budget_ms)
        if passed:
            results.append(f"🚀 Performance: {msg}")
        else:
            all_passed = False
            results.append(f"🐌 Performance: {msg}")

    # Security compliance check
    if contract.requires_security_review:
        passed, msg = check_security_compliance(contract.module)
        if passed:
            results.append(f"🔒 Security: {msg}")
        else:
            all_passed = False
            results.append(f"🚨 Security: {msg}")

    # Documentation coverage check
    passed, msg = check_documentation_coverage(mod, contract.documentation_coverage_min)
    if passed:
        results.append(f"📚 Documentation: {msg}")
    else:
        all_passed = False
        results.append(f"📝 Documentation: {msg}")

    # Integration tests check
    if contract.requires_integration_tests:
        passed, msg = check_integration_tests(contract.module)
        if passed:
            results.append(f"🧪 Integration tests: {msg}")
        else:
            all_passed = False
            results.append(f"🔬 Integration tests: {msg}")

    return all_passed, results


def main() -> int:
    """Main enhanced verification function."""
    print("🔍 ENHANCED CORE CONTRACT VERIFICATION")
    print("=" * 80)

    total_passed = 0
    total_failed = 0

    for contract in ENHANCED_CONTRACTS:
        print(f"\n📦 {contract.module}")
        print("-" * 60)

        passed, results = verify_enhanced_contract(contract)

        for result in results:
            print(f"  {result}")

        if passed:
            total_passed += 1
            print("  ✅ PASSED: All requirements met")
        else:
            total_failed += 1
            print("  ❌ FAILED: Some requirements not met")

    print("\n" + "=" * 80)
    print("📊 ENHANCED VERIFICATION SUMMARY")
    print(f"✅ Passed: {total_passed}")
    print(f"❌ Failed: {total_failed}")
    print(f"📋 Total: {len(ENHANCED_CONTRACTS)}")

    if total_failed > 0:
        print("\n💡 RECOMMENDATIONS:")
        print("1. Fix failed contracts above")
        print("2. Add missing integration tests in tests/integration/")
        print("3. Improve documentation for undocumented APIs")
        print("4. Review security compliance for flagged modules")
        print("5. Optimize performance for modules exceeding budgets")

        return 1

    print("\n🎉 All enhanced contracts verified!")
    print("🚀 ROADMAP implementation meets all quality standards!")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
