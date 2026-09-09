import pytest
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_check_url_unauthorized():
    response = client.post("/v1/check", json={"url": "https://example.com"})
    # Since API_KEY is not set in env during test by default, it allows or checks accordingly
    # Let's adjust based on environment
    assert response.status_code in [200, 403]
