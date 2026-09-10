"""
Quota management service.

Per-tenant quota checking and tracking.
"""

import time
from collections import defaultdict
from typing import Dict
import logging

logger = logging.getLogger(__name__)

class QuotaManager:
    """
    Manage API quotas per tenant/API key.
    
    Features:
    - Track request count per tenant
    - Enforce daily limits
    - Handle tier-based quotas
    """
    
    def __init__(self):
        # In-memory storage (use Redis for production)
        self.request_counts: Dict[str, Dict] = defaultdict(lambda: {
            "count": 0,
            "reset_time": time.time() + 86400  # Reset daily
        })
    
    def check_and_increment(self, api_key: str, quota_limit: int) -> bool:
        """
        Check quota and increment if available.
        
        Args:
            api_key: API key to check
            quota_limit: Daily quota limit
            
        Returns:
            True if request allowed, False if quota exceeded
        """
        current_time = time.time()
        
        # Reset daily if needed
        if current_time > self.request_counts[api_key]["reset_time"]:
            self.request_counts[api_key] = {
                "count": 0,
                "reset_time": current_time + 86400
            }
        
        # Check quota
        if self.request_counts[api_key]["count"] >= quota_limit:
            logger.warning(f"Quota exceeded for API key: {api_key[:8]}...")
            return False
        
        # Increment
        self.request_counts[api_key]["count"] += 1
        return True
    
    def get_remaining(self, api_key: str, quota_limit: int) -> int:
        """Get remaining quota for API key."""
        if api_key not in self.request_counts:
            return quota_limit
        
        return max(0, quota_limit - self.request_counts[api_key]["count"])
    
    def get_count(self, api_key: str) -> int:
        """Get current request count for API key."""
        return self.request_counts.get(api_key, {}).get("count", 0)


# Global instance
quota_manager = QuotaManager()
