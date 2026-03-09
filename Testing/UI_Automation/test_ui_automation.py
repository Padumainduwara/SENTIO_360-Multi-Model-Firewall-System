from selenium import webdriver
from selenium.webdriver.common.by import By
import time

print("[*] SENTIO 360 - Starting Automated UI & Login Testing...")

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)

try:
    print("[*] Navigating to Admin Login Page...")
    driver.get("http://localhost:8000/admin/login.html")
    driver.maximize_window()
    time.sleep(2)

    print("[*] Entering Admin Credentials...")
    driver.find_element(By.ID, "username").send_keys("admin")
    driver.find_element(By.ID, "password").send_keys("admin123")
    time.sleep(1)

    print("[*] Clicking Login Button...")
    # 💥 මෙන්න වෙනස: කීබෝඩ් Enter වෙනුවට කෙලින්ම Button එක හොයලා Click කරනවා
    driver.find_element(By.TAG_NAME, "button").click()
    
    # ඩැෂ්බෝඩ් එක ලෝඩ් වෙනකම් තත්පර 4ක් ඉන්නවා
    time.sleep(4)
    
    current_url = driver.current_url
    if "index.html" in current_url:
        print("[SUCCESS] Login Successful! Dashboard loaded.")
        driver.save_screenshot("automated_login_and_uat_success.png")
        print("[SUCCESS] UI Screenshot automatically saved as 'automated_login_and_uat_success.png'")
    else:
        print("[ERROR] Login Failed. Redirect did not happen.")

except Exception as e:
    print(f"[ERROR] UI Automation failed: {e}")

finally:
    driver.quit()
    print("[*] Browser closed. UAT Automation complete.")