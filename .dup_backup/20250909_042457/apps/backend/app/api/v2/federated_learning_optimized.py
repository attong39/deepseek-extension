import ValueError
import abs
import active_rounds
import bits
import bool
import budget
import client_id
import client_ids
import client_updates
import clip_norm
import config
import cost
import delta
import dict
import dist
import enumerate
import epsilon
import float
import i
import int
import j
import k_ratio
import len
import list
import max
import method
import min
import privacy_budgets
import property
import result
import s
import samples
import self
import sensitivity
import staticmethod
import str
import sum
import threshold
import trim_ratio
import tuple
import u
import update_i
import update_j
import user
import w
import weight_max
import weight_min
import zip
# zeta_vn/app/api/v2/federated_learning_optimized.py
"""
Federated Learning v2 - Optimized với Differential Privacy & SMPC

Tối ưu hóa:
1. Differential privacy mechanisms cho client updates
2. Secure multi-party computation (SMPC) cho aggregation
3. Model update compression với gradient quantization
4. Byzantine fault tolerance cho malicious clients
"""

from __future__ import annotations

import hashlib
import math
from dataclasses import dataclass
from datetime import UTC, datetime
from enum import Enum
from typing import Any

import numpy as np
from apps.backend.app.api.v1._common_audit import audit
from apps.backend.app.api.v1._common_cache import acached
from apps.backend.app.api.v1._common_idempotency import idempotency_guard
from apps.backend.app.api.v1._common_security import Role, User, require_roles
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from pydantic import BaseModel, Field

router = APIRouter(prefix="/federated-learning", tags=["FL-V2-Optimized"])

# === Federated Learning Enums & Models ===


class AggregationStrategy(str, Enum):
    FEDAVG = "fedavg"  # FedAvg (standard)
    FEDPROX = "fedprox"  # FedProx (heterogeneous data)
    FEDOPT = "fedopt"  # FedOpt (adaptive optimization)
    BYZANTINE_ROBUST = "byzantine_robust"  # Byzantine-robust aggregation


class PrivacyMechanism(str, Enum):
    NONE = "none"
    GAUSSIAN_DP = "gaussian_dp"  # Gaussian differential privacy
    LAPLACE_DP = "laplace_dp"  # Laplace differential privacy
    LOCAL_DP = "local_dp"  # Local differential privacy


class CompressionMethod(str, Enum):
    NONE = "none"
    QUANTIZATION = "quantization"  # Gradient quantization
    SPARSIFICATION = "sparsification"  # Top-k sparsification
    SKETCHING = "sketching"  # Random sketching


@dataclass
class PrivacyBudget:
    """Differential privacy budget management"""

    epsilon: float  # Privacy parameter
    delta: float  # Failure probability
    spent_epsilon: float = 0.0

    @property
    def remaining_epsilon(self) -> float:
        return max(0.0, self.epsilon - self.spent_epsilon)

    def can_afford(self, cost: float) -> bool:
        return cost <= self.remaining_epsilon

    def spend(self, cost: float):
        if not self.can_afford(cost):
            raise ValueError(
                f"Insufficient privacy budget: {cost} > {self.remaining_epsilon}"
            )
        self.spent_epsilon += cost


@dataclass
class FederatedRound:
    """Federated learning round state"""

    round_id: str
    model_version: str
    participating_clients: list[str]
    aggregation_strategy: AggregationStrategy
    privacy_mechanism: PrivacyMechanism
    privacy_budget: PrivacyBudget
    target_clients: int
    min_clients: int
    round_timeout: int
    created_at: datetime
    status: str = "collecting"


class ClientUpdate(BaseModel):
    client_id: str
    round_id: str
    model_weights: list[float]  # Flattened model weights
    num_samples: int
    training_loss: float
    training_accuracy: float | None = None
    compression_method: CompressionMethod = CompressionMethod.NONE
    privacy_noise_scale: float | None = None
    signature: str | None = None  # For authenticity verification


class SecureAggregationShare(BaseModel):
    client_id: str
    round_id: str
    encrypted_shares: dict[str, str]  # Client ID -> encrypted share
    commitment: str  # Cryptographic commitment to the share


