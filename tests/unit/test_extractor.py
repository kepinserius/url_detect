import pytest
from inference.features.extractor import URLFeatureExtractor

def test_extractor_basic():
    url = "https://example.com/path?query=1"
    features = URLFeatureExtractor.extract_features(url)
    
    assert features["url_length"] == len(url)
    assert features["is_https"] == 1
    assert features["num_dots"] == 1
    assert features["num_question"] == 1

def test_extractor_ip():
    url = "http://192.168.1.1/login"
    features = URLFeatureExtractor.extract_features(url)
    
    assert features["has_ip"] == 1
    assert features["is_https"] == 0
