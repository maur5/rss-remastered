"""Database connection and session management.

This module provides the SQLAlchemy 2.0 async database infrastructure:
- async_engine: Async SQLAlchemy engine configured for SQLite with aiosqlite
- AsyncSessionLocal: Session factory for creating async database sessions
- get_db: FastAPI dependency for injecting database sessions into routes
- Base: Declarative base class for all SQLAlchemy models

Story 1.5: Updated to use Settings from core.config
"""

from collections.abc import AsyncGenerator
from pathlib import Path
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from src.core.config import get_settings


def _ensure_data_directory(database_url: str) -> None:
    """Ensure the data directory exists for SQLite databases.

    Args:
        database_url: The database URL to check.
    """
    if database_url.startswith("sqlite"):
        # Extract path from SQLite URL (handle both sqlite:/// and sqlite+aiosqlite:///)
        path_part = database_url.split("///")[-1]
        if path_part and path_part != ":memory:":
            db_path = Path(path_part)
            db_path.parent.mkdir(parents=True, exist_ok=True)


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy ORM models.

    All domain models should inherit from this class to be included
    in Alembic migrations and database schema management.
    """

    pass


def create_engine(database_url: str | None = None) -> AsyncEngine:
    """Create and configure the async SQLAlchemy engine.

    Args:
        database_url: Optional database URL override. If not provided,
            uses Settings.database_url from configuration.

    Returns:
        Configured AsyncEngine instance.
    """
    url = database_url or get_settings().database_url
    _ensure_data_directory(url)

    # SQLite-specific connect args for async operation
    connect_args = {}
    if url.startswith("sqlite"):
        connect_args["check_same_thread"] = False

    return create_async_engine(
        url,
        echo=False,  # Set to True for SQL query logging in development
        connect_args=connect_args,
    )


# Global async engine instance
async_engine: AsyncEngine = create_engine()

# Async session factory
AsyncSessionLocal: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency that provides a database session.

    Yields an async database session and ensures proper cleanup
    after the request is complete.

    Yields:
        AsyncSession: Database session for the current request.

    Example:
        ```python
        @router.get("/items")
        async def get_items(db: Annotated[AsyncSession, Depends(get_db)]):
            result = await db.execute(select(Item))
            return result.scalars().all()
        ```
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


# Type alias for FastAPI dependency injection
DatabaseSession = Annotated[AsyncSession, Depends(get_db)]
