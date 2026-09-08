# AGENTS.md

# Open Source Phishing URL Detection Platform

## 1. Project Identity

Project ini adalah **open-source phishing URL detection platform** yang bertujuan menyediakan sistem deteksi phishing berbasis Machine Learning yang dapat:

1. Dilatih menggunakan dataset phishing URL.
2. Digunakan sebagai inference engine.
3. Dijalankan secara lokal.
4. Di-self-host oleh developer atau organisasi lain.
5. Digunakan melalui REST API.
6. Diintegrasikan ke project pihak ketiga.
7. Dikembangkan oleh komunitas open-source.
8. Pada tahap lanjut, disediakan sebagai public hosted API.

Project harus diperlakukan sebagai **software product**, bukan hanya eksperimen Machine Learning atau notebook penelitian.

---

# 2. Core Vision

Visi project:

> Menyediakan phishing URL detection engine yang open-source, mudah digunakan, dapat di-self-host, dan dapat diintegrasikan ke berbagai aplikasi melalui API.

Developer yang menemukan repository ini harus dapat:

```text
Clone Repository
       ↓
Install Dependencies
       ↓
Download / Prepare Model
       ↓
Run API
       ↓
Send URL
       ↓
Receive Prediction
```

Tanpa harus memahami seluruh proses Machine Learning terlebih dahulu.

---

# 3. Open Source Philosophy

Project harus tetap dapat digunakan oleh pihak lain secara mandiri.

Ada dua mode penggunaan utama:

## A. Self-hosted

Developer dapat menjalankan seluruh sistem sendiri:

```text
Developer
    ↓
GitHub Repository
    ↓
Docker / Local Installation
    ↓
Phishing Detection API
    ↓
ML Model
```

Tidak boleh ada ketergantungan wajib terhadap server milik project owner untuk fungsi inti.

---

## B. Hosted Public API

Project juga dirancang agar nantinya dapat menyediakan:

```text
https://api.example.com
```

sehingga developer lain dapat menggunakan sistem tanpa menjalankan model sendiri.

```text
Third-party Application
        │
        │ HTTPS
        ▼
Public API
        │
        ▼
ML Inference Engine
        │
        ▼
Phishing Prediction
```

Hosted API adalah **deployment/service layer**, sedangkan ML engine tetap menjadi bagian dari open-source project.

---

# 4. Separation Between Open Source and Hosted Service

Project harus memisahkan:

### Open Source Core

Berisi:

* Feature extraction
* Data preprocessing
* ML pipeline
* Model inference
* Prediction logic
* API implementation
* Validation
* Testing
* Docker configuration
* Documentation

### Hosted Service

Dapat memiliki:

* API authentication
* API keys
* Rate limiting
* Usage tracking
* Request quotas
* Abuse prevention
* Monitoring
* Analytics
* Billing/subscription jika suatu saat diperlukan

Hosted service tidak boleh membuat core detection engine menjadi closed-source hanya karena API-nya hosted.

---

# 5. Target Users

Project ditujukan untuk:

* Software developers
* Cybersecurity researchers
* Security engineers
* Students
* Open-source contributors
* Startups
* Small businesses
* Developers building security products
* Developers building browser extensions
* Developers building messaging security systems
* Developers building email security systems

Use case yang memungkinkan:

```text
Web Application
Browser Extension
Email Security
Chat Security
WhatsApp-related Security System
SOC Tools
Security Dashboard
Fraud Prevention
Threat Intelligence Platform
```

---

# 6. Main Use Case

Input:

```json
{
  "url": "https://example.com/login"
}
```

Output:

```json
{
  "prediction": "phishing",
  "risk_score": 94,
  "confidence": 0.94
}
```

Developer lain harus dapat mengintegrasikan API tersebut ke aplikasi mereka tanpa perlu mengetahui detail internal model.

---

# 7. API-First Design

API harus dirancang sebagai **public developer API**, bukan hanya endpoint internal untuk frontend.

API harus memiliki:

* Versioning
* Stable request schema
* Stable response schema
* Error handling
* Authentication support
* Rate limiting support
* Documentation
* OpenAPI specification
* Health endpoint
* Predict endpoint

Initial API:

```http
GET /health
```

```http
POST /v1/check
```

atau:

```http
POST /v1/predict
```

Gunakan prefix versioning:

```text
/v1/
```

agar API dapat berkembang tanpa langsung merusak integration pihak ketiga.

---

# 8. API Compatibility

Setelah API publik digunakan oleh pihak lain:

> Jangan mengubah request/response structure secara breaking tanpa menaikkan API version.

Contoh:

```text
/v1/check
```

tidak boleh tiba-tiba berubah menjadi format yang tidak kompatibel.

Untuk breaking changes:

```text
/v2/check
```

API lama harus tetap dipertahankan selama periode migrasi yang wajar jika project sudah memiliki pengguna.

