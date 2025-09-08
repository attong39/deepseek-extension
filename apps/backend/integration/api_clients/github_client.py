from __future__ import annotations

import os
from typing import Any

import httpx
from pydantic import BaseModel, Field, ValidationError
import Exception
import ImportError
import RuntimeError
import ValueError
import attempt
import base
import base_url
import body
import client
import dict
import e
import endpoint
import float
import head
import int
import isinstance
import json_data
import labels
import list
import max_retries
import method
import owner
import range
import repo
import self
import state
import str
import timeout
import title
import token

try:
    from core.observability.logging import get_logger

    logger = get_logger(__name__)
except ImportError:
    import logging

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

"""
GitHub API client cho ZETA_VN.
Tích hợp với GitHub REST API để quản lý repos, issues, PRs, etc.
"""


class GitHubIssuePayload(BaseModel):
    """Schema cho payload tạo issue GitHub."""

    title: str = Field(..., min_length=1, max_length=256, description="Tiêu đề issue.")
    body: str = Field("", max_length=65536, description="Nội dung issue.")
    labels: list[str] = Field(default_factory=list, description="Danh sách labels.")

    class Config:
        validate_assignment = True


class GitHubPRPayload(BaseModel):
    """Schema cho payload tạo PR GitHub."""

    title: str = Field(..., min_length=1, max_length=256, description="Tiêu đề PR.")
    head: str = Field(..., description="Branch nguồn.")
    base: str = Field(..., description="Branch đích.")
    body: str = Field("", max_length=65536, description="Nội dung PR.")

    class Config:
        validate_assignment = True


class GitHubClient:
    """Client để tương tác với GitHub API.

    Hỗ trợ async operations với validation và error handling.
    Sử dụng env vars cho config để tránh hard-code.

    Attributes:
        token: GitHub personal access token (từ env hoặc param).
        base_url: Base URL GitHub API.
    """

    def __init__(
        self,
        token: str | None = None,
        base_url: str = "https://api.github.com",
        timeout: float = 10.0,
        max_retries: int = 3,
    ) -> None:
        """Khởi tạo GitHubClient.

        Args:
            token: GitHub token. Nếu None, lấy từ env GITHUB_TOKEN.
            base_url: Base URL API.
            timeout: Timeout cho requests (giây).
            max_retries: Số lần retry tối đa.

        Raises:
            ValueError: Nếu config không hợp lệ.
        """
        self.token = token or os.getenv("GITHUB_TOKEN")
        self.base_url = base_url
        self.timeout = timeout
        self.max_retries = max_retries

        if not self.token:
            raise ValueError("GitHub token chưa cấu hình (env GITHUB_TOKEN)")

    async def _make_request(
        self,
        method: str,
        endpoint: str,
        json_data: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Thực hiện HTTP request tới GitHub API.

        Args:
            method: Phương thức HTTP.
            endpoint: Endpoint API.
            json_data: Dữ liệu JSON.
            params: Query params.

        Returns:
            Response JSON.

        Raises:
            httpx.HTTPStatusError: Nếu API trả lỗi.
            httpx.RequestError: Nếu network lỗi.
        """
        url = f"{self.base_url}{endpoint}"
        headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json",
        }

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            for attempt in range(self.max_retries):
                try:
                    response = await client.request(
                        method, url, headers=headers, json=json_data, params=params
                    )
                    response.raise_for_status()
                    return response.json()
                except httpx.HTTPStatusError as e:
                    logger.error(f"GitHub API lỗi (attempt {attempt + 1}): {e}")
                    if e.response.status_code >= 500:
                        if attempt < self.max_retries - 1:
                            continue
                    raise
                except httpx.RequestError as e:
                    logger.error(f"Network lỗi GitHub (attempt {attempt + 1}): {e}")
                    if attempt < self.max_retries - 1:
                        continue
                    raise
        raise RuntimeError("GitHub request thất bại sau tất cả retries")

    async def get_repo(self, owner: str, repo: str) -> dict[str, Any]:
        """Lấy thông tin repo.

        Args:
            owner: Chủ sở hữu repo.
            repo: Tên repo.

        Returns:
            Thông tin repo.
        """
        try:
            return await self._make_request("GET", f"/repos/{owner}/{repo}")
        except Exception as e:
            logger.error(f"Lỗi lấy repo {owner}/{repo}: {e}")
            raise

    async def create_issue(
        self,
        owner: str,
        repo: str,
        title: str,
        body: str = "",
        labels: list[str] | None = None,
    ) -> dict[str, Any]:
        """Tạo issue mới.

        Args:
            owner: Chủ sở hữu repo.
            repo: Tên repo.
            title: Tiêu đề issue.
            body: Nội dung issue.
            labels: Danh sách labels.

        Returns:
            Thông tin issue đã tạo.

        Raises:
            ValidationError: Nếu input không hợp lệ.
        """
        try:
            payload = GitHubIssuePayload(title=title, body=body, labels=labels or [])
        except ValidationError as e:
            logger.error(f"Validation lỗi cho issue payload: {e}")
            raise

        try:
            return await self._make_request(
                "POST", f"/repos/{owner}/{repo}/issues", json_data=payload.dict()
            )
        except Exception as e:
            logger.error(f"Lỗi tạo issue trong {owner}/{repo}: {e}")
            raise

    async def create_pull_request(
        self, owner: str, repo: str, title: str, head: str, base: str, body: str = ""
    ) -> dict[str, Any]:
        """Tạo pull request mới.

        Args:
            owner: Chủ sở hữu repo.
            repo: Tên repo.
            title: Tiêu đề PR.
            head: Branch nguồn.
            base: Branch đích.
            body: Nội dung PR.

        Returns:
            Thông tin PR đã tạo.

        Raises:
            ValidationError: Nếu input không hợp lệ.
        """
        try:
            payload = GitHubPRPayload(title=title, head=head, base=base, body=body)
        except ValidationError as e:
            logger.error(f"Validation lỗi cho PR payload: {e}")
            raise

        try:
            return await self._make_request(
                "POST", f"/repos/{owner}/{repo}/pulls", json_data=payload.dict()
            )
        except Exception as e:
            logger.error(f"Lỗi tạo PR trong {owner}/{repo}: {e}")
            raise

    async def list_issues(
        self, owner: str, repo: str, state: str = "open"
    ) -> list[dict[str, Any]]:
        """Liệt kê issues.

        Args:
            owner: Chủ sở hữu repo.
            repo: Tên repo.
            state: Trạng thái issues (open/closed/all).

        Returns:
            Danh sách issues.
        """
        try:
            params = {"state": state}
            response = await self._make_request(
                "GET", f"/repos/{owner}/{repo}/issues", params=params
            )
            return response if isinstance(response, list) else []
        except Exception as e:
            logger.error(f"Lỗi liệt kê issues {owner}/{repo}: {e}")
            raise


__all__ = [
    "GitHubClient",
    "GitHubIssuePayload",
    "GitHubPRPayload",
]