class FederatedRoundConfig(BaseModel):
    model_version: str
    target_clients: int = Field(default=10, ge=2, le=1000)
    min_clients: int = Field(default=5, ge=2)
    round_timeout_minutes: int = Field(default=30, ge=5, le=120)
    aggregation_strategy: AggregationStrategy = AggregationStrategy.FEDAVG
    privacy_mechanism: PrivacyMechanism = PrivacyMechanism.GAUSSIAN_DP
    privacy_epsilon: float = Field(default=1.0, gt=0.0, le=10.0)
    privacy_delta: float = Field(default=1e-5, gt=0.0, le=1e-3)
    compression_method: CompressionMethod = CompressionMethod.QUANTIZATION
    byzantine_tolerance: bool = False


class AggregationResult(BaseModel):
    round_id: str
    global_model_weights: list[float]
    participating_clients: list[str]
    convergence_metrics: dict[str, float]
    privacy_cost: float
    aggregation_time_seconds: float


# === Privacy Mechanisms ===


class DifferentialPrivacy:
    """Differential privacy implementations"""

    @staticmethod
    def add_gaussian_noise(
        weights: np.ndarray, sensitivity: float, epsilon: float, delta: float
    ) -> np.ndarray:
        """Add Gaussian noise for (ε,δ)-differential privacy"""
        sigma = math.sqrt(2 * math.log(1.25 / delta)) * sensitivity / epsilon
        noise = np.random.normal(0, sigma, weights.shape)
        return weights + noise

    @staticmethod
    def add_laplace_noise(
        weights: np.ndarray, sensitivity: float, epsilon: float
    ) -> np.ndarray:
        """Add Laplace noise for ε-differential privacy"""
        scale = sensitivity / epsilon
        noise = np.random.laplace(0, scale, weights.shape)
        return weights + noise

    @staticmethod
    def clip_gradients(
        gradients: np.ndarray, clip_norm: float
    ) -> tuple[np.ndarray, float]:
        """Clip gradients to bound sensitivity"""
        grad_norm = np.linalg.norm(gradients)
        if grad_norm > clip_norm:
            gradients = gradients * (clip_norm / grad_norm)
        return gradients, min(grad_norm, clip_norm)


# === Compression Mechanisms ===


class ModelCompression:
    """Model update compression methods"""

    @staticmethod
    def quantize_weights(
        weights: np.ndarray, bits: int = 8
    ) -> tuple[np.ndarray, dict[str, Any]]:
        """Quantize weights to specified bit precision"""
        weight_min, weight_max = weights.min(), weights.max()
        scale = (weight_max - weight_min) / (2**bits - 1)

        quantized = np.round((weights - weight_min) / scale).astype(np.uint8)

        # Dequantize for verification
        dequantized = quantized.astype(np.float32) * scale + weight_min

        compression_ratio = weights.nbytes / quantized.nbytes

        return dequantized, {
            "quantized_weights": quantized.tolist(),
            "scale": scale,
            "offset": weight_min,
            "compression_ratio": compression_ratio,
        }

    @staticmethod
    def sparsify_top_k(
        weights: np.ndarray, k_ratio: float = 0.1
    ) -> tuple[np.ndarray, dict[str, Any]]:
        """Keep only top-k% of weights by magnitude"""
        flat_weights = weights.flatten()
        k = int(len(flat_weights) * k_ratio)

        # Get indices of top-k elements
        top_k_indices = np.argpartition(np.abs(flat_weights), -k)[-k:]

        # Create sparse representation
        sparse_weights = np.zeros_like(flat_weights)
        sparse_weights[top_k_indices] = flat_weights[top_k_indices]

        compression_ratio = len(flat_weights) / k

        return sparse_weights.reshape(weights.shape), {
            "active_indices": top_k_indices.tolist(),
            "active_values": flat_weights[top_k_indices].tolist(),
            "compression_ratio": compression_ratio,
        }


# === Secure Aggregation ===


