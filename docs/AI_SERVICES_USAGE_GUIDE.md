# 🤖 HƯỚNG DẪN SỬ DỤNG AI SERVICES

## 📋 Tổng quan

Hệ thống AI Services mới cung cấp kiến trúc microservices cho các tính năng AI, bao gồm:

- **Service Orchestrator** - Điều phối các AI services
- **Capability Registry** - Đăng ký và quản lý khả năng AI
- **Chat Service** - Hệ thống chat thông minh với intent recognition
- **Production RAG Service** - Retrieval-Augmented Generation cho Q&A

## 🚀 Quick Start

### 1. Import các components cần thiết

```python
from zeta_vn.app.ai import (
    AIServiceOrchestrator,
    ChatService,
    ProductionRAGService,
    AIRequest,
    get_ai_orchestrator,
    get_capability_registry
)
```

### 2. Setup AI Services

```python
async def setup_ai_services():
    # Lấy orchestrator và registry
    orchestrator = get_ai_orchestrator()
    registry = get_capability_registry()
    
    # Tạo services
    chat_service = ChatService()
    rag_service = ProductionRAGService()
    
    # Đăng ký services
    orchestrator.register_service(chat_service)
    orchestrator.register_service(rag_service)
    
    # Đăng ký capabilities
    orchestrator.register_capability("chat", "chat_service")
    orchestrator.register_capability("rag", "production_rag_service")
    
    # Khởi động
    await orchestrator.start()
    return orchestrator
```

### 3. Sử dụng Chat Service

```python
async def chat_example(orchestrator: AIServiceOrchestrator):
    request = AIRequest(
        request_id="chat_001",
        user_id="user123",
        capability="chat",
        payload={
            "message": "Hello, how can you help me?",
            "conversation_id": None  # Tạo conversation mới
        }
    )
    
    response = await orchestrator.process_request(request)
    
    if response.success:
        print(f"Response: {response.result['message']}")
        print(f"Intent: {response.result['intent']}")
        print(f"Conversation ID: {response.result['conversation_id']}")
```

### 4. Sử dụng RAG Service

```python
async def rag_example(orchestrator: AIServiceOrchestrator):
    # Đầu tiên, index một số documents
    rag_service = orchestrator._services["production_rag_service"]
    
    document = RAGDocument(
        id="doc_1",
        title="AI Guide",
        content="Artificial Intelligence is...",
        source="documentation"
    )
    
    await rag_service.index_document(document)
    
    # Sau đó query
    request = AIRequest(
        request_id="rag_001",
        user_id="user123",
        capability="rag",
        payload={
            "query": "What is AI?",
            "max_results": 3,
            "similarity_threshold": 0.7
        }
    )
    
    response = await orchestrator.process_request(request)
    
    if response.success:
        print(f"Answer: {response.result['answer']}")
        print(f"Sources: {len(response.result['sources'])}")
```

## 🏗️ Kiến trúc Components

### AIServiceOrchestrator

Central coordinator cho tất cả AI services:

```python
class AIServiceOrchestrator:
    async def process_request(self, request: AIRequest) -> AIResponse
    async def get_service_status(self) -> Dict[str, Dict[str, Any]]
    async def get_capabilities(self) -> List[str]
    def register_service(self, service: BaseAIService) -> None
    def register_capability(self, capability: str, service_name: str) -> None
```

**Use cases:**
- Routing requests đến đúng service
- Load balancing và health monitoring
- Centralized logging và metrics

### AICapabilityRegistry

Service discovery và health monitoring:

```python
class AICapabilityRegistry:
    def register_capability(self, name: str, description: str, ...) -> None
    def get_capability(self, name: str) -> CapabilityInfo | None
    def list_capabilities(self, status: CapabilityStatus = None) -> List[CapabilityInfo]
    async def health_check(self, capability_name: str = None) -> Dict[str, HealthCheckResult]
```

**Use cases:**
- Dynamic service discovery
- Health monitoring và alerting
- Capability metadata management

### ChatService

Conversational AI với context management:

```python
class ChatService(BaseAIService, CapabilityProvider):
    async def process(self, request: AIRequest) -> AIResponse
    async def get_conversation_history(self, conversation_id: str, user_id: str) -> Dict[str, Any]
    async def list_user_conversations(self, user_id: str, limit: int = 20) -> List[Dict[str, Any]]
```

