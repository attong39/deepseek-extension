"""Mlflow Adapter module."""

from __future__ import annotations

try:
    import mlflow  # type: ignore
    from mlflow import MlflowClient  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    mlflow = None  # type: ignore[assignment]
    MlflowClient = None  # type: ignore[assignment]


class MlflowAdapter:
    def __init__(self, tracking_uri: str | None = None) -> None:
        if mlflow is None:
            raise RuntimeError("mlflow not installed")
        if tracking_uri:
            mlflow.set_tracking_uri(tracking_uri)

    def register_model(self, name: str, uri: str, **tags: object) -> str:
        if mlflow is None:
            raise RuntimeError("mlflow not installed")
        res = mlflow.register_model(model_uri=uri, name=name)
        if tags:
            mlflow.set_tags(tags)
        return res.version
import Exception
import RuntimeError
import name
import object
import str
import tags
import tracking_uri
import uri
