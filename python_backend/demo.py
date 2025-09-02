#!/usr/bin/env python3
"""
Demo script cho Enhanced Distillation Service.
Demonstrates all optimizations và features.
"""

import asyncio
import sys
import time
from typing import Any

# Add python_backend to path
sys.path.insert(0, '.')

from core.services.enhanced_service import EnhancedDistillationService, EnhancedDistillationConfig
from core.services.cache_service import create_cache_service
from core.services.metrics_service import create_metrics_service
from infrastructure.reliability import (
    CircuitBreakerService,
    ExponentialBackoffRetryService, 
    InputSanitizer
)
from infrastructure.external.teacher_model_client import create_teacher_model_client
from infrastructure.repositories.distillation_repository import create_distillation_repository
from core.use_cases.distillation.orchestrator import DistillationOrchestrator


async def demo_enhanced_service():
    """Demo các features của Enhanced Distillation Service"""
    print("🚀 Starting Enhanced Distillation Service Demo")
    print("=" * 60)
    
    # 1. Setup dependencies
    print("📋 Setting up dependencies...")
    cache_service = create_cache_service("memory")
    metrics_service = create_metrics_service(enabled=True)
    circuit_breaker = CircuitBreakerService(failure_threshold=3, reset_timeout=5)
    retry_service = ExponentialBackoffRetryService(metrics_service)
    input_sanitizer = InputSanitizer(metrics_service)
    
    # Use mock teacher client với realistic behavior
    teacher_client = create_teacher_model_client(
        "mock", 
        {"simulate_delay_ms": 50, "error_rate": 0.1},
        metrics_service
    )
    
    # Enhanced service config
    config = EnhancedDistillationConfig(
        max_concurrent_requests=5,
        batch_chunk_size=10,
        cache_ttl_seconds=60,
        max_retries=2
    )
    
    # Create enhanced service
    enhanced_service = EnhancedDistillationService(
        teacher_client=teacher_client,
        cache_service=cache_service,
        metrics=metrics_service,
        circuit_breaker=circuit_breaker,
        retry_service=retry_service,
        input_sanitizer=input_sanitizer,
        config=config
    )
    
    print("✅ Dependencies setup complete!")
    print()
    
    # 2. Health check
    print("🏥 Running health check...")
    health = await enhanced_service.health_check()
    print(f"Health status: {'✅ Healthy' if health else '❌ Unhealthy'}")
    print()
    
    # 3. Single label generation
    print("🔖 Testing single label generation...")
    test_inputs = [
        "This is an excellent product!",
        "Terrible customer service",
        "How does this feature work?",
        "Average performance overall"
    ]
    
    for input_text in test_inputs:
        start_time = time.time()
        label = await enhanced_service.generate_label(input_text)
        end_time = time.time()
        
        print(f"Input: '{input_text[:50]}...'")
        print(f"  Label: {label.predicted_label}")
        print(f"  Confidence: {label.confidence_score:.3f} ({label.confidence_level.value})")
        print(f"  Processing time: {(end_time - start_time)*1000:.1f}ms")
        print(f"  Cacheable: {'Yes' if label.is_cacheable else 'No'}")
        print()
    
    # 4. Test caching behavior
    print("💾 Testing cache behavior...")
    print("Generating same label twice to test caching...")
    
    # First call
    start_time = time.time()
    label1 = await enhanced_service.generate_label("Great product for testing cache!")
    time1 = time.time() - start_time
    
    # Second call (should hit cache if high confidence)
    start_time = time.time()
    label2 = await enhanced_service.generate_label("Great product for testing cache!")
    time2 = time.time() - start_time
    
    print(f"First call: {time1*1000:.1f}ms, Confidence: {label1.confidence_score:.3f}")
    print(f"Second call: {time2*1000:.1f}ms, Confidence: {label2.confidence_score:.3f}")
    if label1.is_cacheable and time2 < time1:
        print("✅ Cache hit detected!")
    else:
        print("ℹ️  No cache hit (low confidence or cache miss)")
    print()
    
    # 5. Batch processing
    print("📦 Testing batch processing...")
    batch_inputs = [
        "Excellent service quality",
        "Poor user experience", 
        "What are the pricing options?",
        "Decent functionality overall",
        "Amazing customer support",
        "Buggy software implementation",
        "How to configure this setting?",
        "Standard performance metrics"
    ]
    
    start_time = time.time()
    batch_result = await enhanced_service.batch_generate_labels(batch_inputs)
    end_time = time.time()
    
    print(f"Batch results:")
    print(f"  Total items: {batch_result.total_items}")
    print(f"  Successful: {batch_result.successful_items}")
    print(f"  Failed: {batch_result.failed_items}")
    print(f"  Success rate: {batch_result.success_rate:.1%}")
    print(f"  Average confidence: {batch_result.average_confidence:.3f}")
    print(f"  Cache hits: {batch_result.cached_items}")
    print(f"  Cache hit rate: {batch_result.cache_hit_rate:.1%}")
    print(f"  Total processing time: {(end_time - start_time)*1000:.1f}ms")
    print()
    
    # 6. Input sanitization test
    print("🛡️  Testing input sanitization...")
    malicious_inputs = [
        "<script>alert('xss')</script>Good product",
        "Nice product; DROP TABLE users;--",
        "Great item && curl evil.com",
        "Normal input text"
    ]
    
    for malicious_input in malicious_inputs:
        try:
            label = await enhanced_service.generate_label(malicious_input)
            print(f"✅ Sanitized: '{malicious_input[:30]}...' -> Label: {label.predicted_label}")
        except ValueError as e:
            print(f"⚠️  Blocked: '{malicious_input[:30]}...' -> {str(e)}")
    print()
    
    # 7. Metrics summary
    print("📊 Metrics Summary:")
    all_metrics = metrics_service.get_all_metrics()
    
    # Display key counters
    if "counters" in all_metrics:
        print("  Counters:")
        for metric_name, values in all_metrics["counters"].items():
            if "labels_generated" in metric_name or "cache_" in metric_name:
                for labels, count in values.items():
                    print(f"    {metric_name}[{labels}]: {count}")
    
    # Display key histograms
    if "histograms" in all_metrics:
        print("  Performance metrics:")
        for metric_name, values in all_metrics["histograms"].items():
            if "time_ms" in metric_name:
                for labels, stats in values.items():
                    if isinstance(stats, dict) and "avg" in stats:
                        print(f"    {metric_name}[{labels}]: avg={stats['avg']:.1f}ms")
    print()
    
    # 8. Service stats
    print("⚙️  Service Statistics:")
    service_stats = await enhanced_service.get_service_stats()
    print(f"  Circuit breaker: {'Open' if service_stats['circuit_breaker']['is_open'] else 'Closed'}")
    print(f"  Failure count: {service_stats['circuit_breaker']['failure_count']}")
    print(f"  Available permits: {service_stats['semaphore']['available_permits']}/{service_stats['semaphore']['max_permits']}")
    print()
    
    print("🎉 Demo completed successfully!")
    print("=" * 60)


