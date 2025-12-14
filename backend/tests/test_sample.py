"""Sample test to verify pytest is working."""

import sys


def test_python_version() -> None:
    """Verify Python version meets project requirement (>=3.11)."""
    assert sys.version_info >= (3, 11), "Python 3.11+ required per pyproject.toml"


async def test_async_support() -> None:
    """Verify async test support works."""

    async def sample_async() -> str:
        return "async works"

    result = await sample_async()
    assert result == "async works"


def test_httpx_available() -> None:
    """Verify httpx is installed for API testing."""
    import httpx

    assert httpx is not None
