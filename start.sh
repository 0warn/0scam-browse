#!/bin/bash fish
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
pip install -r requirements.txt

# Start API
echo "[*] Starting Local AI Detection API..."
python3 phishing-ai-detector/api/app.py
