"""Core exceptions for the modular monolith."""


class AIInterviewError(Exception):
    """Base application exception."""

    status_code = 500


class ConfigurationError(AIInterviewError):
    """Raised when required configuration is missing or invalid."""


class NotFoundError(AIInterviewError):
    """Raised when a requested domain object is not found."""

    status_code = 404


class ValidationError(AIInterviewError):
    """Raised when a domain validation step fails."""

    status_code = 422


class ConflictError(AIInterviewError):
    """Raised when an operation conflicts with current domain state."""

    status_code = 409


class AuthenticationError(AIInterviewError):
    """Raised when an identity cannot be authenticated."""

    status_code = 401
