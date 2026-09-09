import pandas as pd
import joblib
from inference.predictor import Predictor
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, f1_score
import numpy as np
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def validate_on_external_dataset():
    # Load the trained predictor
    logger.info("Loading trained model...")
    predictor = Predictor()
    
    # Create synthetic validation dataset
    # This includes both legitimate and phishing examples
    validation_data = [
        # Legitimate (label=0)
        {"url": "https://google.com", "label": 0},
        {"url": "https://facebook.com", "label": 0},
        {"url": "https://github.com", "label": 0},
        {"url": "https://stackoverflow.com", "label": 0},
        {"url": "https://wikipedia.org", "label": 0},
        {"url": "https://twitter.com", "label": 0},
        {"url": "https://linkedin.com", "label": 0},
        {"url": "https://microsoft.com", "label": 0},
        {"url": "https://apple.com", "label": 0},
        {"url": "https://netflix.com", "label": 0},
        
        # Typosquatting phishing (label=1)
        {"url": "https://facebok.com", "label": 1},
        {"url": "https://gogle.com", "label": 1},
        {"url": "https://gooogle.com", "label": 1},
        {"url": "https://paypa1.com", "label": 1},
        {"url": "https://paypal-login.xyz", "label": 1},
        {"url": "https://facebook-secure-login.tk", "label": 1},
        {"url": "https://secure-bank-login.cc", "label": 1},
        {"url": "https://instagram-verify-code.ml", "label": 1},
        {"url": "https://whatsapp-web-free.ru", "label": 1},
        {"url": "https://amazon-gift-card-claim.ga", "label": 1},
        
        # Suspicious patterns
        {"url": "http://192.168.1.1:8080/login.php?user=admin&pass=1234", "label": 1},
        {"url": "https://very-long-domain-name-with-dashes-and-numbers-12345.com/login/verify", "label": 1},
        {"url": "https://example.com/login?token=secret&password=123&email=user@domain.com", "label": 0},
        
        # Mixed legitimate with query params
        {"url": "https://github.com/login?return_to=%2Fdashboard", "label": 0},
        {"url": "https://facebook.com/dialog/oauth?client_id=123&redirect_uri=...", "label": 0},
        
        # More phishing patterns
        {"url": "https://apple-id-verification.xyz", "label": 1},
        {"url": "http://microsoft-account-update.cf", "label": 1},
        {"url": "https://google-drive-security-alert.gq", "label": 1},
        {"url": "https://dropbox-file-sharing-notification.cc", "label": 1},
    ]
    
    df = pd.DataFrame(validation_data)
    
    logger.info(f"Validation dataset size: {len(df)}")
    logger.info(f"Class distribution: Legitimate={sum(df['label']==0)}, Phishing={sum(df['label']==1)}")
    
    # Run predictions
    predictions = []
    probabilities = []
    
    logger.info("Running predictions...")
    for idx, row in df.iterrows():
        try:
            result = predictor.predict(row['url'])
            pred_label = 1 if result['prediction'] == 'phishing' else 0
            pred_prob = result['risk_score'] / 100.0  # Convert to 0-1
            
            predictions.append(pred_label)
            probabilities.append(pred_prob)
            
            if idx < 5:  # Log first few predictions
                logger.info(f"URL: {row['url'][:50]}... | True: {row['label']} | Pred: {pred_label} ({result['prediction']}) | Score: {result['risk_score']:.2f}%")
        except Exception as e:
            logger.error(f"Error predicting {row['url']}: {e}")
            predictions.append(0)
            probabilities.append(0.0)
    
    # Calculate metrics
    if len(predictions) > 0 and len(probabilities) > 0:
        y_true = df['label'].values[:len(predictions)]
        y_pred = np.array(predictions)
        y_prob = np.array(probabilities)
        
        # Metrics
        from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
        
        accuracy = accuracy_score(y_true, y_pred)
        precision = precision_score(y_true, y_pred)
        recall = recall_score(y_true, y_pred)
        f1 = f1_score(y_true, y_pred)
        
        # Handle single class for ROC-AUC
        if len(np.unique(y_true)) > 1:
            roc_auc = roc_auc_score(y_true, y_prob)
        else:
            roc_auc = None
        
        logger.info("\n" + "="*50)
        logger.info("EXTERNAL VALIDATION RESULTS")
        logger.info("="*50)
        logger.info(f"Dataset Size: {len(df)}")
        logger.info(f"Accuracy:  {accuracy:.4f}")
        logger.info(f"Precision: {precision:.4f}")
        logger.info(f"Recall:    {recall:.4f}")
        logger.info(f"F1 Score:  {f1:.4f}")
        if roc_auc is not None:
            logger.info(f"ROC-AUC:   {roc_auc:.4f}")
        
        # Confusion matrix
        cm = confusion_matrix(y_true, y_pred)
        tn, fp, fn, tp = cm.ravel()
        logger.info("\nConfusion Matrix:")
        logger.info(f"True Negatives (Legitimate correctly):  {tn}")
        logger.info(f"False Positives (Legitimate as Phishing): {fp}")
        logger.info(f"False Negatives (Phishing as Legitimate): {fn}")
        logger.info(f"True Positives (Phishing correctly):    {tp}")
        
        # False negatives analysis (critical for phishing detection)
        false_negatives = df[(df['label'] == 1) & (y_pred == 0)]
        if len(false_negatives) > 0:
            logger.info("\n⚠️  FALSE NEGATIVES (PHISHING URLs MISSED):")
            for _, row in false_negatives.iterrows():
                logger.info(f"  - {row['url']}")
        
        # False positives analysis
        false_positives = df[(df['label'] == 0) & (y_pred == 1)]
        if len(false_positives) > 0:
            logger.info("\n⚠️  FALSE POSITIVES (LEGITIMATE URLs FLAGGED):")
            for _, row in false_positives.iterrows():
                logger.info(f"  - {row['url']}")
        
        # Save results
        results = {
            "metrics": {
                "accuracy": float(accuracy),
                "precision": float(precision),
                "recall": float(recall),
                "f1_score": float(f1),
                "roc_auc": float(roc_auc) if roc_auc else None,
                "true_negatives": int(tn),
                "false_positives": int(fp),
                "false_negatives": int(fn),
                "true_positives": int(tp),
                "validation_size": len(df)
            },
            "confusion_matrix": cm.tolist()
        }
        
        import json
        with open("models/external_validation_results.json", "w") as f:
            json.dump(results, f, indent=2)
        
        logger.info(f"\nResults saved to: models/external_validation_results.json")
        
        return results
    
    else:
        logger.error("No valid predictions generated")
        return None

if __name__ == "__main__":
    validate_on_external_dataset()
