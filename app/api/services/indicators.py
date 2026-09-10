"""
Indicators Service - Generate explainable indicators for predictions.

Returns human-readable reasons why a URL was flagged as phishing or legitimate.
"""

from typing import List, Dict, Any
import re

class IndicatorsService:
    """
    Generate explainable indicators for phishing detection results.
    """
    
    def __init__(self):
        self.suspicious_tlds = {
            'tk', 'ml', 'ga', 'cf', 'gq', 'pw', 'cc', 'xyz', 'top', 'work',
            'date', 'stream', 'download', 'review', 'club', 'loan', 'racing'
        }
        
        self.brand_keywords = {
            'paypal', 'facebook', 'google', 'amazon', 'apple', 'microsoft',
            'netflix', 'instagram', 'twitter', 'linkedin', 'bank', 'secure',
            'login', 'verify', 'account', 'update', 'confirm', 'suspended'
        }
    
    def generate(self, url: str, prediction: str, details: Dict[str, Any]) -> List[str]:
        """
        Generate indicators explaining the prediction.
        
        Args:
            url: The URL that was checked
            prediction: 'phishing' or 'legitimate'
            details: Prediction details including rule scores
            
        Returns:
            List of indicator strings
        """
        indicators = []
        
        # URL features
        parsed = self._parse_url(url)
        
        # Phishing indicators
        if prediction == "phishing":
            if details.get("rule_score", 0) > 0.8:
                indicators.append("multiple phishing patterns detected")
            if details.get("suspicious_tld"):
                indicators.append("suspicious TLD detected")
            if details.get("typosquatting"):
                indicators.append(f"typosquatting pattern detected (similar to {details.get('typosquatting')})")
            if details.get("brand_abuse"):
                indicators.append(f"suspicious brand usage (contains '{details.get('brand_abuse')}')")
            if parsed.get("has_ip"):
                indicators.append("IP address in URL instead of domain")
            if parsed.get("has_long_domain"):
                indicators.append("unusually long domain name")
            if parsed.get("has_excessive_hyphens"):
                indicators.append("excessive hyphens in domain")
            if parsed.get("has_many_special_chars"):
                indicators.append("high number of special characters")
            if parsed.get("has_long_path"):
                indicators.append("unusually long URL path")
                
        # Legitimate indicators
        else:
            if parsed.get("is_https"):
                indicators.append("uses HTTPS protocol")
            if parsed.get("has_known_tld"):
                indicators.append("uses common TLD")
            if parsed.get("has_short_domain"):
                indicators.append("short domain name (typical for legitimate sites)")
            if parsed.get("has_clean_url"):
                indicators.append("clean URL structure without suspicious elements")
            if details.get("rule_score", 0) < 0.3:
                indicators.append("no suspicious patterns detected")
        
        # Limit to top 5 indicators
        return indicators[:5]
    
    def _parse_url(self, url: str) -> Dict[str, Any]:
        """Parse URL and extract features for indicators."""
        from urllib.parse import urlparse
        
        parsed = urlparse(url)
        hostname = parsed.hostname or ""
        
        # Count characters
        num_hyphens = hostname.count("-")
        num_special = sum(1 for c in url if not c.isalnum() and c not in ":/.?=&#")
        
        # TLD check
        tld = hostname.split(".")[-1] if hostname else ""
        
        return {
            "is_https": parsed.scheme == "https",
            "has_ip": bool(re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", hostname)),
            "has_long_domain": len(hostname) > 40,
            "has_excessive_hyphens": num_hyphens > 4,
            "has_many_special_chars": num_special > 10,
            "has_long_path": len(parsed.path) > 50,
            "has_known_tld": tld not in self.suspicious_tlds,
            "has_short_domain": len(hostname) < 20,
            "has_clean_url": num_hyphens < 2 and num_special < 5,
        }


# Global instance
indicators_service = IndicatorsService()
