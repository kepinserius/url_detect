"""
Core utilities and configuration.

Config, exceptions, and utility functions for URL Detect.
"""

import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings."""
    
    app_env: str = os.getenv("APP_ENV", "development")
    api_v1_str: str = os.getenv("API_V1_STR", "/v1")
    project_name: str = os.getenv("PROJECT_NAME", "URL Detect")
    model_path: str = os.getenv("MODEL_PATH", "models/phishing_improved_model.joblib")
    feature_path: str = os.getenv("FEATURE_PATH", "models/improved_feature_names.joblib")
    api_key: str = os.getenv("API_KEY", "")
    phishtank_api_key: str = os.getenv("PHISHTANK_API_KEY", "")
    redis_url: str = os.getenv("REDIS_URL", "")
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///models/enterprise.db")

settings = Settings()

class APIKeyError(Exception):
    """API key validation error."""
    pass

class QuotaError(Exception):
    """Quota exceeded error."""
    pass

class RateLimitError(Exception):
    """Rate limit exceeded error."""
    pass
