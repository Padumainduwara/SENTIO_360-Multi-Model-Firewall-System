# SENTIO 360 - Multi-Modal AI Web Application Firewall 🛡️

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688.svg)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.14%2B-FF6F00.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 📌 Project Overview
**SENTIO 360** is an advanced, multi-modal machine-learning Web Application Firewall (WAF). Unlike traditional rule-based firewalls, SENTIO 360 leverages three parallel Artificial Intelligence engines to inspect network traffic, text payloads, and file uploads simultaneously. It is designed to block modern, complex cyber attacks (like Zero-Day DDoS, LLM Prompt Injections, and disguised Malware) in real-time with millisecond latency.

## 🚀 Key Features
* **Deep NLP Engine:** Uses TF-IDF and a Deep Neural Network (DNN) to detect and block SQL Injections, XSS, and LLM Prompt Injections.
* **Behavioral Autoencoder & Random Forest:** Analyzes network packet sizes and traffic flow to catch Zero-Day anomalies and volumetric DDoS attacks.
* **Vision AI (CNN) for Malware:** Extracts the first 4096 bytes of binary files, converts them into 64x64 grayscale textures, and visually scans for hidden malware.
* **Meta-Learning Threat Fusion:** Combines predictions from all three AI models using a weighted mathematical formula `(NLP * 0.35) + (Behavior * 0.45) + (Vision * 0.20)` to calculate a final risk score.
* **Explainable AI (SHAP):** Solves the "black-box" AI problem by mathematically calculating and logging the exact feature (e.g., `Max_Packet_Length`) that caused an IP to be blocked.
* **Proxy Bypass (True IP Extraction):** Extracts the `X-Forwarded-For` HTTP header to identify and ban the real hacker, bypassing cloud proxies like Cloudflare.
* **Heuristic Bypass Layer:** Instantly allows simple, safe requests to pass through without AI inspection, saving server RAM and ensuring zero latency for normal users.
* **Secure Admin Dashboard:** A real-time, authenticated control center connected to MongoDB Atlas for live threat monitoring and manual IP management.

## 🛠️ Technology Stack
* **Backend Framework:** FastAPI, Uvicorn
* **Data Science & AI:** TensorFlow (Keras), Scikit-Learn, SHAP, OpenCV (`cv2`), Pandas, NumPy
* **Database & Cloud:** MongoDB Atlas (NoSQL), Render Cloud
* **Frontend:** HTML5, CSS3, Vanilla JavaScript

---

## 💻 Environment Setup & Installation

Follow these steps to set up the SENTIO 360 environment and run the firewall on your local machine.

### Prerequisites
* Python 3.10 or higher installed.
* Git installed.
* An active MongoDB Atlas Cluster (for database logging).

### Step 1: Clone the Repository
```bash
git clone https://github.com/your-username/SENTIO_360.git
cd SENTIO_360
```

### Step 2: Create a Virtual Environment
It is highly recommended to use an isolated Python virtual environment to avoid dependency conflicts.
```bash
python -m venv venv
```

### Step 3: Activate the Virtual Environment
**On Windows:**
```bash
venv\Scripts\activate
```
**On macOS/Linux:**
```bash
source venv/bin/activate
```

### Step 4: Install Dependencies
Install all required Data Science and Backend libraries.
```bash
pip install -r requirements.txt
```

### Step 5: Database Configuration
Open `api/main.py` and locate the MongoDB connection string. Ensure your MongoDB Atlas URI is correctly configured and that your current IP address is whitelisted in your MongoDB Network Access settings.
```python
MONGO_URI = "your_mongodb_atlas_connection_string_here"
```

### Step 6: Run the FastAPI Server
Start the backend firewall engine. The Singleton design pattern will load the `.h5` and `.pkl` AI models into RAM during startup.
```bash
uvicorn api.main:app --reload
```
The firewall API will now be active at `http://127.0.0.1:8000`.

---

## 🎯 Usage Guide

### 1. The Admin Security Dashboard
* Open `admin_dashboard/index.html` in your web browser.
* You will be redirected to the secure login page (`login.html`).
* **Default Credentials:** Username: `admin` | Password: `admin123`
* Once logged in, you can monitor live threat logs, view SHAP explanations, and manually unban IPs.

### 2. Client-Side Testing (AI Portal)
* Open `target_website/ai_portal.html` in your browser.
* Use the test forms to submit malicious text (e.g., `<script>alert(1)</script>`) or upload suspicious files.
* Watch the status box instantly update as the backend FastAPI server intercepts and blocks the payloads.

---

## 📂 Project Structure
```text
SENTIO_360/
│
├── admin_dashboard/           # Secure frontend for network administrators
│   ├── index.html             # Live threat monitoring UI
│   └── login.html             # Secure authentication portal
│
├── api/                       # Core Backend Server
│   ├── main.py                # FastAPI endpoints, Fusion Logic, SHAP
│   └── security_rules.py      # Hardcoded firewall heuristic rules
│
├── notebooks/                 # Data Science & Model Training (Jupyter)
│   ├── data_preprocessing.ipynb
│   ├── text_eda_visuals.ipynb
│   ├── train_deep_text_model.ipynb
│   ├── train_behavior_model.ipynb
│   ├── train_autoencoder.ipynb
│   └── train_vision_model.ipynb
│
├── target_website/            # The vulnerable application being protected
│   ├── ai_portal.html         # Testing ground for AI models
│   └── firewall_guard.js      # Frontend script connecting to FastAPI
│
├── models/                    # Saved AI models (.h5, .pkl) [Ignored in Git]
├── requirements.txt           # Python package dependencies
└── README.md                  # Project documentation
```

## 📜 License
This project is licensed under the MIT License. See the `LICENSE` file for more details.
