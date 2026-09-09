import pandas as pd
import joblib
from training.preprocessing.validator import DataValidator
from training.preprocessing.cleaner import DataCleaner
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from sklearn.metrics import classification_report, roc_auc_score, f1_score
import logging
import json

logging.basicConfig(level=logging.INFO)

def main():
    dataset_path = "data/raw/PhiUSIIL_Phishing_URL_Dataset.csv"
    logger = logging.getLogger(__name__)
    
    logger.info("Training URL-only model (excluding HTML content features)...")
    df = pd.read_csv(dataset_path)
    
    validator = DataValidator()
    report = validator.validate(df, required_cols=['label'])
    
    cleaner = DataCleaner()
    df_clean = cleaner.clean(df)
    
    # Select only URL-based features (exclude HTML/content features)
    url_features = [
        'URLLength', 'DomainLength', 'IsDomainIP', 'URLSimilarityIndex',
        'CharContinuationRate', 'TLDLegitimateProb', 'URLCharProb', 'TLDLength',
        'NoOfSubDomain', 'HasObfuscation', 'NoOfObfuscatedChar', 'ObfuscationRatio',
        'NoOfLettersInURL', 'LetterRatioInURL', 'NoOfDegitsInURL', 'DegitRatioInURL',
        'NoOfEqualsInURL', 'NoOfQMarkInURL', 'NoOfAmpersandInURL',
        'NoOfOtherSpecialCharsInURL', 'SpacialCharRatioInURL', 'IsHTTPS'
    ]
    
    # Only use URL features that exist in dataset
    available_features = [f for f in url_features if f in df_clean.columns]
    X = df_clean[available_features]
    y = df_clean['label']
    
    logger.info(f"Training with {len(available_features)} URL-only features")
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train XGBoost on URL-only features
    model = XGBClassifier(
        n_estimators=185,
        max_depth=6,
        learning_rate=0.0155,
        subsample=0.96,
        colsample_bytree=0.82,
        gamma=3.45,
        reg_alpha=9.10,
        reg_lambda=0.08,
        random_state=42
    )
    
    logger.info("Training model...")
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    
    logger.info("\n" + classification_report(y_test, y_pred))
    logger.info(f"ROC-AUC: {roc_auc_score(y_test, y_pred_proba):.4f}")
    logger.info(f"F1 Score: {f1_score(y_test, y_pred):.4f}")
    
    # Save URL-only model
    joblib.dump(model, "models/phishing_url_only_model.joblib")
    joblib.dump(available_features, "models/url_only_feature_names.joblib")
    
    # Save evaluation
    metrics = {
        "model_type": "url_only",
        "features": available_features,
        "feature_count": len(available_features),
        "roc_auc": float(roc_auc_score(y_test, y_pred_proba)),
        "f1_score": float(f1_score(y_test, y_pred)),
        "test_samples": len(y_test)
    }
    
    with open("models/url_only_evaluation.json", "w") as f:
        json.dump(metrics, f, indent=2)
    
    logger.info("URL-only model saved to models/phishing_url_only_model.joblib")
    logger.info(f"Performance: ROC-AUC={metrics['roc_auc']:.4f}, F1={metrics['f1_score']:.4f}")

if __name__ == "__main__":
    main()
