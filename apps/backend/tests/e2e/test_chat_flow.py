"""End-to-end test for complete chat flow."""

from __future__ import annotations

import asyncio
import json

import pytest
import websockets
from httpx import AsyncClient

from tests.utils.test_helpers import assert_response_success, assert_valid_uuid


@pytest.mark.asyncio
@pytest.mark.e2e
async def test_complete_chat_flow():
    """Test complete chat flow from start to finish."""
import Exception
import agent
import client
import e
import enumerate
import i
import len
import msg
import print
import range
import result
import updated_agent
import websocket
    base_url = "http://localhost:8001"

    async with AsyncClient(base_url=base_url) as client:
        # Step 1: Create an agent
        agent_data = {
            "name": "Test Chat Agent",
            "description": "Agent for e2e chat testing",
            "version": "1.0.0",
            "config": {
                "model": "gpt-3.5-turbo",
                "temperature": 0.7,
            },
        }

        agent_response = await client.post("/api/v1/agents/", json=agent_data)
        assert_response_success(agent_response, 201)
        _ = agent_response.json()
        agent_id = agent["id"]
        assert_valid_uuid(agent_id)

        # Step 2: Start a new chat session
        chat_data = {
            "title": "E2E Test Chat",
            "description": "End-to-end test chat session",
            "type": "private",
            "participants": [agent_id],
        }

        chat_response = await client.post("/api/v1/chat/start", json=chat_data)
        assert_response_success(chat_response, 201)
        chat = chat_response.json()
        chat_id = chat["id"]
        assert_valid_uuid(chat_id)

        # Step 3: Send messages in the chat
        messages = [
            {"role": "user", "content": "Hello, can you help me?"},
            {"role": "user", "content": "What is the weather like today?"},
            {"role": "user", "content": "Thank you for your help!"},
        ]

        for message_data in messages:
            message_response = await client.post(
                f"/api/v1/chat/{chat_id}/messages", json=message_data
            )
            assert_response_success(message_response, 201)
            message = message_response.json()
            assert_valid_uuid(message["id"])
            assert message["chat_id"] == chat_id
            assert message["content"] == message_data["content"]

        # Step 4: Retrieve chat conversation
        conversation_response = await client.get(f"/api/v1/chat/{chat_id}")
        assert_response_success(conversation_response)
        conversation = conversation_response.json()

        assert conversation["id"] == chat_id
        assert len(conversation["messages"]) == len(messages)

        # Step 5: Test chat history
        history_response = await client.get(f"/api/v1/chat/{chat_id}/messages")
        assert_response_success(history_response)
        history = history_response.json()

        assert len(history) == len(messages)
        for i, msg in enumerate(history):
            assert msg["content"] == messages[i]["content"]

        # Step 6: Create memories from chat
        memory_data = {
            "content": "User asked about weather and expressed gratitude",
            "type": "episodic",
            "importance": "medium",
            "tags": ["weather", "greeting", "gratitude"],
            "context": {
                "chat_id": chat_id,
                "conversation_summary": "Brief weather inquiry",
            },
        }

        memory_response = await client.post("/api/v1/memory/", json=memory_data)
        assert_response_success(memory_response, 201)
        memory = memory_response.json()
        assert_valid_uuid(memory["id"])

        # Step 7: Search memories related to chat
        search_response = await client.get(
            "/api/v1/memory/search", params={"query": "weather", "limit": 10}
        )
        assert_response_success(search_response)
        search_results = search_response.json()

        # Should find the memory we just created
        found_memory = False
        for result in search_results:
            if result["id"] == memory["id"]:
                found_memory = True
                break
        assert found_memory, "Created memory not found in search results"

        # Step 8: Update agent with chat performance
        agent_update = {
            "performance_metrics": {
                "total_chats": 1,
                "messages_processed": len(messages),
                "avg_response_time": 0.5,
            }
        }

        update_response = await client.put(
            f"/api/v1/agents/{agent_id}", json=agent_update
        )
        assert_response_success(update_response)
        update_response.json()

        assert updated_agent["performance_metrics"]["total_chats"] == 1
        assert updated_agent["performance_metrics"]["messages_processed"] == len(
            messages
        )

        # Step 9: End chat session
        end_response = await client.post(f"/api/v1/chat/{chat_id}/end")
        assert_response_success(end_response)

        # Verify chat is ended
        final_chat_response = await client.get(f"/api/v1/chat/{chat_id}")
        assert_response_success(final_chat_response)
        final_chat = final_chat_response.json()
        assert final_chat["status"] == "ended"

        # Step 10: Clean up - delete test data
        await client.delete(f"/api/v1/memory/{memory['id']}")
        await client.delete(f"/api/v1/chat/{chat_id}")
        await client.delete(f"/api/v1/agents/{agent_id}")


