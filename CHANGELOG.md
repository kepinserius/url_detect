# CHANGELOG

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial release of Phishing URL Detector
- REST API v1 with FastAPI
- XGBoost-based phishing URL detection model
- Authentication with API keys
- Rate limiting and quota management
- Prometheus metrics for monitoring
- Structured logging with PII redaction
- Python SDK client
- Docker and Docker Compose support
- Hyperparameter tuning with Optuna
- Comprehensive evaluation reporting
- CI/CD pipeline with GitHub Actions
- Support for model versioning and registry

### Security
- API key authentication (X-API-Key header)
- PII redaction in logs (tokens, passwords, emails)
- Static analysis only (no automatic URL fetching)
- Rate limiting to prevent abuse

### Documentation
- Complete API documentation
- Self-hosting guide
- Contributing guidelines
- Security policy
- Usage examples

## [0.1.0] - 2026-09-09

### Initial Release
- MVP with XGBoost model trained on PhiUSIIL dataset
- Basic REST API endpoints
- Docker containerization
- Python client SDK
