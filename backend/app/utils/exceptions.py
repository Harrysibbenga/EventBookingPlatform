"""
Custom exceptions for the Event Booking Platform API.
Provides specific exception types for better error handling and debugging.
"""

from typing import Optional, Dict, Any


class EventBookingException(Exception):
    """Base exception class for Event Booking Platform."""
    
    def __init__(
        self,
        message: str,
        error_code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.error_code = error_code
        self.details = details or {}
        super().__init__(self.message)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert exception to dictionary for API responses."""
        result = {
            "error": self.__class__.__name__,
            "message": self.message
        }
        
        if self.error_code:
            result["error_code"] = self.error_code
        
        if self.details:
            result["details"] = self.details
        
        return result


class ValidationError(EventBookingException):
    def __init__(
        self,
        message: str,
        field: Optional[str] = None,
        value: Optional[Any] = None,
        error_code: Optional[str] = None,  # Make sure this parameter exists
        **kwargs
    ):
        details = kwargs.get("details", {})
        if field:
            details["field"] = field
        if value is not None:
            details["value"] = str(value)
        
        super().__init__(
            message,
            error_code=error_code or "VALIDATION_ERROR",  # Default error_code
            details=details
        )


class BookingServiceError(EventBookingException):
    """Raised when booking service operations fail."""
    
    def __init__(self, message: str, **kwargs):
        super().__init__(
            message,
            error_code="BOOKING_SERVICE_ERROR",
            **kwargs
        )


class ContactServiceError(EventBookingException):
    """Raised when contact service operations fail."""
    
    def __init__(self, message: str, **kwargs):
        super().__init__(
            message,
            error_code="CONTACT_SERVICE_ERROR",
            **kwargs
        )


class EmailServiceError(EventBookingException):
    """Raised when email service operations fail."""
    
    def __init__(self, message: str, **kwargs):
        super().__init__(
            message,
            error_code="EMAIL_SERVICE_ERROR",
            **kwargs
        )


class DatabaseError(EventBookingException):
    """Raised when database operations fail."""
    
    def __init__(self, message: str, operation: Optional[str] = None, **kwargs):
        details = kwargs.get("details", {})
        if operation:
            details["operation"] = operation
        
        super().__init__(
            message,
            error_code="DATABASE_ERROR",
            details=details
        )


class ConfigurationError(EventBookingException):
    """Raised when configuration is invalid or missing."""
    
    def __init__(self, message: str, setting: Optional[str] = None, **kwargs):
        details = kwargs.get("details", {})
        if setting:
            details["setting"] = setting
        
        super().__init__(
            message,
            error_code="CONFIGURATION_ERROR",
            details=details
        )


class AuthenticationError(EventBookingException):
    """Raised when authentication fails."""
    
    def __init__(self, message: str = "Authentication failed", **kwargs):
        super().__init__(
            message,
            error_code="AUTHENTICATION_ERROR",
            **kwargs
        )


class AuthorizationError(EventBookingException):
    """Raised when authorization fails."""
    
    def __init__(self, message: str = "Insufficient permissions", **kwargs):
        super().__init__(
            message,
            error_code="AUTHORIZATION_ERROR",
            **kwargs
        )


class RateLimitError(EventBookingException):
    """Raised when rate limit is exceeded."""
    
    def __init__(
        self,
        message: str = "Rate limit exceeded",
        retry_after: Optional[int] = None,
        **kwargs
    ):
        details = kwargs.get("details", {})
        if retry_after:
            details["retry_after"] = retry_after
        
        super().__init__(
            message,
            error_code="RATE_LIMIT_ERROR",
            details=details
        )


class ExternalServiceError(EventBookingException):
    """Raised when external service calls fail."""
    
    def __init__(
        self,
        message: str,
        service: Optional[str] = None,
        status_code: Optional[int] = None,
        **kwargs
    ):
        details = kwargs.get("details", {})
        if service:
            details["service"] = service
        if status_code:
            details["status_code"] = status_code
        
        super().__init__(
            message,
            error_code="EXTERNAL_SERVICE_ERROR",
            details=details
        )


class BusinessRuleError(EventBookingException):
    """Raised when business rules are violated."""
    
    def __init__(
        self,
        message: str,
        rule: Optional[str] = None,
        **kwargs
    ):
        details = kwargs.get("details", {})
        if rule:
            details["rule"] = rule
        
        super().__init__(
            message,
            error_code="BUSINESS_RULE_ERROR",
            details=details
        )


class ResourceNotFoundError(EventBookingException):
    """Raised when a requested resource is not found."""
    
    def __init__(
        self,
        message: str,
        resource_type: Optional[str] = None,
        resource_id: Optional[Any] = None,
        **kwargs
    ):
        details = kwargs.get("details", {})
        if resource_type:
            details["resource_type"] = resource_type
        if resource_id is not None:
            details["resource_id"] = str(resource_id)
        
        super().__init__(
            message,
            error_code="RESOURCE_NOT_FOUND",
            details=details
        )


class DuplicateResourceError(EventBookingException):
    """Raised when attempting to create a duplicate resource."""
    
    def __init__(
        self,
        message: str,
        resource_type: Optional[str] = None,
        conflicting_field: Optional[str] = None,
        **kwargs
    ):
        details = kwargs.get("details", {})
        if resource_type:
            details["resource_type"] = resource_type
        if conflicting_field:
            details["conflicting_field"] = conflicting_field
        
        super().__init__(
            message,
            error_code="DUPLICATE_RESOURCE",
            details=details
        )


class ServiceUnavailableError(EventBookingException):
    """Raised when a service is temporarily unavailable."""
    
    def __init__(
        self,
        message: str = "Service temporarily unavailable",
        service: Optional[str] = None,
        **kwargs
    ):
        details = kwargs.get("details", {})
        if service:
            details["service"] = service
        
        super().__init__(
            message,
            error_code="SERVICE_UNAVAILABLE",
            details=details
        )


# Exception handling utilities

def handle_database_error(error: Exception) -> DatabaseError:
    """Convert SQLAlchemy errors to DatabaseError."""
    error_message = str(error)
    
    # Detect specific database errors
    if "UNIQUE constraint failed" in error_message:
        return DuplicateResourceError(
            "A record with this information already exists",
            details={"database_error": error_message}
        )
    elif "NOT NULL constraint failed" in error_message:
        return ValidationError(
            "Required field is missing",
            details={"database_error": error_message}
        )
    elif "FOREIGN KEY constraint failed" in error_message:
        return ValidationError(
            "Referenced record does not exist",
            details={"database_error": error_message}
        )
    else:
        return DatabaseError(
            "Database operation failed",
            details={"original_error": error_message}
        )


def format_validation_errors(errors: list) -> ValidationError:
    """Format Pydantic validation errors."""
    error_details = []
    
    for error in errors:
        field = ".".join(str(loc) for loc in error["loc"])
        error_details.append({
            "field": field,
            "message": error["msg"],
            "type": error["type"],
            "input": error.get("input")
        })
    
    return ValidationError(
        "Validation failed",
        details={"validation_errors": error_details}
    )


class ErrorHandler:
    """Centralized error handling utility."""
    
    @staticmethod
    def handle_service_error(error: Exception, service_name: str) -> EventBookingException:
        """Handle service-specific errors."""
        if isinstance(error, EventBookingException):
            return error
        
        # Map common exceptions
        error_message = str(error)
        
        if "connection" in error_message.lower():
            return ExternalServiceError(
                f"{service_name} connection failed",
                service=service_name,
                details={"original_error": error_message}
            )
        elif "timeout" in error_message.lower():
            return ExternalServiceError(
                f"{service_name} request timed out",
                service=service_name,
                details={"original_error": error_message}
            )
        else:
            return ExternalServiceError(
                f"{service_name} error: {error_message}",
                service=service_name,
                details={"original_error": error_message}
            )
    
    @staticmethod
    def get_http_status_code(error: EventBookingException) -> int:
        """Get appropriate HTTP status code for exception."""
        error_code_mapping = {
            "VALIDATION_ERROR": 422,
            "AUTHENTICATION_ERROR": 401,
            "AUTHORIZATION_ERROR": 403,
            "RESOURCE_NOT_FOUND": 404,
            "DUPLICATE_RESOURCE": 409,
            "RATE_LIMIT_ERROR": 429,
            "SERVICE_UNAVAILABLE": 503,
            "EXTERNAL_SERVICE_ERROR": 502,
            "BUSINESS_RULE_ERROR": 400,
            "CONFIGURATION_ERROR": 500,
            "DATABASE_ERROR": 500,
            "BOOKING_SERVICE_ERROR": 500,
            "CONTACT_SERVICE_ERROR": 500,
            "EMAIL_SERVICE_ERROR": 500
        }
        
        return error_code_mapping.get(error.error_code, 500)