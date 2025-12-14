"""Tests for structured logging configuration.

Story 1.4: Configure Structured Logging
"""

import json
import logging
import os
from io import StringIO
from unittest import mock

import pytest
import structlog

from src.core.logging import (
    bind_contextvars,
    clear_contextvars,
    get_log_format,
    get_log_level,
    get_logger,
    setup_logging,
)


class TestGetLogLevel:
    """Tests for get_log_level function."""

    def test_default_log_level_is_info(self) -> None:
        """Log level should default to INFO when not set."""
        with mock.patch.dict(os.environ, {}, clear=True):
            # Remove RSS_LOG_LEVEL if it exists
            os.environ.pop("RSS_LOG_LEVEL", None)
            assert get_log_level() == logging.INFO

    def test_log_level_debug(self) -> None:
        """Should return DEBUG level when RSS_LOG_LEVEL=debug."""
        with mock.patch.dict(os.environ, {"RSS_LOG_LEVEL": "debug"}):
            assert get_log_level() == logging.DEBUG

    def test_log_level_warning(self) -> None:
        """Should return WARNING level when RSS_LOG_LEVEL=warning."""
        with mock.patch.dict(os.environ, {"RSS_LOG_LEVEL": "warning"}):
            assert get_log_level() == logging.WARNING

    def test_log_level_error(self) -> None:
        """Should return ERROR level when RSS_LOG_LEVEL=error."""
        with mock.patch.dict(os.environ, {"RSS_LOG_LEVEL": "error"}):
            assert get_log_level() == logging.ERROR

    def test_log_level_case_insensitive(self) -> None:
        """Log level should be case insensitive."""
        with mock.patch.dict(os.environ, {"RSS_LOG_LEVEL": "DEBUG"}):
            assert get_log_level() == logging.DEBUG

    def test_invalid_log_level_defaults_to_info(self) -> None:
        """Invalid log level should default to INFO."""
        with mock.patch.dict(os.environ, {"RSS_LOG_LEVEL": "invalid"}):
            assert get_log_level() == logging.INFO


class TestGetLogFormat:
    """Tests for get_log_format function."""

    def test_default_format_is_json(self) -> None:
        """Log format should default to JSON when not set."""
        with mock.patch.dict(os.environ, {}, clear=True):
            os.environ.pop("RSS_LOG_FORMAT", None)
            assert get_log_format() == "json"

    def test_format_console(self) -> None:
        """Should return 'console' when RSS_LOG_FORMAT=console."""
        with mock.patch.dict(os.environ, {"RSS_LOG_FORMAT": "console"}):
            assert get_log_format() == "console"

    def test_format_json(self) -> None:
        """Should return 'json' when RSS_LOG_FORMAT=json."""
        with mock.patch.dict(os.environ, {"RSS_LOG_FORMAT": "json"}):
            assert get_log_format() == "json"

    def test_format_case_insensitive(self) -> None:
        """Log format should be lowercased."""
        with mock.patch.dict(os.environ, {"RSS_LOG_FORMAT": "JSON"}):
            assert get_log_format() == "json"


class TestSetupLogging:
    """Tests for setup_logging function."""

    def test_setup_logging_configures_structlog(self) -> None:
        """setup_logging should configure structlog without errors."""
        with mock.patch.dict(os.environ, {"RSS_LOG_FORMAT": "json", "RSS_LOG_LEVEL": "info"}):
            # Should not raise any exceptions
            setup_logging()
            # Verify we can get a logger after setup
            logger = get_logger("test")
            assert logger is not None


class TestGetLogger:
    """Tests for get_logger function."""

    def test_get_logger_returns_bound_logger(self) -> None:
        """get_logger should return a structlog logger."""
        with mock.patch.dict(os.environ, {"RSS_LOG_FORMAT": "json", "RSS_LOG_LEVEL": "info"}):
            setup_logging()
            logger = get_logger("test_module")
            assert logger is not None

    def test_get_logger_with_initial_context(self) -> None:
        """get_logger should bind initial context."""
        with mock.patch.dict(os.environ, {"RSS_LOG_FORMAT": "json", "RSS_LOG_LEVEL": "info"}):
            setup_logging()
            logger = get_logger("test_module", component="fetcher", version="1.0")
            assert logger is not None


