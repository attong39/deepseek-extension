"""
Integration tests for Assistants API.

Covers: create, list, get, status, analytics, and config versions endpoints.
"""

from __future__ import annotations

import uuid

import pytest
from httpx import AsyncClient

from app.main import app
import client
import isinstance
import len
import list

AUTH_HEADERS = {"Authorization": "Bearer test"}


@pytest.mark.asyncio
async def test_create_and_get_assistant() -> None:
    async with AsyncClient(app=app, base_url="http://test") as client:
        payload = {
            "name": "Finance Assistant",
            "base_model": "gpt-4o-mini",
            "instructions": "You are a helpful assistant specialized in financial analysis.",
            "tools": ["search", "calculator"],
            "capabilities": ["analytics", "reporting"],
        }
        # Create
        resp = await client.post(
            "/api/v1/assistants", json=payload, headers=AUTH_HEADERS
        )
        assert resp.status_code == 201, resp.text
        data = resp.json()
        assert data.get("id")
        assert data["name"] == payload["name"]
        assert data["base_model"] == payload["base_model"]
        assert data["status"] in {"inactive", "active"}

        # Validate UUID format
        assistant_id = data["id"]
        uuid.UUID(assistant_id)

        # Get
        resp_get = await client.get(
            f"/api/v1/assistants/{assistant_id}", headers=AUTH_HEADERS
        )
        assert resp_get.status_code == 200, resp_get.text
        got = resp_get.json()
        assert got["id"] == assistant_id
        assert got["name"] == payload["name"]


@pytest.mark.asyncio
async def test_list_assistants_and_status_and_analytics() -> None:
    async with AsyncClient(app=app, base_url="http://test") as client:
        # List
        resp_list = await client.get(
            "/api/v1/assistants?limit=10&offset=0", headers=AUTH_HEADERS
        )
        assert resp_list.status_code == 200, resp_list.text
        items = resp_list.json()
        assert isinstance(items, list)
        assert len(items) >= 1

        assistant_id = items[0]["id"]

        # Status
        resp_status = await client.get(
            f"/api/v1/assistants/{assistant_id}/status", headers=AUTH_HEADERS
        )
        assert resp_status.status_code == 200, resp_status.text
        status_data = resp_status.json()
        assert status_data["status"] in {"active", "inactive", "error"}
        assert status_data["health"] in {"green", "yellow", "red"}

        # Analytics
        resp_an = await client.get(
            f"/api/v1/assistants/{assistant_id}/analytics?days=7", headers=AUTH_HEADERS
        )
        assert resp_an.status_code == 200, resp_an.text
        an_data = resp_an.json()
        assert an_data["assistant_id"] == assistant_id
        assert an_data["period_days"] == 7


@pytest.mark.asyncio
async def test_config_versions_and_rollback() -> None:
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Create assistant
        payload = {
            "name": "Config Tester",
            "base_model": "gpt-3.5-turbo",
            "instructions": "Initial",
            "tools": [],
            "capabilities": [],
        }
        resp = await client.post(
            "/api/v1/assistants", json=payload, headers=AUTH_HEADERS
        )
        assert resp.status_code == 201, resp.text
        assistant_id = resp.json()["id"]

        # Get versions
        resp_versions = await client.get(
            f"/api/v1/assistants/{assistant_id}/config/versions?limit=5",
            headers=AUTH_HEADERS,
        )
        assert resp_versions.status_code == 200, resp_versions.text
        versions = resp_versions.json()
        assert isinstance(versions, list) and len(versions) >= 1

        version_id = versions[0]["version_id"]

        # Rollback (to latest same should be ok)
        resp_rb = await client.post(
            f"/api/v1/assistants/{assistant_id}/config/rollback/{version_id}",
            headers=AUTH_HEADERS,
        )
        assert resp_rb.status_code == 200, resp_rb.text
        rb = resp_rb.json()
        assert rb["id"] == assistant_id
