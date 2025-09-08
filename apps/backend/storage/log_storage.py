"""Log storage system for ZETA AI Server.





This module provides comprehensive log management including:


- Structured log storage with rotation


- Log aggregation and search


- Performance metrics logging


- Error tracking and alerting


- Log archival and cleanup


"""

import gzip
import json
import logging
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any
import Exception
import ValueError
import backup_count
import bool
import classmethod
import cls
import compress_rotated
import dict
import e
import end_time
import extra_data
import f
import f_in
import f_out
import function
import hours
import i
import int
import json_format
import kwargs
import len
import level
import limit
import line_number
import list
import log_type
import log_type_dir
import logger_name
import max_file_size
import message
import message_pattern
import module
import open
import query
import range
import request_id
import retention_days
import reverse
import self
import str
import user_id
import x

logger = logging.getLogger(__name__)


class LogLevel:
    """Log level constants."""

    DEBUG = "DEBUG"

    INFO = "INFO"

    WARNING = "WARNING"

    ERROR = "ERROR"

    CRITICAL = "CRITICAL"


class LogConfig:
    """Configuration for log storage."""

    def __init__(
        self,
        log_dir: str | Path,
        max_file_size: int = 10 * 1024 * 1024,  # 10MB
        backup_count: int = 5,
        retention_days: int = 30,
        compress_rotated: bool = True,
        json_format: bool = True,
    ):
        """Initialize log configuration.





        Args:


            log_dir: Directory for log storage


            max_file_size: Maximum log file size before rotation


            backup_count: Number of backup files to keep


            retention_days: Days to keep logs


            compress_rotated: Whether to compress rotated logs


            json_format: Whether to use JSON log format


        """

        self.log_dir = Path(log_dir)

        self.log_dir.mkdir(parents=True, exist_ok=True)

        self.max_file_size = max_file_size

        self.backup_count = backup_count

        self.retention_days = retention_days

        self.compress_rotated = compress_rotated

        self.json_format = json_format

        # Create log subdirectories

        (self.log_dir / "application").mkdir(exist_ok=True)

        (self.log_dir / "access").mkdir(exist_ok=True)

        (self.log_dir / "error").mkdir(exist_ok=True)

        (self.log_dir / "performance").mkdir(exist_ok=True)

        (self.log_dir / "audit").mkdir(exist_ok=True)