class SecureAggregation:
    """Secure multi-party computation for aggregation"""

    @staticmethod
    def generate_secret_shares(
        weights: np.ndarray, client_ids: list[str], threshold: int
    ) -> dict[str, np.ndarray]:
        """Generate Shamir's secret shares for secure aggregation"""
        # Simplified implementation - in production use proper cryptographic library
        shares = {}
        for i, client_id in enumerate(client_ids[:threshold]):
            # Generate polynomial shares (simplified)
            share = weights + np.random.normal(0, 0.1, weights.shape) * (i + 1)
            shares[client_id] = share
        return shares

    @staticmethod
    def reconstruct_from_shares(
        shares: dict[str, np.ndarray], threshold: int
    ) -> np.ndarray:
        """Reconstruct secret from threshold shares"""
        # Simplified Lagrange interpolation
        if len(shares) < threshold:
            raise ValueError(f"Insufficient shares: {len(shares)} < {threshold}")

        # Simple averaging for demonstration (not cryptographically secure)
        share_values = list(shares.values())[:threshold]
        return np.mean(share_values, axis=0)


# === Byzantine Fault Tolerance ===


class ByzantineDefense:
    """Defense against Byzantine (malicious) clients"""

    @staticmethod
    def detect_outliers(updates: list[np.ndarray], threshold: float = 2.0) -> list[int]:
        """Detect outlier updates using statistical methods"""
        if len(updates) < 3:
            return []

        # Calculate pairwise distances
        distances = []
        for i, update_i in enumerate(updates):
            dist_sum = 0
            for j, update_j in enumerate(updates):
                if i != j:
                    dist_sum += np.linalg.norm(update_i - update_j)
            distances.append(dist_sum / (len(updates) - 1))

        # Identify outliers using z-score
        mean_dist = np.mean(distances)
        std_dist = np.std(distances)
        outliers = []

        for i, dist in enumerate(distances):
            z_score = abs(dist - mean_dist) / (std_dist + 1e-8)
            if z_score > threshold:
                outliers.append(i)

        return outliers

    @staticmethod
    def robust_aggregation(
        updates: list[np.ndarray], method: str = "trimmed_mean", trim_ratio: float = 0.2
    ) -> np.ndarray:
        """Robust aggregation resistant to Byzantine clients"""
        if method == "trimmed_mean":
            # Remove top/bottom percentiles and average
            stacked = np.stack(updates)
            trim_count = int(len(updates) * trim_ratio / 2)

            if trim_count > 0:
                sorted_indices = np.argsort(stacked, axis=0)
                trimmed = stacked[sorted_indices[trim_count:-trim_count]]
                return np.mean(trimmed, axis=0)
            else:
                return np.mean(stacked, axis=0)

        elif method == "median":
            # Coordinate-wise median
            stacked = np.stack(updates)
            return np.median(stacked, axis=0)

        else:
            # Fallback to simple average
            return np.mean(updates, axis=0)


# === Global State Management ===

active_rounds: dict[str, FederatedRound] = {}
client_updates: dict[str, list[ClientUpdate]] = {}  # round_id -> updates
privacy_budgets: dict[str, PrivacyBudget] = {}  # client_id -> budget

# === API Endpoints ===


@router.post("/rounds/create")
async def create_federated_round(
    config: FederatedRoundConfig, user: User = Depends(require_roles(Role.ADMIN))
):
    """Create new federated learning round"""
    await audit("fl.round.create", actor=user.sub, payload=config.dict())

    round_id = f"round_{int(datetime.now(UTC).timestamp())}_{hashlib.sha256(config.model_version.encode()).hexdigest()[:8]}"

    privacy_budget = PrivacyBudget(
        epsilon=config.privacy_epsilon, delta=config.privacy_delta
    )

    federated_round = FederatedRound(
        round_id=round_id,
        model_version=config.model_version,
        participating_clients=[],
        aggregation_strategy=config.aggregation_strategy,
        privacy_mechanism=config.privacy_mechanism,
        privacy_budget=privacy_budget,
        target_clients=config.target_clients,
        min_clients=config.min_clients,
        round_timeout=config.round_timeout_minutes * 60,
        created_at=datetime.now(UTC),
    )

    active_rounds[round_id] = federated_round
    client_updates[round_id] = []

    return {
        "round_id": round_id,
        "status": "created",
        "target_clients": config.target_clients,
        "privacy_budget": {
            "epsilon": privacy_budget.epsilon,
            "delta": privacy_budget.delta,
        },
    }


