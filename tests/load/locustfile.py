from locust import HttpUser, task, between

class PhishingDetectorUser(HttpUser):
    wait_time = between(1, 3)
    
    def on_start(self):
        self.api_key = "your_api_key_here"
    
    @task
    def check_url(self):
        self.client.post(
            "/v1/check",
            headers={"X-API-Key": self.api_key},
            json={"url": "https://example.com/login"}
        )
    
    @task(2)
    def health_check(self):
        self.client.get("/health")
