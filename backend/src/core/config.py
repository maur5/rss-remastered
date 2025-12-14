"""Configuration management using Pydantic Settings.

This module provides a layered configuration system with:
- Environment variables (RSS_ prefix) - highest priority
- YAML config file (config.yaml or data/config.yaml)
- Default values - lowest priority

Story 1.5: Configure Pydantic Settings

Environment Variables:
    RSS_DATABASE_URL: SQLAlchemy async database URL
    RSS_LOG_LEVEL: Logging level (debug, info, warning, error)
    RSS_LOG_FORMAT: Output format (json, console)
    RSS_BASE_URL: Base URL for the application
    RSS_DATA_DIR: Data directory path
    RSS_AI__PROVIDER: AI provider (openai, ollama, none)
    RSS_AI__BASE_URL: AI provider base URL
    RSS_AI__MODEL: AI model name
    RSS_AI__API_KEY: AI API key
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any, Literal

import yaml
from pydantic import Field, field_validator, model_validator
from pydantic_settings import BaseSettings, PydanticBaseSettingsSource, SettingsConfigDict


class LoggingSettings(BaseSettings):
    """Nested settings for logging configuration."""

    model_config = SettingsConfigDict(
        env_prefix="RSS_LOGGING__",
        extra="ignore",
    )

    level: str = Field(default="info", description="Logging level")
    format: str = Field(default="json", description="Log output format")

    @field_validator("level")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Validate log level is a valid option.

        Args:
            v: The log level value to validate.

        Returns:
            The validated log level (lowercase).

        Raises:
            ValueError: If log level is not valid.
        """
        valid_levels = {"debug", "info", "warning", "error"}
        normalized = v.lower()
        if normalized not in valid_levels:
            raise ValueError(
                f"CONFIG_INVALID_LOG_LEVEL: Invalid log level '{v}'. "
                f"Must be one of: {', '.join(sorted(valid_levels))}"
            )
        return normalized

    @field_validator("format")
    @classmethod
    def validate_log_format(cls, v: str) -> str:
        """Validate log format is a valid option.

        Args:
            v: The log format value to validate.

        Returns:
            The validated log format (lowercase).

        Raises:
            ValueError: If log format is not valid.
        """
        valid_formats = {"json", "console"}
        normalized = v.lower()
        if normalized not in valid_formats:
            raise ValueError(
                f"CONFIG_INVALID_LOG_FORMAT: Invalid log format '{v}'. "
                f"Must be one of: {', '.join(sorted(valid_formats))}"
            )
        return normalized


class AISettings(BaseSettings):
    """Nested settings for AI provider configuration.

    Supports OpenAI-compatible APIs (OpenAI, Azure, LocalAI, LiteLLM, etc.)
    and Ollama for local models.
    """

    model_config = SettingsConfigDict(
        env_prefix="RSS_AI__",
        extra="ignore",
    )

    provider: Literal["openai", "ollama", "none"] = Field(
        default="none",
        description="AI provider: openai (OpenAI-compatible), ollama (local), or none (disabled)",
    )
    base_url: str = Field(
        default="",
        description="Base URL for AI provider API (e.g., http://localhost:11434 for Ollama)",
    )
    model: str = Field(
        default="",
        description="AI model name (e.g., gpt-4, llama3.2)",
    )
    api_key: str = Field(
        default="",
        description="API key for AI provider (OpenAI, Azure, etc.)",
    )


class YamlConfigSettingsSource(PydanticBaseSettingsSource):
    """Custom settings source that loads values from a YAML file.

    Looks for configuration in the following locations (first found wins):
    1. config.yaml (project root)
    2. data/config.yaml (data directory)
    """

    def __init__(self, settings_cls: type[BaseSettings]) -> None:
        super().__init__(settings_cls)
        self._yaml_data: dict[str, Any] = {}
        self._load_yaml()

    def _load_yaml(self) -> None:
        """Load YAML configuration from file if it exists."""
        yaml_paths = [
            Path("config.yaml"),
            Path("data/config.yaml"),
        ]

        for yaml_path in yaml_paths:
            if yaml_path.exists():
                try:
                    with open(yaml_path, encoding="utf-8") as f:
                        data = yaml.safe_load(f)
                        if data:
                            self._yaml_data = data
                            return
                except (OSError, yaml.YAMLError):
                    # Skip if file can't be read or parsed
                    continue

    def get_field_value(
        self,
        field: Any,
        field_name: str,
    ) -> tuple[Any, str, bool]:
        """Get value for a field from YAML data.

        Args:
            field: The field definition.
            field_name: The name of the field.

        Returns:
            Tuple of (value, field_name, is_complex).
        """
        # Handle nested settings
        if field_name == "logging":
            logging_data = self._yaml_data.get("logging", {})
            if logging_data:
                return logging_data, field_name, True
        elif field_name == "ai":
            ai_data = self._yaml_data.get("ai", {})
            if ai_data:
                return ai_data, field_name, True
        else:
            # Handle top-level fields
            value = self._yaml_data.get(field_name)
            if value is not None:
                return value, field_name, False

        return None, field_name, False

    def __call__(self) -> dict[str, Any]:
        """Return settings values from YAML file."""
        result: dict[str, Any] = {}

        for field_name in self.settings_cls.model_fields:
            value, _, _ = self.get_field_value(
                self.settings_cls.model_fields[field_name],
                field_name,
            )
            if value is not None:
                result[field_name] = value

        return result


