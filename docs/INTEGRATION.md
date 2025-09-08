# 🌍 Integration Guide - ZETA AI Server

Complete guide for integrating ZETA AI Server with external systems, applications, and services. This document covers APIs, SDKs, webhooks, and best practices for seamless integration.

## 🚀 Integration Overview

ZETA AI Server provides multiple integration methods:

- REST API - Full-featured HTTP API for all operations
- WebSocket API - Real-time communication for chat applications
- SDKs - Official libraries for popular programming languages
- Webhooks - Event-driven notifications for your applications
- OAuth2 - Secure authentication for third-party integrations

## 🚀 Quick Integration

### 30-Second API Test

```bash
# 1. Get API token
curl -X POST "https://api.zeta-ai.com/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "your_username", "password": "your_password"}'

# 2. Create an agent
curl -X POST "https://api.zeta-ai.com/api/v1/agents" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Agent", "description": "My first agent"}'

# 3. Start chatting
curl -X POST "https://api.zeta-ai.com/api/v1/chat/conversations" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"agent_id": "AGENT_ID", "title": "Test Chat"}'
```

---

## 🔗 REST API Integration

### Authentication

All API requests require authentication using JWT tokens:

```http
Authorization: Bearer <your-access-token>
Content-Type: application/json
```

### Error Handling

```python
import requests

def make_api_request(endpoint, method="GET", data=None):
    """Make authenticated API request with error handling."""
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.request(
            method=method,
            url=f"https://api.zeta-ai.com/api/v1{endpoint}",
            headers=headers,
            json=data,
            timeout=30
        )

        # Handle different response codes
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            raise AuthenticationError("Invalid or expired token")
        elif response.status_code == 429:
            raise RateLimitError("Rate limit exceeded")
        elif response.status_code >= 400:
            error_data = response.json()
            raise APIError(f"API Error: {error_data.get('message', 'Unknown error')}")

    except requests.RequestException as e:
        raise NetworkError(f"Network error: {e}")

# Usage example
try:
    agents = make_api_request("/agents")
    print(f"Found {len(agents['items'])} agents")
except APIError as e:
    print(f"API Error: {e}")
```

### Rate Limiting

Implement exponential backoff for rate-limited requests:

```python
import time
import random

def request_with_retry(func, max_retries=3):
    """Execute request with exponential backoff retry."""
    for attempt in range(max_retries):
        try:
            return func()
        except RateLimitError:
            if attempt == max_retries - 1:
                raise
            wait_time = (2 ** attempt) + random.uniform(0, 1)
            time.sleep(wait_time)

# Usage
result = request_with_retry(
    lambda: make_api_request("/agents", "POST", agent_data)
)
```

---

## 📱 SDK Integration

### Python SDK

```bash
pip install zeta-ai-sdk
```

```python
from zeta_ai import ZetaAIClient
import asyncio

async def main():
    # Initialize client
    client = ZetaAIClient(
        api_key="your-api-key",
        base_url="https://api.zeta-ai.com"
    )

    # Create an agent
    agent = await client.agents.create(
        name="Python Assistant",
        description="Helps with Python programming",
        config={
            "model": "gpt-4",
            "temperature": 0.7,
            "system_prompt": "You are a Python expert."
        }
    )

    # Start conversation
    conversation = await client.chat.create_conversation(
        agent_id=agent.id,
        title="Python Help"
    )

    # Send message
    response = await client.chat.send_message(
        conversation_id=conversation.id,
        content="How do I handle exceptions in Python?"
    )

    print(f"Agent response: {response.content}")

# Run async function
asyncio.run(main())
```

### JavaScript/TypeScript SDK

```bash
npm install @zeta-ai/sdk
```

```typescript
import { ZetaAIClient } from '@zeta-ai/sdk';

const client = new ZetaAIClient({
  apiKey: 'your-api-key',
  baseURL: 'https://api.zeta-ai.com'
});

async function createAndChat() {
  try {
    // Create agent
    const agent = await client.agents.create({
      name: 'JavaScript Helper',
      description: 'Helps with JavaScript development',
      config: {
        model: 'gpt-4',
        temperature: 0.7,
        systemPrompt: 'You are a JavaScript expert.'
      }
    });

    // Create conversation
    const conversation = await client.chat.createConversation({
      agentId: agent.id,
      title: 'JS Help Session'
    });

    // Send message
    const response = await client.chat.sendMessage({
      conversationId: conversation.id,
      content: 'Explain async/await in JavaScript',
      role: 'user'
    });

    console.log('Response:', response.content);
  } catch (error) {
    console.error('Error:', error);
  }
}

createAndChat();
```

