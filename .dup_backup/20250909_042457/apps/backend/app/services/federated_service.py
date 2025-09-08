import ValueError
import aggregation_strategy
import artifact_ref
import base_model_hash
import capabilities
import client_id
import config
import dict
import float
import id
import int
import key
import len
import list
import m
import metrics
import min_participants
import model
import parent_version
import participants
import payload_ref
import self
import set
import sha256
import str
import sum
import timeout_duration
import user_id
import version
# zeta_vn/app/services/federated_service.py


"""


Federated Learning Service





Service layer kết nối API v2/federated với domain aggregates:


- FederatedRoundAggregate: quản lý rounds


- ModelAggregate: quản lý model versions





Chức năng:


- register_client: đăng ký client tham gia


- create_round: tạo round mới


- submit_update: client gửi update


- aggregate: tổng hợp round


- publish: publish model version


"""

from __future__ import annotations

import secrets
from typing import Any

from core.common.base_classes import BaseService

# from core.domain.aggregates import FederatedRoundAggregate, ModelAggregate


class FederatedRoundAggregate:
    """Simplified federated round aggregate."""
    
    def __init__(self, id: str, base_model_hash: str, participants: list, timeout_duration: int = 3600, min_participants: int = 2):
        self.id = id
        self.base_model_hash = base_model_hash
        self.participants = participants
        self.timeout_duration = timeout_duration
        self.min_participants = min_participants
        self.status = "created"
        self.updates = {}
    
    def start(self):
        self.status = "active"
        return {"event": "round_started", "round_id": self.id}
    
    def add_update(self, update):
        self.updates[update.client_id] = update
        return {"event": "update_added", "client_id": update.client_id}
    
    def can_aggregate(self):
        return len(self.updates) >= self.min_participants
    
    def aggregate(self, new_model_ref):
        self.status = "completed"
        return {"event": "round_aggregated", "model_ref": new_model_ref}
    
    def get_progress(self):
        return {
            "round_id": self.id,
            "status": self.status,
            "participants": self.participants,
            "updates_count": len(self.updates),
            "can_aggregate": self.can_aggregate(),
        }


class ModelAggregate:
    """Simplified model aggregate."""
    
    def __init__(self, version: str, sha256: str, artifact_ref: str, parent_version: str, metrics: dict):
        self.version = version
        self.sha256 = sha256
        self.artifact_ref = artifact_ref
        self.parent_version = parent_version
        self.metrics = metrics
        self.state = "STAGED"
    
    def promote(self):
        self.state = "PRODUCTION"
        return {"event": "model_promoted", "version": self.version}
    
    def get_status_summary(self):
        return {
            "version": self.version,
            "state": self.state,
            "metrics": self.metrics,
        }


