"""
Distillation Repository implementation.
Data persistence layer cho distillation datapoints và batch results.
"""

import json
import os
from datetime import datetime
from typing import Any, Optional

import aiosqlite

from core.domain.entities import BatchProcessingResult, DistillationDatapoint, TeacherLabel
from core.domain.interfaces import BaseRepository, DistillationRepositoryInterface, MetricsServiceInterface


class SQLiteDistillationRepository(DistillationRepositoryInterface, BaseRepository):
    """
    SQLite-based repository cho distillation data.
    Phù hợp cho development và small-scale deployment.
    """

    def __init__(
        self,
        db_path: str = "distillation.db",
        metrics: Optional[MetricsServiceInterface] = None
    ):
        self.db_path = db_path
        self.metrics = metrics
        self._initialized = False

    async def _ensure_initialized(self) -> None:
        """Ensure database tables are created"""
        if self._initialized:
            return

        await self._create_tables()
        self._initialized = True

    async def _create_tables(self) -> None:
        """Tạo database tables nếu chưa có"""
        async with aiosqlite.connect(self.db_path) as db:
            # Table cho distillation datapoints
            await db.execute("""
                CREATE TABLE IF NOT EXISTS distillation_datapoints (
                    id TEXT PRIMARY KEY,
                    input_data TEXT NOT NULL,
                    teacher_label_json TEXT,
                    student_prediction TEXT,
                    student_confidence REAL,
                    loss_value REAL,
                    dataset_name TEXT,
                    batch_id TEXT,
                    created_at TEXT,
                    updated_at TEXT
                )
            """)

            # Table cho teacher labels (normalized)
            await db.execute("""
                CREATE TABLE IF NOT EXISTS teacher_labels (
                    id TEXT PRIMARY KEY,
                    input_text TEXT NOT NULL,
                    predicted_label TEXT,
                    confidence_score REAL,
                    confidence_level TEXT,
                    model_name TEXT,
                    model_version TEXT,
                    processing_time_ms REAL,
                    metadata_json TEXT,
                    created_at TEXT
                )
            """)

            # Table cho batch processing results
            await db.execute("""
                CREATE TABLE IF NOT EXISTS batch_processing_results (
                    batch_id TEXT PRIMARY KEY,
                    total_items INTEGER,
                    successful_items INTEGER,
                    failed_items INTEGER,
                    processing_time_ms REAL,
                    average_confidence REAL,
                    cached_items INTEGER,
                    errors_json TEXT,
                    created_at TEXT
                )
            """)

            # Indexes cho performance
            await db.execute("CREATE INDEX IF NOT EXISTS idx_datapoints_batch_id ON distillation_datapoints(batch_id)")
            await db.execute("CREATE INDEX IF NOT EXISTS idx_datapoints_dataset ON distillation_datapoints(dataset_name)")
            await db.execute("CREATE INDEX IF NOT EXISTS idx_datapoints_created_at ON distillation_datapoints(created_at)")
            await db.execute("CREATE INDEX IF NOT EXISTS idx_labels_input_text ON teacher_labels(input_text)")
            await db.execute("CREATE INDEX IF NOT EXISTS idx_labels_confidence ON teacher_labels(confidence_score)")

            await db.commit()

    async def save_datapoint(self, datapoint: DistillationDatapoint) -> bool:
        """Lưu distillation datapoint"""
        await self._ensure_initialized()

        try:
            async with aiosqlite.connect(self.db_path) as db:
                # Save teacher label riêng nếu có
                teacher_label_json = None
                if datapoint.teacher_label:
                    await self._save_teacher_label(db, datapoint.teacher_label)
                    teacher_label_json = json.dumps(datapoint.teacher_label.to_dict())

                # Save datapoint
                await db.execute("""
                    INSERT OR REPLACE INTO distillation_datapoints 
                    (id, input_data, teacher_label_json, student_prediction, student_confidence,
                     loss_value, dataset_name, batch_id, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    datapoint.id,
                    datapoint.input_data,
                    teacher_label_json,
                    datapoint.student_prediction,
                    datapoint.student_confidence,
                    datapoint.loss_value,
                    datapoint.dataset_name,
                    datapoint.batch_id,
                    datapoint.created_at.isoformat(),
                    datapoint.updated_at.isoformat()
                ))

                await db.commit()

                if self.metrics:
                    self.metrics.increment_counter("datapoints_saved", {"repository": "sqlite"})

                return True

        except Exception:
            if self.metrics:
                self.metrics.increment_counter("datapoint_save_errors", {"repository": "sqlite"})
            return False

    async def _save_teacher_label(self, db: aiosqlite.Connection, label: TeacherLabel) -> None:
        """Internal method để save teacher label"""
        await db.execute("""
            INSERT OR REPLACE INTO teacher_labels
            (id, input_text, predicted_label, confidence_score, confidence_level,
             model_name, model_version, processing_time_ms, metadata_json, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            label.id,
            label.input_text,
            label.predicted_label,
            label.confidence_score,
            label.confidence_level.value,
            label.model_name,
            label.model_version,
            label.processing_time_ms,
            json.dumps(label.metadata),
            label.created_at.isoformat()
        ))

    async def save_datapoints(self, datapoints: list[DistillationDatapoint]) -> bool:
        """Lưu batch distillation datapoints"""
        await self._ensure_initialized()

        if not datapoints:
            return True

        try:
            async with aiosqlite.connect(self.db_path) as db:
                for datapoint in datapoints:
                    # Save teacher label riêng nếu có
                    teacher_label_json = None
                    if datapoint.teacher_label:
                        await self._save_teacher_label(db, datapoint.teacher_label)
                        teacher_label_json = json.dumps(datapoint.teacher_label.to_dict())

                    # Save datapoint
                    await db.execute("""
                        INSERT OR REPLACE INTO distillation_datapoints 
                        (id, input_data, teacher_label_json, student_prediction, student_confidence,
                         loss_value, dataset_name, batch_id, created_at, updated_at)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        datapoint.id,
                        datapoint.input_data,
                        teacher_label_json,
                        datapoint.student_prediction,
                        datapoint.student_confidence,
                        datapoint.loss_value,
                        datapoint.dataset_name,
                        datapoint.batch_id,
                        datapoint.created_at.isoformat(),
                        datapoint.updated_at.isoformat()
                    ))

                await db.commit()

                if self.metrics:
                    self.metrics.increment_counter("datapoints_batch_saved", {
                        "repository": "sqlite",
                        "count": str(len(datapoints))
                    })

                return True

        except Exception:
            if self.metrics:
                self.metrics.increment_counter("datapoints_batch_save_errors", {"repository": "sqlite"})
            return False

    async def get_datapoint(self, datapoint_id: str) -> Optional[DistillationDatapoint]:
        """Lấy distillation datapoint theo ID"""
        await self._ensure_initialized()

        try:
            async with aiosqlite.connect(self.db_path) as db:
                async with db.execute("""
                    SELECT id, input_data, teacher_label_json, student_prediction, student_confidence,
                           loss_value, dataset_name, batch_id, created_at, updated_at
                    FROM distillation_datapoints 
                    WHERE id = ?
                """, (datapoint_id,)) as cursor:
                    row = await cursor.fetchone()

                    if not row:
                        return None

                    return self._row_to_datapoint(row)

        except Exception:
            if self.metrics:
                self.metrics.increment_counter("datapoint_get_errors", {"repository": "sqlite"})
            return None

    async def get_datapoints_by_batch(self, batch_id: str) -> list[DistillationDatapoint]:
        """Lấy tất cả datapoints trong một batch"""
        await self._ensure_initialized()

        try:
            async with aiosqlite.connect(self.db_path) as db:
                async with db.execute("""
                    SELECT id, input_data, teacher_label_json, student_prediction, student_confidence,
                           loss_value, dataset_name, batch_id, created_at, updated_at
                    FROM distillation_datapoints 
                    WHERE batch_id = ?
                    ORDER BY created_at
                """, (batch_id,)) as cursor:
                    rows = await cursor.fetchall()

                    datapoints = [self._row_to_datapoint(row) for row in rows]

                    if self.metrics:
                        self.metrics.increment_counter("datapoints_batch_retrieved", {
                            "repository": "sqlite",
                            "count": str(len(datapoints))
                        })

                    return datapoints

        except Exception:
            if self.metrics:
                self.metrics.increment_counter("datapoints_batch_get_errors", {"repository": "sqlite"})
            return []

    def _row_to_datapoint(self, row) -> DistillationDatapoint:
        """Convert database row to DistillationDatapoint"""
        (id_, input_data, teacher_label_json, student_prediction, student_confidence,
         loss_value, dataset_name, batch_id, created_at, updated_at) = row

        # Parse teacher label nếu có
        teacher_label = None
        if teacher_label_json:
            label_data = json.loads(teacher_label_json)
            teacher_label = TeacherLabel(
                id=label_data["id"],
                input_text=label_data["input_text"],
                predicted_label=label_data["predicted_label"],
                confidence_score=label_data["confidence_score"],
                model_name=label_data["model_name"],
                model_version=label_data["model_version"],
                processing_time_ms=label_data["processing_time_ms"],
                metadata=label_data["metadata"],
                created_at=datetime.fromisoformat(label_data["created_at"])
            )

        return DistillationDatapoint(
            id=id_,
            input_data=input_data,
            teacher_label=teacher_label,
            student_prediction=student_prediction,
            student_confidence=student_confidence,
            loss_value=loss_value,
            dataset_name=dataset_name,
            batch_id=batch_id,
            created_at=datetime.fromisoformat(created_at),
            updated_at=datetime.fromisoformat(updated_at)
        )

    async def save_batch_result(self, result: BatchProcessingResult) -> bool:
        """Lưu kết quả batch processing"""
        await self._ensure_initialized()

        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute("""
                    INSERT OR REPLACE INTO batch_processing_results
                    (batch_id, total_items, successful_items, failed_items, processing_time_ms,
                     average_confidence, cached_items, errors_json, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    result.batch_id,
                    result.total_items,
                    result.successful_items,
                    result.failed_items,
                    result.processing_time_ms,
                    result.average_confidence,
                    result.cached_items,
                    json.dumps(result.errors),
                    result.created_at.isoformat()
                ))

                await db.commit()

                if self.metrics:
                    self.metrics.increment_counter("batch_results_saved", {"repository": "sqlite"})

                return True

        except Exception:
            if self.metrics:
                self.metrics.increment_counter("batch_result_save_errors", {"repository": "sqlite"})
            return False

    async def get_batch_result(self, batch_id: str) -> Optional[BatchProcessingResult]:
        """Lấy batch processing result theo ID"""
        await self._ensure_initialized()

        try:
            async with aiosqlite.connect(self.db_path) as db:
                async with db.execute("""
                    SELECT batch_id, total_items, successful_items, failed_items, processing_time_ms,
                           average_confidence, cached_items, errors_json, created_at
                    FROM batch_processing_results 
                    WHERE batch_id = ?
                """, (batch_id,)) as cursor:
                    row = await cursor.fetchone()

                    if not row:
                        return None

                    (batch_id, total_items, successful_items, failed_items, processing_time_ms,
                     average_confidence, cached_items, errors_json, created_at) = row

                    return BatchProcessingResult(
                        batch_id=batch_id,
                        total_items=total_items,
                        successful_items=successful_items,
                        failed_items=failed_items,
                        processing_time_ms=processing_time_ms,
                        average_confidence=average_confidence,
                        cached_items=cached_items,
                        errors=json.loads(errors_json),
                        created_at=datetime.fromisoformat(created_at)
                    )

        except Exception:
            if self.metrics:
                self.metrics.increment_counter("batch_result_get_errors", {"repository": "sqlite"})
            return None

    async def health_check(self) -> bool:
        """Health check cho repository"""
        try:
            await self._ensure_initialized()
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute("SELECT 1")
            return True
        except Exception:
            return False

    async def get_stats(self) -> dict[str, Any]:
        """Lấy repository statistics"""
        await self._ensure_initialized()

        try:
            async with aiosqlite.connect(self.db_path) as db:
                # Count datapoints
                async with db.execute("SELECT COUNT(*) FROM distillation_datapoints") as cursor:
                    datapoint_count = (await cursor.fetchone())[0]

                # Count teacher labels
                async with db.execute("SELECT COUNT(*) FROM teacher_labels") as cursor:
                    label_count = (await cursor.fetchone())[0]

                # Count batch results
                async with db.execute("SELECT COUNT(*) FROM batch_processing_results") as cursor:
                    batch_count = (await cursor.fetchone())[0]

                # Database file size
                db_size = os.path.getsize(self.db_path) if os.path.exists(self.db_path) else 0

                return {
                    "repository_type": "sqlite",
                    "db_path": self.db_path,
                    "db_size_bytes": db_size,
                    "datapoint_count": datapoint_count,
                    "teacher_label_count": label_count,
                    "batch_result_count": batch_count,
                }

        except Exception as e:
            return {"repository_type": "sqlite", "error": str(e)}


# Factory function
def create_distillation_repository(
    repository_type: str = "sqlite",
    config: Optional[dict[str, Any]] = None,
    metrics: Optional[MetricsServiceInterface] = None
) -> DistillationRepositoryInterface:
    """
    Factory function để tạo distillation repository.
    
    Args:
        repository_type: "sqlite" (có thể extend sau để support PostgreSQL, MongoDB, etc.)
        config: Configuration dict
        metrics: Metrics service
        
    Returns:
        DistillationRepositoryInterface implementation
    """
    config = config or {}

    if repository_type.lower() == "sqlite":
        return SQLiteDistillationRepository(
            db_path=config.get("db_path", "distillation.db"),
            metrics=metrics
        )
    else:
        raise ValueError(f"Unsupported repository type: {repository_type}")
