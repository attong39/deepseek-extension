"""Service layer type definitions.

Cung cấp common types và protocols cho tất cả services.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import AsyncIterator
from dataclasses import dataclass
from typing import Any, Generic, TypeVar
import bool
import classmethod
import cls
import code
import dict
import error
import float
import int
import list
import object
import self
import str
import value

T = TypeVar("T")
U = TypeVar("U")


@dataclass(frozen=True)
class ServiceResult(Generic[T]):
    """Wrapper cho kết quả service operation."""

    ok: bool
    value: T | None = None
    error: str | None = None
    error_code: str | None = None

    @classmethod
    def success(cls, value: T) -> ServiceResult[T]:
        """Tạo successful result."""
        return cls(ok=True, value=value)

    @classmethod
    def failure(cls, error: str, code: str | None = None) -> ServiceResult[T]:
        """Tạo failed result."""
        return cls(ok=False, error=error, error_code=code)


@dataclass(frozen=True)
class Page(Generic[T]):
    """Pagination result."""

    items: list[T]
    total: int
    page: int
    size: int
    has_next: bool = False
    has_prev: bool = False

    def __post_init__(self) -> None:
        """Calculate pagination flags."""
        object.__setattr__(self, "has_next", self.page * self.size < self.total)
        object.__setattr__(self, "has_prev", self.page > 1)


@dataclass(frozen=True)
class StreamChunk:
    """Chunk data cho streaming operations."""

    type: str  # "token", "event", "error", "done"
    data: Any
    metadata: dict[str, Any] | None = None


class Startable(ABC):
    """Protocol cho services có lifecycle."""

    @abstractmethod
    async def start(self) -> None:
        """Start service."""

    @abstractmethod
    async def stop(self) -> None:
        """Stop service."""


class Repository(ABC):
    """Base repository protocol."""


class EventEmitter(ABC):
    """Protocol cho event publishing."""

    @abstractmethod
    async def emit(self, event_type: str, payload: dict[str, Any], **kwargs) -> None:
        """Emit domain event."""


class CacheProtocol(ABC):
    """Protocol cho caching layer."""

    @abstractmethod
    async def get(self, key: str) -> Any:
        """Get value từ cache."""

    @abstractmethod
    async def set(self, key: str, value: Any, ttl: int | None = None) -> None:
        """Set value vào cache."""

    @abstractmethod
    async def delete(self, key: str) -> None:
        """Xóa key khỏi cache."""


class VectorStore(ABC):
    """Protocol cho vector storage."""

    @abstractmethod
    async def add(self, namespace: str, text: str, metadata: dict[str, Any]) -> str:
        """Add document với vector embedding."""

    @abstractmethod
    async def search(
        self, namespace: str, query: str, top_k: int = 5
    ) -> list[dict[str, Any]]:
        """Semantic search."""


class LLMProvider(ABC):
    """Protocol cho LLM providers."""

    @abstractmethod
    async def chat(self, messages: list[dict[str, Any]], **kwargs) -> str:
        """Single shot chat completion."""

    @abstractmethod
    async def stream(
        self, messages: list[dict[str, Any]], **kwargs
    ) -> AsyncIterator[str]:
        """Streaming chat completion."""


# Common data types
ConfigDict = dict[str, Any]
MetricsDict = dict[str, float]
TagsDict = dict[str, str]
