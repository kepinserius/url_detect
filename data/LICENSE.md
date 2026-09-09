# PhiUSIIL Phishing URL Dataset

## Source
UCI Machine Learning Repository: [PhiUSIIL Phishing URL Dataset](https://archive.ics.uci.edu/dataset/967/phiusiil+phishing+url+dataset)

## License
The PhiUSIIL dataset is provided by the UCI Machine Learning Repository.

**License**: Creative Commons Attribution 4.0 International (CC BY 4.0)

You are free to:
- Share: copy and redistribute the material in any medium or format
- Adapt: remix, transform, and build upon the material for any purpose, even commercially

Under the following terms:
- Attribution: You must give appropriate credit, provide a link to the license, and indicate if changes were made.

## Citation
If you use this dataset, please cite:

```
Chiew, K. L., Yong, K. S. C., & Tan, C. L. (2018). 
A survey of phishing attacks: Their types, vectors and technical approaches. 
Expert Systems with Applications, 106, 1-20.
```

## Download Instructions
1. Visit: https://archive.ics.uci.edu/dataset/967/phiusiil+phishing+url+dataset
2. Download the dataset
3. Extract to: `data/raw/PhiUSIIL_Phishing_URL_Dataset.csv`

## Dataset Description
- **Total samples**: 235,795
- **Features**: 56 columns (URL-based and content-based features)
- **Labels**: Binary (0=legitimate, 1=phishing)
- **Label distribution**:
  - Phishing (1): 134,850
  - Legitimate (0): 100,945

## Features
The dataset includes:
- URL-based features (length, domain, TLD, special characters)
- Content-based features (HTML elements, JavaScript, CSS)
- Security indicators (HTTPS, certificates, redirects)

## Important Notes
1. **No automatic redistribution**: This repository does NOT include the dataset file itself.
2. **User responsibility**: Users must download the dataset themselves from UCI ML Repository.
3. **License compliance**: Ensure you comply with CC BY 4.0 terms.
4. **Attribution required**: Always cite the original dataset source.

## Preprocessing
After download, run:
```bash
PYTHONPATH=. python3 training/train.py
```

This will:
- Validate dataset integrity
- Clean duplicates and missing values
- Train models
- Generate evaluation reports
