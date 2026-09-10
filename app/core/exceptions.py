"""
Core exceptions.

Custom exceptions for URL Detect.
"""

class APIKeyError(Exception):
    """API key validation error."""
    pass

class QuotaError(Exception):
    """Quota exceeded error."""
    pass

class RateLimitError(Exception):
    """Rate limit exceeded error."""
    pass

class HTMLFetchError(Exception):
    """HTML fetch error."""
    pass

class PhishTankError(Exception):
    """PhishTank API error."""
    pass

class TenantError(Exception):
    """Tenant management error."""
    pass