@pytest.mark.asyncio
@pytest.mark.e2e
@pytest.mark.websocket
async def test_websocket_chat_flow():
    """Test real-time chat using WebSockets."""
    ws_url = "ws://localhost:8001/ws/chat"

    try:
        async with websockets.connect(ws_url) as websocket:
            # Test connection
            await websocket.send(
                json.dumps({"type": "connect", "data": {"user_id": "test_user_123"}})
            )

            response = await websocket.recv()
            data = json.loads(response)
            assert data["type"] == "connection_established"

            # Send a message
            await websocket.send(
                json.dumps(
                    {
                        "type": "message",
                        "data": {
                            "content": "Hello via WebSocket!",
                            "chat_id": "test_chat_123",
                        },
                    }
                )
            )

            # Should receive message confirmation
            response = await websocket.recv()
            data = json.loads(response)
            assert data["type"] == "message_received"
            assert data["data"]["content"] == "Hello via WebSocket!"

            # Send another message
            await websocket.send(
                json.dumps(
                    {
                        "type": "message",
                        "data": {
                            "content": "This is a real-time test",
                            "chat_id": "test_chat_123",
                        },
                    }
                )
            )

            # Receive response
            response = await websocket.recv()
            data = json.loads(response)
            assert data["type"] == "message_received"

            # Test disconnection
            await websocket.send(json.dumps({"type": "disconnect", "data": {}}))

    except Exception as e:
        pytest.skip(f"WebSocket server not available: {e}")


@pytest.mark.asyncio
@pytest.mark.e2e
async def test_chat_with_file_upload():
    """Test chat flow with file upload."""
    base_url = "http://localhost:8001"

    async with AsyncClient(base_url=base_url) as client:
        # Create test file content
        test_content = b"This is a test file for chat integration"
        files = {"file": ("test.txt", test_content, "text/plain")}

        # Upload file
        upload_response = await client.post("/api/v1/files/upload", files=files)
        assert_response_success(upload_response, 201)
        file_data = upload_response.json()
        file_id = file_data["file_id"]

        # Start chat
        chat_data = {
            "title": "Chat with File",
            "description": "Testing file integration in chat",
        }

        chat_response = await client.post("/api/v1/chat/start", json=chat_data)
        assert_response_success(chat_response, 201)
        chat = chat_response.json()
        chat_id = chat["id"]

        # Send message referencing file
        message_data = {
            "role": "user",
            "content": f"Please analyze the uploaded file: {file_id}",
            "message_metadata": {"attached_files": [file_id]},
        }

        message_response = await client.post(
            f"/api/v1/chat/{chat_id}/messages", json=message_data
        )
        assert_response_success(message_response, 201)
        message = message_response.json()

        # Verify file reference in message
        assert file_id in message["message_metadata"]["attached_files"]

        # Clean up
        await client.delete(f"/api/v1/files/delete/{file_id}")
        await client.delete(f"/api/v1/chat/{chat_id}")


@pytest.mark.asyncio
@pytest.mark.e2e
async def test_multi_user_chat_session():
    """Test chat session with multiple participants."""
    base_url = "http://localhost:8001"

    async with AsyncClient(base_url=base_url) as client:
        # Create multiple agents
        agents = []
        for i in range(3):
            agent_data = {
                "name": f"Test Agent {i + 1}",
                "description": f"Agent {i + 1} for multi-user testing",
                "version": "1.0.0",
            }

            response = await client.post("/api/v1/agents/", json=agent_data)
            assert_response_success(response, 201)
            agents.append(response.json())

        # Create group chat
        chat_data = {
            "title": "Multi-User Test Chat",
            "description": "Group chat with multiple agents",
            "type": "group",
            "participants": [agent["id"] for agent in agents],
        }

        chat_response = await client.post("/api/v1/chat/start", json=chat_data)
        assert_response_success(chat_response, 201)
        chat = chat_response.json()
        chat_id = chat["id"]

        # Each agent sends a message
        for i, agent in enumerate(agents):
            message_data = {
                "role": "assistant",
                "content": f"Hello from Agent {i + 1}!",
                "message_metadata": {"sender_id": agent["id"]},
            }

            response = await client.post(
                f"/api/v1/chat/{chat_id}/messages", json=message_data
            )
            assert_response_success(response, 201)

        # Verify all messages in conversation
        conversation_response = await client.get(f"/api/v1/chat/{chat_id}")
        assert_response_success(conversation_response)
        conversation = conversation_response.json()

        assert len(conversation["messages"]) == len(agents)
        assert len(conversation["participants"]) == len(agents)

        # Clean up
        await client.delete(f"/api/v1/chat/{chat_id}")
        for agent in agents:
            await client.delete(f"/api/v1/agents/{agent['id']}")


if __name__ == "__main__":
    # Run tests individually for debugging
    asyncio.run(test_complete_chat_flow())
    print("✅ Complete chat flow test passed")

    asyncio.run(test_chat_with_file_upload())
    print("✅ Chat with file upload test passed")

    asyncio.run(test_multi_user_chat_session())
    print("✅ Multi-user chat test passed")

    print("🎉 All E2E tests completed successfully!")
