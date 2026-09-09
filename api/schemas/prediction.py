from pydantic import BaseModel

class URLCheckRequest(BaseModel):
    url: str

class URLCheckResponse(BaseModel):
    prediction: str
    risk_score: float
    confidence: float
