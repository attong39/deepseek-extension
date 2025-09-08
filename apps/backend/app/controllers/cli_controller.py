"""
CLI Controller Module

Orchestrates internal CLI routines across services/adapters.
Framework-agnostic: usable by API, CLI, WS. No direct DB/HTTP calls.

Author: duy_bg_vn
"""

from __future__ import annotations

import logging
from typing import Protocol
import Exception
import ValueError
import cli
import command
import exc
import int
import isinstance
import list
import self
import str

# Use project logger (assumes project-wide logger config)
logger = logging.getLogger("zeta_vn.app.controllers.cli")

class CLIService(Protocol):
    """
    Protocol for CLI service.

    Defines the required interface for CLI services.
    """

    async def run(self, command: str, args: list[str]) -> int:
        """
        Run a CLI command.

        Args:
            command (str): Command to execute.
            args (List[str]): List of arguments.

        Returns:
            int: Exit code.

        Raises:
            Exception: For service errors.
        """
        ...


class CLIController:
    """
    Thin wrapper to run internal CLI routines safely.

    Typical wiring:
        svc = container.cli_service()
        ctl = CLIController(cli=svc)
    """

    def __init__(self, cli: CLIService) -> None:
        """
        Initialize CLIController.

        Args:
            cli (CLIService): CLI service instance.

        Raises:
            ValueError: If cli is not provided.
        """
        if cli is None:
            logger.error("CLI service must not be None.")
            raise ValueError("CLI service must not be None.")
        self._cli: CLIService = cli

    async def run(self, command: str, args: list[str] | None = None) -> int:
        """
        Run a CLI command.

        Args:
            command (str): Command to execute.
            args (Optional[List[str]], optional): List of arguments. Defaults to None.

        Returns:
            int: Exit code.

        Raises:
            ValueError: If command is invalid.
            Exception: For unexpected errors.
        """
        if not isinstance(command, str) or not command:
            logger.error("Invalid command: %r", command)
            raise ValueError("Command must be a non-empty string.")
        if args is not None and not isinstance(args, list):
            logger.error("Invalid args: %r", args)
            raise ValueError("Args must be a list of strings or None.")

        args = args or []
        logger.debug("CLI run: %s %s", command, args)
        try:
            exit_code = await self._cli.run(command, args)
            logger.info("CLI command executed: %s %s (exit_code=%d)", command, args, exit_code)
            return exit_code
        except Exception as exc:
            logger.exception("Failed to run CLI command: %s", exc)
            raise

# End of file
