from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from fastapi import Response
import time

prediction_counter = Counter('phishing_predictions_total', 'Total predictions', ['prediction_type'])
request_duration = Histogram('request_duration_seconds', 'Request duration')
api_errors = Counter('api_errors_total', 'API errors', ['error_type'])

def track_prediction(prediction: str):
    prediction_counter.labels(prediction_type=prediction).inc()

def track_error(error_type: str):
    api_errors.labels(error_type=error_type).inc()

def get_metrics():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)
