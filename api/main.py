from fastapi import FastAPI, Request, Response
from dotenv import load_dotenv
from api.routes import v1
from api.middleware.auth import get_api_key
from api.services.metrics import get_metrics, track_prediction, request_duration, api_errors
import time

load_dotenv()

app = FastAPI(
    title="Phishing URL Detector API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    description="""
    Open-source phishing URL detection engine.

    ## Authentication
    Use `X-API-Key` header with your API key.

    ## Endpoints
    - `GET /health`: Health check
    - `GET /metrics`: Prometheus metrics
    - `POST /v1/check`: Check if a URL is phishing

    ## Example
    ```bash
    curl -X POST http://localhost:8000/v1/check \\
      -H "X-API-Key: your_api_key" \\
      -H "Content-Type: application/json" \\
      -d '{"url": "https://example.com"}'
    ```
    """,
    openapi_tags=[
        {"name": "health", "description": "Service health"},
        {"name": "v1", "description": "API v1 endpoints"}
    ]
)

@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start_time = time.time()
    try:
        response = await call_next(request)
        duration = time.time() - start_time
        request_duration.observe(duration)
        return response
    except Exception as e:
        api_errors.labels(error_type=type(e).__name__).inc()
        raise

@app.get("/health", tags=["health"])
def health_check():
    return {"status": "healthy"}

@app.get("/metrics")
def metrics():
    return get_metrics()

app.include_router(v1.router, prefix="/v1")
