"""Tests for health check endpoint."""

from httpx import AsyncClient


async def test_health_endpoint_returns_healthy(async_client: AsyncClient) -> None:
    """Test that GET /api/health returns status healthy."""
    response = await async_client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


async def test_health_endpoint_content_type(async_client: AsyncClient) -> None:
    """Test that health endpoint returns JSON content type."""
    response = await async_client.get("/api/health")

    assert response.headers["content-type"] == "application/json"


async def test_request_includes_request_id_header(async_client: AsyncClient) -> None:
    """Test that responses include X-Request-ID header from logging middleware."""
    response = await async_client.get("/api/health")

    assert "x-request-id" in response.headers
    # Request ID should be 8 characters (UUID truncated)
    assert len(response.headers["x-request-id"]) == 8
