"""
Batch Processing Route for v1.

Endpoint:
- POST /v1/batch: Check 1000+ URLs in parallel
"""

from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from typing import List, Optional
import asyncio
import time

router = APIRouter()

class BatchRequest(BaseModel):
    urls: List[str]
    fetch_content: Optional[bool] = False
    include_indicators: Optional[bool] = True

class BatchResponseItem(BaseModel):
    url: str
    prediction: str
    risk_score: float
    confidence: float
    indicators: Optional[List[str]] = None
    phishTank_status: Optional[str] = None
    processing_time_ms: float

class BatchResponse(BaseModel):
    results: List[BatchResponseItem]
    total: int
    processing_time_ms: float

# Import predictor (will be set by main.py)
predictor = None

def set_predictor(p):
    """Set predictor from main app."""
    global predictor
    predictor = p

async def check_single_url(url: str) -> BatchResponseItem:
    """Check single URL with timing."""
    start = time.time()
    
    if predictor is None:
        raise RuntimeError("Predictor not initialized")
    
    result = predictor.predict(url)
    
    elapsed = (time.time() - start) * 1000  # ms
    
    return BatchResponseItem(
        url=url,
        prediction=result["prediction"],
        risk_score=result["risk_score"],
        confidence=result["confidence"],
        processing_time_ms=round(elapsed, 2)
    )

@router.post("/v1/batch", response_model=BatchResponse)
async def batch_check(
    request: Request,
    payload: BatchRequest
):
    """
    Batch check multiple URLs for phishing.
    
    Args:
        request: FastAPI request object
        payload: BatchRequest with up to 1000 URLs
        
    Returns:
        List of prediction results with timing info
    """
    urls = payload.urls
    
    if len(urls) > 1000:
        return {"error": "Maximum 1000 URLs per request", "total": 0, "processing_time_ms": 0}
    
    if len(urls) == 0:
        return {"error": "At least one URL is required", "total": 0, "processing_time_ms": 0}
    
    start_time = time.time()
    
    # Process in parallel (max 50 concurrent)
    semaphore = asyncio.Semaphore(50)
    
    async def check_with_semaphore(url):
        async with semaphore:
            return await check_single_url(url)
    
    tasks = [check_with_semaphore(url) for url in urls]
    results = await asyncio.gather(*tasks)
    
    total_time = (time.time() - start_time) * 1000  # ms
    
    return BatchResponse(
        results=list(results),
        total=len(results),
        processing_time_ms=round(total_time, 2)
    )
