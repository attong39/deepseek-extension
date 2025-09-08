"""Test Memory Normalization module."""

from __future__ import annotations

from uuid import UUID, uuid4

import pytest
from apps.backend.core.domain.entities.memory import MemoryImportance, MemoryType
from apps.backend.core.use_cases.memory.store_memory import (
    _derive_idempotency_key,
    _map_enums,
    _normalize_tags,
    _normalize_text,
)


def test_normalize_text_collapses_whitespace() -> None:
    assert _normalize_text("  Hello\n\tworld   ") == "Hello world"
    assert _normalize_text("\n\nA\t\tB\nC\n") == "A B C"


def test_normalize_tags_lowercase_dedupe_limit() -> None:
    tags = ["Alpha", "beta", "alpha", "  Beta  ", "Gamma"]
    out = _normalize_tags(tags, max_tags=3, max_tag_length=5)
    # order preserved, lowercased, duplicates removed, truncated length, capped count
    assert out == ["alpha", "beta", "gamma"]


def test_map_enums_valid() -> None:
    t, imp = _map_enums("episodic", "high")
    assert t is MemoryType.EPISODIC
    assert imp is MemoryImportance.HIGH


@pytest.mark.parametrize(
    "mt_in,expected",
    [("conversation", MemoryType.EPISODIC), ("chat", MemoryType.EPISODIC)],
)
def test_map_enums_legacy_synonyms(mt_in: str, expected: MemoryType) -> None:
    t, _ = _map_enums("episodic" if mt_in == "episodic" else mt_in, "low")
    assert t is expected


def test_derive_idempotency_key_stable() -> None:
    agent: UUID = uuid4()
    k1 = _derive_idempotency_key(agent, "episodic", "hello")
    k2 = _derive_idempotency_key(agent, "episodic", "hello")
    assert k1 == k2
    k3 = _derive_idempotency_key(agent, "episodic", "hello!")
    assert k3 != k1
import agent
import expected
import imp
import mt_in
import str
import t
