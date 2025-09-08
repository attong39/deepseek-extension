"""
Demo setup script for AI services integration.

Shows how to set up and use the new AI orchestrator, registry, and services.
"""

from __future__ import annotations

import asyncio

from apps.backend.core.observability.logging import get_logger
from apps.backend.core.services.ai import (
import Exception
import doc
import e
import enumerate
import i
import isinstance
import j
import key
import len
import print
import query_text
import req_data
import service
import service_name
import service_status
import source
import value
    AIRequest,
    AIServiceOrchestrator,
    ChatService,
    ProductionRAGService,
    RAGDocument,
    get_ai_orchestrator,
    get_capability_registry,
)
from apps.backend.data.adapters.vector import (
    ChunkingService,
    MemoryVectorStoreAdapter,
    OpenAIEmbeddingAdapter,
)

logger = get_logger(__name__)


async def setup_demo_ai_services() -> AIServiceOrchestrator:
    """Set up demo AI services for testing and demonstration."""
    logger.info("Setting up demo AI services...")

    # Get registry and orchestrator
    registry = get_capability_registry()
    orchestrator = get_ai_orchestrator()

    # Create core adapters for RAG với API key từ environment
    import os

    api_key = os.getenv("OPENAI_API_KEY", "demo-key-for-testing")

    if api_key == "demo-key-for-testing":
        logger.warning("Using demo API key - RAG features will be limited")

    embedding_adapter = OpenAIEmbeddingAdapter(api_key=api_key)
    vector_store = MemoryVectorStoreAdapter()
    chunking_service = ChunkingService()

    # Create services
    chat_service = ChatService()
    rag_service = ProductionRAGService(
        embedding_adapter=embedding_adapter,
        vector_store=vector_store,
        chunking_service=chunking_service,
    )

    # Register services with orchestrator
    orchestrator.register_service(chat_service)
    orchestrator.register_service(rag_service)

    # Register capabilities
    orchestrator.register_capability("chat", "chat_service")
    orchestrator.register_capability("rag", "production_rag_service")
    orchestrator.register_capability("qa", "production_rag_service")  # Alias

    # Register with capability registry
    registry.register_capability(
        name="chat",
        description="Conversational AI with intent recognition and context management",
        version="1.0.0",
        service_name="chat_service",
        provider=chat_service,
        tags=["conversation", "nlp", "intent"],
        metadata={"supported_languages": ["en"], "max_context_length": 4000},
    )

    registry.register_capability(
        name="rag",
        description="Retrieval-Augmented Generation for document Q&A",
        version="1.0.0",
        service_name="production_rag_service",
        provider=rag_service,
        tags=["retrieval", "qa", "documents"],
        metadata={"embedding_model": "openai", "chunk_size": 500},
    )

    # Start services
    await orchestrator.start()
    await registry.start_health_monitoring()

    logger.info("Demo AI services setup complete!")
    return orchestrator


async def demo_chat_service(orchestrator: AIServiceOrchestrator) -> None:
    """Demonstrate chat service functionality."""
    logger.info("--- Chat Service Demo ---")

    # Create chat requests
    chat_requests = [
        {"message": "Hello, how are you?", "user_id": "demo_user_1"},
        {"message": "What can you help me with?", "user_id": "demo_user_1"},
        {"message": "I have a problem with my account", "user_id": "demo_user_2"},
    ]

    for i, req_data in enumerate(chat_requests):
        request = AIRequest(
            request_id=f"chat_demo_{i}",
            user_id=req_data["user_id"],
            capability="chat",
            payload=req_data,
        )

        response = await orchestrator.process_request(request)

        if response.success:
            result = response.result
            logger.info(f"Chat Response: {result['message']}")
            logger.info(
                f"Intent: {result['intent']} (confidence: {result['confidence']:.2f})"
            )
            if result["suggestions"]:
                logger.info(f"Suggestions: {result['suggestions']}")
        else:
            logger.error(f"Chat error: {response.error}")

        print()


