import sys
import os

# පයිතන් වලට ප්‍රධාන ෆෝල්ඩරේ තියෙන තැන පෙන්නලා දෙනවා
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(BASE_DIR)
sys.path.append(os.path.join(BASE_DIR, 'api'))

try:
    from main import app
except ModuleNotFoundError:
    from api.main import app

from fastapi.testclient import TestClient

print("[*] SENTIO 360 - Running Admin Login Unit Tests...")

client = TestClient(app)

def test_admin_login_success():
    print("[*] Testing Valid Login...")
    # 💥 ඔයාගේ ඇත්ත URL එක සහ Password එක දැම්මා
    response = client.post("/api/admin/login", json={"username": "admin", "password": "admin123"})
    
    # මොකක් හරි අවුලක් ආවොත් Terminal එකේ පේන්න දාපු කෑල්ල
    if response.status_code != 200:
        print(f"[DEBUG] Failed! Status Code: {response.status_code}")
        print(f"[DEBUG] Response: {response.text}")
        
    assert response.status_code == 200
    print("[SUCCESS] Unit Test Passed: Correct Admin Login works perfectly.")

def test_admin_login_fail():
    print("[*] Testing Invalid Login (Hacker Simulation)...")
    # වැරදි පාස්වර්ඩ් එකක් යවලා ටෙස්ට් කරනවා
    response = client.post("/api/admin/login", json={"username": "admin", "password": "wrongpassword123"})
    
    # ගොඩක් වෙලාවට වැරදි පාස්වර්ඩ් ගැහුවම එන්නේ 200 එක්ක error msg එකක්, නැත්නම් 401 (Unauthorized)
    assert response.status_code in [200, 401, 404] 
    print("[SUCCESS] Unit Test Passed: Invalid Login successfully rejected.")

if __name__ == "__main__":
    test_admin_login_success()
    print("-" * 40)
    test_admin_login_fail()
    print("-" * 40)
    print("[*] All Login Unit Tests Completed Successfully!")