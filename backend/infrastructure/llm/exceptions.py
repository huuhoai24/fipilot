class LLMServiceError(Exception):
    """Raised when an LLM service request fails."""


class LLMConfigurationError(LLMServiceError):
    """Raised when an LLM provider is misconfigured or missing credentials."""


class LLMResponseValidationError(LLMServiceError):
    """Raised when an LLM output fails schema validation."""
