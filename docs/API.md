# Zeta AI Server - API Documentation

## Overview

Zeta AI Server is a comprehensive FastAPI-based platform for managing AI agents, conversations, and intelligent memory systems. This document provides detailed API reference for all available endpoints.

## Base URL

```
http://localhost:8001
```

## Authentication

All API endpoints (except health checks) require authentication. Include the API key in the header:

```http
Authorization: Bearer <your-api-key>
```

## API Versioning

The API uses URL versioning with the prefix `/api/v1/` for version 1.

## Content Type

All requests and responses use JSON format:

```http
Content-Type: application/json
```

## Rate Limiting

- **Limit**: 100 requests per minute per IP
- **Headers**: Rate limit information is included in response headers
  - `X-RateLimit-Limit`: Request limit
  - `X-RateLimit-Remaining`: Remaining requests
  - `X-RateLimit-Reset`: Reset time (Unix timestamp)

## Error Handling

The API uses standard HTTP status codes and returns errors in JSON format:

```json
{
  "detail": "Error message",
  "error_code": "SPECIFIC_ERROR_CODE",
  "timestamp": "2025-08-11T20:00:00Z"
}
```

### Common Status Codes

- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `422` - Validation Error
- `429` - Rate Limit Exceeded
- `500` - Internal Server Error

---

## Health Endpoints

### GET /api/v1/health

Check server health status.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-08-11T20:00:00Z",
  "version": "1.0.0",
  "database": "connected",
  "redis": "connected"
}
```

---

## Agent Management

### POST /api/v1/agents/

Create a new AI agent.

**Request Body:**
```json
{
  "name": "Assistant Agent",
  "description": "A helpful AI assistant",
  "version": "1.0.0",
  "config": {
    "model": "gpt-3.5-turbo",
    "temperature": 0.7,
    "max_tokens": 1000
  }
}
```

**Response (201):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "Assistant Agent",
  "description": "A helpful AI assistant",
  "status": "active",
  "version": "1.0.0",
  "config": {
    "model": "gpt-3.5-turbo",
    "temperature": 0.7,
    "max_tokens": 1000
  },
  "performance_metrics": {
    "response_time": 0.0,
    "accuracy": 0.0,
    "uptime": 0.0
  },
  "created_at": "2025-08-11T20:00:00Z",
  "updated_at": "2025-08-11T20:00:00Z"
}
```

### GET /api/v1/agents/

List all agents with pagination.

**Query Parameters:**
- `limit` (int, optional): Number of results (default: 50, max: 100)
- `offset` (int, optional): Skip number of results (default: 0)
- `status` (string, optional): Filter by status (active, inactive, training)

**Response (200):**
```json
{
  "agents": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "name": "Assistant Agent",
      "description": "A helpful AI assistant",
      "status": "active",
      "version": "1.0.0",
      "created_at": "2025-08-11T20:00:00Z"
    }
  ],
  "total": 1,
  "limit": 50,
  "offset": 0
}
```

### GET /api/v1/agents/{agent_id}

Get specific agent details.

