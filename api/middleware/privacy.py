import re
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

class PrivacyManager:
    @staticmethod
    def sanitize_url(url: str) -> str:
        """
        Redact potential PII (tokens, passwords, email) from URL queries.
        """
        parsed = urlparse(url)
        if not parsed.query:
            return url
        
        query_params = parse_qs(parsed.query, keep_blank_values=True)
        sensitive_keys = {"token", "auth", "key", "password", "pwd", "secret", "email", "id", "session"}
        
        sanitized_params = {}
        for k, v in query_params.items():
            if any(sensitive in k.lower() for sensitive in sensitive_keys):
                sanitized_params[k] = ["[REDACTED]"]
            else:
                sanitized_params[k] = v
                
        new_query = urlencode(sanitized_params, doseq=True)
        return urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, new_query, parsed.fragment))