---

# 9. Example Third-party Usage

Developer lain harus dapat melakukan:

```bash
curl -X POST \
  https://api.example.com/v1/check \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer API_KEY" \
  -d '{"url":"https://example.com"}'
```

Python:

```python
import requests

response = requests.post(
    "https://api.example.com/v1/check",
    headers={
        "Authorization": "Bearer API_KEY"
    },
    json={
        "url": "https://example.com"
    }
)

print(response.json())
```

JavaScript/TypeScript:

```typescript
const response = await fetch(
  "https://api.example.com/v1/check",
  {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": "Bearer API_KEY"
    },
    body: JSON.stringify({
      url: "https://example.com"
    })
  }
);

const result = await response.json();
```

Contoh di atas adalah target developer experience.

---

# 10. SDK

Jika API sudah stabil, project dapat menyediakan official SDK.

Target:

```text
Python
JavaScript / TypeScript
Go
```

Contoh:

```python
from phishing_detector import Client

client = Client(api_key="API_KEY")

result = client.check(
    "https://example.com"
)

print(result.prediction)
```

SDK harus menggunakan public API dan tidak boleh menduplikasi business logic yang tidak diperlukan.

---

# 11. Self-hosting

Self-hosting adalah fitur penting.

Developer harus dapat menjalankan:

```bash
docker compose up
```

kemudian:

```text
localhost:8000
```

dan melakukan:

```http
POST /v1/check
```

Self-hosted deployment tidak boleh membutuhkan API key dari hosted service untuk melakukan inference lokal.

---

# 12. Project Architecture

Target architecture:

```text
                        OPEN SOURCE REPOSITORY
                                  │
              ┌───────────────────┴──────────────────┐
              │                                      │
              ▼                                      ▼
       Training Pipeline                       Inference Engine
              │                                      │
              ▼                                      ▼
         ML Dataset                             Feature Extractor
              │                                      │
              ▼                                      ▼
         Model Training                            Model
              │                                      │
              ▼                                      ▼
        Model Artifact                         Prediction
                                                     │
                                                     ▼
                                               REST API
                                                     │
                              ┌──────────────────────┴─────────────────────┐
                              │                                            │
                              ▼                                            ▼
                         Self Hosted                              Public Hosted API
                              │                                            │
                              ▼                                            ▼
                     Developer Project                          Third-party Project
```

---

# 13. Recommended Repository Structure

```text
phishing-url-detector/
│
├── AGENTS.md
├── README.md
├── LICENSE
├── CONTRIBUTING.md
├── SECURITY.md
├── CODE_OF_CONDUCT.md
├── CHANGELOG.md
│
├── docs/
│   ├── architecture.md
│   ├── api.md
│   ├── self-hosting.md
│   ├── model.md
│   └── development.md
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── README.md
│
├── training/
│   ├── notebooks/
│   ├── preprocessing/
│   ├── features/
│   ├── models/
│   └── train.py
│
├── inference/
│   ├── features/
│   ├── model/
│   └── predictor.py
│
├── api/
│   ├── main.py
│   ├── routes/
│   ├── schemas/
│   ├── middleware/
│   └── services/
│
├── tests/
│   ├── unit/
│   ├── integration/
│   └── api/
│
├── models/
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .env.example
```

---

# 14. Dataset

Initial dataset:

**PhiUSIIL Phishing URL Dataset**

Source:

UCI Machine Learning Repository.

Dataset label mapping must always be verified before training.

Do not assume label mappings from another phishing dataset.

Dataset itself should not automatically be committed to Git if its size or license makes that inappropriate.

Instead provide instructions for downloading/preparing it.

---

# 15. Machine Learning Pipeline

Training pipeline:

```text
Dataset
   ↓
Data Validation
   ↓
Data Cleaning
   ↓
EDA
   ↓
Feature Engineering
   ↓
Feature Selection
   ↓
Train / Validation / Test Split
   ↓
Preprocessing
   ↓
Model Training
   ↓
Cross Validation
   ↓
Hyperparameter Tuning
   ↓
Evaluation
   ↓
Model Selection
   ↓
Model Serialization
```

Initial models:

* Logistic Regression
* Decision Tree
* Random Forest
* XGBoost

Additional models may be added after baseline evaluation.

---

# 16. Model Evaluation

Do not evaluate using accuracy alone.

Required metrics:

* Precision
* Recall
* F1-score
* ROC-AUC
* PR-AUC
* Confusion Matrix
* False Positive Rate
* False Negative Rate

Special attention must be given to:

```text
False Negative
```

because:

```text
Actual phishing
       ↓
Model predicts legitimate
       ↓
Security failure
```

However, excessive false positives are also undesirable.

---

# 17. Model Versioning

Models must be versioned independently from the API.

Example:

