from fastapi import APIRouter, Depends, Request
from api.schemas.prediction import URLCheckRequest, URLCheckResponse
from api.middleware.auth import get_api_key
from api.middleware.rate_limit import rate_limiter
from api.services.logger import prediction_logger
from api.services.metrics import track_prediction
from inference.hybrid_predictor import HybridPredictor
import hashlib

router = APIRouter()
predictor = HybridPredictor()

@router.post("/check", response_model=URLCheckResponse, dependencies=[Depends(get_api_key)])
def check_url(request: Request, payload: URLCheckRequest):
    rate_limiter(request)
    result = predictor.predict(payload.url)
    
    api_key = request.headers.get("X-API-Key")
    api_key_hash = hashlib.sha256(api_key.encode()).hexdigest()[:16] if api_key else "anonymous"
    prediction_logger.log_prediction(payload.url, result["prediction"], result["risk_score"], api_key_hash)
    
    track_prediction(result["prediction"])
    
    return {
        "prediction": result["prediction"],
        "risk_score": result["risk_score"],
        "confidence": result["confidence"]
    }
