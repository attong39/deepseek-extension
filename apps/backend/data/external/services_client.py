"""External services integration for ZETA AI."""

from __future__ import annotations

import asyncio
import logging
from abc import ABC
from datetime import UTC, datetime
from typing import Any

import httpx
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class ExternalServiceError(Exception):
    """Base exception for external service errors."""
import BaseException
import Exception
import api_key
import base_url
import body
import bool
import client
import connection_string
import dict
import e
import endpoint
import float
import from_email
import getattr
import host
import html_body
import int
import isinstance
import key
import len
import list
import max_tokens
import messages
import method
import model
import name
import openai_api_key
import params
import password
import port
import postgresql_connection
import redis_host
import redis_password
import redis_port
import result
import secret
import self
import service
import smtp_host
import smtp_password
import smtp_port
import smtp_username
import str
import subject
import sum
import super
import temperature
import text
import timeout
import to_email
import type
import username
import zip


class ServiceResponse(BaseModel):
    """Standard response from external services."""

    success: bool

    data: Any = None

    error: str | None = None

    status_code: int | None = None

    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))


class BaseExternalService(ABC):
    """Base class for external service integrations."""

    def __init__(
        self, base_url: str, api_key: str | None = None, timeout: int = 30
    ) -> None:
        """


        Initialize external service client.





        Args:


            base_url: Base URL for the service


            api_key: API key for authentication


            timeout: Request timeout in seconds


        """

        self.base_url = base_url.rstrip("/")

        self.api_key = api_key

        self.timeout = timeout

        self.client = httpx.AsyncClient(
            timeout=timeout, headers=self._get_default_headers()
        )

    def _get_default_headers(self) -> dict[str, str]:
        """


        Get default headers for requests.





        Returns:


            Default headers


        """

        headers = {"Content-Type": "application/json", "User-Agent": "ZETA-AI/1.0"}

        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        return headers

    async def _make_request(
        self,
        method: str,
        endpoint: str,
        data: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> ServiceResponse:
        """


        Make HTTP request to external service.





        Args:


            method: HTTP method


            endpoint: API endpoint


            data: Request data


            params: Query parameters


            headers: Additional headers





        Returns:


            Service response


        """

        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        try:
            request_headers = self._get_default_headers()

            if headers:
                request_headers.update(headers)

            response = await self.client.request(
                method=method,
                url=url,
                json=data,
                params=params,
                headers=request_headers,
            )

            response_data = None

            try:
                response_data = response.json()

            except Exception:
                response_data = response.text

            return ServiceResponse(
                success=response.is_success,
                data=response_data,
                status_code=response.status_code,
                error=None if response.is_success else f"HTTP {response.status_code}",
            )

        except httpx.TimeoutException as e:
            logger.error(f"Request timeout for {url}: {e}")

            return ServiceResponse(
                success=False, error="Request timeout", status_code=408
            )

        except Exception as e:
            logger.error(f"Request failed for {url}: {e}")

            return ServiceResponse(success=False, error=str(e))

    async def health_check(self) -> bool:
        """


        Check if the external service is healthy.





        Returns:


            True if healthy, False otherwise


        """

        try:
            response = await self._make_request("GET", "/health")

            return response.success

        except Exception:
            return False

    async def close(self) -> None:
        """Close the HTTP client."""

        await self.client.aclose()


class OpenAIService(BaseExternalService):
    """OpenAI API integration."""

    def __init__(self, api_key: str) -> None:
        """


        Initialize OpenAI service.





        Args:


            api_key: OpenAI API key


        """

        super().__init__("https://api.openai.com/v1", api_key)

    async def create_completion(
        self,
        model: str = "gpt-4",
        messages: list[dict[str, str]] | None = None,
        max_tokens: int = 1000,
        temperature: float = 0.7,
    ) -> ServiceResponse:
        """


        Create chat completion.





        Args:


            model: Model to use


            messages: Conversation messages


            max_tokens: Maximum tokens to generate


            temperature: Sampling temperature





        Returns:


            Completion response


        """

        data = {
            "model": model,
            "messages": messages or [],
            "max_tokens": max_tokens,
            "temperature": temperature,
        }

        return await self._make_request("POST", "/chat/completions", data=data)

    async def create_embedding(
        self, text: str, model: str = "text-embedding-ada-002"
    ) -> ServiceResponse:
        """


        Create text embedding.





        Args:


            text: Text to embed


            model: Embedding model





        Returns:


            Embedding response


        """

        data = {"input": text, "model": model}

        return await self._make_request("POST", "/embeddings", data=data)

    async def health_check(self) -> bool:
        """Check OpenAI API health."""

        try:
            response = await self._make_request("GET", "/models")

            return response.success

        except Exception:
            return False


class RedisService(BaseExternalService):
    """Redis integration for caching and session storage."""

    def __init__(
        self, host: str = "localhost", port: int = 6379, password: str | None = None
    ) -> None:
        """


        Initialize Redis service.





        Args:


            host: Redis host


            port: Redis port


            password: Redis password


        """

        # Note: This would typically use aioredis instead of HTTP

        super().__init__(f"http://{host}:{port}")

        self.password = password

    async def set_cache(
        self, key: str, value: Any, ttl: int | None = None
    ) -> ServiceResponse:
        """


        Set cache value.





        Args:


            key: Cache key


            value: Value to cache


            ttl: Time to live in seconds





        Returns:


            Response


        """

        # This is a placeholder implementation

        # Real implementation would use aioredis

        try:
            logger.info(f"Setting cache key: {key}")

            return ServiceResponse(success=True, data={"key": key, "cached": True})

        except Exception as e:
            logger.error(f"Failed to set cache: {e}")

            return ServiceResponse(success=False, error=str(e))

    async def get_cache(self, key: str) -> ServiceResponse:
        """


        Get cache value.





        Args:


            key: Cache key





        Returns:


            Cached value response


        """

        try:
            logger.info(f"Getting cache key: {key}")

            return ServiceResponse(success=True, data=None)  # Placeholder

        except Exception as e:
            logger.error(f"Failed to get cache: {e}")

            return ServiceResponse(success=False, error=str(e))


class PostgreSQLService(BaseExternalService):
    """PostgreSQL database service for health monitoring."""

    def __init__(self, connection_string: str) -> None:
        """


        Initialize PostgreSQL service.





        Args:


            connection_string: Database connection string


        """

        super().__init__("postgresql://localhost")  # Placeholder

        self.connection_string = connection_string

    async def health_check(self) -> bool:
        """Check database health."""

        try:
            # This would normally connect to PostgreSQL and run a simple query

            logger.info("Checking PostgreSQL health")

            return True  # Placeholder

        except Exception as e:
            logger.error(f"PostgreSQL health check failed: {e}")

            return False

    async def get_metrics(self) -> ServiceResponse:
        """


        Get database metrics.





        Returns:


            Database metrics


        """

        try:
            metrics = {
                "connections": 10,
                "queries_per_second": 50,
                "cache_hit_ratio": 0.95,
                "database_size": "1.2GB",
            }

            return ServiceResponse(success=True, data=metrics)

        except Exception as e:
            logger.error(f"Failed to get database metrics: {e}")

            return ServiceResponse(success=False, error=str(e))


class EmailService(BaseExternalService):
    """Email service integration."""

    def __init__(
        self,
        smtp_host: str,
        smtp_port: int = 587,
        username: str = "",
        password: str = "",
    ) -> None:
        """


        Initialize email service.





        Args:


            smtp_host: SMTP server host


            smtp_port: SMTP server port


            username: SMTP username


            password: SMTP password


        """

        super().__init__(f"smtp://{smtp_host}:{smtp_port}")

        self.username = username

        self.password = password

    async def send_email(
        self,
        to_email: str,
        subject: str,
        body: str,
        html_body: str | None = None,
        from_email: str | None = None,
    ) -> ServiceResponse:
        """


        Send email.





        Args:


            to_email: Recipient email


            subject: Email subject


            body: Email body (plain text)


            html_body: Email body (HTML)


            from_email: Sender email





        Returns:


            Send response


        """

        try:
            # Chuẩn bị payload gửi email (mock) – không cần gán biến nếu không sử dụng
            _ = {
                "to": to_email,
                "subject": subject,
                "body": body,
                "html_body": html_body,
                "from": from_email or self.username,
            }

            logger.info(f"Sending email to {to_email}")

            # This would normally use aiosmtplib or similar

            return ServiceResponse(success=True, data={"message_id": "mock_id_123"})

        except Exception as e:
            logger.error(f"Failed to send email: {e}")

            return ServiceResponse(success=False, error=str(e))


class WebhookService(BaseExternalService):
    """Webhook service for external integrations."""

    def __init__(self) -> None:
        """Initialize webhook service."""

        super().__init__("http://localhost")

    async def send_webhook(
        self, url: str, data: dict[str, Any], secret: str | None = None
    ) -> ServiceResponse:
        """


        Send webhook notification.





        Args:


            url: Webhook URL


            data: Webhook data


            secret: Webhook secret for signing





        Returns:


            Webhook response


        """

        try:
            headers = {}

            if secret:
                # This would normally include HMAC signature

                headers["X-Webhook-Signature"] = f"sha256={secret}"

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url, json=data, headers=headers, timeout=10
                )

                return ServiceResponse(
                    success=response.is_success,
                    data={"delivered": True, "response_code": response.status_code},
                    status_code=response.status_code,
                )

        except Exception as e:
            logger.error(f"Failed to send webhook to {url}: {e}")

            return ServiceResponse(success=False, error=str(e))


