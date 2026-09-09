import re
from urllib.parse import urlparse

class URLFeatureExtractor:
    @staticmethod
    def extract_features(url: str) -> dict:
        parsed = urlparse(url)
        hostname = parsed.hostname or ""
        path = parsed.path or ""

        return {
            "url_length": len(url),
            "hostname_length": len(hostname),
            "path_length": len(path),
            "num_dots": url.count("."),
            "num_hyphens": url.count("-"),
            "num_at": url.count("@"),
            "num_question": url.count("?"),
            "num_percent": url.count("%"),
            "num_equal": url.count("="),
            "num_slash": url.count("/"),
            "is_https": 1 if parsed.scheme == "https" else 0,
            "has_ip": 1 if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", hostname) else 0,
            "num_digits": sum(c.isdigit() for c in url),
            "num_letters": sum(c.isalpha() for c in url),
        }
