// target_website/firewall_guard.js
async function enforceFirewall() {
    try {
        // 1. Check for IP Bans
        const res = await fetch('/api/v1/check_ip');
        const data = await res.json();
        
        if (data.blocked) {
            document.body.innerHTML = `
            <div style="background-color: #0b0205; color: #ff4444; height: 100vh; display: flex; flex-direction: column; align-items: center; justify-content: center; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; text-align: center;">
                <svg style="width: 100px; height: 100px; margin-bottom: 20px;" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
                <h1 style="font-size: 50px; font-weight: 900; margin: 0; letter-spacing: 2px;">ACCESS DENIED</h1>
                <h2 style="font-size: 20px; color: #ff9999; margin-top: 10px;">CONNECTION TERMINATED BY SENTIO 360 FIREWALL</h2>
                <p style="font-size: 16px; margin-top: 30px; color: #aaaaaa; max-width: 600px;">Your IP address has been permanently blacklisted due to the detection of severe malicious activity (DDoS/Bot behavior or Disguised Malware). Further attempts to access this server will be reported.</p>
                <div style="margin-top: 40px; padding: 10px 20px; border: 1px solid #ff4444; color: #ff4444; font-family: monospace; font-weight:bold;">ERROR_CODE: SENTIO_L7_BLOCK</div>
            </div>`;
            return;
        }

        // 2. ADVANCED DATA SCIENCE: Dynamic Baseline Human Telemetry
        // Generate slightly randomized safe values to prevent Autoencoder over-fitting
        const maxLen = Math.floor(Math.random() * (180 - 100 + 1)) + 100;    // Between 100 and 180
        const avgSize = Math.floor(Math.random() * (110 - 70 + 1)) + 70;      // Between 70 and 110
        const variance = Math.floor(Math.random() * (25 - 5 + 1)) + 5;        // Between 5 and 25

        const safeTelemetry = JSON.stringify({
            "Destination Port": 443,
            "Max Packet Length": parseFloat(maxLen),
            "Average Packet Size": parseFloat(avgSize),
            "Packet Length Variance": parseFloat(variance)
        });

        const formData = new FormData();
        formData.append('text_payload', ''); 
        formData.append('behavior_json', safeTelemetry);
        
        // Silently send to AI Engine
        fetch('/api/v1/inspect', {
            method: 'POST',
            body: formData
        });

    } catch (e) { 
        console.log("Firewall Telemetry Sync Failed"); 
    }
}

enforceFirewall();