async def demo_orchestrator():
    """Demo DistillationOrchestrator"""
    print("\n🎭 Testing Distillation Orchestrator")
    print("=" * 60)
    
    # Setup components (reuse from above)
    cache_service = create_cache_service("memory")
    metrics_service = create_metrics_service(enabled=True)
    circuit_breaker = CircuitBreakerService(failure_threshold=3)
    retry_service = ExponentialBackoffRetryService(metrics_service)
    input_sanitizer = InputSanitizer(metrics_service)
    teacher_client = create_teacher_model_client("mock", {"error_rate": 0.05}, metrics_service)
    
    config = EnhancedDistillationConfig(max_concurrent_requests=3, batch_chunk_size=5)
    
    enhanced_service = EnhancedDistillationService(
        teacher_client=teacher_client,
        cache_service=cache_service,
        metrics=metrics_service,
        circuit_breaker=circuit_breaker,
        retry_service=retry_service,
        input_sanitizer=input_sanitizer,
        config=config
    )
    
    # Repository
    repository = create_distillation_repository("sqlite", {"db_path": ":memory:"}, metrics_service)
    
    # Orchestrator
    orchestrator = DistillationOrchestrator(
        enhanced_service=enhanced_service,
        repository=repository,
        metrics=metrics_service,
        config={"default_batch_size": 5}
    )
    
    # Test orchestrator health
    health_status = await orchestrator.health_check()
    print(f"Orchestrator health: {'✅ Healthy' if health_status['overall'] == 'healthy' else '❌ Unhealthy'}")
    
    # Test single processing
    print("\n📝 Processing single input...")
    datapoint = await orchestrator.process_single_input(
        "Test input for orchestrator",
        dataset_name="demo_dataset"
    )
    print(f"Created datapoint with ID: {datapoint.id}")
    print(f"Teacher label: {datapoint.teacher_label.predicted_label}")
    
    # Test dataset creation
    print("\n📚 Creating training dataset...")
    dataset_inputs = [
        "Excellent product quality",
        "Poor customer service", 
        "How much does this cost?",
        "Average user experience",
        "Outstanding performance results"
    ]
    
    dataset_summary = await orchestrator.create_training_dataset(
        input_texts=dataset_inputs,
        dataset_name="demo_training_set",
        chunk_size=3
    )
    
    print(f"Dataset creation results:")
    print(f"  Dataset: {dataset_summary['dataset_name']}")
    print(f"  Success rate: {dataset_summary['success_rate']:.1%}")
    print(f"  Processing time: {dataset_summary['total_processing_time_ms']:.1f}ms")
    print(f"  Chunks processed: {dataset_summary['chunks_processed']}")
    
    print("\n🎉 Orchestrator demo completed!")


if __name__ == "__main__":
    print("🔥 Enhanced Distillation Service - Full Demo")
    print("This demonstrates all optimizations and features implemented.")
    print()
    
    # Run demos
    asyncio.run(demo_enhanced_service())
    asyncio.run(demo_orchestrator())