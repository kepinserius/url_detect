# Tasks v1.1 - URL Detect Enhancement

## Priority: High

### Setup Project (Project sudah ada, skip)
*Skip karena project v1.0 sudah ada*

---

### Modul 1: PhishTank Integration

**T-01: Create PhishTank Service**
- **Deskripsi:** Implement client untuk PhishTank API dengan caching
- **Prioritas:** High
- **Status:** Todo
- **Dependensi:** -
- **Files:** `app/api/services/phishTank.py`
- **Estimasi:** 3 jam

**T-02: Add PhishTank Cache Model**
- **Deskripsi:** SQLAlchemy model untuk PhishTankCache table
- **Prioritas:** High
- **Status:** Todo
- **Dependensi:** T-01
- **Files:** `app/models/__init__.py`
- **Estimasi:** 1 jam

**T-03: Implement PhishTank API Route**
- **Deskripsi:** Endpoint `/v1/phishTank/{url_hash}` untuk check threat intel
- **Prioritas:** High
- **Status:** Todo
- **Dependensi:** T-01, T-02
- **Files:** `app/api/routes/phishTank.py`
- **Estimasi:** 2 jam

---

### Modul 2: Batch Processing

**T-04: Create Batch Processing Route**
- **Deskripsi:** Endpoint `/v1/batch` untuk check 1000+ URLs
- **Prioritas:** High
- **Status:** Todo
- **Dependensi:** -
- **Files:** `app/api/routes/batch.py`
- **Estimasi:** 4 jam

**T-05: Implement Parallel Processing**
- **Deskripsi:** Worker pool dengan asyncio (max 50 concurrent)
- **Prioritas:** High
- **Status:** Todo
- **Dependensi:** T-04
- **Files:** `app/api/services/batch_processor.py`
- **Estimasi:** 3 jam

---

### Modul 3: HTML Content Analysis

**T-06: Create HTML Fetcher Service**
- **Deskripsi:** Safe HTML fetch dengan timeout, size limit, IP block
- **Prioritas:** High
- **Status:** Todo
- **Dependensi:** -
- **Files:** `app/api/services/html_fetcher.py`
- **Estimasi:** 3 jam

**T-07: Add HTML Features to Extractor**
- **Deskripsi:** Ekstraksi features dari HTML (title, links, forms, etc)
- **Prioritas:** High
- **Status:** Todo
- **Dependensi:** T-06
- **Files:** `inference/features/advanced_extractor.py`
- **Estimasi:** 3 jam

---

### Modul 4: Prediction Indicators

**T-08: Create Indicators Service**
- **Deskripsi:** Generate explainable indicators untuk predictions
- **Prioritas:** High
- **Status:** Todo
- **Dependensi:** -
- **Files:** `app/api/services/indicators.py`
- **Estimasi:** 2 jam

**T-09: Add Indicators Route**
- **Deskripsi:** Endpoint `/v1/indicators/{url_hash}` untuk explanation
- **Prioritas:** High
- **Status:** Todo
- **Dependensi:** T-08
- **Files:** `app/api/routes/indicators.py`
- **Estimasi:** 2 jam

---

### Modul 5: Multi-Tenant Support

**T-10: Create Tenant Database Model**
- **Deskripsi:** SQLAlchemy model untuk tenants table
- **Prioritas:** High
- **Status:** Todo
- **Dependensi:** -
- **Files:** `app/models/database.py`
- **Estimasi:** 2 jam

**T-11: Implement Tenant API Routes**
- **Deskripsi:** CRUD endpoints untuk tenant management
- **Prioritas:** High
- **Status:** Todo
- **Dependensi:** T-10
- **Files:** `app/api/routes/tenant.py`
- **Estimasi:** 3 jam

**T-12: Update Auth Middleware**
- **Deskripsi:** Support multi-tenant quota per API key
- **Prioritas:** High
- **Status:** Todo
- **Dependensi:** T-10
- **Files:** `app/api/middleware/auth.py`
- **Estimasi:** 2 jam

---

### Modul 6: SLA Monitoring

**T-13: Create SLA Dashboard Endpoint**
- **Deskripsi:** `/v1/sla` untuk uptime & performance metrics
- **Prioritas:** Medium
- **Status:** Todo
- **Dependensi:** -
- **Files:** `app/api/routes/sla.py`
- **Estimasi:** 2 jam

---

### Tests & Documentation

**T-14: Write Integration Tests**
- **Deskripsi:** Tests untuk batch, phishTank, indicators
- **Prioritas:** High
- **Status:** Todo
- **Dependensi:** All implementation tasks
- **Files:** `tests/integration/`
- **Estimasi:** 4 jam

**T-15: Update Documentation**
- **Deskripsi:** Update README, docs dengan fitur baru
- **Prioritas:** Medium
- **Status:** Todo
- **Dependensi:** -
- **Files:** `README.md`, `docs/*.md`
- **Estimasi:** 3 jam

---

## Priority: Low

**T-16: Redis Caching (Optional)**
- **Deskripsi:** Add Redis untuk cache performance
- **Prioritas:** Low
- **Status:** Todo
- **Dependensi:** -
- **Files:** `app/api/services/cache.py`
- **Estimasi:** 2 jam

---

## Summary

- **Total Tasks:** 16
- **High Priority:** 12
- **Medium Priority:** 3
- **Low Priority:** 1
- **Estimated Time:** ~40 jam

---

## Implementation Order

1. T-01 → T-02 → T-03 (PhishTank)
2. T-04 → T-05 (Batch)
3. T-06 → T-07 (HTML Analysis)
4. T-08 → T-09 (Indicators)
5. T-10 → T-11 → T-12 (Multi-tenant)
6. T-13 (SLA)
7. T-14 → T-15 (Tests & Docs)
8. T-16 (Redis - optional)
