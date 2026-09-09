import re
from urllib.parse import urlparse
import tldextract

class RuleBasedPhishingDetector:
    """
    Rule-based phishing detection for common patterns.
    Complements ML model for better real-world accuracy.
    """
    
    SUSPICIOUS_TLDS = {
        'tk', 'ml', 'ga', 'cf', 'gq', 'pw', 'cc', 'xyz', 'top', 'work',
        'date', 'stream', 'download', 'review', 'club', 'loan', 'racing'
    }
    
    BRAND_KEYWORDS = {
        'paypal', 'facebook', 'google', 'amazon', 'apple', 'microsoft',
        'netflix', 'instagram', 'twitter', 'linkedin', 'dropbox', 'whatsapp',
        'bank', 'secure', 'login', 'signin', 'verify', 'account', 'update',
        'confirm', 'suspended', 'unusual', 'activity'
    }
    
    TYPOSQUATTING_PATTERNS = {
        'paypa1': 'paypal',
        'gogle': 'google',
        'gooogle': 'google',
        'facebok': 'facebook',
        'faceboook': 'facebook',
        'amazom': 'amazon',
        'micosoft': 'microsoft',
        'netfl1x': 'netflix',
    }
    
    @staticmethod
    def check_suspicious_tld(url: str) -> dict:
        """Check if TLD is commonly used for phishing"""
        extracted = tldextract.extract(url)
        tld = extracted.suffix.split('.')[-1] if extracted.suffix else ''
        
        is_suspicious = tld.lower() in RuleBasedPhishingDetector.SUSPICIOUS_TLDS
        return {
            'is_suspicious': is_suspicious,
            'tld': tld,
            'score': 0.7 if is_suspicious else 0.0
        }
    
    @staticmethod
    def check_typosquatting(url: str) -> dict:
        """Detect typosquatting attempts"""
        parsed = urlparse(url)
        domain = parsed.hostname or ''
        domain_lower = domain.lower()
        
        for typo, original in RuleBasedPhishingDetector.TYPOSQUATTING_PATTERNS.items():
            if typo in domain_lower:
                return {
                    'is_typosquatting': True,
                    'detected_pattern': typo,
                    'intended_brand': original,
                    'score': 0.95
                }
        
        return {'is_typosquatting': False, 'score': 0.0}
    
    OFFICIAL_DOMAINS = {
        'microsoft': ['microsoft.com', 'live.com', 'office.com', 'azure.com', 'onedrive.com', ' outlook.com', 'skype.com'],
        'apple': ['apple.com', 'icloud.com', 'icloud.com', 'me.com', 'mac.com'],
        'google': ['google.com', 'gmail.com', 'googlemail.com', 'youtube.com', 'youtube.com'],
        'facebook': ['facebook.com', 'fb.com'],
        'amazon': ['amazon.com', 'amazon.', 'aws.amazon.com'],
        'netflix': ['netflix.com'],
        'twitter': ['twitter.com', 'x.com'],
        'linkedin': ['linkedin.com', 'lnkd.in'],
        'instagram': ['instagram.com'],
        'github': ['github.com'],
        'stackoverflow': ['stackoverflow.com'],
        'wikipedia': ['wikipedia.org'],
    }
    
    @staticmethod
    def check_brand_abuse(url: str) -> dict:
        """Check for brand name + suspicious pattern"""
        parsed = urlparse(url)
        domain = parsed.hostname or ''
        domain_lower = domain.lower()
        
        # Check for brand keyword in non-official domain
        brand_found = None
        for brand in RuleBasedPhishingDetector.BRAND_KEYWORDS:
            if brand in domain_lower:
                brand_found = brand
                break
        
        if brand_found:
            # Check if it's suspicious (not the official domain)
            extracted = tldextract.extract(url)
            main_domain = extracted.domain.lower()
            
            # Check if it's an official subdomain
            for official_brand, official_domains in RuleBasedPhishingDetector.OFFICIAL_DOMAINS.items():
                if main_domain == official_brand or any(main_domain in od for od in official_domains):
                    return {'is_brand_abuse': False, 'score': 0.0}
            
            # Brand keyword but not official domain
            return {
                'is_brand_abuse': True,
                'brand': brand_found,
                'score': 0.8
            }
        
        return {'is_brand_abuse': False, 'score': 0.0}
    
    @staticmethod
    def check_suspicious_patterns(url: str) -> dict:
        """Check for suspicious URL patterns"""
        score = 0.0
        patterns = []
        
        parsed = urlparse(url)
        hostname = parsed.hostname or ''
        path = parsed.path or ''
        
        # IP address
        if re.match(r'https?://\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', url):
            patterns.append('ip_address')
            score += 0.6
        
        # Excessive hyphens (increased weight)
        hyphen_count = hostname.count('-')
        if hyphen_count > 4:
            patterns.append('excessive_hyphens')
            score += 0.5
        elif hyphen_count > 2:
            patterns.append('multiple_hyphens')
            score += 0.3
        
        # Excessive dots
        if hostname.count('.') > 4:
            patterns.append('excessive_subdomains')
            score += 0.5
        
        # Very long domain name
        domain_length = len(hostname)
        if domain_length > 40:
            patterns.append('very_long_domain')
            score += 0.6
        elif domain_length > 30:
            patterns.append('long_domain')
            score += 0.4
        
        # Numbers in domain (common in phishing)
        if re.search(r'\d{3,}', hostname):
            patterns.append('numbers_in_domain')
            score += 0.4
        
        # Port number (non-standard)
        if parsed.port and parsed.port not in [80, 443]:
            patterns.append('non_standard_port')
            score += 0.5
        
        # URL shortener check
        shorteners = ['bit.ly', 'goo.gl', 't.co', 'tinyurl.com', 'ow.ly']
        if any(short in url for short in shorteners):
            patterns.append('url_shortener')
            score += 0.3
        
        # @ symbol (username in URL)
        if '@' in url:
            patterns.append('at_symbol')
            score += 0.7
        
        # Suspicious path keywords
        suspicious_paths = ['login', 'verify', 'confirm', 'update', 'secure', 'account', 'signin', 'banking']
        path_lower = path.lower()
        if any(keyword in path_lower for keyword in suspicious_paths):
            # Only suspicious if combined with other indicators
            if hyphen_count > 2 or domain_length > 30:
                patterns.append('suspicious_path')
                score += 0.4
        
        return {
            'has_suspicious_patterns': len(patterns) > 0,
            'patterns': patterns,
            'score': min(score, 1.0)
        }
    
    @staticmethod
    def analyze(url: str) -> dict:
        """Complete rule-based analysis"""
        tld_check = RuleBasedPhishingDetector.check_suspicious_tld(url)
        typo_check = RuleBasedPhishingDetector.check_typosquatting(url)
        brand_check = RuleBasedPhishingDetector.check_brand_abuse(url)
        pattern_check = RuleBasedPhishingDetector.check_suspicious_patterns(url)
        
        # Aggregate score with weighted combination
        scores = [
            tld_check['score'],
            typo_check['score'],
            brand_check['score'],
            pattern_check['score']
        ]
        
        # Use weighted max to be more aggressive
        weights = [1.2, 1.3, 1.2, 1.1]  # Typosquatting has highest weight
        weighted_scores = [score * weight for score, weight in zip(scores, weights)]
        
        # Also consider average of top 2 scores
        sorted_scores = sorted(weighted_scores, reverse=True)
        avg_top_2 = (sorted_scores[0] + sorted_scores[1]) / 2 if len(sorted_scores) >= 2 else sorted_scores[0]
        
        # Take the higher of weighted max or average top 2
        total_score = max(max(weighted_scores), avg_top_2 * 1.1)
        
        # Cap at 1.0
        total_score = min(total_score, 1.0)
        
        return {
            'rule_based_score': total_score,
            'suspicious_tld': tld_check['is_suspicious'],
            'typosquatting': typo_check.get('is_typosquatting', False),
            'brand_abuse': brand_check.get('is_brand_abuse', False),
            'suspicious_patterns': pattern_check['patterns'],
            'details': {
                'tld': tld_check,
                'typosquatting': typo_check,
                'brand_abuse': brand_check,
                'patterns': pattern_check
            }
        }
