import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from sklearn.metrics import classification_report, roc_auc_score, f1_score, confusion_matrix
import logging
import json

logging.basicConfig(level=logging.INFO)

def main():
    dataset_path = "data/raw/PhiUSIIL_Phishing_URL_Dataset.csv"
    logger = logging.getLogger(__name__)
    
    logger.info("Retraining model with better configuration...")
    df = pd.read_csv(dataset_path)
    
    # Clean data
    df = df.dropna(subset=['label'])
    df = df[df['label'].isin([0, 1])]
    
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
    
    logger.info(f"Training with {len(available_features)} features")
    logger.info(f"Dataset size: {len(df)} (Phishing: {sum(y==1)}, Legitimate: {sum(y==0)})")
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # Train XGBoost with adjusted parameters
    logger.info("Training XGBoost with adjusted params...")
    model = XGBClassifier(
        n_estimators=200,
        max_depth=8,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        scale_pos_weight=1.0,  # Balanced
        min_child_weight=1,
        gamma=0.1,
        reg_alpha=1.0,
        reg_lambda=1.0,
        random_state=42,
        eval_metric='logloss'
    )
    
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    
    # Test different thresholds
    thresholds = [0.3, 0.4, 0.5, 0.6, 0.7]
    best_threshold = 0.5
    best_f1 = 0
    
    logger.info("\nTesting different thresholds:")
    for threshold in thresholds:
        y_pred = (y_pred_proba >= threshold).astype(int)
        f1 = f1_score(y_test, y_pred)
        logger.info(f"Threshold {threshold}: F1={f1:.4f}")
        if f1 > best_f1:
            best_f1 = f1
            best_threshold = threshold
    
    logger.info(f"\nBest threshold: {best_threshold} (F1: {best_f1:.4f})")
    
    # Final prediction with best threshold
    y_pred = (y_pred_proba >= best_threshold).astype(int)
    
    logger.info("\n" + "="*50)
    logger.info("IMPROVED MODEL RESULTS")
    logger.info("="*50)
    logger.info(f"Threshold: {best_threshold}")
    logger.info(f"ROC-AUC: {roc_auc_score(y_test, y_pred_proba):.4f}")
    logger.info(f"F1 Score: {f1_score(y_test, y_pred):.4f}")
    logger.info("\n" + classification_report(y_test, y_pred, target_names=['Legitimate', 'Phishing']))
    
    cm = confusion_matrix(y_test, y_pred)
    tn, fp, fn, tp = cm.ravel()
    logger.info(f"\nConfusion Matrix:")
    logger.info(f"TN: {tn}, FP: {fp}, FN: {fn}, TP: {tp}")
    logger.info(f"False Negative Rate: {fn/(fn+tp):.4f}")
    logger.info(f"False Positive Rate: {fp/(fp+tn):.4f}")
    
    # Save improved model
    joblib.dump(model, "models/phishing_improved_model.joblib")
    joblib.dump(available_features, "models/improved_feature_names.joblib")
    
    config = {
        "threshold": float(best_threshold),
        "features": available_features,
        "metrics": {
            "roc_auc": float(roc_auc_score(y_test, y_pred_proba)),
            "f1_score": float(f1_score(y_test, y_pred)),
            "true_negatives": int(tn),
            "false_positives": int(fp),
            "false_negatives": int(fn),
            "true_positives": int(tp)
        }
    }
    
    with open("models/improved_model_config.json", "w") as f:
        json.dump(config, f, indent=2)
    
    logger.info(f"\n✓ Improved model saved")
    logger.info(f"✓ Optimal threshold: {best_threshold}")

if __name__ == "__main__":
    main()
