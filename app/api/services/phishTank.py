"""
PhishTank API Client

Client untuk PhishTank API dengan caching.
PhishTank menyediakan threat intelligence untuk URL phishing.

API Documentation: https://www.phishtank.com/developer_info.php
"""

import time
import hashlib
import requests
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


class PhishTankClient:
    """
    Client untuk PhishTank API dengan caching.
    
    Features:
    - Caching hasil query (1 jam)
    - Graceful error handling
    - Automatic fallback
    """
    
    # PhishTank API endpoints
    BASE_URL = "https://checkurl.phishtank.com/phishtank_api.php"
    
    # Cache settings
    CACHE_DURATION = 3600  # 1 hour in seconds
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize PhishTank client.
        
        Args:
            api_key: Optional PhishTank API key. Free API keys available at
                    https://www.phishtank.com/developer_info.php
        """
        self.api_key = api_key or ""
        self.cache: Dict[str, Dict[str, Any]] = {}
    
    def _get_cache_key(self, url: str) -> str:
        """Generate cache key from URL hash."""
        return hashlib.sha256(url.encode()).hexdigest()
    
    def _check_cache(self, url: str) -> Optional[Dict[str, Any]]:
        """Check if URL result is in cache."""
        cache_key = self._get_cache_key(url)
        
        if cache_key in self.cache:
            cache_entry = self.cache[cache_key]
            if time.time() - cache_entry["timestamp"] < self.CACHE_DURATION:
                logger.debug(f"Cache hit for {url[:50]}...")
                return cache_entry["result"]
            else:
                # Cache expired, remove it
                del self.cache[cache_key]
        
        return None
    
    def _save_cache(self, url: str, result: Dict[str, Any]) -> None:
        """Save result to cache."""
        cache_key = self._get_cache_key(url)
        self.cache[cache_key] = {
            "result": result,
            "timestamp": time.time()
        }
        logger.debug(f"Cached result for {url[:50]}...")
    
    def check_url(self, url: str) -> Dict[str, Any]:
        """
        Check URL against PhishTank database.
        
        Args:
            url: URL to check
            
        Returns:
            Dict with phishTank status:
            - status: 'verified', 'unverified', 'not_found', 'error'
            - phish_id: PhishTank ID if verified
            - verified_at: Verification timestamp if available
            - online: Whether phishing page is online
            - details: Full API response
        """
        # Check cache first
        cached = self._check_cache(url)
        if cached:
            return cached
        
        try:
            # Build request payload
            payload = {
                "url": url,
                "format": "json"
            }
            
            # Add API key if available
            if self.api_key:
                payload["app_key"] = self.api_key
            
            # Make request to PhishTank API
            logger.debug(f"Querying PhishTank for {url[:50]}...")
            
            response = requests.post(
                self.BASE_URL,
                data=payload,
                timeout=10,
                headers={"User-Agent": "Phishing-Detector/v1.1"}
            )
            
            response.raise_for_status()
            
            data = response.json()
            
            # Parse response
            # PhishTank returns: {"meta": {...}, "results": {...}}
            if "results" in data and data["results"]:
                results = data["results"]
                
                if results.get("in_database", False):
                    status = "verified" if results.get("verified", False) else "unverified"
                    result = {
                        "status": status,
                        "phish_id": results.get("phish_id"),
                        "verified_at": results.get("verified_at"),
                        "online": results.get("online", False),
                        "details": results
                    }
                else:
                    result = {
                        "status": "not_found",
                        "phish_id": None,
                        "details": results
                    }
            else:
                result = {
                    "status": "error",
                    "phish_id": None,
                    "details": data
                }
            
            # Save to cache
            self._save_cache(url, result)
            
            return result
            
        except requests.exceptions.Timeout:
            logger.warning(f"PhishTank API timeout for {url[:50]}...")
            return {
                "status": "error",
                "error": "timeout",
                "phish_id": None,
                "details": {"message": "Request timed out"}
            }
        except requests.exceptions.RequestException as e:
            logger.error(f"PhishTank API error for {url[:50]}: {e}")
            return {
                "status": "error",
                "error": str(e),
                "phish_id": None,
                "details": {"message": str(e)}
            }
    
    def clear_cache(self) -> None:
        """Clear all cache entries."""
        self.cache.clear()
        logger.info("PhishTank cache cleared")
    
    def get_cached_count(self) -> int:
        """Get number of cached entries."""
        return len(self.cache)


# Global client instance
phish_tank_client = PhishTankClient()
