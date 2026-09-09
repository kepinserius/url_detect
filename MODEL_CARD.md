# Model Card: Phishing URL Detector

## Model Overview

**Name**: Phishing URL XGBoost Classifier  
**Version**: 1.0.0  
**Date**: 2026-09-09  
**Type**: Binary Classification (Phishing vs Legitimate URLs)  
**Framework**: XGBoost

## Intended Use

### Primary Use Cases
- Security tools integration (browser extensions, email filters, chat security)
- Real-time URL screening for web applications
- Threat intelligence platforms
- Security operations centers (SOCs)

### Out-of-Scope Uses
- **NOT a guarantee**: This is a probabilistic model, not a security certification
- **NOT for legal evidence**: Should not be used as sole evidence in legal proceedings
- **NOT for blocking without review**: High-stakes decisions should involve human review

## Training Data

**Dataset**: PhiUSIIL Phishing URL Dataset (UCI ML Repository)  
**License**: CC BY 4.0  
**Size**: 235,795 samples  
**Label Distribution**:
- Phishing: 134,850 (57.2%)
- Legitimate: 100,945 (42.8%)

**Features**: 50 URL-based and content-based features including:
- URL structure (length, domain, TLD, special characters)
- Content indicators (HTML elements, JavaScript, redirects)
- Security signals (HTTPS, certificates)

**Preprocessing**:
- Duplicate removal
- Missing value imputation
- No URL fetching (static analysis only)

## Model Architecture

**Algorithm**: XGBoost (Extreme Gradient Boosting)  
**Hyperparameters** (tuned with Optuna):
- n_estimators: 185
- max_depth: 6
- learning_rate: 0.0155
- subsample: 0.96
- colsample_bytree: 0.82
- gamma: 3.45
- reg_alpha: 9.10
- reg_lambda: 0.08

## Performance Metrics

**Test Set (20% split, 47,159 samples)**:
- **Accuracy**: 1.0
- **Precision**: 1.0
- **Recall**: 1.0
- **F1 Score**: 1.0
- **ROC-AUC**: 1.0

**Note**: Perfect metrics on this dataset. Real-world performance may vary due to:
- Evolving phishing techniques
- Dataset bias
- Domain shift

## Limitations & Biases

### Known Limitations
1. **Temporal bias**: Trained on historical data. Phishing techniques evolve rapidly.
2. **Dataset bias**: PhiUSIIL may not represent all phishing types (spear phishing, SMS phishing, etc).
3. **Static analysis only**: Cannot detect dynamically generated phishing pages or advanced obfuscation.
4. **Language bias**: Dataset may overrepresent English-language URLs.
5. **Feature availability**: Some features (e.g., LineOfCode, HasTitle) require HTML content, not just URL string.

### False Negatives Risk
**⚠️ False Negatives Risk**
**Critical risk**: Missing a phishing URL exposes users to security risk. This model achieves 0% false negative rate on our test set (36 URLs), but real-world phishing may include new patterns not represented. Use this model as one signal among many security layers, not the sole decision-maker.

### False Positives Risk
Legitimate URLs misclassified as phishing can disrupt user workflows. On our test set, we achieve 0% false positives. Consider implementing confidence thresholds and human review for borderline cases in production deployments.

### Important Limitations
- Model trained on 2024-2025 data (PhiUSIIL dataset)
- May not detect novel phishing techniques developed after 2025
- Performance may degrade without regular retraining
- Hybrid approach may miss highly sophisticated phishing campaigns
- Always validate critical security decisions with additional checks

## Ethical Considerations

- **Privacy**: No URL is stored or transmitted to external servers by default (self-hosted mode)
- **Transparency**: Model decision-making is based on interpretable features
- **Accessibility**: Open-source enables community auditing and improvement

## Maintenance & Updates

**Recommended retraining frequency**: Every 3-6 months or when performance degrades  
**Monitoring**: Track false positive/negative rates in production  
**Feedback loop**: Collect misclassification reports for model improvement

## Contact & Feedback

Report issues or provide feedback via:
- GitHub Issues: https://github.com/kepinserius/phishing-url-detector/issues
- Security concerns: security@phishing-detector.kepinserius.dev

## References

- UCI PhiUSIIL Dataset: https://archive.ics.uci.edu/dataset/967/phiusiil+phishing+url+dataset
- Model repository: https://github.com/kepinserius/phishing-url-detector
