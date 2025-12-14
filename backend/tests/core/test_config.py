"""Tests for the configuration system.

Story 1.5: Configure Pydantic Settings

Test scenarios:
1. Default values when no env/yaml present
2. Environment variable override precedence
3. YAML file loading when present
4. Nested settings with __ separator
5. Validation errors for invalid values
6. Missing optional fields don't error
7. Integration with database.py and logging.py
"""

import os
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest
import yaml

from src.core.config import (
    AISettings,
    LoggingSettings,
    Settings,
    YamlConfigSettingsSource,
    get_settings,
    validate_settings_on_startup,
)


class TestDefaultValues:
    """Test that default values are correctly set when no configuration is provided."""

    def test_default_database_url(self) -> None:
        """Test default database URL is SQLite in data directory."""
        settings = Settings()
        assert settings.database_url == "sqlite+aiosqlite:///data/rss.db"

    def test_default_log_level(self) -> None:
        """Test default log level is info."""
        settings = Settings()
        assert settings.log_level == "info"

    def test_default_log_format(self) -> None:
        """Test default log format is json."""
        settings = Settings()
        assert settings.log_format == "json"

    def test_default_base_url(self) -> None:
        """Test default base URL is empty string."""
        settings = Settings()
        assert settings.base_url == ""

    def test_default_data_dir(self) -> None:
        """Test default data directory is 'data'."""
        settings = Settings()
        assert settings.data_dir == Path("data")

    def test_default_ai_provider(self) -> None:
        """Test default AI provider is none (disabled)."""
        settings = Settings()
        assert settings.ai.provider == "none"

    def test_default_ai_settings_empty(self) -> None:
        """Test default AI settings have empty values."""
        settings = Settings()
        assert settings.ai.base_url == ""
        assert settings.ai.model == ""
        assert settings.ai.api_key == ""


class TestEnvironmentVariableOverrides:
    """Test that environment variables correctly override defaults."""

    def test_env_override_database_url(self) -> None:
        """Test RSS_DATABASE_URL env var overrides default."""
        with patch.dict(
            os.environ,
            {"RSS_DATABASE_URL": "sqlite+aiosqlite:///custom/path.db"},
            clear=False,
        ):
            settings = Settings()
            assert settings.database_url == "sqlite+aiosqlite:///custom/path.db"

    def test_env_override_log_level(self) -> None:
        """Test RSS_LOG_LEVEL env var overrides default."""
        with patch.dict(os.environ, {"RSS_LOG_LEVEL": "debug"}, clear=False):
            settings = Settings()
            assert settings.log_level == "debug"

    def test_env_override_log_format(self) -> None:
        """Test RSS_LOG_FORMAT env var overrides default."""
        with patch.dict(os.environ, {"RSS_LOG_FORMAT": "console"}, clear=False):
            settings = Settings()
            assert settings.log_format == "console"

    def test_env_override_base_url(self) -> None:
        """Test RSS_BASE_URL env var overrides default."""
        with patch.dict(
            os.environ, {"RSS_BASE_URL": "https://rss.example.com"}, clear=False
        ):
            settings = Settings()
            assert settings.base_url == "https://rss.example.com"

    def test_env_override_data_dir(self) -> None:
        """Test RSS_DATA_DIR env var overrides default."""
        with patch.dict(os.environ, {"RSS_DATA_DIR": "/custom/data"}, clear=False):
            settings = Settings()
            assert settings.data_dir == Path("/custom/data")


class TestNestedSettingsEnvVars:
    """Test nested settings with double underscore env var separator."""

    def test_nested_ai_provider_env(self) -> None:
        """Test RSS_AI__PROVIDER env var sets nested AI provider."""
        with patch.dict(os.environ, {"RSS_AI__PROVIDER": "openai"}, clear=False):
            settings = Settings()
            assert settings.ai.provider == "openai"

    def test_nested_ai_base_url_env(self) -> None:
        """Test RSS_AI__BASE_URL env var sets nested AI base URL."""
        with patch.dict(
            os.environ, {"RSS_AI__BASE_URL": "http://localhost:11434"}, clear=False
        ):
            settings = Settings()
            assert settings.ai.base_url == "http://localhost:11434"

    def test_nested_ai_model_env(self) -> None:
        """Test RSS_AI__MODEL env var sets nested AI model."""
        with patch.dict(os.environ, {"RSS_AI__MODEL": "llama3.2"}, clear=False):
            settings = Settings()
            assert settings.ai.model == "llama3.2"

    def test_nested_ai_api_key_env(self) -> None:
        """Test RSS_AI__API_KEY env var sets nested AI API key."""
        with patch.dict(os.environ, {"RSS_AI__API_KEY": "sk-test123"}, clear=False):
            settings = Settings()
            assert settings.ai.api_key == "sk-test123"

    def test_multiple_nested_env_vars(self) -> None:
        """Test multiple nested env vars are applied together."""
        env_vars = {
            "RSS_AI__PROVIDER": "ollama",
            "RSS_AI__BASE_URL": "http://localhost:11434",
            "RSS_AI__MODEL": "mistral",
        }
        with patch.dict(os.environ, env_vars, clear=False):
            settings = Settings()
            assert settings.ai.provider == "ollama"
            assert settings.ai.base_url == "http://localhost:11434"
            assert settings.ai.model == "mistral"


