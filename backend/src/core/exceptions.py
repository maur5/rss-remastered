"""Base exception classes for the application.

This module defines the exception hierarchy used throughout the application.
All domain-specific exceptions should inherit from these base classes.

Error code pattern: DOMAIN_ACTION_REASON
Example: SUBSCRIPTION_CREATE_INVALID_URL
"""


class AppException(Exception):
    """Base exception for all application exceptions.

    Attributes:
        code: Error code following DOMAIN_ACTION_REASON pattern.
        message: Human-readable error message.
        status_code: HTTP status code for API responses.
    """

    code: str = "APP_ERROR"
    status_code: int = 400

    def __init__(self, message: str | None = None, code: str | None = None) -> None:
        """Initialize the exception.

        Args:
            message: Optional custom error message.
            code: Optional custom error code.
        """
        self.message = message or self.__class__.__doc__ or "An error occurred"
        if code:
            self.code = code
        super().__init__(self.message)


class NotFoundError(AppException):
    """Resource not found."""

    code = "NOT_FOUND"
    status_code = 404


class ValidationError(AppException):
    """Validation failed."""

    code = "VALIDATION_ERROR"
    status_code = 400


class ConflictError(AppException):
    """Resource conflict (e.g., duplicate)."""

    code = "CONFLICT"
    status_code = 409


class UnauthorizedError(AppException):
    """Authentication required."""

    code = "UNAUTHORIZED"
    status_code = 401


class ForbiddenError(AppException):
    """Permission denied."""

    code = "FORBIDDEN"
    status_code = 403
