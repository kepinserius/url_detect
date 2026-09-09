import re
import pandas as pd
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

class PhiUSIILFeatureExtractor:
    @staticmethod
    def extract_all(url: str) -> dict:
        parsed = urlparse(url)
        hostname = parsed.hostname or ""
        path = parsed.path or ""
        query = parsed.query or ""
        
        # Basic URL features
        url_length = len(url)
        domain_length = len(hostname)
        path_length = len(path)
        has_ip = 1 if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", hostname) else 0
        is_https = 1 if parsed.scheme == "https" else 0
        
        # Count features
        num_dots = url.count(".")
        num_hyphens = url.count("-")
        num_at = url.count("@")
        num_question = url.count("?")
        num_percent = url.count("%")
        num_equal = url.count("=")
        num_ampersand = url.count("&")
        num_slash = url.count("/")
        num_digits = sum(c.isdigit() for c in url)
        num_letters = sum(c.isalpha() for c in url)
        
        # Subdomain analysis
        parts = hostname.split(".")
        num_subdomain = max(0, len(parts) - 2) if len(parts) > 1 else 0
        
        # Special character ratios
        sp_chars = ['@', '#', '$', '%', '&', '*', '+', '=', '_', '-', '~', '^', '|']
        num_special = sum(url.count(c) for c in sp_chars)
        
        # TLD analysis (simplified)
        tld = parts[-1] if parts else ""
        tld_length = len(tld)
        
        # URL similarity and pattern features (simplified)
        url_similarity_index = 0  # Would require known phishing patterns
        char_continuation_rate = 0  # Would require sequence analysis
        
        # Build feature dict matching PhiUSIIL training columns
        features = {
            # Exact columns from training
            "URLLength": url_length,
            "DomainLength": domain_length,
            "IsDomainIP": has_ip,
            "URLSimilarityIndex": url_similarity_index,
            "CharContinuationRate": char_continuation_rate,
            "TLDLegitimateProb": 0.5,  # Default neutral
            "URLCharProb": 0.5,
            "TLDLength": tld_length,
            "NoOfSubDomain": num_subdomain,
            "HasObfuscation": 1 if num_special > 5 else 0,
            "NoOfObfuscatedChar": num_special,
            "ObfuscationRatio": num_special / url_length if url_length > 0 else 0,
            "NoOfLettersInURL": num_letters,
            "LetterRatioInURL": num_letters / url_length if url_length > 0 else 0,
            "NoOfDegitsInURL": num_digits,
            "DegitRatioInURL": num_digits / url_length if url_length > 0 else 0,
            "NoOfEqualsInURL": num_equal,
            "NoOfQMarkInURL": num_question,
            "NoOfAmpersandInURL": num_ampersand,
            "NoOfOtherSpecialCharsInURL": num_special - (num_equal + num_question + num_ampersand),
            "SpacialCharRatioInURL": num_special / url_length if url_length > 0 else 0,
            "IsHTTPS": is_https,
            # Content-based features (set to 0 - require HTML content)
            "LineOfCode": 0,
            "LargestLineLength": 0,
            "HasTitle": 0,
            "DomainTitleMatchScore": 0,
            "URLTitleMatchScore": 0,
            "HasFavicon": 0,
            "Robots": 0,
            "IsResponsive": 0,
            "NoOfURLRedirect": 0,
            "NoOfSelfRedirect": 0,
            "HasDescription": 0,
            "NoOfPopup": 0,
            "NoOfiFrame": 0,
            "HasExternalFormSubmit": 0,
            "HasSocialNet": 0,
            "HasSubmitButton": 0,
            "HasHiddenFields": 0,
            "HasPasswordField": 0,
            "Bank": 0,
            "Pay": 0,
            "Crypto": 0,
            "HasCopyrightInfo": 0,
            "NoOfImage": 0,
            "NoOfCSS": 0,
            "NoOfJS": 0,
            "NoOfSelfRef": 0,
            "NoOfEmptyRef": 0,
            "NoOfExternalRef": 0,
        }
        
        return features
