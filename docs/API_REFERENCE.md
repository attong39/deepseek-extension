# 🔗 API Reference - ZETA AI Server

Complete reference documentation for all ZETA AI Server REST API endpoints. This document provides detailed information about request/response formats, authentication, error codes, and usage examples.

See also: `docs/api/openapi.yaml` for the OpenAPI spec.
# ZETA AI - API Reference Documentation

## Table of Contents
- [Authentication](#authentication)
- [Users API](#users-api)
- [Agents API](#agents-api)
- [Memories API](#memories-api)
- [Chat API](#chat-api)
- [File Upload API](#file-upload-api)
- [Voice API](#voice-api)
- [Controllers API](#controllers-api)
- [Monitoring API](#monitoring-api)
- [Analytics API](#analytics-api)
- [System API](#system-api)
- [Error Codes](#error-codes)

## Authentication

ZETA AI uses JWT (JSON Web Tokens) for authentication.

### Login
```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "expires_in": 3600
}
```

### Register
```http
POST /api/v1/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123",
  "full_name": "John Doe"
}
```

### Refresh Token
```http
POST /api/v1/auth/refresh
Authorization: Bearer <refresh_token>
```

## Users API

### Get Current User
```http
GET /api/v1/users/me
Authorization: Bearer <access_token>
```

**Response:**
```json
{
  "id": "user_123",
  "email": "user@example.com",
  "username": "johndoe",
  "full_name": "John Doe",
  "is_active": true,
  "created_at": "2024-01-01T00:00:00Z",
  "last_login": "2024-01-15T10:30:00Z"
}
```

### Update User Profile
```http
PATCH /api/v1/users/me
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "full_name": "John Smith",
  "preferences": {
    "language": "vi",
    "theme": "dark"
  }
}
```

### Change Password
```http
POST /api/v1/users/change-password
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "current_password": "oldpassword",
  "new_password": "newpassword123"
}
```

## Agents API

### Create Agent
```http
POST /api/v1/agents
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "name": "Assistant Agent",
  "description": "General purpose AI assistant",
  "type": "general",
  "personality": {
    "traits": ["helpful", "friendly", "knowledgeable"],
    "tone": "casual",
    "expertise": ["programming", "writing"]
  },
  "configuration": {
    "model": "gpt-4",
    "temperature": 0.7,
    "max_tokens": 2048
  }
}
```

**Response:**
```json
{
  "id": "agent_456",
  "name": "Assistant Agent",
  "description": "General purpose AI assistant",
  "type": "general",
  "status": "active",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z",
  "owner_id": "user_123"
}
```

### List Agents
```http
GET /api/v1/agents?limit=10&offset=0&type=general
Authorization: Bearer <access_token>
```

### Get Agent
```http
GET /api/v1/agents/{agent_id}
Authorization: Bearer <access_token>
```

### Update Agent
```http
PATCH /api/v1/agents/{agent_id}
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "name": "Updated Agent Name",
  "configuration": {
    "temperature": 0.8
  }
}
```

### Delete Agent
```http
DELETE /api/v1/agents/{agent_id}
Authorization: Bearer <access_token>
```

## Memories API

### Create Memory
```http
POST /api/v1/memories
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "title": "Important Notes",
  "content": "This is important information to remember",
  "type": "note",
  "tags": ["important", "work"],
  "metadata": {
    "source": "meeting",
    "date": "2024-01-15"
  }
}
```

### Search Memories
```http
GET /api/v1/memories/search?query=important&limit=10
Authorization: Bearer <access_token>
```

**Response:**
```json
{
  "memories": [
    {
      "id": "memory_789",
      "title": "Important Notes",
      "content": "This is important information to remember",
      "type": "note",
      "relevance_score": 0.95,
      "created_at": "2024-01-01T00:00:00Z"
    }
  ],
  "total": 1,
  "query": "important"
}
```

### Get Memory
```http
GET /api/v1/memories/{memory_id}
Authorization: Bearer <access_token>
```

### Update Memory
```http
PATCH /api/v1/memories/{memory_id}
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "title": "Updated Title",
  "tags": ["updated", "important"]
}
```

## Chat API

### Start Chat Session
```http
POST /api/v1/chat/sessions
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "agent_id": "agent_456",
  "context": {
    "user_preferences": {
      "language": "vi"
    }
  }
}
```

**Response:**
```json
{
  "session_id": "session_101",
  "agent_id": "agent_456",
  "status": "active",
  "created_at": "2024-01-15T10:30:00Z"
}
```

### Send Message
```http
POST /api/v1/chat/sessions/{session_id}/messages
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "content": "Hello, how can you help me?",
  "type": "text",
  "attachments": []
}
```

**Response:**
```json
{
  "message_id": "msg_202",
  "content": "Hello! I'm here to help you with any questions or tasks you have. What would you like to know?",
  "type": "text",
  "sender": "agent",
  "timestamp": "2024-01-15T10:31:00Z",
  "metadata": {
    "processing_time": 1.2,
    "tokens_used": 45
  }
}
```

### Get Chat History
```http
GET /api/v1/chat/sessions/{session_id}/messages?limit=50&offset=0
Authorization: Bearer <access_token>
```

### End Chat Session
```http
DELETE /api/v1/chat/sessions/{session_id}
Authorization: Bearer <access_token>
```

## File Upload API

### Upload File
```http
POST /api/v1/files/upload
Authorization: Bearer <access_token>
Content-Type: multipart/form-data

file: <binary_file_data>
purpose: "document_analysis"
metadata: {"description": "Contract document"}
```

**Response:**
```json
{
  "file_id": "file_303",
  "filename": "contract.pdf",
  "size": 1048576,
  "content_type": "application/pdf",
  "purpose": "document_analysis",
  "status": "uploaded",
  "upload_url": "/api/v1/files/file_303",
  "created_at": "2024-01-15T10:32:00Z"
}
```

### Get File Info
```http
GET /api/v1/files/{file_id}
Authorization: Bearer <access_token>
```

### Download File
```http
GET /api/v1/files/{file_id}/download
Authorization: Bearer <access_token>
```

### Process File
```http
POST /api/v1/files/{file_id}/process
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "processing_type": "text_extraction",
  "options": {
    "language": "vi",
    "extract_tables": true
  }
}
```

## Voice API

### Speech to Text
```http
POST /api/v1/voice/speech-to-text
Authorization: Bearer <access_token>
Content-Type: multipart/form-data

audio: <binary_audio_data>
language: "vi-VN"
```

**Response:**
```json
{
  "transcription": "Xin chào, tôi muốn hỏi về dịch vụ của bạn",
  "confidence": 0.98,
  "language": "vi-VN",
  "duration": 3.5,
  "words": [
    {"word": "Xin", "start_time": 0.0, "end_time": 0.3},
    {"word": "chào", "start_time": 0.3, "end_time": 0.6}
  ]
}
```

### Text to Speech
```http
POST /api/v1/voice/text-to-speech
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "text": "Xin chào! Tôi có thể giúp gì cho bạn?",
  "language": "vi-VN",
  "voice": "female",
  "speed": 1.0
}
```

**Response:**
```json
{
  "audio_url": "/api/v1/voice/audio/audio_404.wav",
  "duration": 2.8,
  "format": "wav",
  "language": "vi-VN"
}
```

## Controllers API

### Desktop Controller
```http
POST /api/v1/controllers/apps/desktop/screen-capture
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "region": {
    "x": 0,
    "y": 0,
    "width": 1920,
    "height": 1080
  },
  "format": "png"
}
```

### Mobile Controller
```http
POST /api/v1/controllers/mobile/push-notification
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "device_tokens": ["token123"],
  "title": "Thông báo mới",
  "body": "Bạn có tin nhắn mới từ ZETA AI",
  "data": {
    "message_id": "msg_505",
    "action": "open_chat"
  }
}
```

### Voice Controller
```http
POST /api/v1/controllers/voice/command
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "command": "Mở ứng dụng calendar",
  "audio_data": "base64_encoded_audio",
  "language": "vi-VN"
}
```

## Monitoring API

### System Health
```http
GET /api/v1/monitoring/health
Authorization: Bearer <access_token>
```

**Response:**
```json
{
  "status": "healthy",
  "cpu_usage": 25.5,
  "memory_usage": 68.2,
  "disk_usage": 45.8,
  "active_connections": 150,
  "uptime": 86400,
  "last_check": "2024-01-15T10:35:00Z"
}
```

### API Metrics
```http
GET /api/v1/monitoring/metrics?endpoint=/api/v1/chat&time_range=24h
Authorization: Bearer <access_token>
```

**Response:**
```json
[
  {
    "endpoint": "/api/v1/chat",
    "method": "POST",
    "total_requests": 2340,
    "success_rate": 99.1,
    "avg_response_time": 89.5,
    "error_count": 21,
    "last_24h_requests": 156
  }
]
```

## Analytics API

### Usage Analytics
```http
GET /api/v1/analytics/usage?time_range=7d
Authorization: Bearer <access_token>
```

### Performance Analytics
```http
GET /api/v1/analytics/performance?time_range=24h
Authorization: Bearer <access_token>
```

### Custom Report
```http
POST /api/v1/analytics/report
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "type": "custom",
  "time_range": "30d",
  "metrics": ["user_activity", "api_usage", "performance"],
  "filters": {
    "user_type": "active",
    "feature": "chat"
  }
}
```

## System API

### System Information
```http
GET /api/v1/system/info
Authorization: Bearer <admin_token>
```

### System Configuration
```http
GET /api/v1/system/config?section=database
Authorization: Bearer <admin_token>
```

### Update Configuration
```http
PATCH /api/v1/system/config
Authorization: Bearer <admin_token>
Content-Type: application/json

{
  "section": "api",
  "key": "max_requests",
  "value": 2000,
  "description": "Increase rate limit"
}
```

### Maintenance Mode
```http
POST /api/v1/system/maintenance
Authorization: Bearer <admin_token>
Content-Type: application/json

{
  "enabled": true,
  "message": "System maintenance in progress",
  "estimated_duration": 60
}
```

## Error Codes

### HTTP Status Codes
- `200` - Success
- `201` - Created
- `204` - No Content
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `422` - Validation Error
- `429` - Rate Limit Exceeded
- `500` - Internal Server Error

### Custom Error Codes
```json
{
  "error": {
    "code": "AGENT_NOT_FOUND",
    "message": "The specified agent was not found",
    "details": {
      "agent_id": "agent_456"
    }
  }
}
```

### Common Error Responses

#### Authentication Error
```json
{
  "detail": "Invalid authentication credentials"
}
```

#### Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

#### Rate Limit Error
```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Too many requests",
    "retry_after": 60
  }
}
```

## Rate Limiting

All API endpoints are subject to rate limiting:
- **Authenticated users**: 1000 requests per hour
- **Premium users**: 5000 requests per hour
- **Chat endpoints**: 100 requests per minute
- **File upload**: 10 requests per minute

Rate limit headers are included in responses:
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1642780800
```

## WebSocket API

### Chat WebSocket
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/chat/{session_id}?token={access_token}');

// Send message
ws.send(JSON.stringify({
  type: 'message',
  content: 'Hello!'
}));

// Receive message
ws.onmessage = function(event) {
  const data = JSON.parse(event.data);
  console.log('Received:', data);
};
```

### Voice WebSocket
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/voice?token={access_token}');

// Send audio chunk
ws.send(audioChunk);

// Receive transcription
ws.onmessage = function(event) {
  const data = JSON.parse(event.data);
  if (data.type === 'transcription') {
    console.log('Transcription:', data.text);
  }
};
```

## SDK Examples

### Python SDK
```python
from zeta_ai_sdk import ZetaAI

client = ZetaAI(api_key="your_api_key")

# Create agent
agent = client.agents.create(
    name="My Assistant",
    type="general"
)

# Start chat
session = client.chat.start_session(agent_id=agent.id)

# Send message
response = client.chat.send_message(
    session_id=session.id,
    message="Hello!"
)

print(response.content)
```

### JavaScript SDK
```javascript
import { ZetaAI } from 'zeta-ai-sdk';

const client = new ZetaAI({
  apiKey: 'your_api_key'
});

// Create agent
const agent = await client.agents.create({
  name: 'My Assistant',
  type: 'general'
});

// Start chat
const session = await client.chat.startSession({
  agentId: agent.id
});

// Send message
const response = await client.chat.sendMessage({
  sessionId: session.id,
  message: 'Hello!'
});

console.log(response.content);
```

---

For more information, visit our [Developer Portal](https://developers.zeta.ai) or contact support at support@zeta.ai.
