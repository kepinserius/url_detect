# Model Documentation

## Overview

The Phishing URL Detector uses supervised machine learning to classify URLs as phishing or legitimate based on static URL features and content-based indicators.

## Model Selection

### Baseline Models Evaluated
1. **XGBoost** (Selected)
2. Random Forest
3. Logistic Regression

### Selection Criteria
- F1 Score (primary metric)
- ROC-AUC
- PR-AUC
- Training time
- Inference latency

**Winner**: XGBoost with hyperparameter tuning

## Features (50 total)

### URL Structure Features
- `URLLength`: Total character count
- `DomainLength`: Domain name length
- `IsDomainIP`: Boolean, if domain is IP address
- `TLDLength`: Top-level domain length
- `NoOfSubDomain`: Number of subdomains
- `NoOfEqualsInURL`: Count of '=' characters
- `NoOfQMarkInURL`: Count of '?' characters
- `NoOfAmpersandInURL`: Count of '&' characters
- `NoOfOtherSpecialCharsInURL`: Count of special characters
- `SpacialCharRatioInURL`: Ratio of special chars to total length
- `IsHTTPS`: Boolean, HTTPS protocol

### Content-Based Features
- `LineOfCode`: HTML line count
- `LargestLineLength`: Max line length
- `HasTitle`: Boolean, title tag present
- `DomainTitleMatchScore`: Domain-title similarity
- `URLTitleMatchScore`: URL-title similarity
- `HasFavicon`: Boolean, favicon present
- `Robots`: robots.txt status
- `IsResponsive`: Responsive design indicator
- `NoOfURLRedirect`: Redirect count
- `NoOfSelfRedirect`: Self-redirect count
- `HasDescription`: Meta description present
- `NoOfPopup`: Popup count
- `NoOfiFrame`: iFrame count
- `HasExternalFormSubmit`: External form action
- `HasSocialNet`: Social media links present
- `HasSubmitButton`: Submit button present
- `HasHiddenFields`: Hidden input fields
- `HasPasswordField`: Password input present
- `Bank`: Banking keyword presence
- `Pay`: Payment keyword presence
- `Crypto`: Crypto keyword presence
- `HasCopyrightInfo`: Copyright notice
- `NoOfImage`: Image count
- `NoOfCSS`: CSS file count
- `NoOfJS`: JavaScript file count
- `NoOfSelfRef`: Self-reference count
- `NoOfEmptyRef`: Empty reference count
- `NoOfExternalRef`: External reference count

### Advanced Features
- `URLSimilarityIndex`: Similarity to known phishing patterns
- `CharContinuationRate`: Character repetition rate
- `TLDLegitimateProb`: TLD legitimacy probability
- `URLCharProb`: Character probability distribution
- `HasObfuscation`: Boolean, obfuscation detected
- `NoOfObfuscatedChar`: Obfuscated character count
- `ObfuscationRatio`: Obfuscation ratio
- `NoOfLettersInURL`: Letter count
- `LetterRatioInURL`: Letter ratio
- `NoOfDegitsInURL`: Digit count
- `DegitRatioInURL`: Digit ratio

## Training Pipeline

### 1. Data Validation
```python
from training.preprocessing.validator import DataValidator

validator = DataValidator()
report = validator.validate(df, required_cols=['label'])
```

Checks:
- Duplicates
- Missing values
- Label corruption
- Column presence

### 2. Data Cleaning
```python
from training.preprocessing.cleaner import DataCleaner

cleaner = DataCleaner()
df_clean = cleaner.clean(df)
```

Operations:
- Remove duplicates
- Drop null labels
- Filter invalid labels
- Impute missing values

### 3. Feature Engineering
Already provided in PhiUSIIL dataset. For new URLs:
```python
from inference.features.extractor import URLFeatureExtractor

features = URLFeatureExtractor.extract_features(url)
```

### 4. Model Training
```python
from training.models.trainer import ModelTrainer

trainer = ModelTrainer(random_state=42)
models = trainer.train(X_train, y_train)
evaluation = trainer.evaluate(models, X_test, y_test)
```

### 5. Hyperparameter Tuning
```python
from training.models.tuner import ModelTuner

tuner = ModelTuner(cv_folds=3)
best_params, best_score = tuner.tune_xgboost(X_train, y_train, n_trials=50)
```

Optimized with Optuna:
- Cross-validation (3-5 folds)
- Bayesian optimization
- 50-100 trials
- Target metric: F1 or ROC-AUC

