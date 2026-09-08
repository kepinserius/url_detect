# API Specification

## Endpoints

### GET /health

Returns operational status.

**Response (200 OK):**
```json
{
  "status": "ok",
  "version": "1.0.0"
}
```

### POST /v1/check

Analyzes a URL and predicts whether it is phishing or legitimate.

**Request Body:**
```json
{
  "url": "https://example.com/login"
}
```

**Response (200 OK):**
```json
{
  "prediction": "phishing",
  "risk_score": 92,
  "confidence": 0.92,
  "indicators": [
    "URL length exceeds standard threshold",
    "Presence of IP address in hostname"
  ],
  "model_version": "1.0.0"
}
```
