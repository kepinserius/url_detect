"""
HTML Content Fetcher Service (async version).

Safe HTML fetching with:
- Timeout (5 seconds)
- Size limit (100KB)
- Internal IP blocking
- SSL verification enabled
"""

import re
import socket
import asyncio
from typing import Optional, Dict, Any
import httpx
import logging

logger = logging.getLogger(__name__)

# Private/internal IP ranges
PRIVATE_IP_PATTERNS = [
    r"^10\.\d{1,3}\.\d{1,3}\.\d{1,3}$",
    r"^172\.(1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3}$",
    r"^192\.168\.\d{1,3}\.\d{1,3}$",
    r"^127\.\d{1,3}\.\d{1,3}\.\d{1,3}$",
    r"^0\.0\.0\.0$",
    r"^::1$",
    r"^::ffff:127\.\d{1,3}\.\d{1,3}\.\d{1,3}$",
]

MAX_CONTENT_SIZE = 100 * 1024
FETCH_TIMEOUT = 5


def is_private_ip(ip: str) -> bool:
    """Check if IP is private/internal."""
    for pattern in PRIVATE_IP_PATTERNS:
        if re.match(pattern, ip):
            return True
    return False


def resolve_ip(hostname: str) -> str | None:
    """Resolve hostname to IP address."""
    try:
        return socket.gethostbyname(hostname)
    except socket.gaierror:
        return None


def validate_url(url: str) -> bool:
    """Validate URL for safe fetching."""
    import urllib.parse
    
    try:
        parsed = urllib.parse.urlparse(url)
        if parsed.scheme not in ["http", "https"]:
            logger.warning(f"Invalid scheme: {parsed.scheme}")
            return False
        if not parsed.hostname:
            logger.warning("No hostname in URL")
            return False
        ip = resolve_ip(parsed.hostname)
        if not ip:
            logger.warning(f"Could not resolve hostname: {parsed.hostname}")
            return False
        if is_private_ip(ip):
            logger.warning(f"Private IP blocked: {ip}")
            return False
        return True
    except Exception as e:
        logger.error(f"URL validation error: {e}")
        return False


class HTMLFetcher:
    """Safe HTML fetcher with security checks."""
    
    def __init__(self, timeout: float = FETCH_TIMEOUT, max_size: int = MAX_CONTENT_SIZE):
        self.timeout = timeout
        self.max_size = max_size
        self.client = None
    
    async def __aenter__(self):
        self.client = httpx.AsyncClient(
            timeout=httpx.Timeout(self.timeout),
            follow_redirects=True,
            max_redirects=5,
            verify=True
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.client:
            await self.client.aclose()
    
    async def fetch(self, url: str) -> Optional[Dict[str, Any]]:
        """Fetch HTML content safely."""
        if not validate_url(url):
            logger.warning(f"Unsafe URL blocked: {url}")
            return None
        
        try:
            response = await self.client.get(url)
            if len(response.content) > self.max_size:
                logger.warning(f"Content too large: {len(response.content)} bytes")
                return None
            
            return {
                "status_code": response.status_code,
                "content": response.text,
                "headers": dict(response.headers),
                "url": str(response.url),
                "size_bytes": len(response.content)
            }
        except httpx.TimeoutException:
            logger.warning(f"Fetch timeout for {url}")
            return None
        except httpx.RequestError as e:
            logger.warning(f"Fetch error for {url}: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error fetching {url}: {e}")
            return None


html_fetcher = HTMLFetcher()


# Sync wrapper
def fetch_html(url: str) -> Optional[Dict[str, Any]]:
    """Synchronous HTML fetch wrapper."""
    try:
        with httpx.Client(
            timeout=httpx.Timeout(FETCH_TIMEOUT),
            follow_redirects=True,
            verify=True
        ) as client:
            response = client.get(url)
            if len(response.content) > MAX_CONTENT_SIZE:
                return None
            return {
                "status_code": response.status_code,
                "content": response.text,
                "headers": dict(response.headers),
                "url": str(response.url),
                "size_bytes": len(response.content)
            }
    except Exception as e:
        logger.warning(f"Sync fetch error for {url}: {e}")
        return None
