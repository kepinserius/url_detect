import pandas as pd
import json
import joblib
from training.preprocessing.validator import DataValidator
from training.preprocessing.cleaner import DataCleaner
from training.preprocessing.preprocessor import DataPreprocessor
from training.models.trainer import ModelTrainer
from sklearn.model_selection import train_test_split
import logging

logging.basicConfig(level=logging.INFO)

def main():
    dataset_path = "data/raw/PhiUSIIL_Phishing_URL_Dataset.csv"
    logger = logging.getLogger(__name__)
    
    logger.info(f"Loading dataset from {dataset_path}")
    df = pd.read_csv(dataset_path)
    
    validator = DataValidator()
    report = validator.validate(df, required_cols=['label'])
    logger.info(f"Validation report: {json.dumps(report, indent=2)}")
    
    if not report["is_valid"]:
        logger.warning("Dataset has issues, but proceeding...")
    
    cleaner = DataCleaner()
    df_clean = cleaner.clean(df)
    
    preprocessor = DataPreprocessor()
    X, y = preprocessor.prepare(df_clean)
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    logger.info(f"Train: {X_train.shape}, Test: {X_test.shape}")
    
    trainer = ModelTrainer(random_state=42)
    models = trainer.train(X_train, y_train)
    
    evaluation = trainer.evaluate(models, X_test, y_test)
    
    best_model_name = trainer.select_best(evaluation)
    best_model = models[best_model_name]["model"]
    
    model_path = f"models/{best_model_name}_model.joblib"
    joblib.dump(best_model, model_path)
    joblib.dump(X.columns.tolist(), "models/feature_names.joblib")
    
    eval_report = {
        "best_model": best_model_name,
        "evaluation": evaluation,
        "training_time": {name: info["training_time"] for name, info in models.items()},
        "feature_count": X.shape[1],
        "test_size": len(y_test)
    }
    
    report_path = "models/evaluation_report.json"
    with open(report_path, "w") as f:
        json.dump(eval_report, f, indent=2)
    
    logger.info(f"Best model: {best_model_name}")
    logger.info(f"Model saved to {model_path}")
    logger.info(f"Evaluation report saved to {report_path}")
    logger.info(f"F1 scores: { {k: v['f1_score'] for k, v in evaluation.items()} }")
    
    return eval_report

if __name__ == "__main__":
    main()
