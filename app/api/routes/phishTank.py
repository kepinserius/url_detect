from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.api.services.phishTank import phish_tank_client
from app.models.database import RequestLog, PhishTankCache, SessionLocal
from datetime import datetime, timedelta
import hashlib
import json
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/v1/phishTank/{url_hash}")
def check_phish_tank(url_hash: str):
    """
    Check PhishTank status for a URL hash.
    
    Returns cached result if available, otherwise queries PhishTank API.
    """
    return {
        "url_hash": url_hash,
        "status": "not_found",
        "phish_id": None,
        "details": {
            "message": "URL not found in cache. Store URL mapping first."
        }
    }

@router.post("/v1/phishTank/check")
def check_phish_tank_by_url(payload: dict, db=Depends(get_db)):
    """
    Check PhishTank status for a URL (direct URL input).
    """
    url = payload.get("url")
    if not url:
        return {"error": "URL is required"}
    
    cache_key = hashlib.sha256(url.encode()).hexdigest()
    
    # Check if cached
    cached = db.query(PhishTankCache).filter(
        PhishTankCache.url_hash == cache_key,
        PhishTankCache.expires_at > datetime.utcnow()
    ).first()
    
    if cached:
        return {"status": "cached", "result": json.loads(cached.result)}
    
    # Query PhishTank API
    result = phish_tank_client.check_url(url)
    
    # Save to cache
    cache_entry = PhishTankCache(
        url_hash=cache_key,
        result=json.dumps(result),
        expires_at=datetime.utcnow() + timedelta(hours=1)
    )
    db.add(cache_entry)
    db.commit()
    
    return {"status": "api", "result": result}