async def demo_rag_service(orchestrator: AIServiceOrchestrator) -> None:
    """Demonstrate RAG service functionality."""
    logger.info("--- RAG Service Demo ---")

    # Get RAG service for document indexing
    rag_service = None
    for service in orchestrator._services.values():
        if isinstance(service, ProductionRAGService):
            rag_service = service
            break

    if not rag_service:
        logger.error("RAG service not found")
        return

    # Index some demo documents
    demo_documents = [
        RAGDocument(
            id="doc_1",
            title="AI Introduction",
            content=(
                "Artificial Intelligence (AI) refers to the simulation of "
                "human intelligence in machines. AI systems can learn, "
                "reason, and make decisions."
            ),
            source="documentation",
            metadata={"category": "technology", "level": "beginner"},
        ),
        RAGDocument(
            id="doc_2",
            title="Machine Learning Basics",
            content=(
                "Machine Learning is a subset of AI that enables computers "
                "to learn and improve from experience without being "
                "explicitly programmed."
            ),
            source="tutorial",
            metadata={"category": "technology", "level": "intermediate"},
        ),
        RAGDocument(
            id="doc_3",
            title="Python Programming",
            content=(
                "Python is a high-level programming language known for its "
                "simplicity and versatility. It's widely used in AI and "
                "data science."
            ),
            source="guide",
            metadata={"category": "programming", "level": "beginner"},
        ),
    ]

    # Index documents
    for doc in demo_documents:
        success = await rag_service.index_document(doc)
        logger.info(f"Indexed document {doc.id}: {'success' if success else 'failed'}")

    # Test RAG queries
    rag_queries = [
        "What is artificial intelligence?",
        "How does machine learning work?",
        "Tell me about Python programming",
        "What are the differences between AI and ML?",
    ]

    for i, query_text in enumerate(rag_queries):
        request = AIRequest(
            request_id=f"rag_demo_{i}",
            user_id="demo_user",
            capability="rag",
            payload={
                "query": query_text,
                "max_results": 3,
                "similarity_threshold": 0.5,
            },
        )

        response = await orchestrator.process_request(request)

        if response.success:
            result = response.result
            logger.info(f"Query: {query_text}")
            logger.info(f"Answer: {result['answer']}")
            logger.info(f"Confidence: {result['confidence']:.2f}")
            logger.info(f"Sources: {len(result['sources'])}")

            for j, source in enumerate(result["sources"][:2]):  # Show top 2 sources
                logger.info(
                    f"  Source {j + 1}: {source['title']} (score: {source['score']:.2f})"
                )
        else:
            logger.error(f"RAG error: {response.error}")

        print()


async def demo_service_monitoring(orchestrator: AIServiceOrchestrator) -> None:
    """Demonstrate service monitoring and health checks."""
    logger.info("--- Service Monitoring Demo ---")

    # Get service status
    status = await orchestrator.get_service_status()
    logger.info("Service Status:")
    for service_name, service_status in status.items():
        logger.info(
            f"  {service_name}: {service_status['status']} (healthy: {service_status['healthy']})"
        )
        logger.info(f"    Capabilities: {service_status['capabilities']}")

    # Get capabilities
    capabilities = await orchestrator.get_capabilities()
    logger.info(f"Available capabilities: {capabilities}")

    # Get registry stats
    registry = get_capability_registry()
    stats = registry.get_registry_stats()
    logger.info("Registry Statistics:")
    for key, value in stats.items():
        logger.info(f"  {key}: {value}")

    print()


async def main() -> None:
    """Main demo function."""
    logger.info("🚀 Starting AI Services Demo")

    try:
        # Setup services
        orchestrator = await setup_demo_ai_services()

        # Wait a bit for services to initialize
        await asyncio.sleep(1)

        # Run demos
        await demo_chat_service(orchestrator)
        await demo_rag_service(orchestrator)
        await demo_service_monitoring(orchestrator)

        logger.info("✅ Demo completed successfully!")

    except Exception as e:
        logger.error(f"❌ Demo failed: {e}")
        raise
    finally:
        # Cleanup
        try:
            await orchestrator.stop()
            registry = get_capability_registry()
            await registry.stop_health_monitoring()
            logger.info("🧹 Cleanup completed")
        except Exception as e:
            logger.error(f"Cleanup error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
