"""Health check service with health check logic.

This module provides health check functionality for the application.
Future enhancements will include database health, queue depth, etc.
"""

from pydantic import BaseModel


class HealthStatus(BaseModel):
    """Health status response model."""

    status: str


def get_health_status() -> HealthStatus:
    """Get the current health status of the application.

    Returns:
        HealthStatus model with status field.

    Future enhancements:
        - Database connectivity check
        - Queue depth monitoring
        - External service availability
        - Memory/CPU metrics
    """
    return HealthStatus(status="healthy")
