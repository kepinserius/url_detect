"""
API schemas for request/response validation.

Pydantic models for API request and response validation.
"""

from pydantic import BaseModel, HttpUrl
from typing import List, Optional

class CheckRequest(BaseModel):
    url: str
    fetch_content: Optional[bool] = False
    include_indicators: Optional[bool] = True

class BatchRequest(BaseModel):
    urls: List[str]
    fetch_content: Optional[bool] = False
    include_indicators: Optional[bool] = True

class CheckResponse(BaseModel):
    url: str
    prediction: str
    risk_score: float
    confidence: float
    indicators: Optional[List[str]] = None
    phishTank_status: Optional[str] = None
    processing_time_ms: float

class BatchResponse(BaseModel):
    results: List[CheckResponse]
    total: int
    processing_time_ms: float

class HealthResponse(BaseModel):
    status: str
    version: str
