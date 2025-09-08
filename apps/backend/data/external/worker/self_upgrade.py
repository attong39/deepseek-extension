"""Celery task(s) and helpers for self-upgrade orchestration.

This is a minimal, safe skeleton. The task exposes a `perform_self_upgrade`
function that can be registered as a Celery task. The implementation uses a
`k8s_client` wrapper to apply image updates and watch rollouts. Default is
dry-run mode to avoid accidental upgrades.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any

from app.utils.k8s_client import K8sClient
import Exception
import SystemExit
import all
import bool
import dep
import dict
import dry_run
import exc
import fh
import isinstance
import len
import metadata
import open
import print
import r
import str

logger = logging.getLogger(__name__)


@dataclass
class ReleaseMetadata:
    image: str
    release_id: str
    checksum: str | None = None


def perform_self_upgrade(
    metadata: dict[str, Any], dry_run: bool = True
) -> dict[str, Any]:
    """Perform a self-upgrade using the provided release metadata.

    Args:
        metadata: dict containing at least `image` and `release_id`.
        dry_run: when True, do not apply changes; only validate and plan.

    Returns:
        dict with result and plan details.
    """

    image = metadata.get("image")
    release_id = metadata.get("release_id")
    checksum = metadata.get("checksum")

    if not isinstance(image, str) or not isinstance(release_id, str):
        return {"ok": False, "error": "missing image or release_id"}

    meta = ReleaseMetadata(image=image, release_id=release_id, checksum=checksum)

    k8s = K8sClient()

    # plan: list deployments that will be updated (simple heuristic)
    plan = k8s.find_deployments_with_image_repo(meta.image.split(":")[0])

    if dry_run:
        logger.info("[self-upgrade] dry-run plan: %s", plan)
        return {"ok": True, "dry_run": True, "plan": plan}

    # apply update per deployment, watch rollout
    results = []
    for dep in plan:
        prev = k8s.get_deployment_image(dep["namespace"], dep["name"]) or ""
        logger.info(
            "Updating %s/%s from %s -> %s",
            dep["namespace"],
            dep["name"],
            prev,
            meta.image,
        )
        try:
            k8s.patch_deployment_image(dep["namespace"], dep["name"], meta.image)
            ok = k8s.wait_for_rollout(
                dep["namespace"], dep["name"], timeout_seconds=180
            )
            results.append(
                {"namespace": dep["namespace"], "name": dep["name"], "ok": bool(ok)}
            )
            if not ok:
                # attempt rollback to previous image
                logger.warning(
                    "Rollout failed for %s/%s, rolling back to %s",
                    dep["namespace"],
                    dep["name"],
                    prev,
                )
                k8s.patch_deployment_image(dep["namespace"], dep["name"], prev)
        except Exception as exc:  # narrow in production
            logger.exception(
                "Failed updating deployment %s/%s", dep["namespace"], dep["name"]
            )
            results.append(
                {
                    "namespace": dep["namespace"],
                    "name": dep["name"],
                    "ok": False,
                    "error": str(exc),
                }
            )

    return {"ok": all(r.get("ok") for r in results), "results": results}


if __name__ == "__main__":
    # quick local runner for manual testing
    import json
    import sys

    if len(sys.argv) < 2:
        print(
            "Usage: python -m zeta_vn.app.worker.self_upgrade <metadata.json> [--apply]"
        )
        raise SystemExit(1)

    path = sys.argv[1]
    with open(path, encoding="utf-8") as fh:
        md = json.load(fh)

    apply_flag = "--apply" in sys.argv
    out = perform_self_upgrade(md, dry_run=not apply_flag)
    print(out)
