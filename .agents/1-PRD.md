# PRD v1.1 - URL Detect Enhancement

## Visi & Tujuan

### Visi Produk
Mengembangkan URL Detect dari open-source phishing detection engine menjadi **platform enterprise-grade** yang siap untuk production, integrasi, dan scale.

### Tujuan Utama
1. **Akurasi >99%** - Dengan HTML content analysis & PhishTank integration
2. **Batch Processing** - Support 1000+ URLs per request
3. **Real-time Threat Intelligence** - Integrasi dengan PhishTank & OpenPhish
4. **Enterprise Ready** - Multi-tenant API, usage analytics, SLA monitoring

### Value Proposition
- Kombinasi **ML + Rules + Threat Intelligence** untuk akurasi maksimal
- **Batch processing** untuk throughput tinggi
- **Open-source** dengan enterprise features tanpa vendor lock-in
- **Self-hostable** dengan multi-tenant support

---

## User Persona

### Persona 1: Security Engineer (Internal)
- **Usia/Pekerjaan:** 25-35 tahun, Security Engineer di startup/enterprise
- **Level Teknis:** Mahir (Python, REST API, threat intelligence)
- **Tujuan:** Protect users dari phishing tanpa rely on third-party
- **Pain Points:** 
  - Akurasi ML tidak cukup untuk production
  - Perlu real-time threat data
  - Batch checking untuk bulk URLs
- **Motivasi:** Security internal yang bisa di-customize & self-host

### Persona 2: Developer (External)
- **Usia/Pekerjaan:** 22-30 tahun, Full-stack developer
- **Level Teknis:** Menengah-Mahir
- **Tujuan:** Integrate phishing detection ke aplikasi mereka
- **Pain Points:**
  - API lambat untuk single URL checking
  - Perlu data akurat untuk user trust
  - Butuh dokumentasi yang jelas
- **Motivasi:** Add security feature ke product mereka dengan cepat

---

## User Stories

### Modul 1: Enhanced Detection
- Sebagai security engineer, saya ingin HTML content analysis, agar bisa detect phishing lebih akurat.
- Sebagai security engineer, saya ingin PhishTank integration, agar update ancaman terkini.
- Sebagai developer, saya ingin batch checking (100+ URLs), agar efisien untuk data processing.
- Sebagai developer, saya ingin confidence score breakdown, agar tahu alasan detection.
- Sebagai developer, saya ingin indicators (penjelasan mengapa phishing), agar transparan.

### Modul 2: Enterprise Features
- Sebagai enterprise user, saya ingin multi-tenant API keys, agar bisa manage banyak client.
- Sebagai enterprise user, saya ingin usage analytics, agar bisa monitor quota & traffic.
- Sebagai enterprise user, saya ingin SLA monitoring, agar tahu uptime & performance.
- Sebagai enterprise user, saya ingin rate limiting per tenant, agar fair usage.

### Modul 3: Developer Experience
- Sebagai developer, saya ingin browser extension template, agar cepat buat extension.
- Sebagai developer, saya ingin Python SDK dengan fitur baru, agar mudah pakai batch.
- Sebagai developer, saya ingin documentation lengkap untuk setiap fitur, agar cepat integrate.
- Sebagai developer, saya ingin examples untuk use case umum, agar cepat start.

*(Total 13 user stories)*

---

## Functional Requirements

### Modul 1: Enhanced Detection Engine

**FR-01: HTML Content Analysis (Optional)**
- **Input:** URL (dengan flag `fetch_content: true`)
- **Proses:** Safe fetch HTML dengan timeout 5s, extract title, links, forms, meta tags
- **Output:** Features tambahan untuk model, indicators list
- **Aturan:** Max 100KB response, timeout 5s, block internal IPs

**FR-02: PhishTank Integration**
- **Input:** URL
- **Proses:** Query PhishTank API (v2), cache response 1 hour
- **Output:** PhishTank report (verified/unverified), confidence boost
- **Aturan:** Free API key required, fallback jika offline

**FR-03: Batch Processing API**
- **Input:** Array of URLs (max 1000)
- **Proses:** Parallel checking (concurrent limit 50), return array of results
- **Output:** Array of predictions dengan timing info
- **Aturan:** Max 1000 URLs/request, rate limit 10 req/min

