"""
Rate limiting middleware.

Per-IP and per-API-key rate limiting.
"""

import time
from collections import defaultdict
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)

class RateLimiter:
    """
    Rate limiter with sliding window.
    
    Features:
    - Per-IP rate limiting
    - Per-API-key rate limiting
    - Configurable limits
    """
    
    def __init__(self):
        self.ip_requests: Dict[str, list] = defaultdict(list)
        self.api_key_requests: Dict[str, list] = defaultdict(list)
    
    def check(self, ip: str, api_key: Optional[str] = None) -> bool:
        """
        Check if request is allowed.
        
        Args:
            ip: Client IP address
            api_key: API key (optional)
            
        Returns:
            True if allowed, False if rate limited
        """
        current_time = time.time()
        window = 60  # 1 minute window
        
        # Clean old requests
        self._cleanup(self.ip_requests, ip, window)
        if api_key:
            self._cleanup(self.api_key_requests, api_key, window)
        
        # Check IP limit (100/min)
        if len(self.ip_requests[ip]) >= 100:
            return False
        
        # Check API key limit (if provided)
        if api_key and len(self.api_key_requests[api_key]) >= 1000:
            return False
        
        # Record request
        self.ip_requests[ip].append(current_time)
        if api_key:
            self.api_key_requests[api_key].append(current_time)
        
        return True
    
    def _cleanup(self, storage: dict, key: str, window: int):
        """Remove old requests outside the window."""
        if key not in storage:
            return
        
        current_time = time.time()
        storage[key] = [t for t in storage[key] if current_time - t < window]
        
        if not storage[key]:
            del storage[key]


# Global instance
rate_limiter = RateLimiter()
