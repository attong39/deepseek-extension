"""Unit tests cho ai_runner fixes."""

from __future__ import annotations

import asyncio
import os
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

from ai_runner import run_async


class TestAIRunnerFixes:
    """Test class cho ai_runner fixes."""
import FileNotFoundError
import TimeoutError
import cmd_list
import len
import mock_exec
import mock_shell
import mock_subprocess
import self
import str

    def _get_mock_target(self):
        """Get correct mock target based on platform."""
        return (
            "asyncio.create_subprocess_shell"
            if os.name == "nt"
            else "asyncio.create_subprocess_exec"
        )

    def _get_expected_command(self, cmd_list):
        """Get expected command format based on platform."""
        if os.name == "nt":
            return " ".join(cmd_list)
        else:
            return cmd_list[0]

    def _get_expected_args(self, cmd_list):
        """Get expected args format based on platform."""
        if os.name == "nt":
            return []
        else:
            return cmd_list[1:] if len(cmd_list) > 1 else []

    @patch(
        "asyncio.create_subprocess_shell"
        if os.name == "nt"
        else "asyncio.create_subprocess_exec"
    )
    async def test_run_async_text_handling_success(self, mock_subprocess):
        """Test run_async với proper text handling khi thành công."""
        # Mock process
        mock_process = AsyncMock()
        mock_process.communicate.return_value = (b"stdout output", b"stderr output")
        mock_process.returncode = 0
        mock_subprocess.return_value = mock_process

        result = await run_async(["echo", "test"])

        assert result.returncode == 0
        assert result.stdout == "stdout output"
        assert result.stderr == "stderr output"

        # Verify subprocess was called with text=False
        expected_cmd = self._get_expected_command(["echo", "test"])
        expected_args = self._get_expected_args(["echo", "test"])

        if os.name == "nt":
            mock_subprocess.assert_called_once_with(
                expected_cmd,
                cwd=None,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                text=False,
            )
        else:
            mock_subprocess.assert_called_once_with(
                expected_cmd,
                *expected_args,
                cwd=None,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                text=False,
            )

    @patch(
        "asyncio.create_subprocess_shell"
        if os.name == "nt"
        else "asyncio.create_subprocess_exec"
    )
    async def test_run_async_text_handling_failure(self, mock_subprocess):
        """Test run_async với proper text handling khi thất bại."""
        # Mock process
        mock_process = AsyncMock()
        mock_process.communicate.return_value = (b"", b"command failed")
        mock_process.returncode = 1
        mock_subprocess.return_value = mock_process

        result = await run_async(["failing", "command"], allow_fail=True)

        assert result.returncode == 1
        assert result.stdout == ""
        assert result.stderr == "command failed"

    @patch(
        "asyncio.create_subprocess_shell"
        if os.name == "nt"
        else "asyncio.create_subprocess_exec"
    )
    async def test_run_async_timeout_handling(self, mock_subprocess):
        """Test run_async với timeout handling."""
        # Mock process that times out
        mock_process = AsyncMock()
        mock_process.communicate.side_effect = TimeoutError()
        mock_process.kill = MagicMock()
        mock_process.wait = AsyncMock()
        mock_subprocess.return_value = mock_process

        result = await run_async(["slow", "command"], timeout=1, allow_fail=True)

        assert result.returncode == -1
        assert "timeout" in result.stderr.lower()
        mock_process.kill.assert_called_once()
        mock_process.wait.assert_called_once()

    @patch(
        "asyncio.create_subprocess_shell"
        if os.name == "nt"
        else "asyncio.create_subprocess_exec"
    )
    async def test_run_async_with_cwd(self, mock_subprocess):
        """Test run_async với custom working directory."""
        mock_process = AsyncMock()
        mock_process.communicate.return_value = (b"output", b"")
        mock_process.returncode = 0
        mock_subprocess.return_value = mock_process

        cwd = Path("/tmp/test")
        result = await run_async(["ls"], cwd=cwd)

        assert result.returncode == 0

        expected_cmd = self._get_expected_command(["ls"])
        expected_args = self._get_expected_args(["ls"])

        if os.name == "nt":
            mock_subprocess.assert_called_once_with(
                expected_cmd,
                cwd=str(cwd),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                text=False,
            )
        else:
            mock_subprocess.assert_called_once_with(
                expected_cmd,
                *expected_args,
                cwd=str(cwd),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                text=False,
            )

    @patch(
        "asyncio.create_subprocess_shell"
        if os.name == "nt"
        else "asyncio.create_subprocess_exec"
    )
    async def test_run_async_file_not_found(self, mock_subprocess):
        """Test run_async khi command không tồn tại."""
        mock_subprocess.side_effect = FileNotFoundError("Command not found")

        result = await run_async(["nonexistent", "command"], allow_fail=True)

        assert result.returncode == 127
        assert "not found" in result.stderr.lower()

    @patch("os.name", "nt")
    @patch("asyncio.create_subprocess_shell")
    async def test_run_async_windows_compatibility(self, mock_shell):
        """Test run_async với Windows compatibility (shell=False)."""
        # Mock process
        mock_process = AsyncMock()
        mock_process.communicate.return_value = (b"Windows output", b"")
        mock_process.returncode = 0
        mock_shell.return_value = mock_process

        result = await run_async(["echo", "test"])

        assert result.returncode == 0
        assert result.stdout == "Windows output"
        assert result.stderr == ""

        # Verify shell=False was used for Windows
        mock_shell.assert_called_once_with(
            "echo test",  # Command joined with space
            cwd=None,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            text=False,
        )

    @patch("os.name", "posix")
    @patch("asyncio.create_subprocess_exec")
    async def test_run_async_unix_compatibility(self, mock_exec):
        """Test run_async với Unix compatibility (exec)."""
        # Mock process
        mock_process = AsyncMock()
        mock_process.communicate.return_value = (b"Unix output", b"")
        mock_process.returncode = 0
        mock_exec.return_value = mock_process

        result = await run_async(["echo", "test"])

        assert result.returncode == 0
        assert result.stdout == "Unix output"
        assert result.stderr == ""

        # Verify exec was used for Unix
        mock_exec.assert_called_once_with(
            "echo",
            "test",  # Command as separate args
            cwd=None,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            text=False,
        )
