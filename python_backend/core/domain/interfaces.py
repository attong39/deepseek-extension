"""
Abstract interfaces/ports cho dependency injection và testing.
Định nghĩa contracts giữa các layers.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Protocol

from core.domain.entities import BatchProcessingResult, DistillationDatapoint, TeacherLabel


class CacheServiceInterface(Protocol):
    """Interface cho cache service"""

    async def get(self, key: str) -> Optional[Any]:
        """Lấy value từ cache"""
        ...

    async def set(self, key: str, value: Any, ttl_seconds: Optional[int] = None) -> bool:
        """Set value vào cache với TTL"""
        ...

    async def delete(self, key: str) -> bool:
        """Xóa key khỏi cache"""
        ...

    async def exists(self, key: str) -> bool:
        """Kiểm tra key có tồn tại trong cache không"""
        ...


class MetricsServiceInterface(Protocol):
    """Interface cho metrics collection"""

    def increment_counter(self, metric_name: str, labels: Optional[Dict[str, str]] = None) -> None:
        """Tăng counter metric"""
        ...

    def record_histogram(self, metric_name: str, value: float, labels: Optional[Dict[str, str]] = None) -> None:
        """Record histogram metric"""
        ...

    def set_gauge(self, metric_name: str, value: float, labels: Optional[Dict[str, str]] = None) -> None:
        """Set gauge metric"""
        ...


class TeacherModelClientInterface(Protocol):
    """Interface cho teacher model client"""

    async def generate_label(self, input_text: str, model_config: Optional[Dict[str, Any]] = None) -> TeacherLabel:
        """Generate label từ teacher model"""
        ...

    async def batch_generate_labels(self, input_texts: List[str], model_config: Optional[Dict[str, Any]] = None) -> List[TeacherLabel]:
        """Batch generate labels từ teacher model"""
        ...

    async def health_check(self) -> bool:
        """Kiểm tra health của teacher model"""
        ...


class DistillationRepositoryInterface(Protocol):
    """Interface cho distillation data repository"""

    async def save_datapoint(self, datapoint: DistillationDatapoint) -> bool:
        """Lưu distillation datapoint"""
        ...

    async def save_datapoints(self, datapoints: List[DistillationDatapoint]) -> bool:
        """Lưu batch distillation datapoints"""
        ...

    async def get_datapoint(self, datapoint_id: str) -> Optional[DistillationDatapoint]:
        """Lấy distillation datapoint theo ID"""
        ...

    async def get_datapoints_by_batch(self, batch_id: str) -> List[DistillationDatapoint]:
        """Lấy tất cả datapoints trong một batch"""
        ...

    async def save_batch_result(self, result: BatchProcessingResult) -> bool:
        """Lưu kết quả batch processing"""
        ...


class CircuitBreakerInterface(Protocol):
    """Interface cho circuit breaker pattern"""

    async def call(self, func, *args, **kwargs) -> Any:
        """Execute function với circuit breaker protection"""
        ...

    @property
    def is_open(self) -> bool:
        """Kiểm tra circuit breaker có đang open không"""
        ...

    @property
    def failure_count(self) -> int:
        """Số lượng failures hiện tại"""
        ...

    def reset(self) -> None:
        """Reset circuit breaker về trạng thái closed"""
        ...


class RetryServiceInterface(Protocol):
    """Interface cho retry logic với exponential backoff"""

    async def execute_with_retry(
        self,
        func,
        *args,
        max_retries: int = 3,
        base_delay: float = 1.0,
        max_delay: float = 60.0,
        exponential_base: float = 2.0,
        **kwargs
    ) -> Any:
        """Execute function với retry logic"""
        ...


class RateLimiterInterface(Protocol):
    """Interface cho rate limiting"""

    async def is_allowed(self, key: str, limit: int, window_seconds: int) -> bool:
        """Kiểm tra xem request có được phép không"""
        ...

    async def get_remaining(self, key: str, limit: int, window_seconds: int) -> int:
        """Lấy số requests còn lại trong window"""
        ...


class InputSanitizerInterface(Protocol):
    """Interface cho input sanitization"""

    def sanitize_text(self, text: str) -> str:
        """Sanitize text input"""
        ...

    def validate_input(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate và sanitize input data"""
        ...

    def is_safe_input(self, text: str) -> bool:
        """Kiểm tra input có safe không"""
        ...


# Abstract base classes for dependency injection

class BaseService(ABC):
    """Base class cho tất cả services"""

    def __init__(self, metrics: MetricsServiceInterface):
        self.metrics = metrics

    @abstractmethod
    async def health_check(self) -> bool:
        """Health check cho service"""
        pass


class BaseRepository(ABC):
    """Base class cho tất cả repositories"""

    @abstractmethod
    async def health_check(self) -> bool:
        """Health check cho repository"""
        pass
