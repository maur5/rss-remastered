"""Pytest configuration and fixtures for backend tests.

This module provides shared fixtures for all backend tests including:
- Async HTTP client for testing FastAPI endpoints
- Database session fixtures for isolated test databases
"""

import os
from collections.abc import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.core.database import Base, get_db
from src.main import app


@pytest.fixture
def anyio_backend() -> str:
    """Configure anyio backend for async tests."""
    return "asyncio"


@pytest.fixture
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    """Async HTTP client for testing FastAPI endpoints.

    Yields:
        AsyncClient configured to test the FastAPI app.
    """
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        yield client


@pytest.fixture
async def test_db() -> AsyncGenerator[AsyncSession, None]:
    """Create a fresh in-memory database for each test.

    This fixture creates an isolated in-memory SQLite database,
    creates all tables, and provides a session for the test.
    The database is disposed after the test completes.

    Yields:
        AsyncSession: Database session connected to test database.
    """
    # Use in-memory SQLite for test isolation
    test_engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        echo=False,
    )

    # Create all tables
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Create session factory for this test database
    TestSessionLocal = async_sessionmaker(
        bind=test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
    )

    # Provide session for the test
    async with TestSessionLocal() as session:
        yield session

    # Cleanup
    await test_engine.dispose()


@pytest.fixture
async def async_client_with_db(
    test_db: AsyncSession,
) -> AsyncGenerator[AsyncClient, None]:
    """Async HTTP client with overridden database dependency.

    This fixture provides an HTTP client where the database session
    is replaced with the test database session, ensuring API tests
    use an isolated in-memory database.

    Args:
        test_db: The test database session fixture.

    Yields:
        AsyncClient configured with test database.
    """

    async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
        yield test_db

    # Override the get_db dependency
    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        yield client

    # Clear the override
    app.dependency_overrides.clear()
