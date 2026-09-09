import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, roc_auc_score, f1_score, precision_recall_curve, auc
import json
import time
import logging

logger = logging.getLogger(__name__)

class ModelTrainer:
    def __init__(self, random_state=42):
        self.random_state = random_state
        self.models = {
            "xgboost": XGBClassifier(random_state=random_state, n_estimators=100),
            "random_forest": RandomForestClassifier(random_state=random_state),
            "logistic_regression": LogisticRegression(random_state=random_state, max_iter=1000)
        }
    
    def train(self, X_train, y_train, X_val=None, y_val=None):
        results = {}
        
        for name, model in self.models.items():
            logger.info(f"Training {name}")
            start = time.time()
            model.fit(X_train, y_train)
            training_time = time.time() - start
            results[name] = {
                "model": model,
                "training_time": training_time
            }
            logger.info(f"{name} trained in {training_time:.2f}s")
        
        return results
    
    def evaluate(self, models_dict, X_test, y_test):
        evaluation = {}
        
        for name, info in models_dict.items():
            model = info["model"]
            y_pred = model.predict(X_test)
            y_pred_proba = model.predict_proba(X_test)[:, 1] if hasattr(model, "predict_proba") else None
            
            metrics = {
                "precision": classification_report(y_test, y_pred, output_dict=True),
                "roc_auc": roc_auc_score(y_test, y_pred_proba) if y_pred_proba is not None else None,
                "f1_score": f1_score(y_test, y_pred)
            }
            
            if y_pred_proba is not None:
                precision, recall, _ = precision_recall_curve(y_test, y_pred_proba)
                metrics["pr_auc"] = auc(recall, precision)
            
            evaluation[name] = metrics
        
        return evaluation
    
    def select_best(self, evaluation):
        best_score = -1
        best_model_name = None
        
        for name, metrics in evaluation.items():
            f1 = metrics.get("f1_score", 0)
            if f1 > best_score:
                best_score = f1
                best_model_name = name
        
        return best_model_name
