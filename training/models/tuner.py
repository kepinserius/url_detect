import optuna
import numpy as np
from sklearn.model_selection import cross_val_score
from xgboost import XGBClassifier
from sklearn.ensemble import RandomForestClassifier
import logging

logger = logging.getLogger(__name__)

class ModelTuner:
    def __init__(self, cv_folds=5, random_state=42):
        self.cv_folds = cv_folds
        self.random_state = random_state
        
    def objective_xgboost(self, trial, X, y):
        params = {
            "n_estimators": trial.suggest_int("n_estimators", 50, 300),
            "max_depth": trial.suggest_int("max_depth", 3, 10),
            "learning_rate": trial.suggest_float("learning_rate", 0.01, 0.3, log=True),
            "subsample": trial.suggest_float("subsample", 0.6, 1.0),
            "colsample_bytree": trial.suggest_float("colsample_bytree", 0.6, 1.0),
            "gamma": trial.suggest_float("gamma", 0, 5),
            "reg_alpha": trial.suggest_float("reg_alpha", 1e-3, 10.0, log=True),
            "reg_lambda": trial.suggest_float("reg_lambda", 1e-3, 10.0, log=True),
            "random_state": self.random_state
        }
        
        try:
            model = XGBClassifier(**params)
            score = cross_val_score(model, X, y, cv=self.cv_folds, scoring="f1", n_jobs=1).mean()
            return score
        except Exception as e:
            logger.warning(f"Trial failed: {e}")
            return 0.0
    
    def objective_random_forest(self, trial, X, y):
        params = {
            "n_estimators": trial.suggest_int("n_estimators", 50, 300),
            "max_depth": trial.suggest_int("max_depth", 5, 30),
            "min_samples_split": trial.suggest_int("min_samples_split", 2, 20),
            "min_samples_leaf": trial.suggest_int("min_samples_leaf", 1, 10),
            "max_features": trial.suggest_categorical("max_features", ["sqrt", "log2"]),
            "bootstrap": trial.suggest_categorical("bootstrap", [True, False]),
            "random_state": self.random_state
        }
        
        model = RandomForestClassifier(**params)
        score = cross_val_score(model, X, y, cv=self.cv_folds, scoring="roc_auc", n_jobs=-1).mean()
        return score
    
    def tune_xgboost(self, X, y, n_trials=50):
        study = optuna.create_study(direction="maximize")
        study.optimize(lambda trial: self.objective_xgboost(trial, X, y), n_trials=n_trials)
        return study.best_params, study.best_value
    
    def tune_random_forest(self, X, y, n_trials=30):
        study = optuna.create_study(direction="maximize")
        study.optimize(lambda trial: self.objective_random_forest(trial, X, y), n_trials=n_trials)
        return study.best_params, study.best_value