### Go SDK

```bash
go get github.com/zeta-ai/go-sdk
```

```go
package main

import (
    "context"
    "fmt"
    "log"

    "github.com/zeta-ai/go-sdk"
)

func main() {
    client := zetasdk.NewClient("your-api-key")
    ctx := context.Background()

    // Create agent
    agent, err := client.Agents.Create(ctx, &zetasdk.CreateAgentRequest{
        Name:        "Go Helper",
        Description: "Helps with Go programming",
        Config: &zetasdk.AgentConfig{
            Model:        "gpt-4",
            Temperature:  0.7,
            SystemPrompt: "You are a Go expert.",
        },
    })
    if err != nil {
        log.Fatal(err)
    }

    // Create conversation
    conv, err := client.Chat.CreateConversation(ctx, &zetasdk.CreateConversationRequest{
        AgentID: agent.ID,
        Title:   "Go Help",
    })
    if err != nil {
        log.Fatal(err)
    }

    // Send message
    response, err := client.Chat.SendMessage(ctx, &zetasdk.SendMessageRequest{
        ConversationID: conv.ID,
        Content:        "How do I handle errors in Go?",
        Role:          "user",
    })
    if err != nil {
        log.Fatal(err)
    }

    fmt.Printf("Response: %s\n", response.Content)
}
```

---

## 🔄 WebSocket Integration

### Real-time Chat

```javascript
// Connect to WebSocket
const ws = new WebSocket('wss://api.zeta-ai.com/ws/chat');

// Authentication
ws.onopen = function() {
    ws.send(JSON.stringify({
        type: 'auth',
        token: 'your-jwt-token'
    }));
};

// Handle messages
ws.onmessage = function(event) {
    const message = JSON.parse(event.data);

    switch(message.type) {
        case 'auth_success':
            console.log('Authenticated successfully');
            joinConversation('conversation-id');
            break;

        case 'message':
            displayMessage(message.data);
            break;

        case 'typing':
            showTypingIndicator(message.data.user);
            break;

        case 'error':
            console.error('WebSocket error:', message.error);
            break;
    }
};

// Join conversation
function joinConversation(conversationId) {
    ws.send(JSON.stringify({
        type: 'join_conversation',
        conversation_id: conversationId
    }));
}

// Send message
function sendMessage(content) {
    ws.send(JSON.stringify({
        type: 'send_message',
        content: content,
        role: 'user'
    }));
}

// Handle connection errors
ws.onerror = function(error) {
    console.error('WebSocket error:', error);
};

ws.onclose = function() {
    console.log('WebSocket connection closed');
    // Implement reconnection logic
    setTimeout(connectWebSocket, 5000);
};
```

### Streaming Responses

```python
import asyncio
import websockets
import json

async def stream_chat():
    uri = "wss://api.zeta-ai.com/ws/chat"

    async with websockets.connect(uri) as websocket:
        # Authenticate
        await websocket.send(json.dumps({
            "type": "auth",
            "token": "your-jwt-token"
        }))

        # Join conversation
        await websocket.send(json.dumps({
            "type": "join_conversation",
            "conversation_id": "conv-123"
        }))

        # Send message and stream response
        await websocket.send(json.dumps({
            "type": "send_message_stream",
            "content": "Tell me a story",
            "role": "user"
        }))

        # Receive streaming response
        async for message in websocket:
            data = json.loads(message)

            if data["type"] == "stream_start":
                print("AI is thinking...")
            elif data["type"] == "stream_content":
                print(data["content"], end="", flush=True)
            elif data["type"] == "stream_end":
                print("\nStream complete")
                break

asyncio.run(stream_chat())
```

---

## 🔔 Webhook Integration

### Setting Up Webhooks

