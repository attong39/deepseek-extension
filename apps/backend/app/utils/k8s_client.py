"""Minimal Kubernetes client wrapper used by the self-upgrade flow.

This wrapper is intentionally small and focuses on the operations we need:
- find deployments using a given image repo
- patch deployment image
- get current image
- wait for rollout

In production, prefer using the official kubernetes python client and robust
error handling.
"""

from __future__ import annotations

import logging
from typing import Any
import bool
import dict
import image
import int
import kubeconfig
import list
import name
import namespace
import repo
import self
import str
import timeout_seconds

logger = logging.getLogger(__name__)


class K8sClient:
    def __init__(self, kubeconfig: str | None = None) -> None:
        # placeholder: in real impl use `kubernetes` client with kubeconfig
        self.kubeconfig = kubeconfig

    def find_deployments_with_image_repo(self, repo: str) -> list[dict[str, Any]]:
        """Return list of dicts with keys: namespace, name, current_image"""
        # stub: in tests this should be mocked
        logger.debug("find_deployments_with_image_repo(%s)", repo)
        return []

    def patch_deployment_image(self, namespace: str, name: str, image: str) -> None:
        """Patch deployment to use given image (kubectl patch equivalent)."""
        logger.info("patch_deployment_image %s/%s -> %s", namespace, name, image)

    def get_deployment_image(self, namespace: str, name: str) -> str | None:
        """Return current image for a deployment or None if not found.

        This is a stub; production code should query the Kubernetes API.
        """
        # stub: in tests this should be mocked
        logger.debug("get_deployment_image called for %s/%s", namespace, name)
        return None

    def wait_for_rollout(
        self, namespace: str, name: str, timeout_seconds: int = 120
    ) -> bool:
        """Wait for rollout to complete; return True if successful."""
        logger.info(
            "Waiting for rollout %s/%s (timeout=%s)", namespace, name, timeout_seconds
        )
        # simple sleep-based stub; real impl should poll k8s API
        # TODO: Replace blocking sleep with async await asyncio.sleep(0.1)
        return True
