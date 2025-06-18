class DomainError(Exception):
    """Base class for domain-specific errors."""
    pass

class NotFoundError(DomainError):
    """Raised when a resource is not found or access is denied."""
    pass

class PermissionDeniedError(DomainError):
    """Raised when a user lacks permission."""
    pass

class ConflictError(DomainError):
    """Raised when a conflicting resource exists."""
    pass

class InternalError(DomainError):
    """Raised on unexpected internal failures."""
    pass