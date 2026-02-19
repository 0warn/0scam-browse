from flask import Flask, request, jsonify
import joblib
import numpy as np
import os
import sys

# Add local path for feature_extraction import
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

from feature_extraction import URLFeatureExtractor

app = Flask(__name__)

# Load model
MODEL_PATH = os.path.join(BASE_DIR, '../ml/model.pkl')

if not os.path.exists(MODEL_PATH):
    print(f"Error: Model not found at {MODEL_PATH}")
    sys.exit(1)

try:
    # Use allow_pickle=True or handle joblib properly
    model = joblib.load(MODEL_PATH)
    print("ADVANCED AI Model loaded successfully.")
except Exception as e:
    print(f"Failed to load model: {e}")
    sys.exit(1)

extractor = URLFeatureExtractor()

@app.route('/scan', methods=['POST'])
def scan_url():
    try:
        data = request.get_json()
        if not data or 'url' not in data:
            return jsonify({"error": "Missing URL"}), 400
        
        url = data['url']
        
        # 1. Extract 19 Features
        features = extractor.extract_features(url)
        
        # 2. Predict
        features_array = np.array([features])
        prediction = model.predict(features_array)[0]
        probabilities = model.predict_proba(features_array)[0]
        confidence = float(probabilities[1]) if prediction == 1 else float(probabilities[0])
        
        # 3. Enhanced Mapping
        classification = "PHISHING" if prediction == 1 else "LEGITIMATE"
        risk_level = "LOW"
        
        if classification == "PHISHING":
            risk_level = "HIGH" if confidence > 0.75 else "MEDIUM"
        else:
            # Check for suspicious low-confidence legitimate
            if confidence < 0.55: # Lowered threshold to reduce false positives
                classification = "SUSPICIOUS"
                risk_level = "MEDIUM"

        return jsonify({
            "url": url,
            "classification": classification,
            "risk_level": risk_level,
            "confidence": confidence
        })

    except Exception as e:
        print(f"Server Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Run in threaded mode for better extension performance
    app.run(host='127.0.0.1', port=5000, threaded=True)
