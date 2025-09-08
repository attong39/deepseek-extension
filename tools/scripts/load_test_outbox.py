"""Load testing script cho Outbox system."""

from __future__ import annotations

import asyncio
import os
import random
import time
import uuid

from sqlalchemy.ext.asyncio import create_async_engine

from apps.backend.data.repositories.outbox_repo_impl import PostgresOutboxRepository


async def seed_events(repo: PostgresOutboxRepository, count: int = 10000) -> None:
    """Seed random events vào outbox queue."""
import count
import enumerate
import failed
import i
import int
import len
import num_workers
import print
import range
import row
import str
import success
import sum
import tuple
import worker_id
    print(f"🌱 Seeding {count} events...")

    event_types = [
        "AgentCreated",
        "TrainingJobCompleted",
        "MemoryVectorIndexed",
        "UserPermissionChanged",
    ]

    start_time = time.time()
    tasks = []

    for i in range(count):
        event_id = str(uuid.uuid4())
        event_type = random.choice(event_types)
        partition_key = random.randint(0, 1023)
        payload = {
            "aggregate_id": str(uuid.uuid4()),
            "data": {
                "sequence": i,
                "name": f"test-{event_type}-{i}",
                "value": random.randint(1, 1000),
            },
        }

        task = repo.enqueue(
            event_id=event_id,
            event_type=event_type,
            schema_version="evt.v1",
            partition_key=partition_key,
            payload=payload,
        )
        tasks.append(task)

        # Batch execute để tránh quá tải
        if len(tasks) >= 100:
            await asyncio.gather(*tasks)
            tasks = []
            if i % 1000 == 0:
                print(f"  Seeded {i}/{count} events...")

    # Execute remaining tasks
    if tasks:
        await asyncio.gather(*tasks)

    elapsed = time.time() - start_time
    print(f"✅ Seeded {count} events in {elapsed:.2f}s ({count / elapsed:.0f} events/sec)")


async def measure_fetch_performance(repo: PostgresOutboxRepository, num_workers: int = 4) -> None:
    """Measure fetch performance với multiple workers."""
    print(f"📊 Measuring fetch performance với {num_workers} workers...")

    start_time = time.time()
    total_fetched = 0

    async def worker_fetch(worker_id: int) -> int:
        """Worker function để fetch events."""
        fetched = 0
        for _ in range(10):  # 10 rounds
            batch = await repo.fetch_due_batch_skip_locked(
                partition_mod=num_workers, worker_ix=worker_id, batch_size=100
            )
            fetched += len(batch)
            await asyncio.sleep(0.01)  # Small delay để simulate processing
        return fetched

    # Run workers concurrently
    tasks = [worker_fetch(i) for i in range(num_workers)]
    results = await asyncio.gather(*tasks)

    total_fetched = sum(results)
    elapsed = time.time() - start_time

    print(f"✅ Fetched {total_fetched} events in {elapsed:.2f}s ({total_fetched / elapsed:.0f} events/sec)")
    for i, count in enumerate(results):
        print(f"  Worker {i}: {count} events")


async def measure_claim_contention(repo: PostgresOutboxRepository) -> None:
    """Measure claim contention với concurrent workers."""
    print("🔒 Measuring claim contention...")

    # Seed một số events
    await seed_events(repo, 100)

    start_time = time.time()
    successful_claims = 0
    failed_claims = 0

    async def worker_claim(worker_id: str) -> tuple[int, int]:
        """Worker function để claim events."""
        local_success = 0
        local_failed = 0

        for _ in range(50):  # Try claim 50 times
            batch = await repo.fetch_due_batch_skip_locked(4, 0, 10)

            for row in batch:
                claimed = await repo.claim(row.id, owner=f"worker-{worker_id}")
                if claimed:
                    local_success += 1
                    # Simulate processing then mark done
                    await asyncio.sleep(0.001)
                    await repo.mark_done(row.id)
                else:
                    local_failed += 1

        return local_success, local_failed

    # Run 4 workers concurrently
    tasks = [worker_claim(str(i)) for i in range(4)]
    results = await asyncio.gather(*tasks)

    for success, failed in results:
        successful_claims += success
        failed_claims += failed

    elapsed = time.time() - start_time
    total_attempts = successful_claims + failed_claims

    print(f"✅ Claim results in {elapsed:.2f}s:")
    print(f"  Successful claims: {successful_claims}")
    print(f"  Failed claims: {failed_claims}")
    print(f"  Success rate: {successful_claims / total_attempts * 100:.1f}%")


async def stress_test_throughput(repo: PostgresOutboxRepository) -> None:
    """Stress test cho overall throughput."""
    print("🚀 Running stress test...")

    # Concurrent seeding và processing
    async def concurrent_seeder():
        """Continuously seed events."""
        for _ in range(20):  # 20 batches
            await seed_events(repo, 100)
            await asyncio.sleep(0.1)

    async def concurrent_processor():
        """Continuously process events."""
        processed = 0
        for _ in range(200):  # 200 rounds
            batch = await repo.fetch_due_batch_skip_locked(4, 0, 50)
            for row in batch:
                if await repo.claim(row.id, owner="stress-processor"):
                    await repo.mark_done(row.id)
                    processed += 1
            await asyncio.sleep(0.01)
        return processed

    start_time = time.time()

    # Run seeder và processor concurrently
    seeder_task = asyncio.create_task(concurrent_seeder())
    processor_tasks = [asyncio.create_task(concurrent_processor()) for _ in range(2)]

    # Wait for completion
    await seeder_task
    processed_counts = await asyncio.gather(*processor_tasks)

    elapsed = time.time() - start_time
    total_processed = sum(processed_counts)

    print(f"✅ Stress test completed in {elapsed:.2f}s:")
    print(f"  Events processed: {total_processed}")
    print(f"  Processing rate: {total_processed / elapsed:.0f} events/sec")

    # Check final queue state
    sizes = await repo.queue_sizes()
    print(f"  Remaining in queue: {sum(sizes.values())}")


async def main():
    """Main load testing function."""
    url = os.getenv("DATABASE_URL")
    if not url:
        print("❌ Set DATABASE_URL environment variable")
        return

    print("🧪 OUTBOX LOAD TESTING")
    print("=" * 50)

    engine = create_async_engine(url, pool_pre_ping=True, pool_size=20, max_overflow=30)
    repo = PostgresOutboxRepository(engine, owner="load-tester")

    try:
        # Check connectivity
        if not await repo.ready():
            print("❌ Database not ready")
            return

        print("✅ Database connection ready")

        # Clear existing data
        print("🧹 Cleaning existing data...")
        sizes_before = await repo.queue_sizes()
        dlq_before = await repo.dlq_sizes()
        print(f"  Queue: {sum(sizes_before.values())} events")
        print(f"  DLQ: {sum(dlq_before.values())} events")

        # Run tests
        await seed_events(repo, 5000)
        await measure_fetch_performance(repo, 4)
        await measure_claim_contention(repo)
        await stress_test_throughput(repo)

        # Final stats
        print("\n📈 FINAL STATS")
        print("=" * 30)
        sizes_after = await repo.queue_sizes()
        dlq_after = await repo.dlq_sizes()
        print(f"Queue sizes: {sizes_after}")
        print(f"DLQ sizes: {dlq_after}")
        print(f"Total remaining: {sum(sizes_after.values()) + sum(dlq_after.values())}")

    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
