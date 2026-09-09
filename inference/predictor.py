import os
import joblib
import pandas as pd
from inference.features.advanced_extractor import PhiUSIILFeatureExtractor

class Predictor:
    def __init__(self):
        # Use URL-only model (22 features) instead of full 50-feature model
        model_path = os.getenv("MODEL_PATH", "models/phishing_url_only_model.joblib")
        feature_path = os.getenv("FEATURE_PATH", "models/url_only_feature_names.joblib")
        
        self.model = joblib.load(model_path)
        self.feature_names = joblib.load(feature_path)
        
        # Verify feature extraction compatibility
        sample_features = PhiUSIILFeatureExtractor.extract_all("https://example.com")
        missing_features = [f for f in self.feature_names if f not in sample_features]
        if missing_features:
            print(f"Warning: {len(missing_features)} training features not in extractor")

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
        prediction_label = "phishing" if prob > 0.5 else "legitimate"
        risk_score = round(prob * 100, 2)

        return {
            "prediction": prediction_label,
            "risk_score": risk_score,
            "confidence": round(prob if prob > 0.5 else 1 - prob, 4)
        }