```python
import requests

def setup_webhook():
    """Configure webhook to receive events."""
    webhook_config = {
        "url": "https://your-server.com/webhook/zeta-ai",
        "events": [
            "conversation.created",
            "message.sent",
            "agent.updated",
            "user.registered"
        ],
        "secret": "your-webhook-secret"
    }

    response = requests.post(
        "https://api.zeta-ai.com/api/v1/webhooks",
        headers={"Authorization": f"Bearer {api_token}"},
        json=webhook_config
    )

    return response.json()
```

### Webhook Handler

```python
from flask import Flask, request, jsonify
import hashlib
import hmac

app = Flask(__name__)
WEBHOOK_SECRET = "your-webhook-secret"

def verify_webhook_signature(payload, signature):
    """Verify webhook signature for security."""
    expected_signature = hmac.new(
        WEBHOOK_SECRET.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(f"sha256={expected_signature}", signature)

@app.route('/webhook/zeta-ai', methods=['POST'])
def handle_webhook():
    # Verify signature
    signature = request.headers.get('X-Signature-256')
    if not verify_webhook_signature(request.data, signature):
        return jsonify({"error": "Invalid signature"}), 401

    event = request.json
    event_type = event.get('type')

    # Handle different event types
    if event_type == 'conversation.created':
        handle_conversation_created(event['data'])
    elif event_type == 'message.sent':
        handle_message_sent(event['data'])
    elif event_type == 'agent.updated':
        handle_agent_updated(event['data'])

    return jsonify({"status": "received"})

def handle_conversation_created(data):
    """Handle new conversation event."""
    print(f"New conversation: {data['id']} by user {data['user_id']}")

    # Send welcome message
    send_welcome_message(data['id'])

def handle_message_sent(data):
    """Handle message sent event."""
    if data['role'] == 'user':
        # Log user message for analytics
        log_user_interaction(data)

def send_welcome_message(conversation_id):
    """Send automated welcome message."""
    welcome_text = "Welcome! How can I help you today?"

    requests.post(
        f"https://api.zeta-ai.com/api/v1/chat/conversations/{conversation_id}/messages",
        headers={"Authorization": f"Bearer {api_token}"},
        json={
            "content": welcome_text,
            "role": "assistant",
            "automated": True
        }
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

---

## 🔐 OAuth2 Integration

### Authorization Code Flow

```python
from flask import Flask, request, redirect, session
import requests
import secrets

app = Flask(__name__)
app.secret_key = 'your-secret-key'

# OAuth2 configuration
OAUTH_CONFIG = {
    "client_id": "your-client-id",
    "client_secret": "your-client-secret",
    "authorize_url": "https://api.zeta-ai.com/oauth/authorize",
    "token_url": "https://api.zeta-ai.com/oauth/token",
    "redirect_uri": "https://your-app.com/oauth/callback"
}

@app.route('/login')
def login():
    """Initiate OAuth2 login flow."""
    state = secrets.token_urlsafe(32)
    session['oauth_state'] = state

    auth_url = (
        f"{OAUTH_CONFIG['authorize_url']}"
        f"?client_id={OAUTH_CONFIG['client_id']}"
        f"&response_type=code"
        f"&redirect_uri={OAUTH_CONFIG['redirect_uri']}"
        f"&scope=read write"
        f"&state={state}"
    )

    return redirect(auth_url)

@app.route('/oauth/callback')
def oauth_callback():
    """Handle OAuth2 callback."""
    # Verify state parameter
    if request.args.get('state') != session.get('oauth_state'):
        return "Invalid state parameter", 400

    # Exchange authorization code for access token
    code = request.args.get('code')
    if not code:
        return "Authorization code not provided", 400

    token_data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": OAUTH_CONFIG['redirect_uri'],
        "client_id": OAUTH_CONFIG['client_id'],
        "client_secret": OAUTH_CONFIG['client_secret']
    }

    response = requests.post(OAUTH_CONFIG['token_url'], data=token_data)

    if response.status_code == 200:
        tokens = response.json()
        session['access_token'] = tokens['access_token']
        session['refresh_token'] = tokens['refresh_token']

        return redirect('/dashboard')
    else:
        return "Failed to obtain access token", 400

