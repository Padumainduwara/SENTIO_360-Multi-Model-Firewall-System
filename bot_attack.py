import requests
import time
import json
import random

BASE_URL = "http://localhost:8000"
API_URL = f"{BASE_URL}/api/v1/inspect"

print("====================================================")
print("💀 SENTIO 360 - ADVANCED APT BOTNET SIMULATOR 💀")
print("====================================================\n")

# STAGE 1: Stealth Reconnaissance (Scraping Pages like a real bot)
pages_to_scrape = ["/site/index.html", "/site/about.html", "/site/contact.html"]
print("[*] PHASE 1: Stealth Reconnaissance (Scraping Website Pages)...")

for page in pages_to_scrape:
    print(f"   [>] Accessing {page}...")
    try:
        res = requests.get(BASE_URL + page)
        if "ACCESS DENIED" in res.text:
            print("   [!] Bot blocked during page navigation!")
            exit()
        time.sleep(1) # Stealth delay to mimic a human
    except Exception as e:
        print("   [!] Target Offline.")
        exit()

# STAGE 2: Triggering the Honeypot (Scraper behavior)
print("\n[*] PHASE 2: Scanning for hidden endpoints...")
print("   [>] Found hidden link! Triggering Honeypot Trap...")
try:
    trap_res = requests.post(f"{BASE_URL}/api/v1/trap")
    if trap_res.status_code == 200:
        print("   ⚠️ TRAP TRIGGERED! IP Flagged by Sentinel.")
except Exception as e:
    pass
time.sleep(1)

# STAGE 3: Volumetric Layer 7 DDoS Attack
print("\n[*] PHASE 3: Launching Massive Layer 7 DDoS Attack...")
ddos_payload = {
    "Max Packet Length": 11607.0,
    "Packet Length Variance": 3865023.0,
    "Avg Bwd Segment Size": 5800.0,
    "Average Packet Size": 4000.0,
    "Destination Port": 80
}

for i in range(1, 4):
    print(f"   [>] Injecting Malicious Packet Burst {i}...")
    try:
        res = requests.post(API_URL, data={"text_payload": "", "behavior_json": json.dumps(ddos_payload)})
        
        if res.json().get('status') == 'BLOCK':
            print(f"   ⚠️ FIREWALL REACTION: BLOCKED!")
            print(f"   🛑 Reason: {res.json()['threat_details'][0]}")
            break # Stop attacking if banned
    except Exception as e:
        print("   [!] API unreachable.")
    time.sleep(0.5)

# STAGE 4: Verify Global IP Ban
print("\n[*] PHASE 4: Bot verifying if it can still access the website...")
time.sleep(1)
web_res = requests.get(f"{BASE_URL}/api/v1/check_ip")
if web_res.json().get('blocked'):
    print("❌ ACCESS DENIED! Bot IP is permanently BANNED from all pages.")
else:
    print("✅ Access Allowed.")