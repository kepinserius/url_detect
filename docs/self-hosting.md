# Self-Hosting Guide

## Prerequisites

- Docker and Docker Compose
- Or Python 3.10+

## Docker Deployment

```bash
docker compose up -d --build
```

Verify deployment:

```bash
curl http://localhost:8000/health
```
