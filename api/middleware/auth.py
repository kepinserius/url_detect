import os
from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader
from api.services.quota import QuotaManager

API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

def get_api_key(api_key: str = Security(api_key_header)):
    valid_api_key = os.getenv("API_KEY")
    
    if not valid_api_key:
        return None
    
    if api_key == valid_api_key:
        if not QuotaManager.check_and_increment(api_key):
            raise HTTPException(status_code=429, detail="Quota exceeded")
        return api_key
    
    raise HTTPException(status_code=403, detail="Invalid API Key")