```text
Model:
phishing-url-xgb

Version:
1.0.0
```

Future:

```text
1.1.0
2.0.0
```

Metadata should include:

```json
{
  "model_name": "phishing-url-xgb",
  "model_version": "1.0.0",
  "dataset": "PhiUSIIL",
  "features": [],
  "metrics": {},
  "training_date": "",
  "random_state": 42
}
```

Never fabricate model metrics or metadata.

---

# 18. Model Update Strategy

Because phishing techniques change over time, the model must be designed to be replaceable.

Do not tightly couple:

```text
API
```

with:

```text
specific model file
```

Instead:

```text
API
 ↓
Inference Interface
 ↓
Model Version
 ↓
Model Artifact
```

This allows future model replacement without rewriting the API.

---

# 19. Security Requirements

The project analyzes potentially malicious URLs.

The initial system must use **static URL analysis**.

Do NOT automatically request or visit arbitrary URLs submitted by users.

Avoid:

```python
requests.get(user_url)
```

unless a dedicated and securely isolated URL-analysis subsystem is explicitly implemented.

Potential risks include:

* SSRF
* DNS rebinding
* malicious redirects
* internal network access
* resource exhaustion
* malicious payloads

The initial ML model should work from URL-derived features without visiting the target website.

---

# 20. Public API Security

The hosted API should eventually support:

### Authentication

```text
API Key
```

### Rate limiting

Example:

```text
Free:
100 requests/day

Developer:
10,000 requests/month
```

Exact limits are deployment decisions and must not be hardcoded into the core engine.

### Abuse prevention

The hosted service must protect itself from:

* Automated abuse
* Excessive requests
* Resource exhaustion
* Credential abuse
* Malformed requests

These protections belong primarily in the hosted service layer.

---

# 21. Privacy

The API should minimize data retention.

URL submissions may potentially contain sensitive information in:

```text
Query parameters
Tokens
IDs
Email addresses
Tracking parameters
```

Therefore:

* Do not log complete URLs by default.
* Avoid storing URLs unnecessarily.
* Sanitize logs.
* Document retention policy.
* Do not expose submitted URLs to other users.
* Never store API keys in plaintext logs.

If request logging is necessary, prefer redacted or hashed identifiers where appropriate.

---

# 22. Explainability

The API may provide indicators such as:

```json
{
  "prediction": "phishing",
  "risk_score": 91,
  "indicators": [
    "unusually long URL",
    "suspicious domain structure",
    "high number of special characters"
  ]
}
```

Indicators must be generated from actual features/model analysis.

Never fabricate reasons for a prediction.

---

# 23. Developer Experience

A new developer should be able to understand the project quickly.

README should contain:

```text
What is this?
Quick Start
API Usage
Self-hosting
Docker
Python Usage
JavaScript Usage
Model Information
Contributing
Security
License
```

Quick start should ideally be:

```bash
git clone ...
cd phishing-url-detector
docker compose up
```

Then:

```bash
curl ...
```

---

# 24. Documentation

Documentation must explain:

1. Project purpose
2. Architecture
3. ML pipeline
4. Dataset
5. Model
6. API
7. Self-hosting
8. Security
9. Privacy
10. Contribution process
11. License
12. Versioning

Public APIs must have machine-readable OpenAPI documentation.

FastAPI's generated documentation can be used where appropriate.

---

# 25. Licensing

The repository must contain an explicit open-source license.

Do not assume the dataset license is automatically the same as the software license.

The project license and dataset license must be documented separately.

Before redistributing:

* Dataset
* Trained model
* Third-party dependencies

verify their respective licenses.

Do not package or redistribute data/model artifacts if their license does not permit it.

---

# 26. Third-party Dependencies

Every major dependency should have a legitimate reason.

Avoid unnecessary dependencies.

Track:

```text
Python packages
System packages
Model libraries
Frontend dependencies
Docker base images
```

Do not copy code from third-party projects without checking their license.

---

# 27. Contributions

The project should support community contributions.

Potential contributions:

```text
New datasets
New features
New models
Performance improvements
Bug fixes
API improvements
Documentation
Tests
SDKs
Security improvements
```

Contributors must not commit:

* Secrets
* Private datasets
* Credentials
* Malicious URLs intended to execute automatically
* Copyrighted datasets without redistribution permission

---

# 28. Pull Request Expectations

Changes should include:

* Description
* Reason for change
* Tests
* Documentation when necessary
* Performance impact when relevant
* Security implications when relevant

ML changes should additionally include:

* Dataset information
* Feature changes
* Model changes
* Evaluation metrics
* Comparison with previous model

Do not accept claims such as:

> "The new model is better"

without actual evaluation results.

---

# 29. Backward Compatibility

Once external developers depend on the project:

Avoid unnecessary breaking changes to:

```text
API
SDK
CLI
configuration
model interface
```

