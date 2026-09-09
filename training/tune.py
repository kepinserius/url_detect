import pandas as pd
import joblib
from training.preprocessing.validator import DataValidator
from training.preprocessing.cleaner import DataCleaner
from training.preprocessing.preprocessor import DataPreprocessor
from training.models.tuner import ModelTuner
from sklearn.model_selection import train_test_split
import logging
import json

logging.basicConfig(level=logging.INFO)

def main():
    dataset_path = "data/raw/PhiUSIIL_Phishing_URL_Dataset.csv"
    logger = logging.getLogger(__name__)
    
    logger.info("Loading and validating data...")
    df = pd.read_csv(dataset_path)
    
    validator = DataValidator()
    report = validator.validate(df, required_cols=['label'])
    if not report["is_valid"]:
        logger.warning("Dataset has issues")
    
    cleaner = DataCleaner()
    df_clean = cleaner.clean(df)
    
    preprocessor = DataPreprocessor()
    X, y = preprocessor.prepare(df_clean)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    logger.info(f"Train: {X_train.shape}, Test: {X_test.shape}")
    
    logger.info("Starting hyperparameter tuning for XGBoost...")
    tuner = ModelTuner(cv_folds=3, random_state=42)
    best_params, best_score = tuner.tune_xgboost(X_train, y_train, n_trials=10)
    logger.info(f"Best XGBoost params: {best_params}")
    logger.info(f"Best CV score: {best_score:.4f}")
    
    from xgboost import XGBClassifier
    tuned_model = XGBClassifier(**best_params, random_state=42)
    tuned_model.fit(X_train, y_train)
    
    y_pred_proba = tuned_model.predict_proba(X_test)[:, 1]
    from sklearn.metrics import roc_auc_score, f1_score
    test_score = roc_auc_score(y_test, y_pred_proba)
    test_f1 = f1_score(y_test, tuned_model.predict(X_test))
    
    logger.info(f"Test ROC-AUC: {test_score:.4f}, Test F1: {test_f1:.4f}")
    
    joblib.dump(tuned_model, "models/xgboost_tuned_model.joblib")
    joblib.dump(X.columns.tolist(), "models/feature_names.joblib")
    
    report = {
        "tuned": True,
        "best_params": best_params,
        "cv_score": best_score,
        "test_roc_auc": test_score,
        "test_f1": test_f1,
        "training_rows": len(y_train),
        "test_rows": len(y_test),
        "feature_count": X.shape[1]
    }
    
    with open("models/tuning_report.json", "w") as f:
        json.dump(report, f, indent=2)
    
    logger.info("Tuning complete. Report saved to models/tuning_report.json")

if __name__ == "__main__":
    main()