**Response (200):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "Assistant Agent",
  "description": "A helpful AI assistant",
  "status": "active",
  "version": "1.0.0",
  "config": {
    "model": "gpt-3.5-turbo",
    "temperature": 0.7,
    "max_tokens": 1000
  },
  "performance_metrics": {
    "response_time": 0.5,
    "accuracy": 0.95,
    "uptime": 0.99
  },
  "created_at": "2025-08-11T20:00:00Z",
  "updated_at": "2025-08-11T20:00:00Z"
}
```

### PUT /api/v1/agents/{agent_id}

Update agent configuration.

**Request Body:**
```json
{
  "name": "Updated Agent Name",
  "description": "Updated description",
  "config": {
    "temperature": 0.8
  }
}
```

### DELETE /api/v1/agents/{agent_id}

Delete an agent.

**Response (200):**
```json
{
  "message": "Agent deleted successfully"
}
```

---

## Chat Management

### POST /api/v1/chat/start

Start a new chat session.

**Request Body:**
```json
{
  "title": "Customer Support Chat",
  "description": "Help with product questions",
  "type": "private",
  "participants": ["550e8400-e29b-41d4-a716-446655440000"]
}
```

**Response (201):**
```json
{
  "id": "660e8400-e29b-41d4-a716-446655440000",
  "title": "Customer Support Chat",
  "description": "Help with product questions",
  "status": "active",
  "type": "private",
  "participants": ["550e8400-e29b-41d4-a716-446655440000"],
  "started_at": "2025-08-11T20:00:00Z",
  "created_at": "2025-08-11T20:00:00Z"
}
```

### POST /api/v1/chat/{chat_id}/messages

Send a message to a chat.

**Request Body:**
```json
{
  "role": "user",
  "content": "Hello, I need help with my order",
  "message_metadata": {
    "client_info": "web_app"
  }
}
```

**Response (201):**
```json
{
  "id": "770e8400-e29b-41d4-a716-446655440000",
  "chat_id": "660e8400-e29b-41d4-a716-446655440000",
  "role": "user",
  "content": "Hello, I need help with my order",
  "message_metadata": {
    "client_info": "web_app"
  },
  "created_at": "2025-08-11T20:00:00Z"
}
```

### GET /api/v1/chat/{chat_id}

Get chat conversation with messages.

**Response (200):**
```json
{
  "id": "660e8400-e29b-41d4-a716-446655440000",
  "title": "Customer Support Chat",
  "status": "active",
  "messages": [
    {
      "id": "770e8400-e29b-41d4-a716-446655440000",
      "role": "user",
      "content": "Hello, I need help with my order",
      "created_at": "2025-08-11T20:00:00Z"
    }
  ],
  "participants": ["550e8400-e29b-41d4-a716-446655440000"],
  "created_at": "2025-08-11T20:00:00Z"
}
```

### POST /api/v1/chat/{chat_id}/end

End a chat session.

**Response (200):**
```json
{
  "message": "Chat session ended",
  "ended_at": "2025-08-11T20:05:00Z"
}
```

---

## Memory Management

### POST /api/v1/memory/

Create a new memory entry.

**Request Body:**
```json
{
  "content": "User prefers morning appointments",
  "type": "semantic",
  "importance": "high",
  "tags": ["preferences", "scheduling"],
  "context": {
    "user_id": "user123",
    "conversation_id": "660e8400-e29b-41d4-a716-446655440000"
  }
}
```

**Response (201):**
```json
{
  "id": "880e8400-e29b-41d4-a716-446655440000",
  "content": "User prefers morning appointments",
  "type": "semantic",
  "status": "active",
  "importance": "high",
  "tags": ["preferences", "scheduling"],
  "relevance_score": 0.9,
  "created_at": "2025-08-11T20:00:00Z"
}
```

### GET /api/v1/memory/search

Search memories by content or context.

**Query Parameters:**
- `query` (string, required): Search query
- `limit` (int, optional): Number of results (default: 10)
- `min_relevance` (float, optional): Minimum relevance score (0.0-1.0)
- `type` (string, optional): Memory type filter
- `importance` (string, optional): Importance filter

**Response (200):**
```json
[
  {
    "id": "880e8400-e29b-41d4-a716-446655440000",
    "content": "User prefers morning appointments",
    "type": "semantic",
    "importance": "high",
    "relevance_score": 0.95,
    "tags": ["preferences", "scheduling"],
    "created_at": "2025-08-11T20:00:00Z"
  }
]
```

### GET /api/v1/memory/{memory_id}

Get specific memory details.

### PUT /api/v1/memory/{memory_id}

Update memory entry.

### DELETE /api/v1/memory/{memory_id}

Delete a memory entry.

---

## File Management

### POST /api/v1/files/upload

Upload a file.

**Request:**
- `Content-Type: multipart/form-data`
- `file`: File to upload (max 10MB)

**Response (201):**
```json
{
  "file_id": "990e8400-e29b-41d4-a716-446655440000",
  "filename": "document.pdf",
  "size": 1024576,
  "content_type": "application/pdf",
  "upload_date": "2025-08-11T20:00:00Z"
}
```

### GET /api/v1/files/download/{file_id}

Download a file.

**Query Parameters:**
- `filename` (string, optional): Custom filename for download

**Response:** File content with appropriate headers

### GET /api/v1/files/metadata/{file_id}

Get file metadata.

**Response (200):**
```json
{
  "file_id": "990e8400-e29b-41d4-a716-446655440000",
  "filename": "document.pdf",
  "size": 1024576,
  "content_type": "application/pdf",
  "upload_date": "2025-08-11T20:00:00Z"
}
```

### GET /api/v1/files/list

List uploaded files.

**Query Parameters:**
- `limit` (int, optional): Number of results (default: 50)
- `offset` (int, optional): Skip number of results (default: 0)

### DELETE /api/v1/files/delete/{file_id}

Delete a file.

---

## WebSocket Endpoints

### WS /ws/chat

Real-time chat WebSocket connection.

**Connection:**
```javascript
const ws = new WebSocket('ws://localhost:8001/ws/chat');
```

**Message Format:**
```json
{
  "type": "message",
  "data": {
    "chat_id": "660e8400-e29b-41d4-a716-446655440000",
    "content": "Hello!",
    "role": "user"
  }
}
```

**Event Types:**
- `connect` - Establish connection
- `message` - Send/receive message
- `disconnect` - Close connection
- `typing` - Typing indicator
- `error` - Error notification

---

## SDK Examples

### Python

```python
import httpx

# Initialize client
client = httpx.Client(
    base_url="http://localhost:8001",
    headers={"Authorization": "Bearer your-api-key"}
)

# Create agent
agent_data = {
    "name": "My Agent",
    "description": "Test agent",
    "version": "1.0.0"
}
response = client.post("/api/v1/agents/", json=agent_data)
agent = response.json()

# Start chat
chat_data = {
    "title": "Test Chat",
    "participants": [agent["id"]]
}
response = client.post("/api/v1/chat/start", json=chat_data)
chat = response.json()

# Send message
message_data = {
    "role": "user",
    "content": "Hello!"
}
response = client.post(f"/api/v1/chat/{chat['id']}/messages", json=message_data)
```

### JavaScript

```javascript
// Initialize client
const baseURL = 'http://localhost:8001';
const headers = {
  'Authorization': 'Bearer your-api-key',
  'Content-Type': 'application/json'
};

// Create agent
const createAgent = async () => {
  const response = await fetch(`${baseURL}/api/v1/agents/`, {
    method: 'POST',
    headers,
    body: JSON.stringify({
      name: 'My Agent',
      description: 'Test agent',
      version: '1.0.0'
    })
  });
  return response.json();
};

// WebSocket connection
const ws = new WebSocket('ws://localhost:8001/ws/chat');
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Received:', data);
};
```

---

## Rate Limits and Quotas

| Endpoint Category | Rate Limit | Quota (Daily) |
|------------------|------------|---------------|
| Health checks    | 1000/min   | Unlimited     |
| Agent operations | 100/min    | 10,000        |
| Chat messages    | 200/min    | 50,000        |
| Memory operations| 150/min    | 20,000        |
| File uploads     | 50/min     | 1,000         |

## Support

For API support and questions:
- Email: api-support@zeta.ai
- Documentation: https://docs.zeta.ai
- Status Page: https://status.zeta.ai