class ExternalServiceManager:
    """Manager for all external service integrations."""

    def __init__(self) -> None:
        """Initialize service manager."""

        self.services: dict[str, BaseExternalService] = {}

        self.health_status: dict[str, bool] = {}

    def register_service(self, name: str, service: BaseExternalService) -> None:
        """


        Register an external service.





        Args:


            name: Service name


            service: Service instance


        """

        self.services[name] = service

        logger.info(f"Registered external service: {name}")

    async def health_check_all(self) -> dict[str, bool]:
        """


        Check health of all registered services.





        Returns:


            Health status for each service


        """

        tasks = []

        service_names = []

        for name, service in self.services.items():
            tasks.append(service.health_check())

            service_names.append(name)

        if tasks:
            results = await asyncio.gather(*tasks, return_exceptions=True)

            for name, result in zip(service_names, results, strict=False):
                if isinstance(result, BaseException):
                    self.health_status[name] = False
                    logger.error(f"Health check failed for {name}: {result}")
                else:
                    # Kết quả mong đợi là bool; ép về bool để thỏa kiểm tra kiểu
                    self.health_status[name] = bool(result)

        return self.health_status

    async def get_service_metrics(self) -> dict[str, Any]:
        """


        Get metrics from all services.





        Returns:


            Metrics from all services


        """

        metrics = {
            "service_count": len(self.services),
            "healthy_services": sum(self.health_status.values()),
            "unhealthy_services": len(self.health_status)
            - sum(self.health_status.values()),
            "services": {},
        }

        for name, service in self.services.items():
            metrics["services"][name] = {
                "healthy": self.health_status.get(name, False),
                "type": type(service).__name__,
                "base_url": getattr(service, "base_url", "N/A"),
            }

        return metrics

    async def close_all(self) -> None:
        """Close all service connections."""

        for name, service in self.services.items():
            try:
                await service.close()

                logger.info(f"Closed service: {name}")

            except Exception as e:
                logger.error(f"Failed to close service {name}: {e}")