class LogEntry:
    """Structured log entry."""

    def __init__(
        self,
        timestamp: datetime,
        level: str,
        logger_name: str,
        message: str,
        module: str | None = None,
        function: str | None = None,
        line_number: int | None = None,
        extra_data: dict[str, Any] | None = None,
        request_id: str | None = None,
        user_id: str | None = None,
    ):
        """Initialize log entry.





        Args:


            timestamp: When the log was created


            level: Log level (DEBUG, INFO, etc.)


            logger_name: Name of the logger


            message: Log message


            module: Module name where log was created


            function: Function name where log was created


            line_number: Line number where log was created


            extra_data: Additional data for the log


            request_id: Request ID for tracing


            user_id: User ID for audit trail


        """

        self.timestamp = timestamp

        self.level = level

        self.logger_name = logger_name

        self.message = message

        self.module = module

        self.function = function

        self.line_number = line_number

        self.extra_data = extra_data or {}

        self.request_id = request_id

        self.user_id = user_id

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON serialization."""

        entry: dict[str, Any] = {
            "timestamp": self.timestamp.isoformat(),
            "level": self.level,
            "logger": self.logger_name,
            "message": self.message,
        }

        if self.module:
            entry["module"] = self.module

        if self.function:
            entry["function"] = self.function

        if self.line_number:
            entry["line_number"] = self.line_number

        if self.request_id:
            entry["request_id"] = self.request_id

        if self.user_id:
            entry["user_id"] = self.user_id

        if self.extra_data:
            entry["extra"] = self.extra_data

        return entry

    def to_text(self) -> str:
        """Convert to text format."""

        timestamp_str = self.timestamp.strftime("%Y-%m-%d %H:%M:%S")

        base_msg = f"{timestamp_str} [{self.level}] {self.logger_name}: {self.message}"

        if self.request_id:
            base_msg += f" [req_id={self.request_id}]"

        if self.user_id:
            base_msg += f" [user_id={self.user_id}]"

        return base_msg

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "LogEntry":
        """Create from dictionary."""

        return cls(
            timestamp=datetime.fromisoformat(data["timestamp"]),
            level=data["level"],
            logger_name=data["logger"],
            message=data["message"],
            module=data.get("module"),
            function=data.get("function"),
            line_number=data.get("line_number"),
            extra_data=data.get("extra", {}),
            request_id=data.get("request_id"),
            user_id=data.get("user_id"),
        )


class LogFilter:
    """Filter for log queries."""

    def __init__(
        self,
        level: str | None = None,
        logger_name: str | None = None,
        message_pattern: str | None = None,
        start_time: datetime | None = None,
        end_time: datetime | None = None,
        request_id: str | None = None,
        user_id: str | None = None,
        module: str | None = None,
    ):
        """Initialize log filter.





        Args:


            level: Filter by log level


            logger_name: Filter by logger name


            message_pattern: Regex pattern for message filtering


            start_time: Start time for filtering


            end_time: End time for filtering


            request_id: Filter by request ID


            user_id: Filter by user ID


            module: Filter by module name


        """

        self.level = level

        self.logger_name = logger_name

        self.message_pattern = message_pattern

        self.start_time = start_time

        self.end_time = end_time

        self.request_id = request_id

        self.user_id = user_id

        self.module = module

        # Compile regex pattern if provided

        self._compiled_pattern = None

        if message_pattern:
            try:
                self._compiled_pattern = re.compile(message_pattern, re.IGNORECASE)

            except re.error as e:
                logger.warning(f"Invalid regex pattern '{message_pattern}': {e}")

    def matches(self, entry: LogEntry) -> bool:
        """Check if log entry matches filter criteria."""

        # Level filter

        if self.level and entry.level != self.level:
            return False

        # Logger name filter

        if self.logger_name and self.logger_name not in entry.logger_name:
            return False

        # Message pattern filter

        if self._compiled_pattern and not self._compiled_pattern.search(entry.message):
            return False

        # Time range filter

        if self.start_time and entry.timestamp < self.start_time:
            return False

        if self.end_time and entry.timestamp > self.end_time:
            return False

        # Request ID filter

        if self.request_id and entry.request_id != self.request_id:
            return False

        # User ID filter

        if self.user_id and entry.user_id != self.user_id:
            return False

        # Module filter

        if self.module and entry.module != self.module:
            return False

        return True


class LogStorage:
    """Comprehensive log storage manager."""

    def __init__(self, config: LogConfig):
        """Initialize log storage.





        Args:


            config: Log storage configuration


        """

        self.config = config

    def _get_log_file_path(self, log_type: str) -> Path:
        """Get current log file path for type."""

        return self.config.log_dir / log_type / f"{log_type}.log"

    def _rotate_log_file(self, log_file: Path) -> None:
        """Rotate log file when it gets too large."""

        if not log_file.exists():
            return

        # Check if rotation is needed

        if log_file.stat().st_size < self.config.max_file_size:
            return

        # Remove oldest backup if at limit

        oldest_backup = log_file.with_suffix(f".log.{self.config.backup_count}")

        if self.config.compress_rotated:
            oldest_backup = oldest_backup.with_suffix(".gz")

        if oldest_backup.exists():
            oldest_backup.unlink()

        # Shift existing backups

        for i in range(self.config.backup_count - 1, 0, -1):
            current_backup = log_file.with_suffix(f".log.{i}")

            next_backup = log_file.with_suffix(f".log.{i + 1}")

            if self.config.compress_rotated:
                current_backup = current_backup.with_suffix(".gz")

                next_backup = next_backup.with_suffix(".gz")

            if current_backup.exists():
                current_backup.rename(next_backup)

        # Move current log to backup

        backup_file = log_file.with_suffix(".log.1")

        if self.config.compress_rotated:
            # Compress the backup

            with open(log_file, "rb") as f_in:
                with gzip.open(backup_file.with_suffix(".gz"), "wb") as f_out:
                    f_out.writelines(f_in)

            log_file.unlink()

        else:
            log_file.rename(backup_file)

    def write_log(self, entry: LogEntry, log_type: str = "application") -> bool:
        """Write a log entry.





        Args:


            entry: Log entry to write


            log_type: Type of log (application, access, error, etc.)





        Returns:


            True if successful, False otherwise


        """

        try:
            log_file = self._get_log_file_path(log_type)

            # Rotate if necessary

            self._rotate_log_file(log_file)

            # Format log entry

            if self.config.json_format:
                log_line = json.dumps(entry.to_dict(), ensure_ascii=False)

            else:
                log_line = entry.to_text()

            # Write to file

            with open(log_file, "a", encoding="utf-8") as f:
                f.write(f"{log_line}\n")

            return True

        except Exception as e:
            logger.error(f"Failed to write log entry: {e}")

            return False

    def read_logs(
        self,
        log_type: str = "application",
        log_filter: LogFilter | None = None,
        limit: int | None = None,
        reverse: bool = True,
    ) -> list[LogEntry]:
        """Read log entries with filtering.





        Args:


            log_type: Type of log to read


            log_filter: Filter criteria


            limit: Maximum number of entries to return


            reverse: Whether to return newest entries first





        Returns:


            List of matching log entries


        """

        entries = []

        try:
            log_files = self._get_log_files_for_type(log_type)

            for log_file in log_files:
                file_entries = self._read_log_file(log_file)

                # Apply filter

                if log_filter:
                    file_entries = [e for e in file_entries if log_filter.matches(e)]

                entries.extend(file_entries)

                # Early exit if limit reached

                if limit and len(entries) >= limit:
                    break

            # Sort entries

            entries.sort(key=lambda x: x.timestamp, reverse=reverse)

            # Apply limit

            if limit:
                entries = entries[:limit]

            return entries

        except Exception as e:
            logger.error(f"Failed to read logs: {e}")

            return []

    def _get_log_files_for_type(self, log_type: str) -> list[Path]:
        """Get all log files for a type, sorted by modification time."""

        log_dir = self.config.log_dir / log_type

        if not log_dir.exists():
            return []

        log_files = []

        # Add current log file

        current_log = log_dir / f"{log_type}.log"

        if current_log.exists():
            log_files.append(current_log)

        # Add backup log files

        for i in range(1, self.config.backup_count + 1):
            backup_file = log_dir / f"{log_type}.log.{i}"

            if backup_file.exists():
                log_files.append(backup_file)

            # Check compressed version

            compressed_backup = backup_file.with_suffix(".gz")

            if compressed_backup.exists():
                log_files.append(compressed_backup)

        # Sort by modification time (newest first)

        log_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)

        return log_files

    def _read_log_file(self, log_file: Path) -> list[LogEntry]:
        """Read entries from a single log file."""

        entries = []

        try:
            # Handle compressed files

            if log_file.suffix == ".gz":
                open_func = gzip.open

                mode = "rt"

            else:
                open_func = open

                mode = "r"

            with open_func(log_file, mode, encoding="utf-8") as f:
                for line in f:
                    line = line.strip()

                    if not line:
                        continue

                    try:
                        if self.config.json_format:
                            # Parse JSON log entry

                            data = json.loads(line)

                            entry = LogEntry.from_dict(data)

                        else:
                            # Parse text log entry (simplified)

                            entry = self._parse_text_log_line(line)

                        if entry:
                            entries.append(entry)

                    except json.JSONDecodeError as e:
                        logger.warning(
                            f"Failed to parse log line: {line[:100]}... Error: {e}"
                        )

                        continue

        except Exception as e:
            logger.error(f"Failed to read log file {log_file}: {e}")

        return entries

    def _parse_text_log_line(self, line: str) -> LogEntry | None:
        """Parse a text format log line."""

        # Simple regex for text log format

        # Format: "YYYY-MM-DD HH:MM:SS [LEVEL] logger_name: message"

        pattern = r"^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) \[(\w+)\] ([^:]+): (.+)$"

        match = re.match(pattern, line)

        if not match:
            return None

        timestamp_str, level, logger_name, message = match.groups()

        try:
            timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")

            return LogEntry(
                timestamp=timestamp,
                level=level,
                logger_name=logger_name,
                message=message,
            )

        except ValueError:
            return None

    def search_logs(
        self, query: str, log_type: str = "application", limit: int = 100
    ) -> list[LogEntry]:
        """Search logs using text query.





        Args:


            query: Search query


            log_type: Type of log to search


            limit: Maximum results





        Returns:


            List of matching log entries


        """

        log_filter = LogFilter(message_pattern=query)

        return self.read_logs(log_type=log_type, log_filter=log_filter, limit=limit)

    def get_error_logs(self, hours: int = 24, limit: int = 100) -> list[LogEntry]:
        """Get recent error logs.





        Args:


            hours: Number of hours to look back


            limit: Maximum results





        Returns:


            List of error log entries


        """

        start_time = datetime.now() - timedelta(hours=hours)

        log_filter = LogFilter(level=LogLevel.ERROR, start_time=start_time)

        return self.read_logs(log_type="error", log_filter=log_filter, limit=limit)

    def cleanup_old_logs(self) -> int:
        """Remove logs older than retention period.





        Returns:


            Number of files removed


        """

        cutoff_date = datetime.now() - timedelta(days=self.config.retention_days)

        removed_count = 0

        for log_type_dir in self.config.log_dir.iterdir():
            if not log_type_dir.is_dir():
                continue

            for log_file in log_type_dir.iterdir():
                if not log_file.is_file():
                    continue

                # Check modification time

                mod_time = datetime.fromtimestamp(log_file.stat().st_mtime)

                if mod_time < cutoff_date:
                    try:
                        log_file.unlink()

                        removed_count += 1

                        logger.info(f"Removed old log file: {log_file}")

                    except Exception as e:
                        logger.error(f"Failed to remove log file {log_file}: {e}")

        return removed_count

    def get_log_stats(self) -> dict[str, Any]:
        """Get log storage statistics.





        Returns:


            Dictionary with log statistics


        """

        stats = {
            "log_directory": str(self.config.log_dir),
            "total_size": 0,
            "by_type": {},
        }

        for log_type_dir in self.config.log_dir.iterdir():
            if not log_type_dir.is_dir():
                continue

            type_stats = {"file_count": 0, "total_size": 0, "files": []}

            for log_file in log_type_dir.iterdir():
                if log_file.is_file():
                    file_size = log_file.stat().st_size

                    type_stats["file_count"] += 1

                    type_stats["total_size"] += file_size

                    type_stats["files"].append(
                        {
                            "name": log_file.name,
                            "size": file_size,
                            "modified": datetime.fromtimestamp(
                                log_file.stat().st_mtime
                            ).isoformat(),
                        }
                    )

            stats["by_type"][log_type_dir.name] = type_stats

            stats["total_size"] += type_stats["total_size"]

        return stats


# Convenience functions for quick log operations


def create_log_storage(log_dir: str | Path) -> LogStorage:
    """Create log storage with default configuration.





    Args:


        log_dir: Directory for logs





    Returns:


        LogStorage instance


    """

    config = LogConfig(log_dir)

    return LogStorage(config)


def quick_log_entry(
    message: str, level: str = LogLevel.INFO, logger_name: str = "application", **kwargs
) -> LogEntry:
    """Create a log entry quickly.





    Args:


        message: Log message


        level: Log level


        logger_name: Logger name


        **kwargs: Additional log entry parameters





    Returns:


        LogEntry instance


    """

    return LogEntry(
        timestamp=datetime.now(),
        level=level,
        logger_name=logger_name,
        message=message,
        **kwargs,
    )
