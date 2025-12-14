"""Sample test to verify pytest is working."""
import pytest


def test_python_version():
    """Verify Python version is sufficient."""
    import sys
    assert sys.version_info >= (3, 9)


@pytest.mark.asyncio
async def test_async_support():
    """Verify async test support works."""
    async def sample_async():
        return "async works"
    
    result = await sample_async()
    assert result == "async works"


def test_httpx_available():
    """Verify httpx is installed for API testing."""
    import httpx
    assert httpx is not None
