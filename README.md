# URL Detect API

Open-source phishing URL detection platform with enhanced features for v1.1.

## Features

### Core
- ML-based phishing detection (99.99% accuracy on PhiUSIIL)
- Hybrid detection (ML + Rules + Threat Intel)
- REST API v1 with FastAPI
- Self-hosted with Docker

### New in v1.1
- **Batch Processing**: Check 1000+ URLs in parallel
- **PhishTank Integration**: Real-time threat intelligence
- **HTML Content Analysis**: Optional safe HTML fetching
- **Prediction Indicators**: Human-readable explanations
- **Multi-tenant Support**: Enterprise-ready API management
- **SLA Monitoring**: Uptime and performance tracking

## Quick Start

### Docker
```bash
git clone https://github.com/kepinserius/url_detect.git
cd url_detect
docker-compose up --build
```

### Local (Python)
```bash
pip install -r requirements.txt
PYTHONPATH=. uvicorn app.main:app --reload --port 8000
```

## API Usage

### Health Check
```bash
curl http://localhost:8000/health
```

### Single URL Check
```bash
curl -X POST http://localhost:8000/v1/check \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your_api_key" \
  -d '{"url": "https://example.com"}'
```

### Batch Check (1000+ URLs)
```bash
curl -X POST http://localhost:8000/v1/batch \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your_api_key" \
  -d '{"urls": ["https://url1.com", "https://url2.com", ...]}'
```

### Prediction Explanation
```bash
curl -X POST http://localhost:8000/v1/indicators \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your_api_key" \
  -d '{"url": "https://example.com"}'
```

### PhishTank Threat Intel
```bash
curl -X POST http://localhost:8000/v1/phishTank/check \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your_api_key" \
  -d '{"url": "https://example.com"}'
```

## Python SDK

```python
from phishing_detector import PhishingDetectorClient

client = PhishingDetectorClient(
    base_url="http://localhost:8000",
    api_key="your_api_key"
)

# Single check
result = client.check("https://example.com")

# Batch check
results = client.batch([
    "https://url1.com",
    "https://url2.com"
])
```

## Environment Variables

```env
APP_ENV=development
API_V1_STR=/v1
PROJECT_NAME=URL Detect
MODEL_PATH=models/phishing_improved_model.joblib
FEATURE_PATH=models/improved_feature_names.joblib
API_KEY=your_api_key_here
PHISHTANK_API_KEY=your_phishtank_key  # Optional
REDIS_URL=redis://localhost:6379      # Optional
```

## Database

### SQLite (Default)
No configuration needed. Database created automatically.

### PostgreSQL (Production)
```env
DATABASE_URL=postgresql://user:pass@localhost:5432/url_detect
```

## Documentation

- **[API Reference](http://localhost:8000/docs)**: Interactive Swagger UI
- **[Tech Spec](.agents/2-TECH-SPEC.md)**: Technical architecture
- **[PRD](.agents/1-PRD.md)**: Product requirements
- **[Tasks](.agents/3-TASKS.md)**: Implementation tasks

## Performance

- Single URL: < 50ms (p95)
- Batch 100 URLs: < 200ms (p95)
- Batch 1000 URLs: < 1500ms (p95)
- Concurrency: 50+ parallel workers

## Testing

```bash
PYTHONPATH=. pytest
```

## License

MIT License - See [LICENSE](LICENSE) for details.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.
