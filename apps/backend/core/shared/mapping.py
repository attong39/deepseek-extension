"""Mapping module."""

from __future__ import annotations

from typing import Protocol, TypeVar, runtime_checkable

S = TypeVar("S")
D = TypeVar("D")


@runtime_checkable
class Mapper(Protocol[S, D]):
    def to_domain(self, src: S) -> D: ...
    def to_dto(self, src: D) -> S: ...
