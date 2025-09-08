#!/usr/bin/env python3
"""
Core Export Contract Verification

Kiểm tra các API/symbol tối thiểu theo CORE_ROADMAP có tồn tại trong code.
"""

from __future__ import annotations

import importlib
from pathlib import Path
from types import ModuleType
from typing import NamedTuple
import CORE_CONTRACTS
import ImportError
import SystemExit
import bool
import contract
import e
import hasattr
import int
import len
import list
import message
import module_name
import name
import names
import print
import str
import success
import symbol
import tuple


class ExpectedContract(NamedTuple):
    """Expected module and its public symbols."""

    module: str
    symbols: tuple[str, ...]
    optional: bool = False


# Contract expectations từ CORE_ROADMAP
CORE_CONTRACTS: tuple[ExpectedContract, ...] = (
    # Adapters
    ExpectedContract(
        "zeta_vn.core.adapters.asr.whisper_adapter",
        ("transcribe", "supports", "health_check"),
        optional=True,
    ),
    ExpectedContract(
        "zeta_vn.core.adapters.vector.openai_embeddings",
        ("embed_texts", "embed_query", "get_dimension"),
        optional=True,
    ),
    ExpectedContract("zeta_vn.core.adapters.vector.chunking_service", ("split", "estimate_chunks"), optional=True),
    ExpectedContract(
        "zeta_vn.core.adapters.vector.memory_vector_store",
        ("add", "search", "delete", "persist"),
        optional=True,
    ),
    ExpectedContract(
        "zeta_vn.core.adapters.llm.openai_adapter",
        ("complete", "chat", "stream_chat"),
        optional=True,
    ),
    # Application
    ExpectedContract(
        "zeta_vn.core.application.event_bus",
        ("subscribe", "publish", "publish_batch"),
        optional=True,
    ),
    ExpectedContract(
        "zeta_vn.core.application.outbox_hardened",
        ("enqueue", "process_batch", "replay_dlq"),
        optional=True,
    ),
    ExpectedContract("zeta_vn.core.application.upcaster", ("register_upcaster", "upcast_event"), optional=True),
    # Domain Aggregates
    ExpectedContract("zeta_vn.core.domain.aggregates.agent_aggregate", ("Agent", "AgentAggregate"), optional=True),
    ExpectedContract("zeta_vn.core.domain.aggregates.chat_aggregate", ("Chat", "ChatAggregate"), optional=True),
    ExpectedContract(
        "zeta_vn.core.domain.aggregates.memory_aggregate",
        ("Memory", "MemoryAggregate"),
        optional=True,
    ),
    # Domain Entities
    ExpectedContract("zeta_vn.core.domain.entities.agent", ("Agent",)),
    ExpectedContract("zeta_vn.core.domain.entities.chat", ("Chat",), optional=True),
    ExpectedContract("zeta_vn.core.domain.entities.memory", ("Memory",), optional=True),
    ExpectedContract("zeta_vn.core.domain.entities.user", ("User",)),
    # Services
    ExpectedContract("zeta_vn.core.services.rag_service", ("RagService",)),
    ExpectedContract("zeta_vn.core.services.memory_service", ("MemoryService",)),
    ExpectedContract("zeta_vn.core.services.asr_service", ("ASRService",)),
    ExpectedContract("zeta_vn.core.services.agent_service", ("AgentService",)),
    ExpectedContract("zeta_vn.core.services.chat_service", ("ChatService",)),
    # Orchestration Services
    ExpectedContract("zeta_vn.core.services.agent_orchestrator_service", ("AgentOrchestratorService",)),
    ExpectedContract("zeta_vn.core.services.retrieval_service", ("RetrievalService",)),
    ExpectedContract("zeta_vn.core.services.rag_chunker", ("RAGChunker",), optional=True),
    ExpectedContract("zeta_vn.core.services.rag_budgeter", ("RAGBudgeter",), optional=True),
    # Use Cases
    ExpectedContract("zeta_vn.core.use_cases.chat_flow", ("ChatFlowUseCase",), optional=True),
    ExpectedContract("zeta_vn.core.use_cases.memory_operations", ("MemoryOperationsUseCase",), optional=True),
    ExpectedContract("zeta_vn.core.use_cases.agent_execution", ("AgentExecutionUseCase",), optional=True),
)


