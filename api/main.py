from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import pytz
import uvicorn
import joblib
import pandas as pd
import numpy as np
import cv2
import json
import os
import logging
import time 
from datetime import datetime
from pathlib import Path
import warnings
import shap 
from scipy.stats import ks_2samp
from pymongo import MongoClient
from pymongo.server_api import ServerApi

warnings.filterwarnings('ignore')
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
from tensorflow.keras.models import load_model

SL_TZ = pytz.timezone('Asia/Colombo')

# SETUP & MEMORY
BASE_DIR = Path(__file__).resolve().parent.parent
LOGS_DIR = BASE_DIR / 'logs'
LOGS_DIR.mkdir(parents=True, exist_ok=True)

# Local Logging Fallback
logging.basicConfig(filename=LOGS_DIR / 'firewall.log', level=logging.WARNING, format='%(asctime)s - THREAT: %(message)s')

MONGO_URI = "mongodb+srv://sentio360_db_user:ZmvjSjwLtjJgfHBo@sentio360.bdy9xve.mongodb.net/?retryWrites=true&w=majority&appName=Sentio360"
BLOCKED_IPS = set() # Kept in memory for instant blocking (Zero-Latency)

try:
    print("[*] Connecting to MongoDB Atlas Cloud...")
    mongo_client = MongoClient(MONGO_URI, server_api=ServerApi('1'))
    db = mongo_client['sentio360_db']
    
    # Database Collections (Tables)
    logs_collection = db['traffic_logs']
    blocked_ips_collection = db['blocked_ips']
    
    # Load all historically blocked IPs from Cloud into server memory on startup!
    for doc in blocked_ips_collection.find({}):
        BLOCKED_IPS.add(doc.get('ip'))
        
    print(f"[SUCCESS] Connected to Cloud Database! Loaded {len(BLOCKED_IPS)} previously blocked IPs.")
except Exception as e:
    print(f"[ERROR] Cloud Database Connection Failed: {e}")

# RATE LIMITING MEMORY
REQUEST_COUNTS = {}
RATE_LIMIT_WINDOW = 10 
MAX_REQUESTS_PER_WINDOW = 15 

# DATA SCIENCE: Statistical Concept Drift Tracking (KS-Test)
baseline_safe_traffic = []  
recent_safe_traffic = []    
drift_alert_active = False

app = FastAPI(title="SENTIO 360 - AI Firewall")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

app.mount("/site", StaticFiles(directory=str(BASE_DIR / "target_website")), name="site")
app.mount("/admin", StaticFiles(directory=str(BASE_DIR / "admin_dashboard")), name="admin")

class MarkSafeRequest(BaseModel):
    ip: str

def get_real_ip(request: Request):
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host

MODELS_DIR = BASE_DIR / 'models'
print("[*] SENTIO 360 AI Brains...")

try:
    rf_behavior_model = joblib.load(MODELS_DIR / 'behavior_encoder' / 'rf_behavior_model.pkl')
    behavior_scaler = joblib.load(MODELS_DIR / 'behavior_encoder' / 'behavior_scaler.pkl')
    
    print("[*] Loading Deep NLP Neural Network...")
    dnn_text_model = load_model(MODELS_DIR / 'text_encoder' / 'dnn_text_model.h5', compile=False)
    tfidf_vectorizer = joblib.load(MODELS_DIR / 'text_encoder' / 'tfidf_vectorizer.pkl')
    
    cnn_vision_model = load_model(MODELS_DIR / 'vision_encoder' / 'cnn_vision_model.h5', compile=False)
    
    try:
        autoencoder_model = load_model(MODELS_DIR / 'behavior_encoder' / 'autoencoder_model.h5', compile=False)
        print(" -> [DS] Deep Autoencoder loaded successfully.")
    except:
        autoencoder_model = None

    print("[*] Initializing SHAP Game Theory Explainer...")
    shap_explainer = shap.TreeExplainer(rf_behavior_model)

    print("[SUCCESS] All Models Loaded!")
