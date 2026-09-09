import os
import joblib
import pandas as pd
import json
import logging
from inference.features.advanced_extractor import PhiUSIILFeatureExtractor

logger = logging.getLogger(__name__)

class ImprovedPredictor:
    def __init__(self):
        # Use improved model
        model_path = os.getenv("MODEL_PATH", "models/phishing_improved_model.joblib")
        feature_path = os.getenv("FEATURE_PATH", "models/improved_feature_names.joblib")
        config_path = "models/improved_model_config.json"
        
        self.model = joblib.load(model_path)
        self.feature_names = joblib.load(feature_path)
        
        # Load threshold config
        with open(config_path, "r") as f:
            config = json.load(f)
        self.threshold = config.get("threshold", 0.7)
        
        logger.debug(f"Using threshold: {self.threshold}")

    def predict(self, url: str) -> dict:
        raw_features = PhiUSIILFeatureExtractor.extract_all(url)
        
        # Build dataframe aligning with training features
        df = pd.DataFrame([raw_features])
        
        # Ensure all model features are present
        for col in self.feature_names:
            if col not in df.columns:
                df[col] = 0
        
        # Reorder columns to match training
        df = df[self.feature_names]

        prob = float(self.model.predict_proba(df)[0][1])
        
        # Use custom threshold (0.7 instead of 0.5)
        prediction_label = "phishing" if prob >= self.threshold else "legitimate"
        risk_score = round(prob * 100, 2)
        
        # Confidence is probability of predicted class
        if prediction_label == "phishing":
            confidence = round(prob, 4)
        else:
            confidence = round(1 - prob, 4)

        return {
            "prediction": prediction_label,
            "risk_score": risk_score,
            "confidence": confidence,
            "threshold_used": self.threshold,
            "raw_probability": prob
        }
