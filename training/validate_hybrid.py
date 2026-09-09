import logging
import pandas as pd
from inference.hybrid_predictor import HybridPredictor
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, f1_score, accuracy_score
import numpy as np

logging.basicConfig(level=logging.INFO)

def test_hybrid_predictor():
    logger = logging.getLogger(__name__)
    logger.info("Testing Hybrid Predictor (ML + Rule-based)...")
    
    predictor = HybridPredictor()
    
    # Updated test set with better examples
    test_data = [
        # Legitimate (0) - Clear legitimate domains
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
        ("https://youtube.com", 0),
        ("https://amazon.com", 0),
        
        # Obvious phishing (1) - Common patterns
        ("https://facebok.com", 1),  # Typosquatting
        ("https://gogle.com", 1),    # Typosquatting
        ("https://gooogle.com", 1),  # Typosquatting
        ("https://paypa1.com", 1),   # Typosquatting (l→1)
        ("https://paypal-login.xyz", 1),  # Suspicious TLD + brand
        ("https://facebook-secure-login.tk", 1),  # Suspicious TLD + brand
        ("https://secure-bank-login.cc", 1),  # Suspicious TLD + keywords
        ("https://instagram-verify-code.ml", 1),  # Suspicious TLD + brand
        ("https://whatsapp-web-free.ru", 1),  # Suspicious ccTLD + brand
        ("https://amazon-gift-card-claim.ga", 1),  # Suspicious ccTLD + brand
        
        # More phishing with suspicious TLDs
        ("https://apple-id-verification.xyz", 1),
        ("http://microsoft-account-update.cf", 1),
        ("https://google-drive-security-alert.gq", 1),
        ("https://dropbox-file-sharing-notification.cc", 1),
        
        # Suspicious patterns
        ("http://192.168.1.1:8080/login.php?user=admin&pass=1234", 1),  # IP address
        ("https://very-long-domain-name-with-dashes-and-numbers-12345.com/login/verify", 1),  # Excessive characters
        
        # Legitimate with query params
        ("https://github.com/login?return_to=%2Fdashboard", 0),
        ("https://facebook.com/dialog/oauth?client_id=123&redirect_uri=...", 0),
        
        # Edge cases
        ("https://example.com/login?token=secret&password=123&email=user@domain.com", 0),  # Legit with params
        ("https://login.live.com", 0),  # Legit subdomain
        ("https://account.google.com", 0),  # Legit subdomain
        
        # Additional phishing patterns
        ("https://paypal-update.secure.tk", 1),  # Multi-subdomain + brand
        ("http://verify-appleid.xyz", 1),  # Brand + suspicious TLD
        ("https://microsoft-online-confirmation.gq", 1),  # Brand + suspicious TLD
    ]
    
    urls, true_labels = zip(*test_data)
    predictions = []
    results = []
    
    logger.info(f"Testing {len(test_data)} URLs...\n")
    
    correct = 0
    false_negatives = []
    false_positives = []
    
    for i, (url, true_label) in enumerate(test_data):
        try:
            result = predictor.predict(url)
            pred_label = 1 if result['prediction'] == 'phishing' else 0
            is_correct = pred_label == true_label
            
            predictions.append(pred_label)
            results.append({
                "url": url,
                "true_label": true_label,
                "pred_label": pred_label,
                "prediction": result['prediction'],
                "risk_score": result['risk_score'],
                "confidence": result['confidence'],
                "method": result['method'],
                "details": result['details']
            })
            
            if is_correct:
                correct += 1
                status = "✓"
            else:
                status = "✗"
                if true_label == 1 and pred_label == 0:
                    false_negatives.append(url)
                elif true_label == 0 and pred_label == 1:
                    false_positives.append(url)
            
            if i < 15:  # Log first 15
                true_desc = "Phishing" if true_label else "Legitimate"
                logger.info(f"{status} {url[:45]:45} | True: {true_desc:10} | Pred: {result['prediction']:10} | Score: {result['risk_score']:5.1f}% | Method: {result['method'][:15]}")
                
        except Exception as e:
            logger.error(f"Error predicting {url}: {e}")
            predictions.append(0)
    
    # Calculate metrics
    if predictions:
        y_true = np.array(true_labels)
        y_pred = np.array(predictions)
        
        acc = accuracy_score(y_true, y_pred)
        f1 = f1_score(y_true, y_pred)
        precision = classification_report(y_true, y_pred, output_dict=True)['weighted avg']['precision']
        recall = classification_report(y_true, y_pred, output_dict=True)['weighted avg']['recall']
        
        cm = confusion_matrix(y_true, y_pred)
        tn, fp, fn, tp = cm.ravel()
        
        logger.info("\n" + "="*70)
        logger.info("HYBRID PREDICTOR RESULTS")
        logger.info("="*70)
        logger.info(f"Test Size: {len(test_data)} URLs")
        logger.info(f"Accuracy:  {acc:.4f} ({correct}/{len(test_data)})")
        logger.info(f"Precision: {precision:.4f}")
        logger.info(f"Recall:    {recall:.4f}")
        logger.info(f"F1 Score:  {f1:.4f}")
        
        logger.info(f"\nConfusion Matrix:")
        logger.info(f"True Negatives (Legitimate correct):    {tn}")
        logger.info(f"False Positives (Legitimate as Phish):  {fp}")
        logger.info(f"False Negatives (Phishing as Legit):    {fn}")
        logger.info(f"True Positives (Phishing correct):      {tp}")
        
        logger.info(f"\nFalse Negative Rate: {fn/(fn+tp+1e-10):.2%} ({fn} missed phishing URLs)")
        logger.info(f"False Positive Rate: {fp/(fp+tn+1e-10):.2%} ({fp} false alarms)")
        
        if false_negatives:
            logger.info(f"\n⚠️  FALSE NEGATIVES ({len(false_negatives)} phishing URLs missed):")
            for url in false_negatives[:5]:
                logger.info(f"  - {url[:60]}")
            if len(false_negatives) > 5:
                logger.info(f"  ... and {len(false_negatives) - 5} more")
        
        if false_positives:
            logger.info(f"\n⚠️  FALSE POSITIVES ({len(false_positives)} legitimate URLs flagged):")
            for url in false_positives[:5]:
                logger.info(f"  - {url[:60]}")
        
        if not false_negatives and not false_positives:
            logger.info(f"\n🎉 PERFECT CLASSIFICATION! All {len(test_data)} URLs correct.")
        
        # Save results
        import json
        detailed_results = {
            "metrics": {
                "accuracy": float(acc),
                "precision": float(precision),
                "recall": float(recall),
                "f1_score": float(f1),
                "confusion_matrix": cm.tolist(),
                "false_negative_rate": float(fn/(fn+tp+1e-10)),
                "false_positive_rate": float(fp/(fp+tn+1e-10))
            },
            "test_summary": {
                "total_urls": len(test_data),
                "phishing_urls": sum(true_labels),
                "legitimate_urls": len(test_data) - sum(true_labels),
                "correct_predictions": correct
            },
            "false_negatives": false_negatives,
            "false_positives": false_positives
        }
        
        with open("models/hybrid_validation_results.json", "w") as f:
            json.dump(detailed_results, f, indent=2)
        
        logger.info(f"\n✓ Detailed results saved to: models/hybrid_validation_results.json")
        
        return detailed_results
    else:
        logger.error("No predictions generated")
        return None

if __name__ == "__main__":
    test_hybrid_predictor()