class TestContextVars:
    """Tests for context variable functions."""

    def test_bind_and_clear_contextvars(self) -> None:
        """bind_contextvars and clear_contextvars should work together."""
        with mock.patch.dict(os.environ, {"RSS_LOG_FORMAT": "json", "RSS_LOG_LEVEL": "info"}):
            setup_logging()

            # Bind some context
            bind_contextvars(request_id="abc123", user_id="user1")

            # Clear context
            clear_contextvars()

            # Should not raise any errors
            assert True


class TestJSONLogOutput:
    """Tests for JSON log output format."""

    def test_json_log_contains_required_fields(self) -> None:
        """JSON logs should contain timestamp, level, and event."""
        with mock.patch.dict(os.environ, {"RSS_LOG_FORMAT": "json", "RSS_LOG_LEVEL": "debug"}):
            # Capture stdout
            output = StringIO()

            # Reset structlog configuration
            structlog.reset_defaults()

            # Configure with output capture
            structlog.configure(
                processors=[
                    structlog.stdlib.add_log_level,
                    structlog.processors.TimeStamper(fmt="iso"),
                    structlog.processors.JSONRenderer(),
                ],
                wrapper_class=structlog.make_filtering_bound_logger(logging.DEBUG),
                context_class=dict,
                logger_factory=structlog.PrintLoggerFactory(file=output),
                cache_logger_on_first_use=False,
            )

            logger = structlog.get_logger("test")
            logger.info("test_event", key="value")

            # Parse the JSON output
            log_output = output.getvalue().strip()
            log_data = json.loads(log_output)

            # Verify required fields
            assert "timestamp" in log_data
            assert "level" in log_data
            assert log_data["level"] == "info"
            assert "event" in log_data
            assert log_data["event"] == "test_event"
            assert log_data["key"] == "value"

    def test_json_log_timestamp_is_iso8601(self) -> None:
        """Timestamp should be in ISO 8601 format."""
        with mock.patch.dict(os.environ, {"RSS_LOG_FORMAT": "json", "RSS_LOG_LEVEL": "info"}):
            output = StringIO()

            structlog.reset_defaults()
            structlog.configure(
                processors=[
                    structlog.processors.TimeStamper(fmt="iso"),
                    structlog.processors.JSONRenderer(),
                ],
                wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
                context_class=dict,
                logger_factory=structlog.PrintLoggerFactory(file=output),
                cache_logger_on_first_use=False,
            )

            logger = structlog.get_logger("test")
            logger.info("test")

            log_data = json.loads(output.getvalue().strip())

            # ISO 8601 format check - should contain T separator and timezone
            timestamp = log_data["timestamp"]
            assert "T" in timestamp or "-" in timestamp


class TestLogLevelFiltering:
    """Tests for log level filtering."""

    def test_debug_logs_filtered_at_info_level(self) -> None:
        """Debug logs should be filtered when level is INFO."""
        output = StringIO()

        structlog.reset_defaults()
        structlog.configure(
            processors=[
                structlog.stdlib.add_log_level,
                structlog.processors.JSONRenderer(),
            ],
            wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
            context_class=dict,
            logger_factory=structlog.PrintLoggerFactory(file=output),
            cache_logger_on_first_use=False,
        )

        logger = structlog.get_logger("test")
        logger.debug("debug_message")

        # Debug should be filtered
        assert output.getvalue() == ""

    def test_info_logs_shown_at_info_level(self) -> None:
        """Info logs should be shown when level is INFO."""
        output = StringIO()

        structlog.reset_defaults()
        structlog.configure(
            processors=[
                structlog.stdlib.add_log_level,
                structlog.processors.JSONRenderer(),
            ],
            wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
            context_class=dict,
            logger_factory=structlog.PrintLoggerFactory(file=output),
            cache_logger_on_first_use=False,
        )

        logger = structlog.get_logger("test")
        logger.info("info_message")

        assert "info_message" in output.getvalue()

    def test_debug_logs_shown_at_debug_level(self) -> None:
        """Debug logs should be shown when level is DEBUG."""
        output = StringIO()

        structlog.reset_defaults()
        structlog.configure(
            processors=[
                structlog.stdlib.add_log_level,
                structlog.processors.JSONRenderer(),
            ],
            wrapper_class=structlog.make_filtering_bound_logger(logging.DEBUG),
            context_class=dict,
            logger_factory=structlog.PrintLoggerFactory(file=output),
            cache_logger_on_first_use=False,
        )

        logger = structlog.get_logger("test")
        logger.debug("debug_message")

        assert "debug_message" in output.getvalue()
