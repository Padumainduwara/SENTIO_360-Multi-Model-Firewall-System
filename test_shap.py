import requests
import json

print("🚀 Sending Direct Attack to Trigger Deep Learning & SHAP XAI...\n")

ddos_payload = {
    "Max Packet Length": 11607.0,
    "Packet Length Variance": 3865023.0,
    "Avg Bwd Segment Size": 5800.0,
    "Average Packet Size": 4000.0,
    "Bwd Packet Length Max": 11607.0,
    "Destination Port": 80,
    "Packet Length Std": 1965.0,
    "Total Length of Bwd Packets": 58000.0,
    "Subflow Fwd Bytes": 300.0,
    "Bwd Header Length": 500.0
}

res = requests.post(
    "https://sentio-360-multi-model-firewall-system.onrender.com/api/v1/inspect", 
    data={"text_payload": "", "behavior_json": json.dumps(ddos_payload)}
)

print(f"🛑 Status: {res.json()['status']}")
print(f"⚠️ Action: {res.json()['action']}")
print("🧠 AI Explanations (Threat Details):")
for detail in res.json()['threat_details']:
    print(f"  -> {detail}")