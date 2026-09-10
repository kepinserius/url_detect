"""
Authentication middleware.

API key validation and tenant lookup.
"""

from fastapi import HTTPException, Security, Depends
from fastapi.security import APIKeyHeader
from app.core.exceptions import APIKeyError
from app.core.config import settings
import hashlib
import logging

logger = logging.getLogger(__name__)

API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

def verify_api_key(api_key: str = Security(api_key_header)):
    """
    Verify API key and return tenant info.
    
    Args:
        api_key: API key from header
        
    Returns:
        Tenant info dict
        
    Raises:
        HTTPException: If API key invalid
    """
    if not api_key:
        raise HTTPException(status_code=403, detail="Missing API Key")
    
    # For MVP, simple API key comparison
    if api_key != settings.api_key:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    
    # In production, query database for tenant info
    return {"tenant_id": 1, "tier": "free", "quota": 100}

def get_api_key(api_key: str = Security(api_key_header)):
    """
    Simple API key validation.
    
    Args:
        api_key: API key from header
        
    Returns:
        API key if valid
        
    Raises:
        HTTPException: If API key invalid
    """
    if not api_key:
        raise HTTPException(status_code=403, detail="Missing API Key")
    
    if api_key != settings.api_key:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    
    return api_key
