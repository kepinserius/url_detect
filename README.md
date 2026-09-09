# Phishing URL Detector

[![CI/CD](https://github.com/kepinserius/url_detect/actions/workflows/ci.yml/badge.svg)](https://github.com/kepinserius/url_detect/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![codecov](https://codecov.io/gh/kepinserius/url_detect/branch/main/graph/badge.svg)](https://codecov.io/gh/kepinserius/url_detect)
[![GitHub Release](https://img.shields.io/github/release/kepinserius/url_detect.svg)](https://github.com/kepinserius/url_detect/releases)

**Open-source phishing URL detection engine. Detect phishing URLs in milliseconds with 99.99% accuracy.**

[Overview](#overview) • [Features](#features) • [Quick Start](#quick-start) • [API](#api) • [Documentation](#documentation)

---

## Overview

Phishing URL Detector is an open-source Machine Learning platform for detecting phishing URLs. Built for developers who need:

- **Fast & accurate**: 99.99% F1 score on PhiUSIIL dataset
- **Self-hosted**: Run locally or in your own infrastructure
- **Enterprise-ready**: Authentication, rate limiting, quotas
- **Privacy-first**: No URL fetching, PII redaction built-in

### How It Works

```text
User Input (URL)
       ↓
Feature Extraction (22 URL features)
       ↓
XGBoost Model Prediction
       ↓
Result: phishing / legitimate + risk score
```

No URL fetching, no HTML analysis—just fast static URL analysis.

---

## Features

### Core Features
- ✅ **ML-based detection**: XGBoost classifier trained on 235K+ URLs
- ✅ **Static analysis only**: No auto-fetching (SSRF-safe)
- ✅ **REST API v1**: FastAPI-based with async support
- ✅ **Python SDK**: Easy integration in Python apps

### Security & Privacy
- ✅ **API authentication**: X-API-Key header
- ✅ **Rate limiting**: Per-IP & per-API-key quotas
- ✅ **PII redaction**: Tokens, passwords, emails auto-redacted in logs
- ✅ **No data retention**: URL submissions not stored by default

### Enterprise Features
- ✅ **Prometheus metrics**: Real-time observability
- ✅ **Structured logging**: JSON logs for SIEM integration
- ✅ **Model versioning**: Multi-model registry
- ✅ **Docker-ready**: Containerized deployment

### Developer Experience
- ✅ **Self-hosted**: Run with `docker-compose` or `pip install`
- ✅ **CI/CD**: GitHub Actions for automated testing
- ✅ **Testing suite**: Unit, integration, load tests
- ✅ **Comprehensive docs**: Architecture, API, deployment guides

---

## Quick Start

### Option 1: Local (Python)

```bash
# 1. Clone the repository
git clone https://github.com/kepinserius/url_detect.git
cd url_detect

# 2. Install dependencies
pip install -r requirements.txt

# 3. Initialize database
python3 api/services/db.py

# 4. Set API key (required for /v1/check)
export API_KEY="your_secure_api_key_here"

# 5. Run API server
PYTHONPATH=. uvicorn api.main:app --reload --port 8000
```

**API available at**: http://localhost:8000

### Option 2: Docker

```bash
# Build and run with Docker Compose
docker-compose up --build
```

**API available at**: http://localhost:8000

---

## API Usage

### 1. Health Check

```bash
curl http://localhost:8000/health
```

```json
{
  "status": "healthy"
}
```

### 2. Check URL for Phishing

```bash
curl -X POST http://localhost:8000/v1/check \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your_secure_api_key_here" \
  -d '{"url": "https://example.com/login"}'
```

```json
{
  "prediction": "legitimate",
  "risk_score": 4.5,
  "confidence": 0.955
}
```

### 3. Prometheus Metrics

```bash
curl http://localhost:8000/metrics
```

---

## Python SDK

### Install

```bash
pip install -e .
# or
pip install phishing-url-detector
```

### Usage

```python
from phishing_detector import PhishingDetectorClient

# Initialize client
client = PhishingDetectorClient(
    base_url="http://localhost:8000",
    api_key="your_api_key"
)

# Check URL
result = client.check("https://example.com")
print(f"Prediction: {result['prediction']}")
print(f"Risk Score: {result['risk_score']}%")
print(f"Confidence: {result['confidence']}")

# Health check
health = client.health()
print(f"API Status: {health['status']}")
```

---

## Model Performance

| Metric | Value |
|--------|-------|
| **F1 Score** | 0.9999 |
| **ROC-AUC** | 0.9999 |
| **Accuracy** | 100% |
| **Features** | 22 URL-based |
| **Inference Time** | <10ms |
| **Training Data** | 235,795 URLs |

*Trained on [PhiUSIIL Phishing URL Dataset](https://archive.ics.uci.edu/dataset/967/phiusiil+phishing+url+dataset)*

---

## Endpoints

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/health` | GET | ❌ | Health check |
| `/v1/check` | POST | ✅ | Check URL for phishing |
| `/metrics` | GET | ❌ | Prometheus metrics |
| `/docs` | GET | ❌ | Swagger UI (interactive API docs) |

---

## Configuration

Environment variables (`.env`):

```env
APP_ENV=development
API_V1_STR=/v1
PROJECT_NAME=Phishing URL Detector
MODEL_PATH=models/phishing_url_only_model.joblib
FEATURE_PATH=models/url_only_feature_names.joblib
API_KEY=your_api_key_here
```

---

## Testing

### Run Tests

```bash
# Unit & integration tests
PYTHONPATH=. pytest

# With coverage
PYTHONPATH=. pytest --cov=. --cov-report=html
```

### Load Testing

```bash
# Install Locust
pip install locust

# Run load test
locust -f tests/load/locustfile.py
```

---

## Documentation

- **[Architecture](docs/architecture.md)**: System design & component breakdown
- **[API Reference](docs/api.md)**: Full API documentation & examples
- **[Deployment](docs/deployment.md)**: Docker, Kubernetes, production guide
- **[Model](docs/model.md)**: Model details, features, performance
- **[Contributing](CONTRIBUTING.md)**: How to contribute
- **[Security](SECURITY.md)**: Security policies & vulnerability reporting

---

## Project Structure

```
url_detect/
├── api/                  # FastAPI application
│   ├── main.py          # App entry point
│   ├── routes/          # API routes (v1/)
│   ├── middleware/      # Auth, rate limiting, privacy
│   ├── schemas/         # Pydantic models
│   └── services/        # Logging, metrics, DB
├── inference/           # Prediction engine
│   ├── predictor.py     # Main predictor class
│   └── features/        # Feature extraction
├── models/              # ML models & registry
│   ├── phishing_url_only_model.joblib
│   ├── registry.json
│   └── evaluation_report.json
├── training/            # Model training pipeline
│   ├── train.py         # Full training script
│   ├── tune.py          # Hyperparameter tuning
│   └── preprocessing/   # Data cleaning
├── phishing_detector/   # Python SDK client
├── tests/               # Test suite
│   ├── unit/           # Unit tests
│   ├── integration/    # Integration tests
│   └── load/           # Load testing (Locust)
├── docs/                # Documentation
├── data/                # Dataset (external)
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── pyproject.toml       # Python packaging
��── .github/workflows/ci.yml
```

---

## Self-Hosting

### Docker

```bash
docker build -t phishing-detector .
docker run -p 8000:8000 -e API_KEY=your_key phishing-detector
```

### Kubernetes

See [Deployment Guide](docs/deployment.md) for Helm chart & K8s manifests.

---

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for:

- Reporting bugs
- Feature requests
- Pull request process
- Code style guide

---

## License

MIT License - See [LICENSE](LICENSE) for details.

Dataset: CC BY 4.0 - See [data/LICENSE.md](data/LICENSE.md)

---

## Citation

If you use this project in research, please cite:

```
@software{phishing_url_detector,
  title={Phishing URL Detector},
  author={kepinserius},
  year={2026},
  version={0.1.0},
  url={https://github.com/kepinserius/url_detect}
}
```

---

## Acknowledgments

- Dataset: [PhiUSIIL Phishing URL Dataset](https://archive.ics.uci.edu/dataset/967/phiusiil+phishing+url+dataset) (UCI ML Repository)
- Framework: [FastAPI](https://fastapi.tiangolo.com/), [XGBoost](https://xgboost.readthedocs.io/)

---

## Support

- 📝 **Documentation**: [See docs/](docs/)
- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/kepinserius/url_detect/issues)
- 🔒 **Security**: [Security Policy](SECURITY.md)
- 💬 **Questions**: [GitHub Discussions](https://github.com/kepinserius/url_detect/discussions)

---

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history.

---

**Made with ❤️ by the open-source community**
