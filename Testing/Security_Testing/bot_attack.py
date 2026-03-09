import requests
import concurrent.futures

URL = "http://localhost:8000/api/v1/inspect"

print("[*] SENTIO 360 Security Testing Initiated...")
print("[*] Launching Asynchronous DDoS Bot Attack (40 Requests at the same exact time)...\n")

# මේ ෆන්ක්ශන් එකෙන් තමයි රික්වෙස්ට් යවන්නේ
def send_attack(req_id):
    data = {"text_payload": f"Bot Brute-force Request {req_id}", "behavior_json": "{}"}
    try:
        res = requests.post(URL, data=data)
        result = res.json()
        status = result.get('status')
        action = result.get('action')
        
        print(f"Request {req_id:02d}: Status -> {status} | Action -> {action}")
        
        if "BANNED" in str(action):
            return True
    except Exception:
        pass
    return False

# ThreadPool එකක් පාවිච්චි කරලා රික්වෙස්ට් 40ම එකම තත්පරේ සර්වර් එකට යවනවා
with concurrent.futures.ThreadPoolExecutor(max_workers=40) as executor:
    results = list(executor.map(send_attack, range(1, 41)))
    
    if any(results):
        print("\n[SUCCESS] Rate Limiter successfully triggered!")
        print("[SUCCESS] Attacker IP has been permanently banned by SENTIO 360.")
    else:
        print("\n[INFO] Attack finished.")