### 6. Evaluation
```python
from training.models.evaluator import EvaluationReportGenerator

evaluator = EvaluationReportGenerator()
report = evaluator.generate(y_test, y_pred, y_pred_proba, model_name, feature_count)
```

Generates:
- JSON metrics report
- Confusion matrix visualization
- Classification report

## Model Performance

### XGBoost (Tuned)
**Test Set Performance (47,159 samples)**:
- Accuracy: 1.0
- Precision: 1.0
- Recall: 1.0
- F1 Score: 1.0
- ROC-AUC: 1.0
- PR-AUC: 1.0

**Hyperparameters**:
```python
{
    "n_estimators": 185,
    "max_depth": 6,
    "learning_rate": 0.0155,
    "subsample": 0.96,
    "colsample_bytree": 0.82,
    "gamma": 3.45,
    "reg_alpha": 9.10,
    "reg_lambda": 0.08
}
```

**Training Time**: ~0.7s (100 estimators baseline)  
**Inference Time**: <10ms per URL

### Confusion Matrix
```
                Predicted
              Legitimate  Phishing
Actual  Legit    20124        0
        Phish        0    27035
```

## Model Limitations

### 1. Perfect Test Performance
The model achieves perfect scores on PhiUSIIL test set. This suggests:
- High-quality, clean dataset
- May not generalize to all real-world scenarios
- Requires validation on external/live data

### 2. Feature Dependency
Some features require HTML content:
- `LineOfCode`, `HasTitle`, `NoOfImage`, etc.
- For URL-only inference, these are set to 0
- May reduce accuracy for URL-only predictions

### 3. Temporal Drift
- Phishing techniques evolve
- Model trained on historical data
- Recommend retraining every 3-6 months

### 4. Dataset Bias
- PhiUSIIL may not cover all phishing types
- Possible language/geographic bias
- Limited to URL-based attacks (not SMS, voice, etc.)

### 5. Static Analysis Only
- Cannot detect dynamic content changes
- No JavaScript execution
- No screenshot/visual analysis

## Production Considerations

### Model Versioning
```json
{
  "active_model": "phishing-url-xgb-1.0.0",
  "models": [
    {
      "name": "phishing-url-xgb",
      "version": "1.0.0",
      "file": "xgboost_tuned_model.joblib",
      "metrics": {...}
    }
  ]
}
```

### Model Registry
- `models/registry.json`: Metadata tracking
- `models/evaluation_report.json`: Performance metrics
- `models/tuning_report.json`: Hyperparameter search results

### Retraining Process
1. Collect new labeled data
2. Merge with existing dataset
3. Run `training/train.py`
4. Evaluate on held-out test set
5. Compare metrics with current model
6. Update registry and deploy if improved

### A/B Testing
For production deployments:
- Serve multiple model versions
- Split traffic (e.g., 90% v1.0, 10% v1.1)
- Monitor performance metrics
- Gradual rollout

## Inference Pipeline

```python
from inference.predictor import Predictor

predictor = Predictor()
result = predictor.predict("https://example.com")
# {"prediction": "legitimate", "risk_score": 5.2, "confidence": 0.948}
```

### Prediction Logic
1. Extract features from URL
2. Align features with training schema
3. Fill missing features with 0
4. Model inference (XGBoost predict_proba)
5. Threshold at 0.5
6. Return prediction + confidence

### Confidence Interpretation
- **High confidence (>0.9)**: Strong signal
- **Medium confidence (0.7-0.9)**: Likely correct
- **Low confidence (<0.7)**: Uncertain, manual review recommended

## Future Improvements

### Short-term
- Ensemble methods (stacking multiple models)
- Feature importance analysis
- SHAP/LIME explainability
- Calibration (probability calibration)

### Long-term
- Deep learning (BERT for URL embeddings)
- Real-time feature extraction (optional HTML fetch)
- Visual similarity detection (screenshot comparison)
- Active learning (user feedback loop)

## References

- XGBoost: Chen & Guestrin (2016), "XGBoost: A Scalable Tree Boosting System"
- PhiUSIIL Dataset: UCI ML Repository
- Optuna: Akiba et al. (2019), "Optuna: A Next-generation Hyperparameter Optimization Framework"

## Support

- Model issues: https://github.com/your-username/phishing-url-detector/issues
- Training questions: See `CONTRIBUTING.md`
- Security concerns: `SECURITY.md`
