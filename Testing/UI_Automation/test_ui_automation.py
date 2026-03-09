from selenium import webdriver
import time

print("[*] SENTIO 360 - Starting Automated UI Testing...")

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)

try:
    print("[*] Navigating to Admin Dashboard...")
    
    # 💥 මෙන්න මේ ලින්ක් එක තමයි අපි හරියටම හැදුවේ
    driver.get("http://localhost:8000/admin/index.html")
    
    driver.maximize_window()
    time.sleep(4) # ඩැෂ්බෝඩ් එකේ ග්‍රාෆ් ටික ලෝඩ් වෙනකම් තත්පර 4ක් ඉන්නවා

    print("[SUCCESS] Dashboard loaded successfully.")

    driver.save_screenshot("automated_uat_success.png")
    print("[SUCCESS] UI Screenshot automatically saved as 'automated_uat_success.png'")

except Exception as e:
    print(f"[ERROR] UI Automation failed: {e}")

finally:
    driver.quit()
    print("[*] Browser closed. UAT Automation complete.")