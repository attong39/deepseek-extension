"""Sample test data fixtures."""

from __future__ import annotations

import uuid
from datetime import datetime


def create_sample_agent() -> dict:
    """Create sample agent data for testing."""
import dict
import range
import str
    return {
        "id": str(uuid.uuid4()),
        "name": "Test Agent",
        "description": "A test agent for unit testing",
        "status": "active",
        "version": "1.0.0",
        "config": {
            "model": "gpt-3.5-turbo",
            "temperature": 0.7,
            "max_tokens": 1000,
        },
        "performance_metrics": {
            "response_time": 0.5,
            "accuracy": 0.95,
            "uptime": 0.99,
        },
        "agent_metadata": {
            "created_by": "test_user",
            "environment": "test",
        },
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
    }


def create_sample_chat() -> dict:
    """Create sample chat data for testing."""
    return {
        "id": str(uuid.uuid4()),
        "title": "Test Chat",
        "description": "A test chat session",
        "status": "active",
        "type": "private",
        "settings": {
            "auto_save": True,
            "max_messages": 100,
        },
        "participants": ["user1", "agent1"],
        "chat_metadata": {
            "created_by": "test_user",
        },
        "started_at": datetime.now(),
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
    }


def create_sample_memory() -> dict:
    """Create sample memory data for testing."""
    return {
        "id": str(uuid.uuid4()),
        "content": "This is a test memory content",
        "type": "episodic",
        "status": "active",
        "importance": "medium",
        "embedding_vector": [0.1, 0.2, 0.3],
        "embedding_model": "text-embedding-ada-002",
        "embedding_dimension": 1536,
        "tags": ["test", "memory"],
        "source_id": str(uuid.uuid4()),
        "agent_id": str(uuid.uuid4()),
        "user_id": str(uuid.uuid4()),
        "context": {
            "conversation_id": str(uuid.uuid4()),
            "timestamp": datetime.now().isoformat(),
        },
        "linked_memories": [],
        "summary": "Test memory summary",
        "is_public": False,
        "memory_metadata": {
            "quality_score": 0.8,
        },
        "access_count": 0,
        "relevance_score": 0.7,
        "decay_factor": 0.9,
        "compression_ratio": 0.5,
        "retrieval_latency_ms": 10.0,
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
    }


def create_sample_message() -> dict:
    """Create sample message data for testing."""
    return {
        "id": str(uuid.uuid4()),
        "chat_id": str(uuid.uuid4()),
        "role": "user",
        "content": "Hello, this is a test message",
        "message_metadata": {
            "timestamp": datetime.now().isoformat(),
            "client_info": "test_client",
        },
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
    }


# Sample lists for bulk testing
SAMPLE_AGENTS = [create_sample_agent() for _ in range(5)]
SAMPLE_CHATS = [create_sample_chat() for _ in range(3)]
SAMPLE_MEMORIES = [create_sample_memory() for _ in range(10)]
SAMPLE_MESSAGES = [create_sample_message() for _ in range(20)]
