# Architecture Overview

## System Design

```
┌─────────────────────────────────────────────────────┐
│                   Third-Party Applications          │
│  (Browser extensions, Security tools, APIs)         │
└─────────────────────────┬───────────────────────────┘
                          │ HTTPS / REST API
                          ▼
┌─────────────────────────────────────────────────────┐
│                 Phishing URL Detector API           │
│                 (FastAPI application)               │
├─────────────────────────────────────────────────────┤
│  • Authentication (API Keys)                        │
│  • Rate Limiting & Quota Management                 │
│  • Structured Logging (with PII redaction)          │
│  • Prometheus Metrics                               │
│  • Privacy Middleware                               │
└─────────────────────────┬───────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────┐
│                Inference Engine                     │
│  • Feature Extractor (static URL analysis)          │
│  • Model Predictor (XGBoost / Random Forest)        │
│  • Model Registry & Versioning                      │
└─────────────────────────┬───────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────┐
│                Model & Data Layer                   │
│  • Machine Learning Models (XGBoost, RF, etc.)      │
│  • Feature Names & Metadata                         │
│  • Dataset (PhiUSIIL - externally sourced)          │
└─────────────────────────────────────────────────────┘
```

## Components

### 1. API Layer (`api/`)
- **Main application** (`api/main.py`): FastAPI app with health check, metrics, versioning
- **Routes** (`api/routes/`): API endpoints (v1/check, etc.)
- **Middleware** (`api/middleware/`):
  - `auth.py`: API key authentication
  - `rate_limit.py`: Rate limiting per IP/API key
  - `privacy.py`: PII redaction in URLs
- **Services** (`api/services/`):
  - `logger.py`: Structured logging
  - `metrics.py`: Prometheus metrics
  - `db.py`: SQLite for API keys & quotas
  - `quota.py`: Multi-tenant quota management

### 2. Inference Layer (`inference/`)
- **Predictor** (`inference/predictor.py`): Main prediction logic
- **Feature extraction** (`inference/features/extractor.py`): URL to feature vector
- **Model loading**: Handles multiple model versions

### 3. Training Layer (`training/`)
- **Data validation** (`training/preprocessing/validator.py`): Dataset quality checks
- **Data cleaning** (`training/preprocessing/cleaner.py`): Preprocessing pipeline
- **Data preparation** (`training/preprocessing/preprocessor.py`): Feature/label split
- **Model training** (`training/models/trainer.py`): Multi-model training
- **Hyperparameter tuning** (`training/models/tuner.py`): Optuna-based optimization
- **Evaluation** (`training/models/evaluator.py`): Metrics & reporting

### 4. Model Registry (`models/`)
- **Model artifacts**: Serialized models (XGBoost, RF, etc.)
- **Feature names**: Column names for consistent inference
- **Registry** (`models/registry.json`): Model version metadata
- **Evaluation reports**: JSON reports with performance metrics
- **Database** (`models/enterprise.db`): SQLite for API keys, quotas

### 5. SDK (`phishing_detector/`)
- **Client** (`phishing_detector/client.py`): Python SDK for easy integration
- **Package structure**: Ready for PyPI distribution

## Security Architecture

### Data Flow Security
1. **No URL fetching**: Static analysis only, prevents SSRF
2. **PII redaction**: URLs are sanitized before logging
3. **API authentication**: Required for all prediction endpoints
4. **Rate limiting**: Prevents abuse and resource exhaustion
5. **Privacy by design**: No data retention by default

### Deployment Security
- **Self-hosted option**: No dependency on external services
- **Docker hardening**: Non-root user, minimal base image
- **Environment variables**: No secrets in code
- **CI/CD security scanning**: Dependencies, code quality

## Scalability Considerations

### Vertical Scaling
- **API**: FastAPI + Uvicorn workers (Gunicorn for production)
- **Database**: SQLite → PostgreSQL for high-volume
- **Model serving**: Multiple model versions in parallel

### Horizontal Scaling
- **Stateless API**: Can be deployed behind load balancer
- **Model inference**: CPU-bound, scales with replicas
- **Database**: Migrate to external database for multi-instance

## Development Workflow

### Local Development
```bash
# Setup
pip install -r requirements.txt
python3 api/services/db.py

# Run
PYTHONPATH=. uvicorn api.main:app --reload

# Test
PYTHONPATH=. pytest
```

### Production Deployment
```bash
# Docker
docker build -t phishing-detector .
docker run -p 8000:8000 -e API_KEY=your_key phishing-detector

# Docker Compose
docker-compose up --build
```

## Monitoring & Observability

### Metrics (Prometheus)
- `phishing_predictions_total`: Prediction counts by type
- `request_duration_seconds`: API latency
- `api_errors_total`: Error classification

### Logging (Structured JSON)
- Request metadata
- Prediction results (with PII redacted)
- Error traces
- Quota usage

## Integration Patterns

### Direct API Integration
```python
from phishing_detector import PhishingDetectorClient
client = PhishingDetectorClient(api_key="...")
result = client.check("https://example.com")
```

### Web Application Integration
- API key authentication
- Rate limiting based on user tiers
- Async predictions for high volume

### Security Tool Integration
- Real-time URL screening
- Batch processing
- Confidence thresholds for different risk profiles
