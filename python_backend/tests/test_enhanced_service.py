"""
Comprehensive tests cho Enhanced Distillation Service.
Cover tất cả optimizations: semaphore, retry, cache, circuit breaker, metrics.
"""

import asyncio
import pytest
import time
from unittest.mock import AsyncMock, MagicMock, patch
from typing import Any, Optional

from core.services.enhanced_service import EnhancedDistillationService, EnhancedDistillationConfig
from core.domain.entities import TeacherLabel, DistillationDatapoint, LabelConfidence
from core.services.cache_service import InMemoryCacheService
from core.services.metrics_service import PrometheusStyleMetricsService
from infrastructure.reliability import (
    CircuitBreakerService, 
    ExponentialBackoffRetryService,
    InputSanitizer
)
from infrastructure.external.teacher_model_client import MockTeacherModelClient


class TestEnhancedDistillationService:
    """Test suite cho Enhanced Distillation Service"""
    
    @pytest.fixture
    async def mock_teacher_client(self):
        """Mock teacher model client"""
        client = AsyncMock()
        client.health_check.return_value = True
        
        # Mock generate_label response
        mock_label = TeacherLabel(
            input_text="test input",
            predicted_label="positive",
            confidence_score=0.85,
            model_name="mock_teacher",
            model_version="1.0.0"
        )
        client.generate_label.return_value = mock_label
        
        return client
    
    @pytest.fixture
    def cache_service(self):
        """In-memory cache service cho testing"""
        return InMemoryCacheService()
    
    @pytest.fixture
    def metrics_service(self):
        """Metrics service cho testing"""
        return PrometheusStyleMetricsService()
    
    @pytest.fixture
    def circuit_breaker(self):
        """Circuit breaker cho testing"""
        return CircuitBreakerService(failure_threshold=3, reset_timeout=1)
    
    @pytest.fixture
    def retry_service(self):
        """Retry service cho testing"""
        return ExponentialBackoffRetryService()
    
    @pytest.fixture
    def input_sanitizer(self):
        """Input sanitizer cho testing"""
        return InputSanitizer()
    
    @pytest.fixture
    def service_config(self):
        """Service configuration cho testing"""
        return EnhancedDistillationConfig(
            max_concurrent_requests=5,
            batch_chunk_size=10,
            cache_ttl_seconds=60,
            max_retries=2,
            circuit_breaker_failure_threshold=3
        )
    
    @pytest.fixture
    async def enhanced_service(
        self, 
        mock_teacher_client, 
        cache_service, 
        metrics_service,
        circuit_breaker,
        retry_service,
        input_sanitizer,
        service_config
    ):
        """Enhanced service instance cho testing"""
        return EnhancedDistillationService(
            teacher_client=mock_teacher_client,
            cache_service=cache_service,
            metrics=metrics_service,
            circuit_breaker=circuit_breaker,
            retry_service=retry_service,
            input_sanitizer=input_sanitizer,
            config=service_config
        )
    
    @pytest.mark.asyncio
    async def test_health_check_success(self, enhanced_service):
        """Test health check khi tất cả dependencies healthy"""
        health = await enhanced_service.health_check()
        assert health is True
    
    @pytest.mark.asyncio
    async def test_health_check_teacher_unhealthy(self, enhanced_service, mock_teacher_client):
        """Test health check khi teacher model unhealthy"""
        mock_teacher_client.health_check.return_value = False
        
        health = await enhanced_service.health_check()
        assert health is False
    
    @pytest.mark.asyncio
    async def test_generate_label_success(self, enhanced_service, mock_teacher_client):
        """Test generate label thành công"""
        input_text = "This is a positive message"
        
        label = await enhanced_service.generate_label(input_text)
        
        assert isinstance(label, TeacherLabel)
        assert label.input_text == input_text
        assert label.predicted_label == "positive"
        assert label.confidence_score == 0.85
        assert label.confidence_level == LabelConfidence.HIGH
        
        # Verify teacher client được call
        mock_teacher_client.generate_label.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_generate_label_with_cache_hit(self, enhanced_service, cache_service, metrics_service):
        """Test generate label với cache hit"""
        input_text = "cached message"
        
        # Pre-populate cache
        mock_label_data = {
            "id": "test-id",
            "input_text": input_text,
            "predicted_label": "positive",
            "confidence_score": 0.9,
            "confidence_level": "high",
            "model_name": "cached_model",
            "model_version": "1.0.0",
            "processing_time_ms": 50.0,
            "metadata": {},
            "created_at": "2024-01-01T00:00:00"
        }
        cache_key = enhanced_service._generate_cache_key(input_text)
        await cache_service.set(cache_key, mock_label_data, ttl_seconds=60)
        
        # Call service
        label = await enhanced_service.generate_label(input_text)
        
        assert label.predicted_label == "positive"
        assert label.confidence_score == 0.9
        
        # Verify cache hit metric
        cache_hits = metrics_service.get_counter_value("cache_hits", {"service": "distillation"})
        assert cache_hits > 0
    
    @pytest.mark.asyncio
    async def test_generate_label_caches_high_confidence(self, enhanced_service, cache_service, mock_teacher_client):
        """Test label với high confidence được cache"""
        input_text = "high confidence message"
        
        # Mock high confidence response
        high_confidence_label = TeacherLabel(
            input_text=input_text,
            predicted_label="positive",
            confidence_score=0.95,  # Very high confidence
            model_name="mock_teacher",
            model_version="1.0.0"
        )
        mock_teacher_client.generate_label.return_value = high_confidence_label
        
        # Generate label
        label = await enhanced_service.generate_label(input_text)
        
        # Verify label cached
        cache_key = enhanced_service._generate_cache_key(input_text)
        cached_data = await cache_service.get(cache_key)
        assert cached_data is not None
        assert cached_data["confidence_score"] == 0.95
    
    @pytest.mark.asyncio
    async def test_generate_label_input_validation(self, enhanced_service):
        """Test input validation"""
        # Test empty input
        with pytest.raises(ValueError, match="Input text không được empty"):
            await enhanced_service.generate_label("")
        
        # Test very long input
        long_input = "x" * 20000  # Longer than max_length
        with pytest.raises(ValueError, match="Input text quá dài"):
            await enhanced_service.generate_label(long_input)
    
    @pytest.mark.asyncio
    async def test_generate_label_input_sanitization(self, enhanced_service, input_sanitizer, mock_teacher_client):
        """Test input được sanitize trước khi gửi teacher model"""
        malicious_input = "<script>alert('xss')</script>positive message"
        
        await enhanced_service.generate_label(malicious_input)
        
        # Verify sanitized input được gửi cho teacher model
        call_args = mock_teacher_client.generate_label.call_args[0]
        sanitized_input = call_args[0]
        assert "<script>" not in sanitized_input
        assert "positive message" in sanitized_input
    
    @pytest.mark.asyncio
    async def test_semaphore_limits_concurrent_requests(self, enhanced_service, mock_teacher_client):
        """Test semaphore giới hạn concurrent requests"""
        # Configure semaphore với limit thấp
        enhanced_service.config.max_concurrent_requests = 2
        enhanced_service._semaphore = asyncio.Semaphore(2)
        
        # Mock slow teacher response
        async def slow_generate(*args, **kwargs):
            await asyncio.sleep(0.1)  # 100ms delay
            return TeacherLabel(
                input_text=args[0],
                predicted_label="test",
                confidence_score=0.8,
                model_name="mock",
                model_version="1.0.0"
            )
        
        mock_teacher_client.generate_label.side_effect = slow_generate
        
        # Start nhiều concurrent requests
        start_time = time.time()
        tasks = [
            enhanced_service.generate_label(f"test message {i}", use_cache=False)
            for i in range(5)
        ]
        
        results = await asyncio.gather(*tasks)
        end_time = time.time()
        
        # Verify results
        assert len(results) == 5
        assert all(isinstance(r, TeacherLabel) for r in results)
        
        # Verify semaphore worked (should take longer due to limited concurrency)
        # With semaphore=2, 5 requests should take at least 3 * 0.1 = 0.3 seconds
        total_time = end_time - start_time
        assert total_time >= 0.25  # Allow some tolerance
    
    @pytest.mark.asyncio
    async def test_retry_logic_on_failure(self, enhanced_service, mock_teacher_client, metrics_service):
        """Test retry logic khi teacher model fail"""
        call_count = 0
        
        async def failing_generate(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count <= 2:  # Fail first 2 attempts
                raise RuntimeError("Temporary failure")
            return TeacherLabel(
                input_text=args[0],
                predicted_label="recovered",
                confidence_score=0.8,
                model_name="mock",
                model_version="1.0.0"
            )
        
        mock_teacher_client.generate_label.side_effect = failing_generate
        
        # Call service
        label = await enhanced_service.generate_label("test message", use_cache=False)
        
        # Verify eventual success
        assert label.predicted_label == "recovered"
        assert call_count == 3  # 2 failures + 1 success
        
        # Verify retry metrics
        retry_attempts = metrics_service.get_counter_value("retry_attempts")
        assert retry_attempts >= 2
    
    @pytest.mark.asyncio
    async def test_circuit_breaker_opens_after_failures(self, enhanced_service, mock_teacher_client, circuit_breaker):
        """Test circuit breaker opens sau khi quá nhiều failures"""
        # Mock persistent failures
        mock_teacher_client.generate_label.side_effect = RuntimeError("Persistent failure")
        
        # Make enough failed requests để trigger circuit breaker
        for i in range(3):  # failure_threshold = 3
            with pytest.raises(RuntimeError):
                await enhanced_service.generate_label(f"test {i}", use_cache=False)
        
        # Verify circuit breaker is open
        assert circuit_breaker.is_open
        
        # Next request should be rejected by circuit breaker
        with pytest.raises(RuntimeError, match="Circuit breaker is OPEN"):
            await enhanced_service.generate_label("should fail", use_cache=False)
    
    @pytest.mark.asyncio
    async def test_batch_processing_success(self, enhanced_service, mock_teacher_client):
        """Test batch processing thành công"""
        input_texts = [f"test message {i}" for i in range(5)]
        
        # Mock successful responses
        async def mock_generate(text, config=None):
            return TeacherLabel(
                input_text=text,
                predicted_label="positive",
                confidence_score=0.8,
                model_name="mock",
                model_version="1.0.0"
            )
        
        mock_teacher_client.generate_label.side_effect = mock_generate
        
        # Process batch
        result = await enhanced_service.batch_generate_labels(input_texts)
        
        # Verify results
        assert result.total_items == 5
        assert result.successful_items == 5
        assert result.failed_items == 0
        assert result.success_rate == 1.0
        assert result.average_confidence == 0.8
    
    @pytest.mark.asyncio
    async def test_batch_processing_with_partial_failures(self, enhanced_service, mock_teacher_client):
        """Test batch processing với một số failures"""
        input_texts = [f"test message {i}" for i in range(5)]
        
        call_count = 0
        async def mixed_generate(text, config=None):
            nonlocal call_count
            call_count += 1
            if call_count % 2 == 0:  # Fail every 2nd request
                raise RuntimeError("Intermittent failure")
            return TeacherLabel(
                input_text=text,
                predicted_label="positive",
                confidence_score=0.8,
                model_name="mock",
                model_version="1.0.0"
            )
        
        mock_teacher_client.generate_label.side_effect = mixed_generate
        
        # Process batch
        result = await enhanced_service.batch_generate_labels(input_texts)
        
        # Verify partial success
        assert result.total_items == 5
        assert result.successful_items < 5  # Some should fail
        assert result.failed_items > 0
        assert 0 < result.success_rate < 1.0
    
    @pytest.mark.asyncio
    async def test_batch_processing_chunking(self, enhanced_service, mock_teacher_client):
        """Test batch processing chia thành chunks"""
        # Set small chunk size
        enhanced_service.config.batch_chunk_size = 3
        
        input_texts = [f"test message {i}" for i in range(10)]
        
        # Mock successful responses
        mock_teacher_client.generate_label.side_effect = lambda text, config=None: TeacherLabel(
            input_text=text,
            predicted_label="positive",
            confidence_score=0.8,
            model_name="mock",
            model_version="1.0.0"
        )
        
        # Process batch
        result = await enhanced_service.batch_generate_labels(input_texts)
        
        # Verify all processed
        assert result.total_items == 10
        assert result.successful_items == 10
        
        # Verify chunking worked (should have multiple calls)
        assert mock_teacher_client.generate_label.call_count == 10
    
    @pytest.mark.asyncio
    async def test_create_distillation_datapoint(self, enhanced_service, mock_teacher_client):
        """Test tạo distillation datapoint"""
        input_data = "test input for distillation"
        dataset_name = "test_dataset"
        batch_id = "test_batch_123"
        
        datapoint = await enhanced_service.create_distillation_datapoint(
            input_data=input_data,
            dataset_name=dataset_name,
            batch_id=batch_id
        )
        
        # Verify datapoint
        assert isinstance(datapoint, DistillationDatapoint)
        assert datapoint.input_data == input_data
        assert datapoint.dataset_name == dataset_name
        assert datapoint.batch_id == batch_id
        assert datapoint.has_teacher_label
        assert datapoint.teacher_label.predicted_label == "positive"
    
    @pytest.mark.asyncio
    async def test_metrics_recording(self, enhanced_service, metrics_service, mock_teacher_client):
        """Test metrics được record correctly"""
        # Reset metrics
        metrics_service.reset_all_metrics()
        
        # Generate some labels
        await enhanced_service.generate_label("test 1")
        await enhanced_service.generate_label("test 2")
        
        # Check metrics
        requests = metrics_service.get_counter_value("labels_generated")
        assert requests >= 2
        
        response_time_stats = metrics_service.get_histogram_stats("label_generation_time_ms")
        assert response_time_stats["count"] >= 2
        assert response_time_stats["avg"] > 0
    
    @pytest.mark.asyncio
    async def test_service_stats(self, enhanced_service):
        """Test service statistics"""
        stats = await enhanced_service.get_service_stats()
        
        assert "service_name" in stats
        assert "config" in stats
        assert "circuit_breaker" in stats
        assert "semaphore" in stats
        assert "timestamp" in stats
        
        # Verify config values
        assert stats["config"]["max_concurrent_requests"] == 5
        assert stats["config"]["batch_chunk_size"] == 10


@pytest.mark.asyncio
async def test_integration_with_real_components():
    """Integration test với real components (không mock)"""
    # Use real implementations
    cache_service = InMemoryCacheService()
    metrics_service = PrometheusStyleMetricsService()
    circuit_breaker = CircuitBreakerService(failure_threshold=3)
    retry_service = ExponentialBackoffRetryService()
    input_sanitizer = InputSanitizer()
    
    # Use mock teacher client với realistic behavior
    teacher_client = MockTeacherModelClient(
        simulate_delay_ms=50,
        error_rate=0.1,  # 10% error rate
        metrics=metrics_service
    )
    
    config = EnhancedDistillationConfig(
        max_concurrent_requests=3,
        batch_chunk_size=5,
        cache_ttl_seconds=30
    )
    
    service = EnhancedDistillationService(
        teacher_client=teacher_client,
        cache_service=cache_service,
        metrics=metrics_service,
        circuit_breaker=circuit_breaker,
        retry_service=retry_service,
        input_sanitizer=input_sanitizer,
        config=config
    )
    
    # Test health check
    health = await service.health_check()
    assert health is True
    
    # Test single label generation
    label = await service.generate_label("This is a great product!")
    assert isinstance(label, TeacherLabel)
    assert label.confidence_score > 0
    
    # Test batch processing
    batch_inputs = [
        "Great product!",
        "Terrible service",
        "Average experience",
        "How does this work?",
        "Best purchase ever!"
    ]
    
    batch_result = await service.batch_generate_labels(batch_inputs)
    assert batch_result.total_items == 5
    assert batch_result.successful_items > 0
    assert batch_result.success_rate > 0.5  # Allow for some failures due to error rate
    
    # Test caching behavior
    # Generate same label twice
    label1 = await service.generate_label("Cached message test")
    label2 = await service.generate_label("Cached message test")
    
    # Second should be faster (from cache) if high confidence
    if label1.is_cacheable:
        assert label2.processing_time_ms < label1.processing_time_ms
    
    # Check metrics
    all_metrics = metrics_service.get_all_metrics()
    assert "counters" in all_metrics
    assert "histograms" in all_metrics
    assert len(all_metrics["counters"]) > 0