Breaking changes require:

1. Documentation
2. Changelog entry
3. Version increment
4. Migration instructions

---

# 30. Release Strategy

Use semantic versioning:

```text
MAJOR.MINOR.PATCH
```

Example:

```text
1.0.0
1.0.1
1.1.0
2.0.0
```

Guideline:

```text
PATCH
Bug fixes

MINOR
Backward-compatible features

MAJOR
Breaking changes
```

API versions may evolve independently:

```text
/v1/
 /v2/
```

---

# 31. Important Product Principle

The project must not claim:

```text
"100% accurate phishing detection"
```

or:

```text
"Guaranteed safe"
```

The system is a Machine Learning classification system.

Use:

```text
Potentially phishing
Suspicious
High risk
Low risk
Potentially legitimate
```

when appropriate.

---

# 32. Production vs Research

Separate experimentation from production code.

Research:

```text
training/
notebooks/
experiments/
```

Production:

```text
inference/
api/
```

Production API must never depend on executing a Jupyter notebook.

---

# 33. Definition of Done — MVP

The MVP is complete when:

* [ ] Dataset is documented.
* [ ] Dataset labels are verified.
* [ ] Data preprocessing works.
* [ ] Feature extraction works.
* [ ] Multiple ML models are evaluated.
* [ ] Best model is selected using real metrics.
* [ ] Model artifact can be saved/loaded.
* [ ] New URL can be classified.
* [ ] FastAPI service works.
* [ ] `/health` works.
* [ ] `/v1/check` works.
* [ ] API validation works.
* [ ] Tests exist.
* [ ] Docker works.
* [ ] Self-hosting documentation exists.
* [ ] API documentation exists.
* [ ] README exists.
* [ ] LICENSE exists.
* [ ] SECURITY.md exists.
* [ ] No secrets are committed.
* [ ] Arbitrary URLs are not fetched automatically.

---

# 34. Definition of Done — Public API

Before exposing a hosted API to the public:

* [ ] API versioning implemented.
* [ ] Authentication implemented.
* [ ] API key management implemented.
* [ ] Rate limiting implemented.
* [ ] Request validation implemented.
* [ ] Abuse prevention implemented.
* [ ] Monitoring implemented.
* [ ] Error handling standardized.
* [ ] Privacy policy documented.
* [ ] Data retention policy documented.
* [ ] Usage limits documented.
* [ ] API documentation published.
* [ ] Health monitoring implemented.
* [ ] Model versioning implemented.
* [ ] Deployment rollback strategy exists.

---

# 35. Long-Term Roadmap

## v0.x — Research

```text
Dataset
 ↓
EDA
 ↓
Feature Engineering
 ↓
Model Training
 ↓
Evaluation
```

## v0.x — Engine

```text
Model
 ↓
Inference Engine
 ↓
Feature Extractor
```

## v0.x — API

```text
Inference Engine
 ↓
FastAPI
 ↓
REST API
```

## v1.0 — Open Source Release

```text
Open Source Repository
+
Stable API
+
Docker
+
Documentation
+
Self-hosting
```

## v1.x — Developer Ecosystem

```text
Python SDK
JavaScript SDK
Go SDK
CLI
```

## v2.x — Hosted Service

```text
Public API
+
API Keys
+
Rate Limits
+
Usage Dashboard
+
Monitoring
```

## Future

```text
URL Detection
     +
Threat Intelligence
     +
Email Detection
     +
Message/Scam Detection
     +
Browser Extension
     +
Security Integrations
```

---

# 36. Agent Rules

AI agents working on this repository MUST:

1. Read this AGENTS.md first.
2. Treat this repository as an open-source software project.
3. Design components for reuse.
4. Avoid unnecessary coupling to the hosted service.
5. Preserve self-hosting capability.
6. Maintain API compatibility.
7. Use API versioning.
8. Never expose secrets.
9. Never fabricate metrics.
10. Never fabricate test results.
11. Never fabricate security guarantees.
12. Never automatically visit arbitrary submitted URLs.
13. Document breaking changes.
14. Run tests after meaningful changes.
15. Prefer incremental changes.
16. Avoid unnecessary dependencies.
17. Respect software and dataset licenses.
18. Keep production code separate from experiments.
19. Consider third-party developers as first-class users.
20. Optimize for developer experience and maintainability.

---

# 37. Final Product Definition

The project should ultimately be understood as:

> **An open-source phishing URL detection engine that developers can self-host or consume through a public API.**

The ML model is the detection engine.

The REST API is the integration interface.

Docker provides deployment portability.

SDKs provide developer convenience.

The hosted API provides managed access.

The GitHub repository provides transparency, collaboration, and self-hosting.

The architecture must ensure that these components can evolve independently.

JANGAN SAMPAI ADA EMOTE DI PROJEK INI
