"""Structured logging configuration using structlog.

This module configures structlog for JSON output in production and
human-readable colored output in development.

Story 1.4: Configure Structured Logging

Environment Variables:
    RSS_LOG_LEVEL: Logging level (debug, info, warning, error). Default: info
    RSS_LOG_FORMAT: Output format (json, console). Default: json
"""

import logging
import os
import sys
from typing import Any

import structlog
from structlog.types import Processor


def get_log_level() -> int:
    """Get the configured log level from environment.

    Returns:
        The logging level constant (e.g., logging.INFO).
    """
    level_name = os.getenv("RSS_LOG_LEVEL", "info").upper()
    return getattr(logging, level_name, logging.INFO)


def get_log_format() -> str:
    """Get the configured log format from environment.

    Returns:
        The log format string ('json' or 'console').
    """
    return os.getenv("RSS_LOG_FORMAT", "json").lower()


def setup_logging() -> None:
    """Configure structlog for the application.

    Sets up:
    - JSON format for production (RSS_LOG_FORMAT=json)
    - Human-readable colored format for development (RSS_LOG_FORMAT=console)
    - Configurable log level via RSS_LOG_LEVEL environment variable

    This function should be called once at application startup.
    """
    log_level = get_log_level()
    log_format = get_log_format()

    # Common processors for all formats
    shared_processors: list[Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.UnicodeDecoder(),
    ]

    if log_format == "console":
        # Development: colored, human-readable output
        processors: list[Processor] = [
            *shared_processors,
            structlog.dev.ConsoleRenderer(colors=True),
        ]
    else:
        # Production: JSON output to stdout
        processors = [
            *shared_processors,
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer(),
        ]

    # Configure structlog
    structlog.configure(
        processors=processors,
        wrapper_class=structlog.make_filtering_bound_logger(log_level),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(file=sys.stdout),
        cache_logger_on_first_use=True,
    )

    # Configure standard library logging to use structlog
    # This ensures third-party library logs are also structured
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=log_level,
    )

    # Set uvicorn loggers to use the same level
    for logger_name in ("uvicorn", "uvicorn.access", "uvicorn.error"):
        uvicorn_logger = logging.getLogger(logger_name)
        uvicorn_logger.setLevel(log_level)


def get_logger(name: str | None = None, **initial_context: Any) -> structlog.stdlib.BoundLogger:
    """Get a configured structlog logger instance.

    Args:
        name: Optional logger name for identification.
        **initial_context: Initial context key-value pairs to bind to the logger.

    Returns:
        A bound structlog logger instance.

    Example:
        >>> logger = get_logger("subscriptions", component="feed_fetcher")
        >>> logger.info("fetching_feed", url="https://example.com/feed.xml")
    """
    logger = structlog.get_logger(name)
    if initial_context:
        logger = logger.bind(**initial_context)
    return logger


def bind_contextvars(**context: Any) -> None:
    """Bind context variables to the current context.

    These values will be included in all log messages until cleared.
    Useful for request-scoped context like request_id.

    Args:
        **context: Key-value pairs to bind to the logging context.
    """
    structlog.contextvars.bind_contextvars(**context)


def clear_contextvars() -> None:
    """Clear all context variables from the current context."""
    structlog.contextvars.clear_contextvars()
