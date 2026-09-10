"""
V1 API routes.

Main endpoints for phishing detection.
"""

from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from typing import Optional
from app.api.middleware.auth import get_api_key
from app.api.middleware.rate_limit import rate_limiter
from app.api.middleware.quota import quota_manager
from app.services.metrics import track_prediction
from inference.hybrid_predictor import HybridPredictor
import hashlib
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

predictor = HybridPredictor()

class CheckRequest(BaseModel):
    url: str
    fetch_content: Optional[bool] = False
    include_indicators: Optional[bool] = True

class CheckResponse(BaseModel):
    prediction: str
    risk_score: float
    confidence: float

@router.post("/v1/check", response_model=CheckResponse)
def check_url(
    request: Request,
    payload: CheckRequest,
    api_key: str = Depends(get_api_key)
):
    """
    Check a single URL for phishing.
    
    Args:
        request: FastAPI request object
        payload: CheckRequest with URL
        api_key: Validated API key
        
    Returns:
        Prediction result
    """
    rate_limiter.check(request.client.host, api_key)
    
    result = predictor.predict(payload.url)
    track_prediction(result["prediction"])
    
    api_key_hash = hashlib.sha256(api_key.encode()).hexdigest()[:16]
    logger.info(f"Prediction: {result['prediction']} for URL hash: {hashlib.sha256(payload.url.encode()).hexdigest()[:16]}")
    
    return CheckResponse(
        prediction=result["prediction"],
        risk_score=result["risk_score"],
        confidence=result["confidence"]
    )