class Settings(BaseSettings):
    """Application settings with layered configuration.

    Configuration priority (highest wins):
    1. Environment variables (RSS_ prefix)
    2. YAML config file (config.yaml or data/config.yaml)
    3. Default values

    Nested settings use double underscore separator for env vars:
    - RSS_AI__PROVIDER=openai
    - RSS_LOGGING__LEVEL=debug
    """

    model_config = SettingsConfigDict(
        env_prefix="RSS_",
        env_nested_delimiter="__",
        extra="ignore",
    )

    # Core settings
    database_url: str = Field(
        default="sqlite+aiosqlite:///data/rss.db",
        description="SQLAlchemy async database URL",
    )
    base_url: str = Field(
        default="",
        description="Base URL for reverse proxy support (empty for direct access)",
    )
    data_dir: Path = Field(
        default=Path("data"),
        description="Data directory for persistent storage",
    )

    # Legacy flat settings (also accessible via nested settings)
    log_level: str = Field(default="info", description="Logging level")
    log_format: str = Field(default="json", description="Log output format")

    # Nested settings
    logging: LoggingSettings = Field(default_factory=LoggingSettings)
    ai: AISettings = Field(default_factory=AISettings)

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Validate log level is a valid option."""
        valid_levels = {"debug", "info", "warning", "error"}
        normalized = v.lower()
        if normalized not in valid_levels:
            raise ValueError(
                f"CONFIG_INVALID_LOG_LEVEL: Invalid log level '{v}'. "
                f"Must be one of: {', '.join(sorted(valid_levels))}"
            )
        return normalized

    @field_validator("log_format")
    @classmethod
    def validate_log_format(cls, v: str) -> str:
        """Validate log format is a valid option."""
        valid_formats = {"json", "console"}
        normalized = v.lower()
        if normalized not in valid_formats:
            raise ValueError(
                f"CONFIG_INVALID_LOG_FORMAT: Invalid log format '{v}'. "
                f"Must be one of: {', '.join(sorted(valid_formats))}"
            )
        return normalized

    @field_validator("database_url")
    @classmethod
    def validate_database_url(cls, v: str) -> str:
        """Validate database URL is a valid SQLAlchemy async URL.

        Args:
            v: The database URL to validate.

        Returns:
            The validated database URL.

        Raises:
            ValueError: If URL is not a valid async SQLAlchemy URL.
        """
        if not v:
            raise ValueError(
                "CONFIG_INVALID_DATABASE_URL: Database URL cannot be empty"
            )

        # Check for valid async SQLAlchemy URL patterns
        valid_async_patterns = [
            "sqlite+aiosqlite://",
            "postgresql+asyncpg://",
            "mysql+aiomysql://",
        ]

        is_valid = any(v.startswith(pattern) for pattern in valid_async_patterns)
        if not is_valid:
            raise ValueError(
                f"CONFIG_INVALID_DATABASE_URL: Invalid database URL '{v}'. "
                f"Must be a valid async SQLAlchemy URL starting with one of: "
                f"{', '.join(valid_async_patterns)}"
            )

        return v

    @field_validator("data_dir")
    @classmethod
    def validate_data_dir(cls, v: Path) -> Path:
        """Validate data directory path.

        Args:
            v: The data directory path to validate.

        Returns:
            The validated data directory path.

        Raises:
            ValueError: If path is invalid.
        """
        if not v:
            raise ValueError(
                "CONFIG_INVALID_DATA_DIR: Data directory path cannot be empty"
            )
        return v

    @model_validator(mode="after")
    def sync_logging_settings(self) -> "Settings":
        """Sync flat log settings with nested logging settings.

        This ensures backward compatibility where log_level and log_format
        can be used directly or via the nested logging object.
        """
        # If nested logging values differ from defaults, they take precedence
        # Otherwise, use the flat values
        if self.logging.level != "info":
            self.log_level = self.logging.level
        else:
            # Update nested from flat
            object.__setattr__(self.logging, "level", self.log_level)

        if self.logging.format != "json":
            self.log_format = self.logging.format
        else:
            object.__setattr__(self.logging, "format", self.log_format)

        return self

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        """Customize settings sources to include YAML config.

        Priority order (highest first):
        1. Init settings (constructor arguments)
        2. Environment variables
        3. YAML config file
        4. Defaults (handled by Pydantic)

        Args:
            settings_cls: The settings class.
            init_settings: Settings from constructor.
            env_settings: Settings from environment variables.
            dotenv_settings: Settings from .env files (not used).
            file_secret_settings: Settings from secret files (not used).

        Returns:
            Tuple of settings sources in priority order.
        """
        return (
            init_settings,
            env_settings,
            YamlConfigSettingsSource(settings_cls),
        )


@lru_cache
def get_settings() -> Settings:
    """Get cached application settings instance.

    Returns:
        The singleton Settings instance.

    Example:
        >>> settings = get_settings()
        >>> print(settings.database_url)
        sqlite+aiosqlite:///data/rss.db
    """
    return Settings()


def validate_settings_on_startup() -> Settings:
    """Validate settings at application startup.

    This function should be called early in application startup to
    ensure all configuration is valid before the application starts
    accepting requests.

    Returns:
        The validated Settings instance.

    Raises:
        ValueError: If any configuration value is invalid.
    """
    try:
        settings = get_settings()
        return settings
    except ValueError as e:
        # Re-raise with clear startup context
        raise ValueError(f"Configuration validation failed at startup: {e}") from e
