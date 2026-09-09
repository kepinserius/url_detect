import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import classification_report, roc_auc_score, f1_score, precision_recall_curve, auc
import logging
import json

logging.basicConfig(level=logging.INFO)

def main():
    dataset_path = "data/raw/PhiUSIIL_Phishing_URL_Dataset.csv"
    logger = logging.getLogger(__name__)
    
    logger.info("Training calibrated model with probability calibration...")
    df = pd.read_csv(dataset_path)
    
    # Select URL-only features
    url_features = [
        'URLLength', 'DomainLength', 'IsDomainIP', 'URLSimilarityIndex',
        'CharContinuationRate', 'TLDLegitimateProb', 'URLCharProb', 'TLDLength',
        'NoOfSubDomain', 'HasObfuscation', 'NoOfObfuscatedChar', 'ObfuscationRatio',
        'NoOfLettersInURL', 'LetterRatioInURL', 'NoOfDegitsInURL', 'DegitRatioInURL',
        'NoOfEqualsInURL', 'NoOfQMarkInURL', 'NoOfAmpersandInURL',
        'NoOfOtherSpecialCharsInURL', 'SpacialCharRatioInURL', 'IsHTTPS'
    ]
    
    available_features = [f for f in url_features if f in df.columns]
    X = df[available_features]
    y = df['label']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train base XGBoost
    base_model = XGBClassifier(
        n_estimators=185,
        max_depth=6,
        learning_rate=0.0155,
        subsample=0.96,
        colsample_bytree=0.82,
        gamma=3.45,
        reg_alpha=9.10,
        reg_lambda=0.08,
        random_state=42,
        scale_pos_weight=(y_train == 0).sum() / (y_train == 1).sum()  # Handle class imbalance
    )
    
    # Calibrate probabilities using cross-validation
    logger.info("Calibrating probabilities...")
    calibrated_model = CalibratedClassifierCV(base_model, method='sigmoid', cv=5)
    calibrated_model.fit(X_train, y_train)
    
    # Test calibrated model
    y_pred_proba = calibrated_model.predict_proba(X_test)[:, 1]
    y_pred = calibrated_model.predict(X_test)
    
    logger.info("\n" + "="*50)
    logger.info("CALIBRATED MODEL RESULTS (Test Set)")
    logger.info("="*50)
    logger.info(f"ROC-AUC: {roc_auc_score(y_test, y_pred_proba):.4f}")
    logger.info(f"F1 Score: {f1_score(y_test, y_pred):.4f}")
    
    # Find optimal threshold
    precision, recall, thresholds = precision_recall_curve(y_test, y_pred_proba)
    f1_scores = 2 * precision * recall / (precision + recall + 1e-10)
    optimal_idx = np.argmax(f1_scores)
    optimal_threshold = thresholds[optimal_idx] if len(thresholds) > 0 else 0.5
    
    logger.info(f"Optimal Threshold (max F1): {optimal_threshold:.4f}")
    logger.info(f"Best F1 at threshold: {f1_scores[optimal_idx]:.4f}")
    
    # Test with optimal threshold
    y_pred_optimal = (y_pred_proba >= optimal_threshold).astype(int)
    logger.info(f"\nWith optimal threshold {optimal_threshold:.4f}:")
    logger.info(f"F1 Score: {f1_score(y_test, y_pred_optimal):.4f}")
    logger.info(classification_report(y_test, y_pred_optimal))
    
    # Save calibrated model
    joblib.dump(calibrated_model, "models/phishing_calibrated_model.joblib")
    joblib.dump(available_features, "models/calibrated_feature_names.joblib")
    
    # Save threshold
    threshold_config = {
        "optimal_threshold": float(optimal_threshold),
        "calibration_method": "sigmoid",
        "cv_folds": 5,
        "features": available_features
    }
    with open("models/threshold_config.json", "w") as f:
        json.dump(threshold_config, f, indent=2)
    
    logger.info(f"\n✓ Calibrated model saved: models/phishing_calibrated_model.joblib")
    logger.info(f"✓ Threshold config saved: {optimal_threshold}")
    
    return calibrated_model, optimal_threshold

if __name__ == "__main__":
    main()
