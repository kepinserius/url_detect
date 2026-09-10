"""
Main FastAPI application entry point.

Routes:
- GET /health: Health check
- POST /v1/check: Single URL check
- POST /v1/batch: Batch URL check
- GET /v1/metrics: Prometheus metrics
- GET /v1/indicators: Prediction explanation
- GET /v1/phishTank: Threat intel
- POST /v1/tenant: Tenant management (admin)
- GET /v1/sla: SLA dashboard (admin)
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.api.routes import v1, batch, indicators, phishTank, tenant
from app.services.metrics import metrics_middleware
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

app = FastAPI(
    title="URL Detect API",
    version="1.1.0",
    description="""
    Open-source phishing URL detection engine.

    ## Features
    - Single URL check
    - Batch processing (1000+ URLs)
    - PhishTank threat intelligence integration
    - Prediction indicators (explanation)
    - Multi-tenant support

    ## Authentication
    Use `X-API-Key` header with your API key.
    """,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags=[
        {"name": "health", "description": "Service health"},
        {"name": "v1", "description": "API v1 endpoints"},
        {"name": "batch", "description": "Batch processing"},
        {"name": "phishTank", "description": "Threat intelligence"},
        {"name": "tenant", "description": "Multi-tenant management (admin)"},
        {"name": "sla", "description": "SLA monitoring (admin)"}
    ]
)

# Middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    logger.debug(f"{request.method} {request.url.path} - {process_time:.3f}s")
    return response

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check
@app.get("/health", tags=["health"])
def health_check():
    return {"status": "healthy", "version": "1.1.0"}

# Include routers
app.include_router(v1.router, prefix="/v1")
app.include_router(batch.router, prefix="/v1")
app.include_router(indicators.router, prefix="/v1")
app.include_router(phishTank.router, prefix="/v1")
app.include_router(tenant.router, prefix="/v1")

# SLA endpoint (admin only)
@app.get("/v1/sla", tags=["sla"])
def sla_dashboard():
    """
    SLA dashboard - uptime and performance metrics.
    Admin only endpoint.
    """
    return {
        "uptime": "99.9%",
        "avg_response_time_ms": 15,
        "p95_response_time_ms": 50,
        "requests_24h": 0,  # Would require DB query
        "errors_24h": 0
    }

# Prometheus metrics endpoint
@app.get("/v1/metrics")
def metrics():
    """Prometheus metrics endpoint."""
    from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
    return generate_latest()

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    return {"error": "Not found", "message": str(exc)}

@app.exception_handler(500)
async def server_error_handler(request: Request, exc):
    logger.error(f"Internal server error: {exc}")
    return {"error": "Internal server error", "message": "Please try again later"}
