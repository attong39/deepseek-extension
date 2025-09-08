#!/usr/bin/env python3
"""
Generate file_expectations.yaml từ PROJECT_MAP.md

Tự động phân tích cấu trúc project và sinh ra config expectations
cho các module và directory structure bắt buộc.
"""

from __future__ import annotations

import re
from pathlib import Path
import SystemExit
import data
import dict
import f
import int
import k
import len
import line
import m
import mod
import pkgs
import print
import s
import set
import spec
import str
import v

OUT = Path("configs/file_expectations.yaml")
SRC = Path(".github/prompts/PROJECT_MAP.md")

# Heuristic patterns từ phân tích domain-driven architecture
DIR_RULES = {
    "zeta_vn.app.api.v1": [
        "router.py",
        "status.py",
        "rag.py",
        "memory.py",
        "chat.py",
        "agent.py",
        "auth.py",
    ],
    "zeta_vn.app.websockets": ["router.py", "training_ws.py"],
    "zeta_vn.core.adapters.asr": ["whisper_adapter.py", "local_asr_adapter.py"],
    "zeta_vn.core.adapters.vector": [
        "openai_embeddings.py",
        "chunking_service.py",
        "memory_vector_store.py",
    ],
    "zeta_vn.core.adapters.llm": ["openai_adapter.py", "anthropic_adapter.py"],
    "zeta_vn.core.domain.entities": ["Agent.py", "Chat.py", "Memory.py", "Plan.py", "User.py"],
    "zeta_vn.core.domain.ports.repositories": [
        "agent_repository.py",
        "chat_repository.py",
        "memory_repository.py",
    ],
    "zeta_vn.core.services": ["agent_service.py", "chat_service.py", "memory_service.py"],
    "zeta_vn.core.use_cases": ["agent_use_cases.py", "chat_use_cases.py", "memory_use_cases.py"],
}

REQUIRED_SYMBOLS = {
    # API layer
    "zeta_vn.app.api.v1.router": ["get_api_router"],
    "zeta_vn.app.api.v1.status": ["router"],
    "zeta_vn.app.api.v1.rag": ["router"],
    "zeta_vn.app.api.v1.memory": ["router"],
    "zeta_vn.app.api.v1.chat": ["router"],
    "zeta_vn.app.api.v1.agent": ["router"],
    "zeta_vn.app.api.v1.auth": ["router"],
    # WebSocket
    "zeta_vn.app.websockets.router": ["get_ws_router"],
    "zeta_vn.app.websockets.training_ws": ["TrainingWebSocket"],
    # Core Application
    "zeta_vn.core.application.outbox": ["Outbox", "OutboxRepository", "OutboxProcessor"],
    # Adapters
    "zeta_vn.core.adapters.asr.whisper_adapter": ["WhisperASRAdapter"],
    "zeta_vn.core.adapters.asr.local_asr_adapter": ["LocalASRAdapter"],
    "zeta_vn.core.adapters.vector.openai_embeddings": ["OpenAIEmbeddingAdapter"],
    "zeta_vn.core.adapters.vector.chunking_service": ["ChunkingService"],
    "zeta_vn.core.adapters.vector.memory_vector_store": ["MemoryVectorStoreAdapter"],
    "zeta_vn.core.adapters.llm.openai_adapter": ["OpenAIAdapter"],
    "zeta_vn.core.adapters.llm.anthropic_adapter": ["AnthropicAdapter"],
    # Domain Entities
    "zeta_vn.core.domain.entities.Agent": ["Agent"],
    "zeta_vn.core.domain.entities.Chat": ["Chat"],
    "zeta_vn.core.domain.entities.Memory": ["Memory"],
    "zeta_vn.core.domain.entities.Plan": ["Plan"],
    "zeta_vn.core.domain.entities.User": ["User"],
    # Repository Ports
    "zeta_vn.core.domain.ports.repositories": [
        "AgentRepository",
        "ChatRepository",
        "MemoryRepository",
        "PlanRepository",
        "UserRepository",
    ],
    # Services
    "zeta_vn.core.services.agent_service": ["AgentService"],
    "zeta_vn.core.services.chat_service": ["ChatService"],
    "zeta_vn.core.services.memory_service": ["MemoryService"],
    # Use Cases
    "zeta_vn.core.use_cases.agent": ["CreateAgentUseCase", "GetAgentUseCase"],
    "zeta_vn.core.use_cases.chat": ["CreateChatUseCase", "GetChatUseCase"],
    "zeta_vn.core.use_cases.memory": ["CreateMemoryUseCase", "GetMemoryUseCase"],
}


