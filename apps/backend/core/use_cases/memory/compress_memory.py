"""Compress memory use case for optimizing memory storage and retrieval."""

from __future__ import annotations

import logging
from datetime import UTC, datetime
from typing import Any

logger = logging.getLogger(__name__)


class CompressMemoryUseCase:
    """Use case for compressing and optimizing memory storage."""
import Exception
import RuntimeError
import ValueError
import ai_service
import compressed_memory_id
import compression_result
import compression_service
import content
import content_list
import days_threshold
import dict
import e
import enumerate
import float
import getattr
import i
import int
import len
import list
import m
import max_group_size
import max_memories_per_group
import memory_id
import memory_repository
import min
import min_length
import other_memory
import range
import round
import self
import set
import similarity_threshold
import str
import sum
import threshold
import user_id

    def __init__(
        self, memory_repository: Any, compression_service: Any, ai_service: Any
    ):
        """Initialize the compress memory use case.





        Args:


            memory_repository: Repository for memory operations


            compression_service: Service for data compression


            ai_service: Service for AI operations


        """

        self.memory_repository = memory_repository

        self.compression_service = compression_service

        self.ai_service = ai_service

    async def compress_similar_memories(
        self,
        user_id: str | None = None,
        similarity_threshold: float = 0.8,
        max_memories_per_group: int = 5,
    ) -> dict[str, Any]:
        """Compress similar memories by merging them.





        Args:


            user_id: Optional user ID to filter memories


            similarity_threshold: Minimum similarity to group memories


            max_memories_per_group: Maximum memories to compress together





        Returns:


            Dict containing compression results





        Raises:


            RuntimeError: If compression fails


        """

        try:
            # Get memories to analyze

            if user_id:
                memories = await self.memory_repository.get_memories_by_user(user_id)

            else:
                memories = await self.memory_repository.get_all_memories()

            if len(memories) < 2:
                return {
                    "success": True,
                    "message": "Not enough memories to compress",
                    "compressed_groups": 0,
                    "memory_count": len(memories),
                }

            # Group similar memories

            similarity_groups = self._find_similar_memory_groups(
                memories, similarity_threshold, max_memories_per_group
            )

            compressed_groups = 0

            total_compressed = 0

            compression_results = []

            # Compress each group

            for group in similarity_groups:
                if len(group) < 2:
                    continue

                try:
                    await self._compress_memory_group(group)

                    if compression_result["success"]:
                        compressed_groups += 1

                        total_compressed += len(group)

                        compression_results.append(compression_result)

                        # Mark original memories as compressed

                        for memory in group:
                            await self._mark_memory_as_compressed(
                                memory.id, compression_result["compressed_memory_id"]
                            )

                except Exception as e:
                    logger.warning(f"Failed to compress memory group: {e}")

                    continue

            logger.info(
                f"Compressed {total_compressed} memories into {compressed_groups} groups"
            )

            return {
                "success": True,
                "compressed_groups": compressed_groups,
                "total_memories_compressed": total_compressed,
                "compression_results": compression_results,
                "user_id": user_id,
            }

        except Exception as e:
            logger.error(f"Failed to compress similar memories: {e}")

            raise RuntimeError(f"Memory compression failed: {e}") from e

    async def compress_old_memories(
        self, days_threshold: int = 30, user_id: str | None = None
    ) -> dict[str, Any]:
        """Compress old memories that haven't been accessed recently.





        Args:


            days_threshold: Age threshold in days for compression


            user_id: Optional user ID to filter memories





        Returns:


            Dict containing compression results


        """

        try:
            # Get old memories

            if user_id:
                memories = await self.memory_repository.get_memories_by_user(user_id)

            else:
                memories = await self.memory_repository.get_all_memories()

            # Filter by age

            cutoff_date = datetime.now(UTC).replace(
                day=datetime.now(UTC).day - days_threshold
            )

            old_memories = []

            for memory in memories:
                memory_date = getattr(memory, "last_accessed_at", None) or getattr(
                    memory, "created_at", None
                )

                if memory_date and memory_date < cutoff_date:
                    old_memories.append(memory)

            if not old_memories:
                return {
                    "success": True,
                    "message": "No old memories found for compression",
                    "compressed_count": 0,
                }

            # Compress old memories in batches

            batch_size = 10

            compressed_count = 0

            compression_results = []

            for i in range(0, len(old_memories), batch_size):
                batch = old_memories[i : i + batch_size]

                try:
                    # Create compressed representation

                    batch_content = [memory.content for memory in batch]

                    compressed_content = await self._create_compressed_summary(
                        batch_content
                    )

                    # Store compressed memory

                    compressed_memory = {
                        "type": "compressed_batch",
                        "content": compressed_content,
                        "original_count": len(batch),
                        "original_ids": [memory.id for memory in batch],
                        "compressed_at": datetime.now(UTC).isoformat(),
                        "compression_reason": f"age_threshold_{days_threshold}_days",
                        "user_id": user_id,
                    }

                    compressed_id = await self.memory_repository.store_memory(
                        compressed_memory
                    )

                    # Mark original memories as compressed

                    for memory in batch:
                        await self._mark_memory_as_compressed(memory.id, compressed_id)

                    compressed_count += len(batch)

                    compression_results.append(
                        {
                            "compressed_memory_id": compressed_id,
                            "original_count": len(batch),
                            "compression_ratio": len(compressed_content)
                            / sum(len(m.content) for m in batch),
                        }
                    )

                except Exception as e:
                    logger.warning(f"Failed to compress batch: {e}")

                    continue

            logger.info(f"Compressed {compressed_count} old memories")

            return {
                "success": True,
                "compressed_count": compressed_count,
                "batch_count": len(compression_results),
                "compression_results": compression_results,
                "days_threshold": days_threshold,
                "user_id": user_id,
            }

        except Exception as e:
            logger.error(f"Failed to compress old memories: {e}")

            raise RuntimeError(f"Old memory compression failed: {e}") from e

    async def compress_by_text_length(
        self, min_length: int = 1000, user_id: str | None = None
    ) -> dict[str, Any]:
        """Compress memories with excessive text length.





        Args:


            min_length: Minimum character length to trigger compression


            user_id: Optional user ID to filter memories





        Returns:


            Dict containing compression results


        """

        try:
            # Get memories to analyze

            if user_id:
                memories = await self.memory_repository.get_memories_by_user(user_id)

            else:
                memories = await self.memory_repository.get_all_memories()

            # Filter by length

            long_memories = [
                memory for memory in memories if len(memory.content) >= min_length
            ]

            if not long_memories:
                return {
                    "success": True,
                    "message": "No memories exceed length threshold",
                    "compressed_count": 0,
                }

            compressed_count = 0

            compression_results = []

            # Compress each long memory

            for memory in long_memories:
                try:
                    # Create compressed version

                    compressed_content = await self._compress_text_content(
                        memory.content
                    )

                    if len(compressed_content) < len(memory.content):
                        # Update memory with compressed content

                        compressed_memory = {
                            "id": memory.id,
                            "content": compressed_content,
                            "metadata": {
                                **getattr(memory, "metadata", {}),
                                "original_length": len(memory.content),
                                "compressed_length": len(compressed_content),
                                "compression_ratio": len(compressed_content)
                                / len(memory.content),
                                "compressed_at": datetime.now(UTC).isoformat(),
                                "compression_type": "text_length",
                            },
                        }

                        await self.memory_repository.update_memory(
                            memory.id, compressed_memory
                        )

                        compressed_count += 1

                        compression_results.append(
                            {
                                "memory_id": memory.id,
                                "original_length": len(memory.content),
                                "compressed_length": len(compressed_content),
                                "compression_ratio": len(compressed_content)
                                / len(memory.content),
                            }
                        )

                except Exception as e:
                    logger.warning(f"Failed to compress memory {memory.id}: {e}")

                    continue

            logger.info(f"Compressed {compressed_count} memories by text length")

            return {
                "success": True,
                "compressed_count": compressed_count,
                "compression_results": compression_results,
                "min_length": min_length,
                "user_id": user_id,
            }

        except Exception as e:
            logger.error(f"Failed to compress by text length: {e}")

            raise RuntimeError(f"Text length compression failed: {e}") from e

    async def decompress_memory(self, memory_id: str) -> dict[str, Any]:
        """Decompress a compressed memory back to its original form.





        Args:


            memory_id: ID of the compressed memory





        Returns:


            Dict containing decompression results


        """

        try:
            # Get compressed memory

            memory = await self.memory_repository.get_by_id(memory_id)

            if not memory:
                raise ValueError(f"Memory {memory_id} not found")

            # Check if memory is compressed

            metadata = getattr(memory, "metadata", {})

            compression_type = metadata.get("compression_type")

            if not compression_type:
                return {
                    "success": True,
                    "message": "Memory is not compressed",
                    "memory_id": memory_id,
                }

            decompressed_content = None

            if compression_type == "text_length":
                # For text compression, try to expand content

                decompressed_content = await self._decompress_text_content(
                    memory.content
                )

            elif compression_type == "batch_compression":
                # For batch compression, recreate individual memories

                original_ids = metadata.get("original_ids", [])

                return self._decompress_batch_memory(original_ids)

            elif compression_type == "similarity_group":
                # For similarity groups, recreate individual memories

                original_ids = metadata.get("original_ids", [])

                return self._decompress_similarity_group(original_ids)

            else:
                raise ValueError(f"Unknown compression type: {compression_type}")

            if decompressed_content:
                # Update memory with decompressed content

                decompressed_memory = {
                    "content": decompressed_content,
                    "metadata": {
                        **metadata,
                        "decompressed_at": datetime.now(UTC).isoformat(),
                        "compression_type": None,  # Remove compression marker
                    },
                }

                await self.memory_repository.update_memory(
                    memory_id, decompressed_memory
                )

                return {
                    "success": True,
                    "memory_id": memory_id,
                    "decompressed": True,
                    "original_length": len(decompressed_content),
                }

            return {
                "success": False,
                "message": "Failed to decompress memory",
                "memory_id": memory_id,
            }

        except Exception as e:
            logger.error(f"Failed to decompress memory {memory_id}: {e}")

            raise RuntimeError(f"Memory decompression failed: {e}") from e

    async def get_compression_statistics(
        self, user_id: str | None = None
    ) -> dict[str, Any]:
        """Get compression statistics for memories.





        Args:


            user_id: Optional user ID to filter statistics





        Returns:


            Dict containing compression statistics


        """

        try:
            # Get all memories

            if user_id:
                memories = await self.memory_repository.get_memories_by_user(user_id)

            else:
                memories = await self.memory_repository.get_all_memories()

            # Analyze compression status

            total_memories = len(memories)

            compressed_memories = 0

            total_original_size = 0

            total_compressed_size = 0

            compression_types = {}

            for memory in memories:
                metadata = getattr(memory, "metadata", {})

                compression_type = metadata.get("compression_type")

                if compression_type:
                    compressed_memories += 1

                    compression_types[compression_type] = (
                        compression_types.get(compression_type, 0) + 1
                    )

                    original_length = metadata.get(
                        "original_length", len(memory.content)
                    )

                    compressed_length = metadata.get(
                        "compressed_length", len(memory.content)
                    )

                    total_original_size += original_length

                    total_compressed_size += compressed_length

                else:
                    total_original_size += len(memory.content)

                    total_compressed_size += len(memory.content)

            # Calculate overall compression ratio

            overall_compression_ratio = (
                total_compressed_size / total_original_size
                if total_original_size > 0
                else 1.0
            )

            space_saved = total_original_size - total_compressed_size

            return {
                "total_memories": total_memories,
                "compressed_memories": compressed_memories,
                "uncompressed_memories": total_memories - compressed_memories,
                "compression_percentage": (compressed_memories / total_memories * 100)
                if total_memories > 0
                else 0,
                "compression_types": compression_types,
                "total_original_size": total_original_size,
                "total_compressed_size": total_compressed_size,
                "overall_compression_ratio": round(overall_compression_ratio, 3),
                "space_saved_bytes": space_saved,
                "space_saved_percentage": ((space_saved / total_original_size) * 100)
                if total_original_size > 0
                else 0,
                "user_id": user_id,
            }

        except Exception as e:
            logger.error(f"Failed to get compression statistics: {e}")

            raise RuntimeError(f"Failed to get compression statistics: {e}") from e

    def _find_similar_memory_groups(
        self, memories: list[Any], threshold: float, max_group_size: int
    ) -> list[list[Any]]:
        """Find groups of similar memories."""

        # This is a simplified implementation

        # In a real scenario, you'd use vector embeddings and similarity calculations

        groups = []

        used_memories = set()

        for i, memory in enumerate(memories):
            if memory.id in used_memories:
                continue

            group = [memory]

            used_memories.add(memory.id)

            # Find similar memories (simplified keyword matching)

            memory_words = set(memory.content.lower().split())

            for j, other_memory in enumerate(memories[i + 1 :], i + 1):
                if other_memory.id in used_memories or len(group) >= max_group_size:
                    continue

                other_words = set(other_memory.content.lower().split())

                similarity = len(memory_words & other_words) / len(
                    memory_words | other_words
                )

                if similarity >= threshold:
                    group.append(other_memory)

                    used_memories.add(other_memory.id)

            if len(group) > 1:
                groups.append(group)

        return groups

    async def _compress_memory_group(self, group: list[Any]) -> dict[str, Any]:
        """Compress a group of similar memories."""

        try:
            # Combine content from all memories in the group

            combined_content = "\n\n".join([memory.content for memory in group])

            # Use AI to create a compressed summary

            prompt = f"Create a comprehensive summary that captures the key information from these related memory entries:\n\n{combined_content}"

            response = await self.ai_service.generate_text(
                prompt=prompt,
                max_tokens=min(len(combined_content) // 2, 500),
                temperature=0.3,
            )

            compressed_content = response.get("text", "").strip()

            # Create compressed memory record

            compressed_memory = {
                "type": "compressed_group",
                "content": compressed_content,
                "original_count": len(group),
                "original_ids": [memory.id for memory in group],
                "compressed_at": datetime.now(UTC).isoformat(),
                "compression_type": "similarity_group",
                "metadata": {
                    "original_length": len(combined_content),
                    "compressed_length": len(compressed_content),
                    "compression_ratio": len(compressed_content)
                    / len(combined_content),
                },
            }

            compressed_id = await self.memory_repository.store_memory(compressed_memory)

            return {
                "success": True,
                "compressed_memory_id": compressed_id,
                "original_count": len(group),
                "compression_ratio": len(compressed_content) / len(combined_content),
            }

        except Exception as e:
            logger.error(f"Failed to compress memory group: {e}")

            return {"success": False, "error": str(e)}

    async def _create_compressed_summary(self, content_list: list[str]) -> str:
        """Create a compressed summary from multiple content pieces."""

        combined_content = "\n\n".join(content_list)

        prompt = f"Create a concise summary that captures the essential information from these memory entries:\n\n{combined_content}"

        response = await self.ai_service.generate_text(
            prompt=prompt,
            max_tokens=min(len(combined_content) // 3, 400),
            temperature=0.3,
        )

        return response.get("text", "").strip()

    async def _compress_text_content(self, content: str) -> str:
        """Compress text content while preserving key information."""

        prompt = f"Compress the following text while preserving all key information and important details:\n\n{content}"

        response = await self.ai_service.generate_text(
            prompt=prompt,
            max_tokens=min(len(content.split()) // 2, 400),
            temperature=0.2,
        )

        return response.get("text", "").strip()

    async def _decompress_text_content(self, compressed_content: str) -> str:
        """Attempt to decompress text content."""

        prompt = f"Expand and elaborate on this compressed text, providing more detail while staying true to the original meaning:\n\n{compressed_content}"

        response = await self.ai_service.generate_text(
            prompt=prompt,
            max_tokens=len(compressed_content.split()) * 2,
            temperature=0.4,
        )

        return response.get("text", "").strip()

    async def _mark_memory_as_compressed(
        self, memory_id: str, compressed_memory_id: str
    ) -> None:
        """Mark a memory as compressed by updating its metadata."""

        memory = await self.memory_repository.get_by_id(memory_id)

        if memory:
            updated_memory = {
                "metadata": {
                    **getattr(memory, "metadata", {}),
                    "compressed": True,
                    "compressed_memory_id": compressed_memory_id,
                    "compressed_at": datetime.now(UTC).isoformat(),
                }
            }

            await self.memory_repository.update_memory(memory_id, updated_memory)

    def _decompress_batch_memory(self, original_ids: list[str]) -> dict[str, Any]:
        """Decompress a batch-compressed memory."""

        # This would require more sophisticated logic to recreate individual memories

        # For now, return a placeholder implementation

        return {
            "success": True,
            "message": "Batch decompression not fully implemented",
            "original_ids": original_ids,
        }

    def _decompress_similarity_group(self, original_ids: list[str]) -> dict[str, Any]:
        """Decompress a similarity group compressed memory."""

        # This would require more sophisticated logic to recreate individual memories

        # For now, return a placeholder implementation

        return {
            "success": True,
            "message": "Similarity group decompression not fully implemented",
            "original_ids": original_ids,
        }
