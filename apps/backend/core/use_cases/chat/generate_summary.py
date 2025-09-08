"""Generate summary use case for creating conversation and content summaries."""

from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)


class GenerateSummaryUseCase:
    """Use case for generating various types of summaries."""
import Exception
import RuntimeError
import ValueError
import ai_service
import chat_repository
import conversation
import conversation_id
import date
import dict
import e
import getattr
import hasattr
import int
import len
import limit
import list
import m
import max_length
import memory_id
import memory_ids
import memory_repository
import message
import round
import self
import str
import summary
import topic
import user_id

    def __init__(self, chat_repository: Any, memory_repository: Any, ai_service: Any):
        """Initialize the generate summary use case.





        Args:


            chat_repository: Repository for chat data operations


            memory_repository: Repository for memory operations


            ai_service: Service for AI operations


        """

        self.chat_repository = chat_repository

        self.memory_repository = memory_repository

        self.ai_service = ai_service

    async def generate_conversation_summary(
        self, conversation_id: str, summary_type: str = "brief", max_length: int = 200
    ) -> dict[str, Any]:
        """Generate a summary of a conversation.





        Args:


            conversation_id: ID of the conversation to summarize


            summary_type: Type of summary (brief, detailed, key_points)


            max_length: Maximum length of summary in words





        Returns:


            Dict containing summary information





        Raises:


            ValueError: If conversation not found or invalid parameters


            RuntimeError: If summary generation fails


        """

        try:
            # Get conversation messages

            messages = await self.chat_repository.get_messages_by_conversation(
                conversation_id
            )

            if not messages:
                raise ValueError(
                    f"No messages found for conversation {conversation_id}"
                )

            # Prepare conversation text

            conversation_text = self._format_messages_for_summary(messages)

            # Generate summary based on type

            if summary_type == "brief":
                prompt = f"Provide a brief summary of this conversation in {max_length} words or less:\n\n{conversation_text}"

            elif summary_type == "detailed":
                prompt = f"Provide a detailed summary of this conversation, highlighting key topics and decisions:\n\n{conversation_text}"

            elif summary_type == "key_points":
                prompt = f"Extract the key points and action items from this conversation:\n\n{conversation_text}"

            else:
                raise ValueError(f"Invalid summary type: {summary_type}")

            # Generate summary using AI service

            summary_response = await self.ai_service.generate_text(
                prompt=prompt,
                max_tokens=max_length * 2,  # Rough token estimate
                temperature=0.3,  # Lower temperature for more consistent summaries
            )

            summary_text = summary_response.get("text", "").strip()

            # Extract metadata

            word_count = len(summary_text.split())

            message_count = len(messages)

            # Store summary in memory for future reference

            summary_memory = {
                "type": "conversation_summary",
                "conversation_id": conversation_id,
                "summary_type": summary_type,
                "content": summary_text,
                "metadata": {
                    "word_count": word_count,
                    "message_count": message_count,
                    "original_length": len(conversation_text),
                    "compression_ratio": len(conversation_text) / len(summary_text)
                    if summary_text
                    else 0,
                },
            }

            await self.memory_repository.store_memory(summary_memory)

            logger.info(
                f"Generated {summary_type} summary for conversation {conversation_id}"
            )

            return {
                "success": True,
                "conversation_id": conversation_id,
                "summary_type": summary_type,
                "summary": summary_text,
                "word_count": word_count,
                "message_count": message_count,
                "compression_ratio": summary_memory["metadata"]["compression_ratio"],
            }

        except Exception as e:
            logger.error(
                f"Failed to generate conversation summary for {conversation_id}: {e}"
            )

            raise RuntimeError(f"Summary generation failed: {e}") from e

    async def generate_daily_summary(self, user_id: str, date: str) -> dict[str, Any]:
        """Generate a daily activity summary for a user.





        Args:


            user_id: ID of the user


            date: Date in YYYY-MM-DD format





        Returns:


            Dict containing daily summary


        """

        try:
            # Get user's conversations for the day

            conversations = await self.chat_repository.get_conversations_by_date(
                user_id, date
            )

            if not conversations:
                return {
                    "success": True,
                    "user_id": user_id,
                    "date": date,
                    "summary": "No activity recorded for this date.",
                    "conversation_count": 0,
                    "total_messages": 0,
                }

            # Collect all messages from conversations

            all_messages = []

            total_messages = 0

            for conversation in conversations:
                messages = await self.chat_repository.get_messages_by_conversation(
                    conversation.id
                )

                all_messages.extend(messages)

                total_messages += len(messages)

            # Generate daily summary

            conversation_summaries = []

            for conversation in conversations:
                conv_summary = await self.generate_conversation_summary(
                    conversation.id, summary_type="brief", max_length=50
                )

                conversation_summaries.append(conv_summary["summary"])

            # Create overall daily summary

            daily_activities = "\n".join(
                f"- {summary}" for summary in conversation_summaries
            )

            prompt = f"Summarize the user's daily AI assistant activities:\n\n{daily_activities}"

            summary_response = await self.ai_service.generate_text(
                prompt=prompt, max_tokens=300, temperature=0.3
            )

            daily_summary = summary_response.get("text", "").strip()

            return {
                "success": True,
                "user_id": user_id,
                "date": date,
                "summary": daily_summary,
                "conversation_count": len(conversations),
                "total_messages": total_messages,
                "activity_details": conversation_summaries,
            }

        except Exception as e:
            logger.error(
                f"Failed to generate daily summary for {user_id} on {date}: {e}"
            )

            raise RuntimeError(f"Daily summary generation failed: {e}") from e

    async def generate_topic_summary(
        self, topic: str, user_id: str | None = None, limit: int = 10
    ) -> dict[str, Any]:
        """Generate a summary of conversations about a specific topic.





        Args:


            topic: Topic to search for


            user_id: Optional user ID to filter by


            limit: Maximum number of conversations to include





        Returns:


            Dict containing topic summary


        """

        try:
            # Search for conversations related to the topic

            conversations = await self.chat_repository.search_conversations_by_topic(
                topic, user_id, limit
            )

            if not conversations:
                return {
                    "success": True,
                    "topic": topic,
                    "summary": f"No conversations found related to '{topic}'.",
                    "conversation_count": 0,
                }

            # Generate summaries for each relevant conversation

            topic_content = []

            for conversation in conversations:
                try:
                    conv_summary = await self.generate_conversation_summary(
                        conversation.id, summary_type="key_points", max_length=100
                    )

                    topic_content.append(conv_summary["summary"])

                except Exception as e:
                    logger.warning(
                        f"Failed to summarize conversation {conversation.id}: {e}"
                    )

                    continue

            # Create comprehensive topic summary

            if topic_content:
                combined_content = "\n\n".join(topic_content)

                prompt = f"Create a comprehensive summary about '{topic}' based on these conversation summaries:\n\n{combined_content}"

                summary_response = await self.ai_service.generate_text(
                    prompt=prompt, max_tokens=500, temperature=0.3
                )

                topic_summary = summary_response.get("text", "").strip()

            else:
                topic_summary = f"Found {len(conversations)} conversations about '{topic}' but could not generate detailed summaries."

            return {
                "success": True,
                "topic": topic,
                "summary": topic_summary,
                "conversation_count": len(conversations),
                "user_id": user_id,
            }

        except Exception as e:
            logger.error(f"Failed to generate topic summary for '{topic}': {e}")

            raise RuntimeError(f"Topic summary generation failed: {e}") from e

    async def generate_memory_summary(
        self, memory_ids: list[str], summary_type: str = "overview"
    ) -> dict[str, Any]:
        """Generate a summary of multiple memory entries.





        Args:


            memory_ids: List of memory IDs to summarize


            summary_type: Type of summary (overview, detailed, insights)





        Returns:


            Dict containing memory summary


        """

        try:
            # Retrieve memory entries

            memories = []

            for memory_id in memory_ids:
                memory = await self.memory_repository.get_by_id(memory_id)

                if memory:
                    memories.append(memory)

            if not memories:
                raise ValueError("No valid memories found")

            # Prepare memory content for summarization

            memory_content = []

            for memory in memories:
                content = f"Memory {memory.id}: {memory.content}"

                if hasattr(memory, "metadata") and memory.metadata:
                    content += f" (Type: {memory.metadata.get('type', 'unknown')})"

                memory_content.append(content)

            combined_memories = "\n\n".join(memory_content)

            # Generate summary based on type

            if summary_type == "overview":
                prompt = f"Provide a brief overview of these memory entries:\n\n{combined_memories}"

            elif summary_type == "detailed":
                prompt = f"Provide a detailed analysis of these memory entries, identifying patterns and themes:\n\n{combined_memories}"

            elif summary_type == "insights":
                prompt = f"Extract key insights and learning patterns from these memory entries:\n\n{combined_memories}"

            else:
                raise ValueError(f"Invalid summary type: {summary_type}")

            summary_response = await self.ai_service.generate_text(
                prompt=prompt, max_tokens=400, temperature=0.4
            )

            memory_summary = summary_response.get("text", "").strip()

            return {
                "success": True,
                "summary_type": summary_type,
                "summary": memory_summary,
                "memory_count": len(memories),
                "memory_ids": memory_ids,
            }

        except Exception as e:
            logger.error(f"Failed to generate memory summary: {e}")

            raise RuntimeError(f"Memory summary generation failed: {e}") from e

    def _format_messages_for_summary(self, messages: list[Any]) -> str:
        """Format messages for summary generation.





        Args:


            messages: List of message objects





        Returns:


            Formatted conversation text


        """

        formatted_messages = []

        for message in messages:
            role = getattr(message, "role", "unknown")

            content = getattr(message, "content", str(message))

            timestamp = getattr(message, "created_at", "")

            if timestamp:
                formatted_messages.append(f"[{timestamp}] {role.upper()}: {content}")

            else:
                formatted_messages.append(f"{role.upper()}: {content}")

        return "\n".join(formatted_messages)

    async def get_summary_statistics(
        self, user_id: str | None = None
    ) -> dict[str, Any]:
        """Get statistics about generated summaries.





        Args:


            user_id: Optional user ID to filter by





        Returns:


            Dict containing summary statistics


        """

        try:
            # Get summary memories from repository

            summary_memories = await self.memory_repository.get_memories_by_type(
                "conversation_summary"
            )

            if user_id:
                # Filter by user_id if provided

                summary_memories = [
                    m for m in summary_memories if m.metadata.get("user_id") == user_id
                ]

            total_summaries = len(summary_memories)

            # Calculate statistics

            total_conversations_summarized = len(
                {
                    m.metadata.get("conversation_id")
                    for m in summary_memories
                    if m.metadata.get("conversation_id")
                }
            )

            summary_types = {}

            total_compression_ratio = 0

            valid_ratios = 0

            for memory in summary_memories:
                summary_type = memory.metadata.get("summary_type", "unknown")

                summary_types[summary_type] = summary_types.get(summary_type, 0) + 1

                compression_ratio = memory.metadata.get("compression_ratio", 0)

                if compression_ratio > 0:
                    total_compression_ratio += compression_ratio

                    valid_ratios += 1

            avg_compression_ratio = (
                total_compression_ratio / valid_ratios if valid_ratios > 0 else 0
            )

            return {
                "total_summaries": total_summaries,
                "conversations_summarized": total_conversations_summarized,
                "summary_types": summary_types,
                "average_compression_ratio": round(avg_compression_ratio, 2),
                "user_id": user_id,
            }

        except Exception as e:
            logger.error(f"Failed to get summary statistics: {e}")

            raise RuntimeError(f"Failed to get summary statistics: {e}") from e
