import json
import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, f1_score, precision_score, recall_score, accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns
import logging

logger = logging.getLogger(__name__)

class EvaluationReportGenerator:
    def __init__(self, output_dir="models"):
        self.output_dir = output_dir
    
    def generate(self, y_true, y_pred, y_pred_proba, model_name, feature_count, training_time=None):
        metrics = {
            "model_name": model_name,
            "accuracy": float(accuracy_score(y_true, y_pred)),
            "precision": float(precision_score(y_true, y_pred)),
            "recall": float(recall_score(y_true, y_pred)),
            "f1_score": float(f1_score(y_true, y_pred)),
            "roc_auc": float(roc_auc_score(y_true, y_pred_proba)) if y_pred_proba is not None else None,
            "feature_count": feature_count,
            "training_time_seconds": training_time,
            "confusion_matrix": {
                "true_negative": int(confusion_matrix(y_true, y_pred)[0][0]),
                "false_positive": int(confusion_matrix(y_true, y_pred)[0][1]),
                "false_negative": int(confusion_matrix(y_true, y_pred)[1][0]),
                "true_positive": int(confusion_matrix(y_true, y_pred)[1][1])
            },
            "classification_report": classification_report(y_true, y_pred, output_dict=True)
        }
        
        report_path = f"{self.output_dir}/evaluation_report_{model_name}.json"
        with open(report_path, "w") as f:
            json.dump(metrics, f, indent=2)
        logger.info(f"Evaluation report saved to {report_path}")
        
        cm = confusion_matrix(y_true, y_pred)
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
        plt.title(f"Confusion Matrix - {model_name}")
        plt.ylabel("True Label")
        plt.xlabel("Predicted Label")
        cm_path = f"{self.output_dir}/confusion_matrix_{model_name}.png"
        plt.savefig(cm_path)
        plt.close()
        logger.info(f"Confusion matrix saved to {cm_path}")
        
        return metrics
