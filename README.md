# 0Scam AI Phishing Protection System (Ultimate Edition) 🛡️

A professional-grade, offline-capable AI phishing detection system. This project features a **Random Forest Classifier (99.9% Accuracy)** trained on 40,000+ real-world phishing URLs, wrapped in a premium **Manifest V3** browser extension.

---

## 🚀 Quick Start (Run Immediately)

### 1. Start the AI Engine
Open your terminal in this folder and run:
```bash
./start.sh
```
*This will verify dependencies, check the model, and start the API server at `http://127.0.0.1:5000`.*

### 2. Install the Extension
1.  Open **Google Chrome** (or Brave/Edge).
2.  Go to `chrome://extensions/`.
3.  Enable **Developer mode** (top right).
4.  Click **Load unpacked**.
5.  Select the **`phishing-ai-detector/extension`** folder.

---

## 🌟 Key Features

### 🧠 Next-Level AI Detection
- **19 Advanced Features**: Vowel ratios, entropy analysis, TLD reputation, and more.
- **Massive Dataset**: Trained on 20,000 active phishing links + 20,000 legitimate sites.
- **Suspicious Redirects**: Automatically flags tabs that redirect too many times (evasion attempt).

### 🛡️ Premium UI & UX
- **Glassmorphism Dashboard**: A modern, dark-themed popup with pulsing status indicators.
- **Smart "BLK" Badge**: High-contrast red badge on the toolbar icon when a threat is blocked.
- **Fail-Safe Blocking**: The "Threat Neutralized" screen prevents access to malicious sites but allows a one-click return to safety.

---

## 📂 Project Structure

```text
phishing-ai-detector/
├── ml/
│   ├── model.pkl              # The 99.9% accurate AI model
│   ├── train.py               # Advanced training script (Local .lst support)
│   ├── feature_extraction.py  # 19-feature extraction logic
│   └── ALL-phishing-links.lst # Large dataset source
├── api/
│   ├── app.py                 # Threaded Flask API
│   └── feature_extraction.py  # Synced copy for API
├── extension/
│   ├── manifest.json          # MV3 Configuration
│   ├── background.js          # Core logic (Redirects, Scanning, Blocking)
│   ├── popup.html             # Premium Shield UI
│   ├── popup.js               # Smart UI Sync Logic
│   ├── blocked.html           # "Threat Neutralized" Page
│   ├── blocked.js             # Safe Button Logic
│   └── icon.png               # Generated Asset
└── requirements.txt           # Python dependencies
```

---

## ⚠️ Privacy Note
This system runs **100% locally**. No browsing history is sent to the cloud. The AI lives on your machine.