except Exception as e:
    print(f"[ERROR] Loading failed: {e}")

BEHAVIOR_FEATURES = ['Max Packet Length', 'Packet Length Variance', 'Avg Bwd Segment Size', 'Average Packet Size', 'Bwd Packet Length Max', 'Destination Port', 'Packet Length Std', 'Total Length of Bwd Packets', 'Subflow Fwd Bytes', 'Bwd Header Length']

# ENDPOINTS FOR DASHBOARD & NEW FEATURES
@app.get("/api/v1/check_ip")
async def check_ip(request: Request):
    client_ip = get_real_ip(request)
    if client_ip in BLOCKED_IPS:
        return {"blocked": True, "reason": "IP Permanently Banned by SENTIO 360"}
    return {"blocked": False}

@app.get("/api/v1/dashboard_data")
async def get_dashboard_data():
    # 💥 FIX: Fetching Data directly from MongoDB Cloud instead of local memory!
    try:
        recent_logs = list(logs_collection.find({}, {"_id": 0}).sort("_id", -1).limit(50))
        total_requests = logs_collection.count_documents({})
    except:
        recent_logs = []
        total_requests = 0

    return {
        "total_requests": total_requests,
        "blocked_ips": list(BLOCKED_IPS),
        "logs": recent_logs,
        "concept_drift": drift_alert_active 
    }

@app.post("/api/v1/trap")
async def trigger_trap(request: Request):
    client_ip = get_real_ip(request)
    
    current_time_sl = datetime.now(SL_TZ)
    
    if client_ip not in BLOCKED_IPS:
        BLOCKED_IPS.add(client_ip)
        blocked_ips_collection.update_one({"ip": client_ip}, {"$set": {"ip": client_ip, "timestamp": current_time_sl.strftime("%Y-%m-%d %H:%M:%S")}}, upsert=True)
    
    action = "IP BANNED (HONEYPOT)"
    details = "[Active Defense] Hidden Honeypot triggered."
    
    log_data = {
        "time": current_time_sl.strftime("%H:%M:%S"),
        "date": current_time_sl.strftime("%Y-%m-%d"),
        "ip": client_ip, "status": "BLOCK", "action": action,
        "details": details, "latency": 0.0, "risk": 1.0, "anomaly_score": 0.0
    }
    
    logs_collection.insert_one(log_data.copy())
    logging.warning(f"IP: {client_ip} | ACTION: {action} | DETAILS: {details}")
    
    return {"status": "BANNED"}

@app.post("/api/v1/mark_safe")
async def mark_safe(req: MarkSafeRequest):
    if req.ip in BLOCKED_IPS:
        BLOCKED_IPS.remove(req.ip)
        # Remove from Cloud DB so it doesn't get blocked again on server restart
        blocked_ips_collection.delete_one({"ip": req.ip})
    return {"status": "UNBANNED"}

