import pandas as pd
import numpy as np
import requests
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os
import random
import string
import time
from feature_extraction import URLFeatureExtractor

def fetch_local_phishing(limit=15000):
    """Read from the local .lst file discovered"""
    file_path = os.path.join(os.path.dirname(__file__), "ALL-phishing-links.lst")
    if not os.path.exists(file_path):
        print(f"Local file {file_path} not found.")
        return []
    
    try:
        print(f"Reading phishing URLs from local file: {file_path}...")
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        
        random.shuffle(urls)
        return urls[:limit]
    except Exception as e:
        print(f"Error reading local file: {e}")
    return []

def get_legitimate_urls(limit=15000):
    legit_domains = [
        "google.com", "youtube.com", "facebook.com", "amazon.com", "wikipedia.org",
        "twitter.com", "instagram.com", "linkedin.com", "netflix.com", "microsoft.com",
        "apple.com", "yahoo.com", "reddit.com", "twitch.tv", "github.com",
        "stackoverflow.com", "example.com", "openai.com", "gemini.google.com",
        "bbc.com", "cnn.com", "nytimes.com", "quora.com", "ebay.com", "walmart.com",
        "imdb.com", "espn.com", "aliexpress.com", "booking.com", "spotify.com",
        "whatsapp.com", "hulu.com", "dropbox.com", "salesforce.com", "adobe.com",
        "tumblr.com", "pinterest.com", "paypal.com", "office.com", "bing.com",
        "medium.com", "stackexchange.com", "wordpress.com", "vimeo.com", "slack.com",
        "zoom.us", "zillow.com", "weather.com", "chase.com", "wellsfargo.com",
        "bankofamerica.com", "espn.go.com", "t-mobile.com", "verizon.com"
    ]
    data = []
    for _ in range(limit):
        domain = random.choice(legit_domains)
        depth = random.randint(0, 3)
        path = ""
        if depth > 0:
            path = "/".join(["".join(random.choices(string.ascii_lowercase, k=random.randint(3, 10))) for _ in range(depth)])
        url = f"https://{domain}/{path}"
        data.append(url)
    return data

def train_model():
    print("--- 0Scam NEXT-LEVEL Model Training ---")
    
    # 1. Gather Data (Local .lst + Generated Legitimate)
    phishing_urls = fetch_local_phishing(20000)
    
    # Generate balanced legitimate set
    legit_urls = get_legitimate_urls(len(phishing_urls))
    
    if not phishing_urls:
        print("CRITICAL: Fetch failed.")
        return

    print(f"Dataset Size: {len(phishing_urls)} Phishing, {len(legit_urls)} Legitimate.")
    
    data = []
    for u in phishing_urls: data.append({"url": u, "label": 1})
    for u in legit_urls: data.append({"url": u, "label": 0})
    
    df = pd.DataFrame(data)
    
    # 2. Extract Features
    print("Extracting features (This will take time due to large dataset)...")
    extractor = URLFeatureExtractor()
    X = []
    y = []
    
    for index, row in df.iterrows():
        try:
            feat = extractor.extract_features(row['url'])
            if len(feat) == 19:
                X.append(feat)
                y.append(row['label'])
            if index > 0 and index % 5000 == 0:
                print(f"Processed {index} samples...")
        except:
            continue

    X = np.array(X)
    y = np.array(y)

    print(f"Final training set size: {X.shape[0]} samples")

    # 3. Train Advanced RF
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=42)

    print("Training 400-Estimator Random Forest Classifier...")
    model = RandomForestClassifier(n_estimators=400, max_depth=40, n_jobs=-1, random_state=42)
    model.fit(X_train, y_train)

    # 4. Evaluate
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"\nNext-Level Model Accuracy: {acc:.6f}")
    print("\nDetailed Report:\n", classification_report(y_test, y_pred))

    # 5. Save Model
    base_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(base_dir, "model.pkl")
    joblib.dump(model, model_path)
    print(f"NEXT-LEVEL Model saved to {model_path}")

if __name__ == "__main__":
    train_model()
