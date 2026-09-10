"""
Indicators Route - Prediction explanation API.

Endpoint:
- GET /v1/indicators/{url_hash}: Get explanation for prediction
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from app.api.services.indicators import indicators_service

router = APIRouter()

class IndicatorsRequest(BaseModel):
    url: str

class IndicatorsResponse(BaseModel):
    url: str
    indicators: List[str]

@router.post("/v1/indicators")
def get_indicators(
    payload: IndicatorsRequest
):
    """
    Get prediction indicators for a URL.
    
    Returns human-readable reasons why a URL was classified as phishing or legitimate.
    
    Args:
        payload: {"url": "https://example.com"}
        
    Returns:
        List of indicator strings explaining the classification
    """
    url = payload.url
    
    # Placeholder - in production, fetch prediction from database
    # For now, simulate with a basic classification
    prediction = "legitimate"
    
    indicators = indicators_service.generate(url, prediction, {
        "rule_score": 0.0,
        "suspicious_tld": False,
        "typosquatting": None,
        "brand_abuse": None
    })
    
    return IndicatorsResponse(
        url=url,
        indicators=indicators
    )
