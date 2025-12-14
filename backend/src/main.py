"""FastAPI application entry point.

This module creates and configures the FastAPI application instance.

Story 1.5: Updated to validate settings at startup
"""

import time
import traceback
import uuid

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from src.core.config import get_settings, validate_settings_on_startup
from src.core.exceptions import AppException
from src.core.logging import bind_contextvars, clear_contextvars, get_logger, setup_logging

# Validate settings before anything else
# This ensures the application fails fast with clear error messages
# if configuration is invalid
settings = validate_settings_on_startup()

# Initialize structured logging (uses settings)
setup_logging()

# Get logger for this module
logger = get_logger("main")

# Development mode detection from settings or DEBUG env var
# Check for explicit DEBUG environment variable for backward compatibility
import os
DEBUG = os.getenv("DEBUG", "false").lower() in ("true", "1", "yes")


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for logging HTTP requests and responses."""

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        """Log request and response details.

        Args:
            request: The incoming HTTP request.
            call_next: The next middleware or route handler.

        Returns:
            The HTTP response.
        """
        # Generate a unique request ID
        request_id = str(uuid.uuid4())[:8]

        # Bind request context for all subsequent log messages
        bind_contextvars(request_id=request_id)

        # Record start time
        start_time = time.perf_counter()

        # Log incoming request (at debug level to avoid noise)
        logger.debug(
            "request_started",
            method=request.method,
            path=request.url.path,
            query=str(request.query_params) if request.query_params else None,
        )

        # Process request
        response = await call_next(request)

        # Calculate duration
        duration_ms = (time.perf_counter() - start_time) * 1000

        # Log completed request
        logger.info(
            "request_completed",
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            duration_ms=round(duration_ms, 2),
        )

        # Add request ID to response headers for tracing
        response.headers["X-Request-ID"] = request_id

        # Clear context vars for this request
        clear_contextvars()

        return response


app = FastAPI(
    title="RSS Remastered",
    description="Content aggregation and transformation backend",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    debug=DEBUG,
)

# CORS configuration for development
# In production, these should be restricted to actual frontend origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite dev server
        "http://localhost:3000",  # Alternative dev port
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request logging middleware (added after CORS so CORS headers are included)
app.add_middleware(RequestLoggingMiddleware)

# Import and mount routers
from src.health import router as health_router
app.include_router(health_router, prefix="/api")


@app.on_event("startup")
async def startup_event() -> None:
    """Log application startup with configuration details."""
    logger.info(
        "application_started",
        title=app.title,
        version=app.version,
        debug=DEBUG,
        database_url=settings.database_url.split("///")[0] + "///***",  # Mask DB path
        log_level=settings.log_level,
        log_format=settings.log_format,
        ai_provider=settings.ai.provider,
    )


@app.on_event("shutdown")
async def shutdown_event() -> None:
    """Log application shutdown."""
    logger.info("application_shutdown")


@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    """Handle application-specific exceptions.

    Args:
        request: The incoming request.
        exc: The raised AppException.

    Returns:
        JSONResponse with error details and appropriate status code.
    """
    logger.warning(
        "app_exception",
        error_code=exc.code,
        error_message=exc.message,
        status_code=exc.status_code,
        path=request.url.path,
        method=request.method,
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
            }
        },
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle unexpected exceptions.

    Args:
        request: The incoming request.
        exc: The raised exception.

    Returns:
        JSONResponse with generic error message (includes details in debug mode).
    """
    logger.error(
        "unhandled_exception",
        error_type=type(exc).__name__,
        error_message=str(exc),
        path=request.url.path,
        method=request.method,
        exc_info=exc,
    )
    content: dict[str, object] = {
        "error": {
            "code": "INTERNAL_SERVER_ERROR",
            "message": "An unexpected error occurred",
        }
    }

    # Include error details in debug mode for easier development
    if DEBUG:
        content["error"]["detail"] = str(exc)  # type: ignore[index]
        content["error"]["traceback"] = traceback.format_exc()  # type: ignore[index]

    return JSONResponse(status_code=500, content=content)
