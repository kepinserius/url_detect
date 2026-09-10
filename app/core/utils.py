"""
Core utilities.

Utility functions for URL Detect.
"""

import hashlib
import re

def hash_url(url: str) -> str:
    """SHA256 hash of URL for storage."""
    return hashlib.sha256(url.encode()).hexdigest()

def is_valid_url(url: str) -> bool:
    """Validate URL format."""
    pattern = r'^https?://[a-zA-Z0-9.-]+(?:/[^\s]*)?$'
    return bool(re.match(pattern, url))

def sanitize_url(url: str) -> str:
    """Sanitize URL for logging (remove sensitive query params)."""
    from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
    
    parsed = urlparse(url)
    if not parsed.query:
        return url
    
    query_params = parse_qs(parsed.query, keep_blank_values=True)
    sensitive_keys = {"token", "auth", "key", "password", "pwd", "secret", "email", "id", "session"}
    
    sanitized = {}
    for k, v in query_params.items():
        if any(sensitive in k.lower() for sensitive in sensitive_keys):
            sanitized[k] = ["[REDACTED]"]
        else:
            sanitized[k] = v
    
    new_query = urlencode(sanitized, doseq=True)
    return urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, new_query, parsed.fragment))

def safe_truncate(text: str, max_length: int = 100) -> str:
    """Safely truncate string."""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."