@app.post("/api/v1/inspect")
async def inspect_traffic(
    request: Request, text_payload: str = Form(""),
    behavior_json: str = Form("{}"), file: UploadFile = File(None)
):
    global drift_alert_active, baseline_safe_traffic, recent_safe_traffic
    start_time = time.time()
    
    client_ip = get_real_ip(request)
    
    current_time_sl = datetime.now(SL_TZ)
    timestamp = current_time_sl.strftime("%H:%M:%S")
    date_str = current_time_sl.strftime("%Y-%m-%d")
    
    if client_ip in BLOCKED_IPS:
        return {"status": "BLOCK", "action": "BANNED", "threat_details": ["IP is already Blacklisted."]}

    current_time = time.time()
    if client_ip not in REQUEST_COUNTS: REQUEST_COUNTS[client_ip] = []
    REQUEST_COUNTS[client_ip] = [t for t in REQUEST_COUNTS[client_ip] if current_time - t < RATE_LIMIT_WINDOW]
    REQUEST_COUNTS[client_ip].append(current_time)
    
    if len(REQUEST_COUNTS[client_ip]) > MAX_REQUESTS_PER_WINDOW:
        if client_ip not in BLOCKED_IPS:
            BLOCKED_IPS.add(client_ip)
            blocked_ips_collection.update_one({"ip": client_ip}, {"$set": {"ip": client_ip, "timestamp": f"{date_str} {timestamp}"}}, upsert=True)
            
        action = "IP BANNED (RATE LIMIT)"
        details = "Spam/Brute-force detected."
        
        log_data = {
            "time": timestamp, "date": date_str, "ip": client_ip, "status": "BLOCK", "action": action,
            "details": details, "latency": float(round((time.time() - start_time) * 1000, 2)), 
            "risk": 1.0, "anomaly_score": 0.0
        }
        logs_collection.insert_one(log_data.copy())
        logging.warning(f"IP: {client_ip} | ACTION: {action} | DETAILS: {details}")
        
        return {"status": "BLOCK", "action": "BANNED", "threat_details": ["Rate Limit Exceeded."]}

    p_nlp_threat, p_beh_threat, p_vis_threat = 0.0, 0.0, 0.0
    threat_explanations = []
    is_bot_attack = False 
    anomaly_error = 0.0 

    # 1. DEEP NLP TEXT ANALYSIS (Neural Network)
    p_nlp_threat = 0.0
    if text_payload.strip():
        word_count = len(text_payload.split())
        special_chars = any(char in text_payload for char in ['<', '>', '{', '}', '(', ')', '/', '\\', '=', "'", '"'])
        
        if word_count < 5 and not special_chars:
            prob_safe, prob_web, prob_llm = 1.0, 0.0, 0.0
        else:
            text_vec = tfidf_vectorizer.transform([text_payload]).toarray() 
            probs = dnn_text_model.predict(text_vec, verbose=0)[0]
            prob_safe, prob_web, prob_llm = probs[0], probs[1], probs[2]
            
            if prob_llm > 0.65: 
                p_nlp_threat = float(prob_llm) 
                threat_explanations.append(f"[NLP-XAI] Deep Neural Net isolated LLM Prompt Injection patterns (Conf: {prob_llm*100:.1f}%)")
            elif prob_web > 0.60:
                p_nlp_threat = float(prob_web) 
                threat_explanations.append(f"[NLP-XAI] Deep Neural Net detected SQLi/XSS syntax (Conf: {prob_web*100:.1f}%)")
                
    # 2. BEHAVIORAL ANALYSIS & DATA SCIENCE UPGRADES
    if behavior_json != "{}" and behavior_json.strip() != "":
        try:
            b_data = json.loads(behavior_json)
            b_df = pd.DataFrame(columns=BEHAVIOR_FEATURES)
            b_df.loc[0] = [float(b_data.get(feat, 0.0)) for feat in BEHAVIOR_FEATURES]
            b_scaled = behavior_scaler.transform(b_df)
            
            p_beh_threat = float(rf_behavior_model.predict_proba(b_scaled)[0][1])
            max_len = float(b_data.get("Max Packet Length", 0.0))
            
            if autoencoder_model:
                reconstruction = autoencoder_model.predict(b_scaled, verbose=0)
                anomaly_error = round(float(np.mean(np.power(b_scaled - reconstruction, 2))), 4)
            else:
                anomaly_error = round(float(np.linalg.norm(b_scaled[0])), 2)

            if anomaly_error > 5.0:
                threat_explanations.append(f"[ZERO-DAY] Autoencoder Anomaly Spike! (MSE: {anomaly_error})")
                p_beh_threat = max(p_beh_threat, 0.85)
                is_bot_attack = True

            if p_beh_threat > 0.40:
                p_beh_threat = max(p_beh_threat, 0.99)
                is_bot_attack = True 
                try:
                    shap_vals = shap_explainer.shap_values(b_scaled)
                    vals = shap_vals[1][0] if isinstance(shap_vals, list) else shap_vals[0]
                    top_feature_idx = int(np.argmax(np.abs(vals)))
                    top_feature_name = BEHAVIOR_FEATURES[top_feature_idx]
                    threat_explanations.append(f"[SHAP-XAI] Mathematical attribution isolated '{top_feature_name}' as root cause.")
                except:
                    threat_explanations.append(f"[BEH-XAI] Behavioral deviation detected.")

            if not is_bot_attack and p_beh_threat < 0.2:
                if len(baseline_safe_traffic) < 50:
                    baseline_safe_traffic.append(max_len)
                else:
                    recent_safe_traffic.append(max_len)
                    if len(recent_safe_traffic) > 30:
                        recent_safe_traffic.pop(0)
                        stat, p_value = ks_2samp(baseline_safe_traffic, recent_safe_traffic)
                        if p_value < 0.05:
                            drift_alert_active = True
        except Exception as e: pass

    # 3. VISION ANALYSIS 
    if file is not None:
        try:
            file_bytes = await file.read()
            nparr = np.frombuffer(file_bytes, np.uint8)
            decoded_img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)
            has_static = any(sig in file_bytes.lower() for sig in [b"<?php", b"<script", b"system(", b"eval(", b"$hacker"])

            if not (decoded_img is not None and not has_static):
                padded_bytes = file_bytes.ljust(4096, b'\x00')[:4096]
                texture_img = np.frombuffer(padded_bytes, dtype=np.uint8).reshape((64, 64)) / 255.0
                p_vis_threat = float(cnn_vision_model.predict(texture_img.reshape(-1, 64, 64, 1), verbose=0)[0][0])
                if has_static: p_vis_threat = max(p_vis_threat, 0.95)
                
                if p_vis_threat > (0.50 if has_static else 0.40):
                    threat_explanations.append(f"[VIS-XAI] Disguised Malware Texture. (Conf: {p_vis_threat*100:.1f}%)")
        except Exception as e: pass

    # DATA SCIENCE: META-LEARNING FUSION LAYER
    W_nlp, W_beh, W_vis = 0.35, 0.45, 0.20
    final_risk_score = float((p_nlp_threat * W_nlp) + (p_beh_threat * W_beh) + (p_vis_threat * W_vis))
    final_risk_score = float(max(final_risk_score, p_nlp_threat, p_beh_threat, p_vis_threat))

    action_taken = "PASSED"
    status = "ALLOW"
    
    if final_risk_score >= 0.6:
        status = "BLOCK"
        if is_bot_attack:
            if client_ip not in BLOCKED_IPS:
                BLOCKED_IPS.add(client_ip)
                # Save newly blocked IP to Cloud
                blocked_ips_collection.update_one({"ip": client_ip}, {"$set": {"ip": client_ip, "timestamp": f"{date_str} {timestamp}"}}, upsert=True)
            action_taken = "IP BANNED (BOTNET)"
        else:
            action_taken = "PAYLOAD DROPPED (WARNING)"
            
    process_time_ms = float(round((time.time() - start_time) * 1000, 2))
    details_string = " | ".join(threat_explanations) if threat_explanations else "[Clean Traffic]"
    
    # 💥 FIX: Uploading directly to MongoDB Collection 💥
    log_data = {
        "time": timestamp,
        "date": date_str,
        "ip": client_ip, 
        "status": status,
        "action": action_taken, 
        "details": details_string,
        "latency": process_time_ms, 
        "risk": float(min(round(final_risk_score, 2), 1.0)),
        "anomaly_score": float(anomaly_error)
    }
    
    try:
        logs_collection.insert_one(log_data.copy())
    except:
        pass # Silently fail if DB has a momentary hiccup so the firewall doesn't crash
    
    if status == "BLOCK":
        log_msg = f"IP: {client_ip} | ACTION: {action_taken} | RISK: {final_risk_score:.2f} | DETAILS: {details_string}"
        logging.warning(log_msg)
        
    return {"status": status, "action": action_taken, "threat_details": threat_explanations}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)