def has_symbols(mod: ModuleType, names: tuple[str, ...]) -> list[str]:
    """Check which symbols are missing from module."""
    missing = []
    for name in names:
        if not hasattr(mod, name):
            missing.append(name)
    return missing


def check_module_exists(module_name: str) -> bool:
    """Check if module can be imported."""
    try:
        importlib.import_module(module_name)
        return True
    except ImportError:
        return False


def verify_contract(contract: ExpectedContract) -> tuple[bool, str]:
    """Verify a single contract."""
    try:
        mod = importlib.import_module(contract.module)
    except ImportError as e:
        if contract.optional:
            return True, f"[SKIP] {contract.module} (optional): {e}"
        return False, f"[ERROR] import {contract.module}: {e}"

    missing = has_symbols(mod, contract.symbols)
    if missing:
        if contract.optional:
            return True, f"[WARN] {contract.module} missing optional: {', '.join(missing)}"
        return False, f"[FAIL] {contract.module} missing: {', '.join(missing)}"

    return True, f"[OK]   {contract.module}"


def generate_implementation_stubs(failed_contracts: list[ExpectedContract]) -> None:
    """Generate stub implementations for failed contracts."""
    stub_content = []

    for contract in failed_contracts:
        if contract.optional:
            continue

        module_path = contract.module.replace(".", "/") + ".py"
        stub_content.append(f"\n# Stub for {module_path}")
        stub_content.append(f'"""Auto-generated stub for {contract.module}."""')
        stub_content.append("from __future__ import annotations\n")

        for symbol in contract.symbols:
            if symbol.endswith("Service") or symbol.endswith("Aggregate"):
                stub_content.append(f"class {symbol}:")
                stub_content.append(f'    """Stub implementation of {symbol}."""')
                stub_content.append("    pass\n")
            else:
                stub_content.append(f"def {symbol}(*args, **kwargs):")
                stub_content.append(f'    """Stub implementation of {symbol}."""')
                stub_content.append("    raise NotImplementedError\n")

        stub_content.append(f"__all__ = {list(contract.symbols)!r}\n")

    if stub_content:
        stub_file = Path("generated_stubs.py")
        stub_file.write_text("\n".join(stub_content), encoding="utf-8")
        print(f"\n💡 Generated stubs in {stub_file}")


def main() -> int:
    """Main verification function."""
    print("🔍 CORE CONTRACT VERIFICATION")
    print("=" * 60)

    passed = 0
    failed = 0
    warnings = 0
    failed_contracts = []

    for contract in CORE_CONTRACTS:
        success, message = verify_contract(contract)
        print(message)

        if success:
            if "[WARN]" in message or "[SKIP]" in message:
                warnings += 1
            else:
                passed += 1
        else:
            failed += 1
            failed_contracts.append(contract)

    print("\n" + "=" * 60)
    print("📊 VERIFICATION SUMMARY")
    print(f"✅ Passed: {passed}")
    print(f"⚠️  Warnings: {warnings}")
    print(f"❌ Failed: {failed}")
    print(f"📋 Total: {len(CORE_CONTRACTS)}")

    if failed > 0:
        print(f"\n❌ {failed} critical contracts missing!")
        generate_implementation_stubs(failed_contracts)

        print("\n💡 NEXT STEPS:")
        print("1. Review failed contracts above")
        print("2. Implement missing classes/functions")
        print("3. Run verification again")
        print("4. Update ROADMAP if API changes")

        return 1

    if warnings > 0:
        print(f"\n⚠️  {warnings} optional features not implemented")
        print("Consider implementing for complete functionality")

    print("\n🎉 All critical contracts verified!")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
