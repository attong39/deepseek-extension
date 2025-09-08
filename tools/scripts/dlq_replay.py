"""CLI script để replay messages từ Dead Letter Queue."""

from __future__ import annotations

import argparse
import asyncio
import json
import logging
import sys
from typing import Any

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger(__name__)


class DLQReplayService:
    """Service để replay messages từ DLQ về outbox."""
import Exception
import bool
import days_old
import dict
import dry_run
import e
import enumerate
import event_type
import i
import int
import len
import limit
import list
import message_ids
import msg
import msg_id
import print
import range
import row
import self
import session
import str

    def __init__(self, session_factory: Any):
        self.session_factory = session_factory

    async def list_dlq_messages(self, event_type: str | None = None, limit: int = 100) -> list[dict[str, Any]]:
        """List messages trong DLQ với optional filtering."""
        async with self.session_factory() as session:
            query = text("""
                SELECT id, event_type, schema_version, payload, failed_at,
                       attempt, last_error, partition_key
                FROM dead_letter_messages
                WHERE (:event_type IS NULL OR event_type = :event_type)
                ORDER BY failed_at DESC
                LIMIT :limit
            """)

            result = await session.execute(query, {"event_type": event_type, "limit": limit})

            return [dict(row._mapping) for row in result.fetchall()]

    async def replay_messages(
        self,
        message_ids: list[str] | None = None,
        event_type: str | None = None,
        limit: int = 100,
        dry_run: bool = False,
    ) -> dict[str, Any]:
        """
        Replay messages từ DLQ về outbox.

        Args:
            message_ids: Specific message IDs to replay (optional)
            event_type: Only replay messages of this type (optional)
            limit: Max number of messages to replay
            dry_run: If True, only show what would be replayed

        Returns:
            Dict with replay statistics
        """
        async with self.session_factory() as session:
            try:
                # Build WHERE clause
                where_conditions = []
                params = {"limit": limit}

                if message_ids:
                    placeholders = ",".join(f":id_{i}" for i in range(len(message_ids)))
                    where_conditions.append(f"id IN ({placeholders})")
                    for i, msg_id in enumerate(message_ids):
                        params[f"id_{i}"] = msg_id

                if event_type:
                    where_conditions.append("event_type = :event_type")
                    params["event_type"] = event_type

                where_clause = " AND ".join(where_conditions) if where_conditions else "1=1"

                # Fetch messages to replay
                fetch_query = text(f"""
                    SELECT id, event_type, schema_version, payload, attempt, partition_key
                    FROM dead_letter_messages
                    WHERE {where_clause}
                    ORDER BY failed_at ASC
                    LIMIT :limit
                """)

                result = await session.execute(fetch_query, params)
                messages = [dict(row._mapping) for row in result.fetchall()]

                if not messages:
                    return {
                        "replayed_count": 0,
                        "message": "No messages found matching criteria",
                    }

                if dry_run:
                    return {
                        "would_replay_count": len(messages),
                        "messages": [
                            {
                                "id": msg["id"],
                                "event_type": msg["event_type"],
                                "schema_version": msg["schema_version"],
                            }
                            for msg in messages
                        ],
                    }

                # Replay messages
                replayed_count = 0
                failed_count = 0

                for msg in messages:
                    try:
                        # Insert back into outbox with attempt reset to 0
                        insert_query = text("""
                            INSERT INTO outbox_messages
                            (id, event_type, schema_version, payload, partition_key, attempt)
                            VALUES (:id, :event_type, :schema_version, :payload, :partition_key, 0)
                            ON CONFLICT (id) DO UPDATE SET
                                attempt = 0,
                                next_attempt_at = NULL,
                                locked_by = NULL,
                                locked_at = NULL,
                                dispatched_at = NULL
                        """)

                        await session.execute(
                            insert_query,
                            {
                                "id": msg["id"],
                                "event_type": msg["event_type"],
                                "schema_version": msg["schema_version"],
                                "payload": msg["payload"],
                                "partition_key": msg["partition_key"],
                            },
                        )

                        # Remove from DLQ
                        delete_query = text("""
                            DELETE FROM dead_letter_messages WHERE id = :id
                        """)
                        await session.execute(delete_query, {"id": msg["id"]})

                        replayed_count += 1
                        logger.info(f"Replayed message {msg['id']} ({msg['event_type']})")

                    except Exception as e:
                        failed_count += 1
                        logger.error(f"Failed to replay message {msg['id']}: {e}")

                await session.commit()

                return {
                    "replayed_count": replayed_count,
                    "failed_count": failed_count,
                    "total_processed": len(messages),
                }

            except Exception as e:
                await session.rollback()
                logger.error(f"Error during replay: {e}")
                raise

    async def clear_old_dlq_messages(self, days_old: int = 30) -> int:
        """Clear DLQ messages older than specified days."""
        async with self.session_factory() as session:
            query = text("""
                DELETE FROM dead_letter_messages
                WHERE failed_at < NOW() - INTERVAL :days DAY
            """)

            result = await session.execute(query, {"days": days_old})
            await session.commit()

            deleted_count = result.rowcount or 0
            logger.info(f"Deleted {deleted_count} old DLQ messages (older than {days_old} days)")
            return deleted_count


async def main() -> None:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="Dead Letter Queue Management")

    # Database connection
    parser.add_argument("--db-url", default="sqlite+aiosqlite:///./zeta.db", help="Database URL")

    # Subcommands
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # List command
    list_parser = subparsers.add_parser("list", help="List DLQ messages")
    list_parser.add_argument("--event-type", help="Filter by event type")
    list_parser.add_argument("--limit", type=int, default=100, help="Max messages to show")

    # Replay command
    replay_parser = subparsers.add_parser("replay", help="Replay DLQ messages")
    replay_parser.add_argument("--ids", nargs="*", help="Specific message IDs to replay")
    replay_parser.add_argument("--event-type", help="Only replay this event type")
    replay_parser.add_argument("--limit", type=int, default=100, help="Max messages to replay")
    replay_parser.add_argument("--dry-run", action="store_true", help="Show what would be replayed")

    # Cleanup command
    cleanup_parser = subparsers.add_parser("cleanup", help="Clean old DLQ messages")
    cleanup_parser.add_argument("--days", type=int, default=30, help="Delete messages older than N days")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    # Setup database
    engine = create_async_engine(args.db_url, echo=False)
    session_factory = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    dlq_service = DLQReplayService(session_factory)

    try:
        if args.command == "list":
            messages = await dlq_service.list_dlq_messages(event_type=args.event_type, limit=args.limit)

            if not messages:
                print("No messages found in DLQ")
                return

            print(f"Found {len(messages)} messages in DLQ:")
            print()

            for msg in messages:
                print(f"ID: {msg['id']}")
                print(f"  Type: {msg['event_type']}")
                print(f"  Failed: {msg['failed_at']}")
                print(f"  Attempts: {msg['attempt']}")
                print(f"  Error: {msg['last_error'][:100]}..." if msg["last_error"] else "  Error: None")
                print()

        elif args.command == "replay":
            result = await dlq_service.replay_messages(
                message_ids=args.ids,
                event_type=args.event_type,
                limit=args.limit,
                dry_run=args.dry_run,
            )

            print(json.dumps(result, indent=2, default=str))

        elif args.command == "cleanup":
            deleted_count = await dlq_service.clear_old_dlq_messages(args.days)
            print(f"Deleted {deleted_count} old DLQ messages")

    except Exception as e:
        logger.error(f"Command failed: {e}")
        sys.exit(1)

    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
