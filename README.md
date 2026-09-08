# Open Source Phishing URL Detection Platform

An open-source phishing URL detection platform providing Machine Learning-based detection engine that can be trained, self-hosted, or consumed via REST API.

## Features

- **Static URL Analysis**: Analyzes URL features safely without making HTTP requests to submitted URLs.
- **REST API**: Built with FastAPI, providing `/health` and `/v1/check` endpoints.
- **Self-Hostable**: Easy deployment with Docker and Docker Compose.
- **API First Design**: Versioned endpoints with structured JSON response.

## Quick Start (Self-Hosting)

### Using Docker Compose

```bash
docker compose up -d
```

The API will be available at `http://localhost:8000`.

### Local Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the API server:
   ```bash
   uvicorn api.main:app --host 0.0.0.0 --port 8000
   ```

## API Usage Example

### Check URL

```bash
curl -X POST "http://localhost:8000/v1/check" \
     -H "Content-Type: application/json" \
     -d '{"url": "https://example.com"}'
```

Example Output:

```json
{
  "prediction": "legitimate",
  "risk_score": 5,
  "confidence": 0.95,
  "indicators": []
}
```

## Project Architecture

For detailed architecture and model documentation, see the `docs/` directory.

## License

MIT License - see [LICENSE](LICENSE) for details.
