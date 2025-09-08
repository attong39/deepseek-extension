"""
Demo Implementation của Core Primitives theo ROADMAP.

Tạo simple demo để test One-Click Learning pipeline.
"""

from __future__ import annotations

import asyncio
import logging
from typing import Any

from apps.backend.core.adapters.vector.chunking_service import ChunkingService
from apps.backend.core.adapters.vector.memory_vector_store import MemoryVectorStoreAdapter
from apps.backend.core.adapters.vector.openai_embeddings import OpenAIEmbeddingAdapter
from apps.backend.core.application.event_bus import InMemoryEventBus
from apps.backend.core.services.rag_service import EnhancedRAGService, QueryRequest, Source
import Exception
import dict
import e
import event
import len
import print
import query
import self
import str

logger = logging.getLogger(__name__)


class OneClickLearningDemo:
    """Demo One-Click Learning pipeline theo ROADMAP."""

    def __init__(self) -> None:
        """Initialize all core components."""
        self.event_bus = InMemoryEventBus()
        self.chunking_service = ChunkingService()
        self.embedding_adapter = OpenAIEmbeddingAdapter()
        self.vector_store = MemoryVectorStoreAdapter()
        self.rag_service = EnhancedRAGService(
            chunking_service=self.chunking_service,
            embedding_adapter=self.embedding_adapter,
            vector_store=self.vector_store,
        )

    async def run_demo(self) -> dict[str, Any]:
        """Run complete One-Click Learning demo."""
        logger.info("🚀 Starting One-Click Learning Demo")

        # Sample documents
        sources = [
            Source(
                content="Python is a high-level programming language known for its simplicity and readability.",
                metadata={"topic": "programming", "language": "python"},
            ),
            Source(
                content="Machine learning is a subset of artificial intelligence that enables computers to learn without being explicitly programmed.",
                metadata={"topic": "ai", "category": "ml"},
            ),
            Source(
                content="Vector databases store high-dimensional vectors and enable similarity search for AI applications.",
                metadata={"topic": "database", "category": "vector"},
            ),
        ]

        # Progress tracking
        progress_events = []

        def track_progress(event):
            progress_events.append(event)
            logger.info(f"📊 Progress: {event.status} - {event.percentage:.1f}% - {event.message}")

        try:
            # Step 1: Ingest documents
            logger.info("📚 Step 1: Ingesting documents...")
            ingest_report = await self.rag_service.ingest(
                sources=sources, profile="optimized", progress_callback=track_progress
            )

            if not ingest_report.success:
                return {"error": "Ingestion failed", "details": ingest_report.errors}

            logger.info(f"✅ Ingested {ingest_report.chunks_created} chunks in {ingest_report.duration_seconds:.2f}s")

            # Step 2: Query the system
            logger.info("🔍 Step 2: Querying RAG system...")

            queries = [
                "What is Python?",
                "How does machine learning work?",
                "Tell me about vector databases",
            ]

            query_results = []
            for query in queries:
                request = QueryRequest(text=query, k=3, rerank=True)

                response = await self.rag_service.query(request)
                query_results.append(
                    {
                        "query": query,
                        "results_count": len(response.results),
                        "context_used": response.context_used,
                        "processing_time_ms": response.processing_time_ms,
                    }
                )

                logger.info(
                    f"📝 Query: '{query}' -> {len(response.results)} results in {response.processing_time_ms:.1f}ms"
                )

            # Step 3: Health check
            logger.info("🏥 Step 3: Health check...")
            health = self.rag_service.health_check()

            # Step 4: Vector store stats
            vector_stats = self.rag_service.vector_store.get_stats()

            # Demo results
            demo_results = {
                "status": "success",
                "ingestion": {
                    "sources_processed": ingest_report.sources_processed,
                    "chunks_created": ingest_report.chunks_created,
                    "embeddings_created": ingest_report.embeddings_created,
                    "duration_seconds": ingest_report.duration_seconds,
                },
                "queries": query_results,
                "health": health,
                "vector_store_stats": vector_stats,
                "progress_events": len(progress_events),
                "components_tested": [
                    "ChunkingService",
                    "OpenAIEmbeddingAdapter",
                    "MemoryVectorStoreAdapter",
                    "EnhancedRAGService",
                    "InMemoryEventBus",
                ],
            }

            logger.info("🎉 One-Click Learning Demo completed successfully!")
            return demo_results

        except Exception as e:
            logger.error(f"❌ Demo failed: {e}")
            return {"error": str(e), "status": "failed"}


async def main() -> None:
    """Run the demo."""
    logging.basicConfig(level=logging.INFO)

    demo = OneClickLearningDemo()
    results = await demo.run_demo()

    print("\n" + "=" * 50)
    print("ONE-CLICK LEARNING DEMO RESULTS")
    print("=" * 50)

    if results.get("status") == "success":
        print(f"✅ Status: {results['status']}")
        print(f"📚 Ingested {results['ingestion']['chunks_created']} chunks")
        print(f"🔍 Processed {len(results['queries'])} queries")
        print(f"🏥 Health: {results['health']['overall_status']}")
        print(f"⚡ Components: {', '.join(results['components_tested'])}")
    else:
        print(f"❌ Status: {results.get('status', 'unknown')}")
        print(f"Error: {results.get('error', 'No error details')}")


if __name__ == "__main__":
    asyncio.run(main())