@app.route('/dashboard')
def dashboard():
    """Protected route requiring authentication."""
    access_token = session.get('access_token')
    if not access_token:
        return redirect('/login')

    # Use access token to make API calls
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(
        "https://api.zeta-ai.com/api/v1/users/me",
        headers=headers
    )

    if response.status_code == 200:
        user_info = response.json()
        return f"Welcome, {user_info['username']}!"
    else:
        return "Failed to fetch user info", 400
```

---

## 🛠️ Custom Tools Integration

### Creating Custom Tools

```python
from typing import Dict, Any
from pydantic import BaseModel

class WeatherTool(BaseModel):
    """Custom tool for weather information."""

    name: str = "get_weather"
    description: str = "Get current weather for a location"

    def execute(self, location: str) -> Dict[str, Any]:
        """Execute weather lookup."""
        # Integration with weather API
        import requests

        api_key = "your-weather-api-key"
        url = f"https://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": location,
            "appid": api_key,
            "units": "metric"
        }

        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            return {
                "location": data["name"],
                "temperature": data["main"]["temp"],
                "description": data["weather"][0]["description"],
                "humidity": data["main"]["humidity"]
            }
        else:
            return {"error": "Could not fetch weather data"}

# Register tool with agent
def register_custom_tool():
    """Register custom tool with ZETA AI agent."""
    tool_config = {
        "name": "get_weather",
        "description": "Get current weather for a location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city or location name"
                }
            },
            "required": ["location"]
        },
        "endpoint": "https://your-server.com/tools/weather"
    }

    response = requests.post(
        "https://api.zeta-ai.com/api/v1/tools",
        headers={"Authorization": f"Bearer {api_token}"},
        json=tool_config
    )

    return response.json()
```

### Tool Endpoint Handler

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/tools/weather', methods=['POST'])
def weather_tool():
    """Handle weather tool requests from ZETA AI."""
    data = request.json
    location = data.get('parameters', {}).get('location')

    if not location:
        return jsonify({"error": "Location parameter required"}), 400

    # Execute weather lookup
    weather_tool = WeatherTool()
    result = weather_tool.execute(location)

    return jsonify({
        "success": True,
        "result": result
    })
```

---

## 📈 Analytics Integration

### Usage Tracking

```python
def track_api_usage():
    """Track API usage and performance."""
    import time
    from functools import wraps

    def track_call(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()

            try:
                result = func(*args, **kwargs)
                success = True
                error = None
            except Exception as e:
                result = None
                success = False
                error = str(e)
                raise
            finally:
                end_time = time.time()
                duration = end_time - start_time

                # Send analytics data
                analytics_data = {
                    "function": func.__name__,
                    "duration": duration,
                    "success": success,
                    "error": error,
                    "timestamp": start_time
                }

                send_analytics(analytics_data)

            return result
        return wrapper
    return track_call

def send_analytics(data):
    """Send analytics data to tracking service."""
    # Send to your analytics platform
    requests.post(
        "https://analytics.yourcompany.com/api/events",
        json=data,
        headers={"Authorization": "Bearer analytics-token"}
    )

# Usage
@track_api_usage()
def create_agent(agent_data):
    return make_api_request("/agents", "POST", agent_data)
```

### Custom Metrics

```python
class ZetaAIMetrics:
    """Custom metrics collection for ZETA AI integration."""

    def __init__(self, metrics_endpoint):
        self.metrics_endpoint = metrics_endpoint
        self.metrics = []

    def record_conversation_start(self, agent_id, user_id):
        """Record conversation start event."""
        self.metrics.append({
            "type": "conversation_start",
            "agent_id": agent_id,
            "user_id": user_id,
            "timestamp": time.time()
        })

    def record_message_sent(self, conversation_id, tokens_used):
        """Record message sent with token usage."""
        self.metrics.append({
            "type": "message_sent",
            "conversation_id": conversation_id,
            "tokens_used": tokens_used,
            "timestamp": time.time()
        })

    def flush_metrics(self):
        """Send accumulated metrics to analytics service."""
        if self.metrics:
            requests.post(self.metrics_endpoint, json=self.metrics)
            self.metrics.clear()

# Usage
metrics = ZetaAIMetrics("https://analytics.yourcompany.com/api/metrics")
metrics.record_conversation_start(agent_id, user_id)
metrics.record_message_sent(conversation_id, 150)
metrics.flush_metrics()
```

---

## 🧩 Integration Patterns

