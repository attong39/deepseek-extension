from __future__ import annotations

import asyncio
from abc import ABC, abstractmethod
from collections import defaultdict
from collections.abc import Awaitable, Callable
from contextlib import asynccontextmanager
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import ClassVar, Protocol, TypeVar
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field
import BaseException
import Exception
import base_delay
import bool
import concurrency
import dict
import e
import etype
import event_type
import float
import h
import handler
import handlers
import i
import int
import isinstance
import list
import logger
import m
import max_queue
import middlewares
import outbox
import priority
import range
import repr
import retries
import s
import self
import spec
import specs
import str
import t
import type
import workers

# ---------- Event base (typed + versioned) ----------


class BaseEvent(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    id: UUID = Field(default_factory=uuid4)
    ts: datetime = Field(default_factory=lambda: datetime.now(UTC))
    source: str = "zeta_vn"
    correlation_id: str | None = None
    # event_name / version làm ClassVar để không vào payload
    event_name: ClassVar[str] = "base.event"
    event_version: ClassVar[str] = "v1"

    def key(self) -> str:
        # Khóa idempotency mặc định
        return f"{self.event_name}:{self.event_version}:{self.id}"


E = TypeVar("E", bound=BaseEvent)


# Ví dụ event mẫu (bạn thay bằng domain event thực tế)
class AgentCreated(BaseEvent):
    event_name: ClassVar[str] = "agent.created"
    agent_id: str
    name: str


# ---------- Middleware Protocol ----------


class EventMiddleware(Protocol):
    async def before_publish(self, event: BaseEvent) -> None: ...
    async def after_publish(
        self, event: BaseEvent, error: BaseException | None
    ) -> None: ...


# ---------- Outbox/Dedup contracts ----------


class OutboxRepository(Protocol):
    async def is_processed(self, event_key: str) -> bool: ...
    async def mark_processed(self, event_key: str) -> None: ...


# ---------- EventBus contracts ----------

Handler = Callable[[BaseEvent], Awaitable[None]]


@dataclass(slots=True)
class HandlerSpec:
    func: Handler
    priority: int = 100
    concurrency: int = 16  # per-handler semaphore
    _sem: asyncio.Semaphore | None = None

    def ensure_sem(self) -> asyncio.Semaphore:
        if self._sem is None:
            self._sem = asyncio.Semaphore(self.concurrency)
        return self._sem


class EventBus(ABC):
    @abstractmethod
    async def publish(self, event: BaseEvent) -> None: ...

    @abstractmethod
    def subscribe(
        self,
        event_type: type[E],
        handler: Handler,
        *,
        priority: int = 100,
        concurrency: int = 16,
    ) -> None: ...

    @abstractmethod
    @asynccontextmanager
    async def lifespan(self):
        yield


# ---------- InMemoryEventBus (DEV/TEST) ----------


class InMemoryEventBus(EventBus):
    def __init__(
        self,
        *,
        middlewares: list[EventMiddleware] | None = None,
        outbox: OutboxRepository | None = None,
        max_queue: int = 10000,
        workers: int = 4,
    ) -> None:
        self._subs: dict[type[BaseEvent], list[HandlerSpec]] = defaultdict(list)
        self._middlewares = middlewares or []
        self._outbox = outbox
        self._q: asyncio.Queue[BaseEvent] = asyncio.Queue(maxsize=max_queue)
        self._workers = workers
        self._worker_tasks: list[asyncio.Task] = []

    def subscribe(
        self,
        event_type: type[E],
        handler: Handler,
        *,
        priority: int = 100,
        concurrency: int = 16,
    ) -> None:
        self._subs[event_type].append(HandlerSpec(handler, priority, concurrency))
        # Sort theo priority tăng dần (số nhỏ chạy trước)
        self._subs[event_type].sort(key=lambda s: s.priority)

    async def publish(self, event: BaseEvent) -> None:
        # Middlewares trước khi enqueue
        for m in self._middlewares:
            await m.before_publish(event)

        # Idempotency check (nếu có outbox)
        if self._outbox and await self._outbox.is_processed(event.key()):
            # Bỏ qua event đã xử lý
            for m in self._middlewares:
                await m.after_publish(event, None)
            return

        await self._q.put(event)

    async def _worker(self, idx: int):
        while True:
            event = await self._q.get()
            error: BaseException | None = None
            try:
                await self._dispatch(event)
                # Mark processed sau khi tất cả handler ok
                if self._outbox:
                    await self._outbox.mark_processed(event.key())
            except BaseException as e:  # không nuốt lỗi — để middleware biết
                error = e
            finally:
                for m in self._middlewares:
                    try:
                        await m.after_publish(event, error)
                    except Exception:
                        pass
                self._q.task_done()

    async def _dispatch(self, event: BaseEvent) -> None:
        # Tìm handler theo type (exact & subclass)
        handlers: list[HandlerSpec] = []
        for etype, specs in self._subs.items():
            if isinstance(event, etype):
                handlers.extend(specs)
        if not handlers:
            return

        # Chạy theo priority, có concurrency per-handler
        async def run_one(spec: HandlerSpec):
            sem = spec.ensure_sem()
            async with sem:
                await spec.func(event)

        await asyncio.gather(*(run_one(h) for h in handlers))

    @asynccontextmanager
    async def lifespan(self):
        try:
            self._worker_tasks = [
                asyncio.create_task(self._worker(i)) for i in range(self._workers)
            ]
            yield
        finally:
            for t in self._worker_tasks:
                t.cancel()
            # Drain cancel
            await asyncio.gather(*self._worker_tasks, return_exceptions=True)


# ---------- Built-in middlewares ----------


class LoggingMiddleware:
    def __init__(self, logger: Callable[..., None] | None = None) -> None:
        self._log = logger or (lambda **kw: None)

    async def before_publish(self, event: BaseEvent) -> None:
        self._log(event="before_publish", name=event.event_name, id=str(event.id))

    async def after_publish(
        self, event: BaseEvent, error: BaseException | None
    ) -> None:
        self._log(
            event="after_publish",
            name=event.event_name,
            id=str(event.id),
            ok=error is None,
            err=repr(error) if error else None,
        )


class RetryMiddleware:
    """Retry handler exceptions theo backoff mịn.
    Lưu ý: retry ở tầng handler hợp lý hơn; ở đây minh họa retry publish/dispatch đơn.
    """

    def __init__(self, retries: int = 2, base_delay: float = 0.1) -> None:
        self.retries = retries
        self.base_delay = base_delay

    async def before_publish(self, event: BaseEvent) -> None:
        return

    async def after_publish(
        self, event: BaseEvent, error: BaseException | None
    ) -> None:
        if not error:
            return
        # Ở InMemory bus, after_publish không có quyền re-dispatch.
        # Nếu cần retry thực sự, chuyển sang handler-level retry (khuyến nghị).
        return
