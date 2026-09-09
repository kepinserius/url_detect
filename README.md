# Phishing URL Detector

Open-source phishing URL detection platform berbasis Machine Learning, siap untuk skala enterprise.

## Fitur Inti
- Deteksi cepat berbasis fitur statis (tanpa visit URL).
- REST API v1 dengan FastAPI, support versi enterprise.
- Authentication via API keys dengan rate limiting.
- Observabilitas lengkap: Log terstruktur, metrik Prometheus.
- Self-hosting dengan Docker dan Kubernetes-ready.
- Model XGBoost terlatih dengan dataset PhiUSIIL, model versioning registry.

## Fitur Enterprise
- **API Authentication & Authorization**: X-API-Key header.
- **Rate Limiting & Quota Management**: Database-based multi-tenant quotas.
- **Privacy First**: Redaksi otomatis PII dari URL.
- **Observability**: Prometheus metrics endpoint `/metrics`.
- **Structured Logging**: JSON logs dengan sanitasi sensitif.
- **Load Testing Ready**: Script Locust untuk stress testing.
- **Model Registry**: Version tracking dengan metadata.
- **Database-backed**: SQLite untuk API key dan quotas.

## Quick Start (Local)
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Inisialisasi database enterprise:
   ```bash
   python3 api/services/db.py
   ```
3. Jalankan API:
   ```bash
   PYTHONPATH=. uvicorn api.main:app --reload
   ```

## Quick Start (Docker)
```bash
docker-compose up --build
```

## API Usage (Basic)
Cek URL:
```bash
curl -X POST http://localhost:8000/v1/check \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your_api_key_here" \
  -d '{"url": "https://example.com"}'
```

## Observability
- Health check: `GET /health`
- Prometheus metrics: `GET /metrics`
- Auto-redaction: Token, password, email dalam logs.

## Testing
Run unit & integration tests:
```bash
PYTHONPATH=. pytest
```

Load testing (Locust):
```bash
locust -f tests/load/locustfile.py
```

## Struktur Projek
- `api/`: Kode sumber FastAPI, routes, middleware, services.
- `inference/`: Engine prediksi dan ekstraksi fitur.
- `models/`: Artifact model (.joblib), registry, enterprise database.
- `training/`: Skrip pelatihan model.
- `phishing_detector/`: Python SDK client.
- `tests/`: Unit, integration, load tests.
- `docs/`: Dokumentasi arsitektur dan API.
