"""
utils.py — Model loader + Feature extractor for phishing detection
Compatible with: main.py (Flask backend) and Chrome extension
"""

import os
import pandas as pd
import joblib
from urllib.parse import urlparse

# Path to trained pipeline
PIPE_PATH = os.path.normpath(os.path.join(os.path.dirname(__file__), "../models/phishing_simple_model.pkl"))

# Must match exactly the training order
FEATURE_ORDER = ["URLLength", "DomainLength", "IsHTTPS", "NoOfSubDomain", "HasDashDomain", "HasAtSymbol"]


def load_pipeline():
    """Load the trained XGBoost pipeline"""
    if not os.path.exists(PIPE_PATH):
        raise FileNotFoundError(f"❌ Model file not found at {PIPE_PATH}")
    pipe = joblib.load(PIPE_PATH)
    print(f"✅ Model loaded successfully from {PIPE_PATH}")
    return pipe


def extract_features_from_url(url: str):
    """
    Extracts lexical features from a given URL.
    Works for both live extension URLs and form input.
    """
    if not isinstance(url, str):
        url = str(url)
    if not url.startswith("http"):
        url = "http://" + url

    parsed = urlparse(url)
    host = parsed.hostname or ""

    return {
        "URLLength": len(url),
        "DomainLength": len(host),
        "IsHTTPS": 1 if parsed.scheme.lower() == "https" else 0,
        "NoOfSubDomain": host.count("."),
        "HasDashDomain": 1 if "-" in host else 0,
        "HasAtSymbol": 1 if "@" in url else 0
    }


def prepare_input(features: dict):
    """Convert features dict → DataFrame (ready for model.predict_proba)"""
    return pd.DataFrame([{f: float(features.get(f, 0)) for f in FEATURE_ORDER}])