def parse_packages_from_project_map(text: str) -> set[str]:
    """Lấy các package paths từ PROJECT_MAP.md."""
    pkgs: set[str] = set()

    # Pattern 1: zeta_vn/... trong code blocks
    for m in re.finditer(r"\bzeta_vn(?:/[a-zA-Z0-9_]+)+", text):
        p = m.group(0).replace("/", ".")
        if p.endswith(".py"):
            p = p[:-3]
        # Giữ các package level (ít nhất 2 dots)
        if p.count(".") >= 2:
            pkgs.add(p.rsplit(".", 1)[0])

    # Pattern 2: directory structure listings
    lines = text.split("\n")
    current_base = ""
    for line in lines:
        if line.strip().startswith("zeta_vn/"):
            # Base directory
            current_base = line.strip().rstrip("/").replace("/", ".")
        elif current_base and line.strip().startswith("├──") or line.strip().startswith("└──"):
            # Sub-item
            item = line.split("─")[-1].strip()
            if "/" in item:
                pkg = f"{current_base}.{item.replace('/', '.').rstrip('.py')}"
                if pkg.count(".") >= 2:
                    pkgs.add(pkg.rsplit(".", 1)[0])

    return pkgs


def main() -> int:
    """Generate expectations YAML từ PROJECT_MAP analysis."""
    if not SRC.exists():
        print(f"❌ {SRC} not found. Using fallback PROJECT_MAP.md")
        fallback = Path("PROJECT_MAP.md")
        if fallback.exists():
            text = fallback.read_text(encoding="utf-8", errors="ignore")
        else:
            print("❌ No PROJECT_MAP.md found. Using hardcoded rules only.")
            text = ""
    else:
        text = SRC.read_text(encoding="utf-8", errors="ignore")

    # Parse packages từ PROJECT_MAP
    discovered_pkgs = parse_packages_from_project_map(text)
    print(f"📦 Discovered {len(discovered_pkgs)} packages from PROJECT_MAP")

    # Merge với heuristic rules
    dir_minimal = dict(DIR_RULES)

    # Add discovered packages với minimal structure
    for pkg in discovered_pkgs:
        if pkg not in dir_minimal:
            # Guess minimal files dựa trên package name
            if "api.v1" in pkg:
                dir_minimal[pkg] = ["router.py"]
            elif "adapters" in pkg or "entities" in pkg or "services" in pkg:
                dir_minimal[pkg] = ["__init__.py"]

    required = {k: {"symbols": v} for k, v in REQUIRED_SYMBOLS.items()}

    # Ensure output directory
    OUT.parent.mkdir(parents=True, exist_ok=True)

    # Generate YAML manually (tránh dependency pyyaml)
    def dump_yaml(data: dict) -> str:
        lines = ["version: 1", "required:"]
        for mod, spec in data["required"].items():
            lines.append(f"  {mod}:")
            symbols_str = ", ".join(f'"{s}"' for s in spec["symbols"])
            lines.append(f"    symbols: [{symbols_str}]")

        lines.append("dir_minimal:")
        for pkg, spec in data["dir_minimal"].items():
            lines.append(f"  {pkg}:")
            files_str = ", ".join(f'"{f}"' for f in spec["must_have_files"])
            lines.append(f"    must_have_files: [{files_str}]")

        return "\n".join(lines)

    content = dump_yaml(
        {
            "required": required,
            "dir_minimal": {k: {"must_have_files": v} for k, v in dir_minimal.items()},
        }
    )

    OUT.write_text(content, encoding="utf-8")
    print(f"✅ Generated {OUT}")
    print(f"📊 {len(required)} required modules, {len(dir_minimal)} directory rules")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
