"""
HTML Content Fetcher Service.

Safe HTML fetching with:
- Timeout (5 seconds)
- Size limit (100KB)
- Internal IP blocking
- SSL verification enabled
"""

import re
import socket
import httpx
import logging

logger = logging.getLogger(__name__)

# Private/internal IP ranges
PRIVATE_IP_PATTERNS = [
    r"^10\.\d{1,3}\.\d{1,3}\.\d{1,3}$",        # 10.0.0.0/8
    r"^172\.(1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3}$",  # 172.16.0.0/12
    r"^192\.168\.\d{1,3}\.\d{1,3}$",           # 192.168.0.0/16
    r"^127\.\d{1,3}\.\d{1,3}\.\d{1,3}$",       # 127.0.0.0/8
    r"^0\.0\.0\.0$",                           # 0.0.0.0
    r"^::1$",                                  # IPv6 localhost
    r"^::ffff:127\.\d{1,3}\.\d{1,3}\.\d{1,3}$",  # IPv6 mapped localhost
]

MAX_CONTENT_SIZE = 100 * 1024  # 100KB
FETCH_TIMEOUT = 5  # seconds


def is_private_ip(ip: str) -> bool:
    """Check if IP is private/internal."""
    for pattern in PRIVATE_IP_PATTERNS:
        if re.match(pattern, ip):
            return True
    return False


def resolve_ip(hostname: str) -> str | None:
    """Resolve hostname to IP address."""
    try:
        ip = socket.gethostbyname(hostname)
        return ip
    except socket.gaierror:
        return None


def validate_url(url: str) -> bool:
    """
    Validate URL for safe fetching.
    
    Returns True if URL is safe to fetch, False otherwise.
    """
    import urllib.parse
    
    try:
        parsed = urllib.parse.urlparse(url)
        
        # Must have valid scheme
        if parsed.scheme not in ["http", "https"]:
            logger.warning(f"Invalid scheme: {parsed.scheme}")
            return False
        
        # Must have hostname
        if not parsed.hostname:
            logger.warning("No hostname in URL")
            return False
        
        # Resolve IP and check if private
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
    """
    Safe HTML fetcher with security checks.
    """
    
    def __init__(
        self,
        timeout: float = FETCH_TIMEOUT,
        max_size: int = MAX_CONTENT_SIZE
    ):
        self.timeout = timeout
        self.max_size = max_size
        self.client = None
    
    async def __aenter__(self):
        self.client = httpx.AsyncClient(
            timeout=httpx.Timeout(self.timeout),
            follow_redirects=True,
            max_redirects=5,
            verify=True  # SSL verification
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.client:
            await self.client.aclose()
    
    async def fetch(self, url: str) -> Optional[Dict[str, Any]]:
        """
        Fetch HTML content safely.
        
        Args:
            url: URL to fetch
            
        Returns:
            Dict with HTML content, status_code, headers, etc.
            Returns None if fetch failed or URL is unsafe
        """
        # Validate URL first
        if not validate_url(url):
            logger.warning(f"Unsafe URL blocked: {url}")
            return None
        
        try:
            response = await self.client.get(url)
            
            # Check content length
            content_length = len(response.content)
            if content_length > self.max_size:
                logger.warning(f"Content too large: {content_length} bytes (max: {self.max_size})")
                return None
            
            # Return content info
            return {
                "status_code": response.status_code,
                "content": response.text,
                "headers": dict(response.headers),
                "url": str(response.url),
                "size_bytes": content_length
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


# Global fetcher instance
html_fetcher = HTMLFetcher()


# Sync wrapper for synchronous usage
def fetch_html(url: str) -> Optional[Dict[str, Any]]:
    """Synchronous HTML fetch wrapper."""
    try:
        return asyncio.run(html_fetcher.fetch(url))
    except RuntimeError:
        # Event loop already running, use sync client
        client = httpx.Client(
            timeout=httpx.Timeout(FETCH_TIMEOUT),
            follow_redirects=True,
            verify=True
        )
        try:
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
        finally:
            client.close()