**Features:**
- Intent classification (greeting, question, request, complaint, etc.)
- Entity extraction
- Conversation context tracking
- Response suggestions
- Multi-user support

### ProductionRAGService

Production-ready RAG với advanced features:

```python
class ProductionRAGService(BaseAIService, CapabilityProvider):
    async def index_document(self, document: RAGDocument) -> bool
    async def search(self, query: RAGQuery) -> List[RAGResult]
    async def query(self, query: RAGQuery) -> RAGResponse
```

**Features:**
- Document chunking và embedding
- Query optimization
- Result ranking với boost factors
- Answer generation
- Caching và performance optimization

## 🔧 Configuration

### Environment Variables

```bash
# OpenAI (for embeddings)
OPENAI_API_KEY=your_openai_key

# Logging
LOG_LEVEL=INFO

# Service Configuration
AI_SERVICE_MAX_WORKERS=4
AI_SERVICE_HEALTH_CHECK_INTERVAL=30
RAG_CACHE_TTL=3600
```

### Service Configuration

```python
# Custom service configuration
orchestrator = AIServiceOrchestrator()
orchestrator._max_workers = 8  # Increase workers
orchestrator._health_check_interval = 15  # More frequent health checks

# RAG Service configuration
rag_service = ProductionRAGService()
rag_service._cache_ttl = 7200  # 2 hours cache
```

## 📊 Monitoring và Debugging

### Health Checks

```python
# Check all services health
status = await orchestrator.get_service_status()
for service_name, health in status.items():
    print(f"{service_name}: {health['status']} ({'healthy' if health['healthy'] else 'unhealthy'})")

# Check specific capability
registry = get_capability_registry()
health_results = await registry.health_check("chat")
```

### Metrics và Logging

```python
# Service metrics
stats = registry.get_registry_stats()
print(f"Total capabilities: {stats['total_capabilities']}")
print(f"Available: {stats['available_capabilities']}")

# RAG metrics
rag_stats = await rag_service.get_document_stats()
print(f"Indexed documents: {rag_stats['total_documents']}")
print(f"Vector count: {rag_stats['total_vectors']}")
```

### Error Handling

```python
async def robust_ai_request(orchestrator, request):
    try:
        response = await orchestrator.process_request(request)
        if not response.success:
            logger.error(f"AI request failed: {response.error}")
            return None
        return response.result
    except Exception as e:
        logger.exception(f"AI request exception: {e}")
        return None
```

## 🔌 Integration với API

### FastAPI Integration

```python
# zeta_vn/app/api/v1/ai_enhanced.py
from fastapi import APIRouter, Depends
from zeta_vn.app.ai import get_ai_orchestrator, AIRequest

router = APIRouter(prefix="/ai", tags=["ai"])

@router.post("/chat")
async def chat_endpoint(
    message: str,
    conversation_id: str = None,
    orchestrator = Depends(get_ai_orchestrator)
):
    request = AIRequest(
        request_id=str(uuid.uuid4()),
        user_id="current_user",  # From auth
        capability="chat",
        payload={
            "message": message,
            "conversation_id": conversation_id
        }
    )
    
    response = await orchestrator.process_request(request)
    return response.result if response.success else {"error": response.error}

@router.post("/rag/query")
async def rag_query_endpoint(
    query: str,
    max_results: int = 5,
    orchestrator = Depends(get_ai_orchestrator)
):
    request = AIRequest(
        request_id=str(uuid.uuid4()),
        user_id="current_user",
        capability="rag",
        payload={
            "query": query,
            "max_results": max_results,
            "similarity_threshold": 0.7
        }
    )
    
    response = await orchestrator.process_request(request)
    return response.result if response.success else {"error": response.error}
```

### WebSocket Integration

```python
# Real-time chat with WebSocket
@router.websocket("/chat/ws")
async def chat_websocket(
    websocket: WebSocket,
    orchestrator = Depends(get_ai_orchestrator)
):
    await websocket.accept()
    
    try:
        while True:
            data = await websocket.receive_json()
            
            request = AIRequest(
                request_id=str(uuid.uuid4()),
                user_id=data.get("user_id"),
                capability="chat",
                payload=data
            )
            
            response = await orchestrator.process_request(request)
            await websocket.send_json(response.result if response.success else {"error": response.error})
            
    except WebSocketDisconnect:
        pass
```

