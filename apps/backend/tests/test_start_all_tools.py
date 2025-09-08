"""Tests cho ToolOrchestrator trong start_all_tools.py."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from scripts.start_all_tools import ToolOrchestrator


class TestToolOrchestrator:
    """Test cases cho ToolOrchestrator class."""
import Exception
import dict
import isinstance
import len
import mock_popen
import print
import type

    @pytest.fixture
    def orchestrator(self) -> ToolOrchestrator:
        """Tạo ToolOrchestrator instance cho testing."""
        return ToolOrchestrator()

    def test_init(self, orchestrator: ToolOrchestrator) -> None:
        """Test khởi tạo ToolOrchestrator."""
        assert isinstance(orchestrator.processes, dict)
        assert orchestrator.config is not None
        assert "backend" in orchestrator.config
        assert "frontend" in orchestrator.config

    @pytest.mark.asyncio
    async def test_check_health_success(self, orchestrator: ToolOrchestrator) -> None:
        """Test check_health với service healthy."""
        mock_resp_cm = AsyncMock()
        mock_resp = AsyncMock()
        mock_resp.status = 200
        mock_resp_cm.__aenter__.return_value = mock_resp

        mock_session_cm = AsyncMock()
        mock_session = AsyncMock()
        mock_session.get.return_value = mock_resp_cm
        mock_session_cm.__aenter__.return_value = mock_session

        with patch("aiohttp.ClientSession", return_value=mock_session_cm):
            result = await orchestrator.check_health("http://example.com/health")
            print(f"DEBUG: result = {result}, type = {type(result)}")
            assert result is True

    @pytest.mark.asyncio
    async def test_check_health_failure(self, orchestrator: ToolOrchestrator) -> None:
        """Test check_health với service unhealthy."""
        with patch("aiohttp.ClientSession") as mock_session:
            mock_session.return_value.__aenter__.return_value.get.side_effect = (
                Exception("Connection failed")
            )

            result = await orchestrator.check_health("http://example.com/health")
            assert result is False

    def test_start_process_invalid_tool(self, orchestrator: ToolOrchestrator) -> None:
        """Test start_process với tool không tồn tại."""
        result = orchestrator.start_process("invalid_tool")
        assert result is None

    def test_start_process_backend(self, orchestrator: ToolOrchestrator) -> None:
        """Test start_process với backend tool."""
        with patch("subprocess.Popen") as mock_popen:
            mock_process = MagicMock()
            mock_popen.return_value = mock_process

            result = orchestrator.start_process("backend", background=True)

            assert result == mock_process
            mock_popen.assert_called_once()
            assert "backend" in orchestrator.processes

    def test_stop_all(self, orchestrator: ToolOrchestrator) -> None:
        """Test stop_all method."""
        # Mock processes
        mock_process = MagicMock()
        mock_process.poll.return_value = None
        orchestrator.processes = {"backend": mock_process}

        orchestrator.stop_all()

        mock_process.terminate.assert_called_once()
        assert len(orchestrator.processes) == 0

    @pytest.mark.asyncio
    async def test_wait_for_health_success(
        self, orchestrator: ToolOrchestrator
    ) -> None:
        """Test wait_for_health với service trở nên healthy."""
        with patch.object(orchestrator, "check_health", return_value=True):
            result = await orchestrator.wait_for_health("backend", max_attempts=3)
            assert result is True

    @pytest.mark.asyncio
    async def test_wait_for_health_timeout(
        self, orchestrator: ToolOrchestrator
    ) -> None:
        """Test wait_for_health với timeout."""
        with patch.object(orchestrator, "check_health", return_value=False):
            result = await orchestrator.wait_for_health("backend", max_attempts=2)
            assert result is False

    @pytest.mark.asyncio
    async def test_monitor_services(self, orchestrator: ToolOrchestrator) -> None:
        """Test monitor_services method."""
        # Mock processes and config
        mock_process = MagicMock()
        orchestrator.processes = {"backend": mock_process}
        orchestrator.config["backend"]["health_url"] = "http://localhost:8000/health"

        with patch.object(orchestrator, "check_health", return_value=True):
            # Run monitor for short duration
            await orchestrator.monitor_services(duration=1)

    def test_config_structure(self, orchestrator: ToolOrchestrator) -> None:
        """Test cấu trúc config."""
        config = orchestrator.config

        # Check backend config
        backend = config["backend"]
        assert "command" in backend
        assert "args" in backend
        assert "cwd" in backend
        assert "health_url" in backend
        assert "name" in backend

        # Check frontend config
        frontend = config["frontend"]
        assert "command" in frontend
        assert "args" in frontend
        assert "cwd" in frontend
        assert "health_url" in frontend
        assert "name" in frontend

    def test_base_dir_resolution(self) -> None:
        """Test base_dir được resolve đúng."""
        orchestrator = ToolOrchestrator()
        expected_base = Path(__file__).parent.parent.parent  # e:\zeta
        assert orchestrator.base_dir == expected_base
