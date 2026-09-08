import pandas as pd
import numpy as np
import sys
import os

sys.path.append('.')
from training.features.extractor import URLFeatureExtractor

def generate_synthetic_phiusiil_dataset():
    extractor = URLFeatureExtractor()
    
    # Representative URLs: Legitimate vs Phishing
    legitimate_urls = [
        "https://www.google.com",
        "https://www.github.com/torvalds/linux",
        "https://en.wikipedia.org/wiki/Main_Page",
        "https://www.microsoft.com/en-us/",
        "https://www.amazon.com/dp/B08N5WRWNW",
        "https://www.python.org/downloads/",
        "https://fastapi.tiangolo.com/tutorial/",
        "https://pypi.org/project/scikit-learn/",
        "https://news.ycombinator.com/",
        "https://stackoverflow.com/questions/tagged/python",
        "https://www.apple.com/macbook-pro/",
        "https://www.bbc.com/news",
        "https://www.nytimes.com/",
        "https://medium.com/@user/article-title",
        "https://www.reddit.com/r/programming/",
        "https://www.cloudflare.com/learning/ddos/what-is-ddos/",
        "https://docs.python.org/3/library/urllib.parse.html",
        "https://developer.mozilla.org/en-US/docs/Web/JavaScript",
        "https://archive.org/web/",
        "https://www.docker.com/products/docker-desktop/"
    ] * 50  # Multiply to create a decent synthetic dataset size (1000 samples)

    phishing_urls = [
        "http://192.168.1.1/login/verify.php?account=update",
        "https://paypal-security-update-center-login.com/login.html",
        "http://secure-banking-verify-update.net/signin/",
        "https://appleid-apple-com-verify-account.tk/index.php",
        "http://www.google-login-security-account.top/auth",
        "http://203.0.113.45/ebayISAPI.dll?SignIn",
        "https://accounts-google-com-login.xyz/serve/index.html",
        "http://login-amazon-com-security-check.info/update.php",
        "http://verify-your-bank-account-online.com/auth/login",
        "http://198.51.100.12/wp-content/plugins/fix/login.php",
        "https://microsoft-online-account-security.cf/login",
        "http://netflix-billing-update-required.online/verify",
        "https://facebook-account-confirmation-code.site/security",
        "http://instagram-login-verify-badge.cc/auth",
        "http://192.0.2.1/bank/of/america/login.htm",
        "https://wellsfargo-online-banking-secure.me/signon",
        "http://chase-bank-account-verification-service.tech/login",
        "http://dhl-parcel-tracking-update-delivery.info/shipment",
        "https://ups-package-redelivery-notice.xyz/confirm",
        "http://crypto-wallet-seed-phrase-verification.top/restore"
    ] * 50

    data = []
    # In PhiUSIIL dataset, label 1 is Legitimate, 0 is Phishing (or vice versa - we standardise 1=Phishing, 0=Legitimate for our core model)
    for url in legitimate_urls:
        feats = extractor.extract(url)
        feats['url'] = url
        feats['label'] = 0 # Legitimate
        data.append(feats)

    for url in phishing_urls:
        feats = extractor.extract(url)
        feats['url'] = url
        feats['label'] = 1 # Phishing
        data.append(feats)

    df = pd.DataFrame(data)
    os.makedirs('data/processed', exist_ok=True)
    df.to_csv('data/processed/dataset.csv', index=False)
    print(f"Generated dataset with {len(df)} records. Sample counts:")
    print(df['label'].value_counts())

if __name__ == '__main__':
    generate_synthetic_phiusiil_dataset()
