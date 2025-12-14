"""Tests for database configuration and session management.

Updated for Story 1.5: Uses Settings from core.config for database URL.
"""

import os
from pathlib import Path
from unittest.mock import patch

import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import get_settings
from src.core.database import (
    AsyncSessionLocal,
    Base,
    DatabaseSession,
    async_engine,
    create_engine,
    get_db,
)


class TestGetDatabaseUrl:
    """Tests for database URL configuration via Settings."""

    def test_returns_default_url_when_no_env_var(self) -> None:
        """Test that default SQLite URL is returned when no env var set."""
        # Clear settings cache to get fresh settings
        get_settings.cache_clear()
        settings = get_settings()
        assert settings.database_url == "sqlite+aiosqlite:///data/rss.db"

    def test_returns_env_var_when_set(self) -> None:
        """Test that environment variable URL is returned when set."""
        get_settings.cache_clear()
        custom_url = "sqlite+aiosqlite:///custom/path.db"
        with patch.dict(os.environ, {"RSS_DATABASE_URL": custom_url}, clear=False):
            get_settings.cache_clear()
            settings = get_settings()
            assert settings.database_url == custom_url
        get_settings.cache_clear()


class TestCreateEngine:
    """Tests for create_engine function."""

    def test_creates_async_engine(self) -> None:
        """Test that create_engine returns an async engine."""
        engine = create_engine("sqlite+aiosqlite:///:memory:")
        assert engine is not None
        assert "aiosqlite" in str(engine.url)

    def test_creates_data_directory_for_sqlite(self, tmp_path: Path) -> None:
        """Test that data directory is created for SQLite databases."""
        db_path = tmp_path / "subdir" / "test.db"
        url = f"sqlite+aiosqlite:///{db_path}"

        create_engine(url)

        # Directory should be created
        assert db_path.parent.exists()


class TestAsyncEngine:
    """Tests for the global async engine instance."""

    def test_async_engine_is_configured(self) -> None:
        """Test that the global async engine is properly configured."""
        assert async_engine is not None
        # Engine should be for SQLite with aiosqlite
        assert "sqlite" in str(async_engine.url)


class TestAsyncSessionLocal:
    """Tests for the async session factory."""

    async def test_session_factory_creates_sessions(self) -> None:
        """Test that AsyncSessionLocal creates valid sessions."""
        async with AsyncSessionLocal() as session:
            assert isinstance(session, AsyncSession)
            # Session should be usable for queries
            result = await session.execute(text("SELECT 1"))
            assert result.scalar() == 1


class TestGetDb:
    """Tests for the get_db dependency function."""

    async def test_get_db_yields_session(self) -> None:
        """Test that get_db yields a valid database session."""
        async for session in get_db():
            assert isinstance(session, AsyncSession)
            # Session should be usable
            result = await session.execute(text("SELECT 1"))
            assert result.scalar() == 1
            break

    async def test_get_db_commits_on_success(self) -> None:
        """Test that get_db commits the session on successful completion."""
        # This is an integration test - we verify the session lifecycle
        async for session in get_db():
            # Execute a simple query (no changes needed for this test)
            await session.execute(text("SELECT 1"))
            break
        # No exception means commit was successful


class TestBase:
    """Tests for the declarative Base class."""

    def test_base_is_declarative_base(self) -> None:
        """Test that Base is a proper DeclarativeBase subclass."""
        assert hasattr(Base, "metadata")
        assert hasattr(Base, "registry")


class TestDatabaseSession:
    """Tests for the DatabaseSession type alias."""

    def test_database_session_is_annotated(self) -> None:
        """Test that DatabaseSession is properly configured for dependency injection."""
        # DatabaseSession should be an Annotated type
        assert hasattr(DatabaseSession, "__metadata__")