**FR-04: Prediction Indicators**
- **Input:** URL + prediction result
- **Proses:** Generate explainable indicators (rule-based)
- **Output:** List of indicators (e.g., "suspicious TLD", "typosquatting detected")
- **Aturan:** Max 5 indicators, relevance threshold 0.6

**FR-05: Confidence Score Breakdown**
- **Input:** Prediction result
- **Proses:** Show contribution per source (ML: 0.7, Rules: 0.2, Threat Intel: 0.1)
- **Output:** Score breakdown JSON
- **Aturan:** Total 1.0, handle missing sources

### Modul 2: Enterprise Features

**FR-06: Multi-Tenant API Keys**
- **Input:** API key
- **Proses:** Lookup tenant from key, track usage per tenant
- **Output:** Tenant metadata, quota info
- **Aturan:** API keys stored in DB, tier-based quotas

**FR-07: Usage Analytics**
- **Input:** API requests
- **Proses:** Aggregate metrics per tenant (requests/day, avg latency, errors)
- **Output:** Daily reports, exportable CSV
- **Aturan:** Anonymize tenant ID, retention 30 days

**FR-08: SLA Monitoring**
- **Input:** Request/response data
- **Proses:** Track uptime, latency p95, error rate
- **Output:** SLA dashboard (endpoint: /v1/sla)
- **Aturan:** Uptime target 99.5%, alert if < 99%

**FR-09: Per-Tenant Rate Limiting**
- **Input:** API key + request
- **Proses:** Check quota per tenant (free: 100/day, pro: 10K/day)
- **Output:** Rate limit headers, 429 response jika exceed
- **Aturan:** Quota reset daily, grace period 10%

**FR-10: Tenant Management API**
- **Input:** Admin API key
- **Proses:** CRUD operations untuk tenants
- **Output:** Tenant management responses
- **Aturan:** Admin only, audit logs

### Modul 3: Developer Experience

**FR-11: Browser Extension Template**
- **Input:** N/A (template code)
- **Proses:** Generate Chrome/Firefox extension scaffold
- **Output:** GitHub repo template, documentation
- **Aturan:** MIT license, customizable

**FR-12: Enhanced Python SDK**
- **Input:** API calls
- **Proses:** SDK with batch support, async, error handling
- **Output:** Clean Python API
- **Aturan:** Backward compatible, docstrings

**FR-13: Example Use Cases**
- **Input:** N/A (docs)
- **Proses:** Tutorials untuk browser ext, email filter, web app
- **Output:** Code examples di docs
- **Aturan:** Python/JS examples, tested

---

## Non-Functional Requirements

### Performa
- Batch API: < 2 detik untuk 100 URLs
- Single URL: < 100ms (p95)
- PhishTank cache: < 10ms
- HTML fetch timeout: 5s max
- Concurrent requests: 50+ parallel

### Keamanan
- HTML fetch: block internal IPs (10.x.x.x, 192.168.x.x, 127.0.0.1)
- API keys: hashed (bcrypt)
- Rate limiting: per tenant + global
- Auth: API key required untuk semua /v1/* endpoints

### Skalabilitas
- Single instance: 100 requests/sec
- Multi-instance: Load balancer ready
- Database: PostgreSQL support (selain SQLite)

### Usability
- Documentation: Lengkap dengan diagrams
- Error messages: Clear & actionable
- Versioning: /v1/, /v2/ dengan deprecation warning

---

## Out of Scope & Dependensi

### Out of Scope (V1.1)
- UI Dashboard (khusus enterprise)
- Mobile app
- Custom model training UI
- API marketplace monetization
- Real-time phishing block (web proxy)

### Dependensi
- **PhishTank API:** Free API untuk threat intelligence
- **tldextract:** Untuk domain parsing (sudah di requirements.txt)
- **requests:** Untuk HTTP calls (sudah ada)
- **asyncio:** Untuk batch processing (Python 3.11+)
- **PostgreSQL (opsional):** Untuk production multi-tenant

### Asumsi
- User punya akses ke PhishTank API (free)
- User bisa deploy database (SQLite default, PostgreSQL optional)
- HTML content fetch optional (user aktifkan via flag)