## 🧪 Testing

### Unit Tests

```python
import pytest
from zeta_vn.app.ai import ChatService, AIRequest

@pytest.mark.asyncio
async def test_chat_service():
    service = ChatService()
    await service.start()
    
    request = AIRequest(
        request_id="test_001",
        user_id="test_user",
        capability="chat",
        payload={"message": "Hello"}
    )
    
    response = await service.process(request)
    
    assert response.success
    assert "Hello" in response.result["message"] or "Hi" in response.result["message"]
    
    await service.stop()
```

### Integration Tests

```python
@pytest.mark.asyncio
async def test_full_ai_pipeline():
    orchestrator = get_ai_orchestrator()
    
    # Setup services
    chat_service = ChatService()
    orchestrator.register_service(chat_service)
    orchestrator.register_capability("chat", "chat_service")
    
    await orchestrator.start()
    
    # Test request
    request = AIRequest(
        request_id="integration_test",
        user_id="test_user",
        capability="chat",
        payload={"message": "Test message"}
    )
    
    response = await orchestrator.process_request(request)
    
    assert response.success
    assert response.result is not None
    
    await orchestrator.stop()
```

## 🚀 Production Deployment

### Docker Configuration

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import asyncio; from health_check import check_ai_services; asyncio.run(check_ai_services())"

CMD ["uvicorn", "zeta_vn.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Health Check Script

```python
# health_check.py
async def check_ai_services():
    try:
        orchestrator = get_ai_orchestrator()
        status = await orchestrator.get_service_status()
        
        for service_name, health in status.items():
            if not health["healthy"]:
                raise Exception(f"Service {service_name} unhealthy")
        
        print("All AI services healthy")
        return True
    except Exception as e:
        print(f"Health check failed: {e}")
        return False
```

### Kubernetes Deployment

```yaml
# k8s-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: zeta-ai-services
spec:
  replicas: 3
  selector:
    matchLabels:
      app: zeta-ai-services
  template:
    metadata:
      labels:
        app: zeta-ai-services
    spec:
      containers:
      - name: zeta-ai
        image: zeta-ai:latest
        ports:
        - containerPort: 8000
        env:
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: ai-secrets
              key: openai-api-key
        livenessProbe:
          httpGet:
            path: /health/ai
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health/ai
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
```

## 🎯 Best Practices

### 1. Service Design
- Mỗi service độc lập và có thể test riêng
- Sử dụng dependency injection
- Implement proper error handling
- Maintain service contracts

### 2. Performance
- Cache frequent queries
- Use connection pooling
- Monitor response times
- Implement circuit breakers

### 3. Security
- Validate all inputs
- Implement rate limiting
- Use proper authentication
- Log security events

### 4. Scalability
- Design for horizontal scaling
- Use async/await consistently
- Implement proper backpressure
- Monitor resource usage

## 🔄 Migration từ Legacy Code

### Từ old RAG implementation

```python
# Old way
from zeta_vn.app.ai.rag.pipeline import RAGPipeline

# New way
from zeta_vn.app.ai import ProductionRAGService

# Migration script
async def migrate_to_production_rag():
    # Setup new service
    rag_service = ProductionRAGService()
    await rag_service.start()
    
    # Migrate documents
    # ... migration logic
    
    return rag_service
```

### Từ manual chat handling

```python
# Old way - manual chat handling
def handle_chat(message, user_id):
    # Manual intent detection
    if "hello" in message.lower():
        return "Hi there!"
    # ... more manual logic

# New way - service-based
async def handle_chat_new(message, user_id, orchestrator):
    request = AIRequest(
        request_id=str(uuid.uuid4()),
        user_id=user_id,
        capability="chat",
        payload={"message": message}
    )
    
    response = await orchestrator.process_request(request)
    return response.result["message"] if response.success else "Error"
```

## 📞 Support

Nếu có vấn đề, liên hệ:
- GitHub Issues: [repository-link]
- Documentation: [docs-link]
- Team Chat: [chat-link]
