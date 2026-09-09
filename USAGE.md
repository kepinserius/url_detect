# How to Use

## Prerequisites
- Python 3.9+
- Docker (optional, for containerized deployment)

## Local Development
1. Clone the repository:
   ```bash
   git clone https://github.com/kepinserius/phishing-url-detector.git
   cd phishing-url-detector
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the API:
   ```bash
   PYTHONPATH=. uvicorn api.main:app --reload
   ```

4. Check health:
   ```bash
   curl http://localhost:8000/health
   ```

5. Make a prediction:
   ```bash
   curl -X POST http://localhost:8000/v1/check \
     -H "Content-Type: application/json" \
     -H "X-API-Key: your_api_key" \
     -d '{"url": "https://example.com"}'
   ```

## Docker
```bash
docker build -t phishing-detector .
docker run -p 8000:8000 phishing-detector
```

## Configuration
Environment variables (`.env.example`):
- `API_KEY`: Your API key
- `MODEL_PATH`: Path to model file
- `APP_ENV`: `development` or `production`

## Available Endpoints
- `GET /health`: Health check
- `GET /metrics`: Prometheus metrics
- `POST /v1/check`: Check URL for phishing

## SDK Usage
```python
from phishing_detector import PhishingDetectorClient

client = PhishingDetectorClient(
    base_url="http://localhost:8000",
    api_key="your_api_key"
)

result = client.check("https://example.com")
print(result)
```

## Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Security
See [SECURITY.md](SECURITY.md) for security policies.