### Microservices Architecture

```python
# Service discovery pattern
class ZetaAIService:
    """Service wrapper for ZETA AI integration in microservices."""

    def __init__(self, service_name, consul_client):
        self.service_name = service_name
        self.consul = consul_client
        self.base_url = self.discover_service()

    def discover_service(self):
        """Discover ZETA AI service via service discovery."""
        services = self.consul.health.service(
            'zeta-ai-api',
            passing=True
        )[1]

        if services:
            service = services[0]['Service']
            return f"http://{service['Address']}:{service['Port']}"
        else:
            raise Exception("ZETA AI service not available")

    async def create_agent_async(self, agent_data):
        """Create agent with async/await pattern."""
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/api/v1/agents",
                json=agent_data,
                headers={"Authorization": f"Bearer {self.api_token}"}
            ) as response:
                return await response.json()
```

### Event-Driven Integration

```python
import asyncio
from dataclasses import dataclass
from typing import Callable, List

@dataclass
class Event:
    type: str
    data: dict
    timestamp: float

class EventBus:
    """Event bus for ZETA AI integration events."""

    def __init__(self):
        self.subscribers = {}

    def subscribe(self, event_type: str, handler: Callable):
        """Subscribe to specific event type."""
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(handler)

    async def publish(self, event: Event):
        """Publish event to all subscribers."""
        if event.type in self.subscribers:
            tasks = [
                handler(event)
                for handler in self.subscribers[event.type]
            ]
            await asyncio.gather(*tasks)

# Usage
event_bus = EventBus()

# Subscribe to events
async def handle_new_message(event):
    print(f"New message: {event.data['content']}")

event_bus.subscribe("message.received", handle_new_message)

# Publish events
await event_bus.publish(Event(
    type="message.received",
    data={"content": "Hello!", "user_id": "123"},
    timestamp=time.time()
))
```

---

## 🚨 Error Handling & Resilience

### Circuit Breaker Pattern

```python
import time
from enum import Enum
from typing import Callable, Any

class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

class CircuitBreaker:
    """Circuit breaker for ZETA AI API calls."""

    def __init__(self, failure_threshold=5, timeout=60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = CircuitState.CLOSED

    def call(self, func: Callable, *args, **kwargs) -> Any:
        """Execute function with circuit breaker protection."""
        if self.state == CircuitState.OPEN:
            if time.time() - self.last_failure_time < self.timeout:
                raise Exception("Circuit breaker is OPEN")
            else:
                self.state = CircuitState.HALF_OPEN

        try:
            result = func(*args, **kwargs)
            self.on_success()
            return result
        except Exception as e:
            self.on_failure()
            raise e

    def on_success(self):
        """Reset circuit breaker on successful call."""
        self.failure_count = 0
        self.state = CircuitState.CLOSED

    def on_failure(self):
        """Handle failure and update circuit state."""
        self.failure_count += 1
        self.last_failure_time = time.time()

        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN

# Usage
circuit_breaker = CircuitBreaker()

def protected_api_call():
    return circuit_breaker.call(make_api_request, "/agents")
```

### Retry with Backoff

```python
import asyncio
import random
from typing import Callable, Any

async def retry_with_exponential_backoff(
    func: Callable,
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    jitter: bool = True
) -> Any:
    """Retry function with exponential backoff."""

    for attempt in range(max_retries + 1):
        try:
            if asyncio.iscoroutinefunction(func):
                return await func()
            else:
                return func()
        except Exception as e:
            if attempt == max_retries:
                raise e

            # Calculate delay with exponential backoff
            delay = min(base_delay * (2 ** attempt), max_delay)

            # Add jitter to prevent thundering herd
            if jitter:
                delay = delay * (0.5 + random.random() * 0.5)

            await asyncio.sleep(delay)

# Usage
async def api_call_with_retry():
    return await retry_with_exponential_backoff(
        lambda: make_api_request("/agents"),
        max_retries=3
    )
```

---

## 📚 Integration Examples

### E-commerce Integration

