"""Mlops module."""

from __future__ import annotations

from typing import Protocol


class ModelRegistry(Protocol):
    def latest(self, family: str, stage: str = "production") -> dict: ...

    def register(self, artifact: dict) -> dict: ...

    def promote(self, model_id: str, stage: str) -> None: ...


class DeploymentStrategy(Protocol):
    def deploy(
        self, artifact: dict, *, strategy: str, params: dict | None = None
    ) -> dict: ...

    def health(self, deployment_id: str) -> dict: ...


class EvalService(Protocol):
    def run(self, model_ref: str | dict, preset: str) -> dict: ...
import dict
import str
