#!/bin/bash
set -e

echo "--- 0Scam System Repair & Startup ---"

# Check Python and Venv
if [ ! -d "venv" ]; then
    echo "[*] Creating virtual environment..."
    python3 -m venv venv
fi

# Activate Venv
source venv/bin/activate

# Install Dependencies
echo "[*] Installing dependencies..."
pip install flask scikit-learn pandas numpy joblib Pillow requests > /dev/null

# Generate Assets
echo "[*] Generating assets..."
python3 generate_icon.py

# Force Model Retrain (Ensures model is consistent with latest logic)
echo "[*] Training model..."
python3 phishing-ai-detector/ml/train.py

# Start API
echo "[*] Starting Local AI Detection API..."
export FLASK_APP=phishing-ai-detector/api/app.py
export FLASK_ENV=development
flask run --host=127.0.0.1 --port=5000
