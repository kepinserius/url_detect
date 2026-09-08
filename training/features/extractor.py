import re
import math
from urllib.parse import urlparse, parse_qs

class URLFeatureExtractor:
    """
    Extracts lexical, structural, and statistical features from a URL string.
    Operates strictly via static analysis without initiating network requests.
    """

    @staticmethod
    def calculate_entropy(text: str) -> float:
        if not text:
            return 0.0
        prob = [float(text.count(c)) / len(text) for c in set(text)]
        return -sum([p * math.log2(p) for p in prob if p > 0])

    def extract(self, url: str) -> dict:
        if not url.startswith(('http://', 'https://')):
            url_to_parse = 'http://' + url
        else:
            url_to_parse = url

        parsed = urlparse(url_to_parse)
        netloc = parsed.netloc
        path = parsed.path
        query = parsed.query
        scheme = parsed.scheme

        # Remove port if present
        hostname = netloc.split(':')[0] if ':' in netloc else netloc

        # Hostname features
        is_ip = 1 if re.match(r'^\d{1,3}(\.\d{1,3}){3}$', hostname) else 0
        hostname_length = len(hostname)
        num_dots = hostname.count('.')
        num_hyphens = hostname.count('-')
        num_at = hostname.count('@')
        num_digits_host = sum(c.isdigit() for c in hostname)

        # URL features
        url_length = len(url)
        num_slash = url.count('/')
        num_question = url.count('?')
        num_equal = url.count('=')
        num_ampersand = url.count('&')
        num_percent = url.count('%')
        num_digits_url = sum(c.isdigit() for c in url)
        has_https = 1 if scheme == 'https' else 0

        # Path features
        path_length = len(path)
        num_double_slash = url.count('//') - (1 if url.startswith(('http://', 'https://')) else 0)

        # Suspicious keywords
        keywords = ['login', 'signin', 'bank', 'account', 'update', 'verify', 'secure', 'ebayisapi', 'paypal', 'admin', 'wp-content']
        found_keywords = sum(1 for kw in keywords if kw in url.lower())

        # Entropy
        entropy = self.calculate_entropy(url)

        return {
            "url_length": url_length,
            "hostname_length": hostname_length,
            "path_length": path_length,
            "is_ip": is_ip,
            "num_dots": num_dots,
            "num_hyphens": num_hyphens,
            "num_at": num_at,
            "num_slash": num_slash,
            "num_question": num_question,
            "num_equal": num_equal,
            "num_ampersand": num_ampersand,
            "num_percent": num_percent,
            "num_digits_host": num_digits_host,
            "num_digits_url": num_digits_url,
            "has_https": has_https,
            "num_double_slash": max(0, num_double_slash),
            "found_keywords": found_keywords,
            "entropy": round(entropy, 4)
        }

    def get_indicators(self, url: str, features: dict) -> list[str]:
        indicators = []
        if features["is_ip"] == 1:
            indicators.append("IP address used as hostname")
        if features["url_length"] > 75:
            indicators.append("URL length exceeds recommended threshold (>75 chars)")
        if features["num_at"] > 0:
            indicators.append("Contains '@' symbol in URL")
        if features["num_hyphens"] > 3:
            indicators.append("Excessive hyphens in hostname")
        if features["num_dots"] > 4:
            indicators.append("High number of dots in domain structure")
        if features["found_keywords"] > 0:
            indicators.append("Contains sensitive security keywords (login, bank, etc.)")
        if features["has_https"] == 0:
            indicators.append("Insecure HTTP protocol used")
        return indicators
