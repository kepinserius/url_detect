# Architecture Documentation

## Core Overview

The system consists of three main modules:

1. **Feature Extractor**: Parses URL string into lexical, structural, and domain features without sending HTTP requests.
2. **Inference Engine**: Loads trained ML models and computes phishing predictions, confidence scores, and risk indicators.
3. **API Service**: FastAPI application exposing versioned REST endpoints.

```text
   User Request (POST /v1/check)
               │
               ▼
         FastAPI App
               │
               ▼
      Inference Engine
               │
               ├───────────────────┐
               ▼                   ▼
       Feature Extractor     ML Predictor
               │                   │
               └─────────┬─────────┘
                         ▼
                   JSON Response
```
