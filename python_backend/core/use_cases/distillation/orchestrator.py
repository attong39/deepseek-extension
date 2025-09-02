"""
Distillation Orchestrator - Main use case coordinator.
Coordinate giữa enhanced service, repository, và các external dependencies.
"""

import asyncio
import time
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from core.domain.entities import BatchProcessingResult, DistillationDatapoint
from core.domain.interfaces import DistillationRepositoryInterface, MetricsServiceInterface
from core.services.enhanced_service import EnhancedDistillationService


class DistillationOrchestrator:
    """
    Main orchestrator cho distillation workflows.
    
    Responsibilities:
    1. Coordinate between enhanced service và repository
    2. Implement high-level business workflows
    3. Handle complex error scenarios
    4. Provide monitoring và observability
    """

    def __init__(
        self,
        enhanced_service: EnhancedDistillationService,
        repository: DistillationRepositoryInterface,
        metrics: MetricsServiceInterface,
        config: Optional[Dict[str, Any]] = None
    ):
        self.enhanced_service = enhanced_service
        self.repository = repository
        self.metrics = metrics
        self.config = config or {}

        # Default workflow config
        self.default_batch_size = self.config.get("default_batch_size", 100)
        self.auto_persist = self.config.get("auto_persist", True)
        self.enable_background_processing = self.config.get("enable_background_processing", True)

    async def process_single_input(
        self,
        input_text: str,
        dataset_name: str = "",
        model_config: Optional[Dict[str, Any]] = None,
        persist: bool = True
    ) -> DistillationDatapoint:
        """
        Process single input với full workflow.
        
        Args:
            input_text: Text cần process
            dataset_name: Tên dataset
            model_config: Config cho teacher model
            persist: Có lưu vào repository không
            
        Returns:
            DistillationDatapoint hoàn chỉnh
        """
        start_time = time.time()

        try:
            self.metrics.increment_counter("orchestrator_single_requests")

            # Tạo datapoint với teacher label
            datapoint = await self.enhanced_service.create_distillation_datapoint(
                input_data=input_text,
                dataset_name=dataset_name,
                model_config=model_config
            )

            # Persist nếu requested
            if persist and self.auto_persist:
                saved = await self.repository.save_datapoint(datapoint)
                if not saved:
                    self.metrics.increment_counter("orchestrator_persistence_failures")
                    # Log warning nhưng không fail

            processing_time = (time.time() - start_time) * 1000
            self.metrics.record_histogram("orchestrator_single_processing_time_ms", processing_time)
            self.metrics.increment_counter("orchestrator_single_successes")

            return datapoint

        except Exception as e:
            processing_time = (time.time() - start_time) * 1000
            self.metrics.record_histogram("orchestrator_single_processing_time_ms", processing_time)
            self.metrics.increment_counter("orchestrator_single_errors", {"error_type": type(e).__name__})
            raise

    async def process_batch(
        self,
        input_texts: List[str],
        dataset_name: str = "",
        model_config: Optional[Dict[str, Any]] = None,
        batch_id: Optional[str] = None,
        persist: bool = True
    ) -> BatchProcessingResult:
        """
        Process batch inputs với full workflow và optimization.
        
        Args:
            input_texts: List các text cần process
            dataset_name: Tên dataset
            model_config: Config cho teacher model
            batch_id: ID cho batch (auto-generate nếu None)
            persist: Có lưu vào repository không
            
        Returns:
            BatchProcessingResult với detailed metrics
        """
        start_time = time.time()
        batch_id = batch_id or str(uuid.uuid4())

        if not input_texts:
            raise ValueError("Input texts list không được empty")

        try:
            self.metrics.increment_counter("orchestrator_batch_requests", {
                "batch_size": str(len(input_texts)),
                "dataset": dataset_name
            })

            # Generate teacher labels với enhanced service
            batch_result = await self.enhanced_service.batch_generate_labels(
                input_texts=input_texts,
                model_config=model_config,
                batch_id=batch_id
            )

            # Tạo datapoints từ successful labels
            datapoints = []
            if batch_result.successful_items > 0:
                # Cần map labels with original inputs (assume same order)
                # Note: Trong production, cần handle failed items properly
                successful_count = 0
                for i, input_text in enumerate(input_texts):
                    if successful_count < batch_result.successful_items:
                        # Simulate label generation (trong thực tế sẽ có proper mapping)
                        label = await self.enhanced_service.generate_label(input_text, model_config)
                        datapoint = DistillationDatapoint(
                            input_data=input_text,
                            teacher_label=label,
                            dataset_name=dataset_name,
                            batch_id=batch_id
                        )
                        datapoints.append(datapoint)
                        successful_count += 1

            # Persist batch nếu requested
            if persist and self.auto_persist and datapoints:
                saved = await self.repository.save_datapoints(datapoints)
                if saved:
                    # Cũng save batch result
                    await self.repository.save_batch_result(batch_result)
                else:
                    self.metrics.increment_counter("orchestrator_batch_persistence_failures")

            processing_time = (time.time() - start_time) * 1000
            self.metrics.record_histogram("orchestrator_batch_processing_time_ms", processing_time)
            self.metrics.increment_counter("orchestrator_batch_successes")

            return batch_result

        except Exception as e:
            processing_time = (time.time() - start_time) * 1000
            self.metrics.record_histogram("orchestrator_batch_processing_time_ms", processing_time)
            self.metrics.increment_counter("orchestrator_batch_errors", {"error_type": type(e).__name__})
            raise

    async def create_training_dataset(
        self,
        input_texts: List[str],
        dataset_name: str,
        model_config: Optional[Dict[str, Any]] = None,
        chunk_size: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Tạo complete training dataset với chunked processing.
        
        Args:
            input_texts: List tất cả inputs
            dataset_name: Tên dataset
            model_config: Config cho teacher model
            chunk_size: Size của mỗi chunk (default từ config)
            
        Returns:
            Dataset creation summary
        """
        if not input_texts:
            raise ValueError("Input texts list không được empty")

        chunk_size = chunk_size or self.default_batch_size
        total_inputs = len(input_texts)

        self.metrics.increment_counter("orchestrator_dataset_creation_started", {
            "dataset": dataset_name,
            "total_inputs": str(total_inputs),
            "chunk_size": str(chunk_size)
        })

        start_time = time.time()
        all_batch_results = []
        total_successful = 0
        total_failed = 0

        try:
            # Process theo chunks
            chunks = [
                input_texts[i:i + chunk_size]
                for i in range(0, len(input_texts), chunk_size)
            ]

            for chunk_idx, chunk in enumerate(chunks):
                chunk_batch_id = f"{dataset_name}_chunk_{chunk_idx}_{int(time.time())}"

                try:
                    batch_result = await self.process_batch(
                        input_texts=chunk,
                        dataset_name=dataset_name,
                        model_config=model_config,
                        batch_id=chunk_batch_id,
                        persist=True
                    )

                    all_batch_results.append(batch_result)
                    total_successful += batch_result.successful_items
                    total_failed += batch_result.failed_items

                    self.metrics.increment_counter("orchestrator_dataset_chunks_completed", {
                        "dataset": dataset_name
                    })

                    # Small delay để không overwhelm system
                    await asyncio.sleep(0.1)

                except Exception as e:
                    total_failed += len(chunk)
                    self.metrics.increment_counter("orchestrator_dataset_chunk_errors", {
                        "dataset": dataset_name,
                        "error_type": type(e).__name__
                    })
                    # Continue với remaining chunks
                    continue

            processing_time = (time.time() - start_time) * 1000

            # Aggregate metrics
            total_processing_time = sum(result.processing_time_ms for result in all_batch_results)
            total_cached_items = sum(result.cached_items for result in all_batch_results)
            average_confidence = (
                sum(result.average_confidence * result.successful_items for result in all_batch_results) /
                total_successful if total_successful > 0 else 0.0
            )

            dataset_summary = {
                "dataset_name": dataset_name,
                "total_inputs": total_inputs,
                "successful_items": total_successful,
                "failed_items": total_failed,
                "success_rate": total_successful / total_inputs if total_inputs > 0 else 0.0,
                "total_processing_time_ms": processing_time,
                "teacher_processing_time_ms": total_processing_time,
                "cached_items": total_cached_items,
                "cache_hit_rate": total_cached_items / total_inputs if total_inputs > 0 else 0.0,
                "average_confidence": average_confidence,
                "chunks_processed": len(all_batch_results),
                "chunk_size": chunk_size,
                "created_at": datetime.utcnow().isoformat(),
                "batch_results": [result.to_dict() for result in all_batch_results]
            }

            self.metrics.record_histogram("orchestrator_dataset_creation_time_ms", processing_time)
            self.metrics.record_histogram("orchestrator_dataset_success_rate", dataset_summary["success_rate"])
            self.metrics.increment_counter("orchestrator_dataset_creation_completed", {
                "dataset": dataset_name,
                "success": "true" if dataset_summary["success_rate"] > 0.8 else "false"
            })

            return dataset_summary

        except Exception as e:
            processing_time = (time.time() - start_time) * 1000
            self.metrics.record_histogram("orchestrator_dataset_creation_time_ms", processing_time)
            self.metrics.increment_counter("orchestrator_dataset_creation_errors", {
                "dataset": dataset_name,
                "error_type": type(e).__name__
            })
            raise

    async def get_dataset_statistics(self, dataset_name: str) -> Dict[str, Any]:
        """Lấy statistics cho một dataset"""
        try:
            # Trong production, repository sẽ có methods để query statistics
            # Hiện tại implement basic version

            stats = {
                "dataset_name": dataset_name,
                "total_datapoints": 0,
                "confidence_distribution": {},
                "model_distribution": {},
                "timestamp": datetime.utcnow().isoformat()
            }

            # Note: Cần implement proper statistics queries trong repository
            # Đây là placeholder implementation

            return stats

        except Exception as e:
            self.metrics.increment_counter("orchestrator_stats_errors", {
                "dataset": dataset_name,
                "error_type": type(e).__name__
            })
            raise

    async def health_check(self) -> Dict[str, Any]:
        """Comprehensive health check cho toàn bộ system"""
        health_status = {
            "orchestrator": "healthy",
            "enhanced_service": "unknown",
            "repository": "unknown",
            "timestamp": datetime.utcnow().isoformat()
        }

        try:
            # Check enhanced service
            service_healthy = await self.enhanced_service.health_check()
            health_status["enhanced_service"] = "healthy" if service_healthy else "unhealthy"

            # Check repository
            repo_healthy = await self.repository.health_check()
            health_status["repository"] = "healthy" if repo_healthy else "unhealthy"

            # Overall health
            overall_healthy = service_healthy and repo_healthy
            health_status["overall"] = "healthy" if overall_healthy else "unhealthy"

            # Add service stats
            health_status["service_stats"] = await self.enhanced_service.get_service_stats()

            self.metrics.set_gauge("orchestrator_health", 1.0 if overall_healthy else 0.0)

            return health_status

        except Exception as e:
            health_status["orchestrator"] = "unhealthy"
            health_status["error"] = str(e)
            self.metrics.set_gauge("orchestrator_health", 0.0)
            return health_status
