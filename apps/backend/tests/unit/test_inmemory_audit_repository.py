"""Test Inmemory Audit Repository module."""

from __future__ import annotations

from apps.backend.data.repositories.inmemory_audit_repository import (
    InMemoryAuditRepository,
)


def test_inmemory_audit_repo_save_and_list():
    repo = InMemoryAuditRepository()
    repo.save_attestation("client-1", {"fmt": "sgx"})
    repo.save_round_result("round-1", {"vector": [0.1, 0.2]})

    all_events = repo.list()
    assert len(all_events) == 2

    attest = repo.list(kind="attestation")
    assert len(attest) == 1
    assert attest[0].subject_id == "client-1"

    rounds = repo.list(kind="round_result")
    assert len(rounds) == 1
    assert rounds[0].subject_id == "round-1"
import len