```python
class EcommerceAIAssistant:
    """AI assistant for e-commerce platform."""

    def __init__(self, zeta_client, product_catalog):
        self.zeta_client = zeta_client
        self.product_catalog = product_catalog
        self.agent_id = self.setup_shopping_agent()

    def setup_shopping_agent(self):
        """Create specialized shopping assistant agent."""
        agent = self.zeta_client.agents.create(
            name="Shopping Assistant",
            description="Helps customers find and choose products",
            config={
                "model": "gpt-4",
                "temperature": 0.7,
                "system_prompt": """
                You are a helpful shopping assistant. You can:
                - Help customers find products
                - Provide product recommendations
                - Answer questions about features and specifications
                - Assist with sizing and compatibility
                Always be friendly and helpful.
                """,
                "tools": ["product_search", "inventory_check"]
            }
        )
        return agent.id

    async def handle_customer_query(self, customer_id, query):
        """Handle customer shopping query."""
        # Create or get existing conversation
        conversation = await self.get_customer_conversation(customer_id)

        # Add product context if query mentions specific products
        context = await self.extract_product_context(query)

        # Send message to AI assistant
        response = await self.zeta_client.chat.send_message(
            conversation_id=conversation.id,
            content=query,
            context=context
        )

        return response.content

    async def extract_product_context(self, query):
        """Extract relevant product information for query."""
        # Search product catalog
        products = self.product_catalog.search(query)

        if products:
            return {
                "products": [
                    {
                        "name": p.name,
                        "price": p.price,
                        "description": p.description,
                        "in_stock": p.inventory > 0
                    }
                    for p in products[:5]  # Limit to top 5 results
                ]
            }
        return {}
```

### CRM Integration

```python
class CRMIntegration:
    """Integrate ZETA AI with CRM system."""

    def __init__(self, zeta_client, crm_api):
        self.zeta_client = zeta_client
        self.crm_api = crm_api
        self.setup_webhook_handlers()

    def setup_webhook_handlers(self):
        """Set up webhooks to sync data with CRM."""
        webhook_config = {
            "url": "https://your-crm.com/webhooks/zeta-ai",
            "events": [
                "conversation.created",
                "conversation.completed",
                "user.registered"
            ]
        }

        self.zeta_client.webhooks.create(webhook_config)

    async def create_lead_from_conversation(self, conversation_data):
        """Create CRM lead from AI conversation."""
        # Extract lead information from conversation
        lead_data = await self.extract_lead_info(conversation_data)

        # Create lead in CRM
        lead = await self.crm_api.leads.create({
            "name": lead_data.get("name"),
            "email": lead_data.get("email"),
            "phone": lead_data.get("phone"),
            "source": "AI Assistant",
            "notes": f"Generated from conversation {conversation_data['id']}"
        })

        # Store lead ID in conversation metadata
        await self.zeta_client.conversations.update_metadata(
            conversation_data['id'],
            {"crm_lead_id": lead.id}
        )

        return lead

    async def extract_lead_info(self, conversation_data):
        """Extract lead information from conversation."""
        # Use AI to extract structured data from conversation
        extraction_prompt = """
        Extract the following information from this conversation:
        - Customer name
        - Email address
        - Phone number
        - Company name
        - Interest level (1-10)
        - Key requirements

        Return as JSON format.
        """

        response = await self.zeta_client.chat.send_message(
            conversation_id=conversation_data['id'],
            content=extraction_prompt,
            role="system"
        )

        # Parse extracted data
        import json
        try:
            return json.loads(response.content)
        except json.JSONDecodeError:
            return {}
```

---

## 🔎 Monitoring & Observability

### Distributed Tracing

```python
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# Setup tracing
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

jaeger_exporter = JaegerExporter(
    agent_host_name="localhost",
    agent_port=6831,
)

span_processor = BatchSpanProcessor(jaeger_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

class TracedZetaAIClient:
    """ZETA AI client with distributed tracing."""

    def __init__(self, api_key):
        self.api_key = api_key
        self.tracer = trace.get_tracer(__name__)

    async def send_message(self, conversation_id, content):
        """Send message with tracing."""
        with self.tracer.start_as_current_span("zeta_ai_send_message") as span:
            span.set_attribute("conversation.id", conversation_id)
            span.set_attribute("message.length", len(content))

            try:
                response = await self._make_request(
                    f"/chat/conversations/{conversation_id}/messages",
                    "POST",
                    {"content": content, "role": "user"}
                )

                span.set_attribute("response.tokens", response.get("tokens_used", 0))
                span.set_status(trace.Status(trace.StatusCode.OK))

                return response
            except Exception as e:
                span.record_exception(e)
                span.set_status(trace.Status(trace.StatusCode.ERROR, str(e)))
                raise
```

