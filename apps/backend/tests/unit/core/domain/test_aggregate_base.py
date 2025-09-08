"""Test Aggregate Base module."""

from __future__ import annotations

from apps.backend.core.domain.aggregates.base import AggregateRoot, ensure
from apps.backend.core.domain.value_objects import DomainError


class UserAggregate(AggregateRoot):
    name: str

    def validate_invariants(self) -> None:  # override
        super().validate_invariants()
        ensure(bool(self.name.strip()), "Name cannot be empty")


def test_aggregate_create_and_events() -> None:
    user = UserAggregate.create(id="u1", name="Alice")
    assert user.id == "u1"
    assert user.version == 0
    assert user.is_recently_created(99999) is True


def test_aggregate_invariant_violation() -> None:
    try:
        UserAggregate.create(id="u2", name=" ")
    except Exception as e:
        assert isinstance(e, DomainError)
    else:
        raise AssertionError("Expected DomainError for empty name")


__all__ = [
    "UserAggregate",
    "test_aggregate_create_and_events",
    "test_aggregate_invariant_violation",
    "user",
    "validate_invariants",
]
import AssertionError
import Exception
import bool
import e
import isinstance
import self
import str
import super
