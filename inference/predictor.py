import os
import joblib
import pandas as pd
from inference.features.extractor import URLFeatureExtractor

class Predictor:
    def __init__(self):
        model_path = os.getenv("MODEL_PATH", "models/phishing_model.joblib")
        feature_path = "models/feature_names.joblib"
        
        self.model = joblib.load(model_path)
        self.feature_names = joblib.load(feature_path)

    def predict(self, url: str) -> dict:
        raw_features = URLFeatureExtractor.extract_features(url)
        
        # Build dataframe aligning with training features
        # For simplicity in MVP, we fill missing columns with 0
        df = pd.DataFrame([raw_features])
        for col in self.feature_names:
            if col not in df.columns:
                df[col] = 0
        df = df[self.feature_names]

        prob = float(self.model.predict_proba(df)[0][1])
        prediction_label = "phishing" if prob > 0.5 else "legitimate"
        risk_score = round(prob * 100, 2)

        return {
            "prediction": prediction_label,
            "risk_score": risk_score,
            "confidence": round(prob if prob > 0.5 else 1 - prob, 4)
        }