# Factory functions for creating service instances


def create_openai_service(api_key: str) -> OpenAIService:
    """Create OpenAI service instance."""

    return OpenAIService(api_key)


def create_redis_service(
    host: str = "localhost", port: int = 6379, password: str | None = None
) -> RedisService:
    """Create Redis service instance."""

    return RedisService(host, port, password)


def create_postgresql_service(connection_string: str) -> PostgreSQLService:
    """Create PostgreSQL service instance."""

    return PostgreSQLService(connection_string)


def create_email_service(
    smtp_host: str, smtp_port: int = 587, username: str = "", password: str = ""
) -> EmailService:
    """Create email service instance."""

    return EmailService(smtp_host, smtp_port, username, password)


def create_webhook_service() -> WebhookService:
    """Create webhook service instance."""

    return WebhookService()


async def initialize_external_services(
    openai_api_key: str | None = None,
    redis_host: str = "localhost",
    redis_port: int = 6379,
    redis_password: str | None = None,
    postgresql_connection: str | None = None,
    smtp_host: str | None = None,
    smtp_port: int = 587,
    smtp_username: str = "",
    smtp_password: str = "",
) -> ExternalServiceManager:
    """


    Initialize all external services.





    Args:


        openai_api_key: OpenAI API key


        redis_host: Redis host


        redis_port: Redis port


        redis_password: Redis password


        postgresql_connection: PostgreSQL connection string


        smtp_host: SMTP host


        smtp_port: SMTP port


        smtp_username: SMTP username


        smtp_password: SMTP password





    Returns:


        Configured service manager


    """

    manager = ExternalServiceManager()

    # Register OpenAI service

    if openai_api_key:
        manager.register_service("openai", create_openai_service(openai_api_key))

    # Register Redis service

    manager.register_service(
        "redis", create_redis_service(redis_host, redis_port, redis_password)
    )

    # Register PostgreSQL service

    if postgresql_connection:
        manager.register_service(
            "postgresql", create_postgresql_service(postgresql_connection)
        )

    # Register email service

    if smtp_host:
        manager.register_service(
            "email",
            create_email_service(smtp_host, smtp_port, smtp_username, smtp_password),
        )

    # Register webhook service

    manager.register_service("webhook", create_webhook_service())

    # Initial health check

    await manager.health_check_all()

    logger.info(
        f"Initialized external service manager with {len(manager.services)} services"
    )

    return manager