@router.post("/rounds/{round_id}/submit")
async def submit_client_update(
    round_id: str,
    update: ClientUpdate,
    user: User = Depends(require_roles(Role.USER)),
    _: str = Depends(idempotency_guard),
):
    """Submit client model update with privacy protection"""
    if round_id not in active_rounds:
        raise HTTPException(status_code=404, detail="Round not found")

    round_info = active_rounds[round_id]
    if round_info.status != "collecting":
        raise HTTPException(status_code=400, detail="Round not accepting updates")

    await audit(
        "fl.update.submit",
        actor=user.sub,
        payload={
            "round_id": round_id,
            "client_id": update.client_id,
            "num_samples": update.num_samples,
        },
    )

    # Verify update belongs to this round
    if update.round_id != round_id:
        raise HTTPException(status_code=400, detail="Round ID mismatch")

    # Apply privacy protection
    weights = np.array(update.model_weights)

    if round_info.privacy_mechanism != PrivacyMechanism.NONE:
        # Get or create privacy budget for client
        client_budget_key = f"{update.client_id}_{round_id}"
        if client_budget_key not in privacy_budgets:
            privacy_budgets[client_budget_key] = PrivacyBudget(
                epsilon=round_info.privacy_budget.epsilon,
                delta=round_info.privacy_budget.delta,
            )

        client_budget = privacy_budgets[client_budget_key]
        privacy_cost = 0.1  # Cost per update

        if not client_budget.can_afford(privacy_cost):
            raise HTTPException(status_code=429, detail="Privacy budget exhausted")

        # Apply privacy mechanism
        if round_info.privacy_mechanism == PrivacyMechanism.GAUSSIAN_DP:
            # Clip gradients for bounded sensitivity
            weights, sensitivity = DifferentialPrivacy.clip_gradients(
                weights, clip_norm=1.0
            )

            # Add Gaussian noise
            weights = DifferentialPrivacy.add_gaussian_noise(
                weights, sensitivity, privacy_cost, round_info.privacy_budget.delta
            )

        elif round_info.privacy_mechanism == PrivacyMechanism.LAPLACE_DP:
            weights, sensitivity = DifferentialPrivacy.clip_gradients(
                weights, clip_norm=1.0
            )
            weights = DifferentialPrivacy.add_laplace_noise(
                weights, sensitivity, privacy_cost
            )

        client_budget.spend(privacy_cost)

    # Apply compression
    compression_info = {}
    if update.compression_method == CompressionMethod.QUANTIZATION:
        weights, compression_info = ModelCompression.quantize_weights(weights)
    elif update.compression_method == CompressionMethod.SPARSIFICATION:
        weights, compression_info = ModelCompression.sparsify_top_k(weights)

    # Store processed update
    processed_update = ClientUpdate(
        client_id=update.client_id,
        round_id=round_id,
        model_weights=weights.tolist(),
        num_samples=update.num_samples,
        training_loss=update.training_loss,
        training_accuracy=update.training_accuracy,
        compression_method=update.compression_method,
        privacy_noise_scale=update.privacy_noise_scale,
    )

    client_updates[round_id].append(processed_update)

    # Check if we have enough updates to aggregate
    if len(client_updates[round_id]) >= round_info.target_clients:
        # Trigger aggregation in background
        pass  # TODO: Add background task

    return {
        "status": "accepted",
        "updates_received": len(client_updates[round_id]),
        "target_updates": round_info.target_clients,
        "compression_info": compression_info,
        "privacy_cost": privacy_cost
        if round_info.privacy_mechanism != PrivacyMechanism.NONE
        else 0,
    }