class TestYamlConfigLoading:
    """Test YAML configuration file loading."""

    def test_yaml_loading_from_config_yaml(self, tmp_path: Path) -> None:
        """Test loading configuration from config.yaml."""
        config_yaml = tmp_path / "config.yaml"
        config_yaml.write_text(
            yaml.dump(
                {
                    "log_level": "warning",
                    "log_format": "console",
                    "ai": {
                        "provider": "ollama",
                        "base_url": "http://localhost:11434",
                    },
                }
            )
        )

        # Change to temp directory where config.yaml exists
        original_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            settings = Settings()
            assert settings.log_level == "warning"
            assert settings.log_format == "console"
            assert settings.ai.provider == "ollama"
        finally:
            os.chdir(original_cwd)

    def test_yaml_loading_from_data_config_yaml(self, tmp_path: Path) -> None:
        """Test loading configuration from data/config.yaml."""
        data_dir = tmp_path / "data"
        data_dir.mkdir()
        config_yaml = data_dir / "config.yaml"
        config_yaml.write_text(
            yaml.dump(
                {
                    "log_level": "error",
                    "ai": {
                        "provider": "openai",
                    },
                }
            )
        )

        original_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            settings = Settings()
            assert settings.log_level == "error"
            assert settings.ai.provider == "openai"
        finally:
            os.chdir(original_cwd)

    def test_env_overrides_yaml(self, tmp_path: Path) -> None:
        """Test environment variables take precedence over YAML."""
        config_yaml = tmp_path / "config.yaml"
        config_yaml.write_text(
            yaml.dump(
                {
                    "log_level": "warning",
                }
            )
        )

        original_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            with patch.dict(os.environ, {"RSS_LOG_LEVEL": "debug"}, clear=False):
                settings = Settings()
                # Env var should override YAML
                assert settings.log_level == "debug"
        finally:
            os.chdir(original_cwd)


class TestValidationErrors:
    """Test validation error messages for invalid configuration."""

    def test_invalid_log_level_error(self) -> None:
        """Test invalid log level raises clear validation error."""
        with pytest.raises(ValueError) as exc_info:
            Settings(log_level="invalid")
        assert "CONFIG_INVALID_LOG_LEVEL" in str(exc_info.value)
        assert "debug, error, info, warning" in str(exc_info.value)

    def test_invalid_log_format_error(self) -> None:
        """Test invalid log format raises clear validation error."""
        with pytest.raises(ValueError) as exc_info:
            Settings(log_format="xml")
        assert "CONFIG_INVALID_LOG_FORMAT" in str(exc_info.value)
        assert "console, json" in str(exc_info.value)

    def test_invalid_database_url_error(self) -> None:
        """Test invalid database URL raises clear validation error."""
        with pytest.raises(ValueError) as exc_info:
            Settings(database_url="mysql://localhost/db")
        assert "CONFIG_INVALID_DATABASE_URL" in str(exc_info.value)
        assert "sqlite+aiosqlite://" in str(exc_info.value)

    def test_empty_database_url_error(self) -> None:
        """Test empty database URL raises validation error."""
        with pytest.raises(ValueError) as exc_info:
            Settings(database_url="")
        assert "CONFIG_INVALID_DATABASE_URL" in str(exc_info.value)
        assert "cannot be empty" in str(exc_info.value)

    def test_valid_postgresql_url(self) -> None:
        """Test valid PostgreSQL async URL is accepted."""
        settings = Settings(database_url="postgresql+asyncpg://localhost/mydb")
        assert settings.database_url == "postgresql+asyncpg://localhost/mydb"

    def test_valid_mysql_url(self) -> None:
        """Test valid MySQL async URL is accepted."""
        settings = Settings(database_url="mysql+aiomysql://localhost/mydb")
        assert settings.database_url == "mysql+aiomysql://localhost/mydb"