### Health Checks

```python
class IntegrationHealthCheck:
    """Health check for ZETA AI integration."""

    def __init__(self, zeta_client):
        self.zeta_client = zeta_client

    async def check_health(self):
        """Comprehensive health check."""
        health_status = {
            "api_connectivity": False,
            "authentication": False,
            "agent_creation": False,
            "message_sending": False,
            "overall": False
        }

        try:
            # Test API connectivity
            health_response = await self.zeta_client.health.check()
            health_status["api_connectivity"] = health_response.get("status") == "healthy"

            # Test authentication
            user_info = await self.zeta_client.users.get_current()
            health_status["authentication"] = bool(user_info.get("id"))

            # Test agent creation
            test_agent = await self.create_test_agent()
            health_status["agent_creation"] = bool(test_agent)

            if test_agent:
                # Test message sending
                response = await self.send_test_message(test_agent["id"])
                health_status["message_sending"] = bool(response)

                # Cleanup test agent
                await self.zeta_client.agents.delete(test_agent["id"])

            # Overall health
            health_status["overall"] = all([
                health_status["api_connectivity"],
                health_status["authentication"],
                health_status["agent_creation"],
                health_status["message_sending"]
            ])

        except Exception as e:
            print(f"Health check failed: {e}")

        return health_status

    async def create_test_agent(self):
        """Create temporary test agent."""
        try:
            return await self.zeta_client.agents.create(
                name="Health Check Agent",
                description="Temporary agent for health checking",
                config={"model": "gpt-3.5-turbo", "temperature": 0.5}
            )
        except Exception:
            return None

    async def send_test_message(self, agent_id):
        """Send test message to verify functionality."""
        try:
            conv = await self.zeta_client.chat.create_conversation(
                agent_id=agent_id,
                title="Health Check"
            )

            response = await self.zeta_client.chat.send_message(
                conversation_id=conv.id,
                content="Health check test"
            )

            return response
        except Exception:
            return None
```

---

## 📖 Best Practices

### Security

1. API Key Management
   - Store API keys in environment variables
   - Rotate keys regularly
   - Use different keys for different environments

2. Webhook Security
   - Always verify webhook signatures
   - Use HTTPS endpoints
   - Implement replay attack protection

3. Data Privacy
   - Encrypt sensitive data in transit and at rest
   - Implement proper access controls
   - Follow data retention policies

### Performance

1. Connection Pooling
   - Use connection pools for HTTP clients
   - Configure appropriate timeouts
   - Implement proper retry logic

2. Caching
   - Cache frequently accessed data
   - Use appropriate cache TTLs
   - Implement cache invalidation strategies

3. Rate Limiting
   - Respect API rate limits
   - Implement client-side rate limiting
   - Use exponential backoff for retries

### Reliability

1. Error Handling
   - Implement comprehensive error handling
   - Use circuit breakers for external calls
   - Log errors with proper context

2. Monitoring
   - Monitor API response times
   - Track error rates and patterns
   - Set up alerts for critical issues

3. Testing
   - Write integration tests
   - Test error scenarios
   - Perform load testing

---

## 🧭 Support & Resources

### Documentation
- API Reference: ./API_REFERENCE.md
- User Guide: ./USER_GUIDE.md
- Troubleshooting: ./TROUBLESHOOTING.md

### SDKs
- Python SDK: https://github.com/zeta-ai/python-sdk
- JavaScript SDK: https://github.com/zeta-ai/javascript-sdk
- Go SDK: https://github.com/zeta-ai/go-sdk

### Community
- GitHub Issues: https://github.com/zeta-ai/zeta-ai-server/issues
- Discord Community: https://discord.gg/zeta-ai
- Stack Overflow: https://stackoverflow.com/questions/tagged/zeta-ai

### Support
- Email: integration-support@zeta-ai.com
- Slack: #integration-help (Enterprise customers)
- Documentation: https://docs.zeta-ai.com

---

Happy Integrating!

Last updated: 2025-08-14