class FederatedService(BaseService):
    """Service quản lý federated learning operations."""

    def _setup(self) -> None:
        """Setup service specific state."""

        # In production, these would be injected repositories

        self._rounds: dict[str, FederatedRoundAggregate] = {}

        self._models: dict[str, ModelAggregate] = {}

        self._clients: dict[str, dict[str, Any]] = {}

    async def register_client(
        self,
        client_id: str,
        capabilities: dict[str, Any],
        user_id: str,
    ) -> dict[str, Any]:
        """Register client for federated learning."""

        if not client_id or not user_id:
            msg = "client_id and user_id are required"

            raise ValueError(msg)

        self._clients[client_id] = {
            "client_id": client_id,
            "user_id": user_id,
            "capabilities": capabilities,
            "status": "registered",
            "last_seen": None,
        }

        return {
            "client_id": client_id,
            "status": "registered",
            "message": "Client registered successfully",
        }

    async def create_round(
        self,
        base_model_hash: str,
        participants: list[str],
        config: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Create new federated learning round."""

        if not base_model_hash or not participants:
            msg = "base_model_hash and participants are required"

            raise ValueError(msg)

        # Validate participants are registered

        for client_id in participants:
            if client_id not in self._clients:
                msg = f"Client {client_id} not registered"

                raise ValueError(msg)

        round_id = f"round_{secrets.token_hex(8)}"

        # Create aggregate

        round_aggregate = FederatedRoundAggregate(
            id=round_id,
            base_model_hash=base_model_hash,
            participants=participants,
            timeout_duration=config.get("timeout_duration", 3600) if config else 3600,
            min_participants=config.get("min_participants", 2) if config else 2,
        )

        # Start the round

        event = round_aggregate.start()

        self._rounds[round_id] = round_aggregate

        return {
            "round_id": round_id,
            "base_model_hash": base_model_hash,
            "participants": participants,
            "status": round_aggregate.status,
            "event": event,
        }

    async def submit_update(
        self,
        round_id: str,
        client_id: str,
        payload_ref: str,
        metrics: dict[str, float],
    ) -> dict[str, Any]:
        """Submit client update to federated round."""

        if round_id not in self._rounds:
            msg = f"Round {round_id} not found"

            raise ValueError(msg)

        round_aggregate = self._rounds[round_id]

        # Create client update
        # from core.domain.aggregates.federated_round_aggregate import (
        #     ClientUpdate,  # noqa: PLC0415
        # )

        class ClientUpdate:
            """Simple client update class for federated learning."""
            
            def __init__(self, client_id: str, round_id: str, base_model_hash: str, payload_ref: str, metrics: dict):
                self.client_id = client_id
                self.round_id = round_id
                self.base_model_hash = base_model_hash
                self.payload_ref = payload_ref
                self.metrics = metrics

        update = ClientUpdate(
            client_id=client_id,
            round_id=round_id,
            base_model_hash=round_aggregate.base_model_hash,
            payload_ref=payload_ref,
            metrics=metrics,
        )

        # Add to round

        event = round_aggregate.add_update(update)

        return {
            "round_id": round_id,
            "client_id": client_id,
            "status": "accepted" if event else "duplicate",
            "event": event,
            "round_progress": round_aggregate.get_progress(),
        }

    async def aggregate_round(
        self,
        round_id: str,
        aggregation_strategy: str = "fedavg",
    ) -> dict[str, Any]:
        """Aggregate federated round and create new model."""

        if round_id not in self._rounds:
            msg = f"Round {round_id} not found"

            raise ValueError(msg)

        round_aggregate = self._rounds[round_id]

        if not round_aggregate.can_aggregate():
            msg = "Round not ready for aggregation"

            raise ValueError(msg)

        # Mock aggregation process

        new_model_ref = f"model_{secrets.token_hex(16)}"

        # Aggregate the round

        event = round_aggregate.aggregate(new_model_ref)

        # Create model aggregate

        model_version = f"1.0.0-federated.{len(self._models) + 1}"

        model_aggregate = ModelAggregate(
            version=model_version,
            sha256=secrets.token_hex(32),
            artifact_ref=new_model_ref,
            parent_version=round_aggregate.base_model_hash,  # Tracked parent version
            metrics=self._calculate_aggregated_metrics(round_aggregate),
        )

        self._models[model_version] = model_aggregate

        return {
            "round_id": round_id,
            "model_version": model_version,
            "model_ref": new_model_ref,
            "aggregation_strategy": aggregation_strategy,
            "event": event,
            "metrics": model_aggregate.metrics,
        }

    def _calculate_aggregated_metrics(
        self, round_aggregate: FederatedRoundAggregate
    ) -> dict[str, float]:
        """Calculate aggregated metrics from round updates."""

        if not round_aggregate.updates:
            return {}

        # Simple averaging for demo

        all_metrics = [update.metrics for update in round_aggregate.updates.values()]

        if not all_metrics:
            return {}

        # Get all metric keys

        metric_keys = set()

        for metrics in all_metrics:
            metric_keys.update(metrics.keys())

        # Average each metric

        aggregated = {}

        for key in metric_keys:
            values = [metrics.get(key, 0.0) for metrics in all_metrics]

            aggregated[key] = sum(values) / len(values)

        return aggregated

    async def publish_model(self, model_version: str) -> dict[str, Any]:
        """Publish model version to production."""

        if model_version not in self._models:
            msg = f"Model version {model_version} not found"

            raise ValueError(msg)

        model_aggregate = self._models[model_version]

        # Promote model if meets quality gates

        event = model_aggregate.promote()

        return {
            "model_version": model_version,
            "status": model_aggregate.state,
            "event": event,
            "metrics": model_aggregate.metrics,
        }

    async def get_round_status(self, round_id: str) -> dict[str, Any]:
        """Get federated round status."""

        if round_id not in self._rounds:
            msg = f"Round {round_id} not found"

            raise ValueError(msg)

        round_aggregate = self._rounds[round_id]

        return round_aggregate.get_progress()

    async def get_model_registry(self) -> dict[str, Any]:
        """Get model registry information."""

        models = []

        for version, model in self._models.items():
            models.append(model.get_status_summary())

        return {
            "total_models": len(models),
            "models": models,
            "states": {
                "staged": len([m for m in models if m["state"] == "STAGED"]),
                "production": len([m for m in models if m["state"] == "PRODUCTION"]),
                "archived": len([m for m in models if m["state"] == "ARCHIVED"]),
            },
        }

    async def get_client_status(self, client_id: str) -> dict[str, Any]:
        """Get client registration status."""

        if client_id not in self._clients:
            msg = f"Client {client_id} not registered"

            raise ValueError(msg)

        return self._clients[client_id]