class TestLoggingSettingsNested:
    """Test nested LoggingSettings model."""

    def test_logging_settings_defaults(self) -> None:
        """Test LoggingSettings has correct defaults."""
        logging_settings = LoggingSettings()
        assert logging_settings.level == "info"
        assert logging_settings.format == "json"

    def test_logging_settings_validation(self) -> None:
        """Test LoggingSettings validates level and format."""
        with pytest.raises(ValueError) as exc_info:
            LoggingSettings(level="verbose")
        assert "CONFIG_INVALID_LOG_LEVEL" in str(exc_info.value)

    def test_logging_settings_case_insensitive(self) -> None:
        """Test log level is case insensitive."""
        logging_settings = LoggingSettings(level="DEBUG", format="CONSOLE")
        assert logging_settings.level == "debug"
        assert logging_settings.format == "console"


class TestAISettings:
    """Test nested AISettings model."""

    def test_ai_settings_defaults(self) -> None:
        """Test AISettings has correct defaults."""
        ai_settings = AISettings()
        assert ai_settings.provider == "none"
        assert ai_settings.base_url == ""
        assert ai_settings.model == ""
        assert ai_settings.api_key == ""

    def test_ai_settings_valid_providers(self) -> None:
        """Test AISettings accepts valid providers."""
        for provider in ["openai", "ollama", "none"]:
            ai_settings = AISettings(provider=provider)  # type: ignore[arg-type]
            assert ai_settings.provider == provider


class TestGetSettings:
    """Test the get_settings cached singleton function."""

    def test_get_settings_returns_settings(self) -> None:
        """Test get_settings returns a Settings instance."""
        # Clear cache
        get_settings.cache_clear()
        settings = get_settings()
        assert isinstance(settings, Settings)

    def test_get_settings_is_cached(self) -> None:
        """Test get_settings returns the same cached instance."""
        get_settings.cache_clear()
        settings1 = get_settings()
        settings2 = get_settings()
        assert settings1 is settings2


class TestValidateSettingsOnStartup:
    """Test the startup validation function."""

    def test_validate_settings_returns_settings(self) -> None:
        """Test validate_settings_on_startup returns Settings on success."""
        get_settings.cache_clear()
        settings = validate_settings_on_startup()
        assert isinstance(settings, Settings)

    def test_validate_settings_raises_on_invalid(self) -> None:
        """Test validate_settings_on_startup raises on invalid config."""
        get_settings.cache_clear()
        with patch.dict(os.environ, {"RSS_LOG_LEVEL": "invalid"}, clear=False):
            with pytest.raises(ValueError) as exc_info:
                validate_settings_on_startup()
            assert "Configuration validation failed at startup" in str(exc_info.value)


class TestYamlConfigSettingsSource:
    """Test the YAML config settings source."""

    def test_source_returns_empty_when_no_file(self) -> None:
        """Test source returns empty dict when no YAML file exists."""
        # Use a directory without config.yaml
        original_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp_dir:
            try:
                os.chdir(tmp_dir)
                source = YamlConfigSettingsSource(Settings)
                result = source()
                assert result == {}
            finally:
                os.chdir(original_cwd)

    def test_source_loads_yaml_fields(self, tmp_path: Path) -> None:
        """Test source correctly loads fields from YAML."""
        config_yaml = tmp_path / "config.yaml"
        config_yaml.write_text(
            yaml.dump(
                {
                    "log_level": "debug",
                    "base_url": "https://test.com",
                }
            )
        )

        original_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            source = YamlConfigSettingsSource(Settings)
            result = source()
            assert result.get("log_level") == "debug"
            assert result.get("base_url") == "https://test.com"
        finally:
            os.chdir(original_cwd)


class TestSettingsIntegration:
    """Integration tests for settings with other modules."""

    def test_settings_provides_database_url_for_database_module(self) -> None:
        """Test settings can provide database URL for database.py."""
        get_settings.cache_clear()
        settings = get_settings()
        assert settings.database_url.startswith("sqlite+aiosqlite://")

    def test_settings_provides_log_config_for_logging_module(self) -> None:
        """Test settings can provide log config for logging.py."""
        get_settings.cache_clear()
        settings = get_settings()
        assert settings.log_level in {"debug", "info", "warning", "error"}
        assert settings.log_format in {"json", "console"}

    def test_settings_syncs_flat_and_nested_logging(self) -> None:
        """Test flat log_level/format syncs with nested logging settings."""
        settings = Settings(log_level="warning", log_format="console")
        # Flat values should be set
        assert settings.log_level == "warning"
        assert settings.log_format == "console"
        # Nested values should also be synced
        assert settings.logging.level == "warning"
        assert settings.logging.format == "console"
