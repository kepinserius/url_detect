import requests

class PhishingDetectorClient:
    def __init__(self, base_url="http://localhost:8000", api_key=None):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.headers = {"X-API-Key": api_key} if api_key else {}

    def check(self, url: str):
        response = requests.post(
            f"{self.base_url}/v1/check",
            headers={"Content-Type": "application/json", **self.headers},
            json={"url": url}
        )
        response.raise_for_status()
        return response.json()

    def health(self):
        response = requests.get(f"{self.base_url}/health")
        response.raise_for_status()
        return response.json()
