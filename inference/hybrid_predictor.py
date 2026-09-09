import os
import joblib
import pandas as pd
import json
import logging
from inference.features.advanced_extractor import PhiUSIILFeatureExtractor
from inference.rules.phishing_rules import RuleBasedPhishingDetector

logger = logging.getLogger(__name__)

class HybridPredictor:
    """
    Hybrid phishing detector combining:
    1. ML model (XGBoost)
    2. Rule-based detection
    3. Ensemble decision
    """
    
    def __init__(self):
        # Load ML model
        model_path = os.getenv("MODEL_PATH", "models/phishing_improved_model.joblib")
        feature_path = os.getenv("FEATURE_PATH", "models/improved_feature_names.joblib")
        config_path = "models/improved_model_config.json"
        
        self.model = joblib.load(model_path)
        self.feature_names = joblib.load(feature_path)
        
        with open(config_path, "r") as f:
            config = json.load(f)
        self.ml_threshold = config.get("threshold", 0.7)
        
        # Rule-based detector
        self.rule_detector = RuleBasedPhishingDetector()
        
        logger.info(f"Hybrid predictor initialized (ML threshold: {self.ml_threshold})")

    def predict(self, url: str) -> dict:
        """
        Hybrid prediction combining ML and rules.
        
        Decision logic:
        1. If rule-based score > 0.7: PHISHING (high confidence)
        2. If rule-based score > 0.5: Use ML as tiebreaker
        3. If rule-based score < 0.5: Primarily ML decision
        """
        # 1. Rule-based analysis
        rule_result = self.rule_detector.analyze(url)
        rule_score = rule_result['rule_based_score']
        
        # 2. ML model prediction
        raw_features = PhiUSIILFeatureExtractor.extract_all(url)
        df = pd.DataFrame([raw_features])
        
        for col in self.feature_names:
            if col not in df.columns:
                df[col] = 0
        df = df[self.feature_names]
        
        ml_prob = float(self.model.predict_proba(df)[0][1])
        
        # 3. Hybrid decision
        if rule_score >= 0.8:
            # High confidence phishing from rules
            final_prediction = "phishing"
            confidence = max(rule_score, 0.85)
            decision_method = "rule_based_high_confidence"
        elif rule_score >= 0.5:
            # Medium rule score - use ensemble
            ensemble_score = (rule_score * 0.6 + ml_prob * 0.4)
            final_prediction = "phishing" if ensemble_score >= 0.5 else "legitimate"
            confidence = ensemble_score if final_prediction == "phishing" else (1 - ensemble_score)
            decision_method = "ensemble"
        else:
            # Low rule score - primarily ML
            final_prediction = "phishing" if ml_prob >= self.ml_threshold else "legitimate"
            confidence = ml_prob if final_prediction == "phishing" else (1 - ml_prob)
            decision_method = "ml_primary"
        
        risk_score = confidence * 100 if final_prediction == "phishing" else (1 - confidence) * 100
        
        return {
            "prediction": final_prediction,
            "risk_score": round(risk_score, 2),
            "confidence": round(confidence, 4),
            "method": decision_method,
            "details": {
                "ml_probability": round(ml_prob, 4),
                "rule_score": round(rule_score, 4),
                "suspicious_tld": rule_result['suspicious_tld'],
                "typosquatting": rule_result['typosquatting'],
                "brand_abuse": rule_result['brand_abuse'],
                "suspicious_patterns": rule_result['suspicious_patterns']
            }
        }
