"""
Batch Controller Module

Orchestrates background job management (Celery/RQ/Arq/etc.) across services/adapters.
Framework-agnostic: usable by API, CLI, WS. No direct DB/HTTP calls.

Author: duy_bg_vn
"""

from __future__ import annotations

import logging
from typing import Any, Protocol
import Exception
import ValueError
import batch
import cron
import dict
import exc
import isinstance
import name
import params
import self
import str

# Use project logger (assumes project-wide logger config)
logger = logging.getLogger("zeta_vn.app.controllers.batch")

class BatchService(Protocol):
    """
    Protocol for batch job service.

    Defines the required interface for batch job services.
    """

    async def enqueue(self, *, name: str, params: dict[str, Any]) -> str:
        """
        Enqueue a background job.

        Args:
            name (str): Job name.
            params (Dict[str, Any]): Job parameters.

        Returns:
            str: Job ID.

        Raises:
            Exception: For service errors.
        """
        ...

    async def schedule_cron(
        self, *, name: str, cron: str, params: dict[str, Any]
    ) -> str:
        """
        Schedule a background job with cron expression.

        Args:
            name (str): Job name.
            cron (str): Cron expression.
            params (Dict[str, Any]): Job parameters.

        Returns:
            str: Job ID.

        Raises:
            Exception: For service errors.
        """
        ...

    async def status(self, job_id: str) -> dict[str, Any]:
        """
        Get status of a background job.

        Args:
            job_id (str): Job ID.

        Returns:
            Dict[str, Any]: Job status.

        Raises:
            Exception: For service errors.
        """
        ...


class BatchController:
    """
    Controller for managing background jobs.

    Typical wiring:
        svc = container.batch_service()
        ctl = BatchController(batch=svc)
    """

    def __init__(self, batch: BatchService) -> None:
        """
        Initialize BatchController.

        Args:
            batch (BatchService): Batch job service instance.

        Raises:
            ValueError: If batch is not provided.
        """
        if batch is None:
            logger.error("Batch service must not be None.")
            raise ValueError("Batch service must not be None.")
        self._batch: BatchService = batch

    async def enqueue_job(self, name: str, params: dict[str, Any]) -> str:
        """
        Enqueue a background job.

        Args:
            name (str): Job name.
            params (Dict[str, Any]): Job parameters.

        Returns:
            str: Job ID.

        Raises:
            ValueError: If input is invalid.
            Exception: For unexpected errors.
        """
        if not isinstance(name, str) or not name:
            logger.error("Invalid job name: %r", name)
            raise ValueError("Job name must be a non-empty string.")
        if not isinstance(params, dict):
            logger.error("Invalid job params: %r", params)
            raise ValueError("Job params must be a dictionary.")

        logger.info("Enqueue job name=%s", name)
        try:
            job_id = await self._batch.enqueue(name=name, params=params)
            logger.info("Job enqueued successfully: job_id=%s", job_id)
            return job_id
        except Exception as exc:
            logger.exception("Failed to enqueue job: %s", exc)
            raise

    async def schedule(self, name: str, cron: str, params: dict[str, Any]) -> str:
        """
        Schedule a background job with cron expression.

        Args:
            name (str): Job name.
            cron (str): Cron expression.
            params (Dict[str, Any]): Job parameters.

        Returns:
            str: Job ID.

        Raises:
            ValueError: If input is invalid.
            Exception: For unexpected errors.
        """
        if not isinstance(name, str) or not name:
            logger.error("Invalid job name: %r", name)
            raise ValueError("Job name must be a non-empty string.")
        if not isinstance(cron, str) or not cron:
            logger.error("Invalid cron expression: %r", cron)
            raise ValueError("Cron must be a non-empty string.")
        if not isinstance(params, dict):
            logger.error("Invalid job params: %r", params)
            raise ValueError("Job params must be a dictionary.")

        logger.info("Schedule job name=%s cron=%s", name, cron)
        try:
            job_id = await self._batch.schedule_cron(name=name, cron=cron, params=params)
            logger.info("Job scheduled successfully: job_id=%s", job_id)
            return job_id
        except Exception as exc:
            logger.exception("Failed to schedule job: %s", exc)
            raise

    async def get_status(self, job_id: str) -> dict[str, Any]:
        """
        Get status of a background job.

        Args:
            job_id (str): Job ID.

        Returns:
            Dict[str, Any]: Job status.

        Raises:
            ValueError: If job_id is invalid.
            Exception: For unexpected errors.
        """
        if not isinstance(job_id, str) or not job_id:
            logger.error("Invalid job_id: %r", job_id)
            raise ValueError("Job ID must be a non-empty string.")

        logger.debug("Get status for job_id=%s", job_id)
        try:
            status = await self._batch.status(job_id)
            logger.info("Job status retrieved: job_id=%s", job_id)
            return status
        except Exception as exc:
            logger.exception("Failed to get job status: %s", exc)
            raise

# End of file
