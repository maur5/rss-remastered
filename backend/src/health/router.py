"""Health check router with endpoints for health probes.

Endpoints:
    GET /api/health - Basic health check for container orchestration
"""

from fastapi import APIRouter

from src.health.service import HealthStatus, get_health_status

router = APIRouter(prefix="/health", tags=["health"])


@router.get("", response_model=HealthStatus)
def health_check() -> HealthStatus:
    """Health check endpoint for container orchestration.

    Returns:
        HealthStatus with status field set to "healthy".

    Used by:
        - Docker health probes
        - Kubernetes liveness/readiness probes
        - Load balancer health checks
    """
    return get_health_status()
