"""
Metrics service for Prometheus.

Tracks predictions, latency, and errors.
"""

from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from fastapi import Response
import logging

logger = logging.getLogger(__name__)

# Metrics
prediction_counter = Counter(
    'phishing_predictions_total',
    'Total predictions',
    ['prediction_type']
)

request_duration = Histogram(
    'request_duration_seconds',
    'Request duration',
    buckets=[0.01, 0.05, 0.1, 0.2, 0.5, 1.0, 2.0, 5.0]
)

api_errors = Counter(
    'api_errors_total',
    'API errors',
    ['error_type']
)

def track_prediction(prediction: str):
    """Track prediction count."""
    prediction_counter.labels(prediction_type=prediction).inc()

def track_error(error_type: str):
    """Track error count."""
    api_errors.labels(error_type=error_type).inc()

def get_metrics():
    """Get Prometheus metrics."""
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)
