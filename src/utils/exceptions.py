from fastapi import HTTPException, status
from typing import Any, Dict, Optional


class BaseAPIException(HTTPException):
    """Base exception class for all API exceptions"""

    def __init__(
        self,
        status_code: int,
        message: str,
        error_code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ):
        self.error_code = error_code
        self.details = details or {}
        super().__init__(
            status_code=status_code,
            detail={"message": message, "error_code": error_code, "details": details},
        )


# ============= Authentication Exceptions =============
class AuthenticationException(BaseAPIException):
    """Base authentication exception"""

    def __init__(
        self,
        message: str = "Authentication failed",
        error_code: str = "AUTH_ERROR",
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message=message,
            error_code=error_code,
            details=details,
        )


class InvalidCredentialsException(AuthenticationException):
    """Raised when login credentials are invalid"""

    def __init__(self, message: str = "Invalid email or password"):
        super().__init__(message=message, error_code="INVALID_CREDENTIALS")


class InvalidTokenException(AuthenticationException):
    """Raised when JWT token is invalid or expired"""

    def __init__(self, message: str = "Invalid or expired token"):
        super().__init__(message=message, error_code="INVALID_TOKEN")


class TokenExpiredException(AuthenticationException):
    """Raised when JWT token has expired"""

    def __init__(self, message: str = "Token has expired"):
        super().__init__(message=message, error_code="TOKEN_EXPIRED")


class MissingTokenException(AuthenticationException):
    """Raised when authorization token is missing"""

    def __init__(self, message: str = "Authorization token is required"):
        super().__init__(message=message, error_code="MISSING_TOKEN")


class InactiveUserException(AuthenticationException):
    """Raised when user account is inactive"""

    def __init__(self, message: str = "User account is inactive"):
        super().__init__(message=message, error_code="INACTIVE_USER")


class UnverifiedUserException(AuthenticationException):
    """Raised when user email/phone is not verified"""

    def __init__(self, message: str = "User account is not verified"):
        super().__init__(message=message, error_code="UNVERIFIED_USER")


# ============= Authorization Exceptions =============
class AuthorizationException(BaseAPIException):
    """Base authorization exception"""

    def __init__(
        self,
        message: str = "Access denied",
        error_code: str = "AUTHORIZATION_ERROR",
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            message=message,
            error_code=error_code,
            details=details,
        )


class InsufficientPermissionsException(AuthorizationException):
    """Raised when user lacks required permissions"""

    def __init__(
        self,
        message: str = "You don't have permission to perform this action",
        required_permission: Optional[str] = None,
    ):
        super().__init__(
            message=message,
            error_code="INSUFFICIENT_PERMISSIONS",
            details=(
                {"required_permission": required_permission}
                if required_permission
                else None
            ),
        )


# ============= Resource Exceptions =============
class NotFoundException(BaseAPIException):
    """Raised when a requested resource is not found"""

    def __init__(
        self, message: str = "Resource not found", resource: Optional[str] = None
    ):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            message=message,
            error_code="NOT_FOUND",
            details={"resource": resource} if resource else None,
        )


class AlreadyExistsException(BaseAPIException):
    """Raised when trying to create a resource that already exists"""

    def __init__(
        self, message: str = "Resource already exists", resource: Optional[str] = None
    ):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            message=message,
            error_code="ALREADY_EXISTS",
            details={"resource": resource} if resource else None,
        )


# ============= Validation Exceptions =============
class ValidationException(BaseAPIException):
    """Raised when input validation fails"""

    def __init__(
        self,
        message: str = "Validation failed",
        errors: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            message=message,
            error_code="VALIDATION_ERROR",
            details={"errors": errors} if errors else None,
        )


class InvalidInputException(ValidationException):
    """Raised when input data is invalid"""

    def __init__(
        self, message: str = "Invalid input data", field: Optional[str] = None
    ):
        super().__init__(message=message, errors={"field": field} if field else None)


# ============= Database Exceptions =============
class DatabaseException(BaseAPIException):
    """Base database exception"""

    def __init__(
        self,
        message: str = "Database operation failed",
        error_code: str = "DATABASE_ERROR",
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=message,
            error_code=error_code,
            details=details,
        )


class DuplicateEntryException(DatabaseException):
    """Raised when a duplicate entry is detected in database"""

    def __init__(
        self, message: str = "Duplicate entry detected", field: Optional[str] = None
    ):
        super().__init__(
            message=message,
            error_code="DUPLICATE_ENTRY",
            details={"field": field} if field else None,
        )


class ServiceException(BaseAPIException):
    """Base service exception"""

    def __init__(
        self,
        message: str = "Service error occurred",
        error_code: str = "SERVICE_ERROR",
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=message,
            error_code=error_code,
            details=details,
        )


class ExternalServiceException(ServiceException):
    """Raised when external service call fails"""

    def __init__(
        self,
        message: str = "External service error",
        service_name: Optional[str] = None,
    ):
        super().__init__(
            message=message,
            error_code="EXTERNAL_SERVICE_ERROR",
            details={"service": service_name} if service_name else None,
        )