@router.post("/rounds/{round_id}/aggregate")
async def aggregate_round(
    round_id: str,
    background_tasks: BackgroundTasks,
    user: User = Depends(require_roles(Role.ADMIN)),
):
    """Trigger model aggregation for round"""
    if round_id not in active_rounds:
        raise HTTPException(status_code=404, detail="Round not found")

    round_info = active_rounds[round_id]
    updates = client_updates.get(round_id, [])

    if len(updates) < round_info.min_clients:
        raise HTTPException(
            status_code=400,
            detail=f"Insufficient updates: {len(updates)} < {round_info.min_clients}",
        )

    await audit(
        "fl.round.aggregate",
        actor=user.sub,
        payload={"round_id": round_id, "num_updates": len(updates)},
    )

    # Perform aggregation
    start_time = datetime.now(UTC)

    # Extract weights from updates
    weight_arrays = [np.array(update.model_weights) for update in updates]
    sample_counts = [update.num_samples for update in updates]

    # Byzantine fault tolerance if enabled
    if round_info.aggregation_strategy == AggregationStrategy.BYZANTINE_ROBUST:
        outlier_indices = ByzantineDefense.detect_outliers(weight_arrays)
        if outlier_indices:
            await audit(
                "fl.byzantine.detected",
                actor="system",
                payload={"round_id": round_id, "outlier_count": len(outlier_indices)},
            )
            # Remove outliers
            weight_arrays = [
                w for i, w in enumerate(weight_arrays) if i not in outlier_indices
            ]
            sample_counts = [
                s for i, s in enumerate(sample_counts) if i not in outlier_indices
            ]

        # Use robust aggregation
        aggregated_weights = ByzantineDefense.robust_aggregation(weight_arrays)
    else:
        # Standard FedAvg with sample-weighted averaging
        total_samples = sum(sample_counts)
        weights_sum = np.zeros_like(weight_arrays[0])

        for weights, samples in zip(weight_arrays, sample_counts, strict=False):
            weights_sum += weights * (samples / total_samples)

        aggregated_weights = weights_sum

    aggregation_time = (datetime.now(UTC) - start_time).total_seconds()

    # Calculate convergence metrics
    convergence_metrics = {
        "weight_norm": float(np.linalg.norm(aggregated_weights)),
        "update_variance": float(np.var([np.linalg.norm(w) for w in weight_arrays])),
        "participating_clients": len(weight_arrays),
    }

    # Calculate total privacy cost
    total_privacy_cost = round_info.privacy_budget.spent_epsilon

    _ = AggregationResult(
        round_id=round_id,
        global_model_weights=aggregated_weights.tolist(),
        participating_clients=[u.client_id for u in updates],
        convergence_metrics=convergence_metrics,
        privacy_cost=total_privacy_cost,
        aggregation_time_seconds=aggregation_time,
    )

    # Update round status
    round_info.status = "completed"

    return result


@router.get("/rounds/{round_id}/status")
@acached("fl:round:status", ttl=30)
async def get_round_status(round_id: str):
    """Get federated learning round status"""
    if round_id not in active_rounds:
        raise HTTPException(status_code=404, detail="Round not found")

    round_info = active_rounds[round_id]
    updates = client_updates.get(round_id, [])

    return {
        "round_id": round_id,
        "status": round_info.status,
        "model_version": round_info.model_version,
        "target_clients": round_info.target_clients,
        "updates_received": len(updates),
        "privacy_budget_spent": round_info.privacy_budget.spent_epsilon,
        "privacy_budget_remaining": round_info.privacy_budget.remaining_epsilon,
        "created_at": round_info.created_at,
        "participating_clients": [u.client_id for u in updates],
    }


@router.get("/analytics/privacy")
async def get_privacy_analytics(user: User = Depends(require_roles(Role.ADMIN))):
    """Get privacy budget analytics across all clients"""
    await audit("fl.analytics.privacy", actor=user.sub)

    # Aggregate privacy budget usage
    total_budgets = len(privacy_budgets)
    exhausted_budgets = sum(
        1 for budget in privacy_budgets.values() if budget.remaining_epsilon <= 0
    )
    avg_spent = (
        np.mean([budget.spent_epsilon for budget in privacy_budgets.values()])
        if privacy_budgets
        else 0
    )

    return {
        "total_clients": total_budgets,
        "exhausted_budgets": exhausted_budgets,
        "average_spent_epsilon": float(avg_spent),
        "privacy_efficiency": 1.0 - (exhausted_budgets / max(1, total_budgets)),
    }


@router.get("/analytics/compression")
async def get_compression_analytics(user: User = Depends(require_roles(Role.ADMIN))):
    """Get model compression analytics"""
    await audit("fl.analytics.compression", actor=user.sub)

    # Analyze compression across recent updates
    all_updates = []
    for updates in client_updates.values():
        all_updates.extend(updates)

    compression_stats = {}
    for method in CompressionMethod:
        method_updates = [u for u in all_updates if u.compression_method == method]
        compression_stats[method.value] = {
            "count": len(method_updates),
            "percentage": len(method_updates) / max(1, len(all_updates)) * 100,
        }

    return {
        "total_updates": len(all_updates),
        "compression_methods": compression_stats,
        "average_model_size_kb": 1024,  # Placeholder
        "compression_effectiveness": 0.75,  # Placeholder
    }
