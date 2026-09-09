import pandas as pd
import json
import logging
from inference.improved_predictor import ImprovedPredictor
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, f1_score, accuracy_score

logging.basicConfig(level=logging.INFO)

def validate_improved():
    logger = logging.getLogger(__name__)
    logger.info("Testing improved model with threshold 0.7...")
    
    predictor = ImprovedPredictor()
    
    # Test dataset with clear phishing patterns
    test_data = [
        # Legitimate (0)
        ("https://google.com", 0),
        ("https://facebook.com", 0),
        ("https://github.com", 0),
        ("https://stackoverflow.com", 0),
        ("https://wikipedia.org", 0),
        ("https://twitter.com", 0),
        ("https://linkedin.com", 0),
        ("https://microsoft.com", 0),
        ("https://apple.com", 0),
        ("https://netflix.com", 0),
        
        # Obvious phishing (1)
        ("https://facebok.com", 1),
        ("https://gogle.com", 1),
        ("https://gooogle.com", 1),
        ("https://paypa1.com", 1),
        ("https://paypal-login.xyz", 1),
        ("https://facebook-secure-login.tk", 1),
        ("https://secure-bank-login.cc", 1),
        ("https://instagram-verify-code.ml", 1),
        ("https://whatsapp-web-free.ru", 1),
        ("https://amazon-gift-card-claim.ga", 1),
        
        # More phishing with suspicious TLDs
        ("https://apple-id-verification.xyz", 1),
        ("http://microsoft-account-update.cf", 1),
        ("https://google-drive-security-alert.gq", 1),
        ("https://dropbox-file-sharing-notification.cc", 1),
        
        # Suspicious patterns
        ("http://192.168.1.1:8080/login.php?user=admin&pass=1234", 1),
        ("https://very-long-domain-name-with-dashes-and-numbers-12345.com/login/verify", 1),
        
        # Legitimate with query params
        ("https://github.com/login?return_to=%2Fdashboard", 0),
        ("https://facebook.com/dialog/oauth?client_id=123&redirect_uri=...", 0),
    ]
    
    urls, true_labels = zip(*test_data)
    predictions = []
    probabilities = []
    results = []
    
    logger.info(f"Testing {len(test_data)} URLs...")
    
    for i, (url, true_label) in enumerate(test_data):
        try:
            result = predictor.predict(url)
            pred_label = 1 if result['prediction'] == 'phishing' else 0
            
            predictions.append(pred_label)
            probabilities.append(result['raw_probability'])
            results.append({
                "url": url,
                "true_label": true_label,
                "pred_label": pred_label,
                "prediction": result['prediction'],
                "risk_score": result['risk_score'],
                "confidence": result['confidence']
            })
            
            if i < 8:  # Log first few
                status = "✓" if pred_label == true_label else "✗"
                logger.info(f"{status} URL: {url[:40]:40} | True: {'Phishing' if true_label else 'Legit'} | Pred: {result['prediction']:10} | Score: {result['risk_score']:5.1f}% | Conf: {result['confidence']:.3f}")
                
        except Exception as e:
            logger.error(f"Error predicting {url}: {e}")
            predictions.append(0)
            probabilities.append(0.0)
    
    # Calculate metrics
    if predictions:
        y_true = np.array(true_labels)
        y_pred = np.array(predictions)
        y_prob = np.array(probabilities)
        
        acc = accuracy_score(y_true, y_pred)
        f1 = f1_score(y_true, y_pred)
        
        # Handle ROC-AUC carefully
        if len(np.unique(y_true)) > 1:
            roc_auc = roc_auc_score(y_true, y_prob)
        else:
            roc_auc = None
        
        cm = confusion_matrix(y_true, y_pred)
        tn, fp, fn, tp = cm.ravel()
        
        logger.info("\n" + "="*60)
        logger.info("IMPROVED MODEL VALIDATION RESULTS")
        logger.info("="*60)
        logger.info(f"Test Size: {len(test_data)} URLs")
        logger.info(f"Accuracy:  {acc:.4f}")
        logger.info(f"F1 Score:  {f1:.4f}")
        if roc_auc:
            logger.info(f"ROC-AUC:   {roc_auc:.4f}")
        
        logger.info(f"\nConfusion Matrix:")
        logger.info(f"True Negatives (Legit correct):    {tn}")
        logger.info(f"False Positives (Legit as Phish):  {fp}")
        logger.info(f"False Negatives (Phish as Legit):  {fn}")
        logger.info(f"True Positives (Phish correct):    {tp}")
        
        logger.info(f"\nFalse Negative Rate: {fn/(fn+tp+1e-10):.2%}")
        logger.info(f"False Positive Rate: {fp/(fp+tn+1e-10):.2%}")
        
        # Show misclassifications
        misclassified = [r for r in results if r['true_label'] != r['pred_label']]
        if misclassified:
            logger.info(f"\n⚠️  Misclassifications ({len(misclassified)}):")
            for r in misclassified:
                logger.info(f"  - {r['url'][:50]:50} | True: {r['true_label']} | Pred: {r['prediction']} | Score: {r['risk_score']:.1f}%")
        else:
            logger.info(f"\n🎉 PERFECT CLASSIFICATION! No errors.")
        
        # Save detailed results
        detailed_results = {
            "metrics": {
                "accuracy": float(acc),
                "f1_score": float(f1),
                "roc_auc": float(roc_auc) if roc_auc else None,
                "confusion_matrix": cm.tolist(),
                "false_negative_rate": float(fn/(fn+tp+1e-10)),
                "false_positive_rate": float(fp/(fp+tn+1e-10)),
                "threshold_used": predictor.threshold
            },
            "predictions": results
        }
        
        with open("models/improved_validation_results.json", "w") as f:
            json.dump(detailed_results, f, indent=2)
        
        logger.info(f"\n✓ Detailed results saved to: models/improved_validation_results.json")
        
        return detailed_results
    else:
        logger.error("No predictions generated")
        return None

if __name__ == "__main__":
    validate_improved()
