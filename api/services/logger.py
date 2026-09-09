import logging
import json
from datetime import datetime
from api.middleware.privacy import PrivacyManager

class StructuredLogger:
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def log_prediction(self, url: str, prediction: str, risk_score: float, api_key_hash: str):
        sanitized_url = PrivacyManager.sanitize_url(url)
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event": "prediction",
            "url_sanitized": sanitized_url,
            "prediction": prediction,
            "risk_score": risk_score,
            "api_key_hash": api_key_hash
        }
        self.logger.info(json.dumps(log_entry))

prediction_logger = StructuredLogger("prediction")
