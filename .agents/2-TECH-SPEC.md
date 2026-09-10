# Tech Spec v1.1 - URL Detect Enhancement

## Tech Stack & Arsitektur

### Tech Stack
| Layer | Technology | Version |
|-------|------------|---------|
| Backend | FastAPI | 0.110.0+ |
| Language | Python | 3.11+ |
| Database | SQLite | Built-in |
| ORM | SQLAlchemy | 2.0+ |
| Authentication | JWT + API Keys | PyJWT |
| Caching | Redis (optional) | 7.x |
| Hosting | Docker + Docker Compose | Latest |

### Arsitektur Sistem
```
┌─────────────┐
│   Client    │
│ (Browser/   │
│  App/SDK)   │
└──────┬──────┘
       │ HTTPS
       ▼
┌─────────────────────────────────────────────────────┐
│              FastAPI Application                    │
├─────────────────────────────────────────────────────┤
│  • v1/check (single URL)                            │
│  • v1/batch (1000+ URLs)                            │
│  • v1/health                                        │
│  • v1/metrics (Prometheus)                          │
│  • v1/indicators (explanation)                      │
│  • v1/phishTank (threat intel)                      │
│  • v1/tenant/* (multi-tenant, admin only)          │
│  • v1/sla (monitoring)                              │
└───────────────────────┬─────────────────────────────┘
                        │
        ┌───────────────┴───────────────┐
        ▼                               ▼
┌──────────────────┐         ┌─────────────────────┐
│   SQLite/        │         │   External API      │
│   PostgreSQL     │         │   PhishTank API     │
│   (Local)        │         │   (Cache 1hr)       │
└──────────────────┘         └─────────────────────┘
```

### Struktur Folder
```
url_detect/
├── app/
│   ├── api/
│   │   ├── routes/
│   │   │   ├── v1.py              # Main v1 endpoints
│   │   │   ├── batch.py           # Batch processing
│   │   │   ├── indicators.py      # Explanation API
│   │   │   ├── phishTank.py       # Threat intel
│   │   │   └── tenant.py          # Multi-tenant
│   │   ├── middleware/
│   │   │   ├── auth.py
│   │   │   ├── rate_limit.py
│   │   │   └── quota.py
│   │   ├── schemas/
│   │   │   ├── request.py
│   │   │   └── response.py
│   │   └── services/
│   │       ├── phishTank.py       # PhishTank client
│   │       ├── html_fetcher_async.py  # Safe HTML fetch
│   │       ├── indicators.py      # Indicators service
│   │       └── metrics.py         # Prometheus metrics
│   ├── models/
│   │   ├── __init__.py
│   │   └── database.py            # DB connection
│   ├── core/
│   │   ├── config.py
│   │   ├── exceptions.py
│   │   └── utils.py
│   ├── main.py
├── inference/
│   ├── hybrid_predictor.py
│   ├── features/
│   └── rules/
├── tests/
│   ├── unit/
│   ├── integration/
│   └── load/
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

---

## Database Design

### Ringkasan Database
| Item | Detail |
|------|--------|
| Database | SQLite (primary), PostgreSQL (optional) |
| ORM | SQLAlchemy 2.0 |
| Pendekatan | Relational |
| Tools Migrasi | Alembic (PostgreSQL only) |

### Entity Overview

**Tenant (multi-tenant support)**
- id: INTEGER, Primary key
- name: VARCHAR(100)
- api_key: VARCHAR(64) - SHA256 hash
- tier: VARCHAR(20) - free/pro/enterprise
- quota_daily: INTEGER
- created_at, updated_at: TIMESTAMP

**RequestLog (audit logging)**
- id: INTEGER
- url_hash: VARCHAR(64) - SHA256 of URL
- prediction: VARCHAR(20)
- risk_score: FLOAT
- confidence: FLOAT
- tenant_id: INTEGER (FK)
- created_at: TIMESTAMP

**PhishTankCache (threat intel caching)**
- url_hash: VARCHAR(64) - Primary key
- result: TEXT - JSON response
- expires_at: TIMESTAMP
- created_at: TIMESTAMP

---

## Interface Design

### API Endpoints v1

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| GET | /health | Health check | ❌ |
| POST | /v1/check | Single URL check | ✅ API Key |
| POST | /v1/batch | Batch check (max 1000) | ✅ API Key |
| GET | /v1/indicators | Prediction explanation | ✅ API Key |
| POST | /v1/phishTank/check | PhishTank status | ✅ API Key |
| GET | /v1/metrics | Prometheus metrics | ❌ |
| GET | /v1/tenant/{id} | Get tenant info | ✅ Admin |
| POST | /v1/tenant | Create tenant | ✅ Admin |
| GET | /v1/sla | SLA dashboard | ✅ Admin |

---

## Alur Logika & Business Rules

### Alur 1: Single URL Check
User → Auth → Quota → HTML Fetch (optional) → ML → PhishTank → Combine → Log

### Alur 2: Batch Processing
Batch Request → Validate → Parallel Queue (50 workers) → Process Each → Aggregate → Return

### Business Rules
1. URL Validation: no internal IPs, timeout 5s
2. HTML Fetch: safe fetching, max 100KB
3. PhishTank Cache: cache 1 hour
4. Score Combination: ML(70%) + Rules(20%) + ThreatIntel(10%)
5. Rate Limiting: 100 req/min per IP, 1000 req/min per API key
6. Privacy: URL not stored, only hash

---

## Keamanan, Performa, & Deployment

### Keamanan
- API Authentication: X-API-Key header
- Rate Limiting: per API key + global
- Quota Management: daily limit per tenant
- URL Validation: block internal IPs
- PII Redaction: query params di-redact
- SQL Injection: SQLAlchemy ORM

### Performa
- Single URL: < 50ms (p95)
- Batch 100 URLs: < 200ms (p95)
- Batch 1000 URLs: < 1500ms (p95)
- Concurrency: 50+ parallel workers

### Deployment
**Local:**
```bash
PYTHONPATH=. uvicorn app.main:app --reload
```

**Docker:**
```bash
docker-compose up --build
```

---

## Next Steps

1. Implement PhishTank client
2. Implement Batch Processing
3. Implement HTML Fetcher
4. Implement Multi-Tenant DB
5. Add Redis caching (optional)